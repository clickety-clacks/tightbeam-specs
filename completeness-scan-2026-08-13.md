# Completeness scan — fabric Phases 0-2 vs main (2026-08-13)

Status: RECORD. Dual independent scans at Mike's direction: Opus 5
(source-reading agent) and Sol high (gpt-5.6-sol, codex exec
danger-full-access — first direct-filesystem Sol run on gibson), both
against main e932a50, both deriving the checklist from fabric r4.2
§§5-7/§13. Both verdicts: NOT COMPLETE modulo the four recorded deltas.
Each vendor found real gaps the other missed — the cross-vendor bet
paying out at the completeness layer.

## Agreement (settled by both)

Phase 0 COMPLETE. Seam ③ COMPLETE (arm, verbs, outbox, proof-10,
centralized helpers, named refusals). Seam ④ complete except cursor
uniformity. Stub sweep CLEAN — zero genuine TODO/FIXME/stub bodies in
lib/ or cli/src/ (all hits are SQL bind-placeholder vocabulary). Law 2
and Law 3 verified holding on the batching path (no DELETE FROM wakes
exists; every delivery-policy arm ends in a scheduled exit). The four
recorded deltas confirmed; nothing silently joins them.

## Opus-only findings (Sol missed)

- **O1 HIGH (live Law 2 defect): retarget_in_txn erases class election.**
  wakes.ex ~490-506: INSERT..SELECT omits class/classElection/
  deliveryRule/digest/summon — a retargeted classed wake loses its
  election (destroyed, not superseded); a retargeted summon silently
  enters acceptance-№1's numerator. Reachable from org.ex:688.
- **O2 MED (spec §4 contradiction, bites at Phase 3 rebind): digest
  carrier drops role re-resolution** — carrier built with no target_role;
  members canceled; a role rebound inside the ceiling window sends the
  digest to the previous holder. Spec explicitly claims the opposite.
- **O3 MED: cursor_not_found non-uniform** (attests cursor_not_found vs
  toplines/transcript not_found); fixture pins the divergence. (Also
  found by Sol.)
- **O4 MED latent: the all-or-nothing raise is unrescued in the tick
  loop** — a poisoned digest member (constructible via linked-work
  replacement matching; verified unreachable today) would crash delivery
  for every session every tick, no agent-reachable repair.
- **O5 LOW: digest_members (the C4/acceptance-2 audit) has no sanctioned
  surface** — a status question answerable from rows no agent can ask.
- **O6 LOW: policy-skew row hardcodes rule "turn-boundary-digest r1"**
  even when the wake was batcher-inhibited — misattributed reflex (§8).
- **O7 LOW: blocker/algedonic ceiling_ms: 0 is a false datum** for
  future Phase 6 policy extraction (inert today).
- **O8 LOW: coordination-share CLI help says "classed" — abandoned
  formula.** (Sol found the same wording in the operating manual.)

## Sol-only findings (Opus missed)

- **S1 (spec-vs-code divergence): the classifier has NO production
  ingress** — classify/1 exists and is correct but only tests call it;
  the shipped design (wave 1, deliberate, review-accepted: election is
  how traffic enters the fabric; unclassed wakes untouched) contradicts
  spec §5's "stamps inbound messages; unclassified → fyi". Reconcile by
  spec fold (r4.3) or by wiring ingress — the wave-1 rationale
  (retroactively holding all org mail nobody elected) argues for fold.
- **S2 (spec defect): the coalescer is MISSING and §13 never schedules
  it** — §5 names the behaviour (sender+card grouping, dedupe, "×3,
  latest"), no phase builds it; v1 digests deliver every payload
  verbatim. Needs a scheduling ruling (proposal: Phase 4, where digest
  FORM starts to matter at desk scale).
- **S3: receiver re-classification (§7) unimplemented, deferral
  unrecorded** — it is a desk behavior; belongs at Phase 3, needs the
  record to say so.
- **S4 coverage: Phase 2 docs pinned by PATH only** — no test would fail
  if the delegation card's verbatim verb list were emptied; semantic
  content pins missing (verb-list presence, REBIND-then-revoke ordering,
  five directive keys).
- **S5 coverage: transcript class test pins key set, never non-null
  values; toplines pending_wake_classes has zero tests** (Opus also
  flagged the toplines half); status-query §7 no-desk cell restated
  (already in wave-1 recorded dirt).

## Disposition

Fix wave (code): O1, O2, O3, O4, O6, O8+manual wording, O5 (small read
verb), O7 (comment). Spec fold r4.3: S1 (classifier = election-is-entry,
fold the §5 row), S2 (schedule coalescer Phase 4 — proposal for Mike),
S3 (record receiver-reclass as Phase 3 desk behavior), status-query cell
note. Coverage wave: S4 + S5 pins. All through the standing review
discipline; landings to the build ledger as usual.
