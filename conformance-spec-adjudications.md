# Spec adjudication queue — conformance recovery

The recovery's HANDOFF ledger surfaced these places where two governing specs
contradict or a required behavior is underdefined. Per the recovery checklist (item
7c) these get a Flynn/spec-authority ruling, never another implementation pass. Each
ruling lands in the OWNING spec; this file then records the disposition and empties.

Recommendations are Fable's, argued from the ratified design record. Ruling is
Flynn's.

## 1. Supervision r20 vs rails/escalation turn-end model — RULED (Flynn, 2026-07-24)

**Disposition:** not a values conflict — a stale territorial claim. r20's
sole-authority fence replaced by schedule ownership + amendment duty;
principles kept as invariants; termination argument extended over the fold.
Landed: supervision-impl-v1 §r21, the visible pipeline + lease comments in
supervision.ex, and the order-pinning test (commit 2cd4a25). Item 2 ruled the
same way in the same amendment. ~20 clauses resolve at the corpus re-run.

<details>
<summary>Original writeup</summary>

## (was) 1. Supervision r20 vs rails/escalation turn-end model (BIGGEST — ~20 clauses)

Supervision 5, 12, 15, 22, 33, 42, 50, 60, 74, 75, 86, 89, 107, 119, 122, 123, 125,
129; Escalation 21, 122.

**Conflict:** `supervision-impl-v1.md` r20 claims sole authority and forbids what
`rails-mechanism-v1.md` + ratified `escalation-substrate-v1.md` r7 require (and what
is SHIPPED and live-smoked): the turn-end rail fold in `Supervision.evaluate` —
adjudication hold, `Rules.decide/2`, remedy close/fire, escalation open/park, rail
lifecycle emission before the pending-wake check. r20 wants supervision limited to
wakes/stamps: no statute-expressed policy, no check-tier gate, no `rail_sweep` kind.

**Recommendation: the rails/escalation model wins.** The P4/P5/P6 spine was designed,
ratified, built, adversarially reviewed, and proven in the live e2e smoke THIS cycle;
supervision r20's constraints encode the pre-spine worldview. Amend supervision-impl
to r21: incorporate the turn-end fold as in-scope, extend the public result-tag set
and termination argument accordingly. The conformance corpus already asserts the
shipped ordering. Choosing r20 would mean ripping out the working, verified
enforcement spine.

## 2. Supervision 29 — retirement withdrawal ownership — RULED with #1 (Flynn, 2026-07-24)

**Disposition:** escalation r7 wins; the withdrawal call stays in the retirement
handler, permitted by the same r21 amendment (schedule ownership, not sole
authority). Landed in supervision-impl-v1 §r21.

<details><summary>Original writeup</summary>

**Conflict:** r20 makes `notify_retired` doorbell-only; escalation r7 §8 requires
the same handler to call `Escalation.withdraw_for_retired/2` (the retirement fast
path).

**Recommendation: escalation r7 wins** (same reasoning — r7 is the later, ratified,
shipped model; the fast path exists so a retired raiser's requests don't linger
open). Amend supervision r21 to permit the withdrawal call in the retirement
handler, keeping Supervision 31's total catch around it. Alternative if you want
r20's purity: move withdrawal to a wake-driven follower — costs a latency window
where a dead session's decision requests stay open.

</details>

</details>

## 3. Accountability 82 — retired-holder ancestor notification — RULED (Flynn, 2026-07-24)

**Disposition (Flynn's formulation):** the condition is the ROW, not a judgment —
"if it was doing something there's an assignment record; if there isn't a record
it wasn't doing anything anyway." Notification fires iff the retired holder has
open assignment rows: first living ancestor, org owner at the root, one
addressed notice through the existing owner-delivery seam. No open rows →
doorbell/stamp only. The supervision-vs-constitution "conflict" dissolves: no
judgment was ever required. Landed: accountability-constitution §5 (strand
condition), supervision-impl §r21 (retirement handler — the amendment duty's
first admitted tenant). Implementation queued with integration work.

## 4. Rails F2(b) — literal remedy target/param → fact mapping — RULED (Flynn, 2026-07-24)

**Disposition:** narrowed. F2(b)'s fixed-attribute set is exactly `verb` +
`caller.origin_class="remedy"` — the promise of a literal-target/param → fact
dictionary is removed (it was the load-time satisfiability prover wishing for a
higher-resolution model than any statute has needed; the coarse kind-level
producer registry answers every real question). Landed in rails-mechanism-v1
§F2(b) with the provenance noted. If a statute ever needs finer blocking
analysis, the per-action mapping is designed then as its own spec change.
Closes core-rules HANDOFF clauses Rails I8.2 / F2.2 / P5.1 / C6.8 against the
narrowed text.

## 5. Artifacts clause 7 — unrecorded workspace at cleanup — RULED (Flynn, 2026-07-24)

**Disposition:** archive-if-artifacts wins; the "archive every closing workspace"
floor sentence was a pre-simplification leftover, now rewritten. Rows → archive
with the rows' own work-item edge; no rows → remove ("if there isn't a record it
wasn't doing anything anyway"). Landed in artifacts-and-reconciliation.md
(essence section, floor bullet).

## 6. Artifacts clause 45 — time-window filter — RULED BY REMOVAL (Flynn, 2026-07-24)

**Disposition:** the filter is deleted from the spec rather than defined —
Flynn: "what is this filter for... we aren't providing search, just
recordkeeping." Provenance (Fable, on being pressed): the filter was
spec-author reflex (query APIs "usually" have a time filter) plus a leaked
find-by-fuzzy-memory motif — time is a RECALL aid, and recall/search was
explicitly ruled someone else's layer in the same design conversation.
Work-item/session filters are FK traversals over recorded edges (the record
side); by-time crossed the boundary because it was cheap, and cheap isn't the
criterion. Deletion is a boundary correction, not just YAGNI. Clause 45
resolves by removal; a real by-time need costs one ratified sentence later.
Landed in artifacts-and-reconciliation.md §4.

---

**Not in this queue:** the ~15 cross-lane TEST placements in the ledger (verdict
matrix in check_tier, supervision denial rows, producer gate proof, etc.) — those
are integration work now that the implementation lanes are merged; a dedicated
integration-tests lane closes them without any ruling.

## 7. cli-rust-v1 verb freeze vs the shipped CLI surface — RULED (Flynn, 2026-07-24)

**Disposition:** option (c), and the port spec is RETIRED entirely so it can't
be confused again (archive/cli-rust-v1-PORT-SPEC-RETIRED.md). The "no new
verbs" invariant was port-fidelity discipline — the only way a port is provable
is byte-equivalence against the reference — kept in force past the port's
completion (the same expired-moment disease as r20's fence and F2(b)'s
dictionary). Replacement: cli-surface-v1.md, a living contract enumerating the
surface from the greppable demand ledger (kungfu kernels/skills + smoke +
operator ceremonies), with an amendment duty. The cli lane restores the
demanded families (attest/attests, work-item, assign/assignments/dispatch,
artifacts, config) from git history; undemanded families (probe, condition,
escalation/waiver, critical, adjudicate, producer-mgmt, cli-init) stay deleted.

<details><summary>Original writeup</summary>

## (was) 7. cli-rust-v1 verb freeze vs the shipped CLI surface — AWAITING FLYNN

**Conflict (found by verify3, 2026-07-24):** `cli-rust-v1.md` says "no new verbs,"
so the conformance fix lane — correctly obeying the spec letter — deleted 1,911
lines of working CLI: the `probe`, `condition`, facts/artifacts, escalation/
waiver, `critical`, `adjudicate`, assignment/dispatch, producer, work-item,
attestation, `config`, and `init` command families, plus session-derived
identity and cwd-ancestor `.tightbeam-session` discovery. Those verbs grew with
the roadmap; the spec never did. This is the stale-spec bug class in its most
expensive form: spec-obedient destruction of real functionality. The cli lane's
MERGE IS HELD on this ruling.

**Decision needed:** which CLI surface is v1?
(a) The spec is right — the CLI ships minimal, the deleted families return
    later behind an amended v2 spec (the deletion stands).
(b) The shipped surface is right — amend cli-rust-v1 to enumerate the grown
    verb families as in-scope, and the lane restores them (the deletion is
    reverted before merge).
(c) Split: name which families are v1 (e.g. work-item/assignment/attest/config,
    the ones the kungfu's own skills reference) and which wait.

**Recommendation:** (c), anchored on one test: any verb the shipped engineering
kungfu's skills/kernels instruct agents to run (`work-item-create`, `assign`,
`attest`, `wake`, `spawn`, `retire`, `config`) MUST be in the v1 surface — the
bundle's own guidance is the demand ledger. Families nothing in the bundle
references (e.g. `critical`, `adjudicate`) can wait for v2. The spec then
enumerates the surface so the freeze means something.

</details>
