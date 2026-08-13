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
