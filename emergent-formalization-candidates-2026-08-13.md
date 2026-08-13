# Emergent behavior → formalization candidates (2026-08-13)

Status: SPEC INPUT for the 0.2 fold and workstreams 2-4. Source: one day of
live 0.1.x operation, reconstructed from rows. Each entry: the observed
emergent behavior, then the proposed formalization and its home.

## 1. Specimens → typed evidence attests (seed vocabulary + Miller's diet)
Observed: agents repurposed attests as evidence samples of substrate
misbehavior, with informal naming and context conventions. No vocabulary
supports this; specimens are found by grepping notes.
Formalize: an attest note-class or kind for `specimen` (typed, queryable,
carrying observed row ids). Aligns with the org's own never-worked item
wi_c4f5112b (grow attest vocabulary: note/finding/heuristic). Home: substrate
vocabulary (Phase 1-adjacent, additive) + seed guidance on filing discipline.
Payoff: Miller's C-probes read specimens directly instead of text-mining.

## 2. Stall classes + case law → Avasarala's real contract (Phase 4)
Observed: the stall patrol adjudicates every routed blocker against a learned
class taxonomy (Class 1-5), distinguishes "correctly blocked" from "actively
stalled," executes known recoveries, cites prior rulings as precedent, and
escalates only novel classes — one ring per class, taxonomy grows on ruling.
Formalize: fabric v1 specs Avasarala as a threshold watermark only. Phase 4
should adopt the richer contract: stall classes as DATA (seed base set,
org-extensible), adjudicate-before-escalate as the loop, and class-learned-
after-ruling as the ring-once guarantee. The 0.1.x patrol is the reference
implementation, running on inference; Phase 4 decides which parts become
bone.

## 3. "Correctly blocked" as first-class state
Observed: the patrol's most common verdict is that a card is lawfully waiting
on a precondition, and only inference can currently tell that from a stall.
Formalize: typed blocker rows (precondition + expected releasing fact),
letting wake-on-fact release them and letting watchdogs skip them without
judgment. Home: fabric §7 input-needed/blocker classes; ties to gh#11.

## 4. The no-acknowledgment law (immediate, free)
Observed: directive fan-outs generated hundreds of turns whose entire content
is "RECEIVED." Half of today's attests are comms-class.
Formalize: receipt is proven by the fired wake and the next filing; directives
must not request acknowledgment turns. Home: seed guidance + the fyi class
contract in fabric §7 (fyi never obliges a reply turn). Adopted for program
communications effective now.

## 5. Doorbell/record separation + notification dedup
Observed: agents self-enforced "the push is the doorbell, the row is the
record" and one-push-per-blockage with do-not-repeat-unless-materially-changed.
Formalize: external-notification dedup keyed on blockage identity as a
coalescer property (fabric §5); the maxim into seed guidance.

## 6. Quarantine-of-authority → security incident playbook (kungfu)
Observed: on credential exposure, agents separated EVIDENCE from AUTHORITY —
rows preserved immutable, their authority suspended pending owner ruling —
and self-imposed a notification moratorium with named exit conditions. All by
coordination, no substrate hold: the lawful form of a freeze.
Formalize: as an engineering-kungfu incident playbook (workstream 3), NOT as
substrate mechanism (a substrate authority-hold would re-create adjudication).
Include the credential-exposure protocol: never quote values, freeze by
convention, owner rules admissibility, rotation-or-acceptance as exits.

## 7. Verify-then-relay for authority messages
Observed: agents verified the announced commit hash before re-transmitting a
rule change downward, and issued corrections tree-wise.
Formalize: authority messages should carry a verifiable anchor (commit or
artifact hash); receivers verify before propagating. Home: seed guidance now;
optional later: a typed authorityRef on wakes.

## 8. The anti-busywork test
Observed: the patrol refused to create a receipt-only assignment: "that would
manufacture work."
Formalize: one line in seed guidance and the archetype playbooks: before
filing, ask whether the row RECORDS work or MANUFACTURES it. Candidate for
the philosophy gate's org-agent counterpart in workstream 3.

Disposition: items 1, 3, 5 are Phase 1-2 fold candidates; 2 is Phase 4's
reference contract; 4, 7, 8 are seed guidance (workstream 2-3); 6 is a
kungfu playbook. tb02 to absorb at the next fold sitting.

## The shipped-vs-emergent razor (RULED in discussion, 2026-08-13)

Observed law: every institution the 0.1 org invented was expressible in
shipped primitives alone. Fertilizer means keeping it that way.

- **Substrate (mechanism):** only domain-free, contentless floors whose
  absence fails silently. The starvation timer. Typed vocabulary. Batching.
- **Seed (template, content empty):** patterns proven in a live org whose
  SHAPE is domain-free but whose CONTENT is local. The nurse playbook with
  an EMPTY casebook. The specimen discipline and its vocabulary. Charter
  templates. An org can unlearn any of it.
- **Emergent (never ship):** anything learned from one org's failures.
  Class taxonomies, thresholds, rulings, staffing. Shipping these is the
  gh#8 disease at the knowledge level.

Case-law rot: casebook entries must cite their evidence and record their
hits (template requirement), so a class that stops matching is visible in
rows. Retirement stays a local judgment. Ship the ability to notice;
noticing is emergent.

The pipeline is the product: org invents → evidence accrues → proven
domain-free shapes promote to seed → contentless floors promote to
substrate. This document is one such promotion request.

## 9. The org invented its own Miller (noted 2026-08-13)
Observed: tenet-driven, row-cited, falsifiable audits already run in the 0.1
org — the churn-detection auditor session, the 2026-07-30 sample-then-act
and topology-probe audits (tenet → checks → quoted-evidence findings F1-F12
→ verdicts), and the forged-verdict catch as a live refutation probe.
Formalize per the razor: Miller ships as a SEED PLAYBOOK — the tenet-audit
discipline with an empty probe list. The program's C1-E8 probes are our
org's casebook content and never ship. Phase 5+ posture changes from build
Miller to formalize Miller; the reference implementation already runs.

### Division of labor: nurse vs Miller over the same casebook (ruled 2026-08-13)
The nurse works cases, synchronously: adjudicates, treats, and MINTS
provisional classes at the moment of encounter (ring-once requires a name
now). Miller works the taxonomy, asynchronously: merges and splits classes,
retires zero-hit entries, converts busy classes into repair demands (a high
hit count is a managed bug, not a triage success), and files promotion
requests for domain-free shapes. The casebook, with evidence links and hit
counts, is the shared artifact: the nurse writes it as a tool; Miller reads
it as evidence.

### Ruling by recommendation (RULED 2026-08-13 — the owner is not a queue)
Human adjudication of every promotion is a bottleneck and contradicts the
dark-factory ruling (humans only for genuine decisions). Promotion requests
therefore carry a recommendation, a risk tier, and a default:
- Tier 1, reversible housekeeping (retirements, demotions, seed guidance
  additions): the recommendation AUTO-EXECUTES with a durable notice; the
  owner may reverse after the fact.
- Tier 2, new shapes entering the seed (playbooks, patterns, vocabulary):
  default-executes at a stated deadline unless the owner objects; the
  notification carries the one-line recommendation so dissent costs one word.
- Tier 3, substrate mechanism, floors, or anything irreversible: explicit
  owner ruling, always. Rare by construction; the razor pushes nearly
  everything into tiers 1-2.
The owner's station in the pipeline is veto-with-context, not adjudication.

### Naming correction for the Phase 4 fold (ruled in discussion 2026-08-13)
Fabric r3 assigns the name Avasarala to the deterministic watermark bone.
Misassigned: the character is judgment, not machinery. At the fold, the name
moves UP to the role — Avasarala is the triage mind (the nurse: analysis,
treatment, minting, on-shift accountability) — and the bone beneath takes a
boring name, the starvation floor. General rule adopted: NAME THE MINDS,
KEEP THE MACHINERY BORING. A dramatic name on a deterministic component
invites people to expect judgment from it.

### Staffing at first boot (RULED 2026-08-13): the substrate never staffs
Names ratified: AVASARALA is the triage role (the nurse); THE PRODDER is the
deterministic starvation floor (the bone keeps the legacy name).
A fresh org, no kungfu learned, gets: the prodder always on, escalating to
Main (Main is the day-one nurse); both archetypes in the seed, charters
ready, casebook and probe list EMPTY; staffing TRIGGERS in seed guidance
(prodder ring-rate hires Avasarala; ledger depth / rumination cadence hires
Miller). No auto-spawn, ever — organs arrive when load demands and the org
decides, one spawn each. Ship the inevitability, never the employee.

## 10. Product inception SOP + the altitude rule (Mike's design, 2026-08-13)
SOP: product-scale request (from user OR agent) → huddle work item + spawn a
Product Owner → spirit interview → spirit CHARTER as a commons document
(invariants, non-goals, taste, boundaries), artifact-recorded and bound to
the product's work items via spec-ref → PO commissions an ORCHESTRATOR →
orchestrator builds and runs the graph; PO stands aside as judgment.
- Q1 ruled: spirit lives as a doc; substrate holds hash + spec-ref bindings.
- Q2 ruled: the user is summoned via the input-needed decision-request
  (gh#11 create-path, conversation anchor); PO drives a structured interview
  per playbook, STE comms; DR closes on charter ratification.
- Q3 ruled: PO judges, orchestrator coordinates. Orchestrator charter gains
  the lifecycle contract: owns the LIFETIME of its work items and their
  toplines (staffing, sequencing, review commissioning, dispositions) under
  the PO's spirit rulings. Graph-building craft = orchestrator playbook
  (workstream 3). The altitude rule ships as a seed STATUTE TEMPLATE orgs
  may arm: POs do not assign implementation cards directly; product work
  items carry an orchestrator. Evidence for need: 0.1 POs staffing coders
  and running reviews directly despite orchestrators existing.
Queue with the CR-001 fold batch (fabric r5 + workstream 3).

## 11. Exec containment (Mike's concern, 2026-08-13): cheap minds, environmental limits
Execs are fast, cheap, and untrusted for substance; never rely on their
judgment to know their limits. Three layers, none requiring exec wisdom:
(1) CAPABILITY: the exec home ships without means of production — no repo,
no workdir beyond own scratch, archetype-armed gates (no git, no edits).
A hard gate is CORRECT here: capability boundary, not judgment prohibition.
(2) LAW: the delegation charter's MUST-NOT list compiles into per-archetype
dispatch rules (bySession + archetype make it deterministic): no substance
verdicts, no holding/being-assigned implementation cards, no completions
off the delegation card, no spawning workers. Refused with the rule named.
(3) AUDIT: exec overreach is a specimen class; Miller probes it, effort-
checkin notices work-shaped token burn.
Razor: mechanism (archetype-scoped verb enforcement) is contentless
substrate; the restrictive matrix ships prearmed on the seed exec archetype;
orgs may loosen by ordinary law amendment. Queue with the CR-001 fold batch.

### 10b/11b correction (Mike, 2026-08-13): desks do the spawning; the office is the unit of hiring
Minds judge; desks execute. The inception flow corrected: the PO rules
"spirit ratified" and the PO's DESK spawns the orchestrator AND the
orchestrator's desk, wires PO-desk to orchestrator-desk, and binds the
charter. Worker hires likewise: the orchestrator decides shape and staffing;
ITS desk performs the spawns and wires each new office in. The nervous
system is not assembled after the fact — it is BUILT BY HIRING, because the
unit of hiring is the office (mind + desk), plumbed to the parent desk at
birth. Directives flow down the desk graph; summons bubble up it.
Item 11 amended: the exec no-spawn clause becomes spawn-as-directed-
execution — a desk spawn filing MUST cite the authority row (the
principal's recorded decision) and draw from seed office templates;
uncited spawns are refused by rule. Initiative stays with minds.
Graph-building mechanics (spawn + wire patterns) live in the DESK playbook
(seed, domain-free); shape judgment stays with orchestrator minds (kungfu).

### 11c: desk provisioning and notes (ruled in discussion, 2026-08-13)
Archetype manifests gain a provisioning election: desk-class homes ship with
no repo and only ephemeral scratch. A desk's notes are ROWS: working state
(directives, queues, tracking) lives as attests on its own delegation card,
latest-wins per key — survivable across restaffing, auditable, org-visible.
Nothing durable may live only in scratch; document-shaped durables are
artifacts. Zero new doctrine: projected homes are already declared
disposable; desks simply live that truth fully.

### 11d: one desk archetype, cost-elected pairing (clarified 2026-08-13)
The exec/desk is ONE seed archetype — desk craft is domain-free; per-pairing
specialization arrives via the delegation card and standing directives
(told, not smart), with optional kungfu flavoring. Pairing is not 1:1 by
rule but by economics (fabric granularity ruling): dedicated desk for
frontier-class minds, pooled desks for mid-tier squads, bones-only below.
Recursion terminates: desks have no desks — the prodder floor below and the
principal above are their only guardians.

### 11e: how desks bend (Mike's question, 2026-08-13) — identity composition, not prompts alone
A desk shaped only by runtime directives collapses into a policy
interpreter. Bending is LAYERED through the identity system: (1) seed desk
core, invariant craft; (2) kungfu desk guidance fragments, domain bend,
versioned via learn/relearn; (3) THE PRINCIPAL ARCHETYPE'S DESK FRAGMENT —
worker archetype manifests gain a desk section contributing to their
front desk's composed identity at office creation ("what my desk should
know about fronting a coder"); (4) standing directives, runtime, latest-
wins. One anatomy, bent by composition. The desk's inference exists to read
these layers over the bones and handle the residue no table can: conflict,
ambiguity, novelty. Layers 2-3 make the org's desk-craft durable,
reviewable, and promotable; layer 4 stays conversational.
