# Core causality fixes — stop discarding facts the substrate holds — v1

Status: READY (gate-cleared 2026-07-26, r4 verdict READY, no blocking findings — vocabulary grep clean, C1 consistently durability-only with all five proofs runnable on rows alone, direct/resolved split confined correctly. Trajectory 6→2→3→0.) REWRITTEN rather than patched: r3's gate
found the causal vocabulary surviving in the status line and downstream section while the
normative body had retired it — patching is what produced that contradiction. Trajectory
6 → 2 → 3 → this, and r4 is SMALLER than r3: C1 is durability-only, and C2 stops trying
to unify reads that legitimately answer different questions.

Flynn ruling: "spec as core fixes and prioritize." These are CORE MODEL changes: each
closes a place where the substrate discards a fact it holds, or leaves a relation
unconstrained so readers must guess.

## Priority

**C1 first** (the enabler), **C2 second** (independent). Both additive; both merge before
any topology reader is implemented.

---

## C1 — record the creating context (durability only)

**The defect.** At `work-item-create` the substrate knows which turn is running (the lane
serializes: at most one per session, ledger.ex:169) and DISCARDS it. Every later
reconstruction fails: `openedAt`/`closedAt`/`createdAt` are millisecond integers with no
shared ordering sequence, so same-millisecond events have undefined order. The only
substitute available — principal class — is a heuristic wrong in both directions.

**The change — TWO additive columns, nothing else:**
- `createdInTurnSeq INTEGER NULL` — the creating session's running turn at create time.
  SUBSTRATE-ONLY: stripped from agent/dispatch params, never accepted (the forensics-v2
  boundary discipline).
- `createdContextKnown INTEGER NOT NULL DEFAULT 0` — 1 when the substrate evaluated the
  context at create; 0 for pre-C1 rows. One nullable column cannot mean both "nothing was
  running" and "this row predates the feature"; without this bit they are
  indistinguishable.

**What the stamp MEANS — concurrency, not proven causality.** The request carries no turn
identity, so the stamp says "this create was concurrent with that running turn of that
session." That is the causal answer in the normal case and is NOT proof. Two deviations,
stated because they are load-bearing for every consumer:
- a SEPARATE request on the same session token while a turn runs is stamped with that
  turn (false positive);
- cancel and boot-recovery terminalize a turn BEFORE serving stops, so an in-flight
  request can land `seq = NULL` even though work was underway (false negative).

`createdContextKnown = 1` means THE SUBSTRATE LOOKED — not that causal truth is known.
There is no upgrade to proof: the wire-carrier remedy this section once named is not
constructible — a wire field is agent-filled, hence forgeable, hence exactly what the
forensics-v2 boundary strips (Flynn's carrier ruling, 2026-07-29, per
artifact-carrier-proposal-v1). The attainable ceiling is the best substrate-observed
edge plus an explicit evidence class; hook-seam observation (`tool-call-observed`) is
the highest class and remains an observation-quality claim, never an unforgeability
claim.

**Why the turn and not the assignment:** a bracket turn (slate or routing nag) can create
an item while holding NO assignment; an assignment-based column would stamp NULL there.
The turn is the only carrier present on every path, and it already carries `assignmentId`
and `jobRef`.

**C1 IS DURABILITY-ONLY (gate r3-F2).** It adds NO response field, requires NO consumer
change, and makes NO claim about roots, parents, children, or trees — those words appear
in no field this spec defines. How to present the evidence (shape, naming, whether to
offer a tree at all) is the consuming reader's decision, in that reader's spec, gated on
its own merits. r3 defined a response representation while also declaring "no wire
surface"; that was incoherent.

**Proofs.** (1) An item created during a running turn carries that seq with `known = 1`;
created with no running turn carries NULL with `known = 1`. (2) An agent-supplied
`createdInTurnSeq` in create params is STRIPPED at the boundary and does not land
(fail-before/pass-after). (3) A bracket-turn create (jobRef, no assignment) stamps the
turn — the case that ruled out the assignment-based design. (4) Migration: two additive
ALTERs, existing rows land `known = 0`, index on `createdInTurnSeq` proven. (5) A
cancel-then-arriving create lands `known = 1, seq = NULL` — the documented false
negative, ASSERTED so the deviation is pinned rather than folkloric.

---

## C2 — an assignment belongs to AT MOST ONE item

**The defect.** `workItemId` and `reviewsAssignmentId` are independently nullable with
nothing tying them together, so an assignment can resolve to zero items or to two (its
own `workItemId` is B while it reviews an assignment of A). Readers must guess or report
ambiguity; reporting it was cruft covering a missing constraint.

**The change — a creation guard plus a named resolution rule:**
- REFUSE at creation a review assignment whose `workItemId` is set AND differs from its
  reviewed assignment's item, with the named error `review_item_conflict` ("a review
  assignment must belong to the item it reviews"). The two-item case becomes impossible
  rather than described.
- RESOLUTION rule, pinned once for readers that want it: own `workItemId` when set, else
  the reviewed assignment's item (transitively), else NONE. "At most one" — the NONE case
  is legal and stays legal.

**The two memberships answer DIFFERENT QUESTIONS and stay separate (gate r3-F3).** r3
tried to make `work-item-get` adopt resolved membership so item reads would "agree." That
is both unsafe and false:
- unsafe — feature_smoke's cleanup fetches `work-item-get` and REVOKES every open
  assignment it returns (feature_smoke.exs:787); widening would turn story-membership
  into lifecycle action against review assignments;
- false — device/client snapshots intentionally stay direct (work_state.ex:97,217), so
  "every item read agrees" was never achievable by changing one verb.

So the divergence is NAMED, not removed: **DIRECT membership = what the item OWNS**
(lifecycle: guards, brackets, revocation, snapshots); **RESOLVED membership = what the
item's STORY includes** (trace, and any future topology reader). Both are correct answers
to different questions; each consumer states which it uses. Nothing changes for existing
lifecycle consumers.

**Audit of legacy rows.** A one-shot audit after the gateway schema loop (NOT `Boot` — it
runs before assignment schema assembly; NOT `Assignments.ensure_schema` — it may run
repeatedly) LOGS pre-existing conflicts. Cycle-safe (memoized resolver or visited-set
recursion) because it runs over legacy/possibly-corrupt rows even though API-created
review links are acyclic by construction. Log-only: only a human knows which pin was
intended.

**Proofs.** (1) A conflicting review-assignment create is refused with
`review_item_conflict` (fail-before/pass-after). (2) A NULL-`workItemId` review assignment
resolves transitively for RESOLVED readers and counts exactly once. (3) An assignment with
neither key resolves to NONE. (4) DIRECT consumers UNCHANGED: feature_smoke's revoke-loop
still sees only directly-owned assignments, and client snapshots are byte-identical
(preservation proofs, per the gate). (5) The boot audit logs conflicts without mutating,
and terminates on a synthetic cycle.

---

## Non-goals

No declared parents, tags, or labels. No backfill. No new tables. No response fields, no
wire changes, no consumer rewrites — this spec changes the MODEL; readers change in their
own specs. No unification of direct and resolved membership.

## Component touches

C1: `work_items` two additive columns, create-seam stamp, boundary strip, migration,
tests. C2: assignment create-path guard, the pinned resolution helper (for resolved
readers), one-shot boot-loop audit, tests. No wire surface in either.
