# Agentic-Engineering Guidance — documentation spec

This is the **spec** for the guidance of the always-on substrate operating manual and the
`agentic-engineering` kungfu bundle: what guidance exists, where it lives, who reads it,
and the doctrines it must carry.

**The canonical textual home of the guidance is the shipped tree in the tightbeam
repository:** `priv/guidance/operating-manual.md` (the substrate manual) and
`priv/kungfu/agentic-engineering/` (the bundle). The wording agents read lives there and
only there; amendments edit those files, and git carries their history. This spec carries
the layout, the elections, the doctrines, and the authoring rules — it does not transcribe
the files' text. A second textual home re-arms the drift engine: transcription here is
forbidden. (Canonical-home ruling, 2026-07-28.)

**How to read this spec.** Everything below is instruction prose for the guidance author:
what file exists, where it goes, who reads it, and what doctrine it must state. To read
the guidance itself, open the shipped file. Guidance content remains **definitive** (rules
and facts, no hedges, conditions stated) and carries **no meta** (no version notes, no
rationale, no cross-references to this spec).

---

## 1. File layout

All bundle paths are under `priv/kungfu/agentic-engineering/` in the tightbeam
repository; the manual ships inside the substrate at `priv/guidance/operating-manual.md`
and is served as the built-in `operating-manual.md` fragment.

| File (path) | Read by | Loaded |
|---|---|---|
| `priv/guidance/operating-manual.md` | every session | always on |
| `manifest.toml` (`root_archetype = "product-owner"`) | the substrate | never read as prose |
| `capabilities.md` | any session, without electing the bundle | at user-conversation start |
| `intake.md` | the learning agent, at install/relearn | during intake |
| `preferred-models.md` (bundle root) | intake destination; source of the kungfu activity table | on election, via the composed kernel |
| `guidance/<archetype>.md` — one kernel per archetype: `orchestrator`, `spec-writer`, `coder`, `reviewer`, `recon`, `product-owner`, `default` | sessions of that archetype | on election |
| `guidance/engineering-tenets.md` | every engineering archetype | on election |
| `guidance/preferred-models.md` — the substrate working set: model capsules, table-reading rule, substrate activities | every engineering archetype | on election |
| `guidance/wisdom-core.md`, `guidance/wisdom-meta.md` | per archetype election | on election |
| `guidance/harness-support.md`, `guidance/operating-model.md` | per archetype election | on election |
| `archetypes/<name>.toml` — the election manifests | the substrate (identity composition) | never read as prose |
| `skills/<name>/SKILL.md` | the electing archetype | on load |
| `rails/engineering.toml` | the substrate (enforced) | never read as prose |
| `rules/engineering.toml` | the substrate (enforced) | never read as prose |

Mapping to the engine: the substrate serves the bundle's guidance as its built-in
fragment library (`Tightbeam.Archetypes.builtin_fragments/0`); an org's identity
repository may override any fragment by name, and the org file wins. Each
`archetypes/<name>.toml` manifest declares the archetype's name, its skill election, and
a `[guidance]` text composed of `#include "<fragment>.md"` directives — the kernel an
elected session actually receives. Skills are the agent-skills format: a directory per
skill whose `SKILL.md` opens with YAML frontmatter (`name`, `description` — the
description states when to use the skill) followed by the body.

**Model guidance is named `preferred-models.md`** at both levels: the substrate's
`guidance/preferred-models.md` carries the working-set capsules, the table-reading rule
(one ordered column of minds per activity; step rightward on unavailability; the end of
the list is the floor — park rather than degrade below it, as a recorded decision with a
re-check wake or escalation; `any` = floorless), and the substrate's own activity rows;
the bundle-root `preferred-models.md` carries the engineering activity table. Both are
org-authored intake destinations — the shipped rows are the current org's judgments.
The engineering table carries two rulings as law: implementation is split by difficulty
(new patterns / critical code / tough bugs to the strong-reasoning tier; straightforward
well-specced bounded goals and established-pattern extension to the workhorse tier), and
code review is **cross-harness and cross-model/thinking-level from the producer — never
the same family, never the same effort tier**. Review independence is a family/harness
axis, not a capability step-up; the reviewer's tier comes from the review row.

---

## 2. Substrate operating manual

Ships inside the substrate; every session receives it at boot. The manual is the PATTERNS
of operating tightbeam — each section is a situation and the move, illustrated with one
exemplary command using example names the reader substitutes from the live catalog. It is
not a flag reference: agents discover mechanics from `tightbeam --help`; the manual
carries only what cannot be discovered — the compositions.

Authoring rule (the design-insight capture pipeline): every ratified spec that changes
what agents should recognize or compose answers "what pattern does this teach?" — the
answer is either "none" or a manual amendment landing with the spec. Pattern sections for
capabilities not yet shipped are forbidden; the manual never teaches commands that do not
exist.

Disclosure rule: everyday substrate operation — waking, attesting, assigning, spawning,
reading denials — belongs in this manual; a RARE ceremony (assimilating a machine,
credential onboarding) becomes a library skill instead. Frequency of performance decides,
and the number of textual homes stays minimal because prose has no rails.

The manual's required patterns, by section:

- **The CLI is an executable.** The manual opens by naming `tightbeam` an ordinary
  executable on PATH, run through the shell tool — it is not a built-in tool and appears
  in no tool list. JSON on stdout; nonzero exit is failure with the reason on stderr.
- **Where you are** — one session with an address, an owner, and a job; refusals name
  the rule, read the reason.
- **See what is around you** — `tightbeam list`: sessions, archetypes, hosts, the model
  catalog; the session's own key in `.tightbeam-session` at the workdir root.
- **Identity** — commands are attributed; workdir-derived by default, `--as <role>`,
  `--as-user <id>`.
- **Wake** — prompts to mailboxes, `--after`/`--at`; answering origin tags: a prompt
  tagged `[from user:<id>]` is answered with `wake --user`, one tagged
  `[from agent:<name>]` with `wake --role`.
- **Wake yourself to work later** — deferred work is a self-wake; `cancel-wake`.
- **Colleagues without disruption** — no idle nudges; routine progress to your owner.
- **Hire and retire** — spawn with display/name/archetype/host, idempotency keys, the
  naming rule ("<Role> — <specific purpose>" displays; "<function>:<work-slug>" roles),
  and the dispatch law: the assignment row IS the dispatch — open the card first, wake
  with a pointer; retire what you hired, dependents first.
- **Before you build what tightbeam already is** — the tentpole recognitions, and
  reading each installed kungfu's `capabilities.md` at user-conversation start.
- **Track work** — work-items, assignments, attests (progress / completion / surrender /
  verdict); state is computed from facts, never set. `artifact-record` declares work
  produced outside the workdir — tightbeam sees workdir files; everything else is
  invisible until pointed at.
- **Recover after losing context** — re-derive from the rows, never from scrollback.
- **Where your files live** — the workdir is the durable artifact space, surviving
  restarts, home regeneration, and machine moves; the home is substrate-owned identity
  that may be regenerated at any time, and anything loose in it is forfeit.
- **Never end a turn with open work and nothing on the clock** — every turn under an
  open assignment ends with a filing or a scheduled continuation wake; a turn with
  neither is a stall the substrate checks in on, and unanswered check-ins escalate to
  the spawner. The check-in and the never-idle rule are one doctrine: the check-in asks
  for verbs the agent already has, and filing as work happens is the same answer given
  first.
- **Work alongside other agents** — another agent's in-progress material is neither
  discardable nor a blocker; reconcile it. Own work happens in an own worktree created
  **inside the own workdir** (the worktree-session skill carries the full convention).
- **When a rule stops a command** — do not route around it; repeated denial means the
  approach is wrong.
- **When a decision is the user's** — ask, do not guess and do not stall; the answer is
  recorded as a fact and releases the work.
- **Report so the user can act** — every claim sourced; "done" means the user can try
  it; identifiers explained; record now what should be kept.

---

## 3. Engineering tenets

`guidance/engineering-tenets.md` is elected by every engineering archetype: the
requirement-before-code, passing-is-not-working, real-fixtures, provenance-before-change,
build-exactly-the-spec, evidence-per-step, regression-provenance, report-tool-failure,
ordering, and hand-off tenets. One page, definitive, no hedges.

---

## 4. Archetype kernels

One kernel per archetype at `guidance/<archetype>.md`, composed into the served identity
by the archetype's manifest. Each kernel states the archetype's job and rules in its own
voice.

- **orchestrator** — judgment and flow, never specs or code; the board is the work-item
  rows; dispatch by the card-first law with brief, authority, and definition of done;
  decompose by the seam with `--files` declared; a handful of goals truly in-flight;
  every sweep advances or kills; two failed attempts revert; repeat-failure bugs go to
  recon for a `diagnosed` verdict; independent review is **cross-harness and
  cross-family from the producer** with the reviewer's tier from the preferred-models
  review row; real runs before ship (`run-smoke`); orchestrators never edit source.
- **spec-writer** — invariants first, testable acceptance, open questions marked,
  non-goals named; substrate specs stay free of product concerns; carries its `##
  Patterns` directive section.
- **coder** — build exactly the spec; own worktree inside the own workdir; reconcile
  with main before building; completion attests name repo and commit; carries its `##
  Patterns` directive section.
- **reviewer** — independent, breaks work, flags without fixing; clause-by-clause
  conformance; reproduces findings; **necessity-gates behavioral deltas**: every change
  to existing observable behavior needs a LIVE requiring clause, and a delta authorized
  only by conformance, fidelity, a retired clause, or tidiness is a blocking finding —
  the adjudication goes up, the change stays out; carries its `## Patterns` directive
  section.
- **recon** — truth before building; evidence-cited findings; yes / no / conditional /
  not-proven answers.
- **product-owner** — owns the product's spirit and quality; converses with the user in
  concepts and drives ambiguity to definition (product-discovery); spawns and owns its
  orchestrators, never borrowing another's; self-assigns agreed work items; judges
  readiness per slice; acceptance is judged against the SPIRIT, and for substantial
  changes that judgment happens pre-merge (the spirit-review gate, defined in
  `feature-cycle`); does not orchestrate lanes — its context belongs to the user
  conversation. It elects `tightbeam-dispatching` and `product-discovery`, not the
  pattern doctrine.
- **default** — carries the shared operating model only.

Kungfu bundle manifest: the bundle declares `root_archetype = "product-owner"` in
`manifest.toml` and ships a capability matrix (`capabilities.md`: what adopting it gives
an org plus conversation watch-fors per capability) readable without electing the bundle,
and an operational intake (`intake.md`): the questions whose answers only the operator
has, each naming where the answer lands — working-set capsules and activity rows (→ the
substrate's `guidance/preferred-models.md` and the bundle's `preferred-models.md`),
producer commands per repo, the spec workspace root, review-independence stance. Learning
a kungfu is deterministic install + intake conversation, question by question, each
answer written to its named destination; the kungfu is not operational until intake is
complete or each skipped item is explicitly deferred. Relearn re-runs intake only for
questions the update added. `root_archetype` pairs with the org's `default_archetype`
setting: adopting the kungfu triggers the one-time offer to point the setting at the
bundle's root.

Pattern doctrine: there is no shared architecture-principles file. The anti-drift
doctrine (one concept one pattern; patterns detectable; no silent deviation; invariants
stated at their seam; right-weight structure; one mutation seam; substrate/product
separation; build exactly the spec; production code by default) is deployed ONLY as the
per-role `## Patterns` directive sections inside the shipped spec-writer, coder, and
reviewer kernels — guidance is directives, not an encyclopedia. Those three sections are
refractions of one doctrine; any amendment edits the three sections together, in the
bundle.

---

## 5. Skills

Each skill is its own `skills/<name>/SKILL.md` with agent-skills YAML frontmatter. The
election per archetype (from the shipped manifests):

- orchestrator: `feature-cycle`, `work-tracking`, `unblocking`, `tightbeam-law-minting`,
  `tightbeam-guidance-authoring`.
- spec-writer: `drafting-requirements`, `spec-homing`, `spec-handoff`,
  `tightbeam-law-minting`, `tightbeam-guidance-authoring`.
- coder: `worktree-session`, `committing-and-pushing`.
- reviewer: `reviewing-code`, `reviewing-specs`, `spec-conformance`,
  `review-for-completeness`, `review-for-yagni`, `tightbeam-law-minting`,
  `tightbeam-guidance-authoring`.
- recon: `recon-first-investigation`, `recon-lifecycle`, `bug-provenance`.
- product-owner: `tightbeam-dispatching`, `product-discovery`.

Canonical vocabulary, used identically by every guidance file:

- Verdict values: `reviewed-clean` | `changes-requested` for reviews;
  `spirit-accepted` | `changes-requested` for the product owner's spirit verdict;
  `yes` | `no` | `conditional` | `not-proven` for recon answers; `diagnosed` for
  bug-provenance; the user's decision recorded verbatim for user rulings. Verdicts are
  open strings at the substrate; these are the bundle's values.
- Bug-cause classes: `code-violates-spec` | `spec-hole` | `stale-spec` | `spec-conflict`
  | `wrong-proof` | `composition` | `environment-drift`.
- Finding severities: `blocking` | `important` | `nit`.
- Spec-clause classes: `satisfied` | `unsatisfied` | `unproven` | `out-of-scope`.

Dispatch vocabulary: `tightbeam dispatch --to <holder> --subject … --brief … --work-item
<id>` opens a plain card and wakes its holder atomically; a card that declares files
(`--files`, refused on overlap with an open assignment at dispatch time) or links a
review (`--reviews <reviewedAssignmentId>`, the fact that lets the substrate witness
review independence) opens with `assign` and is then woken. A work item pins its spec by
content, not memory: `--spec-ref <name> --spec-sha256 <hex>`. `tightbeam run-tests
<assignmentId>` and `tightbeam run-smoke <assignmentId>` run the org's committed commands
and stamp the `tests-passed` and `real-run-passed` verdicts — mechanical evidence, not
self-attestation.

Spec skeleton (spec-homing): every spec has all eight canonical sections — Goal,
Non-Goals, Terms, Assumptions, Invariants, Architecture, Acceptance, Open Questions — a
canonical set, not a minimum or a menu; an empty section is stated empty, never omitted.
Open questions are marked blocking or non-blocking; builders build around a marked hole
and never an unmarked one.

Spirit-review gate (feature-cycle, with pointers from committing-and-pushing and the
product-owner kernel): a substantial change — product behavior with no
product-owner-gated spec authority behind it — does not integrate until the product owner
has answered its spirit summary with a verdict attest on the goal's assignment; a routine
change advances on the normal review gates alone. The boundary is defined once, in
`feature-cycle`; the other two files point at it.

Worktree convention (worktree-session): the worktree is the isolation boundary, created
inside the assignment's own workdir; destructive git on any tree that may hold another
agent's work is forbidden; merged branches and finished worktrees are pruned as part of
completion.

---

## 6. Rails (the enforcement model — author-facing; never agent-read prose)

This section is for whoever authors the bundle's rails. None of it is shown to an agent.
It defines what a rail is, how enforcement behaves, where rails live, and how the author
decides whether a rule is a rail or advisory guidance.

### The principle: rails check evidence, never behavior
A rail never enforces what happens inside an agent — understanding, care, effort, intent.
It enforces evidence: a fact that the behavior, done right, necessarily produces. The
author's first question for any rule is "what evidence does following this rule leave
behind, and who produces it?" A rule whose observance leaves no producible evidence is
advisory guidance, not a rail.

### The red-tape test
A rail is a backstop and an aid, never process. A compliant agent experiences a rail as
nothing at all; a rail prices only the failure path. Every rail must pass all of:
- **Silent when satisfied.** The gate fires only at its boundary verb and passes without
  output when the evidence exists. No acknowledgments, no pre-clearance, no per-step checks.
- **Evidence is a byproduct.** The fact a gate checks is produced by doing the work — a
  commit, a review session's verdict, a build's emitted result — and the substrate derives
  facts from what it can observe. An agent attests judgment (a verdict, a surrender); it does
  not file descriptions of work the substrate can see.
- **Remedy before deny.** Where a remedy can produce the missing evidence, the gate starts
  the producer instead of bouncing the agent. Deny-and-wait is for evidence only the agent's
  own work can produce.
- **Outcome verbs only.** Evidence-gates sit on ship, merge, and complete — the boundaries
  where defects escape — never on working verbs (edit, run, spawn, wake). Two exemptions: a
  commission-time check on a working verb is allowed when it is instantaneous and mechanical
  (argument shape, overlap of declared file sets), never a wait for evidence; and containment
  denying a destructive action outright is not an evidence-gate.
- **A rail that fires on compliant work is a defective rail.** Repeated denial of correct
  work is a bug in the rail, not the agent; the rail is narrowed or removed, and the
  false-positive signal feeds the tuning system.

### What a rail is
A rail is a contained, value-returning script the substrate runs at the dispatch chokepoint.
The script returns a value from a declared set, and the statute maps each value to an effect:
allow the verb, deny it, run a remedy, or escalate — halt the verb behind a decision-request
delivered to the owner, with the raiser parked on the ruling (at the turn-end edge, the sweep
opens the request and parks the holder). A rail's check is either a mechanical comparison the
script computes directly (compare two identities, read a gauge) — always synchronous and
time-boxed — or a judgment, which no script performs or awaits: the gate checks for the
judgment's verdict fact, and the statute's remedy originates the judge session that produces
it. A rail's definition — its TOML statute and its script — is a version-tracked artifact in
the rails repository, not an ad-hoc patch.

### The bar is accountability, not perfect prevention
A rail does not have to be correct to be worth having; it has to be legible. A rail is a
registered artifact; its evaluations are derivable from the recorded verb events (every
gated dispatch is already a row — predicate passes are not separately recorded, which keeps
the hot path free); and every non-pass — deny, script error, timeout, a value outside the
declared set, a script that hangs — emits a record that names the rail, the dispatch it
fired on, the identity-manifest SHA it ran under, and the reason it did not pass. A wrong rail is
therefore a fixable, attributable, revertable problem, not an archaeology exercise. The target
is that a rail's failure is visible without forensics.

### Two kinds of rail, by time
- **Synchronous check.** A fast script that returns on the dispatch path (compare two
  identities, read a gauge). It is time-boxed. A synchronous check that exceeds its box is
  broken, and the timeout denies. The box detects a pathological script; it is not a limit on
  how long any real work may take.
- **Asynchronous judgment.** A review, or any check that invokes inference or spawns a session.
  It is never a blocking call and never time-boxed. The gate itself is an instantaneous
  fact-existence check: the required verdict fact exists, or the verb is denied now. The
  judgment that produces the fact runs as a separate, supervised, unbounded session. Its
  liveness is enforced by supervision on that session — heartbeat and progress — not by capping
  how long the judgment may take. A twenty-minute review and a hung reviewer are different
  conditions, and supervision distinguishes them; a timeout cannot.

### The second firing edge: the turn-end sweep
A gate fires at its boundary verb (commission) and at turn suspension (omission). The sweep
is a step inside the supervision terminal-edge evaluation: for a session idling with an open
obligation and no self-scheduled continuation wake, the substrate dry-evaluates the
obligation's gates. A remedy decision runs that remedy, at most once; any other unsatisfied
outcome re-obligates — wake the holder to attest or schedule — or escalates up the
supervision ladder. An agent that finishes and goes idle without attesting is caught; an
agent that scheduled its own continuation is not, and a wake scheduled by someone else does
not suppress the sweep.

### Fail closed on the check, not on the judgment
An absent required fact denies. An errored, hung, or out-of-set synchronous script denies. A
judgment session that dies is caught by supervision and escalated, and the gated verb stays
denied until a verdict fact lands or the user rules. The gate never guesses a value for a check
it could not complete.

### Producer strength
A gate is exactly as trustworthy as the producer of the fact it checks. The ladder, weakest to
strongest: a self-attested fact (the actor claims it); an independent judge's verdict (a
separate session, different model family, whose only job is the judgment — protected from
author bias, but still inference); an independent mechanical producer (a build or a real run —
reality touches it); exogenous verification (the user, production). Judges carry the judgment
qualities — quality, scope, spec-fit; mechanical and exogenous producers anchor "it actually
works." Judge-passed work is sampled and re-verified against reality; a judge-passed item that
fails reality is a finding about the judge, and it feeds the tuning system.

### Containment
Containment plays two roles in enforcement. It is the sandbox that enforces the actions the
dispatch chokepoint never sees — destructive filesystem and git actions, credential movement,
auto-start registration — which no rail script intercepts because they happen below the verb
layer. It is also the runtime that makes rail scripts safe to run: a rail script executes inside
the sandbox, time-boxed and resource-capped, so a misbehaving rail is itself contained and
fails closed. Host placement is substrate constitution (set membership), not a rail.

### The independent-review rail (worked example, shipped)
`completion-requires-review` in `rules/engineering.toml`: `attest completion` for a
code-change requires a `reviewed-clean` verdict fact whose author session is not the
producer and whose harness differs from the producer's (cross-harness is the enforceable
form of cross-model: harness is substrate-known, model ids stay opaque). Absent that
fact, the remedy assigns the review to the org's bound reviewer role (cross-harness,
failing loud if unbound), hands it the change, and denies the completion. The reviewer
attests its verdict; a `changes-requested` verdict wakes the producer to iterate and
re-attest; the cycle repeats until the verdict is `reviewed-clean`. On clean, the
completion is allowed. The producer cannot skip the review or ship an unclean change —
each is a rail-enforced condition, not a remembered one. Gating on reviewer-session
teardown is an org-authored rail over a session-liveness observable, not part of this
bundle's rail.

### The re-entry twin (shipped)
`refix-requires-diagnosis` in `rules/engineering.toml`: an implementation dispatch on a
bug work-item with at least one completed prior fix assignment and no `diagnosed` verdict
is remedied by assigning a recon with `bug-provenance`; the diagnosed verdict releases
the dispatch. The flagship rail gates work's EXIT on an independent verdict; this gates
work's RE-ENTRY on one. Its predicate reads the closed rule facts `work_item.is_bug` and
`assignment.prior_completed_fix_count`, which the substrate exposes. First-attempt bugs
are guidance-only — railing every bug through an autopsy prices the compliant path.

### Rails are software
The TOML statutes and their scripts are version-tracked in a repository. A rail change is a
diff: reviewed, attributed by history, revertable, bisectable. Enforcement is self-hosting — a
change to a rail is a code-change subject to the same review rail as any other change. The
self-tuning system writes rails by proposing commits to this repository, gated by review and
evaluation; it does not mutate a running substrate.

### Changing guidance is an org policy, not substrate law
The substrate makes every guidance change a tracked, attributed, revertable commit; it imposes
no review. Requiring a review verdict before a guidance change loads is an org-authored rail,
shipped off. The meta-rails below are the one such rail this bundle recommends an org adopt.

### Meta-rails
A thin set of rails governs changes to the rails themselves. A change to an ordinary rail
advances on a clean review verdict. A change to a meta-rail — a rule governing who may change
rails — escalates to the user.

### The author decision: rail or advisory
A rule is a rail when a script can return a verdict on it — a mechanical comparison, a gauge
read, or a judgment delegated to a spawned judge. A rule is advisory when no script can decide
it even by delegation: demo-data-is-not-proof, and the escalation triggers (subsystem de-scope,
ambiguous requirement, CRITICAL review finding). Advisory rules live in the kernels and
skills, where the agent recognizes them and acts.

### The enforcement mapping
The author decision applied to this bundle's guidance, rule by rule. "Edge" is where the rail
fires: the dispatch verb, the turn-end sweep, or the tool layer (harness matcher /
containment). "Strength" is the producer-strength ladder. Rows marked **(pending)** need an
observable or producer the substrate does not yet have; their guidance still ships, and the
rail lands when the observable does.

| Rule | Mechanism | Edge | Strength |
|---|---|---|---|
| Independent review — `reviewed-clean`, author ≠ producer, cross-harness | fact-gate + remedy — **shipped** as `completion-requires-review` | verb + turn-end | strong (independent judge) |
| Re-fix of a failed fix requires a `diagnosed` verdict | fact-gate + remedy — **shipped** as `refix-requires-diagnosis` | verb | strong (independent judge) |
| Tests pass before reporting success | fact-gate on `tests-passed` (`run-tests`) | verb + turn-end | strong (mechanical) |
| Real run against real inputs before ship | fact-gate on `real-run-passed` (`run-smoke`) | verb + turn-end | strong (mechanical) |
| Reconcile with main before building on it | sync check (git ancestry) | verb | strong (mechanical) |
| Two failed attempts → revert to known-good | fact-gate (count of `changes-requested` verdicts) **(pending: derived count)** | verb | mechanical |
| Order changes touching the same code; parallel only when independent | deny overlapping dispatch — **shipped** via `--files` overlap refusal | verb | mechanical |
| Hand-off states what is passed / expected back / whom to wake | arg-presence check **(pending: structured hand-off fields)** | verb | mechanical |
| No unrequested additions (build exactly the spec) | judge gate (`yagni` verdict) | verb + turn-end | judge |
| Spec has its eight canonical sections | judge gate (`spec-reviewed` verdict) | verb + turn-end | judge |
| Fixtures from real responses; every claim sourced; every review clause proven | judge gate (part of the review verdict) | verb | judge |
| No destructive git (stash, reset --hard, clean -f, checkout --, restore) on any worktree | containment / tool-call statutes — **shipped** in `rails/engineering.toml` | tool layer | accident-grade |
| Write only in your own worktree | containment | tool layer | accident-grade |
| No ad-hoc substitution when a known tool fails | containment (partial — catches the action, not the intent) | tool layer | partial |
| Spirit review before a substantial change integrates | guidance-tier (feature-cycle) — hardening into a rail is a separate decision | — | taught |
| Find the requirement before the code; read before you change; ask when the decision is the user's; re-derive from facts after context loss; root-cause before a FIRST fix attempt; no idle nudges | **advisory only** — no producible evidence (root-cause becomes enforceable only at re-fix, where the failed attempt is the observable) | — | taught |

### What the bundle ships
Only rails universal to engineering: the destructive-git tool-call statutes
(`rails/engineering.toml`) and the two enforced rules (`rules/engineering.toml`:
`completion-requires-review`, `refix-requires-diagnosis`). Remaining evidence-gates in
the mapping land as their observables do. A rule an org merely prefers (for example, a
human ruling before a merge to main) is added by that org, not shipped here.

### Substrate mechanism (separate specs)
The substrate machinery this section relies on — the statute engine and its predicates,
the containment integration, the fact schema that makes every rail invocation and
non-pass legible, and the rules loading/reload wiring — is substrate design, not bundle
documentation: see `rails-mechanism-v1.md`, `statute-engine-v1.md`, and
`rails-v1-implementation.md`.

---

## 7. Excluded from this documentation

Do not author these here.
- **Personality / persona.** Not produced.
- **Self-improvement / tuning.** Covered by a separate system.
- **Subspace, Clawline, device/UI operation.** Contributed by those packages and learned
  later.
- **Session/dispatch/lock plumbing.** The substrate provides these verbs; the operating manual
  (§2) is the only guidance for them.
- **Tracker state-machine procedures.** Replaced by work-item + facts + supervision; the
  `work-tracking` skill is the only artifact.
