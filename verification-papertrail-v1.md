# Verification papertrail — the substrate requires, inference produces — v1

Status: DRAFT for Flynn's gate (#90 re-ruling, 2026-07-29). Supersedes
`producer-definitions-v1.md` (amended 2026-07-28) in full and the producer
subsystem of `p3-observables-producers-v1.md` §5 (the `producer_jobs` queue,
substrate execution, mechanical verdict stamps). Ground truth read on main:
`lib/tightbeam/producers.ex` (whole module + `ProducerRunner`),
`lib/tightbeam/rules.ex` (remedy validation :365–474, F1/F2 :598–729, fact
table :98–121), `lib/tightbeam/assignments.ex` (attests schema :66–95, verdict
attests :1101–1127, `insert_producer_verdict_in_txn` :320,
`produced_verdict_kinds` :283–291), `lib/tightbeam/artifacts.ex` (registry
schema :9–26), `lib/tightbeam/rail_remedy.ex` (episode lifecycle),
`lib/tightbeam/gateway.ex` (:243–248, :374–381, :826–843),
`lib/tightbeam/wire/router.ex` (:48, :813–814), `cli/src/args.rs`,
`cli/src/dispatch.rs`, `priv/kungfu/agentic-engineering/`.

## Problem

The substrate performs domain work. `run-tests` and `run-smoke` accept an
assignment, and the substrate itself runs the org's committed command in the
holder's workdir and stamps the verdict (`producers.ex` `@producer_shapes`
:27–30, `execute/4`, `insert_producer_verdict_in_txn`). Two conflations ride
on that:

- **Kungfu vocabulary in the verb set.** `run-tests`/`run-smoke`,
  `tests-passed`/`real-run-passed`, and the `tests`/`smoke` config keys are
  the engineering school's words, hardcoded in substrate source across two
  languages (router `@agent_verbs`, gateway handler table, `producers.ex`,
  `rules.ex` F1, CLI args/dispatch).
- **The substrate as actor.** The 2026-07-28 amendment
  (producer-definitions-v1: org-declared producers, one generic
  `run-producer` verb) fixed the vocabulary conflation but kept the deeper
  one — the substrate still executed org-defined commands on the work path,
  and its trust argument (witnessed execution, unforgeable exit codes) was
  the malicious-agent framing that is explicitly out of scope
  (rails-not-attackers). Both designs make inference a cog: the machine does
  the verifying and the mind is left to press the button.

What the org actually needs is that completion claims are backed by evidence
of verification. That is a papertrail requirement, and the substrate already
owns every primitive it takes: attests, artifacts, statutes, remedies.

## Ruling

Flynn, 2026-07-29 (recorded in memory `substrate-records-inference-acts`;
supersedes the 2026-07-28 producer-definitions gate direction):

**The substrate records, observes, prods, and gates on records; it never
performs domain work.** Enforcement means requiring papertrails — attests
plus recorded artifacts — never producing them. "The job of the substrate is
to record and make observable, and in that way guide inference or force
inference to a goal — not to make inference just a cog in the machine."

The principle, as this spec's constraint set:

1. **Inference is the only actor for work — and the line is work
   vs. checking, not script vs. no-script.** Work brings new state into
   existence or needs domain judgment to read it: building, testing,
   exercising a product, judging a poem sad. Checking reads state that
   already exists: a row is present, a branch is an ancestor of main, a
   workdir is clean. The substrate never performs work — no execution of
   org- or project-defined commands that do work, ever. It may check: a
   rail check script (`[rule.check]`, rails-mechanism-v1 §A) is the
   substrate reading existing state to adjudicate a call, the same act as
   evaluating a predicate over its own tables, extended to material it
   hosts. The discriminator: if the command must perform the domain
   activity to learn the answer, it is work and belongs to a mind that
   files the record; if it only reads records that already exist, it is a
   check. `run-smoke` fails this test — the answer does not exist until
   the product is exercised. A reconcile-before-build ancestry check
   passes it — the repo already contains the answer.

   The two proof tiers partition the fact space, and neither substitutes
   for the other. A **check** senses live state: deterministic,
   re-observed at the moment of every call, sound precisely because it
   cannot go stale — "is this branch an ancestor of main *now*." A
   **verdict** witnesses a judgment about a fixed referent: "this diff
   was reviewed," "this poem is good" — append-only, filed by a mind,
   counted as rows, sound precisely because the fact cannot drift after
   filing. Gating on a row is correct only when the fact cannot change
   under it; live state must be sensed, never memorialized (a
   `reconciled` verdict is false the moment main advances, and the
   statute would still count it). Symmetrically, a check that needs
   judgment must become a verdict — the statute summons a mind that
   files the row — never a script that invokes inference from inside
   the gate: that puts nondeterminism on the synchronous chokepoint and
   produces a judgment with no attributed record. Cost follows the same
   line: gates evaluate on every call and almost all should pass —
   sensing makes the happy path free, while gating live state on
   verdicts taxes every pass with a remedy round-trip or trains agents
   to pre-file ceremony rows.
2. **Rules summon inference; they never replace it.** The remedy mechanism
   is the canonical embodiment: statute effects are
   allow/deny/remedy/escalate, and a remedy's action is validated to exactly
   `assign | wake | spawn` (rules.ex:373–374) — the substrate's only active
   move is summoning a mind with a natural-language sentence. It is
   structurally incapable of running domain scripts, and stays so.
3. **The coupling law.** Four vocabulary spaces exist: substrate schema
   (fixed), repos (semi-stable, org-portable), shipped kungfu (semi-stable),
   org-local identity (freely mutable). Any mechanical token joining
   repo↔kungfu — a config key a component KNOWS to look for — couples a
   project to one org's current spelling and breaks silently on rename,
   unlearn, or a second org. Only two joins are sound: substrate schema, and
   minds reading prose. An agent that cannot bridge escalates the gap
   legibly ("I'm being hounded to verify and nothing here defines
   verification"), which surfaces process gaps to humans; a config reader
   only breaks silently.
4. **Sloppiness is the threat, not malice.** Requiring an attest plus a
   recorded results artifact forces actual doing. Fabricating the papertrail
   is deception — out of scope per the rails posture.

## Design

### 1. Verification is an org statute

The engineering kungfu ships verification as ITS policy — statute rules in
the bundle's `rules/`, installed on learn, org-editable on `main` like any
other identity law. The substrate contributes no verification concept; it
contributes the generic statute engine, the attest and artifact registries,
and the remedy mechanism, all of which already exist.

The shipped shape (bundle content — every token below except the fact names
and operators is org vocabulary, editable after learn):

```toml
# rules/verification.toml — the engineering school's completion papertrail
[[rule]]
name = "completion-requires-verification"
verb = "attest"
edges = ["verb"]
effect = "remedy"
text = "completion requires a verification verdict on the assignment"
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  { fact = "assignment.holder_archetype", op = "in", value = ["coder"] },
  { fact = "assignment.verdicts", op = "not_in", value = ["verified"] },
]
[rule.remedy]
action = "wake"
produces = "verified"
target_session = "{holder_key}"
[rule.remedy.params]
prompt = "Your completion of {assignment_id} is blocked: no verification verdict is filed. Verify the work the way this repository defines verification (its AGENTS.md or equivalent prose), then file `tightbeam attest {assignment_id} --kind verdict --verdict verified` with a note saying what you ran and what you observed."

[[rule]]
name = "completion-requires-results-artifact"
verb = "attest"
edges = ["verb"]
effect = "remedy"
text = "completion requires a recorded results artifact from the holder"
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  { fact = "assignment.holder_archetype", op = "in", value = ["coder"] },
  { fact = "assignment.artifact_kinds", op = "not_in", value = ["report"] },
]
[rule.remedy]
action = "wake"
target_session = "{holder_key}"
[rule.remedy.params]
prompt = "Your completion of {assignment_id} is blocked: no results artifact is recorded. Record the verification results (output, logs, evidence) with `tightbeam artifact-record` as a report artifact on this work item, then complete."
```

Semantics, all existing machinery:

- The gate fires at the dispatch chokepoint on the completion attest; the
  completion is denied (`remedy_fired`) and `RailRemedy.fire/5` wakes the
  holder with the sentence naming exactly what record is missing. The holder
  produces the missing record by inference — runs whatever the repo's prose
  defines, files the verdict attest, records the artifact — and re-attests
  completion.
- Verdict attests are filable by any session or user principal on an open
  assignment (assignments.ex:1101–1127); the holder's own `verified` verdict
  is the intended filing. Self-attestation is correct under the threat
  model: the attest plus the artifact force the doing; forging them is
  deception, out of scope.
- Conditions AND within a rule, so the two obligations are two rules. They
  prod sequentially (the first matching remedy statute halts evaluation,
  rules.ex `fold_effect`): an agent missing both gets the verification wake
  first, then the artifact wake on its next attempt. Each sentence names its
  own missing record; the first statute's prompt may mention the full
  papertrail.
- When the papertrail is complete, the completion attest passes and the
  live remedy episodes close through the existing actor-owned close
  (`maybe_close`/`RailRemedy.close`). Filing the verification verdict itself
  is never blocked — `attest.kind` is then `"verdict"`, not `"completion"`.
- The `holder_archetype` narrowing scopes the requirement to implementation
  work; a reviewer's completion (whose evidence IS its verdict filing) is
  not artifact-gated. Scope is a statute-authoring choice — §Open 3.

### 2. The engine delta (minimal, flagged)

Verified against `rules.ex` on main — most of the vocabulary exists:

- `attest.kind` (:string, eq/ne/in/not_in) — exists (:111, :991–999).
- `assignment.verdicts` (list of distinct filed verdict kinds) — exists
  (:111, :1001–1006). The `not_in` gate over it is a verdict-fact
  requirement; F1 satisfiability accepts it because the remedy's
  `produces = "verified"` covers the gate (`remedy_covers?`, :624–630).
- `assignment.holder_archetype` — exists (:116, :1066–1071).
- Remedy `wake` with `target_session = "{holder_key}"` and an interpolated
  `prompt` — exists (`@remedy_keys`, `@binding_tokens`, `@whole_fields`,
  :70–84; RailRemedy binding/resolution).

Two additions are required, both substrate-neutral, both flagged here as the
entire engine delta:

**D1 — new fact `assignment.artifact_kinds`** (`{:list, :string}`,
in/not_in): the distinct `artifacts.kind` values of artifact rows whose
`workItemId` is the assignment's work item and whose `createdBySession` is
the assignment's holder session. Resolved through the existing `$assignment`
dependency; `nil` when the assignment cannot be resolved (nil never
satisfies any operator, the standing posture); empty list when the holder
recorded nothing (so `not_in` fires — same shape as `assignment.verdicts`).
The fact ignores artifact `state`: in-workspace, archived, and released rows
all count — a record counts in every state (do not import the referents
precedent's archived-row filter).
Holder-scoping mirrors the referents precedent (effort-checkin-v2 §Design 5:
"an attest's referents are the artifacts the HOLDER recorded",
assignments.ex:684–689) — the papertrail must be attributable to the party
completing. The fact reads only the substrate's own artifact registry and
the substrate's own `kind` enumeration
(`spec|report|doc|data|other`, artifacts.ex:11) — a substrate-schema join,
sound under the coupling law. No artifact-content interpretation, ever.

**D2 — artifact-fact gates become remedy-eligible.** Today a predicate
remedy REQUIRES a verdict-fact gate and `produces` must be one of the gate's
kinds (rules.ex:439–446), so the second statute above would fail load.
Extension: a `not_in` condition over `assignment.artifact_kinds` counts as a
remedy-qualifying requirement. `produces` stays verdict-only and is omitted
when the gate's only requirements are artifact requirements. Satisfiability
needs no producer: `artifact-record` is a constitutional verb available to
every session, so an artifact requirement is statically satisfiable — F1
accepts it, and the F2 chain walk treats a statute whose requirements are
all artifact requirements as escaping (the role
`producer_registry_covers?` played for statically-covered gates, which §5
deletes). Episode closure needs nothing: `maybe_close` already closes when
the gate stops matching.

### 3. HOW to verify lives in repo prose

WHAT record is required is statute law (§1). HOW to produce it lives in the
project repository as prose for minds — the AGENTS.md convention: "verify by
running `./smoke.py` against staging", "verification here means the assay
pipeline completes clean". Agents read it the way they read everything else
in a repo.

Explicitly ruled out, and this is a load-bearing boundary, not an omission:

- **No substrate or kungfu schema for verification method.** No
  `producers.toml` successor, no verify-command key, no declaration table.
- **No deterministic kungfu readers of repo config.** No component parses a
  repo-side file to learn what verification means.

The rationale is the coupling law (§Ruling 3). A mechanical token the kungfu
looks for in repos welds one org's current spelling into every project that
adopts it and fails silently on rename, unlearn, or a second org. Prose read
by minds is rename-proof — the agent bridges vocabulary by inference — and
when the bridge is missing it fails LEGIBLY: the agent being hounded to
verify says so, escalates, and a human learns the project never defined
verification. Rules state WHAT record is missing; agents determine HOW, or
escalate the gap.

### 4. The verbs die

`run-tests`, `run-smoke`, and `cancel-producer-job` cease to exist as
substrate surface. The seam is multi-site and two-language; the sites,
exhaustively:

- `lib/tightbeam/wire/router.ex` — the three `@agent_verbs` members (:48);
  the `unknown_producer_job` (404) and `producer_unconfigured` (403) error
  statuses (:813–814).
- `lib/tightbeam/gateway.ex` — the three handler-table entries (:826–843).
- `cli/src/args.rs` — the `RunTests`/`RunSmoke` command variants (:109–115),
  parse arms (:987–1003), help lines (:397–399), the unknown-command
  command-list string and its test copy (:1289, :1860), the shell-completion
  entries (:1546–1547), and the `cancel-producer-job` row in the
  not-exposed-surface test list (:1879).
- `cli/src/dispatch.rs` — the `RunTests`/`RunSmoke` dispatch arms
  (:291–306), identity arms (:963–964), the byte-exact body test fixtures
  (:1343–1351), and the attest fixture carrying verdictKind `tests-passed`
  (:1253–1257), rewritten to a neutral kind.
- `cli/src/ceremonies.rs` — the stale "producer fixture" comment (:307),
  rewritten to drop the reference.

Sunset timing — hard deletion now versus a compatibility window — is §Open
1; the recommendation is one cut with no alias seam.

### 5. The producer job-runner subsystem: deletion, evaluated honestly

Every consumer of the subsystem on main, enumerated:

1. `lib/tightbeam/producers.ex` itself — `Producers` (the `producer_jobs`
   table DDL, `load!` of `identity/producers.toml`, the three verb handlers,
   `cancel_for_holder`, `recover`, `claim_next`/`execute` and the whole
   local-execution and signal-identity apparatus) and the `ProducerRunner`
   GenServer.
2. `lib/tightbeam/gateway.ex` — boot `Producers.load!` (:243), the
   `producer_config`/`producer_runner` handler-config keys (:244, :253–257),
   the retire-path `Producers.cancel_for_holder` (:248), the
   `ProducerSupervisor` + `ProducerRunner` child specs (:374–381), and the
   `producer_config` argument fed to `Rules.load!` (:259).
3. `lib/tightbeam/rules.ex` — `Rules.load!/3`'s producer-registry parameter;
   `producer_registry_covers?/3` + `maybe_add_producer_kind/4` (F1
   satisfiability for `assignment.produced_verdict_kinds`, :632–644);
   `escaping_static_producer?/2` (F2 cycle exemption, :697–706); the fact
   `assignment.produced_verdict_kinds` (@facts :115, @verdict_facts :85–91,
   `compute_fact` :1059–1064, the `remedy_covers?` exclusion arm :625); the
   moduledoc's `tests-passed` example.
4. `lib/tightbeam/assignments.ex` — `insert_producer_verdict_in_txn/2`
   (:320, the sole writer of producer-stamped verdicts) and
   `produced_verdict_kinds/2` (:283–291, the fact's only reader). The
   `attests.producer`/`producerCommand` columns and their CHECK.
5. The verb surfaces of §4 (router, gateway, CLI).
6. Tests — `test/producers_test.exs` (whole file); the conformance corpus's
   `producer_job`/`producer_verdict` world vocabulary and transition
   fixtures (`test/conformance_test.exs`); producer fixtures in
   `test/rules_test.exs` and the `produced_verdict_kinds` gate in
   `test/rail_remedy_test.exs`; the run-verb cases in
   `test/cli_integration_test.exs`; the producer-verdict insertion tests in
   `test/assignments_test.exs`.
7. Bundle content — `guidance/coder.md`, `guidance/orchestrator.md`,
   `skills/feature-cycle/SKILL.md`, `skills/spec-conformance/SKILL.md`
   (instruct `run-tests`/`run-smoke`), `intake.md` Q3 (destination
   `identity/producers.toml`).
8. Test-org identity repos (shrdlu, tars) — committed `producers.toml`,
   served guidance snapshots instructing the verbs.
9. Forensic surfaces — `producer_failed`/`producer_kill_failed` lifecycle
   event emissions; historical `attests` rows carrying producer stamps.
   (No forensic READER of `producer_jobs` exists in lib/ — verified; the
   table is written and read only by `producers.ex` and the conformance
   corpus.)

**Verdict: full deletion of the subsystem.** No consumer survives on its own
necessity: the runner exists solely to execute the dying verbs; with no
writer, `assignment.produced_verdict_kinds` is permanently empty, so any
gate over it is permanently unsatisfiable and the fact is meaningless — a
half-alive fact would be exactly the stubbed-projection failure mode.
Deleted: items 1–3 in full (the module, both processes, the boot load, the
retire hook, the F1/F2 producer arms, the fact and its `@verdict_facts`
membership and `compute_fact` arm), `insert_producer_verdict_in_txn/2` and
`produced_verdict_kinds/2` from item 4, all of items 5–6 (tests rewritten to
the statute shape of §1 or dropped), and the item-7 bundle prose rewritten
per §7. `Rules.load!/3` becomes `load!/2`.

What minimally survives, each with its necessity named:

- **`attests.producer`/`producerCommand` columns** (and their CHECK, and
  their projection in `list_attests`): historical rows on upgraded orgs are
  records, and the substrate never falsifies records. Writers die
  (`insert_attest` already stamps NULL); the columns become read-only
  history. The old-schema migration tests that prove column preservation
  survive with them.
- **Existing `producer_jobs` tables in upgraded databases**: the DDL leaves
  `ensure_schema`, so fresh databases never create the table; existing
  databases keep theirs as inert historical data — no `DROP`, for the same
  records reason. No code reads it.
- **The `external_producer` rule key** (rules.ex:263–267): it marks a
  verdict-fact gate as satisfied by a producer OUTSIDE the substrate — a
  concept this ruling strengthens, not weakens. Unchanged.
- **Remedy-producer vocabulary** (`producerKey`, `producer_id`,
  `producer_live?` in `rail_remedy.ex`) and the denial error schema's
  `producer` key — populated with the remedy's `producer_id` on
  `remedy_fired` denials (dispatch.ex:105) and carried as `producer: nil`
  in the denial shape (rules.ex:841, dispatch.ex:134): "producer" there
  names the session, assignment, or wake a remedy summoned — rails
  vocabulary with a different referent, and a wire error-schema key clients
  already read. Untouched, and the acceptance sweep is scoped so it never
  false-hits either.

Consumers' replacements: F1 coverage for evidence gates comes from
remedy-covered verdict facts and D2's artifact requirements; mechanical
verdict stamps are replaced by inference-filed verdict attests plus recorded
artifacts (provenance via the existing `bySession`/`byHarness`/`byProvider`
stamps); the retire-path cancel has nothing to cancel; `producers.toml`
becomes an unread file (§Migration).

### 6. Repeat and refusal

No new machinery. An agent that re-attempts completion while the papertrail
is missing hits the same statute; the live remedy episode rewakes the holder
with the pending-remedy sentence and increments `rewakeCount`
(rail_remedy.ex `rewake/10`) — the substrate prods, the record it demands is
unchanged. Sustained refusal is caught by the existing rungs, on their own
terms: statutes with `effect = "escalate"` open durable decision requests to
the owning human (escalation.ex), and a holder burning turns without
clearing the obligation is what the effort-without-effect check-in ladder
already escalates up its lineage rungs to the user (effort-checkin-v2). This
spec adds no counters, thresholds, or ladder edges. The two mechanisms can
hound the same agent simultaneously: a denied completion writes no attest
row, so it registers on none of the effort channels and neither mechanism
resets the other. Accepted — both are describing the same stall, from two
vantage points, to two audiences.

### 7. Bundle content and the arrival path

Consistent with neutral-seed-v1's bundle/receipt model: everything here is
bundle content, never seed.

- `rules/verification.toml` (§1) joins the bundle beside
  `rules/engineering.toml`; installed on learn, delivered to already-learned
  and grandfathered orgs by relearn, org-editable on `main` after either.
  The engine delta (§2) ships with the substrate — fact vocabulary is
  substrate schema, the fixed space.
- Bundle guidance is rewritten from the dead verbs to the papertrail:
  `coder.md` and `feature-cycle` teach verify-per-repo-prose, record the
  results artifact, file the `verified` verdict; `orchestrator.md`'s
  real-proof passage points at the verification statute instead of
  `run-smoke`; `spec-conformance` likewise. The kinds
  `tests-passed`/`real-run-passed` leave the bundle with the machinery that
  minted them.
- `intake.md` Q3 re-homes: the recorded answer is no longer
  `identity/producers.toml` but (a) the org's chosen verification verdict
  kind and artifact kind in `rules/verification.toml`, and (b) per-project
  verification prose in each repo's AGENTS.md.

## Rationale — the ruling worked through

The coupling law (§Ruling 3) is the negative case: what schemas break. The
positive case is what inference buys that no schema can:

- **Absence becomes work.** "Test this" succeeds against a project with no
  tests defined: the woken agent writes them, or escalates "should this
  project have them?". A script scheme's absence-semantics is failure;
  inference's is a dispatchable task. The remedy hound bootstraps
  verification into bare projects — schemas can only reference what already
  exists.
- **Unilateral evolution.** Adding a new obligation to a kungfu — say, lint
  — under any deterministic binding gates the school's growth on
  coordinating every project: each must learn the slot before the
  obligation can touch it. Under "wake and lint this," the new obligation
  deploys against every existing repo instantly, demanding nothing of them.
  Lockstep is the tax every schema charges.

Worked examples from the ruling dialogue, preserved — the dead ends
included, because they make the line legible:

1. **Write a sad poem.** No command exits 0 on sadness. This is the
   boundary case of the two-tier law: mechanical facts witness themselves
   (an exit status, an output file — recordable as artifacts), while
   judgment is witnessed only by another mind's attest. Both are
   papertrails; neither requires the substrate to act.
2. **The poetry org, end to end.** A poetry org verifies form mechanically
   with its own ~30-line `check_form.py` — the agent runs it and records
   the output as the results artifact — and verifies sadness by an editor
   session's verdict attest. Its completion statute is the engineering
   org's rule verbatim, with its own kinds substituted. Zero shared
   vocabulary between the two worlds, and the substrate knows neither.
3. **"Test this" with nothing to test.** See absence-becomes-work above:
   the agent writes the tests or escalates the question; a script scheme
   just fails, silently or loudly, with no path forward.
4. **The lint example.** See unilateral-evolution above: "wake and lint
   this" reaches every existing repo on the day the kungfu adopts it; any
   `lint:` slot requires every project to pre-support it — coupling every
   project to one kungfu's current shape.
5. **The `test:` toml anti-pattern chain.** A deterministic reader implies
   a component that KNOWS to look for `test:`. The kungfu renames the
   obligation to `smoke:` and every project breaks — silently, because a
   config reader has no way to say "I no longer understand this repo." The
   remedy sentence bridged by inference survives the rename untouched.
6. **The set-name fourth costume (failed design, preserved).** Splitting
   the binding across files — the archetype declares `gates = ["code"]`,
   the repo declares `sets.code = [...]` — looked like decoupling, but the
   set name `code` is the same repo↔kungfu dependency in its fourth
   costume: one mechanical token both sides must spell identically,
   breaking on rename exactly like its three predecessors. This is why the
   coupling law names tokens, not files.
7. **The reviewer-writes-a-review-doc chain (failed design, preserved).**
   Each hop of that design stacked another implicit proxy — a document
   standing for a judgment, a reader standing for the document — "making
   implicit what we can't say explicitly." Every proxy was a new silent
   coupling. The resolution is to say the requirement where it CAN be said
   explicitly: a statute demanding the verdict attest itself.
8. **The rail-check near-contradiction (resolved objection, preserved).**
   Read alone, this ruling seems to kill `[rule.check]` — the substrate
   forking an org script is the very thing forbidden. The resolution
   chain, each step a live objection: *Why a script instead of asking the
   agent?* Because the claimant cannot adjudicate its own claim, and "the
   agent forgot" is invisible from inside the agent — something has to
   notice, and noticing is deterministic. *Isn't the deny just asking the
   agent anyway?* Yes — the deny or remedy IS the ask; the script only
   decides when asking is needed and holds the claim open until the fact
   flips, so "done" never lands while false. *Then how does it differ
   from `run-smoke`, also a substrate-forked org script?* By what is on
   the other side of the fork: the check reads state that already exists;
   the smoke must perform the work to bring the answer into existence.
   That chain is where work-vs-checking (§Ruling 1) came from. The script
   is a sensor wired to the law, never an actor.

## Migration

Greenfield permissions hold (no production org until gibson); the two test
orgs are the whole upgrade surface.

- **One cut, no alias seam** (recommendation; timing is §Open 1). The verbs,
  handlers, runner, and CLI commands delete together; the CLI rebuild is
  part of the cut. shrdlu's and tars's identity repos are rewritten in the
  same cut: `producers.toml` deleted, relearn delivers the rewritten
  guidance and the new statute file.
- **`producers.toml` becomes inert.** Nothing reads it after the cut; a
  committed copy left in an un-rewritten org is dead weight, not an error.
- **Rules referencing the dead fact fail loud.** An org rule gating
  `assignment.produced_verdict_kinds` fails `Rules.load!` at boot with the
  unknown-fact error naming file and rule. No shipped rule uses the fact
  (`engineering.toml` gates independence facts only); the test orgs' rule
  files are checked and rewritten during the cut.
- **In-flight producer jobs.** Rows in `queued`/`running` at upgrade are
  simply stranded in the inert table; nothing recovers, fails, or re-runs
  them — the machinery that owned their lifecycle no longer exists, and
  their rows remain readable history.
- **Historical attests are untouched.** Producer-stamped verdict rows keep
  their stamps and keep satisfying `assignment.verdicts` gates exactly as
  any verdict attest does.
- **Spec-tree cut-step.** `p3-observables-producers-v1.md` claims authority
  over the producer subsystem; the cut narrows its authority line to
  observables and review-of and places the dated supersession banner at its
  §5 (done with this draft), and `producer-definitions-v1.md` is already a
  superseded stub. No other spec asserts authority over the deleted
  subsystem.

## Non-goals

- **No substrate execution surface, ever again** — no run-producer, no
  gates.toml, no witnessed execution, no artifact-content verification. The
  substrate records pointers and hashes (existing artifact registry); it
  does not grade evidence.
- **No verification schema, and no well-known verify slot.** No
  verify-command declaration in substrate or kungfu config — and,
  considered and REJECTED at this ruling (Flynn, 2026-07-29): a
  substrate-owned well-known verify-entry-point slot (a `.tightbeam/verify`
  file or key whose content a remedy sentence would quote). Its only
  distinct value would be substrate auto-execution, which the Principle
  rules out; absent that, it merely saves inference one README read while
  adding a permanent schema surface, convention pressure on repos, and a
  stale-pointer hazard. The remedy sentence IS the stable interface, and
  its payload stays natural language by design so nothing downstream
  ossifies.
- **No new escalation machinery** (§6): no rewake-count facts, no
  thresholds, no ladder changes.
- **No rules-algebra changes beyond §2** (one fact, one remedy-eligibility
  extension). `external_producer`, check-tier scripts, edges, and effects
  are untouched.
- **No forced identity migration and no history rewriting**: committed
  `producers.toml` files, historical attest stamps, and existing
  `producer_jobs` rows are left as records.
- **No CLI surface additions.** `attest`, `artifact-record`, and `attests`
  already carry the whole papertrail.

## Acceptance

- **A1 — the remedy wake, fail-before demonstrable.** On current main, a
  coder-held assignment with a `reviewed-clean` independent verdict
  completes with no verification papertrail. Post-spec, on a learned org:
  the same completion attest is denied `remedy_fired` by
  `completion-requires-verification`, and the holder receives a wake whose
  sentence names the missing verification verdict; after filing it, the
  next completion attempt is denied by
  `completion-requires-results-artifact` with a wake naming the missing
  results artifact. Each sentence names its own missing record.
- **A2 — the papertrail stands.** With a `verified` verdict attest filed and
  a holder-recorded `report` artifact on the work item, the completion
  attest passes, the assignment closes `completed`, and both remedy
  episodes close through the existing actor-owned close.
- **A3 — escalation on the ladder's terms.** With the remedy episode live,
  repeated back-to-back completion attempts — no intervening attest —
  produce rewakes with incrementing `rewakeCount` and no new episode (the
  precondition matters: an intervening attest, e.g. progress, is a gated
  call the statute no longer matches, which closes the live episode and
  resets `rewakeCount` on the next occurrence — pre-existing episode
  semantics, not this spec's); an org statute with
  `effect = "escalate"` on the same gate opens a decision request to the
  owning human through the existing escalation path, and the effort
  check-in ladder's behavior is unchanged by this spec (its existing suite
  stays green).
- **A4 — substrate vocabulary purge (exact, executable).** A test asserts
  `lib/tightbeam/producers.ex` does not exist, and that six files —
  `lib/tightbeam/rules.ex`, `lib/tightbeam/gateway.ex`,
  `lib/tightbeam/wire/router.ex`, `lib/tightbeam/assignments.ex`,
  `cli/src/args.rs`, `cli/src/dispatch.rs` — contain zero word-boundary
  matches of: `run-tests`, `run-smoke`, `cancel-producer-job`,
  `producer_jobs`, `producer_job`, `ProducerRunner`, `ProducerSupervisor`,
  `produced_verdict_kinds`, `producer_unconfigured`, `unknown_producer_job`,
  `producer_failed`, `tests-passed`, `real-run-passed`, and the quoted
  literals `"tests"` and `"smoke"`. The quoted clause is a regression
  tripwire, not a deletion check: the six files carry zero quoted matches
  even today — the config-key literals live only in the deleted
  `producers.ex`, and `rules.ex` reaches them as atoms — so the clause
  guards against the vocabulary re-entering, and the quoted form keeps it
  from false-hitting Rust `mod tests` or prose. The
  bare word `producer` is deliberately NOT swept: `attests.producer`
  columns are surviving history (§5) and remedy-producer vocabulary is a
  different referent.
- **A5 — a non-engineering org is never prodded.** A neutral-seeded org
  that never learned the bundle: an assignment is opened, held, and
  completed with a bare completion attest — no denial, no remedy episode,
  no wake, no verification-flavored event, nothing verification-shaped
  anywhere in its identity tree or event log.
- **A6 — engine delta unit coverage.** `assignment.artifact_kinds` resolves
  holder-recorded kinds, empty-list for a holder with none, nil for an
  unresolvable assignment; an artifact-gated remedy statute loads without
  `produces` (D2); a verdict-gated remedy statute still requires it.
- **A7 — smoke and platforms.** A1/A2/A5 run end-to-end through the real
  gateway + CLI before ready-to-verify (org smoke-coverage practice), on
  both macOS and Linux gateways, platforms named in the report.
## Open (for Flynn)

1. **Sunset timing of the legacy verbs.** Options: (a) one cut, hard
   deletion, test-org identity repos rewritten in the same change; (b) a
   fenced alias seam through gibson go-live (the superseded spec's shape).
   **Recommendation: (a).** The seam existed to keep un-relearned served
   guidance working mid-upgrade; with only deletable test orgs live and
   relearn shipping the rewritten guidance in the same cut, a compatibility
   seam is machinery for an imagined future.
2. **Fate of the producer_jobs machinery.** §5's verdict — full deletion;
   survivors are records only (attest stamp columns, inert historical
   tables) plus `external_producer`. Named open at the #90 gate, so stated
   here for confirmation. **Recommendation: confirm §5 as written** — no
   consumer with independent necessity was found, and nothing is kept for
   imagined futures.
3. **Scope of the requirement.** Org-wide (every completion) versus
   per-statute-scope (narrowed by conditions such as
   `assignment.holder_archetype`). **Recommendation: per-statute-scope, as
   shipped in §1** — the bundle narrows to implementation archetypes so
   reviewer completions are not artifact-gated, and scope remains an
   ordinary statute-authoring choice (org-editable conditions), not
   substrate policy. Widening to org-wide is deleting one condition line.
