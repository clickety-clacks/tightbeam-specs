# Rails + Guidance — implementation roadmap (beginning to end)

**NON-LOAD-BEARING.** This is a tracking document: phases, checkboxes, sequencing. The
authority for every decision and design is its SPEC; dated ruling provenance lives in
`tightbeam-decisions.md`. Where this document and a spec disagree, the spec wins. Nothing may
have this document as its only home.

Purpose: a single, completion-reviewable plan from the current code state to the full
enforcement model and guidance we designed. Each phase states a **Goal**, a **Deliverable**,
**Done** criteria (checkable), **Depends on**, and the **Spec** that defines it. Check the boxes
as phases land. Ground truth for the baseline was read from `rails.ex`, `rules.ex`,
`dispatch.ex`, and `archetypes.ex` on `main` at `8aec21b`.

Related specs — this roadmap is the guide; these carry the detail it points into:
- `agentic-engineering-guidance-spec.md` — the guidance content (§2–§5) and the enforcement
  model (§6): the evidence-not-behavior principle, the red-tape test, producer strength, the
  sync-check/async-judgment split, the reviewer-loop worked example, and the **enforcement
  mapping** (rule → mechanism → edge → strength) that P1, P2, and P7 execute against.
- `self-tuning-rails-core-FUTURE.md` — the horizon after P7 (track T-B): §6e **exogenous
  ground truth** (the anchor requirement), §6f the **institutional expectations register**
  (the failure modes future outcomes are reviewed against), §6g **remedy rate** (the automatic
  guidance eval fed by the cross-cutting observability requirement below).

---

## End state (what "done" means)

The enforcement model as discussed, fully implemented, plus the guidance authored and loaded:
- Rails are **contained, value-returning checks** (mechanical or judge-delegating), gating verbs
  at **two edges** — the dispatch verb (commission) and the **turn-end sweep** (omission).
- Fact-gates key on **provenance-stamped facts**, strongest when produced by an **independent
  actor** (reviewer verdict, build result, smoke run).
- Gates carry **remedies** (spawn/wake/assign) so the substrate originates the producer — the
  agent cannot skip, ship-dirty, or leak the producer.
- Every rail invocation is **legible**: recorded, and every non-pass emits a self-naming fact.
- The substrate/product boundary holds: the **agentic-engineering kungfu** (guidance + skills +
  rails TOML + scripts) is a portable bundle loaded from the git-backed `identity/` repo; the
  substrate ships only mechanism.

---

## Cross-cutting requirement — observability rides every phase

Every enforcement mechanism emits its events **in the phase that builds it**, not in a later
observability pass: gate evaluations that deny, remedies that fire, sweep triggers, script
non-passes. Rating is **derived, never stored** — queries over the event log (backstop rate
per agent/archetype/model, firing rate per rail, remedy outcomes, denied-then-overridden),
so the tuning system (T-B) inherits a corpus as old as the rails themselves. **Remedy rate** —
remedies fired per gated outcome, sliced by rule, archetype, model, and guidance SHA — is the
automatic guidance eval (FUTURE §6g); these events are its corpus. A phase whose mechanism
acts invisibly is not Done.

---

## P0 — Baseline (DONE)

Goal: record the starting line so later phases are reviewable against it.

- [x] Guidance/archetype/skill loading from `identity/` (git-backed as of `8aec21b`).
- [x] `tightbeam init` + attributed skill-verb commits (every guidance mutation is a tracked,
      caller-attributed git commit; only change path is edit-in-repo → commit → restart).
- [x] `rules.ex` — dispatch-chokepoint **deny-only** verb statutes; **closed, typed fact
      registry** (`@facts`) with fail-closed-on-unknown; includes **check-tier verdict facts**
      (`assignment.verdicts`, `attest.kind`, `assignment.caller_is_holder`).
- [x] `rails.ex` — harness **PreToolUse command matchers** (tool + POSIX-ERE → refuse), compiled
      into claude `settings.json` / codex `hooks.json`, boot-proven via the wiring probe.

Not yet built (the rest of this roadmap): scripts, remedies/active gates, dedicated-judge gates,
the turn-end edge, `allow`/`escalate` effects, and several flagship observables.

---

## P1 — Author the guidance (no engine work)

Goal: the guidance spec becomes real files the existing loader reads. This is authoring, not
engine work, and it is immediately useful.

Deliverable: the substrate operating manual (ships in-binary), and the engineering kungfu in
`identity/` — engineering tenets, five archetype files (orchestrator, spec-writer, coder,
reviewer, recon), and the skills manifest.

Done:
- [x] Each §2–§5 `CONTENT` block from the guidance spec exists as its target file (manual
      in-binary at `24540dd`; kungfu seeded in the live org's identity repo at `effe0c0`).
- [ ] A session electing each archetype receives exactly that archetype's guidance (smoke: spawn
      one session per archetype, confirm loaded guidance).
- [x] Guidance-spec §6 carries the enforcement model: the evidence-not-behavior principle, the
      red-tape test, producer strength, and the enforcement mapping (rule → mechanism → edge →
      strength).
- [x] Guidance-spec §6 gains the two remaining passages: the turn-end sweep as a first-class
      firing edge, and review-of-guidance-changes as an opt-in org policy, default off. §1
      gains the mapping of bundle paths onto the current identity-repo layout.

Depends on: P0. Spec: `agentic-engineering-guidance-spec.md`.

---

## P2 — Author the rails expressible today

Goal: ship the rails the current engine already supports, so the enforcement layer starts
covering real rules before the engine grows.

Deliverable: harness command matchers for the containment-lite rules (no destructive
git — stash/reset/clean/checkout/restore; writes outside own worktree), and dispatch
deny-predicates over **existing** facts (admin-only verbs; verdict-present gates over
`assignment.verdicts`).

Done:
- [x] Rails/rules TOML authored, loads clean, fires (5 destructive-git gate statutes proven
      both directions against tool-call JSON; dispatch rules honestly empty — every §6
      candidate verified inexpressible over today's fact registry, blocked on P3).
- [x] Each authored rule maps to a row in the §6 enforcement mapping.
- [x] Every authored rail passes the §6 **red-tape test** criteria available at this phase:
      silent when satisfied, evidence as a byproduct, outcome verbs only. The
      remedy-before-deny criterion applies from P5, when remedies exist. (Two documented
      accident-grade over-matches kept deliberately: `git stash list/show` excluded by
      pattern; `git restore --staged` matched, commented in the TOML.)
- [x] **Backstop counting works**: `backstop-query.md` runs against the events table
      (dispatch appends `verb`/`denied` events; counts by rule/caller/verb).
- [x] **Harness-tier gap recorded**: PreToolUse gate firings happen inside the harness and
      leave no substrate event. Design note filed (adapter scrapes `[gate: <name>]` refusal
      markers from the session stream and appends events); implementation may land here or
      ride P4.

Depends on: P0. Spec: `agentic-engineering-guidance-spec.md` §6, `rails.ex`, `rules.ex`.

---

## P2.5 — Enforcement conformance smoke set (the engine's executable spec)

Goal: a graded conformance suite spanning every rail class — classes with existing machinery
run green now; P3–P7 classes are authored now and sit pending, and a phase is Done when its
class goes green.

Deliverable: a smoke-set spec (class taxonomy C1–C7 + a capstone reviewer-loop scenario),
fixtures mined from the assembled guidance (§6 enforcement mapping, tenets, the shipped
statutes' proven refuse/pass cases), a data corpus format reusable by the tuning system, and
a committed runner. Every class carries negative fixtures (compliant work passes silently)
and legibility assertions (each denial produces its named reason and event row). Script-guard
fixtures (C5) cover the fail-closed matrix: pass, fail, timeout→deny, out-of-set→deny,
crash→deny, containment-escape→deny.

Done:
- [x] Smoke-set spec written and reviewed **READY-FOR-IMPLEMENTATION** with the trio
      (2026-07-21; 66 fixtures, 13 green / 53 pending; representativeness attested through
      eight ensemble rounds).
- [ ] Runner committed; C1–C3 fixtures green on main; C4–C7 + capstone authored, pending.
- [ ] Shipped-statute corpus is a regression test (last night's proofs made durable).
- [ ] Claude-side hook wiring check exists or its absence is justified in the spec.

Depends on: P2. Gates: P3–P7 Done criteria reference their smoke-set class.

## KP1 — Kungfu pattern: model adjudication (parallel track)

> **AMENDED 2026-08-12 — this phase's mechanism is CANCELLED as written.**
> Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`).
> The substrate owes truth + a named failure + a record — no adjudication
> wake, no swap seam, no hold. Model policy lives in guidance, acted on by
> agents. The open checklist item below dies with it. See `adjudication-deletion-amendment.md`.

Goal: choosing the mind for a job is inference at EVERY decision edge — spawn, and each
classified failure (quota, unavailability, auth, boot) — guided by org-authored
characterizations (model-selection.md), the archetype's declared model preferences (a prior,
never a substrate-walked chain — `model_preferences` (né `fallback_models`) is preference data), and live state. The
substrate ships mechanism only: classification, classified refusals, routing a failure edge
to the owner's inference (an adjudication wake), the serialized swap seam, catalog freshness,
and the fail-loud floor. A quality-floor BLOCK is a legitimate recorded outcome; its exit is
a condition wake (S1), with timed fallback. Spec: model-ringdown-pattern.md (retitled the
model-adjudication pattern).

Done:
- [x] Recon report on `fallback_models` (display-only today) + error surfacing (unclassified).
- [x] Adjudication pattern spec reviewed **READY** (2026-07-21, 11 rounds of cross-model
      adversarial review; model-ringdown-pattern.md + the catalog freshness amendment).
- [ ] Substrate gaps implemented per the spec's gap list (classification, catalog validation
      + freshness, wake-owner routing, swap seam, usage-gauge investigation).

## G1 — The manual is the patterns (Flynn ruled, 2026-07-21)

The always-on substrate manual IS the operating-patterns document: each section a pattern
(situation → the move) with one exemplary command; mechanics are discoverable via
`tightbeam --help` and are not the manual's job. No separate idioms artifact. The capture
pipeline: every ratified spec answers "what pattern does this teach?" — none, or a manual
amendment landing with the spec (enforced via the spec-writer/reviewer guidance; operational
rediscoveries in transcripts are tuning signal for the same file). Patterns for unshipped
machinery are forbidden — the manual never teaches commands that do not exist.

Done:
- [x] Principle recorded in guidance-spec §2 instruction + the manual's intro points at
      --help.
- [ ] Pattern batch lands WITH S1/E1 shipping (wait-is-one-shape, block-with-a-record,
      judgment-becomes-a-fact, adjudicate-at-edges) + flag-enumeration trim, as ONE Sol
      manual-sync lane — deferred until those capabilities exist.
- [ ] The ratification question wired into spec-writer/reviewer guidance.

## E1 — Escalation ratification (Flynn ruled, 2026-07-21; revision in flight)

The four open questions are ruled: escalation is a RESUME — a slow dependency inside the
raising agent's assignment (it parks on a condition wake for the decision fact and continues
on ruling; the substrate never auto-replays; execute-once). No blocked-on-owner state or flag
exists — legibility is the open decision-request fact + the waiting assignment; an
orchestrator may retire an overtaken waiter, which auto-withdraws its requests. Rulings are
per-request, plus the WAIVER form ("ignore that rule for now"): a recorded fact scoped to the
raiser's lifetime or explicit revoke — and every waiver is a §6g false-positive datapoint for
the tuning loop. The raiser may withdraw its own requests, recorded, never silent.

Done:
- [x] escalation-substrate-v1.md rewritten to the ruled model, reviewed **READY** (2026-07-21,
      6 rounds: resolve/escalate/consume seam, four-shape union, consumable rulings, waivers,
      raiserId, concurrent-open index).
- [x] The rails `escalate` outcome unblocks at implementation (the review landed clean — the
      load gate's condition is satisfied); org escalate-rails become authorable once P4/P5
      ship the engine.

Depends on: S1 (the condition-wake primitive is the wait mechanism).

## S1 — Substrate: wake-on-fact (condition wakes)

Goal: a wake can be due on a CONDITION, not only a time — "wake me when a fact matching P is
filed." One primitive unifying gates-awaiting-verdicts, parked blocks awaiting quota, remedies
awaiting producers, and external-event smart wakes (the restate-lineage functionality, landed
as a fact-stream subscription instead of an external system).

Deliverable: the wake table gains a due-on-fact form (literal pattern match, no predicates —
consistent with the engine doctrine); substrate-produced condition facts for conditions the
substrate observes, first among them `quota-recovered(harness)` (pairs with KP1's
classification/gauge gaps — the substrate owns the harness integration, so no org script
polls for it); kungfu scripts/producers file condition facts for conditions the substrate
cannot see. INVARIANT: delivery is not resumption — the substrate never auto-resumes parked
work; the woken agent re-adjudicates (inference at every edge). Permanent-block stays a
supported policy by construction: it is simply not subscribing.

Done:
- [x] wake-on-fact spec written and reviewed **READY** (2026-07-21, 7 rounds:
      wake-on-fact-v1.md — condition wakes, creatorSessionKey, CAS-gated firing with
      cause-at-CAS, fact-ordered bounded scheduling, quota-episodes).
- [ ] Implemented; a parked block exits via condition subscription (timed fallback remains
      available).
- [ ] `quota-recovered` filed by the substrate on observed recovery; a subscribed wake
      delivers; the woken agent re-adjudicates rather than auto-resuming.

Depends on: KP1 gaps 1/6/7 for the quota condition; the primitive itself is independent.

## KP2 — Kungfu pattern: template kungfu + author guide (parallel track)

Goal: writing a good kungfu is taught by structure. Deliverable: (a) a TEMPLATE KUNGFU — a
skeleton bundle (guidance/, archetypes/, skills/, rails/ + scripts/, producers.toml,
preference data) whose placeholder content teaches what belongs in each file, what makes it
good (red-tape test, evidence-not-behavior, characterization format, corpus convention), and
what must not appear (substrate-mechanism restatement, per P9) — and which LOADS CLEAN, so
the structure is executable pedagogy (`tightbeam init --template`); (b) a writing-kungfu
AUTHOR GUIDE, assembled from the author-facing material already in the guidance spec (§6
sections, separation rules, skills style rules, enforcement-mapping method). Assembly-weight,
not design-weight.

Done:
- [ ] Template bundle exists, loads clean, seeds via init.
- [ ] Author guide written; a new kungfu author needs no other document to start.

## D1 — Decision: enforcement-substrate direction (before P3)

The current engine is closed-predicate. The design leaned toward **scripts**. Choose the spine:
- **A. Extend-predicate** — keep the closed algebra; grow the fact registry + add remedies +
  turn-end. Auditable/terminating, but every new observable is substrate work.
- **B. Scriptable-pivot** — contained value-returning scripts subsume predicates; scripts
  compute their own observables, so the registry stops growing. Maximally expressive; trades
  static auditability for runtime legibility.
- **C. Hybrid (recommended)** — keep the predicate engine as the fast, static, always-on path
  for trivial hot-path checks; add scripts for everything else. Registry grows only for the
  handful of hot mechanical checks.

Ruling: **C — hybrid** (Flynn, 2026-07-21, via the conformance-smoke-set directive requiring
script execution in guards). Predicates remain the always-on hot path; scripts are added.
Much of P3 becomes script-computed rather than registered; §6 stands as written.

---

## P3 — Fact / observable + producer layer

Goal: make the flagship deny-gates *expressible* by giving the substrate the observables they
need. (Under D1=B/C, the pure-mechanical ones move into scripts; the **producer** facts below
are still real substrate work either way.)

Deliverable, the flagship observables/producers:
- [ ] **Verdict-author independence** — a fact distinguishing the verdict's author from the
      work's producer (enables "reviewer ≠ implementor", cross-model). *Not expressible today.*
- [ ] **Review-of relation** — a verdict names the producer assignment it covers, so the
      independent-review predicate keys on the link rather than on work-item co-membership
      (guidance ships the subject convention `review of assignment <id>`; this makes it a
      substrate relation).
- [ ] **Build producer** — a `tests-passed` fact emitted by the build, not self-attested.
- [ ] **Smoke producer** — a `real-run-passed` fact emitted by a real run against real inputs.
- [ ] **Files-touched** — the file set an assignment touches (for order-same-code + worktree
      overlap).

Done:
- [ ] Each observable is registered/typed (or script-computed per D1) and correctly produced.
- [ ] The **deny half** of independent-review, tests-pass, and smoke gates is expressible and
      proven (deny the verb when the required independent fact is absent).

Depends on: D1. Spec: `agentic-engineering-guidance-spec.md` §6 (enforcement mapping).

---

## P4 — Script effect (contained, value-returning)

Goal: rails can run scripts. The pivot from closed-predicate to scriptable enforcement.

Deliverable: a statute may name a script whose check runs **inside containment**, returns a
value from a **declared set**, and gates the verb; **fail-closed** on error, timeout, or
out-of-set; every invocation **recorded**, every non-pass emits a **self-naming fact**.

Done:
- [ ] A TOML statute names a script; the script runs contained and gates the verb.
- [ ] Sync checks are time-boxed (pathology detector); async judgment is **not** time-boxed —
      the gate is an instantaneous fact-existence check, the judgment is an unbounded supervised
      session.
- [ ] A failed/hung/out-of-set script denies and produces a legible fact (which rail, which
      dispatch, why).

Depends on: D1 (=B/C). Spec: `agentic-engineering-guidance-spec.md` §6.

---

## P5 — Remedies / active gates

Goal: an unsatisfied gate originates its producer instead of only denying.

Deliverable: a statute carries a **remedy** (spawn/wake/assign). On an absent required fact, the
substrate creates the producer (e.g. a reviewer session), blocks the verb, and the produced fact
releases it. Remedy is **idempotent** (no double-spawn if a producer is already in flight).

Done:
- [ ] A gate with an absent fact spawns the required producer, blocks the verb, and self-releases
      when the fact lands.
- [ ] Re-running the verb with a producer already in flight does not spawn a second.
- [ ] **Rail-set satisfiability** checked at load: every gated verb has a reachable producer
      chain under the full statute set — no gate whose remedy or producer is itself denied by
      another statute (e.g. a review gate whose reviewer-spawn a quota rail forbids). A
      jointly-unsatisfiable set is rejected at load, loudly; single-statute validation cannot
      catch this.

Depends on: P3, P4. Spec: `agentic-engineering-guidance-spec.md` §6.

---

## P6 — Turn-end sweep edge

Goal: catch omission — the agent that finishes and idles without attesting.

Deliverable: the sweep is a step inside Supervision's terminal-edge evaluation (one
adjudicator — no separate GenServer, no race). Trigger = open obligation + no SELF-scheduled
continuation wake + idling. The obligation's gates are dry-evaluated (`Rules.decide`); a
remedy decision **runs the remedy** at most once (remedy XOR prod); an escalate decision
opens the decision-request and **parks the holder** (escalation-substrate-v1 owns the text);
any other unsatisfied outcome **re-obligates** (wake "attest or schedule") or escalates up
the existing ladder.

Done:
- [ ] An agent that finishes-and-idles with an open obligation triggers the sweep.
- [ ] An agent that scheduled a continuation wake does **not** trigger it (no false positive).

Depends on: P3, P5. Spec: `agentic-engineering-guidance-spec.md` §6.

---

## P7 — Flagship enforcement loops, end-to-end

Goal: compose P3–P6 into the actual rails the guidance calls for, firing at both edges.

Deliverable: the enforced loops — **independent review** (deny → remedy assigns to the bound cross-model
reviewer role, loud `unbound` if unprovisioned → iterate on `changes-requested` → `reviewed-clean` releases; reviewer teardown is
an org rail over a session-liveness observable, not v1 capstone scope
enforced), **smoke-before-ship**, **YAGNI**, **spec-review**, **tests-pass** — each fires at
both the dispatch verb and the turn-end edge.

Done:
- [ ] The §6 reviewer-loop worked example runs **enforced** end-to-end (producer cannot skip
      or ship-dirty; reviewer-session teardown gating is an org-authored rail over a
      session-liveness observable, filed as a P3-adjacent gap — not v1 capstone scope).
- [ ] Each flagship rail's §6 enforcement-mapping row is marked satisfied, with its strength
      (independent-producer vs self-attested) recorded.

Depends on: P4, P5, P6. Spec: `agentic-engineering-guidance-spec.md` §6.

---

NOTE: the transferable design wisdom is now canonical in
`wisdom.md` (25 rules, enforcement/substrate-vs-inference/work/
guidance-authoring/process) — spec-writers, reviewers, and kungfu authors read it
before minting law; future spec reviews cite rules by number.

## Morning agenda (Flynn, 2026-07-22 night — next working session)

RULED (Flynn 2026-07-22): SUBSTRATE SKILLS ARE BASELINE-PROJECTED, not elected — every
session's home projects the tightbeam-* skill set (dispatching, assimilate, harnesses,
tour, skills) ahead of archetype elections: frontmatter is an index line (cheap,
always-on), the body loads on invocation, so the disclosure rule is enforced by the
frontmatter/body split rather than by election bookkeeping. Election remains for
kungfu/role skills (org choice). Mechanics: Homes.project adds the baseline set;
per-archetype tightbeam-* elections removed as redundant. Small lane, post-LKP1 window.

Progress: default-archetype spec DONE (Flynn dictated live 2026-07-22): general agent +
first-contact tour (tightbeam-tour skill; tour-given fact as the seen-flag, filed via the
condition verb) + wake-time health glance + network-map.md (org-authored machine purposes)
+ proactive purpose-asking. Deployed to identity (4518212); guidance-spec content blocks
to be synced by the formalization pass. Mechanics needing a small lane later:
(a) `tightbeam doctor` — a mechanical config-health report, and it is the BOOTSTRAP
path (Flynn: guidance cannot check harness health when no harness can run inference —
chicken-and-egg). Doctor is inference-free by requirement: CLI-runnable pre-boot, the
gateway runs it at boot and exposes the verdict on the wire so the client renders
"org not ready: <reason>" natively. The default agent's guidance glance covers only the
degraded-but-running middle (ready-to-rumble checks:
default model valid in a fresh catalog, harness credentials live, hosts registered,
advertised URL set) the default agent can invoke instead of eyeballing `list`;
(b0) `createdAt` added to the list verb's session projection (one atom in the
Map.take) — upgrades the kungfu-moment trigger from presence-count to span-of-days;
(b) a read path for querying a fact by kind+scope (the tour flag check) if none ships
with the current verbs. Archetype manifest loads at boot — default's new elections go
live at the next batched restart.

1. **Formalize product-owner + orchestrator guidance** — both archetypes accreted rulings
   all night (self-assignment, exclusivity, slates, no-source-editing, expecter-cards,
   naming, cleanup, bottom-up sweep); they need a deliberate authoring pass into coherent
   directive sets (per guidance-authoring doctrine: directives, role voice, minimal homes)
   rather than accumulated bullets.
2. **Model/harness-release intake — DEV time first** (Flynn correction: we live at dev
   time; the gateway is optional). (a) Detector = a runnable check, no gateway: `mix
   tightbeam.catalog.diff` runs the L0 fetchers standalone and diffs live inventories
   against the models characterized in model-selection.md (uncharacterized / vanished).
   (b) Completeness = a `model-release-intake` SKILL (rare ceremony → library skill):
   run the diff, characterize the new model, sweep every archetype's preferences +
   quality floors, update the capability matrix, attest. Trigger is the human or the
   diff. (c) RUNTIME version stays queued for long-lived orgs: same diff promoted into
   the catalog's refresh heartbeat, filing a model-added condition fact; steward
   condition-wake. Trigger mechanism (Flynn: git hook): tuned to the factory —
   a BLOCKING network hook is wrong (agents commit dozens of times/night); instead
   (i) advisory TTL-cached post-merge hook, never blocks, one loud drift line; and/or
   (ii) preferred: an externally-tagged catalog-coverage test run AT THE MERGE GATE
   only (--only external; excluded from default runs) — one runner pays the fetch at
   the choke point, gate-loud on uncharacterized models. Dev-time pieces are small and
   giftable to the morning session."

## Artifacts & reconciliation (Flynn 2026-07-22; spec: artifacts-and-reconciliation.md)

The general answer to the spec-storage gap: an artifacts registry (existence recorded,
home tracked, searchable), reconciliation as a workspace-close gate (parent notified,
archive-whole-workspace as always-valid fallback), a per-level artifact-policy.md
preference doc (kind→destination, inference applies), and discovery via registry query +
transcript search. Resolves specRefName and the WV-lane pause. A real subsystem — sequence
AFTER the current post-LKP1 lanes + the spine; the artifact-policy doc + artifact-record
discipline (guidance) can ship earlier as the interim while the table/gate wait.

## Priority order of record (2026-07-22 reprioritization — org-test findings first)

Ruling: recently ratified constitution/org-test items take PRECEDENCE over the remaining
spine, except where an item is dependency-blocked by spine machinery.

- NOW (parallel with LKP1, disjoint files): drawer provenance fields — origin/spawnedBy
  as OPTIONAL keys in the wire session payload, fail-open to visible (payloads.ex only).
- After LKP1, BEFORE LP4 — two lanes:
  - session-lifecycle: retire cascade + loud interruption rows; harness-process reaping;
    stream_removed emission; zombie running-turn boot-recovery fix; critical-section
    lease (split out if the lane runs large).
  - org-settings + default-archetype (Flynn 2026-07-22): first org_settings KV row;
    `tightbeam config set default-archetype <name>` (admin verb, validated against
    known archetypes); session-create without explicit archetype reads the setting
    (falls back "default"); kungfu manifests declare root_archetype (specced in the
    guidance spec); the post-adoption offer guidance lands WITH the verb in the
    kungfu-adoption module + user.md records the decision.
  - work-item-brackets: work_items gains owner/icebox/routingWakeId; create-txn arms
    the routed-or-deadline timed wake (cancel on first assign/icebox); close-txn
    delivers the concluded-or-adjudicated owner wake on last-open-close; icebox verb +
    CLI; config seam for the routing deadline. Spec: accountability-constitution §2
    (mechanism-grade). Files: work_items.ex, assignments.ex, gateway verbs, CLI —
    slots cleanly in this post-LKP1 window.
  - work-visibility: work-lifecycle tombstones (attest/assignment marker rows via the
    messages projection); marker provenance (cause + principal on reset/failure
    tombstones); atomic `dispatch` verb (assign + wake, one txn).
- Then the spine resumes: LP4 → LP5 → LP6 — which UNBLOCKS (and absorbs): strand
  notification + empty-chain-to-owner escalation (lands with LP6's sweep),
  assignment-as-capability rail (own lane after P6), chain-of-command binding statute
  (with P5 predicates), then LP8 → LP7 → LP7b (+ statute candidates, C5-C7/capstones).
- After: credential onboarding flow (detection half already riding LKP1), org-health
  view, wire full-stream emission (typed stream; tombstones deliver interim visibility),
  cross-arch assimilate. Future-triggered: ACP-conformant protocol (new client UX).

## Known gaps (tracked here, NOT in playground work-items — test install, disposable)

NOTE: the session-lifecycle / accountability / binding-policy items below are now
CANONICAL in `accountability-constitution-v1.md` (ratified 2026-07-22) — that spec wins
over these tracking notes; entries below remain for scheduling only.

- **assimilate is same-arch-only**: the CLI-install step scps `current_exe()` gated on
  target-triple equality (cli/src/ceremonies.rs:443); a cross-arch satellite (Mac ARM
  control → Linux x86-64 worker) skips the CLI with a misleading remediation hint.
  Fix direction ranked: build-on-satellite fallback > per-target release artifacts >
  assimilate-from-same-arch. Interim runbook lives in the tightbeam-assimilate skill.
- **Session provenance missing from the app catalog payload**: sessions carry
  `origin`/`spawnedBy` (substrate) and the org-verb `list` projects them, but the wire's
  `stream_session` payload (the clawline drawer) omits both — the client cannot segregate
  user-created from agent-spawned ("under the hood") sessions. Fix: add the two fields to
  the payload; clawline then groups/hides agent-origin sessions behind a toggle. Good
  candidate for the in-substrate org's second test work-item.
- **Agent attribution requires a role even with a session credential** (in-substrate test,
  PO session): archetype-spawned session with no `--name` → no roles row → first org verb
  refused `no_role`; only workaround is `--as-user`, which mis-attributes agent acts to the
  human. Ruling direction: the session credential should itself be a valid attribution
  principal ("session:<key>" — the escalation spec already models session-tagged
  principals); roles remain for ADDRESSABILITY (wake --role), not attribution necessity.
  At minimum, fail/warn at spawn, not on first command.
- **Work-lifecycle tombstones (NEAR-TERM micro-lane, Flynn 2026-07-22)**: extend the
  existing turn-tombstone pattern ([context reset]/[turn failed] — which surface only
  because the turn pipeline writes the messages projection) to WORK transitions: attest
  edges also write a compact marker row into the actor's transcript — [surrendered
  asg_x — verdict: unverified; needs user input], [completion filed on asg_x],
  [assignment opened]. Zero wire/client changes; renders today through the same path.
  Interim until the typed stream; sequence after LKP1 (projection/gateway contention).
- **Retire leaks the harness process**: retiring a session updates rows + supervision but
  never reaps that session's harness-side subprocess (a dozen observed resident for
  retired sessions). Fix: retire walks to the adapter and ends the ACP session/process.
  Adapter seam — sequence after LKP1 (same file).
- **No stream_removed wire event**: client is never told a session disappeared; drawer
  shows ghosts until reconnect (snapshot is active-only). Fix: emit a removal event from
  the retire path. Gateway/payloads — sequence after LKP1 (gateway.ex contention).
- **Top-of-chain accountability (stalled PO)**: the prodder watches assignment holders;
  a PO holding no rows is invisible, and a user-created session has no spawner chain to
  escalate up. Shipped now: PO guidance — self-assign every agreed work item (puts POs
  under the ordinary sweep). Substrate half: when the escalation chain is empty or dead,
  escalate to the ORG OWNER via the wake-to-user path (composes with the strand fix —
  one rule: always find a living authority, the user being the root).
- **Strands are silent (live incident 2026-07-22)**: prods target holders, so a retired
  holder gets zero prods, zero missed-prod escalation — and the escalation path walks to
  the opener, who may also be retired. P6's sweep classifies :stranded by design but
  nobody is TOLD. Fix: a strand files a fact + notifies the first LIVE ancestor up the
  spawner chain, falling back to the org owner. (Cascade-retire's interruption rows
  reduce strands; this covers the rest.)
- **Role reuse enables cross-org borrowing (same incident)**: a PO dispatched to another
  PO's hire by addressing its existing role; the hire's parent later swept it, stranding
  the borrower silently. Nothing records "borrowed." Direction: guidance shipped (spawn
  your own with fresh slug); consider making wake-by-role to a session you neither
  spawned nor own at least visible to the session's owner. RULED (Flynn 2026-07-22):
  orchestrators are per-work-item instruments of ONE product owner — dispatching to an
  orchestrator you didn't spawn is forbidden (context pollution + uncontrolled
  lifecycle). Guidance shipped. GENERALIZED (Flynn 2026-07-22): obligations follow the
  chain of command for EVERY archetype — a session accepts assignments only from its
  spawner chain or the org owner/admin — but REVISED (Flynn): this is ORG POLICY, not
  substrate hardcode. Binding policy is modeled as LAW: the substrate exposes neutral
  relationship facts (spawner-of, same-spawner-chain, owner, archetype, role) as rail
  predicates; the org's statutes say who may bind whom. Chain-of-command ships as the
  DEFAULT statute in the bundle; other topologies (shared specialist pools, borrowing
  within a product family only) replace or scope it — selective borrowing is a narrower
  predicate, and named agent-groups become an org-config fact when a second real
  topology needs them. Conversation wakes stay open regardless; strangers talk, law
  decides who binds. Card-creation enforcement RULED, revised (Flynn
  2026-07-22): spawn does NOT require a work item — pools of pre-spawned agents are
  legitimate; existence needs no ticket. spawn --subject/--work-item stays as the atomic
  AFFORDANCE. The actual defect (root-caused from the strand incident): the EXPECTER
  never opened a card — the worker self-carded, recording effort but not expectation,
  and the expectation died with the worker. LAW: the expecter opens the card — assign
  first, wake second; a work-shaped wake with no opener-side card is chosen silence.
  Rail status RULED (Flynn 2026-07-22): NO rail — an
  unrecorded expectation leaves no evidence, and threshold-based unbooked-work detection
  is arbitrary (rejected). Close the gap BY CONSTRUCTION instead: (a) atomic `dispatch`
  verb = assign + wake in one txn (card opened, holder woken with the assignment id, one
  command — correct dispatch becomes the easiest action); (b) an org-health VIEW listing
  busy-but-bookless sessions, ranked, threshold-free — observability without enforcement
  (a view denies nothing, so it needs no cutoff); judgment stays with the PO/owner.
  Work-item propagation RULED: one work-item, many assignments — decomposition happens
  in assignment subjects down the tree, all referencing the same thread; new work-items
  only for genuinely new discovered scope, raised to the PO. (Org already practices
  this — every playground assignment is work-item-linked.) Note: the anti-pattern propagated by example from the operator's
  own pointer-only wakes — pattern propagation applies to coordination behavior, not
  just code. Orchestrators may hold a SET
  of work items (exclusivity is of OWNERSHIP, not cardinality); on slate-clear the
  spawner hands more work or retires deliberately — never auto-retire. Escalation-to-living-ancestor stays substrate
  (it's delivery mechanics, not policy).
- **Retire doesn't consider the subtree (orphan hazard)**: retiring a session leaves its
  hires alive with an escalation chain through a dead link; nothing warns the retirer.
  Ruling (Flynn, 2026-07-22): CASCADE BY DEFAULT — a hire's output has one consumer, its
  spawner; orphaned work is unconsumable effort, and everything durable already lives in
  rows (work-items/assignments/attests survive; a replacement org re-staffs from the
  record). Requirements: the cascade is LOUD (result names every session taken down; each
  cascaded hire's open assignment gets a terminal row marking the interruption, resumable
  from the work-item history). Keeping a subtree is the explicit minority path: reassign
  those hires BEFORE retiring the parent — no quiet reparenting flag. Guidance (sweep
  bottom-up) stays as etiquette, not law. Verify where chain-walk escalation lands past a
  retired link (moot once cascade lands, relevant until then).
  Completion (Flynn, 2026-07-22): (a) LAW — mutations belong in your workdir; shared
  mutations (main commits, identity repo, gateway restart) are ceremonies. Cascade is safe
  BECAUSE work is workdir-confined. (b) CRITICAL-SECTION LEASE — a session doing a shared
  mutation declares `critical --for <t> --reason <r>` (hard cap, bounded renewal, no
  immortality). Retire/cascade on an unexpired lease DEFERS, never skips: target gets the
  retire-intent as final instruction ("clean up; hard-retire at T" — the hard kill is a
  scheduled wake), retirer is told the deferral + deadline. The lease is a row, so rails
  can later REQUIRE one for risky ceremonies (gateway-restart-without-lease: denied).
- **Turn timeout: 10-minute hard ceiling kills work turns** (org PO dispatch died
  :timeout at exactly 600s). Immediate: env-configurable TIGHTBEAM_TURN_TIMEOUT_MS
  (micro-lane dispatched; playground set to 30m). RULED (Flynn 2026-07-22 — day-long turns are the industry
  trajectory, not an edge case): THREE liveness layers, each at its own granularity —
  (1) turn duration UNBOUNDED by policy (a turn takes what the work takes; no ceiling is
  correct); (2) harness WEDGE detected by ACTIVITY STALENESS (the adapter already
  streams session/updates; "no update of any kind for N minutes" is the pathology
  signal at any total duration — the only layer that may terminate, via check-in
  semantics); (3) work ABANDONMENT judged by the accountability patrol
  (attests/prods/escalation) at the assignment level. FINAL (Flynn): the ceiling is DROPPED NOW —
  freeze detection is supervisory JUDGMENT and orchestrators already do it (streams,
  cadence, context a timer cannot have); the mechanical check's only demonstrated act
  was interrupting valid work. Playground env goes effectively-infinite at the next
  restart. When activity-staleness ships it returns as a BACKSTOP TO the orchestrators
  — substrate backstops inference; that is the point of tightbeam — never the primary
  judge. Designed future: timeout-as-check-in —
  on ceiling, mark the turn honestly AND auto-schedule the continuation nudge (harness
  session survives, resume is cheap); the :timeout marker names the ceiling + the
  scheduled continuation (legibility cluster).
- **Clawline rename/delete 404: '+'-encoded space in session-key path params** — the
  routes exist (PATCH/DELETE /api/streams/:key); clawline encodes the key's space as '+',
  router matches literally, lookup misses → not_found. Fix: normalize '+'→space in :key
  decoding (keys never contain literal '+'). Repro'd live 2026-07-21. Handed to the
  in-substrate PO as a work-item.
- **Tombstone provenance (Flynn ask)**: [context reset] should carry CAUSE + PRINCIPAL —
  "guidance amended by user:mike (fingerprint a1b2→c3d4), home reprojected" vs
  "orchestrator:model-picker restarted the gateway; resume failed". Ingredients exist:
  home-manifest guidance_sha256, boot epochs/dirty-exit inference, and the lineage stamp
  the org's orchestrator improvised (TIGHTBEAM_LINEAGE) — formalize restart-principal
  recording. Same legibility doctrine as turn-failure cause.
- **Turn-failure legibility**: boot-recovery marks in-flight turns failed_unknown and the
  client renders "interrupted: outcome unknown" with no cause. Honest (never fake an
  outcome) but improvable: the recovery marker can carry WHAT interrupted (gateway
  restart + boot epoch, adapter crash class). Ties into classified edges (KP1) and
  full-stream emission.
- **In-substrate test rough edges (orchestrator + reviewer reports, 2026-07-21):**
  (a) post-gateway-restart window where implicit session-credential identity fails
  ("identity required") until the ACP reconnect re-registers — explicit --as works;
  (b) harness auto-resume transparently recovers a session whose gateway died mid-turn
  (good) but surfaces a phantom "tool use rejected by user" at the reconnect seam;
  (c) `retire` returns bare misleading not_found under session-credential identity;
  (d) `attest --help` never enumerates the valid --verdict vocabulary;
  (e) verdict --note 2000-char cap is tight for real reviews (spec'd value — revisit);
  (f) identity-required errors give no hint toward --as/--as-user;
  (g) NO "why is this session stalled" diagnostic — root-causing the codex outage took
  manual PID tracing + adapter-stderr grep (KP1 classification + P8 legibility close
  this). Stale-binary artifact excluded: assign --reviews existed on main, org's CLI
  binary predated LC (refreshed 2026-07-21).
- **Codex adapter crash-loops at boot on dead credentials**: {:gate_attestation_failed,
  :turn_error} → supervisor churn until restart limits. Fail-loud floor works but is
  noisy and illegible; KP1's classified auth_denied + hold is the designed fix — this
  incident is its acceptance scenario.
- **No deployed/production state in the work model**: assignments walk
  open→active→claims-done→verified; nothing records "live on a gateway." Spec it when a
  real rollout pipeline exists or a rail first needs to gate on liveness (Flynn may want
  it earlier — dark factory should know what's deployed).

## Kungfu operational intake (Flynn 2026-07-22; pairs with learn/relearn)

Bundles ship `kungfu/<name>/intake.md` — operator questions with named answer
destinations. Learn = install + intake conversation (walk the operator through, write
answers to destinations, operational only when complete-or-deferred); relearn re-asks
only new questions. Engineering kungfu's intake to be authored (model characterizations
/prefs/floors, producers.toml commands, spec workspace root, independence stance) —
this also retires the model-selection template debt: the template IS the unanswered
intake.

## Kungfu update & reintegration (Flynn 2026-07-22; design ratified, packaged-bundle era)

Three-way merge over the identity repo's own git. PROVENANCE IS RECORDED, NEVER
INFERRED: `tightbeam learn` commits the pristine bundle and TAGS it
(kungfu/<name>@<version>, vendor-branch discipline) — user mods = diff(tag, HEAD) over
bundle paths. MUST-DO-FIRST: learn tags pristine installs from its first real version
(provenance cannot be added retroactively). Update: the substrate-level `kungfu-reintegration` skill drives `tightbeam relearn` — relearn brackets inference:
(1) deterministic STAGE — three-way merge (base=install tag) onto a BRANCH, never live
identity; determinism owns transactionality, NOT safety; (2) INFERENCE REVIEWS THE
WHOLE DIFF (Flynn: clean-merge is textual, not semantic — nothing applies unread): the
reintegration agent reads every hunk with the user's tag-diff customization set in
hand, hunting interference between clean changes and user mods, textual conflicts
(user's side proposed-to-user, never silently overridden), and semantic
redundancy/contradiction (upstream now covers a hand-built local thing -> offer
retirement; disjoint-but-conflicting rules -> surface); resolutions are ordinary
commits on the branch; (3) deterministic verify — loads clean, rails compile + satisfiability, corpus
proofs, tag @v2. RULED (Flynn): the skill's inference pass is a DE-CONFLICTING + DE-DUPING pass over
the merged guidance, and it NEVER unilaterally changes user or kungfu guidance — every
reconciliation is walked through with the user, who decides. Skill ships WITH the
relearn lane. Detection = catalog-delta
sibling (update fact -> default/PO tells the
user, never auto-applies); application batches with a restart (memory tax).

## Future: ACP-conformant org protocol (filed 2026-07-21; revisit with the tightbeam-native client)

The clawline wire was created ad hoc for openclaw. When a better tightbeam-native UX gets
built (Flynn intends one, separate from clawline), define a NEW client protocol that fuses
the two layers cleanly: the ORG envelope (device identity/auth, multi-session multiplexing,
seq-ordered durable replay, owner-scoped fan-out, org verbs — spawn/wake/assign/attest/list)
conforming to ACP's patterns and structures wherever a concept overlaps (session/update kind
vocabulary for activity payloads, its request/notification shapes). Design seeds already
ruled: one interleaved typed event stream (see next section); ACP vocabulary as activity
payload schema, never as the org envelope; optional ACP server facade (present an org session
AS an ACP session so ACP-native clients can attach as alternate views). Trigger to revisit:
the new-client UX work starts. Until then the clawline wire stays as-is.

## Credential lifecycle + remote onboarding (queued; spec-first — Flynn 2026-07-21)

Credential death is a recurring operational event on BOTH harnesses; today it is illegible
(boot gate detects, tells no one — the in-substrate org needed PID/stderr archaeology) and
recovery needs a terminal on the gateway host. Design shape ruled:
1. Credential health as substrate state per {org, host, harness}: valid|expired|revoked,
   written by the adapter boot gate's existing detection, read in list/org-options, emitted
   as a wire event on transition (rides KP1 auth_denied classification + stream emission).
2. Relay the login FLOW, never the login PAGE (no provider-HTML proxying — brittle and
   phishing-shaped). Structured wire steps rendered natively by the client:
   codex → {kind: device_code, url, code, expiresAt}; claude → {kind: paste_back, url} with
   a code-return verb. Real provider pages open in the real device browser.
3. A credential-onboard ceremony verb: gateway drives the harness login subprocess on the
   target host (same ssh plumbing as assimilate), streams steps, accepts paste-back,
   verifies with a probe turn, files credential:valid; held sessions resume via recovery.
Medic statute (Flynn 2026-07-22 — the auto-spawn suggestion, adopted): when the ENTIRE
affected authority chain sits on the dead harness (owner path unusable), a default-bundle
REMEDY STATUTE fires: on credential:revoked(H) with no live-harness authority in the
chain, spawn a recovery session on a surviving harness, carded with the recovery work —
prepare the onboard ceremony, push the user card, re-staff urgent work. Law-triggered
(P5 remedy machinery; orgs tune/remove), predicate never fires when a live owner exists
(brief path wins). Addendum (Flynn 2026-07-22): the OWNER is the cross-harness
recovery agent by construction — the adjudication brief for auth_failed reaches a live
session on a working harness (or escalates to the user); its option set gains
"initiate credential-onboard" (triggers the ceremony → user card), alongside re-staffing
interim work. No dedicated medic archetype; if every harness is dead, the user card via
living-authority root is the path. Clawline: a "harness needs reconnecting" card driving the flow. Bar: tonight's codex
outage replayed = card within seconds, tap → authorize → paste → org resumes.

## Wire full-stream emission (queued; spec addendum before build — Flynn ruling 2026-07-21)

One totally ordered stream of TYPED events per session — user/assistant messages, thinking
chunks, tool calls, attests, spawns, rail denials — interleaved at true position (seq + ts),
emitted live post-commit in commit order. Presentation is the client's (clawline groups/
collapses by kind); the substrate emits neutrally. Subscription-side kind filtering. Durable
(row-backed) kinds replay on reconnect; thinking/progress ephemeral-by-default with an org
toggle. Today's coarse progress channel ("Thinking…", tool titles via Adapter.progress_status
+ ConnRegistry publish_work_state) is the seed, not the contract. Investigate separately:
whether the existing progress emission regressed on the wire or stopped rendering client-side.
Ties into LP8 legibility (denials visible in-transcript). Refinement (2026-07-22 incident:
PO surrendered + asked the user; UI showed nothing raiseable): AWAITING-USER-INPUT is a
first-class attention state, not just a stream event — surrender/verdict attests emit as
system rows, and questions-to-user materialize as decision-requests (LE1's table is the
substrate form once the fold wires escalate), rendered client-side as a badged inbox of
open DRs with deadlines. A session waiting on the user must be visually distinct from a
stalled one. Spec home: a wire-projection
addendum; clawline picks up rendering after the wire lands.

## Assignment-as-capability (Flynn, 2026-07-22; statute design, post P4-P6)

The strong form of no-unbooked-work: MUTATING tool calls require an open assignment —
the card is the capability. Read/query stays free (pools consult, POs look around);
mutation (file writes, state-changing shell, tightbeam effect verbs) is gated on "caller
holds an open assignment" — pure row evidence at existing enforcement points (C1 harness
hooks for commands, P4-P6 dispatch for verbs). RULED (Flynn): this is a SUBSTRATE RAIL,
constitutional — kungfu CANNOT turn it off. It completes the substrate's attribution
guarantee: every act names WHO, every mutation names UNDER WHAT OBLIGATION. Org law
still owns who-may-bind-whom (binding POLICY); binding EXISTENCE is physics. Self-carding
stays legal — the guarantee is no INVISIBLE work, not no autonomous work: a self-opened
card is patrolled, attributed, readable, revocable. v2: tag every tool call with the assignment
it serves → full provenance chain (mutation → obligation → work item → user agreement).
Bootstrap: expecter-opens-card + atomic dispatch put the card before the first turn;
self-carding covers self-directed work; admin axis exempt as always.

## P7b — Shipped tranche-2 law (authoring deliverable; from the lattice reviews)

The flagship statutes themselves — the concrete `independent-review`, `tests-pass`,
`real-run`, `yagni`, `spec-review` TOML files, their scripts in `rails/scripts/`, and the
live org's `producers.toml` content — authored as identity-repo artifacts per the mechanism
grammar and §6 mapping, exactly P2's pattern: authored, loads clean, fires, corpus-proven.
No spec previously owned these as artifacts (both lattice reviews, H1/H8).

Done:
- [ ] The five flagship statute files + scripts + producers.toml authored and corpus-proven.
- [ ] Statute candidates (2026-07-22, PM anti-patterns -> rails; row evidence only):
  `spirit-section-exists` — a PO's work-items must reference a spec whose Spirit
  section exists (specRef row + C5 script check on the section); `outcome-traced
  filing` — PO-filed work items carry a spec-ref (feature-factory guard: no
  intent-free filings; specRefName presence is a row); `acceptance-is-the-owners` —
  acceptance verdicts on a product's work come from its PO (row check; constitution
  already implies it). NOT railable (stays guidance): stop-at-first-answer,
  reframe quality, saying no — judgment. EXCEPT trigger (d), now railable (Flynn 2026-07-22):
  `digest-before-orchestration` — assign-to-orchestrator-archetype at the verb edge
  requires >=1 self-wake with the `digest:` prompt prefix since the previous
  orchestration hand-off (prefix-match = C1-class pattern, not content comprehension;
  both sides are rows: assign + wakes + archetype). Mirrors the unconditional guidance
  trigger; deny with remedy "schedule your digest first". P5-era statute. Other
  rumination triggers likewise (conversation
  content + spec-file edits are outside substrate rows); the generic never-idle patrol
  already backstops the scheduling habit. FUTURE: if product specs move under
  substrate-tracked assets (assets table + specRef sha exist), spirit-edits become
  row-visible and "hand-off without digest after spirit change" becomes a checkable
  statute — rails follow rows.
- [ ] Statute candidate (2026-07-22): `onboarding-artifact` — C5 script gate: user.md
  exists for the user a default-archetype session serves (file-existence via script;
  sweep edge; remedy wakes the session to onboard). Stronger form once facts-read
  ships: onboarding-completion as a ROW -> pure-row statute, no script (also fixes the
  per-machine flag limit). Judgment (timing, declines, warmth) stays guidance.
- [ ] Statute candidate (from the org test, 2026-07-21): `worktree-discipline` — C1 harness
  gate denying `git commit`/build-mutating commands executed IN the canonical checkout
  (pattern-matchable like no-git-stash); remedy names the worktree-session skill. Norm
  exists as coder guidance; the org's orchestrator coded in the canonical checkout twice —
  guidance without rails drifted within hours, which is the whole §6 thesis.

## P8 — Legibility & guidance-change policy

Goal: enforcement is accountable, and changing guidance/rails is tracked-and-reversible.

Deliverable: every rail invocation is a recorded event; non-pass emits self-naming facts that
answer "which rail, which dispatch, why" without forensics. Guidance changes are
git-tracked-reversible (done for skills → extend to rule/rail edits). Optional org **review-gate
on guidance changes (default off)** and **meta-rail escalation** (who may change rails → user).

Notes (from the lattice reviews): predicate PASSES are not separately recorded — evaluations
are derivable from verb events (the hot path stays free; §6 wording aligned). Non-pass
records carry the identity-manifest SHA (§6g's slicing axis — cheap now, unbackfillable
later). The guidance-change review gate is enforceable only at load/commit time, outside
dispatch — it stays a policy statement until an org wants it designed (Flynn ruled it off by
default). Implementation-lane doctrine: the DB-owner re-entry trap (rediscovered three times
in spec-land) and the `*_in_txn` convention get written ONCE as db.ex doctrine before the
wave — a paragraph, not a framework; the five CAS tables stay separate by design.

Done:
- [ ] A `rail-denials`-class read verb/CLI exposes the non-pass records (the "point at the
      failure without forensics" query), with rule/caller/SHA dimensions.
- [ ] "Point at the failure without forensics" query works against real invocations.
- [ ] A bad rail is one `git revert` away; a guidance change is a diff with an attributed author.
- [ ] Review-on-guidance-change is an opt-in org rail, off by default.

Depends on: P4. Spec: `agentic-engineering-guidance-spec.md` §6, `self-tuning-rails-core-FUTURE.md`.

---

## P9 — Separation review (final gate)

Goal: prove the substrate/product boundary held through everything built above.

Deliverable: an independent review — a fresh session that authored none of the content —
audits every guidance file, skill, and rail for placement. The substrate carries only neutral
operating mechanism: the operating manual, generic verbs, containment. The engineering kungfu
carries every engineering-specific tenet, archetype, skill, and rail. No substrate file names
an engineering concept; no kungfu file restates substrate mechanism.

Done:
- [ ] Every file in the shipped layout is classified substrate or kungfu with zero
      cross-boundary content; violations are moved, not annotated.
- [ ] The review verdict is recorded and referenced from this roadmap.

Depends on: P1, P2 (re-run after any later phase that adds guidance or rails).

---

## Completion checklist (at-a-glance)

- [ ] P1 guidance authored & loaded (+ §6 finalized)
- [ ] P2 today-expressible rails authored & firing
- [ ] D1 enforcement-direction ruling recorded
- [ ] P3 flagship observables/producers live; deny-halves proven
- [ ] P4 contained scripts gate verbs, fail-closed, legible
- [ ] P5 active-gate remedies spawn producers idempotently; rail-set satisfiability checked
- [ ] P6 turn-end sweep catches omission without false positives
- [ ] P7 flagship loops enforced end-to-end at both edges
- [ ] P8 invocations legible; guidance changes tracked/reversible
- [ ] P9 separation review passed (substrate vs engineering kungfu)

---

## Parallel / optional tracks (non-blocking)

- **T-A — DeltaDB backend evaluation.** Resolve the one deciding question: self-hostable/
  embeddable vs. Zed-hosted-only. If self-hostable, it can replace the git store, delete the
  worktree ceremony, and give facts durable delta-anchored references — a backend swap behind the
  same invariant. Does not block any phase.
- **T-B — Self-tuning rails core.** Begins after P7; specced in `self-tuning-rails-core-FUTURE.md`
  (OASIS signal + Hermes eval-gate + tightbeam enforcement; writes rails as reviewed commits).
  Its metric layer accrues long before it starts: remedy rate (§6g) is collected from P5 onward
  by the cross-cutting observability requirement; its corpus must include exogenous ground
  truth (§6e); its outcomes are reviewed against the §6f expectations register.
