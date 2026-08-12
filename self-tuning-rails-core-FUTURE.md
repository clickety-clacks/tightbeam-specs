# Self-tuning core for tightbeam rails — discovery & recommendation (FUTURE PHASE)

Status: **NOT a spec.** A hand-off capture for a future design agent. It records what
was discovered (two reference systems) and the recommended shape, so the design phase can
start from conclusions rather than re-derive them. Authored 2026-07-20 during the
tightbeam kungfu/guidance work.

---

## 1. The need

Tightbeam has **rails**: deny-only / escalate TOML **statutes** the substrate enforces at
the dispatch chokepoint (deterministic law — a `deny` stops a verb, an `escalate` blocks
it on the owner). Today those rails are hand-authored.

The goal of this future phase: a **self-tuning core** that generates candidate rails from
real operating experience and hardens them safely into enforced TOML — so the factory's
own scar tissue becomes law without a human hand-coding every rule.

Two hard constraints make this different from ordinary "self-improving guidance":
- Rails are **fail-closed enforced law.** A wrong `deny` blocks legitimate work. So the
  bar to *promote* a candidate to an enforced rail is much higher than for advisory prose.
- Rails encode **operator preference** (per the tenet-vs-preference rule: universal
  SW-dev tenets are guidance; org-configurable rules are rails). So the *signal* must come
  from what the operator actually wants, corrected over time.

Two existing systems each solve *half* of this. Neither solves it whole. Tightbeam has the
piece both are missing (deterministic enforcement).

---

## 2. Reference system A — OASIS v2 (Flynn's openclaw self-improvement)

Source: https://clawline.chat/self-improvement-v2.html . Goal: behavioral lessons survive
agent compaction and compound, without stuffing transcripts into prompts.

**Four layers:**
1. **Raw signal capture** — append-only daily logs `memory/YYYY-MM-DD.md`, written at a
   pre-compaction "memory flush." A **14-bucket signal model**: attaboys, admonishments,
   friction patterns, preferences/boundaries, failure-mode signatures, success patterns,
   environment facts, retrospectives, **permission-signal flips** ("just do it" ↔ "don't
   do that without asking"), implementation details, locations, interests/synthesis,
   conversation summary, next-step recommendations. Short bullets, not transcripts.
2. **Analytical staging** — `tuning.md` (+ `sops.md`), read by Opus overnight only. The
   core data structure is a **principle**:
   ```
   - **P-012: Over-investigation before dispatch** [H:3 M:0 last:2026-02-22]
     Situation: … / Bad default: … / Better default: … / Check question: "Am I describing WHAT or telling HOW?"
   ```
   Stable ID `P-NNN`; **H** = times applied correctly; **M** = times the user had to
   correct something this principle should prevent; `last:` date; situation signature;
   bad/better defaults; a check question.
3. **Runtime imperatives** — `rules.md`, the ONLY behavioral file injected at every boot.
   Short command-only directives synthesized from principles; no counters/analysis.
4. **Durable environment** — `environments.md` (stable IDs, config).

**The loop:** boot loads `rules.md`+`environments.md` → runtime (corrections bump M) →
pre-compaction flush → **overnight synthesis (4:15 AM)** → daily rating (10:03 PM) → next
boot.

**Overnight synthesis (6 steps):** read inputs → update principles (match each
admonishment to a P-NNN, `M++`; new → create with `M:1`; attaboy → `H++`; 3+ misses →
strengthen check question; `M > H by 5+` → add structural intervention) → snapshot
`tuning.md` to `memory/tuning-history/YYYY-MM-DD/` → **synthesize `rules.md`** (imperative
directives, one section per principle with `M>0`, higher-miss → stronger; graduated SOPs
added) → conflict/duplicate scan → `tuning-conflicts.md` (human-reviewable, no auto-fix) →
report.

**Forcing functions** (counter-driven, human-confirmed actions): leave-alone / promote /
rewrite / strengthen / archive / shape-problem (high H AND M) / structural-tension.
**"No auto-execution. The agent proposes; the user confirms."**

**Gate:** human review of the conflict scan + a **daily 1–5 rating** correlated over time
(tuning Δ → rating Δ). **Enforcement: advisory** (`rules.md` is prompt context, not a hard
gate). **Rollback:** manual, no automated mechanism.

**OASIS's strengths:** cheap, interpretable, operator-aligned; the **H:M counters are a
clean "which rules aren't working" signal**; every principle carries provenance (its
situation/origin); compaction-survival is the design center (very tightbeam-relevant).
**Weaknesses:** the gate is weak for enforced law (human review + a noisy scalar rating);
synthesis is LLM-reasoning that can overfit recent noise; enforcement is advisory only.

---

## 3. Reference system B — Hermes (Nous Research)

Repos: `NousResearch/hermes-agent` (runtime) + `NousResearch/hermes-agent-self-evolution`
(the self-tuning engine, DSPy + GEPA). MIT.

**Key finding:** Hermes is stronger than soft-guidance injection, but NOT because it
hard-enforces synthesized prose. Two mechanisms:
1. **A hand-written deterministic runtime layer** (`tool_guardrails.py`): SHA256-hashes
   canonical tool args into a stable call-signature; counts exact-failure / same-tool /
   no-progress; returns `allow | warn | block | halt` (a circuit breaker). **Fixed rules +
   tunable thresholds — never self-modified.**
2. **Eval-gated PROMOTION** is what makes a *synthesized* rule real. **GEPA** (reflective
   genetic-pareto prompt evolution) + **DSPy** mine real **execution traces**, propose
   targeted mutations of skills/prompts/tool-code, and a candidate ships only after:
   **100% test suite (zero tolerance) → an independent benchmark the optimizer is forbidden
   to optimize against (regression auto-reject) → holdout scoring (anti-overfit) → git PR,
   human-reviewed, never direct commit.** Rollback = `git revert`. The synthesis act itself
   is scanned (injection/credential) and staged for approval.

**The transferable idea:** the **promotion gate makes a generated rule binding, not
runtime enforcement of prose.** Hermes's synthesized artifacts stay advisory; only its
human-gated code-evolution phase touches enforced code.

**Hermes's strengths:** a rigorous, objective, hard-to-game gate (independent benchmark +
holdout); trace-driven (learns from real failures); git-native rollback. **Weaknesses:**
heavy (full optimization runs, ~$2–10 each); no lightweight per-rule operator signal;
needs a good benchmark/eval-set (expensive to build); still advisory enforcement.

---

## 4. Comparison, and the rails-specific insight

| Axis | OASIS v2 | Hermes |
|---|---|---|
| Signal source | the *human's* corrections (attaboys/admonishments, permission-flips) | the *system's* execution traces (why runs failed) |
| Synthesis engine | LLM (Opus) over P-NNN H:M counters + hand-designed forcing functions | an optimizer (GEPA genetic-pareto + DSPy) searching candidate mutations |
| Gate | human review + noisy daily 1–5 rating | objective eval (tests + independent benchmark + holdout) + human PR |
| Enforcement | advisory (`rules.md` at boot) | advisory (+ a hand-written, non-synthesized breaker) |
| Rollback | manual | git revert |

**Essence:** OASIS's genius is the **signal + forcing-functions**; Hermes's genius is the
**promotion gate**. Both end at advisory prose.

**Why neither alone fits rails — the complementary-signal insight:**
- **OASIS detects false *negatives*.** `M` = "a rule that should have fired didn't; the
  operator corrected me." That's how you discover a rail is **needed**. A high-miss
  permission-flip ("don't do X without asking") *is* a `deny`/`escalate` candidate,
  provenance-stamped with its situation.
- **A Hermes-style eval detects false *positives*.** "Would this rule have wrongly blocked
  something the operator actually wanted?" — proven by **replaying the candidate rail
  against a corpus of past real decisions/traces** (a regression/holdout check). That's
  what proves it's **safe to enforce.**

Neither system has both. OASIS finds the need but can't prove safety (human-review + a
scalar is too weak to trust a deterministic gate). Hermes proves safety but has no
lightweight per-rule need-signal from the operator. **Rails require both**, precisely
because they are fail-closed.

---

## 5. Recommendation: a synthesis, with tightbeam as the missing piece

**OASIS is the candidate engine. A Hermes-style eval is the promotion gate. Tightbeam's
rails are the enforcement target that closes the loop neither system closes.** A
**graduated hardening path** for every candidate rail:

1. **Signal (OASIS-style).** Operator corrections → principles with H:M. A principle that
   is a hard "don't / ask" with rising misses is a rail candidate, carrying its origin.
2. **Advisory first.** The synthesized rule ships as **guidance** (OASIS `rules.md`-style):
   accumulate hits, keep receiving the false-negative signal. It is not yet enforced.
3. **Promotion gate (Hermes-style, dogfood tightbeam).** To harden a candidate from
   advisory guidance → an **enforced `deny`/`escalate` TOML rail**, it must pass an
   objective gate: **replay against historical decisions to prove a low false-positive
   rate** (it would not have blocked legitimate work), plus a human ruling. Run that gate
   **through tightbeam's own check-tier** — the eval produces **verdict facts** that gate
   the promotion (eval-gated promotion, on our own substrate).
4. **Enforcement (tightbeam).** The survivor becomes a deterministic rail — a
   **self-synthesized operator-preference promoted to law.** OASIS ends at advisory; Hermes
   ends at advisory-plus-a-breaker; **tightbeam is the only one of the three where a mined
   rule can become enforced without a human hand-coding it.**

The one-line answer to "OASIS, Hermes, or a synthesis?": **synthesis** — OASIS's signal +
Hermes's gate + tightbeam's enforcement, with rails **earning** enforcement through a
false-positive eval rather than being born hard.

---

## 6. Tightbeam-native reshaping (how the pieces map onto substrate we have/are building)

Don't port OASIS's markdown machinery; re-express it on tightbeam primitives:
- **Signals → facts.** The daily-log / `tuning.md` capture becomes **attested facts** in
  the substrate (attest tier). H:M counters are **derived from fact history**, not stored
  markdown. Each principle's origin is real provenance (the attest chain).
- **Overnight synthesis → a recurring wake.** The 4:15 AM Opus run becomes a **recurring
  wake** (the deferred recurring-wake capability) firing a synthesis agent.
- **The promotion gate → the check tier.** The false-positive replay/eval runs through the
  same spec→review→build→review pipeline and emits **verdict facts**; a rail is only
  promoted when a `verdict:safe-to-enforce` fact exists. This dogfoods the check tier.
- **Enforcement → the rails/statute engine** (already built). The TOML is generated, then
  gated, then loaded.
- **Escalation ties in:** a candidate that's ambiguous escalates to the operator (the
  escalation-substrate + escalation-policy work) — the operator's ruling is a fact that
  either promotes or rejects it. This whole loop *is* escalation-policy's first customer.

---

## 6b. Rule shape: enforceable rail vs. teachable prose (one loop over both)

The first question for any candidate is **"is this enforceable, or only teachable?"** —
can it be expressed as a mechanical predicate over what the substrate observes (a verb,
its args, the caller, the facts)?
- **Rail-able** (mechanical predicate): "no merge to main without a ruling fact," "don't
  spawn on host Z," "escalate a subsystem de-scope." → a deterministic rail. Once
  translated, the rail **supersedes** prompt/guidance evolution for that lesson (keep at
  most a one-line orientation so the agent isn't surprised by the deny). No further
  prose-tuning needed — the substrate enforces it.
- **Not rail-able** (judgment/behavior): "describe WHAT not HOW when dispatching," "smoke
  against reality before done," "read before you change." There is no fact to check;
  enforcement is impossible. These stay **advisory prose**, and prose-evolution
  (GEPA-style) is the ONLY lever.

So rails and prose-evolution are **not redundant — they cover different classes of
lesson.** Rails retire prompt-evolution for the checkable ones; guidance-evolution remains
the only tool for the judgment ones.

**The translation lesson→TOML is itself fallible, and the same loop re-translates it.** A
candidate rail can be wrong three ways: **over-broad** (false positive — denies legitimate
work), **under-broad** (false negative — misses cases; the bad thing recurs), or **wrong
predicate**. Each surfaces as a hit/miss signal *on the rail*: a false positive = the
operator overriding a deny; a false negative = the original lesson recurring despite the
rail. Both feed the SAME reflect→propose→eval loop — but the artifact mutated is now TOML,
not prose ("this deny fired on something wanted → propose a narrower predicate → re-run the
false-positive eval → replace the rail").

**Net:** the self-tuning core is **one loop over a spectrum of artifact types** — prose for
judgment lessons, TOML for enforceable ones — where the eval gate decides both whether to
promote a lesson to enforcement and whether a re-translation improved the rail.
Prompt-evolution and rail-translation are the same loop pointed at whichever encoding a
lesson belongs in, re-encoding when the encoding is wrong.

## 6c. Level of effort (how hard are the Hermes-style techniques?)

Short answer: **straightforward-to-moderate orchestration loops — NOT like training an LLM,
and NOT like building a formal constraints solver.** No GPUs, no fine-tuning, no SAT/
formal-methods engine. Cost and risk concentrate in ONE place: the eval corpus + metric.

- **`tool_guardrails` circuit breaker** — TRIVIAL (~a day): hash canonical args, count
  failures, threshold to allow/warn/block/halt. Tightbeam may not even need it — supervision's
  prod-ladder already handles no-progress loops.
- **DSPy (framework)** — DON'T adopt wholesale (would mean restructuring agent LM calls
  into DSPy programs; wrong fit for ACP/harness sessions). BORROW the concept — a call's
  typed input→output **signature** + validate-the-output-and-retry. LOW to borrow.
- **GEPA (optimizer)** — the ALGORITHM is straightforward: trace → LLM reflects on why it
  failed → proposes a targeted text edit → keep it if it scores better (Pareto frontier).
  LLM-in-the-loop search, NOT novel ML (no training, no gradients, no solver); off-the-shelf
  LLM as the reflection engine (~$2–10/run). LOW-MODERATE; tightbeam is built to run it
  (a synthesis agent on a recurring wake).
- **Rail-translation (lesson → TOML)** — MODERATE: an LLM generation task constrained to
  the statute grammar; output must be a valid, loadable rail (validate-and-retry, like a
  DSPy signature).
- **Eval-gated promotion** — pipeline mechanics (tests, benchmark, holdout, human ruling)
  are EASY. **The hard, ongoing part is the EVAL CORPUS + METRIC** — a representative,
  un-gameable set of real decisions to replay a candidate rail against. A DATA-CURATION
  problem, not an algorithm problem. This is where the budget goes.

Two things make rails MORE tractable than general self-improvement:
1. **The metric is concrete** — "false-positive rate against history" (did this rail deny
   something the operator actually did/wanted?) beats Hermes's fuzzy task-success metric.
2. **The corpus is native** — the substrate's event/attest log is the raw material,
   though labelling it (what SHOULD have been denied vs allowed) still needs curation.

The enforcement engine (statutes/rails) already exists. Net build = an LLM synthesis loop
(moderate) + rail-translation-with-grammar-validation (moderate) + a replay eval harness
and its corpus (the real cost, mostly curation).

## 6d. Reusing Hermes (it's MIT — what to steal, what won't transfer)

Hermes is MIT — legally reusable. But most of the cost doesn't live in code you can lift,
so the recommendation is **"read Hermes, lift the algorithm + the eval-gate structure, and
build the thin tightbeam-native version around our own corpus" — NOT fork the codebase.**

**Worth taking:**
- **GEPA the optimizer** — a published algorithm with an open implementation (also
  available through DSPy). Lifting it removes the "reinvent the reflection loop" work.
- **The eval-pipeline scaffolding as a reference template** — `benchmark_gate.py`,
  `fitness.py` (LLM-as-judge rubric), `constraints.py`, `pr_builder.py`,
  `dataset_builder.py`. The *structure* of score→gate→holdout→PR is a good starting shape.

**What does NOT transfer (and it's exactly the expensive stuff):**
1. **Python + DSPy vs. Elixir/BEAM.** Can't drop Hermes into the substrate. Best case the
   evolution engine runs as a **separate Python side-tool** that reads tightbeam data and
   emits candidates (fine — synthesis is an offline batch, not substrate code), but that's
   integration glue, not clone-and-go. Forking a whole Python agent framework into our
   Elixir substrate is more pain than value.
2. **The corpus and metric are Hermes's own, and useless to us.** Their `dataset_builder`
   mines *their* SessionDB + golden sets; their fitness is *their* task rubric +
   TBLite/YC-Bench. Ours is: operator-corrections-about-rails as signal, false-positive-
   rate-of-a-deny-against-real-decisions as metric, the substrate event/attest log
   (labelled for should-deny) as corpus. **None of that ships with the repo — and it's the
   long pole.** Stealing Hermes shaves zero off the corpus.
3. **The tightbeam-specific half is ours regardless** — rail-translation to TOML
   constrained to the statute grammar, and enforcement. Enforcement we already have (the
   rails/statute engine); Hermes has NO equivalent (its synthesized rules stay advisory —
   the whole reason we're doing this).

**Net effect on the estimate:** lifting GEPA + the pipeline structure trims maybe a couple
weeks off the MVP's loop mechanics. It moves **neither** critical-path item — the corpus
curation (the real long pole) or the tightbeam glue. Consistent with §6c: the algorithm was
never the expensive part. The reusable asset is the **design + the optimizer**, not the
codebase, because the codebase is a Python agent for a different domain and the costly parts
(our data, our metric, our enforcement) are things only we can supply.

## 6e. Exogenous ground truth (the anchor requirement)

The fact economy the tuning loop consumes — attestations plus judge verdicts — is entirely
**internal**. A gate never verifies truth, only provenance; independence protects against
*author bias*, not against *shared drift from reality*. Under optimization pressure (agents
adapting, and this tuning loop itself), the internal signals degrade together: producers learn
what judges pass, facts inflate, and the loop cannot detect it because it tunes on the same
facts. A dedicated external reviewer IS more trustworthy than the author — its only job is
fault-finding, with no attachment to the choices — but it is still inference inside the same
economy, with model-family blind spots.

**Empirical case (2026-07-20, this repo):** the derived-model-catalog change passed a
two-round cross-model review AND a green test suite, then failed in production three ways.
Independent inference review is not ground truth.

**Producer-strength ladder** (weakest → strongest): self-attested < independent judge <
independent mechanical producer (build, real run — reality touches it) < exogenous
verification (operator, production). Judges are the workhorse for judgment qualities;
mechanical and exogenous producers anchor "it actually works."

**Requirement for this system:** the tuning corpus MUST include exogenous signals — operator
verification outcomes, production failures, and **sampled re-verification of judge-passed work
against reality**. A judge-passed item that fails reality is a *finding about the judge* and a
first-class tuning signal (it calibrates the judges, not just the rails). Without this anchor,
the loop is closed on its own outputs and the fact economy inflates undetectably.

## 6f. Design lineage: institutional expectations register

This system is institutional design in the Searle sense — evidence that "counts as"
completion (attestations = institutional facts), gates as permits, judges as inspectors, the
turn-end sweep as audit. Institutions are the battle-tested answer to coordinating unreliable
agents at scale: make the *workflow* deterministic without pretending the *minds* are.

The analogy holds only after translation to agent terms. Reviewers are spawned fresh per
review and retired after; there is no persistent inspector to soften, fatigue, or be captured.
Statelessness is structural incorruptibility — fresh-spawn provides what human institutions
need rotation and audit to approximate. The persistent-inspector failure modes (rubber-stamp
drift, inspector capture) therefore do not exist in this design.

The failure modes that do exist, what each looks like, and what each needs — future work
reviews outcomes against this register the way completion is reviewed against the roadmap:

- **Static blind spots** — a frozen model family misses the same category on every fresh
  spawn; resampling the distribution resamples the holes. Watch: pass rates and escaped-defect
  categories diverging by judge model family. Need: cross-model diversity (already the rule) +
  the §6e exogenous anchor for blind spots the families share.
- **Checkbox compliance** — producers satisfy the letter of a gate while defeating its spirit
  (minimal smoke that exercises nothing, tests written to pass). Watch: gate-passed work
  failing exogenous verification. Need: the §6e anchor.
- **Persistent-side adaptation** — sessions are ephemeral, but guidance, the tuning corpus,
  and producer patterns persist and evolve; adaptation pressure lives there, drifting toward
  what a judge family's static blind spots pass. The tuning system must not amplify this loop.
  Watch: the §6e calibration signal. Need: exogenous ground truth in the tuning corpus (§6e).
- **Meta-rule capture** — pressure accumulating on the rules-about-changing-rules. Need: the
  meta-rail split (changes to who-may-change-rails escalate to the operator) — already
  designed.

## 6g. Remedy rate: the automatic guidance eval

The rails give the tuning system a metric neither reference system has. Guidance teaches the
fast path (produce the evidence before the boundary); the gate checks; the remedy fires only
when teaching failed. Every gated outcome is therefore an unlabeled trial of the guidance,
generated by real work at zero labeling cost.

- **Unit:** a gated outcome — a boundary verb (complete/merge) or turn-end sweep on work
  subject to rule R.
- **Metric:** remedy rate `RR = remedies fired / gated outcomes`, sliced by rule, archetype,
  model, and **guidance version** (the identity-repo SHA the session ran under — guidance
  changes are commits, so every version is addressable).
- **Guidance eval:** a guidance commit is a treatment; RR before/after the commit, same
  slices, scores the prose change. This supplies the concrete objective metric Hermes lacks
  for prose (its task-success rubrics are fuzzy): "did the rewrite work" = "did the backstop
  rate drop."
- **Diagnosis by slicing:** RR high across all models → the prose is unclear or missing. RR
  high only for weaker models → capability, not guidance. RR high on one rule only → that
  lesson is not landing (per-lesson granularity — OASIS's per-principle M counter,
  mechanized).
- **Secondary metrics:** first-pass-clean rate (review returns clean on the first attempt —
  rates the content guidance, not just process-following); time-to-evidence (evidence produced
  proactively vs. at the boundary); denied-then-overridden (rates the rail, not the guidance).
- **Guard pairing:** RR alone Goodharts into checkbox compliance (perfunctory evidence to
  dodge the remedy). RR is always read next to downstream quality — verdict outcomes and the
  §6e exogenous anchor. Improvement = RR down AND escaped defects flat-or-down.

Division of signal labor in the synthesis (§5): for railed lessons, RR replaces the operator's
M counter — automatic, dense, no human in the loop. Operator corrections (OASIS) remain the
only signal for the advisory residue, where there is no gate to measure. Replay evals (Hermes)
remain the promotion gate for rail false positives. The enforcement layer thereby becomes the
evaluator of the teaching layer: guidance teaches, rails measure, tuning rewrites, RR
validates the rewrite.

---

## 7. Open design questions for the future agent
- **The false-positive corpus:** where does the "history of real decisions/traces" to
  replay against come from? (Tightbeam's event/attest log is the natural source — is it
  rich enough? does it record the would-be-denied actions?)
- **H:M on facts:** exact derivation of hit/miss from the fact stream — what counts as a
  hit (rail correctly matched an action the operator wanted stopped) vs a miss (operator
  corrected something a candidate should have caught)?
- **Advisory→enforced threshold:** what accumulated evidence (min hits, max false-positive
  rate on the replay, min age) gates the harden step? These are themselves org-tunable.
- **Scope of a synthesized rail:** deny/escalate on which fact predicates? The rail grammar
  the generator can emit (must stay within what the statute engine supports — see
  codex-gates/statute-engine; PreToolUse is deny-only, allow/rewrite is vendor-blocked).
- **Rollback:** git-native (like Hermes) vs a substrate "retire this rail" verb + provenance.
- **Does OASIS's daily 1–5 rating survive?** It's a weak signal; likely replaced by the
  objective replay-eval for rails, but may stay as a coarse health metric.
- **Relationship to Flynn's existing self-improvement system** (he has one he'll adapt to
  tightbeam) — this doc is input to that adaptation, not a competitor.

---

## 8. References & glossary
- OASIS v2: https://clawline.chat/self-improvement-v2.html
- Hermes: `NousResearch/hermes-agent`, `NousResearch/hermes-agent-self-evolution` (MIT).
- **DSPy** — a framework for *programming* (not prompting) LMs: LM calls are modules with
  typed input→output signatures; the prompt strings + few-shot examples are **parameters an
  optimizer tunes against a metric**. "Prompts as weights you compile."
- **GEPA (Genetic-Pareto)** — a *reflective prompt-evolution* optimizer (ICLR 2026):
  **genetic** = evolves prompt candidates by mutation; **Pareto** = keeps a *frontier* of
  candidates (each best on some task subset) to avoid local-optimum collapse; **reflective**
  = reads execution **traces** (natural-language "why it failed") to propose *targeted*
  mutations — far more sample-efficient than RL because it learns from textual failure
  signal, not a scalar reward.
- Related tightbeam specs: escalation-substrate-v1 (the `escalate` gate outcome),
  the statute/rails engine, check-tier (verdict facts), attest (provenance),
  agentic-engineering-kungfu-plan (where advisory guidance vs rails live).
