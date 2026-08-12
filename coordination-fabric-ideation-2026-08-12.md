# Coordination fabric — ideation record (2026-08-12)

> "Tightbeam is a machined part for binding agents together, not duct tape."
> — Mike, setting the design bar. The executive-assistant idea is a variety
> attenuator protecting scarce inference: not duct tape, the correct machined
> part.

Status: IDEATION — SUPERSEDED as design authority by
`coordination-fabric-v1.md` (same day; the four open forks below were ruled and
folded in). Retained as provenance. Pre-spec discussion record (Mike + Claude,
2026-08-12), not law, not reviewed, deliberately dense.

## Problem

The product owner — the org's spirit enforcer and rumination seat, staffed with
the most expensive judgment available — is inundated by its subgraph's
coordination traffic. Verified in `state.db` 2026-08-12: the relief PO's open
cards were lifecycle-repair procedure, custody relays, and review-cascade
coordination, not spirit work. Every knowledge worker (coder, reviewer,
spec-writer) is exposed the same way. The scarcest resource in the org is
frontier-model attention. Ashby's Law of Requisite Variety names the problem: a
controller must absorb the variety of what it controls. Simon names the cost: a
wealth of information creates a poverty of attention. The design problem is
variety attenuation protecting scarce judgment.

## Laws that bound any design (standing Tightbeam doctrine)

1. **Agent-first.** Agents run the org; the org does not run them. The
   substrate records truth, prods, and faithfully executes named, visible,
   org-authored law — it never judges and never seizes (precedent: the
   2026-08-05 adjudication deletion; a named-rule refusal is the org's law
   speaking through the substrate, not the substrate deciding). Rationale:
   resilience to change, exceptions, fault, and decimation.
2. **Attenuate interruption, never information.** State is computed from
   durable rows; the fabric shapes *when inference is spent*, never *what is
   recorded*. A wrong reflex costs latency, never truth.
3. **No substrate state whose exit is someone's decision.** The fabric routes,
   batches, and summons — never holds, never rules. A batched wake exits on
   time or a turn boundary. Cross this line and adjudication is rebuilt with a
   friendlier face.

## Shape: bones and cartilage — not tiers

Not strata with one over the other; tissues, composed.

**Bones — deterministic coordination behaviors.** Message classes as
first-class data (`fyi`, `status-query`, `input-needed`, `blocker`,
`algedonic`) with declarative handling: coalescing (N progress attests → one
digest), delivery batching at turn boundaries (the org's natural quantum —
interrupt coalescing / Linux NAPI: under load, stop interrupting, switch to
polling), `status-query` auto-answered from rows (toplines exists because the
substrate already knows; a status question should never reach a mind),
wake-on-fact subscriptions instead of polling, dedup, starvation watermarks.

**Cartilage — inference at the joints.** Small fast exec agents judging the one
question a table cannot: *does this change what my principal is doing right
now?* Verbs deliberately bounded: file/consume attests, answer routine queries,
batch and schedule delivery, summon the principal with a brief, escalate to
rumination. Never: verdicts on substance, accepting/rejecting work, product
judgment.

**Every bone is a default with an inhibition seam.** Any mind can override,
install, tune, or revoke any reflex (the withdrawal reflex screams to pull the
hand from the flame; descending pathways let the mind override to save a
puppy). Deterministic failure is *correlated* — a wrong rule wrongs every
message identically, silently, forever — and correlated failure is what
brittleness IS. Inference failure is uncorrelated and self-noticing. Hence the
fabric must be both: bones for form, cartilage for give.

**Containment inversion.** In failed systems the machine is the frame and
inference is permitted inside where the machine allows (workflow engine calls
LLM). Agent-first inverts it: the machinery is a toolkit agents wield and
delegate to. Kungfu ships the bones (the skeleton is org-authored, versioned in
the identity tree beside rails, same learn/relearn lifecycle); the substrate
ships only calcium (neutral executors of whatever coordination law the org
wrote). The exec is *delegation an agent or archetype chooses* — a front desk
elected by the worker — not a layer installed above anyone.

## The error asymmetry that makes it safe

- The exec decides **when the worker context-switches**, not **what the worker
  thinks**. Wrong-involvement is cheap and self-correcting ("not now, resume").
  Wrong-gating costs only delay — and delay is bounded by deterministic
  watermarks ("open obligation quiet > X → escalate regardless"), so a
  mis-gated message is late, never lost.
- Audit is circular by tissue: reflexes audit the cartilage (watermarks catch
  exec starvation); agents audit the reflexes (override/tune); effort-checkin
  catches worker stall; rumination audits artifacts AND the fabric itself;
  algedonic signals bypass everything.
- **Top-down modulation** answers "how does the exec know?": it is told, not
  smart. Workers publish standing directives ("deep in the tune-CLI until
  artifact X lands; interrupt only for review verdicts on commit Y") — data the
  bones and cartilage consult. The thalamus gates well only because the cortex
  projects back into it.
- Cascade rule (FrugalGPT / MoE routing): the cheap tier's escalation *default*
  must itself be cheap — here, "deliver at next turn boundary," which is almost
  always right.

## VSM mapping (Beer, adopted with the tier-language dropped)

S1 = knowledge workers. S2 = coordination — Beer explicitly wants it routine
and mechanical, so deterministic bones *conform* rather than compromise. S3 =
the exec layer. S3* = rumination (sporadic audit, its own channel, bypassing
routine reporting). S4 = outward-and-future intelligence — recon archetypes,
roadmap, catalog watching; rumination needs S4 input because judging spirit-fit
requires knowing where the product is going, not just what it is. S5 = spirit =
the PO. The algedonic channel carries genuine pain (constitution violations,
spirit drift) past every tissue straight to S5/the human. Beer's own
constraint: the entire metasystem exists to serve S1 autonomy — which is
agent-first stated in 1972.

## Why agent-first is not folly

- **Auftragstaktik / mission command:** commander's intent plus local
  initiative, born because detailed orders die on contact. Decimation
  resilience is its origin story: units holding *intent* keep functioning when
  comms are cut and leaders are lost; units holding *procedures* stop. Spirit
  IS commander's intent; the PO keeps intent legible; rumination is the
  after-action review.
- **End-to-end principle:** intelligence at the edges, dumb pipes; the internet
  out-survived every smart-network competitor.
- **Let-it-crash (the org's own stack):** supervisors restart, they don't
  prevent.
- **Children of the magenta line:** the cautionary inverse — automation that
  controls too much atrophies the judgment it will someday need. A substrate
  that controls trains agents that can't.
- Costs owned honestly: (1) judgment-everywhere is paid in tokens — the exact
  pressure motivating this fabric; (2) agent-first coheres only under strong
  shared intent — **without spirit, agent-first is a mob; without agent-first,
  spirit is a bureaucracy.** Kungfu identity, the constitution, and the PO are
  the keel, not decoration.

## Existing org material this promotes (emergent practice → architecture)

`attend` tiers (sender-side attention election); exception-based reporting
(already adopted as discipline in live attests); wake-on-fact (S1 condition
subscriptions); supervision watermarks/prods; toplines; decision-requests —
with GitHub issue #11 (agent create-path) as the typed `input-needed` channel
with lifecycle. The org already invented fragments of this fabric by necessity;
the redesign makes them structural — usually the sign the formalization is
right.

## Open forks (deliberately unanswered as of this record)

1. **Accountability:** who holds the obligation when a chosen delegate answers —
   one office/two desks, a delegate role with bounded written authority, or a
   substrate-side smart mailbox below the role line. Must preserve holder-filed
   attest doctrine; sharpened by the reframe: delegation is agent-*chosen*.
2. **Exec context:** rows + standing directives, full principal visibility, or
   directives-only.
3. **Granularity:** exec per worker, per subgraph/office, or tiered by the cost
   of what it protects.
4. **Bones' home:** substrate mechanism + kungfu policy (OTP
   behaviours-vs-callbacks split), pure substrate, or pure kungfu.
