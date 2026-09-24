# Bounded guidance review: source 19eb9895 / tree 21581 plus staged live and legacy candidates

Review assignment: asg_23375f4e-e255-4bbe-8121-67d0222d58ab
Producer assignment: asg_06a5780a-2f21-44cb-ab84-94b993992197 (guidance writer s_2643a7d6)
Work item: wi_c13b63c8-b21f-47ce-bfac-61d51de854a4
Reviewer: guidance-reviewer session (claude-opus-5-5), independent of the producer
Date: 2026-09-24

Verdict: changes-requested. This is a bounded review. It is NOT an overall
reviewed-clean for the work item. No tests, gates or probes ran on Gibson or
anywhere else; this review read bytes and read-only state only.

## Subject and revisions

| Subject | Identity |
|---|---|
| Source worktree `alignment-source` | HEAD 19eb9895, tree 21581becff1f5a3b042a6d04a6055f761af8a03d, clean; base e28880d6; 24 files, +475/-319 |
| Staged live candidate | `alignment-evidence/live-candidate.patch` sha256 a437ffcb... |
| Staged legacy candidate | `alignment-evidence/legacy-candidate/SKILL.md` sha256 9d61c12b...; before copy 74c7b436... |
| Runtime wording handoff | `alignment-evidence/runtime-wording-handoff.md` sha256 1663473c... |
| Governing inputs | brief art_9a93de49 (e042b849), Mike questions art_5b91c742 (cf4fccb0), PO amendment art_30178d3e (6f4b14b8), topology art_250b81dd (032905f4) and v2 (0a1f6590) |

All listed hashes were recomputed and match.

## Evidence used and its limits

- Full composed reads of the source guidance, role kernels, includes and elected
  skills the change touches (pdo, orchestrator, product-owner, team-planner,
  coder, reviewers, guidance roles, archetype-roster, delivery-coordination,
  engineering-tenets, preferred-models, engineering-model-activities,
  capabilities, intake, manifests, operating-manual, guidance-policy-craft,
  wisdom-core).
- Live candidate compared against the currently published identity as projected
  into sessions; legacy candidate compared against the one active legacy copy
  found locally (`/home/mike/.claude/skills/tightbeam/SKILL.md`, 74c7b436).
- Read-only state.db queries for the live PDO population and model catalog.
- Lane 2 gate evidence (36b0798e, Racter gate report art_8215447b) read only as
  context. It is "prepared, not admitted" and does not establish anything here.

Limits: I did not verify emitted runtime bytes, fresh default session creation,
publication, receipt, or the second legacy active copy named by the publication
plan (not located locally). I judged guidance, not the Lane 2 runtime code.

## Findings

### Blocking

**F1. Legacy candidate removes the "PO where no PDO exists" fallback.**
Owner: guidance writer; PO/Main if the intent is contested.
The before text routes external requests to "(the PDO, or the PO where no PDO
exists)". The candidate says "(the PDO). If ownership is absent, have Main
arrange it first" and "Ask Main to identify or establish missing ownership."
The live org has PDO sessions only for Tightbeam (s_777369c7) and Engram
(s_417a6fb8). Clawline, surf-ace, atc, lachesis, agentd, looplens,
rest-state-api, headless-org-init and others have POs without a PDO. On
publication, every external request for those products gains a new
prerequisite: Main must first establish a PDO. That is a live routing change and
an added gate, contrary to Mike's Q1 ("no added gate") and to the publication
plan's own statement that neither change repoints Main or a legacy PDO.
Consequence: the legacy candidate cannot be published as staged.
Remedy: keep an interim route to the existing delivery owner or addressed PO
where no PDO exists, or obtain an explicit PO/Main ruling that the new
prerequisite is intended.

**F2. capabilities.md claims Claude-only support the activity rows no longer provide.**
Owner: guidance writer; PO decides whether Claude-only support stays.
capabilities.md still states "Activity-based model selection supports mixed,
Codex-only and Claude-only organizations", and shared preferred-models still
says to filter for mixed, Codex-only or Claude-only operation. The PDO,
executive/lane orchestration and both implementation rows now name only Codex
candidates (gpt-6-sol[low], gpt-6-luna[max], gpt-6-astra/gpt-6-sol). A
Codex-only PDO table exists; no Claude-only counterpart does, and the
single-family paragraph covers only specification and review. The same diff
also drops "or require a provider family" from guidance-policy-craft. A
Claude-only org following this bundle finds no qualified candidate for PDO,
orchestration or implementation and is blocked, while the offer says it is
supported.
Remedy (no new machinery): either list qualified Claude candidates for those
rows, or state the Claude-only limitation plainly in capabilities.md and the
selection guidance. Which one is a PO call.

### Post-mvp

**F3.** product-owner.md: "Work alongside that orchestrator" now refers to the
PDO; "Return that judgment to the responsible orchestrator" should name the
delivery owner. Owner: writer.

**F4.** team-planner and PO wording about the PO retaining an orchestrator sits
awkwardly with the roster's "PO opens no delivery assignments". Small ambiguity,
no blocked action. Owner: writer.

**F5.** operating-manual.md spawn example now carries engineering policy
(`--model gpt-6-sol --effort low`) into neutral substrate guidance, while the
same diff adds to guidance-policy-craft "Do not hardcode ... model policy into
the neutral substrate." Illustrative only, but self-contradictory within one
change. Prefer a neutral placeholder. Owner: writer.

**F6.** The engineering-tenets sentence on where product-level reporting stops
was removed; the roster and delivery-coordination now carry that routing.
Acceptable; noted.

**F7.** The Codex-only PDO table repeats the main row. Harmless redundancy.

**F8.** Pre-existing: capsule names claude-fable-5 while the catalog also offers
claude-fable-5-1. Not introduced here.

**F9.** Live pdo, orchestrator and coder manifests allow `["gibson","racter"]`,
but Racter offers no gen-6 model, so the defaults cannot run there. Known,
PO-acknowledged placement limitation; noted only.

## Answers to Mike's questions (art_5b91c742), bounded

- **Q1.** The legacy `--as-user` qualification is correct and adds no gate by
  itself. The candidate still fails Q1 because of F1. Recipient claims depend on
  Lane 2 Q4 evidence.
- **Q2.** The proposed notice text is neutral: it grants no authority and asks
  for no acknowledgement. The final emitted bytes are unverified.
- **Q3.** The gpt-6-sol/low PDO row supports consultation. Source and live
  manifests match the PO amendment (coder luna max; orchestrator and PDO sol
  low; spec-writer, reviewer-code and guidance-reviewer opus-5-5 high;
  reviewer-spec astra high; legacy reviewer.toml opus-5-5; coder second
  preference sol high within coder discretion). Fresh-default creation evidence
  is absent.
- **Q4.** Lane 2 evidence; open. 36b0798e is not admitted and Mike's audit found
  the engineering admission rule absent at 504825b3.
- **Q5.** The PDO election of human-communication is consistent for a
  user-facing intake owner; wisdom-core keeps "The operating manual owns routine
  reporting". The Lane 2 archetypes test encodes that single exception; at
  19eb9895 alone, test/archetypes_test.exs:305-328 still expects no pdo and no
  human-communication, which Lane 2 owns.

## Judgments that carry forward unchanged

- `topology-decided` verdict kind is supported (open text matching
  `^[a-z0-9][a-z0-9-]*$`, lib/tightbeam/assignments.ex:3287).
- No stale row names or superseded model ids remain in guidance ("deeper review
  row", "Adversarial specification", "Mixed-family", gpt-5.6-sol,
  claude-opus-5); remaining hits are tests, historical records and harness
  evidence.
- Include graph: archetype-roster included once via engineering-tenets (live
  candidate removes the separate include); delivery-coordination included once
  each by pdo.md and orchestrator.md.
- Manifest defaults match the PO amendment (Q3 above).
- Q5 composition judgment.
- Deliberate live differences are appropriate: org-local includes
  (no-testing-on-gibson, specs-home, specs-interim-durability, osanwe ruling),
  tightbeam-atc and human-communication elections, the delivery-records
  effect-kind paragraph replacing the tightbeam-dispatching dependency, the
  0.1.8 completion-requires-review wording, the engineering-model-activities
  pointer file, the manifest root corrected to orchestrator, and the trimmed
  team-design skill.
- The operating-manual "Explicit permission to add guidance" section matches the
  rule already in the live identity; the "the user" naming rule in craft is
  sound.
- The gibson-018 README reapplication boundary correctly marks the historical
  overlay as evidence, not a restoration payload.

These carry forward only while the reviewed bytes are unchanged. A revision that
touches the cited files needs a delta check of those hunks.

## Needs a later delta review

1. Runtime operation prose and CLI names, still held out of guidance
   (runtime-wording-handoff.md).
2. Installed-baseline and current-org comparison against the final candidate.
3. Fresh PDO default creation and provider receipt.
4. Final emitted notice bytes (Q2).
5. Live publication and receipt evidence, covering both applicable legacy active
   copies (only one located locally).
6. Q4 recipient behavior after an owner becomes unavailable.
7. Lane 2 test corrections at the final landed revision.
8. The writer's F1 and F2 corrections.
