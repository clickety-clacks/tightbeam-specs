# Guidance delta re-review: d1ce1712 F1/F2 correction, staged live and legacy inputs

Review assignment: asg_d25e4b2e-910c-44a5-91cc-b1c132ad6897
Producer assignment: asg_06a5780a-2f21-44cb-ab84-94b993992197 (guidance writer s_2643a7d6)
Work item: wi_c13b63c8-b21f-47ce-bfac-61d51de854a4
Governing brief: art_e2d36e2f (sha256 20f516c1...)
Controlling PO ruling: att_0c9fceb4 / art_e37b6363 (sha256 ef5b1cc5...)
Prior review: art_0a19acff (df505d88...), addendum art_d485297c (19fa10e1...)
Reviewer: guidance-reviewer s_16e60e31 (claude-opus-5-5), independent of the producer
Date: 2026-09-24

Verdict: changes-requested, on one blocking finding (N1) that affects the staged
live candidate only. The changed source slice's F1, F2, F3 and F5 corrections are
sound and I would clear that slice on its own (scope below). This is not overall,
runtime, 0.1.9 or live acceptance. No tests, gates or probes ran anywhere; this
review read bytes and read-only state only.

## Subject and revisions

| Subject | Identity |
|---|---|
| Source `alignment-source` | HEAD d1ce171284cc27d78c7aded7b08ea507562fc820, tree 8610407742b1e40ad3f2c9912713ca218180d451, clean. Delta 19eb9895..d1ce1712 (commits 71823081, d1ce1712): 8 files, +51/-23, diff sha256 b3d5b296...; cumulative e28880d6..d1ce1712 sha256 0bdf032c... |
| Staged live candidate | `alignment-evidence/live-candidate.patch` sha256 bf0b6ce6...; applying it to `live-before.tar` reproduces `live-candidate/` exactly |
| Staged legacy candidate | `alignment-evidence/legacy-candidate/SKILL.md` sha256 140c2ae7...; before copy 74c7b436... |
| Active legacy copies | `/home/mike/.codex/skills/tightbeam/SKILL.md` and `/home/mike/.claude/skills/tightbeam/SKILL.md`, both 74c7b436... (unchanged, as expected before publication) |

All hashes above were recomputed and match.

## Evidence and limits

- Read the full delta and the complete affected source compositions: roster,
  intake, capabilities, shared and kungfu preferred-models, product-owner,
  orchestrator, operating-manual, the design doc and the manifest.
- Compared the live candidate to source file by file. Roster, capabilities and
  product-owner F3 lines match source. `engineering-model-activities.md` matches
  source kungfu `preferred-models.md` byte for byte from "Use shared" onward.
  The retained local differences (Engram section, omitted `identity current`
  line, 0.1.8 intake wording) are appropriate.
- Read Main's served composition in the live candidate
  (`archetypes/default.toml`, `guidance/default.md`) and the live Main session's
  archetype (`default`) from read-only state.
- Limits: source-only. I did not verify emitted runtime bytes, publication,
  session refresh, readback of either legacy copy after publication, fresh
  default creation, recipient behavior or admission. I did not review Lane 2 code.

## Answers to the brief

### 1. F1 across roster, intake, legacy and live copies

Corrected in text, consistent with the PO ruling (Main or an existing owner may
bootstrap the PDO; my earlier Q1 inference is withdrawn).

- Full facts and same item: roster requires the full request, facts,
  constraints, work-item identity and authorization state, and keeps a named
  agent accountable until the delivery owner explicitly accepts custody on the
  same work item. Intake points to that route. Met.
- File-only stays nonexecuting: "Preserve file-only requests as nonexecuting
  backlog." Met.
- Agent-owned bootstrap with explicit same-item acceptance: met in source text.
- Neither PO nor Main staffs production: "neither Main nor PO commissions
  production workers"; PO "opens no delivery assignments". Met.
- No user setup, reconfirmation, duplicate PO or lost obligations: "do not ask
  the user to set up routine seats, confirm again or repeat"; "Retain an existing
  addressed PO rather than creating a duplicate office." Incumbent obligations
  are preserved by the operating manual's existing handoff rule. Met.
- `--as-user` authority contract and separate neutral CLI: legacy lines 20-77
  unchanged; the "no parent" claim is now qualified; the PO-where-no-PDO bullet
  routes through bootstrap. Met.

Exception: N1 below, for the live candidate.

### 2. F2 single-harness limits

Corrected in both directions. capabilities.md states the complete workflow needs
both Codex and Claude and points to preferred-models. Shared preferred-models
filters on the activity table's explicit family limitations and says a candidate
for one activity does not establish the complete workflow. The kungfu
preferred-models paragraph names what Claude-only and Codex-only operation cannot
supply. Sol6-low PDO and orchestrator, Luna6-max coder discretion, Opus 5.5 high
specification, and review on the harness opposite the actual producer are all
preserved. The live copies match.

### 3. F3, F5, examples and carry-forward

- F3 fixed: all three product-owner referents now read "delivery owner".
- F5 fixed: the operating-manual spawn example uses neutral placeholders.
- The two new acceptance rows (docs 725-726, no-PDO intake and single-harness
  limits) are consistent with the guidance.
- F4, F6, F7, F8, F9 carry forward unchanged. The prior carry-forward judgments
  in art_0a19acff stand where their bytes are unchanged, plus the spawn-seam
  credit in art_d485297c.

### 4. Scope statement

See the verdict and "Scope of the clean slice" below.

## Findings

### Blocking

**N1. The live candidate routes bootstrap to a Main that never receives the duty.**
Owner: guidance writer; PO/PDO adjudicate the remedy.
The roster assigns bootstrap to "Main or the existing owner", with its limits:
reuse a delivery owner or establish the smallest PDO/PO arrangement, commission
no production workers, keep intake accountable until explicit same-item
acceptance, and do not ask the user to set up routine seats. In the shipped
bundle this fits, because the bundle root is `orchestrator` and orchestrator.md
covers executive scope and reads the roster. On Gibson the live Main session runs
archetype `default`. The live candidate leaves `default.toml` and `default.md`
unchanged, and neither includes the roster or engineering-tenets. The only
related text Main receives is "Main is not a fallback worker" (shared
preferred-models). `default.md` also tells Main to bring offers to the user and
"do it for them if they say yes", which invites the user setup step the roster
forbids.
Consequence: for intake that enters through Main, or that a PO routes to Main
when no PDO exists (most live products), Main acts without the bootstrap limits.
The F1 behavior the brief requires is not served to the agent it names, so the
live candidate cannot be accepted for F1 as staged.
Remedy, proportionate, writer's and PO's choice: give live Main the roster (a
short pointer or include in the org-local `default` composition), or name the
live bootstrap owner that does receive it, or state the limitation plainly in the
live candidate with a PO ruling accepting it. No new mechanism is needed.

### Post-mvp

**N2.** The legacy candidate says "using the served engineering roster's
bootstrap route". External operators do not see that roster. The following
sentences are enough on their own; the pointer could go. Owner: writer.

**N3.** docs/engineering-kungfu-019-consolidation.md lines 120-121 ("complete
single-family fallback orders") and 130-133 ("Same-family independent review
remains eligible, including single-family organizations") contradict the new
acceptance rows and the opposite-harness rule. They predate this delta, and no
priv/ file or served identity references the doc. Owner: writer.

## Scope of the clean slice

If N1 is resolved or accepted by PO ruling, my judgment of the changed source
slice 19eb9895..d1ce1712 (8 files) is clean. That judgment covers guidance text
only. It is not overall acceptance of the work item, not runtime or 0.1.9
acceptance, and not live acceptance.

## Still needs later delta review (Lane 2 or publication)

1. Runtime operation prose and CLI names (runtime-wording-handoff.md).
2. Installed-baseline and current-org comparison against the final combined
   candidate.
3. Shipped-bundle fresh PDO defaults from the learned package manifests, the
   omitted-archetype path, and a real host or provider receipt.
4. Final emitted notice bytes.
5. Publication and readback of the live identity and both legacy copies.
6. Q4 recipient behavior, admission, and Lane 2 tests at the landed revision.
7. How explicit same-item custody acceptance is carried on 0.1.8 (which record
   shows it), for the intake route.
8. N1 correction.
