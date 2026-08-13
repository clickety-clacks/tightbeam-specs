# Coordination fabric — bones and cartilage — v1

Status: r5 FOLDED (2026-08-13; executes the AUTHORIZED change requests
`0.2-change-request-001.md` §C and `0.2-change-request-002.md` D1–D9 —
both authorized by Mike, 2026-08-13 — in one fold sitting per their
terms; source log: `emergent-formalization-candidates-2026-08-13.md`).
Prior: r4 READY (2026-08-13; declared after the cross-vendor delta
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
protecting judgment. r5 extends the same protection into the org's shape:
expensive minds think, cheap desks coordinate, and the wiring between desks
— grown by hiring, never assembled — is the org's nervous system (§4).

## Non-Goals

The fabric will NEVER: judge substance or file verdicts; hold, gate, or
block any turn, completion, or assignment lifecycle (§10); own model policy
(adjudication deletion, 2026-08-05); read worker transcripts or workdirs;
replace supervision's liveness machinery or effort-checkin (it retargets and
policyizes the prodder, §5); introduce new substrate nouns in v1 ("office"
is a convention — and, at r5, the unit of hiring — until Phase 7's
promotion criteria are met); staff anyone — organs arrive when the org
decides, never by auto-spawn (Invariant 4, §8c); adjudicate promotions —
the pipeline's tiers are org-authored defaults that minds execute, and the
owner's station is veto-with-context (§8b); serve as a workflow engine that
contains inference. Out of scope for this spec: cross-org federation; UI
rendering of classes (Clawline's business); 0.1.x-line behavior.

## Terms

- **Principal** — the agent whose attention a front desk protects; the
  worker in an office.
- **Front desk / back desk** — the exec session the role binds to / the
  worker session holding the obligations.
- **Office** — the convention binding one exec (front desk) to one
  principal (back desk) via a delegation card — and, at r5, the UNIT OF
  HIRING: a hire creates mind + desk together, wired to the spawner's desk
  at birth (§4). Not a substrate noun in v1.
- **Desk graph** — the parent-to-child wiring of desks, built by hiring and
  never assembled after the fact; the org's nervous system. Directives flow
  down it; summons bubble up it (§4).
- **Delegation card** — the single assignment the exec holds; its subject
  enumerates the exec's bounded verbs (§6); revoking it dissolves the
  office.
- **Standing directive** — a durable, ordered, queryable instruction from
  principal to desk, filed as a directive-kind attest on the delegation
  card; latest-wins per directive key.
- **Dispatch rule** — org-authored, archetype-keyed verb law the substrate
  executes deterministically (bySession + archetype) over STRUCTURAL facts
  only — verb, attest kind, target card, authority reference — never
  content; a refusal names its rule (§6, §8). Mechanism is contentless;
  the matrix is org content.
- **Authority citation** — the row (attest or ruling) a desk's spawn filing
  must cite as the recorded decision it executes; an uncited spawn is
  refused by rule (§6).
- **Desk fragment** — the optional `desk` section of a worker archetype's
  manifest: a guidance fragment the principal's archetype contributes to
  its OWN desk's composed identity at office creation (§6b).
- **Obligation** — an open assignment, review, or decision-request a
  session holds.
- **Summon** — a wake the desk sends its principal carrying a brief;
  the desk's only way to spend the principal's turn.
- **Turn boundary** — the moment a session's in-flight turn ends; the
  org's natural delivery quantum.
- **Prodder** — the deterministic starvation floor (§5): the watermark bone.
  r5 rename (was "avasarala" r3–r4.3); the bone keeps the legacy
  supervision name. Same watermark contract, floors, and population — only
  the name changed.
- **Avasarala** — the triage ROLE (the nurse): a staffed MIND that
  adjudicates routed blockers over the casebook (§5b). Never machinery.
- **Miller** — the tenet-auditor role: conformance probing, effect
  evidence, promotion/demotion scouting (§5b, §8b, §13 Phase 5b). A seed
  playbook with an empty probe list; never machinery.
- **Casebook** — org DATA: the blocker-class taxonomy, one entry per class,
  each citing its evidence rows and recording its hit count. The nurse
  writes it as a tool; Miller reads it as evidence. Ships EMPTY (§5b).
- **Specimen** — an evidence filing citing observed rows: raw material for
  class minting and Miller's probes (§8b).
- **Provisional class** — a blocker class minted by the nurse at first
  encounter, so ring-once-per-class has a name to hang on (§5b).
- **Promotion tiers** — risk-tiered defaults on promotion requests: tier 1
  auto-executes with notice, tier 2 default-executes at a deadline, tier 3
  requires the owner's explicit word (§8b).
- **Spirit charter** — a commons document holding a product's invariants,
  non-goals, and taste rulings; artifact-recorded, bound to the product's
  work items via spec-ref (§6c).
- **Altitude rule** — PO judges, orchestrator coordinates; the orchestrator
  owns the lifetime of its work items and toplines (§6c). Seed statute
  template.
- **Watermark population** — the set of rows the prodder watches: open
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
   pattern without new mechanism through Phase 6 — amended at r5: except
   the named r5 increments (the manifest `desk` section + home-projection
   composition, §6b; archetype-keyed dispatch-rule enforcement and the
   provisioning election, §6), each a named build card, none a new noun.
6. The desk graph built by hiring suffices as the org's routing topology —
   directives down, summons up — with no new routing mechanism. Refuted if
   cross-tree traffic (desk to non-ancestor desk) dominates and forces a
   second wiring system.
7. Hit counts and evidence citations make case-law rot VISIBLE in rows
   (§5b). Refuted if stale casebook entries persist across Miller runs
   despite flat counts — noticing shipped but nobody could notice.
8. One desk archetype bent by composition (§6b) serves all principals.
   Refuted if a domain demonstrably needs desk anatomy that the four
   knobs cannot express.

## Invariants (governing laws; r5 adds the fourth)

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
4. **The substrate never staffs.** No auto-spawn, ever. Triggers are
   information; hires are a mind's ruling; spawns are a desk's cited
   execution of that ruling (§6, §8c). Ship the inevitability, never the
   employee.

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

**Naming law (r5, adopted from the 2026-08-13 ruling): NAME THE MINDS,
KEEP THE MACHINERY BORING.** A dramatic name on a deterministic component
invites people to expect judgment from it. Roles get characters (Avasarala,
Miller); bones get job descriptions (prodder, batcher, coalescer). This is
why r5 moves the name Avasarala UP off the §5 bone and onto the triage role
(§5b).

### 4. The office pattern (accountability + hiring — RULED; r5: the office is the unit of hiring)

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

**The office is the unit of hiring (r5, CR-002 D1).** A hire creates the
mind and its desk TOGETHER — one office, spawned from the paired seed
templates (role charter + desk delegation-card template) — and wires the
new desk to the spawner's desk at birth. The desk graph IS the org's
nervous system, and nobody builds the network: it grows as a side effect of
hiring, because no mind arrives unwired. Directives flow down the desk
graph; summons bubble up it. Spawn-and-wire mechanics live in the desk
playbook (seed, domain-free); WHO to hire and what shape the org takes stay
mind judgments (kungfu). A hire's desk may be dedicated, pooled, or absent
(bones-only) per §6's pricing — the unit is still the office; a bones-only
office simply has the prodder floor standing where a desk would.

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
obligation in the prodder watermark (60-min quiet floor) and under
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
restaffing decided BY THE WORKER'S PARENT/SPAWNER per existing restaffing
law — at r5 the parent MIND rules and the parent's DESK executes the
respawn, citing that ruling (§6); the worker's own exec cannot restaff its
principal (not in its verbs — the decision lives above it) but keeps
triaging and may summon or escalate; card revoked → the office is over in
authority; the role never rebinds itself — the dissolver rebinds (first,
per the ordering above). Restaffing a DESK costs one spawn and zero
knowledge: the successor reads the delegation card and resumes mid-shift,
because nothing lived only in the desk (§6, D4).

**Layering (ruled 2026-08-12; extended r5):** the office is
domain-independent, so it does NOT live in domain kungfu. Three layers: (1)
substrate MECHANISM — already exists (role-as-address vs
assignment-as-obligation, delegation card = assignment), plus the named r5
increments (§6, §6b); (2) **NEUTRAL SEED** — the pattern itself: the exec
archetype, the office convention, the paired office templates (role charter
+ desk delegation-card template), the desk playbook (spawn-and-wire,
notes-in-rows), the base directive vocabulary, the dispatch-rule template
with the prearmed exec matrix; (3) domain kungfu — only the domain shaping:
which archetypes warrant dedicated execs, domain directive vocabulary, cost
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
| `prodder` | starvation watermark over the WATERMARK POPULATION: any member quiet past its floor → escalate regardless of any gate. Population = open obligations (quiet = no attest) AND unanswered `input-needed`/`blocker` rows (quiet = no answer, consume, or summon since creation). A misclassified decision still enters the population the moment any mind re-classifies it upward; a decision misclassified `fyi` AND never re-classified is bounded by rumination audit (§9), not by the watermark — the fabric does not claim otherwise. (r5 rename, CR-001: was "avasarala" — the name moved up to the triage role, §5b; the bone keeps the legacy supervision name. Same watermark contract, same floors, same population — only the name.) | floors (pilot seed values; skeletal to change): 30 min for unanswered `input-needed`/`blocker`; 60 min attest-quiet for open obligations | thresholds per class/archetype |

`wake-on-fact` (S1) already exists and is the subscription bone; this spec
consumes it, not respecifies it.

**Policy skew rule (seed default):** a message carrying an extended class
the receiver's identity has no mapping for is delivered as `fyi` (never
dropped — Law 2; never promoted to immediate) and a named skew row is filed
so the vocabulary gap is visible and repairable. Fail quiet and visible.

**External-notification dedup (r5, CR-001 — coalescer property):** pushes
that leave the fabric for a human channel are keyed on BLOCKAGE IDENTITY —
one doorbell per blockage; a repeat only on material change. The push is
the doorbell; the row is the record (§7 carries the contract statement).
Dedup shapes interruption, never information (Law 2): every suppressed
push's content is already in rows.

### 5b. Avasarala, the triage role (anatomy — a staffed MIND, never machinery)

New at r5 (CR-001 item 2). The name moved UP from the §5 bone under the §3
naming law. Avasarala is the org's triage mind — the nurse standing on the
prodder's floor. She is STAFFED by the org when load demands (§8c), shaped
by a seed charter, and judged by her casebook. The substrate routes rows to
her and floors her waits; it never does her job.

**Charter template (seed content; the org reshapes or unlearns it):**

- **Adjudicate before escalate.** Every routed blocker gets her verdict,
  not her forward: she distinguishes CORRECTLY BLOCKED (lawfully waiting on
  a named precondition) from ACTIVELY STALLED — the distinction only a mind
  can currently draw.
- **Execute known recoveries.** Where the casebook holds a treatment, she
  applies it and files the outcome.
- **Cite precedent.** Rulings cite prior casebook entries; adjudication
  that never cites is the smell of a taxonomy nobody uses.
- **Mint provisional classes at encounter.** Ring-once-per-class requires a
  name NOW: a novel blocker is given a provisional class the moment it is
  met, so the second instance has something to match and the escalation has
  something to be once-per.
- **Escalate only novel classes.** One ring per class;
  class-learned-after-ruling is the ring-once guarantee.

**The casebook is DATA, never mechanism.** Entries MUST cite their evidence
rows and MUST record hit counts — so case-law rot is visible in rows (a
class that stops matching shows a flat count), and retirement stays a local
judgment. Ship the ability to notice; noticing is emergent. The seed ships
the charter with an EMPTY casebook — the shipped-vs-emergent razor (§8b):
shapes ship, one org's case law never does.

**Division of labor over the shared casebook (ruled 2026-08-13):** the
nurse works CASES, synchronously — adjudicates, treats, mints, carries
on-shift accountability — and writes the casebook as a tool. Miller works
the TAXONOMY, asynchronously — merges and splits classes, retires zero-hit
entries, converts busy classes into repair demands (a high hit count is a
managed bug, not a triage success), and files promotion requests for
domain-free shapes (§8b) — and reads the casebook as evidence. Same rows,
two altitudes; row provenance keeps their disagreements visible instead of
silent.

**Reference implementation:** the 0.1 stall patrol, running this whole
contract on inference today — a learned class taxonomy, correctly-blocked
vs stalled verdicts, executed recoveries, precedent citations,
escalate-only-novel. Its taxonomy is that org's case law and never ships.

Gate answers, said once: routing and floors are physics; the charter and
casebook SHAPE are anatomy; every entry's CONTENT is culture. The nurse can
be wrong, absent, or never hired and the prodder still escalates — the
floor never depends on the mind standing on it (Q7). When a class's
treatment becomes deterministic, extracting it to a repair verb is a demand
Miller files, never a seizure the substrate performs (Q8, Q1).

### 6. Cartilage: the exec (front desk)

A small, fast, cheap-per-token model. Bounded verbs — the delegation card's
subject enumerates exactly these:

MAY: read substrate rows; file its own lifecycle attests on its own card and
acknowledge directives there; answer routine queries answerable from rows;
batch, schedule, and deliver to its principal within §7's ceilings; summon
its principal with a brief; escalate to rumination; tune its principal's
personal reflex policy on instruction (§8); spawn offices from the seed
templates as DIRECTED EXECUTION of its principal's recorded decision — the
spawn filing cites the authority row (the attest or ruling it executes) and
wires the new desk to this desk at birth (§4; r5, CR-002 D2).

MUST NOT: file verdicts on substance (defined: any verdict-kind attest on a
card the exec does not hold, or any attest content accepting, rejecting, or
judging a work product); accept or reject work; make product judgments;
alter another principal's reflexes; restaff its principal; hold or RECEIVE
implementation cards — the delegation card is its only assignment; file
completions off the delegation card; spawn uncited — a spawn filing with no
authority citation is refused by rule, with the rule named; hold anything —
where "hold" is §Terms' definition: obligations, lifecycle transitions, and
verdicts are never delayed by the exec; delivery TIMING within §7's bounded
ceilings is the exec's job, not a hold. Its only "no" is "later"; every
"later" has a ceiling the BATCHER enforces by creating the delivery wake
(Invariant 3), and the prodder bounds starvation across its watermark
population (§5) — two different guarantees, neither claiming the other's.

**Minds decide, desks execute (r5, CR-002 D2).** A desk spawns only as the
directed execution of its principal's recorded decision — initiative stays
with minds. The citation requirement is not ceremony: it is what makes the
desk graph an execution layer instead of a shadow management layer. An
uncited spawn is exactly a desk exercising initiative, and it is refused by
rule (dispatch rule template in seed), with the rule named.

**Containment is environmental, three layers (r5, CR-002 D3).** Desks are
cheap minds we do not trust with substance, so their limits are walls, not
wisdom — none of the three layers requires exec judgment:

1. **Provisioning (capability).** Archetype manifests gain a provisioning
   election (desk vs workshop): desk-class homes ship with NO repository
   and only throwaway scratch — no means of production. A hard capability
   gate is CORRECT here: it is a capability boundary, not a judgment
   prohibition — the anti-cage rule (gate Q2) forbids caging judgment, not
   withholding tools from a role that must never use them.
2. **Law (dispatch rules).** The delegation charter's STRUCTURAL
   must-nots compile into per-archetype dispatch rules — deterministic
   (bySession + archetype), org-authored, executed by the substrate as
   named law over structural facts ONLY: verb, attest kind, target card,
   authority reference. The compiled set: no verdict-kind attests off the
   delegation card; no holding or receiving implementation cards; no
   completions off the delegation card; no uncited spawns. Refusals name
   the rule. The SEMANTIC half of the substance prohibition — attest
   content that accepts, rejects, or judges a work product in prose (this
   section's definition) — never compiles: enforcing prose semantics
   would require the substrate to read meaning, i.e. to judge (gate
   Q1/Q6); that half binds as law-as-text in the charter and is enforced
   by layer 3. The MECHANISM (archetype-scoped verb enforcement) is
   contentless substrate (candidates item 11); the restrictive MATRIX
   ships prearmed on the seed exec archetype, and any org may loosen it
   by ordinary law amendment (§8 — skeletal path, never a directive).
3. **Audit.** Desk overreach — including the semantic half of layer 2's
   prohibition, prose that judges a work product past the structural
   walls — is a specimen class Miller probes (§8b), and effort-checkin
   notices work-shaped token burn on a session that should only
   coordinate.

**A desk's memory is rows (r5, CR-002 D4).** Working state — directives,
queues, tracking — lives as attests on its OWN delegation card, latest-wins
per key: survivable across restaffing, auditable, org-visible.
Document-shaped durables become artifacts via artifact-record. Nothing
durable may live only in scratch — projected homes are already declared
disposable; desks simply live that truth fully. Restaffing a desk costs one
spawn and zero knowledge: the successor reads the card and resumes
mid-shift.

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

**One desk archetype; pairing is priced, not prescribed (r5, CR-002 D5).**
Desk craft is domain-free, so ONE seed archetype serves all principals —
per-pairing specialization arrives by identity composition (§6b) and
standing directives, never by new anatomy. Granularity is economics under
cost-tiered kungfu guidance, not substrate law: frontier-class minds
warrant a dedicated desk; mid-tier squads share a pool desk; the cheapest
workers take bones-only protection. Recursion terminates: **desks have no
desks** — the prodder floor below and the principal above are their only
guardians.

### 6b. How desks bend (identity composition, four knobs)

New at r5 (CR-002 D6, RATIFIED as the build target). A desk shaped only by
runtime directives collapses into a policy interpreter. Bending is LAYERED
through the identity system — one anatomy, bent by composition:

1. **Seed desk core** — the invariant craft (triage, batching,
   summon-writing, card discipline). Ships with the one desk archetype.
2. **Kungfu desk guidance fragments** — the domain bend: installed by
   `learn`, merged by `identity relearn`, pushed live by `identity apply`.
   Versioned, reviewable, org-shared.
3. **The principal archetype's desk fragment** — worker archetype manifests
   gain a `desk` section: a guidance fragment the principal's archetype
   contributes to its OWN desk's identity, composed into the desk's
   projected home at office creation — the coder's job description teaches
   the coder's receptionist. **This is the one real substrate mechanism
   change in CR-002**, specced here: (a) manifest schema — a worker
   archetype manifest accepts an optional `desk` section carrying a
   guidance fragment in the same format as kungfu desk guidance (absent =
   contributes nothing); (b) home projection — at office creation, the
   desk's projected home composes seed core, then kungfu fragments, then
   the principal archetype's `desk` fragment, in that order (later layers
   refine earlier ones; none deletes — Law 2's spirit applied to
   identity). Implementation is a NAMED BUILD CARD (Phase-2-class,
   queued with the recorded Phase 3 entry increments — §13), not this
   fold.
4. **Standing directives** — runtime, latest-wins per key (§6): the sticky
   notes.

Beneath all four, dispatch rules and gate statutes stay HARD: no layer of
guidance loosens a wall (§8 — the matrix moves by skeletal law only). The
desk's inference exists to read these layers over the bones and handle the
residue no table can: conflict, ambiguity, novelty. Layers 2–3 are the
point of the design: they make the org's desk-craft durable, reviewable,
and PROMOTABLE (§8b) instead of dying with a session's context window.

### 6c. Inception (how a product is born) and the altitude rule

New at r5 (CR-002 D7/D8). The SOP is seed guidance — a shape any org may
reshape; the spirit-interview protocol lives in the PO playbook; the
charter template lives in the commons conventions.

**The SOP:** a product-scale request — from the user OR an agent — opens a
huddle work item and spawns a Product Owner. The PO runs a structured
SPIRIT INTERVIEW: the requester is summoned via the input-needed
decision-request (the gh#11 create-path, with its conversation anchor), in
plain STE-style language; the decision-request closes on charter
ratification. The output is a **spirit charter**: a document in the spec
commons holding the product's invariants, non-goals, and taste rulings —
recorded via artifact-record and bound to the product's work items via
spec-ref (ruled: the spirit lives as a doc; the substrate holds hash +
bindings, nothing more). The PO rules "spirit ratified"; then the PO's DESK
spawns the orchestrator AND the orchestrator's desk, wires PO-desk to
orchestrator-desk, and hands over the charter binding — minds decide, desks
execute, from the very first hire (§4, §6).

**The altitude rule:** the PO judges; the orchestrator coordinates. The
orchestrator owns the LIFETIME of its work items and their toplines —
staffing, sequencing, review commissioning, dispositions — under the PO's
spirit rulings. POs do not assign implementation cards directly. Ships as a
seed STATUTE TEMPLATE an org may arm (anatomy: the org can decline the
statute; the orchestrator charter carries the norm either way). Evidence of
need: 0.1 POs staffing coders and running reviews themselves while
orchestrators sat idle — a System-5 mind doing System-3 work, precisely the
waste this spec exists to end (Goal).

**The six workflows (operational summary, CR-002):**

- **W1 Inception:** request → huddle + PO spawn → spirit interview
  (requester summoned by decision-request) → charter written, recorded,
  bound → PO ratifies → PO's desk spawns orchestrator + desk, wires the
  graph.
- **W2 Hiring:** orchestrator decides a role is needed → its desk spawns
  the office from seed templates, citing the decision row → new desk wired
  to parent desk at birth.
- **W3 A day at the desk:** triage inbound by class → batch the routine →
  summon the principal only for judgment → file everything on the card.
- **W4 Bending a desk:** ship it (seed) / learn it (kungfu) / inherit it
  (the worker archetype's `desk` section) / note it (standing directive).
- **W5 Violation path:** a desk oversteps → the filing is refused with the
  rule named → the refusal is specimen material → Miller's probes count it.
- **W6 Restaffing:** desk dies or is replaced → successor spawned from the
  same template reads the delegation card → resumes mid-shift; nothing was
  lost because nothing lived only in the desk.

### 7. Message classes (§5 `classifier` vocabulary)

Seed-shipped base vocabulary (anatomy, not physics — the class FIELD and
the behaviours are mechanism; the names and defaults below are seed
content). Kungfu may extend freely; reshaping or removing a base class is a
skeletal change (§8) — lawful via the identity tree, never silent.

| Class | Meaning | Seed immediacy (desk exists / no desk) | Ceiling |
|---|---|---|---|
| `fyi` | record only | digest at next turn boundary / same | 4 h |
| `status-query` | answerable from rows | desk answers from rows; principal never / rows answer (Phase 5), else parent | 30 min |
| `input-needed` | a decision is genuinely required; typed carrier is decision-requests (issue #11) | desk immediately; principal summoned with a brief no later than the prodder floor / principal at next turn boundary | prodder floor (30 min seed) |
| `blocker` | progress stopped | desk immediately; summon at desk's judgment, floor-bounded / principal immediately | prodder floor |
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

**The no-acknowledgment law's fabric anchor (r5, CR-001):** `fyi` NEVER
obliges a reply turn. Receipt is proven by the fired wake and the next
filing; directives never request acknowledgment turns. (Observed origin:
directive fan-outs generating hundreds of turns whose entire content was
"RECEIVED" — half a day's attests were comms-class. The class contract is
where the law becomes a bone's default instead of a discipline agents must
remember.)

**External-notification dedup (r5, CR-001):** notifications leaving the
fabric for a human channel are deduplicated on BLOCKAGE IDENTITY — one
doorbell per blockage, repeats only on material change. The push is the
doorbell; the row is the record. This is a coalescer property (§5), stated
here as the class-contract guarantee: a human never gets rung twice for the
same standing blockage, and never loses a row to the suppression (Law 2).

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
- **Skeletal** (shared vocabulary, base-class reshaping, prodder floors,
  org-wide routing): the normal law path — identity-tree edit, owner/PO
  authority, learn/relearn distribution. Nobody silences someone else's
  alarm.

**Dispatch rules and provisioning gates are skeletal by construction (r5,
CR-002 D3).** Per-archetype verb law and desk-class capability walls are
org law on the identity-tree path: the exec matrix ships prearmed on the
seed exec archetype, and loosening it is an ordinary law amendment — never
a standing directive. A desk cannot note itself past its own containment.
Every dispatch-rule refusal names its rule — refusal-with-the-rule-named is
how a wall stays a wall without becoming a judge.

**Legibility requirement:** every bone signs its work — a digest names the
rule that produced it ("coalesced by `progress-digest` r2") so any agent
knows which reflex to inhibit. An unattributable reflex is a bug.

### 8b. The promotion pipeline (the pipeline is the product)

New at r5 (CR-001 item 6; the razor and tiers ruled 2026-08-13). Observed
law from one day of live 0.1 operation: every institution the org invented
was expressible in shipped primitives alone. Fertilizer means keeping it
that way.

**The shipped-vs-emergent razor:**

- **Substrate (mechanism):** only domain-free, contentless floors whose
  absence fails silently. The starvation timer. Typed vocabulary. Batching.
- **Seed (template, content empty):** patterns proven in a live org whose
  SHAPE is domain-free but whose CONTENT is local. The nurse charter with
  an EMPTY casebook. The specimen discipline. Charter templates. An org can
  unlearn any of it.
- **Emergent (never ship):** anything learned from one org's failures —
  class taxonomies, thresholds, rulings, staffing. Shipping these is the
  gh#8 disease at the knowledge level.

**The pipeline:** witnesses file SPECIMENS (evidence filings citing
observed rows) → Avasarala MINTS provisional classes at encounter (§5b) →
evidence accrues in the casebook (hit counts, citations) → Miller
RECOMMENDS with a risk tier and a default (promotion scouting, §13 Phase
5b; demotion scouting is the mirror duty — shipped seed content no org
adopts, casebook entries gone quiet). Ruling by recommendation (RULED
2026-08-13 — the owner is not a queue; the dark-factory ruling reserves
humans for genuine decisions):

- **Tier 1 — reversible housekeeping** (retirements, demotions, seed
  guidance additions): the recommendation AUTO-EXECUTES with a durable
  notice; the owner may reverse after the fact.
- **Tier 2 — new shapes entering the seed** (playbooks, patterns,
  vocabulary): default-executes at a stated deadline unless the owner
  objects; the notification carries the one-line recommendation, so dissent
  costs one word.
- **Tier 3 — substrate mechanism, floors, anything irreversible:** the
  owner's explicit word, always. Rare by construction — the razor pushes
  nearly everything into tiers 1–2.

**The owner's station is veto-with-context, not adjudication.** And the
boundary that keeps this section lawful (§10): the tiers are org-authored
defaults that MINDS execute — Miller files the request, a mind lands the
tier-1/2 change, the owner vetoes or reverses — while the substrate only
records the request rows, the durable notices, and the deadline wakes
(wake-on-fact and scheduled wakes are the only machinery involved). The
moment a bone executes a promotion, adjudication has been rebuilt.

### 8c. First boot (staffing posture — ship the inevitability, never the employee)

New at r5 (CR-001 item 7; staffing ruled 2026-08-13). A fresh org, no
kungfu learned, gets:

- **The prodder, always on, escalating to Main.** Main is the day-one
  nurse: the floor guarantee exists from the first boot with zero staffing.
- **Avasarala and Miller seeded as ARCHETYPES, unstaffed.** Charters ready;
  casebook and probe list EMPTY (§5b, §13 Phase 5b — the razor).
- **Staffing TRIGGERS in seed guidance, never in mechanism:** a sustained
  prodder ring-rate is the trigger to hire Avasarala; ledger depth and
  rumination cadence are the trigger to hire Miller. The trigger is
  information; the hire is a mind's ruling; the spawn is a desk's cited
  execution of that ruling (§6).

No auto-spawn, ever — THE SUBSTRATE NEVER STAFFS (Invariant 4). Organs
arrive when load demands and the ORG decides, one spawn each.

### 9. Self-healing map (audit is circular by tissue)

| Failure | Caught by |
|---|---|
| bone misroutes | prodder watermark (deterministic catches deterministic) |
| exec mis-gates | prodder bounds the delay; worker feedback tunes directives |
| worker stalls | effort-checkin (exists) |
| nurse wrong, absent, or unstaffed | prodder floor escalates regardless — the bone beneath the mind (§5b) |
| desk oversteps | dispatch-rule refusal, rule named (§6); the refusal is specimen material Miller probes; effort-checkin notices work-shaped burn |
| case-law rot | flat hit counts visible in casebook rows; Miller retires (§5b) |
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
No staffing (r5): nothing in the fabric spawns a mind on its own initiative
— triggers inform, minds hire, desks execute cited spawns (Invariant 4,
§8c). No promotion execution (r5): tier defaults are executed by minds
under org law; a bone that lands a promotion has rebuilt adjudication
(§8b).

## 11. v1 scope and pilot

Pilot on the observed pain: **the product owner gets the first front desk.**
The PO becomes back-desk only — summoned for rumination cadence, spirit
verdicts, algedonic signals, AND aged `input-needed`/`blocker` per §7's
immediacy table (decisions reach the PO; the desk fronts everything else
under the delegation card). Until the r5 dispatch-rule mechanism ships
(§13), the exec matrix binds as seed convention — the delegation card's
verb list is the law's text either way.

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
   UNANSWERED and UNCONSUMED past the prodder floor (30 min seed)
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
5. RESOLVED at Phase 1 (was B: Phase 3 exit): metrics plumbing for
   acceptance №1 — the classed-row query landed with seam ① (build ledger,
   wave 1). Retained for the record.
6. (NB) Promotion criteria details for the office noun beyond §13 Phase
   7's list.
7. (B: the D6 build card) The `desk` fragment's exact manifest field
   shape and fragment format details — the build card decides WITHIN §6b's
   fixed composition order (seed core → kungfu → principal fragment →
   directives); the order itself is ruled, not open.
8. (NB) Pooled-desk mechanics: how one pool desk holds delegation cards
   for several principals without blurring §4's one-card-one-office
   accountability. Phase 4 evidence decides; until then pools are a
   priced option, not a built one.
9. (NB) Tier-2 deadline seed value (§8b): every promotion request must
   state its own deadline; whether the seed also ships a default duration
   is workstream 2-3 authoring.
10. (NB) Typed specimen attests and typed blocker rows
    (precondition + expected releasing fact — the "correctly blocked"
    first-class state, candidates items 1 and 3): NEXT-iteration seam
    candidates per CR-001 §B, deliberately not in the current build. Until
    then specimens are a filing discipline and correctly-blocked is the
    nurse's verdict (§5b).
11. (NB) Spirit-interview protocol details (question set, STE style
    guide): the PO playbook's business (workstream 3), not this spec's.

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

*r5 addenda (CR-001 + CR-002; Phase 2 landed pre-r5, so these are
Phase-2-class follow-on cards, authored before Phase 3 entry alongside the
two recorded entry blockers — the directive attest kind and the role-bind
CLI surface):* SEED — the paired office templates (role charter + desk
delegation-card template, §4); the desk playbook (spawn-and-wire mechanics,
notes-in-rows discipline, §4/§6); the dispatch-rule template with the
prearmed exec matrix (§6); the inception SOP + spirit-charter template +
PO-playbook spirit-interview protocol (§6c); the orchestrator charter's
lifecycle contract + the altitude statute template (§6c); the Avasarala and
Miller archetype charters, casebook and probe list EMPTY, + staffing
triggers in seed guidance (§5b, §8c). SUBSTRATE (named build cards, small
substrate increments at the Phase 3 entry): the manifest `desk` section +
home-projection composition (§6b — the one real mechanism change of
CR-002); the archetype-keyed dispatch-rule enforcement + provisioning
election (§6).

**Phase 3 — the PO pilot (entry: Phases 1+2; §11 is this phase).**
Spawn the PO's exec, rebind the role, file the delegation card and first
directives; route supervision prods to desks where a desk exists. The
before-window for acceptance №1 opens at Phase 1 ship (classed rows exist
from then). Exit: the five §11 acceptance criteria, plus an explicit owner
ruling to generalize.

**Phase 4 — worker desks + the nurse contract (entry: Phase 3 acceptance
RULED, not just met; r5 rewrite, CR-001 item 3).**
Generalize offices per cost-tier guidance (frontier-class workers first;
pooled desks and bones-only tiers per §6). Harden the directive schema from
pilot lessons (§12 Q1). Build the COALESCER (§5: sender+card grouping,
dedupe, "×3, latest" — scheduled here by r4.3; digest form starts to
matter at desk scale), including the external-notification dedup property
(§5, §7). **Build the nurse contract over the bare watermark:** the seed's
Avasarala charter (§5b) becomes operable — casebook discipline (entries
cite evidence rows, record hit counts), provisional-class minting at
encounter, adjudicate-before-escalate as the loop,
class-learned-after-ruling as the ring-once guarantee. The prodder floor
stays BONE beneath her: every §5 guarantee holds with the nurse unstaffed,
wrong, or dead — she reduces the interruption cost of escalations; she
never carries the floor. The 0.1 stall patrol is the reference
implementation; its taxonomy is that org's case law and never ships (§8b).
**Unbraid the prodder per the original plan:** sweep mechanics stay
physics; thresholds, cadence, quiet-definitions, and ladder shape move to
anatomy defaults + culture overrides in the identity tree (input:
`prodder-provenance-v1.md`, per the program's deferred ledger). Exit: ≥2
worker archetypes running offices; prod false-positive cost measured at
desks; coordination share of worker turns down against the Phase 3
baseline; at least one provisional class minted and one precedent-cited
adjudication visible in rows.

**Phase 5 — status-responder (entry: read path ready — #10 read
serialization fixed, #12 doorbell replay/cursor closed; #13 done in Phase 1).**
Auto-answer `status-query` from rows per §5's scope-and-degradation
contract; rate shaping if abuse appears. Excluded from v0 because it leans
hardest on read-path guarantees. Exit: in-scope status questions answered
with zero mind-turns, with a stated freshness bound; out-of-scope queries
demonstrably route to the desk with a named degradation row.

**Phase 5b — Miller, formalized (entry: the program's soak designation —
Phase 4 exit evidence recorded plus ≥2 weeks of live Phase-3/4 operation;
r5 rewrite, CR-001 item 4).**
Posture: FORMALIZE Miller, never build him — the reference implementation
already runs (the 0.1 churn-detection auditor and the 2026-07-30
tenet-driven, row-cited audits; the forged-verdict catch as a live
refutation probe). The seed gains the Miller playbook: the tenet-audit
discipline with three duties — conformance probing; effect evidence;
promotion/demotion scouting with the shipped-vs-emergent razor as its
rubric (§8b). The probe list ships EMPTY: the program's C1–E8 probes are
THIS program's local casebook content and never ship (the razor). Exit:
the playbook merged in the seed; run №1's evidence ledger exists as the
local reference output; the org's staffing trigger for Miller recorded in
seed guidance (§8c).

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
justified by friction observed, never by symmetry. An office-noun
promotion is tier 3 by definition (§8b): substrate mechanism, the owner's
explicit word.

## Spec-homing

Canonical set for this design: this file (design authority);
`coordination-fabric-pragmatics-2026-08-12.md` (sealed Q&A record);
`coordination-fabric-ideation-2026-08-12.md` (sealed provenance);
`v0.2-program-2026-08-12.md` (program record: workstreams, staffing,
phases); `review-gate-findings-2026-08-13.md` (review gate record + fold
rulings); `0.2-change-request-001.md` and `0.2-change-request-002.md`
(the authorized r5 change sets); `emergent-formalization-candidates-2026-08-13.md`
(the r5 source log: observed behaviors, the razor, the tiers, the naming
and staffing rulings — and itself the reference example of a promotion
request); `adjudication-deletion-amendment.md` (the boundary this spec must
never cross); `wake-on-fact-v1.md` (consumed primitive); `tightbeam.md`
(hub — may not lag this file).

## Revision trail

r5 fix round (2026-08-13, same day; Sol fold review, finding 3): §6 layer
2 sharpened — dispatch rules compile the charter's STRUCTURAL must-nots
only (verb, attest kind, target card, authority reference); the SEMANTIC
half of the substance prohibition (prose judging a work product) binds as
law-as-text in the charter and is enforced by layer 3's audit, never by
the substrate parsing content (gate Q1/Q6; candidates item 11's
contentless-mechanism ruling). Terms entry aligned. Finding 8 (bone still
named Avasarala in program-doc measurement text) fixed in the program
record, same sitting.

r5 (2026-08-13): the CR fold — executes `0.2-change-request-001.md` §C
(items 1–7) and `0.2-change-request-002.md` (D1–D9), both AUTHORIZED by
Mike 2026-08-13, one sitting, per the candidates log
(`emergent-formalization-candidates-2026-08-13.md`). NAMING: the §5 bone
renamed avasarala → `prodder` (same watermark contract, floors, and
population — only the name); AVASARALA moved up to the triage role (§5b,
new — charter template, casebook-as-data with mandatory evidence citations
and hit counts, provisional-class minting, empty seed content, the 0.1
stall patrol as reference implementation, the nurse/Miller division of
labor); the naming law adopted spec-wide (§3): name the minds, keep the
machinery boring. NEW SECTIONS: §6b how desks bend (identity composition,
four knobs; the manifest `desk` section + home-projection composition
specced as CR-002's one real mechanism change, implementation a named
build card); §6c inception + the altitude rule + workflows W1–W6; §8b the
promotion pipeline (razor, specimens → minting → tiered recommendations;
owner = veto-with-context); §8c first boot (prodder always on, Main the
day-one nurse, archetypes unstaffed, triggers in guidance). AMENDED: §4
(the office is the unit of hiring; the desk graph as nervous system, built
by hiring; restaffing text harmonized), §6 (spawn-as-directed-execution
with mandatory authority citation; three-layer containment —
provisioning/law/audit; desk memory is rows; one desk archetype, priced
pairing, desks have no desks), §7 (fyi never obliges a reply turn — the
no-acknowledgment law's anchor; external-notification dedup on blockage
identity), §8 (dispatch rules and provisioning gates skeletal by
construction), §9 (three new rows), §10 (no staffing; no promotion
execution), §11 (prodder naming; convention note until the dispatch
mechanism ships), §13 (Phase 2 r5 addenda; Phase 4 rewritten around the
nurse contract with the prodder kept bone and the r4.3 coalescer kept;
Phase 5b added — Miller formalized as a seed playbook, probe list empty).
Invariant 4 added (the substrate never staffs). Terms, Assumptions (5
amended; 6–8 added), and Open Questions (5 resolved; 7–11 added, B/NB
marked) updated. Sealed files untouched.

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
Supervision's prodder unbraids INTO this behaviour at Phase 4. (r5 note:
the name later moved up to the triage role; the bone reverted to the
legacy name `prodder` — §3's naming law.)

r2 (2026-08-12): §4 layering corrected (office pattern is neutral-seed
anatomy, not domain kungfu — Mike's catch); §13 implementation phases added,
evidence-gated, placing every v0 exclusion.

r1 (2026-08-12): authored from the ideation record plus four rulings
(accountability = office-as-convention; bones = substrate mechanism + kungfu
policy; exec context = rows + directives; override = self + spirit backstop).
