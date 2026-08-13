# Coordination fabric — bones and cartilage — v1

Status: r4 READY (2026-08-13; declared after the cross-vendor delta
re-check + its prescribed fix round — see `review-gate-findings-2026-08-13.md`).
Folded from the 2026-08-13 review gate
(`review-gate-findings-2026-08-13.md`: one Fable round, one Sol-xhigh round,
blind, both changes-requested; integrator rulings recorded there). r3 and
earlier authored from the ruled forks of
`coordination-fabric-ideation-2026-08-12.md` (retained as provenance; this
file supersedes it as design authority). Rulings: Mike, 2026-08-12; fold
rulings: integrator 2026-08-13, overridable.

> "Tightbeam is a machined part for binding agents together, not duct tape."

## Goal

Protect the org's scarcest resource — frontier-model attention — by shaping
WHEN coordination traffic spends a mind's turn, without ever shaping WHAT is
recorded. Verified 2026-08-12 in `state.db`: the relief product owner's open
cards were lifecycle-repair procedure, custody relays, and review-cascade
coordination — System-2/3 work consuming a System-5 mind. Every knowledge
worker is exposed the same way. This spec is variety attenuation (Ashby)
protecting judgment.

## Non-Goals

The fabric will NEVER: judge substance or file verdicts; hold, gate, or
block any turn, completion, or assignment lifecycle (§10); own model policy
(adjudication deletion, 2026-08-05); read worker transcripts or workdirs;
replace supervision's liveness machinery or effort-checkin (it retargets and
policyizes the prodder, §5); introduce new substrate nouns in v1 ("office"
is a convention until Phase 7's promotion criteria are met); serve as a
workflow engine that contains inference. Out of scope for this spec:
cross-org federation; UI rendering of classes (Clawline's business);
0.1.x-line behavior.

## Terms

- **Principal** — the agent whose attention a front desk protects; the
  worker in an office.
- **Front desk / back desk** — the exec session the role binds to / the
  worker session holding the obligations.
- **Office** — the convention binding one exec (front desk) to one
  principal (back desk) via a delegation card. Not a substrate noun in v1.
- **Delegation card** — the single assignment the exec holds; its subject
  enumerates the exec's bounded verbs (§6); revoking it dissolves the
  office.
- **Standing directive** — a durable, ordered, queryable instruction from
  principal to desk, filed as a directive-kind attest on the delegation
  card; latest-wins per directive key.
- **Obligation** — an open assignment, review, or decision-request a
  session holds.
- **Summon** — a wake the desk sends its principal carrying a brief;
  the desk's only way to spend the principal's turn.
- **Turn boundary** — the moment a session's in-flight turn ends; the
  org's natural delivery quantum.
- **Watermark population** — the set of rows avasarala watches: open
  obligations AND unanswered `input-needed`/`blocker` rows (§5).
- **Hold** — preventing or prolonging a substrate lifecycle transition or
  another agent's obligation exit. Delivery timing (batching to a turn
  boundary or ceiling) is NOT a hold.
- **Classes** — `fyi`, `status-query`, `input-needed`, `blocker`,
  `algedonic` (§7).
- Toplines, rumination, spirit verdict, identity tree, archetype, kungfu,
  wake, attest carry their standing substrate meanings (see
  `tightbeam.md`).

## Assumptions (falsifiable; Miller's E-probes test several)

1. The exec can gate well while "told, not smart": rows + standing
   directives suffice; model capability is not the binding constraint.
   Refuted if pilot desks mis-gate persistently despite tuned directives.
2. Turn-boundary delivery is almost always the right default for
   non-urgent traffic (the cheap-escalation-default rule). Refuted if
   bounded-latency complaints dominate pilot feedback.
3. Frontier-model attention is the org's scarcest resource and
   coordination traffic is its main waste (E1 tests this).
4. Coordination traffic is classifiable: the five classes cover it with
   `fyi` as a safe default (refuted if unclassifiable-but-urgent traffic
   appears).
5. The existing role-address/assignment-holder seam carries the office
   pattern without new mechanism through Phase 6.

## Invariants (governing laws; this spec adds none)

1. **Agent-first.** Agents run the org. The substrate records truth, prods,
   and executes named org-authored law; it never judges, never seizes
   (adjudication deletion, 2026-08-05). The fabric below is a toolkit agents
   wield and delegate to — never a frame inference lives inside.
2. **Attenuate interruption, never information.** Every message still lands
   in durable rows. The fabric shapes *when inference is spent*, never
   *what is recorded*. A wrong reflex costs latency, never truth.
3. **No fabric state whose exit is someone's decision.** The fabric routes,
   batches, and summons; it never holds and never rules. A batched delivery
   exits on time (its class ceiling) or a turn boundary, nothing else — the
   batcher CREATES the wake at whichever comes first; an idle session's
   digest materializes its own turn at the ceiling.

## Architecture

### 3. Shape

**Bones** — deterministic coordination behaviors: defaults, cheap, fast,
load-bearing, correlated in failure and therefore kept small, boring, and
overridable. **Cartilage** — inference at the joints: small fast exec agents
judging the one question no table can ("does this change what my principal is
doing right now?"). Neither is over the other; they are composed, and every
bone carries an inhibition seam (§8). Deterministic failure is correlated —
correlated failure is what brittleness is — so anything with judgment content
is cartilage, not bone.

### 4. The office pattern (accountability — RULED)

No new substrate concept. Tightbeam already separates address from obligation:
a role resolves to a session at send time; an assignment's holder is pinned at
creation. The office exploits the seam:

- **Role binds to the front desk.** Wakes addressed to the role land on the
  exec session.
- **Obligations stay on the back desk.** The worker holds its assignment cards
  and files its own lifecycle attests — holder-filed doctrine untouched
  (scoped: LIFECYCLE attests — progress, completion, surrender — are
  holder-only; directive-kind attests on a delegation card may be filed by
  the card's named principal, and by nobody else, refused by name).
- **The delegation card is the written scope.** The exec holds exactly one
  assignment whose subject IS its bounded verb list (§6). The card names its
  principal at creation. Everything the exec does traces to that card;
  revoking it dissolves the office.

**Dissolution and failover (v1: convention, non-atomic, degraded window
named; ordering corrected r4.1):** REBIND-then-revoke is a documented
two-verb sequence executed by the same authority (the principal or the org
actor dissolving the office). Order matters: revoking a card never changes
role binding (address and obligation are different seams), so revoke-first
would leave a window where the role routes to an off-card desk. Rebind
first puts the role safe on its next session; a crash between the verbs
leaves a bounded, explicitly governed DUAL-AUTHORITY window: the on-card
desk gets no new role traffic but may act on already-resolved/queued/
session-addressed work concurrently with the new desk — worst case a
duplicated delivery or summon (interruption cost, never truth, per the
error asymmetry; the exec's verbs cannot hold, judge, or file substance).
The window cannot persist quietly: the leftover card is an open
obligation in the avasarala watermark (60-min quiet floor) and under
effort check-in, and a desk that reads its role rebound away while its
card stands must stand down and surrender (seed exec guidance carries
the rule). In-flight batched traffic:
rows are durable (Law 2), digests are signed (§8); an undelivered wake
addressed to the ROLE re-resolves at send time per existing law; a wake
addressed to the dead exec SESSION follows the existing wake-delivery
lifecycle (delivered/failed terminal states). Atomic desk rebind is Phase
7's noun-promotion work, not v1's.

Failure modes degrade to today's topology: exec dies → role falls back per
the existing unstaffed rule, worker's cards unaffected; worker dies → normal
restaffing BY THE WORKER'S PARENT/SPAWNER per existing restaffing law (the
exec cannot restaff — not in its verbs — but keeps triaging and may summon
or escalate); card revoked → the office is over in authority; the role
never rebinds itself — the dissolver rebinds (first, per the ordering
above).

**Layering (ruled 2026-08-12):** the office is domain-independent, so it
does NOT live in domain kungfu. Three layers: (1) substrate MECHANISM —
already exists (role-as-address vs assignment-as-obligation, delegation card
= assignment); (2) **NEUTRAL SEED** — the pattern itself: the exec
archetype, the office convention, the delegation template, the base
directive vocabulary — shipped with Tightbeam as content, so an org can
reshape or unlearn it; (3) domain kungfu — only the domain shaping: which
archetypes warrant dedicated execs, domain directive vocabulary, cost
tiers. Same mechanism/shared-vocabulary/domain-shaping split as §5's bones —
one layering everywhere. The substrate blesses "office" as a first-class
noun only if the pattern proves out (§13 Phase 7).

### 5. Bones' home (RULED: substrate mechanism + seed vocabulary + kungfu policy)

The substrate ships neutral **behaviours** (mechanism — physics); the
**seed** ships the base vocabulary and default tables (anatomy —
reshapeable content); each kungfu ships the **policy** that configures them
(culture) — the OTP behaviours-vs-callbacks split. Policy lives in the
identity tree beside rails, versioned, distributed by the same
learn/relearn lifecycle. Hardcoded seed defaults are the fallback when no
policy row exists. The substrate stays calcium: it executes the org's
coordination law and owns none of it.

v1 behaviour set (deliberately minimal):

| Behaviour | What it does | Seed default | Policy knobs |
|---|---|---|---|
| `classifier` | guards elections: a sender's elected class is NEVER overwritten, and an unknown class receives fyi's POLICY plus a named skew row, never a rewrite (r4.3: ELECTION IS HOW TRAFFIC ENTERS THE FABRIC — wakes with no election are untouched legacy traffic, deliberately: auto-stamping would retroactively hold mail nobody elected; the classify seam exists in code for per-sender default elections when an org authors them) | unclassed → untouched; unknown class → fyi policy + skew row | class vocabulary extensions; per-sender default elections (the sender's own org-authored defaults, applied at send when the sender elected nothing) |
| `coalescer` | N routine attests/messages → one signed digest | group by sender+card, dedupe, "×3, latest" | grouping keys, window |
| | ^ SCHEDULING (r4.3): the coalescer ships at PHASE 4 — v1/Phase-1 digests carry every payload verbatim (form matters at desk scale, not before); §13 Phase 4 now names it | | |
| `batcher` | creates the delivery wake at min(next turn boundary, class ceiling) | ceilings: §7 table | class → immediacy map |
| `status-responder` | answers `status-query` from rows (toplines/trace) when the query is in its answerable scope; out-of-scope or rows-unavailable → files a named degradation row and routes the query to the desk (the cheapest mind), never silently drops (Phase 5; until then the desk answers from rows) | scope: toplines + trace reads | scope of auto-answerable queries |
| `avasarala` | starvation watermark over the WATERMARK POPULATION: any member quiet past its floor → escalate regardless of any gate. Population = open obligations (quiet = no attest) AND unanswered `input-needed`/`blocker` rows (quiet = no answer, consume, or summon since creation). A misclassified decision still enters the population the moment any mind re-classifies it upward; a decision misclassified `fyi` AND never re-classified is bounded by rumination audit (§9), not by the watermark — the fabric does not claim otherwise | floors (pilot seed values; skeletal to change): 30 min for unanswered `input-needed`/`blocker`; 60 min attest-quiet for open obligations | thresholds per class/archetype |

`wake-on-fact` (S1) already exists and is the subscription bone; this spec
consumes it, not respecifies it.

**Policy skew rule (seed default):** a message carrying an extended class
the receiver's identity has no mapping for is delivered as `fyi` (never
dropped — Law 2; never promoted to immediate) and a named skew row is filed
so the vocabulary gap is visible and repairable. Fail quiet and visible.

### 6. Cartilage: the exec (front desk)

A small, fast, cheap-per-token model. Bounded verbs — the delegation card's
subject enumerates exactly these:

MAY: read substrate rows; file its own lifecycle attests on its own card and
acknowledge directives there; answer routine queries answerable from rows;
batch, schedule, and deliver to its principal within §7's ceilings; summon
its principal with a brief; escalate to rumination; tune its principal's
personal reflex policy on instruction (§8).

MUST NOT: file verdicts on substance (defined: any verdict-kind attest on a
card the exec does not hold, or any attest content accepting, rejecting, or
judging a work product); accept or reject work; make product judgments;
alter another principal's reflexes; restaff its principal; hold anything —
where "hold" is §Terms' definition: obligations, lifecycle transitions, and
verdicts are never delayed by the exec; delivery TIMING within §7's bounded
ceilings is the exec's job, not a hold. Its only "no" is "later"; every
"later" has a ceiling the BATCHER enforces by creating the delivery wake
(Invariant 3), and the avasarala bounds starvation across its watermark
population (§5) — two different guarantees, neither claiming the other's.

**Context (RULED): rows + standing directives.** The exec reads toplines,
attests, traces, and the directives its principal files on the delegation
card (§4's doctrine scoping makes that filing lawful). It never reads the
worker's transcript or workdir. The exec is told, not smart: gating quality
comes from directives, not from model capability (Assumption 1 — the pilot
tests it).

**Standing directives** (v1, zero new rows): directive-kind attests on the
delegation card — durable, ordered, queryable; latest-wins per directive
key. v1 directive contract (minimum for the pilot; §12 Q1 tracks the rest):
a directive is `key: value` prose with a designated key from the seed
vocabulary (`focus`, `interrupt-only-for`, `digest`, `dnd-until`,
`escalate-to`); latest-wins per key; a directive with no designated key is
advice, not policy; cancellation = filing the key with value `off`.
Personal directives never override skeletal floors (§8).

**Granularity:** archetype-elected, with cost-tiered kungfu guidance —
frontier-class workers warrant dedicated execs; cheap workers take
bones-only protection. Not a substrate decision.

### 7. Message classes (§5 `classifier` vocabulary)

Seed-shipped base vocabulary (anatomy, not physics — the class FIELD and
the behaviours are mechanism; the names and defaults below are seed
content). Kungfu may extend freely; reshaping or removing a base class is a
skeletal change (§8) — lawful via the identity tree, never silent.

| Class | Meaning | Seed immediacy (desk exists / no desk) | Ceiling |
|---|---|---|---|
| `fyi` | record only | digest at next turn boundary / same | 4 h |
| `status-query` | answerable from rows | desk answers from rows; principal never / rows answer (Phase 5), else parent | 30 min |
| `input-needed` | a decision is genuinely required; typed carrier is decision-requests (issue #11) | desk immediately; principal summoned with a brief no later than the avasarala floor / principal at next turn boundary | avasarala floor (30 min seed) |
| `blocker` | progress stopped | desk immediately; summon at desk's judgment, floor-bounded / principal immediately | avasarala floor |
| `algedonic` | genuine pain (constitution violation, spirit drift, data loss) | bypasses every bone and every desk: delivered to the principal AND the org's configured human channel (seed default: both; skeletal to reshape). Never batched, never digested, never triaged | none — immediate |

Class is **advisory metadata extending `attend`** — sender-elected. The
classifier stamps only unclassified traffic (§5); a receiver may
RE-CLASSIFY for its own handling, recorded as its own row with the sender's
election preserved (Law 2) — receiver re-classification shapes the
receiver's delivery, and for `algedonic` it takes effect only AFTER the
first bypass delivery (nobody, including the receiver's bones, mutes an
alarm before it rings once). (r4.3: re-classification is a DESK behavior —
it ships with Phase 3's first front desk, recorded here so its absence in
Phase 1 is a deferral, not a hole.)

**Misclassification costs, stated honestly:** downward misclassification
(`blocker` sent as `fyi`) costs latency; the watermark bounds it once the
row is in the population, rumination audit bounds the remainder (§5).
Upward misclassification (`fyi` sent as `algedonic`) costs one bypass
interruption of the principal — receiver re-classification bounds
repetition from the same sender, and algedonic use is a standing rumination
audit item (§9); repeated abuse is a culture problem for a mind, never a
substrate gate. Neither direction ever costs truth.

### 8. The inhibition seam (override power — RULED)

Two kinds of reflex changes, two authorities:

- **Personal** (shapes only my attention: my digests, my batching, my DND):
  the affected agent, instantly, no permission — filed as a standing
  directive. The mind that overrides the reflex is the mind whose hand is in
  the fire.
- **Skeletal** (shared vocabulary, base-class reshaping, avasarala floors,
  org-wide routing): the normal law path — identity-tree edit, owner/PO
  authority, learn/relearn distribution. Nobody silences someone else's
  alarm.

**Legibility requirement:** every bone signs its work — a digest names the
rule that produced it ("coalesced by `progress-digest` r2") so any agent
knows which reflex to inhibit. An unattributable reflex is a bug.

### 9. Self-healing map (audit is circular by tissue)

| Failure | Caught by |
|---|---|
| bone misroutes | avasarala watermark (deterministic catches deterministic) |
| exec mis-gates | avasarala bounds the delay; worker feedback tunes directives |
| worker stalls | effort-checkin (exists) |
| never-reclassified downward misclass | rumination audit (standing item) |
| algedonic abuse | rumination audit (standing item) |
| fabric drifts systemically | rumination audits artifacts AND the fabric itself |
| genuine pain | algedonic class bypasses everything |

### 10. What the fabric must never do (anti-adjudication clauses)

No hold: nothing in the fabric ever blocks a turn, a completion, or an
assignment lifecycle. No rule: the fabric files no verdicts. No gate on
substance: an open decision-request is data its asker chooses to honor, never
a condition the substrate enforces — the moment a bone consumes one as a gate,
adjudication has been rebuilt with a friendlier face and this spec is void.

## 11. v1 scope and pilot

Pilot on the observed pain: **the product owner gets the first front desk.**
The PO becomes back-desk only — summoned for rumination cadence, spirit
verdicts, algedonic signals, AND aged `input-needed`/`blocker` per §7's
immediacy table (decisions reach the PO; the desk fronts everything else
under the delegation card).

Acceptance (evidence, not vibes; each clause decidable):

1. **Coordination-turn drop:** PO-session turns materialized by
   non-summon, non-algedonic wakes, as a share of all PO turns, drop ≥50%
   over the 7 days after desk stand-up vs the 7 days before it — both
   windows measured by the same query over classed rows (both
   post-Phase-1, so the method is identical; the 2026-08-12 `state.db`
   remains historical context, not the measure).
2. **Zero information loss:** every attenuated message present in rows —
   digest-member audit (C4) returns zero missing sources.
3. **Summon latency bounded:** no `input-needed`/`blocker` row still
   UNANSWERED and UNCONSUMED past the avasarala floor (30 min seed)
   without a summon or escalation row — a row cleared by answer, consume,
   or summon (§5's quiet definition) is satisfied, not a violation.
4. **Both seams exercised:** at least one personal override and one
   skeletal change end-to-end.
5. **No substance verdicts:** audit of the exec's card shows only its
   lifecycle attests and directive acknowledgments — zero verdict-kind
   attests on cards it does not hold, zero attest content judging work
   products (§6's definition decides).

Generalize to worker archetypes only after the pilot (Phase 4 entry is a
RULING on this acceptance, not just the evidence).

## 12. Open Questions

Marked blocking (B: blocks the phase named) or non-blocking (NB).

1. (B: Phase 4) Directive schema beyond the v1 contract: full key
   vocabulary, precedence beyond latest-wins, cross-key conflicts. v1's
   five-key contract (§6) suffices for Phase 3.
2. (NB) Digest format craft — what a good brief looks like: guidance, not
   mechanism; feeds from wi_4ed08ef3's drafts.
3. (NB) Class-vocabulary completeness per domain kungfu (Phase 6 evidence
   will show).
4. (NB) Whether `status-responder` needs rate/abuse shaping beyond §5's
   degradation rule (Phase 5 decides on evidence).
5. (B: Phase 3 exit) Metrics plumbing for acceptance №1: the classed-row
   query must exist before the pilot's before-window opens — build it in
   Phase 1 with seam ① (it is a read, not a new mechanism).
6. (NB) Promotion criteria details for the office noun beyond §13 Phase
   7's list.

## 13. Implementation phases

Phases gate on EVIDENCE from the prior phase, never on schedule. Each phase
names its entry gate, contents, and exit evidence. §11's pilot is Phase 3;
everything "deliberately excluded from v0" is placed, not dropped.

**Phase 0 — the repair verb (entry: none; the wedge is live).**
Fix completion-selection to prefer the latest holder-filed verdict over
lifecycle rows; add the lawful agent-reachable exit (reopen/relink or
verdict-reselect). Why this gates Phase 1: the pilot's delegation cards
ride the assignment lifecycle, and standing up new coordination machinery
on a lifecycle with a known unlawful-exit defect would build the fabric on
the one part of the chassis currently violating Law 3 — repair the chassis
first. Exit: the wi_1b0237fe wedge CLASS is exercisable via the new verb by
an agent in conformance tests (the live wi_1b0237fe card itself is 0.1.x's
to unwedge, by cherry-pick election); a conformance fixture pinning
holder-verdict-wins.

**Phase 1 — substrate seams (entry: Phase 0 merged).**
① `wake --class` with the five-class vocabulary (unclassified → `fyi`;
`algedonic` bypass per §7's seed default) + the acceptance-№1 classed-row
query (§12 Q5). ② Delivery-policy seam in `wakes.ex`: class→immediacy
table, ceilings, turn-boundary digests materializing one turn for N
payloads, signed provenance. ③ decision-request create-path (issue #11) as
the `input-needed` carrier. ④ `--after` cursors on attests and toplines
(issue #13). Ships WITH a minimal operating-manual amendment teaching the
classes and the create-path verb (rubric check 8; Phase 2 expands it).
Exit: conformance fixtures per seam; classes visible in transcript and
toplines; live feature-smoke green on both harnesses (deferrable only by
recorded ruling if no live gateway exists on the 0.2 line at the time).

Existing carriers, absorb rather than duplicate: **wi_1100e078** ("Batch
pending non-user notices into one agent turn while preserving source rows"
— unstaffed) is seam ② in embryo, its title already carrying Law 2; its
narrower scope (substrate notices only) is a sane first increment before
classed agent traffic. **wi_4ed08ef3** (HUDDLE — Main as Mike's executive
assistant — unstaffed) independently drafted the class vocabulary, the
rows-not-prose context rule, and the typed metadata the directive schema
needs — feed it into §7 and §12 Q1/Q2. Third independent invention of the
fabric inside this org (after attend and exception-based reporting).

**Phase 2 — anatomy (entry: Phase 1 shipped; zero substrate changes).**
Neutral seed gains: the exec archetype, the office convention doc (incl.
§4's dissolution sequence), the delegation-card template (bounded verb list
verbatim), the base directive vocabulary (§6's five keys). The philosophy
gate lands in repo AGENTS.md/CLAUDE.md (done 2026-08-12). Exit: `identity
relearn` merges the seed cleanly; a fresh org can stand up a front desk by
convention alone.

**Phase 3 — the PO pilot (entry: Phases 1+2; §11 is this phase).**
Spawn the PO's exec, rebind the role, file the delegation card and first
directives; route supervision prods to desks where a desk exists. The
before-window for acceptance №1 opens at Phase 1 ship (classed rows exist
from then). Exit: the five §11 acceptance criteria, plus an explicit owner
ruling to generalize.

**Phase 4 — worker desks (entry: Phase 3 acceptance RULED, not just met).**
Generalize per cost-tier guidance (frontier-class workers first). Harden the
directive schema from pilot lessons (§12 Q1). Build the COALESCER (§5:
sender+card grouping, dedupe, "×3, latest" — scheduled here by r4.3;
digest form starts to matter at desk scale). Unbraid the prodder: sweep
mechanics stay physics; thresholds, cadence, quiet-definitions, ladder shape
move to anatomy defaults + culture overrides in the identity tree. Exit: ≥2
worker archetypes running offices; prod false-positive cost measured at
desks; coordination share of worker turns down against the Phase 3 baseline.

**Phase 5 — status-responder (entry: read path ready — #10 read
serialization fixed, #12 doorbell replay/cursor closed; #13 done in Phase 1).**
Auto-answer `status-query` from rows per §5's scope-and-degradation
contract; rate shaping if abuse appears. Excluded from v0 because it leans
hardest on read-path guarantees. Exit: in-scope status questions answered
with zero mind-turns, with a stated freshness bound; out-of-scope queries
demonstrably route to the desk with a named degradation row.

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

## Spec-homing

Canonical set for this design: this file (design authority);
`coordination-fabric-pragmatics-2026-08-12.md` (sealed Q&A record);
`coordination-fabric-ideation-2026-08-12.md` (sealed provenance);
`v0.2-program-2026-08-12.md` (program record: workstreams, staffing,
phases); `review-gate-findings-2026-08-13.md` (review gate record + fold
rulings); `adjudication-deletion-amendment.md` (the boundary this spec must
never cross); `wake-on-fact-v1.md` (consumed primitive); `tightbeam.md`
(hub — may not lag this file).

## Revision trail

r4.3 (2026-08-13): completeness-scan fold (dual-vendor scan,
completeness-scan-2026-08-13.md). §5 classifier row rewritten to match
the shipped, review-accepted design — election is how traffic enters the
fabric; unclassed wakes are untouched legacy traffic (auto-stamping would
retroactively hold unelected mail); the classify seam remains for
org-authored per-sender defaults. Coalescer explicitly SCHEDULED at Phase
4 (it was named in §5 but scheduled nowhere — a spec defect). Receiver
re-classification recorded as a Phase 3 desk behavior (deferral, not
hole). Mike may overrule any of the three.

r4.2 (2026-08-13): §4 crash-window claim narrowed per Sol micro-review —
the post-crash state is a bounded, governed dual-authority window (not
"benign"): duplicated-delivery worst case named, watermark/effort-checkin
bounds named, exec stand-down rule added to the seed guidance.

r4.1 (2026-08-13): §4 dissolution ordering corrected — REBIND-then-revoke
(was revoke-then-rebind; revocation never changes role binding, so the old
order left the role routing to an off-card desk in the crash window; found
by Sol's Phase 2 review of the office-convention doc, which inherited the
defect from this section; both fixed in the same breath).

r4 fix round (2026-08-13, same day): three defects the Sol delta re-check
named, fixed as prescribed — §11.3 accepts answer/consume as lawful
clearing; §6's avasarala clause re-scoped to the watermark population
(batcher enforces ceilings, Invariant 3); §5 seeds the open-obligation
quiet floor (60 min) alongside the 30-min decision floor. READY declared.

r4 (2026-08-13): review-gate fold. Canonical structure added (Goal,
Non-Goals, Terms, Assumptions, spec-homing; Open Questions marked). Class
vocabulary re-layered seed-not-substrate with skeletal reshape path
(integrator ruling 2). Avasarala's watermark population defined over
obligations + classed rows; misclassification costs restated honestly.
Classifier stamps only unclassified traffic; sender election preserved.
Algedonic routing pinned (principal AND human channel, seed default).
"Hold" designated; exec verb list tightened (restaff excluded, substance
verdict defined). Directive v1 contract (five keys, latest-wins,
cancellation). Batcher creates the wake at min(turn boundary, ceiling) —
idle-session digests materialize their own turn. Office dissolution
sequence + degraded windows named. §11 summon set corrected; acceptance
made decidable (thresholds, windows, definitions). Policy-skew and
status-query degradation rules added. Phase 0 gate rationale stated;
Phase 1 ships its manual amendment.

r3 (2026-08-12): the watchdog behaviour is named **Avasarala** (Mike's
ruling; Tightbeam is Expanse-themed — port 11373 = 1373 gates + 1 Earth).
Supervision's prodder unbraids INTO this behaviour at Phase 4.

r2 (2026-08-12): §4 layering corrected (office pattern is neutral-seed
anatomy, not domain kungfu — Mike's catch); §13 implementation phases added,
evidence-gated, placing every v0 exclusion.

r1 (2026-08-12): authored from the ideation record plus four rulings
(accountability = office-as-convention; bones = substrate mechanism + kungfu
policy; exec context = rows + directives; override = self + spirit backstop).
