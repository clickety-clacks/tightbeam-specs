# Coordination fabric — pragmatics record (2026-08-12)

Status: RECORD (sealed). Companion to `coordination-fabric-v1.md` (design
authority) and `coordination-fabric-ideation-2026-08-12.md` (provenance).
Captures the pragmatic Q&A of the same session that the spec compresses —
kept so the reasoning has a base to return to when drift sets in. Mike's
words: "i bet this shit will drift like crazy and we need a base to return to."

## Q: Does the fabric change substrate architecture?

No. Overwhelmingly seam-sharpening. The fabric is cheap BECAUSE rows +
computed-state + wakes + attests were built right — durable truth turned out
to be exactly the chassis a nervous system bolts onto. Inventory: office
pattern = existing role-address/assignment-holder seam, zero change; classes =
extend `attend`; input-needed = issue #11, additive; batcher = the ONE genuine
new mechanism (delivery-policy seam in wakes.ex); watchdog = retarget +
policyize existing supervision; subscriptions = wake-on-fact, exists;
directives = attests, exists; distribution = identity tree, exists. The only
architectural pressure is pre-existing: gateway split (5,694 lines) and read
path (#10, #12, #13).

## Q: How do we keep kungfu and substrate straight?

Physics / anatomy / culture. Physics = substrate mechanism: invariant,
judgment-free, domain-blind (test: does it exercise judgment or encode a
preference? then not physics — the adjudication ruling is the boundary
oracle). Anatomy = neutral seed: true in every domain but shipped as CONTENT,
reshapeable, unlearnable (test: could a sane org want to reshape it?).
Culture = kungfu (test: does it mention the domain?). One-liner: physics
never asks what the org values; anatomy is what every org starts with;
culture is what this org chose.

## Q: What's wrong / right-with-tweaks / right-spirit-wrong-body?

WRONG: almost nothing post-adjudication-deletion, except the live specimen —
the completion-selection gate wedged wi_1b0237fe (lifecycle row displaced the
holder's verdict) and CLI 0.1.7 exposes no agent-reachable repair verb.
Agents blocked by substrate bookkeeping with no lawful exit IS "the substrate
controls," arrived at by accident. Principle extracted: every substrate state
must have a lawful agent-reachable exit; repair requiring an admin at a
database console = incomplete design.

CORRECT AS-IS: rows/computed-state, holder-filed attests, work-items/
assignments, rails-as-executed-org-law, identity learn/relearn,
wake-carries-prompt, toplines, wake-on-fact, neutral-seed concept.

SPIRITUALLY CORRECT, EXPRESSED WRONG: supervision prods (right watchdog
instinct; hardcoded cadence prodding the WORKER — live false positive
observed 2026-08-12, prod seconds after a progress attest); `attend` (class
vocabulary in embryo — grow, don't replace); exception-based reporting (a
discipline agents pay inference to remember = a bone waiting to be
extracted); the PO archetype (spirit function right, plumbed as a traffic
sink); the read path (truth right, access wrong: no cursors, best-effort
doorbells, serialized reads).

## Q: What happens to the prodder?

Promoted, not deleted — it was a fabric bone before the word existed. Four
changes: (1) UNBRAID by the layer test — sweep mechanics/watermark guarantee
stay physics; thresholds, cadence, quiet-definitions, ladder shape become
anatomy defaults + culture overrides; the current hardcoded/data-driven mix
is an accident of which rules got parameterized first, not a design. (2)
RETARGET — prods land on the front desk where one exists; most terminate
there ("are you stalled?" is usually answerable from rows + directives;
false positives then cost exec-pennies, not Fable-turns). (3) INHIBITION
SEAM WITH A FLOOR — personal cadence tunable by directive, but the watchdog
FLOOR is skeletal: you can ask your desk to hold your calls; the org still
checks you're alive; nobody, including you, fully silences your own
life-signs monitor. (4) CLASSED OUTPUT — ladder height expressed as message
class; top rungs emit blocker/algedonic, which bypass batching by law.
Effort-without-effect stays separate: "productively busy?" is judgment and
rightly summons a mind; "alive?" never should.

## Q: What does the batcher/coalescer do?

A wake materializes a TURN — every delivery is a full inference pass at the
target's model price plus a context switch. Batcher decides WHEN (class →
immediacy; fyi holds to the target's next turn boundary; the NIC-interrupt-
coalescing move). Coalescer decides IN WHAT FORM (N held messages → one
signed digest turn: grouped, deduplicated, "×3, latest," pre-sorted by
actionability). Never touched: rows (every message individually durable —
lose a row and it's a bug); algedonic (pain doesn't wait). The seam in
action: digests sign themselves ("coalesced by progress-digest r1") so a
worker can inhibit exactly that rule for exactly that sender, instantly.

## Q: Where do the self-correction heuristics live?

RULED (Mike): they govern agents CODING Tightbeam, not org agents at runtime
— so not the neutral seed; the repo's AGENTS.md and CLAUDE.md (both — the
files had drifted and each harness reads its own), conspicuous, first
section. Landed as "THE PHILOSOPHY GATE — run it before you design, again
before you ship": ten litmus questions (who judges / can an agent say no /
what's the exit / does failure correlate / interruption or information /
which layer / decimation test / is the discipline a bone yet / does a status
question reach a mind / can you say it as a maxim). Branch
`docs/philosophy-gate`, commit e983d1f, docs gate (assemble.sh) green.
Merge = Mike's authorization.

## Q: Existing tickets?

wi_1100e078 ("Batch pending non-user notices into one agent turn while
preserving source rows", unstaffed) = Phase 1 seam ② in embryo, Law 2
already in its title — absorb, don't duplicate. wi_4ed08ef3 (HUDDLE — Main
as Mike's executive assistant, unstaffed) = independent draft of the class
vocabulary, the rows-not-prose context rule, and the directive metadata
schema — feed into §7 and §12; arguably folds into the Phase 3 pilot (Main
IS a front desk with Mike as principal). Third independent invention of the
fabric inside this org, after attend and exception-based reporting.

## Artifact manifest (as sealed; SHA-256 at time of writing)

| Artifact | Where | Hash/ref |
|---|---|---|
| coordination-fabric-v1.md (r2, design authority) | canonical NFS specs | de20462713c02053… (LIVING — hash will move with revisions) |
| coordination-fabric-ideation-2026-08-12.md | canonical NFS specs | fa005dbc2c8a6d03… |
| adjudication-deletion-amendment.md + 14 bannered specs | canonical NFS specs | amendment sweep verified 2026-08-12 |
| Philosophy gate (AGENTS.md + CLAUDE.md) | tightbeam repo, branch docs/philosophy-gate | commit e983d1f (UNMERGED — lost if branch deleted before merge) |
| Session memory (agent-first law, redesign thread) | gibson ~/.claude project memory | machine-local to gibson |
