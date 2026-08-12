# Coordination fabric — bones and cartilage — v1

Status: DRAFT r1 (2026-08-12). Authored from the ruled forks of
`coordination-fabric-ideation-2026-08-12.md` (retained as provenance; this file
supersedes it as design authority). Rulings: Mike, 2026-08-12. Not yet
spirit-reviewed; route through the normal review pipeline before
implementation.

> "Tightbeam is a machined part for binding agents together, not duct tape."

## 1. Problem

The org's most expensive judgment is spent on its cheapest traffic. Verified
2026-08-12 in `state.db`: the relief product owner's open cards were
lifecycle-repair procedure, custody relays, and review-cascade coordination —
System-2/3 work consuming a System-5 mind. Every knowledge worker is exposed
the same way. The scarcest resource in the org is frontier-model attention;
this spec is variety attenuation (Ashby) protecting it.

## 2. Governing laws (standing doctrine; this spec adds none)

1. **Agent-first.** Agents run the org. The substrate records truth, prods,
   and executes named org-authored law; it never judges, never seizes
   (adjudication deletion, 2026-08-05). The fabric below is a toolkit agents
   wield and delegate to — never a frame inference lives inside.
2. **Attenuate interruption, never information.** Every message still lands in
   durable rows. The fabric shapes *when inference is spent*, never *what is
   recorded*. A wrong reflex costs latency, never truth.
3. **No fabric state whose exit is someone's decision.** The fabric routes,
   batches, and summons; it never holds and never rules. A batched delivery
   exits on time or a turn boundary, nothing else.

## 3. Shape

**Bones** — deterministic coordination behaviors: defaults, cheap, fast,
load-bearing, correlated in failure and therefore kept small, boring, and
overridable. **Cartilage** — inference at the joints: small fast exec agents
judging the one question no table can ("does this change what my principal is
doing right now?"). Neither is over the other; they are composed, and every
bone carries an inhibition seam (§8). Deterministic failure is correlated —
correlated failure is what brittleness is — so anything with judgment content
is cartilage, not bone.

## 4. The office pattern (accountability — RULED)

No new substrate concept. Tightbeam already separates address from obligation:
a role resolves to a session at send time; an assignment's holder is pinned at
creation. The office exploits the seam:

- **Role binds to the front desk.** Wakes addressed to the role land on the
  exec session.
- **Obligations stay on the back desk.** The worker holds its assignment cards
  and files its own lifecycle attests — holder-filed doctrine untouched.
- **The delegation card is the written scope.** The exec holds exactly one
  assignment whose subject IS its bounded verb list (§6). Everything the exec
  does traces to that card; revoking it dissolves the office.

Failure modes degrade to today's topology: exec dies → role falls back per the
existing unstaffed rule, worker's cards unaffected; worker dies → normal
restaffing while the exec keeps triaging; card revoked → role rebinds to the
worker.

**Layering (ruled 2026-08-12, correcting r1's first draft):** the office is
domain-independent — as true of biosciences as of engineering — so it does NOT
live in domain kungfu. Three layers: (1) substrate MECHANISM — already exists
(role-as-address vs assignment-as-obligation, delegation card = assignment);
(2) **NEUTRAL SEED** — the pattern itself: the exec archetype, the office
convention, the delegation template, the base directive vocabulary — shipped
with Tightbeam as content, so an org can reshape or unlearn it (agent-first
survives; it could never decline a hard mechanism); (3) domain kungfu — only
the domain shaping: which archetypes warrant dedicated execs here, domain
directive vocabulary, cost tiers. Same mechanism/shared-vocabulary/domain-shaping
split as §5's bones — one layering everywhere. The substrate blesses "office"
as a first-class noun only if the pattern proves out (promote emergent practice
into architecture — the exception-based-reporting play).

## 5. Bones' home (RULED: substrate mechanism + kungfu policy)

The substrate ships neutral **behaviours**; each kungfu ships the **policy**
that configures them — the OTP behaviours-vs-callbacks split. Policy lives in
the identity tree beside rails, versioned, distributed by the same
learn/relearn lifecycle. The substrate stays calcium: it executes the org's
coordination law and owns none of it.

v1 behaviour set (deliberately minimal):

| Behaviour | What it does | Policy knobs (kungfu) |
|---|---|---|
| `classifier` | stamps inbound messages with a class (§9); unclassified → `fyi` | class vocabulary extensions, sender defaults |
| `coalescer` | N routine attests/messages → one digest | grouping keys, window |
| `batcher` | delivers non-urgent classes at turn boundaries | class → immediacy map |
| `status-responder` | answers `status-query` from rows (toplines/trace); the question never reaches a mind | scope of auto-answerable queries |
| `avasarala` | starvation watermark: open obligation quiet > X → escalate regardless of any gate (née prodder/watchdog — renamed r3; Expanse: the org's relentless prodder, escalates pain to the top) | thresholds per class/archetype |

`wake-on-fact` (S1) already exists and is the subscription bone; this spec
consumes it, not respecifies it.

## 6. Cartilage: the exec (front desk)

A small, fast, cheap-per-token model. Bounded verbs — the delegation card's
subject enumerates exactly these:

MAY: read substrate rows; file/consume attests on its own card; answer routine
queries answerable from rows; batch, schedule, and deliver to its principal;
summon its principal with a brief; escalate to rumination; tune its
principal's personal reflex policy on instruction (§8).

MUST NOT: file verdicts on substance; accept or reject work; make product
judgments; alter another principal's reflexes; hold anything — its only
"no" is "later," and the avasarala bounds every "later."

**Context (RULED): rows + standing directives.** The exec reads toplines,
attests, traces, and the directives its worker publishes. It never reads the
worker's transcript or workdir. The exec is told, not smart: gating quality
comes from directives, not from model capability.

**Standing directives** (v1, zero new rows): filed as attests on the
delegation card — durable, ordered, queryable; latest-wins per directive key.
Example: "deep in tune-CLI until art_X lands; interrupt only for review
verdicts on commit Y; digest everything else."

**Granularity:** archetype-elected, with cost-tiered kungfu guidance —
frontier-class workers warrant dedicated execs; cheap workers take bones-only
protection. Not a substrate decision.

## 7. Message classes (§5 `classifier` vocabulary)

Substrate-shipped base vocabulary; kungfu may extend, never remove:

- `fyi` — record only; digest at most
- `status-query` — auto-answered from rows; never reaches a mind
- `input-needed` — a decision is genuinely required; typed channel is
  decision-requests (issue #11's agent create-path is this class's carrier)
- `blocker` — progress stopped; front desk triages immediately
- `algedonic` — genuine pain (constitution violation, spirit drift,
  data loss): bypasses every bone and every desk, straight to the principal
  and/or the human. Never batched, never digested, never triaged.

Class is **advisory metadata extending `attend`** — sender-elected, receiver
re-classifiable, never a gate. Mis-classification costs latency (avasarala
bounds it), never truth.

## 8. The inhibition seam (override power — RULED)

Two kinds of reflex changes, two authorities:

- **Personal** (shapes only my attention: my digests, my batching, my DND):
  the affected agent, instantly, no permission — filed as a standing
  directive. The mind that overrides the reflex is the mind whose hand is in
  the fire.
- **Skeletal** (shared vocabulary, avasarala floors, org-wide routing): the
  normal law path — identity-tree edit, owner/PO authority, learn/relearn
  distribution. Nobody silences someone else's alarm.

**Legibility requirement:** every bone signs its work — a digest names the
rule that produced it ("coalesced by `progress-digest` r2") so any agent knows
which reflex to inhibit. An unattributable reflex is a bug.

## 9. Self-healing map (audit is circular by tissue)

| Failure | Caught by |
|---|---|
| bone misroutes | avasarala watermark (deterministic catches deterministic) |
| exec mis-gates | avasarala bounds the delay; worker feedback tunes directives |
| worker stalls | effort-checkin (exists) |
| fabric drifts systemically | rumination audits artifacts AND the fabric itself |
| genuine pain | algedonic class bypasses everything |

## 10. What the fabric must never do (anti-adjudication clauses)

No hold: nothing in the fabric ever blocks a turn, a completion, or an
assignment lifecycle. No rule: the fabric files no verdicts. No gate on
substance: an open decision-request is data its asker chooses to honor, never
a condition the substrate enforces — the moment a bone consumes one as a gate,
adjudication has been rebuilt with a friendlier face and this spec is void.

## 11. v1 scope and pilot

Pilot on the observed pain: **the product owner gets the first front desk.**
The PO becomes back-desk only — summoned for rumination cadence, spirit
verdicts, and algedonic signals; its exec fronts everything else under a
delegation card. Generalize to worker archetypes only after the pilot.

Acceptance (evidence, not vibes): (1) PO-session coordination turns drop
measurably (toplines/turn counts, before/after); (2) zero information loss —
every attenuated message still present in rows; (3) summon latency bounded —
no `input-needed`/`blocker` older than the avasarala floor without a summon;
(4) at least one personal override and one skeletal change exercised
end-to-end; (5) exec never files a substance verdict (audit its card).

## 12. Open gaps

- Directive schema: key vocabulary and precedence beyond latest-wins.
- Digest format: what a good brief looks like (the summon brief is the exec's
  craft; guidance, not mechanism).
- Class-vocabulary completeness per domain kungfu.
- Whether `status-responder` needs rate/abuse shaping.
- Metrics plumbing for acceptance №1 (turn counts by class exist in rows;
  a `toplines` cut may suffice).
- Promotion criteria for "office" as a substrate noun.

## 13. Implementation phases

Phases gate on EVIDENCE from the prior phase, never on schedule. Each phase
names its entry gate, contents, and exit evidence. §11's pilot is Phase 3;
everything "deliberately excluded from v0" is placed, not dropped.

**Phase 0 — the repair verb (entry: none; the wedge is live).**
Fix completion-selection to prefer the latest holder-filed verdict over
lifecycle rows; add the lawful agent-reachable exit (reopen/relink or
verdict-reselect). Exit: wi_1b0237fe unwedged via the new verb by an agent,
not an admin; a conformance fixture pinning holder-verdict-wins.

**Phase 1 — substrate seams (entry: Phase 0 merged).**
① `wake --class` with the five-class vocabulary (unclassified → `fyi`;
`algedonic` substrate-reserved, never batchable). ② Delivery-policy seam in
`wakes.ex`: class→immediacy table, turn-boundary digests materializing one
turn for N payloads, signed provenance. ③ decision-request create-path
(issue #11) as the `input-needed` carrier. ④ `--after` cursors on attests and
toplines (issue #13). Exit: conformance fixtures per seam; classes visible in
transcript and toplines; live feature-smoke green on both harnesses.

Existing carriers, absorb rather than duplicate: **wi_1100e078** ("Batch
pending non-user notices into one agent turn while preserving source rows" —
unstaffed) is seam ② in embryo, its title already carrying Law 2; its
narrower scope (substrate notices only) is a sane first increment before
classed agent traffic. **wi_4ed08ef3** (HUDDLE — Main as Mike's executive
assistant — unstaffed) independently drafted the class vocabulary (decision /
material-progress / stalled-work / release-risk digests), the rows-not-prose
context rule, and the typed metadata the directive schema needs — feed it
into §7 and the §12 digest-format gap. Third independent invention of the
fabric inside this org (after attend and exception-based reporting).

**Phase 2 — anatomy (entry: Phase 1 shipped; zero substrate changes).**
Neutral seed gains: the exec archetype, the office convention doc, the
delegation-card template (bounded verb list verbatim), the base directive
vocabulary. The philosophy gate lands in repo AGENTS.md/CLAUDE.md (done
2026-08-12, branch `docs/philosophy-gate`). Exit: `identity relearn` merges
the seed cleanly; a fresh org can stand up a front desk by convention alone.

**Phase 3 — the PO pilot (entry: Phases 1+2; §11 is this phase).**
Spawn the PO's exec, rebind the role, file the delegation card and first
directives; route supervision prods to desks where a desk exists. Baseline for
acceptance №1 is the 2026-08-12 `state.db`. Exit: the five §11 acceptance
criteria, plus an explicit owner ruling to generalize.

**Phase 4 — worker desks (entry: Phase 3 acceptance RULED, not just met).**
Generalize per cost-tier guidance (frontier-class workers first). Harden the
directive schema from pilot lessons (key vocabulary, precedence beyond
latest-wins). Unbraid the prodder: sweep mechanics stay physics; thresholds,
cadence, quiet-definitions, ladder shape move to anatomy defaults + culture
overrides in the identity tree. Exit: ≥2 worker archetypes running offices;
prod false-positive cost measured at desks; coordination share of worker
turns down against the Phase 3 baseline.

**Phase 5 — status-responder (entry: read path ready — #10 read
serialization fixed, #12 doorbell replay/cursor closed; #13 done in Phase 1).**
Auto-answer `status-query` from rows; rate shaping if abuse appears. Excluded
from v0 because it leans hardest on read-path guarantees. Exit: status
questions answered with zero mind-turns, with a stated freshness bound.

**Phase 6 — policy extraction (entry: a second consumer exists — the
rule-of-three moment).** Kungfu policy tables for classes, cadences, and cost
tiers in the identity tree; domain classifier extensions. Hardcoded seed
defaults stay the fallback. Exit: two kungfu (or two orgs) running different
policies on identical behaviours.

**Phase 7 — the office noun (entry: promotion criteria met).** Substrate
blesses "office" first-class: atomic desk rebind, desk recorded in
attribution, office-scoped queries. Promotion criteria (defining "proved
out"): ≥2 archetypes in offices across ≥4 weeks of live work, zero
accountability ambiguities in rumination audits, and a written list of the
convention's manual frictions that the noun would remove — the noun is
justified by friction observed, never by symmetry.

## Revision trail

r3 (2026-08-12): the watchdog behaviour is named **Avasarala** (Mike's
ruling; Tightbeam is Expanse-themed — port 11373 = 1373 gates + 1 Earth).
Supervision's prodder unbraids INTO this behaviour at Phase 4.

r2 (2026-08-12): §4 layering corrected (office pattern is neutral-seed
anatomy, not domain kungfu — Mike's catch); §13 implementation phases added,
evidence-gated, placing every v0 exclusion.

r1 (2026-08-12): authored from the ideation record plus four rulings
(accountability = office-as-convention; bones = substrate mechanism + kungfu
policy; exec context = rows + directives; override = self + spirit backstop).
