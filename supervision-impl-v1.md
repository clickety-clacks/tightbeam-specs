# Supervision impl v1 — reaction executor, prod counter, escalation ladder (implementation spec, r21)

## r21 — the turn-end schedule (Flynn-ratified 2026-07-24)

r20's sole-authority claim over the turn-end moment is REPLACED by schedule
ownership. This module owns the SHIFT — the ordered step list, the shared turn
context, the single-writer watermark, and the termination argument — while each
step's SEMANTICS belong to the spec that governs it (rails-mechanism-v1 +
escalation-substrate-v1 for `:rail_enforcement`; this spec for the rest).

The shift, in order, first halt wins (mirrored verbatim by
`Supervision.turn_end_schedule/0` and its order-pinning test):

> **AMENDED 2026-08-12:** schedule step 1 (`:adjudication_hold`) died with
> adjudication. Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`).
> The live schedule is `[:rail_enforcement, :pending_wake_gate, :prod_ladder]`
> (`supervision.ex` `@turn_end_schedule`). Step-1 references below are history. See `adjudication-deletion-amendment.md`.

1. `:adjudication_hold` — an open adjudication freezes everything downstream.
2. `:rail_enforcement` — the org's statutes get the turn before the substrate's
   ladder: `Rules.decide/2`, remedy close/fire, escalation open/park, rail
   lifecycle legibility rows. Hosted here; specified in rails-mechanism-v1.
3. `:pending_wake_gate` — a pending wake means not stalled; halt as
   continuation.
4. `:prod_ladder` — the r20 sweep proper (prods, ladder, watermark). Always
   halts.

**Amendment duty (replaces the sole-authority fence):** anything new at
turn-end takes a named slot in this list AND extends the termination argument
AND the order-pinning test. No other path in.

**Termination, extended over the fold:** the r20 argument covers step 4; the
enforcement loop added by step 2 is bounded because remedy episodes are
once-per-occurrence (CAS-deduped by producer occurrence key — a fired remedy
cannot re-fire on the same offense) and escalation parks exactly one wake per
decision request. Each shift therefore performs bounded work and cannot
re-trigger itself on an already-handled occurrence.

**r20's principles are kept verbatim as invariants inherited by every step:**
no why-inference, no punitive action (substrate acts are wakes, stamps, and
org-authored statute effects), no content reading. Statute enforcement does not
breach neutrality: statutes are org-authored law mechanically applied.

**Superseded by this amendment:** the sole-authority clause; the non-goals
lines deferring "check-tier completion gating" and "statute-expressed
supervision policy" (built, governed by rails-mechanism-v1); any r20 clause
enumerating outcomes or lifecycle kinds is now "as of r20" — the tag set gains
`{:acted, :rail_remedy}`, `{:acted, :rail_escalate}`, `{:held,
:adjudication_hold}`, and the `rail_sweep` lifecycle kind.

**Retirement handler (r21, ruling #2 + #3):** `notify_retired` keeps
`Escalation.withdraw_for_retired/2` (escalation r7 §8's fast path — ruling #2)
and gains the strand notice (accountability constitution §5, Flynn-ruled
adjudication #3): iff the retired holder has open assignment rows, deliver ONE
addressed notice to the first living ancestor (org owner at the root) through
the existing owner-delivery seam. The condition is a row count — a retired
session with no open assignment was doing nothing anyone is owed — so r20's
"waking is operator judgment" concern never applies: no judgment, just the row.
No open rows → doorbell/stamp only, unchanged. This is the first new tenant
admitted under the amendment duty: it takes its slot in the retirement path,
its work is bounded (one walk up the spawner chain + one delivery per
retirement), and the retirement tests extend accordingly. (UNBUILT: queued
with the recovery's integration work.)

Status: r21 (stale "DRAFT r20" label corrected by the 2026-08-12 amendment;
the r20 gate record follows: r19-review returned NOT-READY on TWO findings, both
now closed — NO change to the atomic-fire mechanism, which the reviewer
independently CONFIRMED correct and wireable at the named seam. (1) SCOPE
LEAK: origin `process:tightbeam` was NOT exclusive to supervision because
the external attribution seams accepted `asProcess: "tightbeam"`
(router.ex ~332/~410-415), so the `:fire_wake_in_txn` selector could gate
a FORGED external wake. FIX: `process:tightbeam` is now a RESERVED
substrate origin — both `asProcess` acceptance points return `403
reserved_origin` for the name `tightbeam`, an integrity invariant (the
substrate's own canonical self-name is not externally attributable, like
one session cannot forge another's identity); after r20 origin
`process:tightbeam` on a wake row can ONLY be supervision's, so the
selector is exact by construction (§Atomic wake delivery RESERVED ORIGIN;
scope-control test adds the rejection case). (2) TEST-ORACLE BUG: the
escalation verbatim oracle compared against the UNSTAMPED ladder template
though delivery prepends `[from process:tightbeam]` exactly as the PROD
oracle already required — fixed to compare the STAMPED delivered message.
Both are spec/test fixes plus one tiny router rejection; mechanism, proof,
and boundedness UNCHANGED.) Prior: DRAFT r19 (the BUILD of r18 correctly STOPPED on a genuine
implementation-vs-spec race the r18 liveness argument had ASSUMED
away. Wake DELIVERY is DELIVER-THEN-MARK — `deliver_prompt` commits
the turn's enqueue transaction and post-commit `LaneManager.ensure_lane`
NUDGES the lane (gateway.ex ~456-495) BEFORE `Wakes.deliver_due` marks
the wake FIRED in a SEPARATE later transaction (wakes.ex ~204-233;
verified against main 5770d7c). A fast provoked turn can terminate in
the gap between the lane nudge (step 2) and the fired-mark (step 3): at
that moment supervision's step-4 predicate reads the ORIGINATING prod
wake STILL 'pending' (`Wakes.pending_count > 0`) and returns
`:continuation` (SUPPRESSED), the fired-mark then lands with no new
terminal edge, and the prod→turn→prod self-driving chain STALLS
PERMANENTLY. The r18 termination proof assumed delivery was atomic with
fired-marking; it is not. FIX (Flynn-orchestrator PRIMARY ruling —
atomic-fire, the source-level fix): for supervision's OWN delivered
wakes ONLY, the wake is marked FIRED ATOMICALLY inside the SAME
`deliver_prompt` enqueue transaction that enqueues the turn (additive
`:fire_wake_in_txn` opt on `deliver_prompt`, set by the wake deliver
closure for supervision's process-origin direct wakes only), so a
delivered supervision prod/escalation is committed 'fired' BEFORE the
post-commit lane nudge and is NEVER observable as 'pending' by the
terminal it provokes; post/role/external wakes keep today's
deliver-then-mark fired-marking UNCHANGED (minimal blast radius). This
was VERIFIED FEASIBLE at the real seam — the fired-mark is one in-txn
CAS added to `deliver_prompt`'s existing append+enqueue transaction,
`opts[:wake_id]` already in scope — so the atomic-fire approach is
taken; the recorded FALLBACK (the suppression-predicate: exclude
supervision's own just-delivered gated wake from step-4's pending
count — supervision's `:continuation` suppression is for a
FUTURE-scheduled continuation the AGENT scheduled, never for
supervision's own in-flight prod) was NOT needed and survives below as
the documented alternative only. §Atomic wake delivery, §Self-driving
liveness, §step 4, Invariants 5/8, and §Tests are updated; the SETTLED
mechanism and the §Cascade-boundedness TERMINATION proof are otherwise
UNCHANGED — this is a LIVENESS fix (a stalled chain is still bounded),
not a boundedness one). Prior: DRAFT r18 (r17-review confirmed 'no infinite internal cascade found — the path-blind watermark argument is complete' with ONE lemma correction: a past-sink wake to Main may have ONE successor — an SC wake for another Main-held stalled assignment — which strictly DECREASES Φ and is already in the ≤Φ SC budget, never a PS-provokes-PS escape; wording 'the chain ends at Main' was imprecise, now stated as the SC-only continuation). Prior: DRAFT r17 (§Cascade-boundedness REWRITTEN: the r12–r16 closed-form wake-COUNT (2·(Φ+|R|), episode/frontier/credit machinery) is REPLACED by a path-blind TERMINATION argument from two pinned facts — (1) the watermark admits ONE claim per (session,terminal) EVER regardless of re-evaluation path, so reconcile-republish/sweep/request_sweep can't produce unbounded wakes; (2) each internal wake decreases the finite Φ measure or hits the immortal Main sink. Termination given finite external input; no numeric count to enumerate frontiers for. Mechanism UNCHANGED, feasible per r13-review). Prior: DRAFT r16 (r15-review: SWEEPS — both the restart recovery sweep AND the public request_sweep/1 — are now EXPLICIT EPISODE BOUNDARIES, not in-episode events; a sweep is the only thing that re-evaluates a session without a new terminal, so it ends an episode like any external trigger and directly emits ≤|open assignments| wakes charged to ITSELF, never to a prior t₀. This closes the suppressed-terminal / past-sink reclaim as sweep-rooted external work. Overall claim reframed as termination given finite external triggers, with 2·(Φ+|R|) the per-episode figure. Mechanism unchanged, feasible per r13-review). Prior: DRAFT r15 (r14-review's one remaining proof gap closed: suppressed terminals produce nothing within an episode, and past-sink OPEN assignments — slots=0 — emit escalations bounded by EXTERNAL input/restarts, not the internal Φ-cascade, so they are not counterexamples to the 2·(Φ+|R|) figure; mechanism unchanged, CONFIRMED FEASIBLE in r13-review). Prior: DRAFT r14 (revised per the r13 confirmation round: verdict
NOT-READY with TWO blockers, BOTH proof-rigor findings against
§Cascade-boundedness's termination argument — NO design change
anywhere; the r13 MECHANISM was CONFIRMED SOUND against main
f739c07 (flag resolution below). (1) the r13 "≤ 2·Φ(t₀) + |R|"
figure was FALSE on r13's own in-flight scenario: at t₀ a
slot-consuming wake already pending, its source assignment closed,
and the recipient's assignment past-sink give Φ(t₀) = 0 and
|R| = 1, yet the root wake's delivery PLUS the one past-sink wake
its terminal claims toward Main are TWO delivered wakes against a
bound of one — the single root credit was spent both on the root's
own delivery and on the past-sink tail its terminal provokes. r14
replaces the chain argument with PER-TOKEN CREDIT ACCOUNTING —
every frontier token is credited for its OWN delivery AND for the
≤ 1 past-sink successor its terminal can claim, every Φ unit
likewise — and the corrected bound is ≤ 2·(Φ(t₀) + |R(t₀)|); the
required tests now assert the bound VALUE, not termination alone
(r13's test asserted termination only — exactly how the false
figure survived review). (2) r13's root set R was neither complete
nor fixed at t₀: a supervision wake FIRED before t₀ whose provoked
turn had not yet reached terminal — neither a pending wake nor an
external terminal — could claim an uncredited post-t₀ past-sink
wake; terminals already occurred but not yet evaluated had the same
gap; pending outbox entries with a past-sink rung produce an unpaid
wake with no post-t₀ claim at all; and "the recovery sweep's claims
if a start occurs" made R depend on FUTURE restarts. r14 defines
R(t₀) as the COMPLETE FRONTIER — pending wake rows, in-flight
turns, unevaluated terminals, pending outbox entries, each finite
and fixed by the state at t₀ alone — and rules that a RESTART
STARTS A NEW EPISODE with its own t₀ and its own fresh frontier: no
episode's R ever includes another episode's events
(§Cascade-boundedness). ⚑ FLYNN FLAG RESOLVED (r13 review, against
f739c07): the r13 transactional wrap is CONFIRMED FEASIBLE in the
real deliver path — `deliver_prompt` already wraps the projection
append and `Ledger.enqueue_in_txn` in one transaction (gateway.ex
~448), `DB.transaction` runs its body as one BEGIN IMMEDIATE…COMMIT
pass in the single DB-owner process (db.ex ~123), `Org.retire`
writes through that same owner (org.ex ~411) and serializes
whole-before-whole, the in-txn `Txn.q` target read and the pure
`ladder_target(txn, holder, rung)` walk are safe inside it, the
three nullable wake columns and triple validation fit the additive
migration path, and H→S→H re-resolves to Main. The bounded-sweep
fallback is NO LONGER A LIVE ALTERNATIVE — the no-periodic-sweep
ruling HOLDS as designed; the flag survives in the r13 history
below as record only, and §Atomic wake delivery's build-time STOP
remains the ordinary escalate-don't-improvise guard.)
r13 was: (revised per the r12 confirmation round's three
blockers — each closes a gap in an r12 fix; no ruled question is
reopened. (1) WAKE DELIVERY IS CHECK-AND-ACT ATOMIC — r12-review
finding 1: the deliver closure's active-check (gateway.ex ~226) and
`deliver_prompt`'s enqueue transaction (~448) were SEPARATE DB-owner
calls, so `Org.retire` (~1832) could commit in the gap — the turn
enqueued on a retired session, the wake marked fired, delivered to no
one. r13 moves the target-state read INSIDE `deliver_prompt`'s
existing single transaction (`DB.transaction/2` = one BEGIN
IMMEDIATE…COMMIT pass in the one DB-owner process, whole-serialized
against `Org.retire`'s own write): delivery either reads the target
LIVE and enqueues in the same transaction, or reads it RETIRED and —
in that same transaction — re-resolves (escalation) or no-ops (prod →
derived-stranded). The race is closed with NO sweep, preserving the
no-periodic-sweep ruling (§Atomic wake delivery). ⚑ FLYNN FLAG
(RESOLVED by the r13 review — wrap CONFIRMED feasible, see the r14
note above): this
transactional wrap is the ALTERNATIVE to a bounded safety sweep; if
the wrap proves infeasible in the real deliver path during the build,
the fallback is that sweep — STOP and put the choice to Flynn; do not
improvise a third design. SCOPE: this touches the SHARED wake
pipeline — every direct wake's retired-target no-op becomes
race-free with identical observable behavior (a general correctness
improvement); only supervision ESCALATION wakes gain the
in-transaction re-resolve branch. (2) THE DELIVERY RE-RESOLVER IS THE
HOLDER-SEEDED LADDER WALK; `lineage_target/2` IS DELETED —
r12-review finding 2: a resolver walking up from the DEAD target
without the holder in its visited set resolves the cycle H→S→H (S
retired) back to H — the original holder — where `ladder_target(H, 1)`
skips the cycle and resolves Main; coherence, the non-holder
escalation leg, and the contiguous-chain bound all broke. r13: the
escalation wake row PERSISTS its resolution inputs (`reresolveSeed` =
the holder, `reresolveRung` = the rung) and delivery re-RUNS
`ladder_target(seed, rung)` — the SAME walk dispatch ran, holder seed
and all, on fresh truth inside the delivery transaction — so a
retired intermediate resolves exactly as the original walk would,
skipping cycles, sinking at the immortal Main. (3) THE TERMINATION
BOUND IS EPISODE-RELATIVE; IN-FLIGHT WAKES ARE ROOTS — r12-review
finding 3: `prodCount` consumes its Φ slot at wake CREATION (the
outbox clear), before delivery, so a slot-consuming wake still
PENDING when its source assignment closes leaves Φ = 0 with a wake in
flight, whose later delivery can provoke a past-sink escalation no
live Φ unit pays for. r13 replaces the "≤ 2·Φ_global" figure with a
CHAIN argument over an episode's finite ROOT SET R — external
terminals, progress/assign events, sweep claims, AND every
supervision wake already pending at episode start, each carrying its
own credit — proving internally-provoked delivered wakes
≤ 2·Φ(t₀) + |R| (§Cascade-boundedness); the N=0 cross-assignment
counterexample and a new in-flight-wake case are required
terminating tests.)
r12 was: (revised per the r11 adversarial round's two
blockers; BOTH fixes PRESERVE the no-periodic-sweep ruling by
exploiting MAIN IMMORTALITY — the retire verb denies built-in Mains
("main sessions are permanent", gateway.ex ~1809), so the owner's
Main is an always-live terminal sink for every escalation ladder.
(1) ESCALATION TARGETS RE-RESOLVE AT DELIVERY, NEVER PINNED-DEAD —
r11-review finding 1: an escalation target retiring after its claim,
or after its wake row was scheduled, left a LIVE holder's ladder
permanently silent (the holder's reply-chain had already ended at
the escalation, the holder is not derived-stranded — it is alive —
the restart sweep dies at `:duplicate`, and no internal edge ever
re-resolves the rung). The fix: the outbox stores the RUNG, never a
target — `pendingTarget` is DELETED from the schema; the act/drain
resolves `ladder_target(holder, rung)` AT DISPATCH TIME, skipping
retired ancestors and sinking at the immortal Main — and the
scheduled escalation wake row carries the new additive
`reresolve: "lineage"` wake param, so the DELIVERY tick, on finding
its target retired, re-resolves up the dead target's own
`spawned_by` lineage to the nearest active ancestor or the owner's
Main instead of silently no-opping (§Escalation delivery
re-resolution). A claimed escalation is therefore ALWAYS delivered
to a live session, crash-robustly: both carriers — the outbox entry
and the wake row — are DURABLE and retried until they land. PRODS
ARE UNCHANGED: only escalations have an immortal sink to walk
toward; a retired PROD target IS the retired holder — the
derived-stranded case, never delivered. (2) the r11 per-assignment
≤ N+1 termination claim is DELETED — r11-review finding 2: false as
stated (with n = 0, cross-assignment re-entry lets one assignment
emit more than N+1 internally-provoked wakes) and its "separately
bounded chains compose" argument was circular. Replaced by a GLOBAL
TERMINATION argument on the measure Φ_global — the sum, over open
assignments, of remaining prod slots plus remaining rungs to the
Main sink (§Cascade-boundedness) — well-defined and finite
precisely because Main is immortal; N+1 survives only as a
per-contiguous-reply-chain observation.) r11 was: (ARCHITECTURAL
SIMPLIFICATION, ruled by Flynn after the r10 round returned five
blockers: (1) STRANDED IS DERIVED, NOT EMITTED — an assignment is
stranded iff it is OPEN and its HOLDER session is RETIRED, a
view-state computed at query time from the join, never a fact that
must be reliably emitted; `supervision_stranded`/`strandedAt`/
`notify_retired` all demoted to OPTIONAL best-effort doorbells
(thin-event/fat-query) and the r9/r10 atomic stranded-write protocol
DELETED as a correctness requirement — dissolving r10-review
findings 2 and 5. (2) NO PERIODIC SWEEP, EVER — prods SELF-DRIVE the
ladder for LIVE holders (prod→turn→prod→…→escalation, no timer,
§Self-driving liveness), dead holders' work is derived-stranded;
only the START-TIME recovery sweep remains. (3) the r10 global
potential Φ deleted — unbounded below — for a per-assignment ≤ N+1
bound, itself deleted by r12. (4) delivery requalified to LIVE
holders and the evaluation order fixed to drain → IDLE-DETERMINATION
→ dedupe, so a drained stale closed-assignment entry on a session
with no open assignments returns `:idle`, never `:duplicate`.)
r10 was: (r9 round: eight
adversarial blockers — F1 retired-TARGET drain split from
retired-HOLDER stranding; F2 retirement as an edge, `notify_retired`;
F3 drain-first-then-idle; F4 stranded row + strandedAt as one
transaction; F5 raising-handler test → `supervision_dispatch_failed`;
F6 self-target guard scoped to the ESCALATION branch; F7
cascade-boundedness as a global potential Φ; F8 the ≤tick_ms SLA
weakened to eventual delivery — F2/F4/F7 since superseded by r11's
rulings, F8's weakening kept). r9 was: (r8 round: the
r8 inline patches propagated into the
normative sections — the schema formally carries `strandedAt` /
`pendingK` / `pendingN` and the evaluation contract gains `:stranded`;
the outbox stores BOTH numbers (k-or-rung AND the prod_limit in force
at claim) and the act renders template text ENTIRELY from stored
values, never recomputing; the drain checks the pending TARGET's
session state — retired target clears without dispatch and emits the
stranded row, live non-holder targets dispatch normally; the
retired-holder rule strands PER-ASSIGNMENT over EVERY open assignment
in both terminal path and sweep, with the four edge cases ruled
explicitly; "every stall claims a wake" scoped to LIVE holders —
retired holders strand). r8 was: (r7 round: retired-holder rule made UNIFORM — stranded-rows-only, never woken, strandedAt dedupe column, sweep branch explicit; transient-retry prose aligned with the drain short-circuit; pendingK added to the outbox for config-change-proof replay; attest-absence finding was the build-ordering gate working). r7 was: (r6 confirmation round: transient-drain short-circuit pinned — the outbox slot is never overwritten while occupied; RETIRED-HOLDER RULE — retired holders escalate, never prodded, with the post-claim retire race accepted + supervision_stranded sweep observability; denied clear pinned as one transaction; supervision_dispatch_failed added to the lifecycle inventory; proof scoped per-assignment). r6 was: revised per the clean r5 re-review (two required
findings: cascade-proof legs 3-4 rewritten — no fixed per-epoch bound,
self-termination at N+1 internally-provoked wakes, terminus
disambiguated; sweep candidates = open-holders UNION pending-outbox
sessions, with the closed-assignment drain rule clear-without-dispatch;
plus: denied-clear restricted to statute-tier codes with
supervision_dispatch_failed retry semantics for transient errors,
clear pinned as one transaction; idempotency-key question adjudicated
KEEP-TRADEOFF). r5 was: The r5 model is
EXACTLY-ONCE COUNTING with what r5 called "at-least-once delivery"
(requalified by r11 — see the normative contract, §The seam: delivered
to LIVE targets; a dead holder's obligation is derived-stranded, never
delivered): the claim transaction
records the decided action as an OUTBOX entry on the watermark row
(`pendingBranch`/`pendingTarget`/`pendingAssignment`), and every
evaluation and sweep DRAINS the outbox first — a claim can no longer
be lost to a crash, and the rare crash between dispatch and clear
yields a duplicate wake, ACCEPTED and documented (a duplicate prod is
a harmless message; permanent silence violated the invariant — that is
the tradeoff). Supervision never inline-fires: its wakes are scheduled
rows (dueAt = now) delivered by WakeScheduler's own tick, which
removes every synchronous edge out of Supervision except the DB owner
and moves the sweep trigger back into Supervision's own init. The
counter splits into `attemptCount` (every claim) and `prodCount`
(delivered wakes only — drives branch, ladder text, and escalation),
with `supervision_prod_denied`/`supervision_blocked` lifecycle rows
for statute-denied attempts. Older-seq rejections are renamed
`:coalesced` and documented as accepted per-session coalescing. The
cascade proof is redone on four honest legs. Prior history: r4
per-session monotone watermark + claim-then-act + total catch +
predicate-NOW sweep; r3 equality watermark, recovery sweep,
`--session` flag fix; r2 serialized executor GenServer, decoupled
attest column names, seeded ladder walk.
Parent design: supervision-v1.md (ratified; §Prerequisites items 2–4 —
this spec implements them EXACTLY). This spec is the sole authority for
the build lane; supervision-v1.md is background.

DEPENDENT ON ATTEST: attest-v1.md (r5 as of this revision) must be
merged to main before this worktree is cut — build ordering unchanged.
This spec consumes attest's
schema (`assignments`, `attests`) — via two additive query functions
this spec itself adds to attest's module, `Assignments.oldest_open/2`
and `Assignments.attest_count/2`. They are extensions THIS spec
authorizes on the attest module, built in this spec's lane; attest r5's
public-API inventory mirrors them by name. Attest has ruled
camelCase column names; this spec still names attest columns by ROLE
("the opened-at column"), never by literal spelling — if a later attest
revision renames anything, this spec follows attest, never the reverse.

The deterministic backstop for the residency invariant: a resident must
never end a turn with outstanding work and nothing on the record. Every
turn-terminal leaves a terminal filing, a continuation, or it is STALLED —
and a stall is an event the substrate reacts to. "Never silent" is a
LIVE/DEAD split, and that split is the core of the design (r11): a
LIVE holder's stall CLAIMS exactly one wake, delivered to it while it
remains live — and because a delivered wake provokes a turn whose
terminal is the next stall edge, live holders SELF-DRIVE the
prod→turn→prod chain up the ladder with no timer (§Self-driving
liveness); a RETIRED holder's stall claims nothing — its open
assignments are DERIVED-STRANDED, a view-state any observer computes
at query time (open ∧ holder retired, §step 7), surfaced by query, not
by event. Idle is an edge, not a state: nothing polls, nothing ticks
on supervision's account, zero cost when quiet.

BUILD ORDERING: cut the worktree from main AFTER attest-v1 merges (attest
itself requires the statute-engine and cli-rust branches — transitively
present). If `assignments`/`attests` or the attest API are absent from
main, STOP and report — do not vendor around it. No cli/ changes in this
build.

## Goals

1. Stall detection at turn-terminal, event-driven: the gateway's own
   terminal transitions are the only steady-state trigger (plus a
   start-time recovery sweep — §The seam); zero polling, zero clocks.
2. The prod: for a LIVE holder, exactly one CLAIMED neutral countdown
   wake per stall event, delivered to it while it remains live
   (duplicates only across a crash boundary — accepted), origin
   `process:tightbeam`, satisfied only by state (rows), never by
   words. A RETIRED holder's stall claims no wake — its open
   assignments are DERIVED-STRANDED, computed at query time, never
   delivered (§step 7).
3. Per-assignment prod counter with progress-reset / pause semantics, and
   the escalation ladder over `spawned_by` with the owner-Main terminus.
4. The residency guidance line and the dispatching skill (design item 4).

## Non-goals (later specs; do not build)

Check-tier completion gating. `tightbeam probe` subcommand. Ephemeral
watcher. Lineage env markers / census. Re-staffing or any punitive verb.
New CLI subcommands or inspect surface for prod state. Per-assignment or
per-archetype N overrides. Statute-expressed supervision policy. A
PERIODIC safety sweep of ANY kind — RULED OUT by Flynn (r11), no
longer an open question: live holders self-drive their own ladder
(§Self-driving liveness) and dead holders' work is derived-stranded
at query time (§step 7), so no timer has a correctness job; only the
start-time recovery sweep is in scope. No UI.

## The seam (exact, from lib/ as of main)

Turn-terminal transitions happen in exactly three places, all via
`Ledger.finish/4` CAS wins or `Ledger.recover_running/1`:

- `Tightbeam.SessionLane.finalize/3` (lib/tightbeam/session_lane.ex) —
  normal completion, failure, task crash.
- `Tightbeam.SessionLane.handle_call(:cancel_current, ...)` — cancel wins
  the CAS.
- `Tightbeam.Ledger.recover_running/1` at boot (failed_unknown), whose
  rows surface in `Tightbeam.LaneManager.do_reconcile/1` via
  `Ledger.unpublished_terminals/1`.

Hook all three with ONE injected closure, `:on_terminal` (arity 2,
takes the session_key and the terminal turn's `seq` — the stall event's
identity; default `fn _, _ -> :ok end`, same idiom as
`:terminal_publisher`):

- SessionLane: new struct field + opt `:on_terminal`. Invoke as the last
  statement of the `:ok` branch of `finalize/3` (after
  `publish_terminal`; the turn's `seq` is finalize's own argument), and
  in `:cancel_current` immediately after the `Ledger.finish` `:ok` win
  (with `current_seq`). The `:already_terminal` branches never
  invoke it — the CAS winner is the evaluator.
- LaneManager: new opt `:on_terminal`, passed through to lanes in
  `ensure/2`, and invoked in `do_reconcile/1` for each republished row
  after `terminal_publisher` + `mark_published` (covers boot-recovered
  terminals; the republished row carries the same `seq` as any cast the
  lane already sent, so a double evaluation is a watermark no-op — see
  Invariant 8).
- Composition (`Tightbeam.Gateway.children/1`): the closure is a CAST
  into a single new GenServer:

      on_terminal = fn session_key, seq ->
        Supervision.notify_terminal(session_key, seq)   # GenServer.cast
      end

DERIVED STRANDING (r11, Flynn's ruling — dissolves r10-review finding
2): an assignment is STRANDED iff it is OPEN and its HOLDER session is
RETIRED. That is a DERIVED VIEW-STATE, computed at query time by any
observer from the join (assignment holderKey → session state via
attest's `Assignments.list` + `Org.get`) — NOT a fact supervision must
reliably emit, store, or keep current. Nothing in this spec's
correctness depends on a stranded record being written: the
post-clear/pre-tick retirement race, a pending outbox entry sitting
occupied at retirement, a crash sliver between `Org.retire` and any
notification — all are harmless, because the next query recomputes
stranded work from scratch (thin-event/fat-query, per the decisions
ledger's observability-v1 model). The `supervision_stranded` lifecycle
row survives only as an OPTIONAL BEST-EFFORT DOORBELL — a prompt UI
notification that stranded work exists — emitted where supervision
happens to encounter a retired holder; a lost or duplicated doorbell
row changes nothing.

THE RETIREMENT DOORBELL (r11: the r10 retirement EDGE, kept but
demoted to an optional best-effort doorbell): retirement already flips
state and broadcasts to clients (`Org.retire` + `broadcast(...
Payloads.stream_deleted ...)`, gateway.ex ~1832-1833; `Org.retire`,
org.ex ~331-333). KEEP the ONE injected closure `:on_retired` (arity
1, the retiring session_key; default `fn _ -> :ok end`, same idiom as
`:on_terminal`), threaded as a gateway verb-handler opt exactly like
`:lane_manager`, invoked as the last statement of the retire verb's
active branch — immediately after `Org.retire` + `broadcast`. In
`children/1` the closure is a CAST into the same Supervision server:

      on_retired = fn session_key ->
        Supervision.notify_retired(session_key)          # GenServer.cast
      end

`notify_retired/2` (`notify_retired(server \\ Tightbeam.Supervision,
session_key)`) handles the cast by enumerating that session's open
assignments (attest's `Assignments.list`, open-state filter, holder =
the retired key) and emitting the best-effort doorbell for each
(§step 7's doorbell write) — NO wake, NO claim, NO watermark write;
wrapped in the same total catch. WHY KEPT rather than cut: the
doorbell's entire value is PROMPTNESS — without this edge it could
fire only at restart sweeps or incidental drains, i.e. never in steady
state — and the hook site is real, unique, and one closure in the
`:on_terminal` idiom (verified against main: the retire verb's active
branch, gateway.ex ~1832-1833). WHY it is now safe to be best-effort:
the cast is non-durable (a process death between `Org.retire` and the
cast drops it) and it performs no outbox drain (an occupied outbox
entry at retirement stays pending until a later drain) — both were r10
correctness holes and are now, by Flynn's ruling, no holes at all:
stranded-ness is derived at query time regardless, a pending PROD
entry whose holder has retired is cleared without dispatch by
whatever drain next touches it (hygiene, not correctness), and a
pending ESCALATION entry never pins a target at all — the drain
resolves its rung to a live target and dispatches (r12, §step 1).
Nothing anywhere branches on a stranded record existing.

SELF-DRIVING LIVENESS (r11, Flynn's ruling — pinned as the reason no
periodic sweep exists): a prod IS a wake. Delivered to a LIVE holder,
it provokes a turn, and that turn's terminal IS the next stall edge —
so the chain prod→turn→prod→…→escalation advances with NO timer
anywhere. Verified against the code seam at main f739c07 (re-verified for r13,
attest merged): a due wake
row is read by `WakeScheduler.deliver_due` (wakes.ex ~204), which
calls the gateway `deliver` closure (gateway.ex ~203); for a direct
wake to a session whose state is `active` it calls `deliver_prompt`
(gateway.ex ~226-232), which appends the message AND enqueues a turn
in the same transaction (`Ledger.enqueue_in_txn`, gateway.ex ~449-468)
then `LaneManager.ensure_lane` (gateway.ex ~491) runs the lane; that
turn's terminal goes through `SessionLane.finalize/3`
(session_lane.ex ~188) — exactly the `:on_terminal` hook site.

THE ADVANCE HOLDS ONLY IF THE PROD IS ALREADY 'FIRED' WHEN ITS TURN
TERMINATES (r19, the deliver-then-mark race — the fix the r18 BUILD
correctly STOPPED on). "That turn's terminal claims the NEXT prod" is
the load-bearing step of self-driving, and on main it is NOT automatic:
delivery is DELIVER-THEN-MARK. `deliver_due` (wakes.ex ~204-233) calls
the deliver closure — which runs `deliver_prompt`'s enqueue transaction
(append + `Ledger.enqueue_in_txn`, gateway.ex ~456-475) and then, POST
COMMIT, `LaneManager.ensure_lane` (gateway.ex ~491) NUDGES the lane —
and ONLY AFTER the closure returns does `deliver_due` open its SEPARATE
transaction marking the wake `pending → fired` (wakes.ex ~220-228). A
fast provoked turn can run to terminal in the gap between the lane
nudge and that fired-mark; supervision then evaluates the terminal
while the ORIGINATING prod wake is STILL 'pending', step 4 reads
`Wakes.pending_count > 0`, returns `:continuation` (SUPPRESSED, no
claim, no watermark), and the fired-mark then lands producing no new
terminal edge — the chain STALLS PERMANENTLY (a live holder, so nothing
is derived-stranded, and the watermark refuses no reclaim because
nothing was claimed; only an external terminal or a restart sweep can
ever restart it). The fix (r19, §Atomic wake delivery): supervision's
own delivered wakes are marked FIRED ATOMICALLY inside `deliver_prompt`'s
SAME enqueue transaction (the `:fire_wake_in_txn` opt), so the prod is
committed 'fired' BEFORE `ensure_lane` even nudges the lane — the turn
it provokes can NEVER observe it 'pending', step 4's only surviving
`:continuation` is a continuation the AGENT actually scheduled, and the
prod→turn→prod advance holds by construction. The
chain terminates only when: the holder files progress (counter reset),
the ladder reaches the no-wake terminus (self-target), or the holder
DIES — a wake to a non-active session is a deliberate no-op
(gateway.ex ~226; wakes.ex marks it fired; r13: the state read and
the no-op decision happen INSIDE the delivery transaction — §Atomic
wake delivery — same outcome, now race-free), no turn ever comes,
and the holder's open assignments are exactly the derived-stranded set
per the ruling above. That silent no-op is the behavior for prods and
for every plain wake; it is NOT the behavior for a supervision
ESCALATION wake — those carry the `reresolve` triple and are
re-resolved to a live recipient, atomically with the enqueue, at that
exact branch (r12/r13, §Escalation delivery re-resolution), so an
escalation recipient's death is NOT a fourth terminator of the chain
(the r11-review finding-1 hole, closed). That live/dead split IS "never silent": LIVE
holders are prodded (self-driving); DEAD holders' open assignments are
derived-stranded (query-surfaced).

ESCALATION DELIVERY RE-RESOLUTION (r12, closing r11-review finding 1
— the mechanism that makes escalation delivery unconditional). The
hole had two variants, both confirmed against main pre-r12 (and the
race remainder against f739c07 by the r12 review):
POST-DISPATCH — escalation claimed, wake row created, outbox cleared
and `prodCount` advanced; target S retires before the tick; the
deliver closure's non-active branch returns `:ok` (gateway.ex
~224-225) and `deliver_due` marks the wake fired (wakes.ex ~219-229)
— counted delivered, received by no one. PRE-DISPATCH — the pending
escalation entry's target retires before the drain; r11 cleared
without dispatch and waited for "the next edge or the next restart
sweep", but the holder's reply-chain already ended at the escalation
(no next edge comes internally) and the sweep dies at `:duplicate`
(the claim already watermarked that terminal). In both variants the
holder is LIVE — so the assignment is NOT derived-stranded and no
query surfaces anything wrong — and the ladder is permanently
silent. The fix exploits Main immortality end to end; the rule is:
AN ESCALATION'S RECIPIENT IS NEVER PINNED — it is resolved at every
dispatch and re-resolved at every delivery, and every resolution
walk sinks at the owner's Main, which cannot die:

- CLAIM: the outbox stores the RUNG (`pendingK`), never a target —
  `pendingTarget` is deleted (§Schema). There is nothing in the
  outbox that can go stale by dying.
- DISPATCH (act/drain, §steps 1 and 9): the target is resolved THEN,
  `ladder_target(db, session_key, pendingK)` — retired ancestors are
  skipped at walk time and the walk terminates at the immortal Main,
  so the resolved target is always a live session. The r10/r11
  retired-ESCALATION-target clear-and-wait drain branch is DELETED —
  there is no pinned target to find retired.
- DELIVERY (r13 — atomic, holder-seeded): supervision's escalation
  dispatch passes THREE additive optional wake params — `reresolve:
  "lineage"` plus its resolution inputs `reresolve_seed` (the HOLDER
  key — the watermark row's own sessionKey) and `reresolve_rung`
  (the rung — pendingK) — persisted as nullable `wakes.reresolve` /
  `wakes.reresolveSeed` / `wakes.reresolveRung` columns; defaults
  nil preserve today's behavior exactly (§Public API). Delivery is
  CHECK-AND-ACT ATOMIC (§Atomic wake delivery): the target-state
  read runs INSIDE `deliver_prompt`'s one enqueue transaction, and
  on reading the direct target non-active, a wake with
  `reresolve = "lineage"` re-RUNS
  `ladder_target(txn, wake.reresolveSeed, wake.reresolveRung)` IN
  THAT SAME TRANSACTION — the IDENTICAL holder-seeded walk the
  dispatch ran (visited set seeded with the holder, retired rungs
  skipped, Main sink), on fresh truth — and enqueues to the session
  it resolves (same wake_id, same stamped prompt), instead of the
  silent no-op. `ladder_target` is a PURE module function (row reads
  only, no GenServer interaction — the deliver closure runs in the
  WakeScheduler process and must not call into the Supervision
  server; it reads via the open transaction handle), its walk is
  total, and it sinks at
  `Org.personal_session_key(holder.owner_user_id)` — the owner's
  Main, which exists and is active by construction (retire denies
  built-ins, gateway.ex ~1823). The resolved target is live AS OF
  THE DELIVERY TRANSACTION, and the enqueue commits in that same
  transaction — no retirement can slip between resolution and
  enqueue. The r12 `lineage_target/2` is DELETED — r12-review
  finding 2: a resolver that walks up from the DEAD target without
  the holder in its visited set resolves the cycle H→S→H (S
  retired) back to H, the original holder, where the holder-seeded
  walk skips the cycle and resolves Main. Re-resolution must be the
  SAME walk as dispatch — and now it is: the wake row carries the
  walk's inputs precisely so delivery can re-run it.

COHERENCE (r13 — now definitional): dispatch-time and delivery-time
resolution are the SAME FUNCTION on the SAME inputs
(`ladder_target(holder, rung)`), differing only in WHEN they read
the org — delivery runs it later, with fresher truth, inside the
enqueue transaction. The frozen text (`pendingK`/`pendingN`) is
unaffected: the escalation template names the holder and the rung,
never the recipient, so a re-resolved delivery carries the
identical message. Redelivery across a crash is deduped by
`turns.wakeId` UNIQUE exactly as today — even if successive
attempts resolve different recipients (further retirements), at
most one turn is ever enqueued per wake.

ATOMIC WAKE DELIVERY (r13, closing r12-review finding 1 — the
load-bearing fix; the header's ⚑ FLYNN FLAG records the fallback).
The r12 delivery path was check-THEN-act across TWO DB-owner calls:
the deliver closure read the target's state (`Org.get`, gateway.ex
~226) and only then called `deliver_prompt`, whose transaction
appends the echo and enqueues the turn (gateway.ex ~448-468);
`Org.retire`'s write (gateway.ex ~1832) could commit in the gap —
the turn landed on a retired session and `deliver_due` marked the
wake fired (wakes.ex ~219-230), "delivered" to no one; for an
escalation the always-live guarantee was therefore false. r13 makes
delivery CHECK-AND-ACT ATOMIC at the only seam that needs it — the
DIRECT-wake branch of the composed deliver closure moves its
target-state read INSIDE `deliver_prompt`'s existing single
transaction. Every `DB.transaction/2` body runs as ONE
BEGIN IMMEDIATE…COMMIT pass inside the single DB-owner process
(db.ex — one connection, one mailbox), and `Org.retire` is itself
one owner call, so the two serialize whole-before-whole: the
delivery transaction reads the target either LIVE — and the enqueue
commits in the same transaction; a retire arriving next serializes
AFTER an enqueued turn, the ordinary retire-with-work-queued case —
or RETIRED, and the SAME transaction re-resolves
(`reresolve = "lineage"`: the ladder re-run above) or no-ops (a
prod / any plain wake: no append, no enqueue; `deliver_due` marks
the row fired as today — the derived-stranded boundary, now
race-free). MECHANICS, pinned: `deliver_prompt` gains ONE additive
optional opt, `:target_gate` — nil (default) preserves today's
behavior for every existing caller ("post", role wakes); the wake
deliver closure passes the wake row. With the gate present, the
transaction body FIRST reads the target session's row in-txn (the
`must_get`/`Txn.q` idiom org.ex already uses inside transactions):
`active` → append + enqueue as today; non-active ∧
`wake.reresolve = "lineage"` →
`target := ladder_target(txn, wake.reresolveSeed,
wake.reresolveRung)`, then append + enqueue to THAT key in the same
transaction; non-active otherwise → return `:skipped` (no append,
no enqueue). Post-commit side effects (publish, turn-state
broadcast, `ensure_lane`) run for the session actually enqueued.
The role-wake branch is otherwise untouched — `Roles.resolve` keeps
its own semantics (its races are §step 4's inherited edge windows,
out of scope). SCOPE NOTE, deliberate: this is a general
correctness improvement to the SHARED wake pipeline — for every
non-supervision direct wake the retired-target no-op becomes
race-free with identical observable behavior — not a
supervision-specific branch; only wakes carrying `reresolve` gain
new behavior. FEASIBILITY FALLBACK (Flynn's decision, not the
builder's): if the wrap proves infeasible in the real deliver path
— e.g. the in-txn state read or the txn-scoped ladder walk cannot
be made to fit `deliver_prompt`'s transaction — STOP and report;
the recorded alternative is a bounded safety sweep, and choosing it
reopens the no-periodic-sweep ruling, which only Flynn may do.

ATOMIC FIRED-MARK (r19, closing the deliver-then-mark self-suppression
race the r18 BUILD correctly STOPPED on — the SECOND atomicity property
of gated delivery, distinct from the r13 target-state-read atomicity
above and scoped MORE NARROWLY). The race, exact, verified against main
5770d7c: `Wakes.deliver_due` is DELIVER-THEN-MARK by construction
(wakes.ex ~201-233, and the module's own "never reorder" moduledoc) —
(1) it calls `deliver.(wake)`, which runs `deliver_prompt` (the enqueue
transaction commits the turn) and then, POST-COMMIT, nudges the lane
via `LaneManager.ensure_lane` (gateway.ex ~491); (2) the lane is now
running the provoked turn; (3) ONLY AFTER `deliver.(wake)` returns does
`deliver_due` open its SEPARATE `transaction!` marking the wake
`pending → fired` (wakes.ex ~220-228). A fast turn terminates between
(2) and (3); supervision evaluates that terminal with the originating
prod wake STILL 'pending', step 4 (`Wakes.pending_count > 0`) returns
`:continuation` — SUPPRESSED — and the fired-mark then lands producing
no new terminal, permanently stalling the prod→turn→prod chain
(§Self-driving liveness). This threatens LIVENESS, not boundedness (a
stalled chain is still bounded — §Cascade-boundedness is unaffected),
but it silences a live holder's ladder, which the invariant forbids
(Invariant 5). THE FIX (Flynn-orchestrator PRIMARY ruling — the
source-level fix): for SUPERVISION'S OWN delivered wakes ONLY, the wake
is marked FIRED ATOMICALLY inside `deliver_prompt`'s SAME enqueue
transaction — so a delivered supervision prod is committed 'fired'
BEFORE the post-commit `ensure_lane` nudge and is NEVER observable as
'pending' by any later terminal. MECHANICS, pinned: `deliver_prompt`
gains ONE further additive optional opt, `:fire_wake_in_txn` (boolean,
default false — every existing caller and every non-supervision wake
keeps today's deliver-then-mark exactly). When true (and
`opts[:wake_id]` present), the enqueue transaction, on its
append+enqueue path (target active, OR the `reresolve` re-resolved key
above), executes ONE additional statement — the SAME CAS `deliver_due`
uses: `UPDATE wakes SET state = 'fired', firedAt = ? WHERE wakeId = ?
AND state = 'pending'` — on the open `txn` handle, atomically with the
append and enqueue. The `:skipped` path (a retired-holder prod, no
`reresolve`) enqueues NOTHING and fires NOTHING in-txn — `deliver_due`
marks it fired post-closure exactly as today (no turn is enqueued, so
there is no self-drive and no race). `deliver_due` is otherwise
UNCHANGED: its post-closure CAS `WHERE state = 'pending'` is a benign
idempotent no-op for a wake already fired in-txn, and it remains the
sole fired-marker for every non-gated wake. SCOPE — the wake deliver
closure sets `:fire_wake_in_txn` true for DIRECT wakes whose origin is
the substrate's supervision process origin (`process:tightbeam` — the
marker that selects exactly supervision's prods and escalations among
wake rows; `notify_session`/push use that origin but never create wake
rows, verified against main); post, role, and external direct wakes are
NOT gated and keep today's post-closure fired-mark UNCHANGED (minimal
blast radius, Flynn's ruling).

RESERVED ORIGIN — `process:tightbeam` IS EXCLUSIVE TO THE SUBSTRATE (r20,
closes review finding 1). The marker above only selects supervision's own
rows if no external caller can create a wake row carrying that origin.
Today the external attribution seams accept it: an authenticated org-CLI
request with `asProcess: "tightbeam"` resolves to origin
`process:tightbeam` (router.ex `agent_identity(:org)` ~332 and
`agent_origin` ~410–415) and the wake handler persists it unchanged, so
the selector would gate a forged external wake. INVARIANT (integrity, not
policy — the substrate's own canonical self-name is not externally
attributable, exactly as one session cannot forge another's identity):
the process attribution seams REJECT the reserved name `tightbeam`. Both
`asProcess` acceptance points (`agent_identity(:org)` and `agent_origin`)
return `403 reserved_origin` ("process:tightbeam is reserved to the
substrate") when `asProcess == "tightbeam"`; no other process name is
touched. This is the ONE reserved name — the exact string the supervision
composition closure emits — so after r20 origin `process:tightbeam` on a
wake row can ONLY have been created by supervision, and the
`:fire_wake_in_txn` selector is exact by construction. The bare local
`process:` power vocabulary (wake + cancel-own-wakes) is otherwise
unchanged; every non-reserved process name still attributes normally. `deliver_prompt` itself learns nothing
of supervision — the supervision/non-supervision decision lives in the
composition closure (`children/1`), and `deliver_prompt` exposes only
the generic "fire this wake_id in my txn" capability. FEASIBILITY
(verified, so the atomic-fire approach is TAKEN): the fired-mark is one
in-txn CAS added to a transaction that already writes (append +
`enqueue_in_txn`), on the DB owner's single mailbox, `opts[:wake_id]`
already threaded to `deliver_prompt` (gateway.ex ~463) — no new seam,
no walk, no owner call. RECORDED FALLBACK (Flynn's alternative, NOT
taken — documented per the r13 ⚑-flag pattern): had the in-txn fire
been infeasible, the suppression-predicate fix instead — supervision's
step-4 `:continuation` suppression is for a FUTURE continuation the
AGENT scheduled, never for supervision's OWN in-flight prod, so step 4
would EXCLUDE from its pending-count the just-delivered gated wake
whose delivery is in-progress/done (matched by wake origin +
`sessionKey` = the holder). It is not needed because the atomic-fire
removes the observable-'pending' window entirely at the source.

WHY DELIVERY-TIME, NOT A RETIREMENT EDGE: this is the one place
retirement handling is LOAD-BEARING again — for ESCALATIONS ONLY —
and it deliberately does NOT ride `notify_retired`. The retirement
cast is non-durable (a process death between `Org.retire` and the
cast drops it forever), and unlike derived stranding NO QUERY
SELF-HEALS A STUCK LADDER — a live holder's silenced escalation is
invisible to the stranded view (holder not retired) and refused by
the watermark (`:duplicate`). An unreliable edge guarding a
non-self-healing loss is exactly the crash-sliver-fatal shape r11
deleted. Delivery re-resolution is crash-robust instead: the wake
row is DURABLE and `deliver_due` retries it until it delivers, so
the re-resolution decision is re-made at every attempt, whatever
crashed in between. `notify_retired` stays what r11 made it — an
optional promptness doorbell with no correctness role.

New module: `Tightbeam.Supervision` (lib/tightbeam/supervision.ex) — a
GenServer started in `children/1`, opts `:db`, `:handlers`,
`:prod_limit`, `:name` (default `Tightbeam.Supervision`). Each cast is
handled by running `evaluate/5` synchronously inside the server, so ALL
evaluations serialize through one mailbox — which subsumes per-session
serialization. What serialization buys is ORDER; the correctness
contract is EXACTLY-ONCE COUNTING, LIVE-TARGET DELIVERY (Invariant 8;
the r11/r12 qualification — a claimed PROD is delivered to its
holder while the holder remains LIVE, re-dispatched across crashes
until delivered or converted, and a DEAD holder's obligation is
surfaced as derived-stranded, never delivered; a claimed ESCALATION
is ALWAYS delivered to a live session — its target is resolved at
dispatch and re-resolved at delivery, sinking at the immortal Main
(r12, §Escalation delivery re-resolution) — so the only delivery
this spec ever declines is a dead HOLDER's
prod): at most one CLAIM per (session, terminal) — the per-session
MONOTONE watermark (`supervision_watermarks.lastEvaluatedTerminal`,
compared `terminal_seq <= watermark`, moved only upward) — and the
claim transaction also records the decided action in the OUTBOX
columns of the same row (`pendingBranch`,
`pendingAssignment`; non-NULL pendingBranch IS the ruling's
actionPending flag; NO target column — the recipient is derived at
act time, §Schema). The act phase drains the outbox: dispatch, then a
second small write that clears the pending entry and advances the
delivered counter. A crash between claim and dispatch leaves the
pending entry, and EVERY evaluation and sweep drains any pending entry
first — a claim cannot be silently lost (r4's hole: a lost claim
watermarked its own terminal and became unrecoverable). A crash
between dispatch and clear re-dispatches on the next drain: a rare
DUPLICATE wake, accepted and documented — a duplicate prod is a
harmless message, while permanent silence violated the invariant.
That is the tradeoff, chosen deliberately. Re-acting never advances
any counter — the claim already counted (`attemptCount`); the
delivered counter (`prodCount`) advances exactly once, in the guarded
clear.

NO INLINE FIRING — supervision's wakes ride the tick: every
supervision dispatch passes `nudge: false` (an ADDITIVE optional param
on the existing wake verb; default `true` preserves today's behavior
exactly; ESCALATION dispatches additionally pass the `reresolve`
triple — §Escalation delivery re-resolution), so the
wake handler persists the scheduled row (dueAt = now)
and SKIPS the immediate `Wakes.fire_due` nudge — the row is delivered
on a SUBSEQUENT WakeScheduler tick. Delivery is EVENTUAL, not a latency
SLA and NOT bounded by `TIGHTBEAM_WAKE_TICK_MS`: the scheduler's
`deliver_due` is a serial pass that may synchronously call
`LaneManager.ensure_lane` (gateway.ex) and schedules its next tick only
after that pass returns (wakes.ex), so end-to-end latency is bounded by
the scheduler's own throughput, not by one tick. The guarantee this
spec makes is eventual delivery WITHOUT supervision blocking on it —
fine for prods. The param rides
the repo's own principle (the doorbell is an optimization; the scan is
the guarantee). Consequence: Supervision's act phase never calls into
WakeScheduler, `deliver_prompt`, or LaneManager at all — its only
synchronous dependency is the DB owner. Any WakeScheduler tick-path
crash risk (`deliver_due`'s rescue misses exits from `ensure_lane`) is
PRE-EXISTING behavior for every due wake in the system; supervision
only adds rows to that existing pipeline and adds no new trigger of
it.

CHILD ORDER IS LOAD-BEARING on one edge: start Supervision BEFORE
`Tightbeam.LaneManager`. LaneManager's `init` runs its first
reconcile, which may invoke `on_terminal`; a cast to a not-yet-started
named server is silently dropped — a missed stall event. (Supervision's
position relative to Wakes stopped mattering in r5 — it never calls
into WakeScheduler — but keep the slot after `Tightbeam.Wakes` for
stability.) Pin the order in the children list and test it.

THE CAST IS LOAD-BEARING for serialization, not deadlock-avoidance:
r5's evaluation touches only the DB, so the old inline-deadlock chain
(Supervision → WakeScheduler → LaneManager) is gone, but terminal
sites still must not block on evaluation, and the single-mailbox
serialization is what makes the claim writes exclusive — all
evaluations run in the one Supervision server. Do not "simplify" the
cast to a call, and do not evaluate inline at the terminal sites.

THE TOTAL CATCH IS LOAD-BEARING: the Supervision server wraps EVERY
evaluation — outbox drains and the sweep's per-candidate calls
included — in a total catch: `rescue` for raises PLUS `catch :exit, _`
/ `catch :throw, _`, statute-engine style. The act phase can still
fail: `Dispatch.invoke` rescues raises only (dispatch.ex), the
accepted-path `:ok = EventLog.append_event` raises on a sink failure,
and DB-owner calls can exit on timeout. Supervision must NEVER crash
into the rest_for_one blast radius: a Supervision crash restarts
LaneManager, whose init runs `recover_running` and marks every running
turn org-wide `failed_unknown` while its lane and task still live —
fresh spurious terminals, possible prods to actively working sessions,
and a max_restarts budget burned toward whole-BEAM shutdown. On
escape, append one lifecycle row —
`EventLog.lifecycle(db, "supervision_evaluate_failed", session_key,
detail)`, itself best-effort (the failure log must not crash the
server) — and continue to the next message. A caught failure is safe
by construction: the claim and its outbox entry are already durable,
so the pending action is re-dispatched by the next drain — delivery
late, never lost.

RECOVERY SWEEP (every Supervision start, including restarts): the child
order closes the STARTUP window, not the RESTART window — lanes live
under `Tightbeam.LaneSupervisor`, which precedes every gateway child in
the one rest_for_one root (application.ex), so lanes OUTLIVE a
Supervision crash; a lane's finalize marks the row published and THEN
casts, so a cast fired while Supervision is down (or queued in its dead
mailbox) is dropped, and reconcile never re-fires it —
`unpublished_terminals` only revisits unpublished rows. Left alone, a
session whose last terminal lands in that gap stalls silently forever,
violating Invariant 5. Therefore every Supervision start runs a
recovery sweep over the UNION of (a) every session holding ≥ 1 open
assignment and (b) every session with a non-NULL pendingBranch in
supervision_watermarks (one query on supervision's own table — a
pending entry whose assignment closed while Supervision was down must
still drain; open-assignment enumeration alone would orphan it). For
each candidate, FIRST drain any pending outbox entry (step 1 of
§steps — a claim is a promise that predates any retirement, and
step 1's rules govern the drain: a PROD whose holder — the row's own
sessionKey, a prod's only possible target — is RETIRED clears
without dispatch, a dead holder's obligation, derived-stranded by
any query and never delivered (optionally one best-effort doorbell,
§step 7); an ESCALATION never pins a target — the drain resolves
`ladder_target(session_key, pendingK)` NOW, skipping retired
ancestors and sinking at the immortal Main, and DISPATCHES to that
live target (r12 — the clear-and-wait branch for a retired
escalation target is DELETED, §Escalation delivery re-resolution);
the transient-error short-circuit applies only where a dispatch is
actually attempted), THEN: if the holder session is RETIRED, skip it —
its open assignments are the derived-stranded set, surfaced by query,
not by this sweep (the sweep MAY emit the best-effort doorbell per
§step 7, deduped by `strandedAt`; nothing depends on it) — and move to
the next candidate; otherwise evaluate the CURRENT stall predicate. DRAIN RULE for a
closed assignment (here and in step 1 everywhere): if the pending
entry's pendingAssignment is no longer open, CLEAR WITHOUT DISPATCH,
counters untouched — the obligation is gone, the episode is over; a
prod naming a closed assignment must never be sent. That
framing is the sweep's SEMANTICS, not shorthand — the sweep does not
claim to act only on missed events; it acts wherever the predicate
holds NOW. A terminal once legitimately suppressed by a then-pending
wake that has since been canceled is genuinely stalled now — prodding
is CORRECT. A last terminal that predates the assignment's opening is
an idle holder with an open obligation — the invariant's exact target
— prodding is CORRECT. What the sweep never does is re-COUNT a
claimed edge: the monotone session watermark
(`terminal_seq <= lastEvaluatedTerminal` → `:duplicate`/`:coalesced`)
refuses every already-claimed terminal, and the only re-dispatch is of
a pending, never-cleared outbox entry — which advances no claim
counter. Candidates come from attest's existing public surface —
`Assignments.list` with the open-state filter, distinct holder keys;
no new attest API. For each candidate the triggering terminal is
`Ledger.last_terminal_seq(db, session_key)` (nil → skip for the
predicate; the OUTBOX drain still runs — a pending entry is a claimed
action and must deliver to its live target, or convert per step 1's
closed-assignment / retired-holder-prod / escalation-resolution
rules), run through the SAME
serialized `evaluate/5` path. This start-time sweep is the ONLY sweep:
between starts, liveness is the self-driving chain (§Self-driving
liveness) — a wake the sweep or an edge scheduled provokes the turn
whose terminal is the next edge, and no timer is needed or permitted.

Sweep trigger mechanics (r5: back in Supervision's OWN init): `init`
returns `{:ok, state, {:continue, :recovery_sweep}}`; the
`handle_continue` runs the sweep before any queued cast, in the same
serialized server. This is safe now precisely because of NO INLINE
FIRING: the sweep's act phase is DB writes only — it schedules wake
rows and never calls WakeScheduler or LaneManager, so it cannot race
their startup (r4 had to trigger from `LaneManager.init` because its
act phase ended in `ensure_lane`; that chain no longer exists, and the
LaneManager `:supervision` opt is DELETED with it). Every Supervision
start — boot or restart — therefore runs exactly one sweep, by
construction. `request_sweep/1` remains as the public cast for tests
and forensics; it runs the identical sweep. Wake rows the sweep
schedules during boot are delivered by WakeScheduler's tick like any
other due wake; the tick's boot-window exposure is pre-existing and
supervision-neutral (see NO INLINE FIRING). This sweep is
RESTART-RECOVERY ONLY: a PERIODIC safety sweep is RULED OUT (r11,
Flynn — §Non-goals): the loss classes it would have caught are covered
by the self-driving chain for live holders and by derived stranding
for dead ones; a clock would add nothing but cost.

Register `Tightbeam.Supervision` in the `ensure_schema` list in
`Gateway.children/1` after the attest module(s).

## Schema (two tables; repo migration conventions)

    CREATE TABLE IF NOT EXISTS assignment_prods (
      assignmentId TEXT PRIMARY KEY REFERENCES assignments(id),
      attemptCount INTEGER NOT NULL DEFAULT 0,  -- claims this epoch, incl. statute-denied attempts
      prodCount    INTEGER NOT NULL DEFAULT 0,  -- DELIVERED wakes this epoch; drives branch, ladder, text
      deniedStreak INTEGER NOT NULL DEFAULT 0,  -- consecutive statute-denied attempts; reset on delivery
      attestCount  INTEGER NOT NULL DEFAULT 0,  -- attest rows for the assignment at last claim
      lastProdAt   INTEGER,                     -- when a wake row was last actually CREATED
      stalledAt    INTEGER,                     -- set at first escalation CLAIM of the current epoch
      strandedAt   INTEGER NULL                 -- best-effort DOORBELL dedupe only (r11): stamped when a
                                                -- stranded doorbell row is emitted for this assignment;
                                                -- NOTHING correctness-bearing branches on it — stranded-ness
                                                -- itself is DERIVED at query time (open ∧ holder retired)
    );

    CREATE TABLE IF NOT EXISTS supervision_watermarks (
      sessionKey            TEXT PRIMARY KEY,
      lastEvaluatedTerminal INTEGER NOT NULL,   -- turns.seq of the newest CLAIMED terminal; monotone
      pendingBranch         TEXT CHECK (pendingBranch IN ('prod','escalation','terminus')),
                                                -- OUTBOX: non-NULL = claimed action not yet acted
      pendingAssignment     TEXT,               -- assignment id the pending action belongs to
      pendingK              INTEGER NULL,       -- the k (prod) or RUNG (escalation) this delivery bears
      pendingN              INTEGER NULL        -- the prod_limit in force at the claim
    );

NO TARGET COLUMN (r12): the outbox records WHAT was claimed — branch,
assignment, and the frozen numbers — never WHO receives it. The
recipient is DERIVED at act/drain time: a prod or terminus targets
the row's own `sessionKey` (the holder — a prod's target is always
its holder, and a terminus never dispatches); an escalation resolves
`ladder_target(sessionKey, pendingK)` at dispatch. The r5–r11
`pendingTarget` column is deleted BECAUSE it was r11-review finding
1's bug class: a pinned target can die between claim and act, and
clearing the entry on its corpse wedged the ladder forever. For
escalation entries `pendingK` IS the pending rung. (r13: at dispatch
the escalation's WAKE row is stamped with the same resolution inputs
— `reresolveSeed` := the row's own sessionKey, `reresolveRung` :=
pendingK — so DELIVERY can re-run the identical holder-seeded walk;
§Escalation delivery re-resolution.)

(The FK names attest's primary-key column as `id` per attest r5; like
every attest column reference in this spec, follow the spelling attest
lands with.) Two watermarks, two scopes: `attestCount` is the PROGRESS
watermark, per-assignment — a ROW COUNT, not a max id, because attest
ids are TEXT and row count is monotone (attest rows are never
deleted). `lastEvaluatedTerminal` is the STALL-EVENT watermark,
PER-SESSION — r4 moved it off the assignment row, because an
assignment-scoped watermark lets a revoked target re-arm an
already-claimed terminal (`oldest_open` shifts to a fresh row), and a
last-seq EQUALITY check re-acts on out-of-order republishes of older
terminals and rolls the cell backward. It holds the `seq` (INTEGER
PRIMARY KEY AUTOINCREMENT, ledger.ex) of the newest terminal the
session's evaluation ever CLAIMED; dedupe is
`terminal_seq <= watermark`, and claims only move it upward —
monotone, never rolled back. TWO COUNTERS, split by r5 (a
statute-denied attempt must not walk the ladder or falsify the
templates): `attemptCount` advances on every claim; `prodCount`
advances only when the wake row was actually created, in the guarded
outbox clear — it alone drives the prod/escalation branch, the rung,
and the `<k>`/`<N>` numbering, so "N prods" in any template always
means N DELIVERED prods. The four pending* columns are the OUTBOX:
written by the claim, cleared by the act — the successful clear NULLs
ALL of them, `pendingK`/`pendingN` included; non-NULL `pendingBranch`
is the actionPending flag. `pendingK` and `pendingN` FREEZE the
numbers the claimed delivery bears (the k-or-rung, and the prod_limit
in force at the claim): the act renders template text entirely from
the stored entry, never from current counters or current n, so a
replay after restart reproduces the claimed text exactly even across
a prod_limit change. `strandedAt` (r11) is the best-effort DOORBELL
dedupe stamp and nothing more: when supervision emits the optional
`supervision_stranded` doorbell row for an assignment (§step 7) it
upserts the `assignment_prods` row if absent and stamps
`strandedAt := now WHERE strandedAt IS NULL`, emitting the doorbell
row only when the stamp took effect — so repeat encounters (every
restart sweep, say) do not spam the log. The stamp, the row, and
their pairing are ALL best-effort: a lost stamp means a duplicate
doorbell, a lost row means a missing doorbell, and both are harmless
because stranded-ness is DERIVED at query time (open ∧ holder
retired) — no code path branches on `strandedAt` or on a
`supervision_stranded` row existing. (This replaces the r9/r10
one-transaction protocol, which is deleted as a correctness
requirement, and moots the r10-review finding-5 absent-row question:
the write is an upsert, and even a wrong write would break nothing.)
These tables are supervision's own state;
the `assignments` table and the attest verbs are not modified in any
way. The `stalled` stamp of the design is `stalledAt` on the counter
row.

## The predicate and the executor

`Supervision.evaluate(db, handlers, n, session_key, terminal_seq)` —
the cast handler's body: synchronous, pure DB + one dispatched verb;
unit-testable without processes by calling it directly. `terminal_seq`
is the triggering terminal turn's `seq` — the stall event's identity —
or nil (a sweep candidate with no terminal history: the outbox drain
still runs, the predicate is skipped). Returns a tag
(`:busy | :continuation | :idle | :duplicate | :coalesced
| {:prodded, k} | {:escalated, rung, target} | :terminus | :stranded
| {:refused, code}`) for tests; call sites ignore it. `:stranded` is
the retired-holder branch (step 7): the holder is retired, so nothing
is claimed and nothing is woken — the assignment's stranded-ness is
derived at query time, and the branch's only write is the OPTIONAL
best-effort doorbell. The tag reports
the NEW terminal's outcome; the step-1 drain is a side effect.

The design predicate, conjunct by conjunct (all ledger rows, zero
interpretation):

    stalled(session) := turn just terminal          (the triggering event itself)
                      ∧ no running/queued turn       (Ledger.pending_count == 0)
                      ∧ no pending wake targeting it (Wakes.pending_count == 0)
                      ∧ ≥1 open assignment held      (oldest_open ≠ nil ⇔ open_count ≥ 1)

Steps, in order:

1. OUTBOX DRAIN, unconditional — before dedupe, before the predicate:
   read the session's `supervision_watermarks` row; if `pendingBranch`
   is non-NULL, a claimed action was never cleared — the claim is a
   promise that predates anything that happened since, retirement
   included, and the drain honors it in this order:
   - `pendingAssignment` no longer OPEN → CLEAR WITHOUT DISPATCH,
     counters untouched (the closed-assignment DRAIN RULE, §The seam).
     No doorbell — a closed assignment carries no obligation.
   - else `pendingBranch = 'prod'` → the target IS the holder — the
     row's own `sessionKey` (a prod's only possible target; no target
     is stored, §Schema). If the holder's session state is `retired`
     → CLEAR WITHOUT DISPATCH, same mechanics as the
     closed-assignment clear (all pending* columns NULLed, counters
     untouched); a wake must never be dispatched at a retired
     session, and no dispatch is attempted, so the transient-error
     short-circuit cannot fire here. The obligation is a dead
     holder's — exactly the derived-stranded case, surfaced by any
     query (open ∧ holder retired); this drain owes it NOTHING for
     correctness but MAY emit the best-effort doorbell (§step 7's
     doorbell write, strandedAt-deduped). If the holder is LIVE → ACT
     on it now (the act routine, step 9: dispatch the prod to the
     holder, then the guarded clear).
   - else `pendingBranch = 'escalation'` → NO pinned target exists
     (r12). Resolve `target := ladder_target(db, session_key,
     pendingK)` NOW — the walk skips retired ancestors and sinks at
     the immortal owner's Main, so the resolved target is ALWAYS a
     live session; there is no retired-escalation-target branch left
     to take. (Re-resolution can never yield the holder: an
     'escalation' entry's holder is never a Main — a Main holding its
     own assignment resolves self-target at claim time and writes a
     'terminus' entry — so the drain needs no second self-target
     guard.) ACT: dispatch to the resolved target with the
     `reresolve` triple (§step 9), then the guarded clear. This
     holds even when the HOLDER has since retired: waking a live
     supervisor about a dead worker is correct — "never woken" scopes
     to the retired session itself (§step 7).
   - else `pendingBranch = 'terminus'` → no dispatch was ever
     recorded (a self-target Main). Drain per the TERMINUS act
     (§step 9): re-append the lifecycle row, then clear.
   Post-claim outboxes therefore obey the r12 delivery contract
   exactly: a claimed PROD is delivered to its LIVE holder or
   converted — a retired holder's obligation is derived-stranded,
   never delivered; a claimed ESCALATION is ALWAYS dispatched to a
   live target, resolved at dispatch and re-resolved at delivery
   (§Escalation delivery re-resolution), sinking at the immortal
   Main — a claim can never wedge on a corpse. Re-acting
   advances NO claim
   counter — the claim already counted (`attemptCount`);
   `prodCount`/`lastProdAt` land in the clear, exactly once per claim.
   Continue with the new terminal ONLY if the drain CLEARED the entry
   (delivered, denied-clear, closed-assignment clear, or
   retired-prod-target clear). If the drain
   left the entry PENDING (transient error — the
   supervision_dispatch_failed branch), SHORT-CIRCUIT: return without
   evaluating the new terminal. The single outbox slot must never be
   overwritten while occupied; the skipped terminal is an accepted
   under-evaluation, recovered by predicate-NOW on a later edge or
   sweep.
2. IDLE DETERMINATION, then DEDUPE — in THIS order, so the watermark
   can never swallow the idle determination (r11, fixes r10-review
   finding 4: a drained stale closed-assignment entry followed by
   no-open-assignments must return `:idle`, not `:duplicate`).
   (2a) `a := Assignments.oldest_open(db, session_key)`; nil → return
   `:idle` — the session holds no open assignment, so whatever the
   watermark says about this terminal is irrelevant: no claim, no
   wake, no counter movement, no watermark write; the only write this
   evaluation may have made is a step-1 clear (Invariant 7,
   drain-first-then-idle). `a` — the oldest open, ordered by attest's
   opened-at column (by its landed name) ascending, id ascending as
   tiebreak, limit 1 — is carried forward to step 5.
   (2b) DEDUPE, session-scoped, monotone: if
   `terminal_seq == lastEvaluatedTerminal`, return `:duplicate` (a
   re-delivery of the claimed terminal: finalize-vs-reconcile double
   casts, sweep re-walks). If `terminal_seq < lastEvaluatedTerminal`,
   return `:coalesced` — an OLDER terminal arriving after a newer
   claim (T1's cast lost while Supervision was down, T2 claimed first,
   T1 republished later). Zero writes, zero dispatch, either way, and
   regardless of which assignment `oldest_open` would select now: a
   revoked target cannot re-arm the event, because the watermark
   belongs to the SESSION, not the assignment. `:coalesced` is
   ACCEPTED at-most-once-per-session coalescing, not a defect:
   multiple terminals accumulated while supervision was down are ONE
   stall episode, and one prod per stall episode is arguably the
   CORRECT reading — T2's claim acted (or its outbox entry will, via
   step 1), so the episode is never silent. Absent row = nothing ever
   claimed; evaluate.
3. `Ledger.pending_count(db, session_key) > 0` → return `:busy`.
4. `Wakes.pending_count(db, session_key) > 0` → return `:continuation`.
   This is the PAUSE: a scheduled continuation suppresses the event and
   leaves the counters untouched — pauses are not progress. Pending wakes
   are matched on the stored `sessionKey` (role-targeted wakes count
   against the key they resolved to at schedule time; the predicate never
   re-resolves — a deterministic row lookup, per the substrate boundary).
   NOT SUPPRESSED — supervision's OWN just-delivered prod (r19): the
   wake that PROVOKED this very turn was already marked 'fired' inside
   the same transaction that enqueued the turn (`:fire_wake_in_txn`,
   §Atomic wake delivery), so it is NOT 'pending' and does NOT count
   here. This `:continuation` PAUSE is therefore only ever a
   continuation the AGENT scheduled during its turn — never a
   self-suppression by supervision's own in-flight prod. Without the
   atomic fired-mark this predicate would read the originating prod as a
   pending continuation and stall the self-driving chain permanently
   (the deliver-then-mark race the r18 build stopped on); with it, the
   chain advances by construction.
   Inherited edge windows, recorded here, not re-litigated: the
   suppressing wake may later be canceled, may re-resolve to a different
   session at fire time (role wakes), or may no-op against a retired
   target — in each case no turn ever arrives and the suppressed stall
   stays silent until some future terminal re-fires the edge or a
   sweep finds the predicate true. That is the parent's ratified
   idle-is-an-edge ruling, not an impl defect. Suppressed evaluations
   (`:busy`, `:continuation`, `:idle`) write NOTHING — the watermark
   advances only on a claim, which is exactly what lets a later sweep
   act on a once-suppressed, now-genuinely-stalled session (§sweep).
5. `a` is the oldest open assignment already read at step 2a (non-nil
   here — a nil returned `:idle` there, BEFORE the dedupe). ONE stall
   event → ONE claimed prod (design; for a LIVE holder — a retired
   holder's stall claims nothing, step 7). Other open assignments'
   counters do not advance on this event.
6. Read the `assignment_prods` row for `a.id` (absent = all zeros).
   `cur := Assignments.attest_count(db, a.id)`. If `cur > attestCount`,
   the PROGRESS RESET: `attemptCount := 0`, `prodCount := 0`,
   `deniedStreak := 0`, `stalledAt := NULL` (new attest rows landed
   since the last claim — kind is irrelevant; completion/surrender
   would have closed the assignment and never reach here). Words never
   reset anything: nothing in this module reads message or note content.
   Clearing `stalledAt` on reset is THIS spec's epoch-semantics ruling,
   not the parent verbatim (the parent stamps at first escalation and is
   silent on clearing): the row states the CURRENT epoch truthfully, and
   the permanent record that an escalation epoch ever happened is the
   wake rows and verb event rows, which are never erased.
   Then `attemptCount := attemptCount + 1` — the claim's count.
7. Resolve the branch and target — pure reads, no writes yet, from the
   DELIVERED counter. The self-target TERMINUS guard lives INSIDE the
   ESCALATION branch EXCLUSIVELY (F6 — a prod's target being the holder
   is normal and is NEVER a terminus; applying the guard to both
   branches would forbid every prod):
   - `prodCount < n` → PROD: `k := prodCount + 1` (the number this
     delivery will bear), `target := holder`, ALWAYS dispatched. No
     terminus test — a prod always wakes its holder.
   - `prodCount >= n` → ESCALATION: `rung := prodCount - n + 1`,
     `target := ladder_target(db, session_key, rung)` (§ladder); and
     ONLY here, IF that resolved `target == holder` (a Main holding its
     own assignment escalating to itself) → TERMINUS (no wake, §step 9
     terminus act). (`n = 0`: `prodCount >= n` from the first claim, so
     the first stall escalates.)
   The claim-time resolution DECIDES THE BRANCH ONLY (prod vs
   escalation vs terminus); the resolved target is NOT stored (r12,
   §Schema — no target column) — the act re-resolves at dispatch
   time. The branch decision is stable across the claim→act gap: a
   non-Main holder's escalation can never re-resolve to the holder,
   and a Main holder's terminus can never un-terminus (Main is
   immortal and its chain is empty forever).
   RETIRED-HOLDER RULE (r11, derived): a retired
   holder NEVER claims and is NEVER woken — not prodded, not
   escalated. "Never woken" is scoped to THE RETIRED SESSION ITSELF:
   a live non-holder (spawner ancestor or Main) may still receive an
   escalation ABOUT a retired holder when a pre-retirement claim's
   outbox entry targets it — the step-1 drain dispatches it normally;
   waking a live supervisor about a dead worker is correct. At branch
   resolution (here) AND in the sweep, a holder whose session state is
   `retired` short-circuits: NO wake, NO counter movement, NO
   watermark write for this terminal; return `:stranded`. That is the
   WHOLE correctness obligation — the assignment's stranded-ness is
   DERIVED (open ∧ holder retired), computed at query time by any
   observer from the join; nothing needs recording for it to be true
   or findable. Rationale: a corpse cannot file, and waking anyone is
   a judgment the operator makes from the derived-stranded view — the
   remedy is revocation, per attest.
   THE DOORBELL (optional, best-effort): wherever this rule fires —
   here, in the sweep, in the step-1 retired-prod-target drain, and in
   `notify_retired` — supervision MAY emit one `supervision_stranded`
   lifecycle row per open assignment of the retired holder, as a
   prompt notification only, deduped by the `strandedAt` stamp (the
   upsert protocol, §Schema). Emission, dedupe, and the row itself are
   all best-effort: a lost, duplicated, or never-emitted doorbell
   changes no behavior anywhere — the next query recomputes stranded
   work from scratch. (This dissolves the r9/r10 machinery: the
   one-transaction stranded-write protocol, the four-case (a)-(d)
   ruling, and the post-clear/pre-tick race analysis all existed to
   make EMISSION reliable, and emission no longer has a correctness
   job. A claim still PENDING at retirement is likewise not a problem:
   the entry sits until the next drain converts it — retired PROD
   target → clear, retired ESCALATION target → clear + re-resolve
   (step 1) — and the obligation is query-visible the entire time.)
8. CLAIM — one DB transaction, committed BEFORE any dispatch: upsert
   `supervision_watermarks` (`lastEvaluatedTerminal := terminal_seq`,
   `pendingBranch := branch`,
   `pendingAssignment := a.id`, `pendingK := k_or_rung`,
   `pendingN := n` — the OUTBOX
   entry; no target is written (r12, §Schema — the act derives it);
   pendingK stores the NUMBER this delivery bears and pendingN
   the prod_limit in force at the claim, so a replay
   after restart reproduces the claimed text exactly even if
   prod_limit changed across the restart — the act renders from the
   stored numbers, never from current counters or current n) and
   upsert the
   `assignment_prods` row (`attemptCount`, `attestCount := cur`, and
   on ESCALATION/TERMINUS `stalledAt := stalledAt || now` — the stamp,
   set once per epoch at the first escalation CLAIM; on PROD
   `stalledAt` carried). `prodCount` and `lastProdAt` are NOT written
   here — they belong to the clear. Claim-then-act inverts the
   wakes.ts deliver-then-mark precedent: a crash after the claim
   leaves the outbox entry, and the next drain delivers it — the claim
   is never lost; the reverse order risked acting twice.
9. ACT = drain the outbox entry just written (the same routine as
   step 1, idempotent per claim — guarded by `pendingBranch`):
   - PROD / ESCALATION: dispatch through the chokepoint as an ordinary
     audited verb call, identical shape, only target and text differ.
     The text is rendered ENTIRELY from the stored outbox entry —
     `pendingBranch`/`pendingK`/`pendingN` supply the branch and both
     numbers and `pendingAssignment` supplies the id/subject lookup;
     the RECIPIENT is resolved NOW (r12): prod → the holder (the
     watermark row's own `sessionKey`); escalation →
     `ladder_target(db, session_key, pendingK)` at dispatch time
     (always live — Main-sunk, §step 1). Nothing is read from current
     counters or current prod_limit — so a re-dispatch composes the
     identical message, even across a restart and a config change
     (only the recipient may differ, tracking lineage truth at
     dispatch time — that is the r12 fix, not a defect):

         Dispatch.dispatch(db, handlers, %{
           verb: "wake", origin: "process:tightbeam",
           session_key: target,
           params: %{prompt: text, after_ms: 0, nudge: false}
         })

     (escalations add the `reresolve` triple to params —
     `reresolve: "lineage"`, `reresolve_seed: session_key` (the
     holder — the watermark row's own key), `reresolve_rung:
     pendingK` — §Escalation delivery re-resolution; prods never
     pass any of it: a dead holder's wake must no-op into the
     derived-stranded case, never walk.)

     `{:ok, _}` (the wake row exists, dueAt = now, tick-delivered;
     for an escalation, delivery re-resolves a target that retires
     before the tick — §Escalation delivery re-resolution — so the
     row's eventual delivery to a live session is unconditional) →
     the CLEAR, one small transaction (it spans supervision_watermarks
     AND assignment_prods — never split it): ALL four pending columns
     NULLed (`pendingBranch/pendingAssignment/pendingK/
     pendingN := NULL`), `prodCount :=
     prodCount + 1`, `lastProdAt := now`, `deniedStreak := 0`. Return
     `{:prodded, k}` or `{:escalated, rung, target}`. A crash between
     dispatch and clear leaves the entry pending: the next drain
     re-dispatches — the accepted duplicate-wake window.
     `{:error, %{code: code}}` where code is a STATUTE-TIER denial
     ("rule_denied" | "rule_error") → the DENIED CLEAR — like the
     successful clear, ONE transaction spanning both tables (never
     split; a crash between the writes must not lose or double-count
     `deniedStreak`): `pending* := NULL`,
     `deniedStreak := deniedStreak + 1`, `prodCount`/`lastProdAt`
     untouched — a denied attempt is not a delivered prod and never
     advances the ladder — plus one
     `EventLog.lifecycle(db, "supervision_prod_denied", a.id, detail)`
     row, and when `deniedStreak` reaches `max(n, 1)` also one
     `EventLog.lifecycle(db, "supervision_blocked", a.id, detail)`
     row (observability: the operator's own deny rule is respected —
     deny-only — but never silently). The statute-denial event row
     itself is on Dispatch's best-effort terms (dispatch.ex).
     ANY OTHER error code (e.g. "server_error" from a transient
     handler fault) is NOT a denial: leave the entry PENDING (no
     clear, no deniedStreak, no prod bookkeeping), emit one
     best-effort `supervision_dispatch_failed` lifecycle row, and let
     the next drain retry — a transient fault must never forfeit a
     claimed delivery nor masquerade as policy. Return
     `{:refused, code}`. (This retry-on-future-edges sentence applies
     to CLEARED statute denials only; a transient-error entry stays
     PENDING and is retried by the DRAIN — step 1's short-circuit —
     never by a fresh claim.) For cleared denials, retry happens on
     future stall edges
     (each a fresh claim, `attemptCount` advancing, branch unchanged
     because `prodCount` is frozen — a fully denied assignment retries
     its first branch forever, visibly: PROD 1, or rung 1 when
     `n = 0`; it never advances past it, because advancement is earned
     only by DELIVERED wakes).
   - TERMINUS: no dispatch; append one
     `EventLog.lifecycle(db, "supervision_terminus", assignment_id,
     detail)` row (naming holder and attemptCount), then the clear
     (`pending* := NULL`; counters untouched — no wake row was
     created). Return `:terminus`. A crash between append and clear
     re-appends on the next drain — at-least-once lifecycle rows,
     same accepted window as duplicate wakes.

Delivery mechanics, a subsequent tick behind: a later WakeScheduler
tick fires the row (`nudge: false` skipped the inline nudge),
`deliver_prompt` stamps `[from process:tightbeam]` as the first line
(sender = wake origin), and the enqueued turn is the prod's reply turn.
When that turn ends with still no rows and nothing scheduled, its
terminal is a NEW stall event → next prod, a tick later. No deliberate
spacing — the delivery latency is delivery mechanics, not policy, and
is EVENTUAL, not bounded by `TIGHTBEAM_WAKE_TICK_MS`: `deliver_due` is
a serial pass that may synchronously call `LaneManager.ensure_lane`
(wakes.ex, gateway.ex), and the next tick is scheduled only after that
pass returns, so latency rides the scheduler's own throughput. What
supervision guarantees is that its act phase never BLOCKS on delivery,
not a per-tick SLA; delay would reward empty replies, and none is
added.

RACE WINDOW, ACKNOWLEDGED (TOCTOU): evaluation is asynchronous to the
org. A turn enqueued between the step-3 `pending_count` read and the
step-9 dispatch receives a prod anyway — queued behind the new turn —
and the counters advance even though the agent is actively working. This
over-prod window is accepted and self-healing: progress rows reset the
counters, and the new turn's own terminal re-evaluates on fresh rows. The
serialization guarantee (one evaluator) makes the window at most one
extra prod per race, always visible as rows; the monotone watermark
dedupes re-claims of already-claimed terminals and is no help here —
this is one evaluation of one terminal, just late. Neither mechanism
makes evaluation atomic with the org's writes, and no stronger claim
is made.

## The prod wake (exact template)

Origin `process:tightbeam`. Neutral, fact-stating, carries its own
countdown. With `<id>` = assignment id, `<subject>` = assignment subject,
`<k>` = count, `<N>` = prod_limit:

    Your turn ended with no filing and no continuation scheduled for
    assignment <id> — "<subject>". File completion, schedule your
    continuation, or file surrender. This is prod <k> of <N>; a reply
    without a row escalates to your spawner.

`<k>` counts DELIVERED prods (`prodCount + 1` at claim time) — a
statute-denied attempt consumes no number, so the countdown the agent
reads is always truthful. Both numbers are frozen in the outbox at
the claim (`pendingK`/`pendingN`), and the delivered text renders
from those stored values — never from live counters or live
prod_limit (steps 8–9); the same holds for the escalation template's
`<N>` and `<rung>`. A prod is satisfied only by STATE: a
terminal filing closes the
assignment (step 5 goes `:idle` via close), a scheduled continuation
pauses (step 4), a progress attest resets the counters (step 6). A reply
containing only words changes nothing and its terminal advances the
count. Note the pinned consequence: a turn that files progress but ends
with no continuation and the assignment still open is STILL a stall event
— it draws prod 1 of a fresh countdown. Progress buys the counter back;
only a filing-or-clock-bearing turn ends clean. That is the invariant,
verbatim.

## The ladder (mechanical walk, Main terminus)

`ladder_target(db, holder_key, rung)`:

    holder = Org.get(db, holder_key)          # row always exists: attest pinned a
                                              # live session; rows are never deleted
    chain: walk spawned_by from holder, collecting session_keys of rows
           with state = 'active' only (retired rungs are skipped), with a
           visited-set stop on repeats, the set SEEDED WITH THE HOLDER
           (the walk must be total; a cyclic chain must not hang the
           executor, and the holder never appears in its own chain).
           Pinned consequence: A-spawned-B-spawned-A with A the holder
           yields chain [B] — rung 1 wakes B, rung 2 (and beyond) wakes
           the owner's Main; the self-target guard never fires for a
           lineage cycle, only for the Main-holding-its-own-assignment
           terminus.
    rung <= length(chain) → chain[rung]       # 1-indexed: rung 1 = nearest
                                              # active ancestor, judgment lives there
    rung >  length(chain) → Org.personal_session_key(holder.owner_user_id)

Delivery-time re-resolution (r13 — §Escalation delivery
re-resolution): there is NO separate delivery resolver. The
escalation wake row persists the walk's inputs (`reresolveSeed` =
the holder, `reresolveRung` = the rung), and delivery re-RUNS
`ladder_target(seed, rung)` — the same holder-seeded walk above, on
fresh truth, inside the delivery transaction. `ladder_target` is
therefore a PURE module function on `Tightbeam.Supervision` (row
reads only, no server interaction), callable on the db handle OR an
open transaction handle — the composed deliver closure, running in
the WakeScheduler process, calls it with the delivery transaction's
txn. (The r12 `lineage_target/2` — a walk up from the dead target
seeded only with itself — is DELETED: without the holder in its
visited set, the cycle H→S→H with S retired resolved back to the
holder H instead of skipping to Main; r12-review finding 2.)

The no-void terminus: Mains are permanent by construction (retire refuses
them), so the ladder always resolves. A worker spawned by a user
(`spawned_by` nil) escalates straight to its owner's Main. Successive
DELIVERED escalations walk successive rungs (`rung = prodCount − n + 1`
— each delivered escalation advances `prodCount`, so the next stall
edge carries the next rung; a DENIED escalation freezes the rung and
retries it, visibly, on the next edge) — a spawner that is itself
stalled, retired, or unresponsive is passed mechanically: retired rungs
are skipped at walk time, a rung that retires after its wake was
scheduled is passed at DELIVERY time (the ladder re-run,
§Escalation delivery re-resolution), and an unresponsive spawner is
walked past by the next delivered escalation. Once the chain is
exhausted, every further event targets Main. Wakes to a busy Main are
NOT deduped — each delivery enqueues its own turn and the lane serializes
them; boundedness never depended on coalescing, only on each escalation
wake being claimed against exactly one worker terminal — internal or
external — per the four legs of §Cascade-boundedness.

Escalation wake, origin `process:tightbeam`, exact template:

    Assignment <id> — "<subject>" — held by <holderKey> is stalled:
    <N> prods produced no filing and no continuation. This is
    escalation <rung> for this assignment. Why, and what happens next,
    is your judgment — the substrate only reports the rows.

SELF-TARGET GUARD: if the resolved target equals `holder_key` (a Main
holding its own assignment escalates to itself), the evaluation takes
the TERMINUS branch — no wake is dispatched, ever. The step-8 claim
commits the watermark, `attemptCount`, `stalledAt` if NULL, and a
`terminus` outbox entry; the step-9 act is exactly one lifecycle event
(`EventLog.lifecycle(db, "supervision_terminus", assignment_id, detail)`
naming holder and attemptCount) plus the clear. A duplicate evaluation
dies at step 2, so the terminus never double-counts; a crash between
append and clear re-appends the lifecycle row on the next drain —
at-least-once, the same accepted window as duplicate wakes. The prods
already sitting in that Main's stream are the operator-visible record;
a self-wake would be the substrate prodding its own prod — the
infinite reaction the design forbids.

## Cascade-boundedness (the mechanical argument, on four legs)

HONESTY FIRST (r5): escalation 1 is CAUSED by the terminal of prod N's
reply turn — an internal, substrate-provoked edge, not an external
one. Boundedness never rested on external causation; it rests on these
four legs:

1. Each ACTION is 1:1 with a CLAIMED terminal: the monotone session
   watermark admits at most one claim per (session, terminal), and the
   outbox may re-DELIVER a claim across a crash boundary but never
   re-COUNTS it (the guarded clear) — duplicates are bounded by
   restarts, not by agent behavior.
2. `prodCount` is monotone within a progress epoch: every delivered
   wake advances it exactly once, nothing else advances it, and only a
   progress row (agent action) resets it.
3. Within one epoch the delivered sequence is prods 1..N, then
   ESCALATIONS FOREVER — rungs 1..length(chain) and then Main
   repeatedly (§ladder: past-chain events target Main, and wakes to a
   busy Main are not deduped). Each escalation is 1:1 with a CLAIMED
   HOLDER terminal (leg 1). There is NO fixed per-epoch wake count —
   the bound comes from leg 4.
4. Only PRODS target the holder. Escalations target non-holders
   (spawner ancestors / Main), whose reply turns evaluate against
   the RECIPIENT's own assignments and cannot produce new HOLDER
   terminals. The executor's no-wake TERMINUS branch is ONLY the
   self-target case (the resolved target IS the holder — e.g. a Main
   holding its own assignment); do not confuse it with the ladder's
   Main terminus, which IS a delivered wake. (The word "terminus" is
   used for both in earlier sections; this leg is the disambiguation.)

TERMINATION, GIVEN FINITE EXTERNAL INPUT (r17 — this REPLACES the
r12–r16 episode/frontier/credit machinery ENTIRELY). The reaction
cannot cascade infinitely. Rounds r12–r16 each tried to COUNT internal
wakes with a closed-form figure (`2·Φ_global`, then `2·(Φ(t₀)+|R|)`),
which forced enumerating every in-flight token AND every re-evaluation
entry point — and each review round found one the frontier set missed
(a lost cast, a `LaneManager` reconcile republish, a restart sweep, a
public `request_sweep/1`). r17 drops the count and proves TERMINATION
from two facts already pinned in the mechanism — both PATH-BLIND, so
the entry point is irrelevant:

FACT 1 — ONE CLAIM PER TERMINAL, EVER. The monotone per-session
watermark (`terminal_seq <= lastEvaluatedTerminal` →
:duplicate/:coalesced, no claim) admits AT MOST ONE claim per
(session, terminal_seq), for the life of the org. This holds NO MATTER
HOW that terminal's evaluation is triggered — the finalize/cancel
cast, a `LaneManager.do_reconcile` republish, a restart recovery
sweep, or `request_sweep/1` — because every path routes through the
same `evaluate`, whose step 2 is the watermark dedupe. A terminal that
already claimed is inert on every later re-evaluation through every
path. The one terminal that can still claim after t₀ is a SUPPRESSED
one (:continuation wrote no watermark); but it too claims AT MOST ONCE,
because its first successful claim writes the watermark and every later
re-evaluation of that seq then dedupes. "Suppressed then reclaimed —
by reconcile, sweep, or anything else" is therefore ≤ 1 wake, never
unbounded. (This is why the earlier proofs' failure to enumerate
reconcile-republish was never a livelock: the watermark caps it.)

FACT 2 — EACH INTERNAL WAKE DECREASES A FINITE MEASURE, OR HITS THE
IMMORTAL SINK. Over the currently open assignments:

    slots(a) := (N − prodCount(a))⁺ + (L(a) + 1 − escCount(a))⁺
    Φ := Σ over open assignments a of slots(a)

L(a) is the finite visited-set-guarded lineage length to the IMMORTAL
Main sink (retire denies built-ins, gateway.ex ~1823 — the sink
exists, is live, and never leaves the chain, which is what makes "rungs
to the sink" well-defined). Φ is finite (finitely many open
assignments, each finite N, finite L) and NO INTERNAL event increases
it: retirement only shrinks chains, spawning inserts no ancestors, and
only EXTERNAL agent action opens an assignment or resets a counter (a
progress row — step 6 — or a new `assign`). Call a delivered wake
SLOT-CONSUMING (SC) if it strictly decrements Φ — a prod with
prodCount < N, or an escalation with escCount < L+1, on SOME open
assignment's measure toward ITS OWN Main sink (cross-assignment
re-entry is fine: it still consumes one unit somewhere) — and PAST-SINK
(PS) otherwise (ladder exhausted; targets Main only).

THE CHAIN TERMINATES. Each delivered wake provokes ≤ 1 turn, hence ≤ 1
terminal (`turns.wakeId` UNIQUE, §Self-driving liveness); that terminal
claims ≤ 1 action (Fact 1); that claim creates ≤ 1 wake (the single
guarded clear). Follow any maximal chain of internally-provoked wakes:
- Every SC wake strictly decreases Φ, a non-negative integer no
  internal event refills — so a chain holds AT MOST Φ(now) SC wakes
  before Φ = 0, after which no SC wake is possible.
- A PS wake targets the immortal Main, whose terminal evaluates MAIN's
  OWN assignments; for the assignment being escalated Main is NOT the
  holder, so Main's terminal never claims a further escalation OF THAT
  ASSIGNMENT (and a Main holding its own assignment self-targets to the
  zero-wake TERMINUS, step 7). A PS wake thus provokes no successor FOR
  ITS OWN ASSIGNMENT. LEMMA (the one continuation a PS wake CAN have,
  and why it does not escape the bound): Main's terminal, evaluating
  under §steps, may claim at most one action — and if Main holds ANOTHER
  open assignment b that is now stalled, that claim is an SC wake for b
  (a prod or an on-chain escalation, prodCount(b) < N or escCount(b) <
  L(b)+1), which STRICTLY DECREASES Φ (it spends one of b's own units
  toward b's own Main sink). It is therefore an ordinary Fact-2
  Φ-descent step, already counted in the ≤ Φ SC-wake budget — NOT an
  unbounded PS continuation. So a PS wake's ONLY possible successor is a
  Φ-decreasing SC wake for a different assignment, or nothing; either
  way the maximal chain still spends a finite Φ and cannot recur on a
  zero-Φ (all-past-sink) state. (Cross-assignment re-entry is exactly
  this: legal, and bounded because every such step is SC — it consumes
  Φ — never PS-provokes-PS.)
So every internally-provoked chain is finite — each step is either an SC
wake spending one of the finite Φ units or a PS-wake-to-Main whose only
successor is itself SC (above) or an empty terminal. Φ is a
non-negative integer no internal event refills, so a chain takes
finitely many SC steps and then quiesces. NO infinite internal cascade
exists.

BOUNDED BY EXTERNAL INPUT. New chains start ONLY from EXTERNAL triggers:
an externally-prompted terminal, a progress reset, a new `assign`, an
externally scheduled wake, a restart, or `request_sweep/1`. Each
re-evaluates some finite set of terminals; by Fact 1 each distinct
terminal yields ≤ 1 claim, and by Fact 2 each resulting chain is finite.
Finitely many external triggers → finitely many finite chains → the
reaction emits finitely many wakes and QUIESCES. That is
cascade-boundedness: bounded by external input, never self-sustaining.
The sweep double-emit r16-review raised (a drain PLUS a fresh claim in
one `evaluate`) is bounded the same way: the drained wake is the
RE-DELIVERY of an already-counted claim (Fact 1 counted it when it was
first claimed — re-delivery across a crash never re-counts, leg 1), and
the fresh claim is the ≤ 1-per-terminal of Fact 1; neither escapes the
argument.

The N+1 figure survives ONLY as a per-contiguous-reply-chain
observation (prods 1..N, then the escalation that moves off the holder
— leg 4); it is NOT a per-assignment total and no invariant, template,
or test may state it as one. §Tests asserts TERMINATION, not a count:
given fixed finite external input the reaction quiesces (the N=0
cross-assignment re-entry, the past-sink-open assignment under repeated
external terminals emitting exactly one escalation each, the
suppressed-then-reconcile/sweep-reclaimed terminal emitting exactly one
wake, and the H→S→H lineage cycle resolving to Main — each terminates).

Crash-window duplicates are EXCLUDED from this steady-state bound as
before: a never-cleared outbox entry can re-dispatch a duplicate
wake, bounded by the number of restarts, never by agent behavior
(leg 1). And each individual walk is finite regardless of lineage
cycles — the visited set, SEEDED WITH THE HOLDER, stops on repeats
(§ladder), so `ladder_target` always terminates — at dispatch and at
delivery alike (r13: delivery re-runs the same walk).

## N: operator data

`prod_limit` — app env `config :tightbeam, :prod_limit`, default `3`,
runtime override `TIGHTBEAM_PROD_LIMIT` (mirror the `TIGHTBEAM_WAKE_TICK_MS`
block in config/runtime.exs, `String.to_integer`). Thread it exactly like
`wake_tick_ms`: Application config map (lib/tightbeam/application.ex) →
`Gateway.config()` type → `children/1` → the Supervision server's
`:prod_limit` opt. Validate
in `children/1`: an integer ≥ 0 or raise (law fails closed). `n = 0` is a
legal ruling: no worker prods, first stall escalates. APPROVED
DEVIATION, recorded verbatim per the orchestrator's r4 ruling message
(2026-07-19, the authorization for this narrowing): v1 hardcodes the
ladder SHAPE (spawner-walk → Main terminus); the parent's "policy
knobs are operator data" (supervision-v1.md) is satisfied by N
(`TIGHTBEAM_PROD_LIMIT`); shape-as-data is deferred to a future
revision.

## Public API additions (same module conventions as EventLog.verb_count)

- `Ledger.pending_count(db, session_key) :: non_neg_integer` —
  `COUNT(*) WHERE sessionKey = ? AND status IN ('queued','running')`.
- `Ledger.last_terminal_seq(db, session_key) :: integer | nil` —
  `MAX(seq) WHERE sessionKey = ? AND status IN ('delivered','canceled',
  'failed','failed_unknown')`; the recovery sweep's triggering-terminal
  lookup.
- `Wakes.pending_count(db, session_key) :: non_neg_integer` —
  `COUNT(*) WHERE state = 'pending' AND sessionKey = ?`.
- `Assignments.oldest_open(db, session_key) :: assignment | nil` and
  `Assignments.attest_count(db, assignment_id) :: non_neg_integer` —
  additive to attest's module, built in THIS spec's lane; extensions
  this spec authorizes, mirrored by name in attest r5's public-API
  inventory. Dumb row lookups both. The sweep's candidate enumeration
  uses attest's EXISTING `Assignments.list` (open-state filter,
  distinct holder keys) — no third extension.
- `Tightbeam.Supervision`: `start_link/1` (opts `:db`, `:handlers`,
  `:prod_limit`, `:name`; init returns
  `{:ok, state, {:continue, :recovery_sweep}}`), `notify_terminal/3` —
  precisely
  `notify_terminal(server \\ Tightbeam.Supervision, session_key,
  terminal_seq)`, a cast, the only way terminal sites reach it; the
  composition closure calls it with two arguments, taking the default
  server — `notify_retired/2` — precisely
  `notify_retired(server \\ Tightbeam.Supervision, session_key)`, a
  cast, the RETIREMENT DOORBELL (r11: optional, best-effort — §The
  seam): the gateway retire-site closure calls it with one argument
  (default server); its handler emits the best-effort
  `supervision_stranded` doorbell for each of the retired session's
  open assignments (strandedAt-deduped upsert, §step 7's doorbell
  write; no wake, no claim, no watermark write, no correctness role —
  stranded-ness is derived at query time), under the
  total catch — `request_sweep/1` (a cast running the identical sweep; the
  test/forensics hook — LaneManager no longer triggers it and has no
  `:supervision` opt), `evaluate/5` (the synchronous core, called by
  the cast/continue handlers and directly by unit tests),
  `ladder_target/3` (r13 — the ONE resolver, public and PURE, §ladder:
  `ladder_target(db_or_txn, holder_key, rung)`, a module function
  with no server interaction, row reads only; called by the act/drain
  on the db handle and by the composed deliver closure on the
  delivery transaction's txn handle; no start-order constraint, since
  it is never a GenServer call — the r12 `lineage_target/2` is
  DELETED), `ensure_schema/1` (creates BOTH
  tables),
  `prod_state(db, assignment_id) :: map | nil` and
  `watermark(db, session_key) :: map | nil` — the full row, watermark
  plus outbox columns — (row readers; tests and forensics). No other
  surface.

No new verbs — FOUR additive optional params on the existing `wake`
verb: `nudge` (default `true` = today's inline `fire_due` nudge;
`false` = the row is due now and WakeScheduler's next tick delivers
it; supervision always passes `false`), and the `reresolve` triple
(r12, reshaped by r13): `reresolve` (default nil = today's behavior
exactly; `"lineage"` = if the DIRECT target is not `active` at fire
time, delivery re-resolves by re-running the holder-seeded ladder
walk `ladder_target(reresolve_seed, reresolve_rung)` inside the
delivery transaction, sinking at the owner's Main — §Escalation
delivery re-resolution), `reresolve_seed` (the walk's holder-seed
session key), and `reresolve_rung` (the 1-indexed rung). Validation:
`reresolve: "lineage"` REQUIRES both companions (else `invalid`);
either companion without `reresolve` is `invalid`; all nil is
today's wake, byte-for-byte. Supervision passes the triple on
ESCALATION dispatches only, never on prods. The triple persists as
three additive nullable `wakes` columns —
`reresolve TEXT NULL CHECK (reresolve IN ('lineage'))`,
`reresolveSeed TEXT NULL`, `reresolveRung INTEGER NULL` — migrated
by the same ALTER-TABLE-ADD-COLUMN idiom as `targetRole` (wakes.ex
~63); it is a generic late-binding delivery mode over org-owned
lineage truth — the role-wake fire-time resolution precedent — not a
supervision-specific branch in the wake pipeline.
`Gateway.deliver_prompt` gains TWO additive optional opts. (1)
`:target_gate` (r13, §Atomic wake delivery — the wake row; nil
default preserves today's behavior for every existing caller): with
the gate present the enqueue transaction first reads the target's
state in-txn and applies the active / re-resolve / skip branch
atomically with the enqueue. (2) `:fire_wake_in_txn` (r19,
§Atomic wake delivery — boolean, default false preserves today's
deliver-then-mark for every existing caller and every non-supervision
wake): when true, the enqueue transaction ALSO marks `opts[:wake_id]`
`pending → fired` (the same CAS `deliver_due` uses) atomically with
the append+enqueue, so the wake is committed 'fired' before the
post-commit lane nudge. The wake deliver closure (`children/1`) sets
`:fire_wake_in_txn` true ONLY for direct wakes whose origin is the
substrate's supervision process origin (`process:tightbeam`) — the
composition layer owns that supervision/non-supervision decision;
`deliver_prompt` stays generic. No new event kinds — prods and
escalations are ordinary `wake` verb rows (origin `process:tightbeam`)
appended by Dispatch; the SIX lifecycle names this spec introduces
(`supervision_evaluate_failed`, `supervision_prod_denied`,
`supervision_blocked`, `supervision_terminus`,
`supervision_dispatch_failed`, and `supervision_stranded` — the last
an OPTIONAL best-effort doorbell only, r11) ride the
EXISTING lifecycle event mechanics; the `assignment_prods` and
`supervision_watermarks` tables are the domain record; do not
double-log.

## Guidance line + dispatching skill (design item 4)

Append ONE bullet to `@builtin_comms` (lib/tightbeam/archetypes.ex),
exactly:

    - NEVER end a turn with outstanding work and nothing on the clock:
      while you hold an open assignment, end every turn with a filing
      (`tightbeam attest <id> --kind progress|completion|surrender`) or a
      scheduled continuation wake to yourself. A turn that ends with
      neither draws a prod; prods answered without rows escalate to your
      spawner.

Add ONE built-in skill to `@builtin_skills`, name `tightbeam-dispatching`
(operator edits win / delete-restores, like the existing three), content:

    ---
    name: tightbeam-dispatching
    description: Assignment and attest hygiene when dispatching work to another session or holding an assignment yourself. Use when hiring, delegating, or working under an open assignment.
    ---

    Dispatching work: spawn (or pick) the worker, then open the
    obligation as a row — `tightbeam assign --subject "..."
    (--session K | --role R)` — and wake the worker with the brief.
    Done is rows, not prose: the assignment closes only by the holder's
    completion or surrender attest, or the operator's revoke.

    Holding an assignment: every turn you end must leave a filing
    (`tightbeam attest <id> --kind progress|completion|surrender
    [--note "..."]`) or a continuation wake on the clock. Progress rows
    reset the prod countdown; scheduled wakes pause it; words do
    neither. If you stall, prods arrive from process:tightbeam and
    escalate up your spawner chain after N misses.

    Supervising: an escalation wake means your hire's assignment
    stalled — N prods, no rows. Judgment is yours: read their stream,
    wake them, re-staff, or ask the operator to revoke the assignment.
    The substrate will not conclude why and will not act for you.

## What the substrate never does (invariants, acceptance lens)

1. NO WHY-INFERENCE: no "gave up" state exists anywhere; `stalledAt` is
   the timestamp escalation began, not a judgment. The executor reads
   row existence and counts only.
2. NO PUNITIVE ACTION: the only substrate acts are wakes and the stamp.
   No retire, no cancel, no re-staff, no closing of assignments — ever.
   Re-staffing is a supervisor's verb, by judgment, in an agent.
3. NO CONTENT READING: reply text, attest notes, and prompts are never
   inspected. Rows or nothing.
4. NO STANDING REMINDERS: prods are discrete addressed correspondence
   through the wake verb — the comms-clock pillar — never context
   injection; rails-never-add-guidance is untouched.
5. Every prod, escalation, and stamp is rows: wake rows + verb event
   rows + `assignment_prods`/`supervision_watermarks` columns; refusals
   are denied event rows on Dispatch's best-effort terms (an
   unavailable audit sink cannot fail the call open — dispatch.ex)
   PLUS a `supervision_prod_denied` lifecycle row per denied attempt
   and a `supervision_blocked` row when a denial streak reaches the
   threshold; an evaluation that escapes the total catch leaves a
   `supervision_evaluate_failed` lifecycle row. "Nothing happens
   silently" is the LIVE/DEAD split (r11): a LIVE holder is PRODDED —
   its claimed action lives in the outbox until delivered to it, and
   each delivered wake provokes the turn whose terminal is the next
   edge (self-driving, §Self-driving liveness) — and that terminal
   actually CLAIMS the next edge because supervision's own delivered
   wake is marked 'fired' atomically with the enqueue (r19,
   §Atomic wake delivery), never left 'pending' to self-suppress the
   provoked terminal into a false `:continuation` (the deliver-then-mark
   race the r18 build stopped on); a DEAD holder's open
   assignments are DERIVED-STRANDED — a view-state any observer
   computes at query time (open ∧ holder retired), true and findable
   with zero rows written. A pending entry whose PROD target (the
   holder) has retired is cleared without dispatch at the next drain.
   An ESCALATION never pins a target: the drain resolves its rung to
   a live session and dispatches (§step 1), and a scheduled
   escalation wake whose recipient retires before the tick is
   re-resolved AT DELIVERY by re-running the holder-seeded ladder
   walk — inside the delivery transaction, atomically with the
   enqueue, so no retirement can slip between check and act (r13,
   §Atomic wake delivery) — landing on the nearest surviving rung or
   the immortal Main (§Escalation delivery re-resolution): a LIVE
   holder's ladder can never be silenced by a dead supervisor. And the recovery sweep both
   drains pending entries and re-runs the stall predicate over every
   open-assignment holder at every start. The `supervision_stranded`
   doorbell and `notify_retired` are best-effort promptness only —
   losing every one of them silences nothing, because the derived view
   never depends on them.
6. Cascade-bounded per §Cascade-boundedness; the self-target guard and
   the delivered counter are the mechanical enforcement.
7. Zero NEW claims for sessions holding no open assignments —
   DRAIN-FIRST, THEN IDLE, THEN DEDUPE (r11 order, fixing r10-review
   finding 4): `evaluate` runs the unconditional step-1 outbox drain
   FIRST (a stale pending entry, e.g. one whose assignment has since
   closed, is cleared WITHOUT dispatch — a legitimate write, not a
   claim), then the step-2a idle determination — no open assignments →
   `:idle`, with no claim, no wake, no counter movement, no watermark
   advance — and only for sessions that DO hold an open assignment
   does the watermark dedupe run: the watermark can never swallow the
   idle determination, so a drained stale closed-assignment entry
   followed by no-open-assignments returns `:idle`, not `:duplicate`.
   A session that never had a pending
   entry writes nothing at all. This is not a contradiction of the
   mandatory drain: the invariant forbids new CLAIMS on idle sessions,
   not the drain of a promise made earlier. And zero behavior change
   for every existing verb — the `wake` verb's new `nudge` param and
   `reresolve` triple all default to today's behavior, and
   `deliver_prompt`'s `:target_gate` opt defaults nil for every
   existing caller; a database from before this build boots
   unchanged.
8. EXACTLY-ONCE COUNTING, LIVE-TARGET DELIVERY, by serialization +
   the monotone session watermark + the outbox: every evaluation runs
   alone in the one Supervision server; at most one CLAIM per
   (session, terminal) — same-seq duplicate casts (`:duplicate`),
   out-of-order older-terminal republishes (`:coalesced`, the accepted
   per-session coalescing), revoked-target `oldest_open` shifts, and
   sweep re-walks all die at step 2b, on every branch. Each claim is
   counted exactly once (`attemptCount` at the claim, `prodCount` at
   the single guarded clear) and its wake is DELIVERED TO A LIVE
   TARGET: the pending outbox entry survives any crash and is
   re-dispatched by the next drain until delivered or converted — a
   claim can never be silently lost — and the only over-delivery is a
   duplicate wake across a crash between dispatch and clear, accepted
   and bounded by restarts. Delivery is NEVER promised to a dead
   HOLDER: its obligation is surfaced as derived-stranded, never
   delivered. A claimed ESCALATION, by contrast, IS always delivered
   to a live session: its target is resolved at dispatch (§steps 1
   and 9) and re-resolved at delivery — the same holder-seeded walk,
   re-run atomically with the enqueue (r13, §Atomic wake delivery;
   §Escalation delivery re-resolution) — sinking at the immortal
   Main. And every supervision wake — prod or escalation — is marked
   'fired' atomically with the enqueue that provokes its turn (r19,
   `:fire_wake_in_txn`, §Atomic wake delivery), so the provoked
   terminal never observes it 'pending' and the self-driving chain is
   never silenced by a delivered wake suppressing its own reply
   (the deliver-then-mark race the r18 build stopped on). Queued-work
   suppression (steps 3–4) still fires when it applies, but the
   invariant does not rest on it — escalations and termini leave the
   holder idle.

## Tests (condensed contract — cover every clause)

r19 additions (the deliver-then-mark race the r18 build correctly
stopped on, plus the review's four contract-test gaps).

DELIVER-THEN-MARK SELF-SUPPRESSION (the exact race — the load-bearing
r19 test). A live holder H with one open assignment and an empty
terminal draws prod k; the scheduler delivers it. Drive the EXACT
(2)-(3) window: run the provoked turn to its terminal AFTER
`deliver_prompt` commits its enqueue transaction but BEFORE any
post-closure fired-mark could run (e.g. a runner/deliver closure that
terminates the provoked turn synchronously inside the `ensure_lane`
nudge, or a test scheduler that yields the turn to terminal between
`deliver.(wake)` returning and `deliver_due`'s mark). ASSERT the
originating prod wake is already `state = 'fired'` at the moment
supervision evaluates that terminal, and ASSERT the evaluation returns
`{:prodded, k+1}` (or the escalation at the ladder boundary) — the
chain ADVANCES — NOT `:continuation`. SCOPE CONTROL: a non-supervision
EXTERNAL direct wake (origin NOT `process:tightbeam`, no
`:fire_wake_in_txn`) still exhibits today's deliver-then-mark ordering
unchanged (fired only post-closure) — the fix is scoped to supervision.
RESERVED-ORIGIN CONTROL (r20, §Atomic wake delivery RESERVED ORIGIN):
assert an authenticated org-CLI wake dispatched with `asProcess:
"tightbeam"` is REJECTED with `403 reserved_origin` and NO wake row is
persisted — so no externally-created wake row can ever carry origin
`process:tightbeam`, and the `:fire_wake_in_txn` selector cannot gate a
forged external wake; a wake with `asProcess: "ci"` (any non-reserved
name) still attributes normally to `process:ci` and stays ungated.
PLUS a repeated-iteration racer hammering the (2)-(3) window across
many deliveries: assert EVERY provoked terminal reads its own
originating prod as `fired` (never `pending`), the self-driving chain
NEVER stalls on a false `:continuation`, and the fixture quiesces ONLY
at the ladder terminus.

INTERNAL-TERMINATION CASCADE ASSERTS QUIESCENCE (gap (a) — the review's
"true internal-termination-cascade" gap: the r11/r12 tests asserted the
test process stopped receiving casts, not that the substrate reached
rest). The N=0 cross-assignment re-entry, the past-sink-open assignment
under repeated external terminals, the suppressed-then-reclaimed
terminal, and the H→S→H lineage cycle each run to completion with NO
fresh external input and assert ACTUAL QUIESCENCE as the oracle: after
the reaction settles, `Wakes.pending_count(db, s) = 0` and
`Ledger.pending_count(db, s) = 0` for every session `s`, every outbox
is clear (`pendingBranch IS NULL` on every watermark row), and the
finite measure Φ has drained to 0 (or to exactly the residual past-sink
slots no internal event can consume). The N=0 re-entry additionally
asserts the reaction DID re-enter (internally-provoked wake count for
the escalated assignment exceeds N+1) AND still quiesced — termination,
not a count (§Cascade-boundedness). The N=0 RE-ENTRY quiescence run is
the direct assertion that no infinite internal cascade exists on the
adversary's own counterexample.

RECOVERY SEAMS (gap (c)). (i) RESTART GAP: a lane's `finalize` marks the
terminal published and casts while Supervision is DOWN (drop the cast);
on Supervision (re)start the `{:continue, :recovery_sweep}` runs BEFORE
any queued cast and prods the now-stalled holder exactly once — assert
the sweep BOTH drains a pending outbox entry whose assignment closed
while down (clear-without-dispatch, counters untouched) AND re-runs the
stall predicate over open-assignment holders. (ii) DISPATCH-CLEAR CRASH:
the outbox entry survives a crash between dispatch and clear; the next
drain re-dispatches (the accepted duplicate wake) and `prodCount`
advances EXACTLY once. (iii) EXACTLY ONE SWEEP PER START: a Supervision
restart runs exactly one recovery sweep (not zero, not two), verified
by counting sweep passes across a boot and a forced restart.

VERBATIM PROMPT TEMPLATES (gap (d)). Assert the delivered PROD message
equals the §The prod wake template BYTE-FOR-BYTE with `<id>`,
`<subject>`, `<k>`, `<N>` interpolated AND the `[from process:tightbeam]`
first-line stamp the delivery prepends; assert the delivered ESCALATION
message equals the §The ladder escalation template byte-for-byte with
`<id>`, `<subject>`, `<holderKey>`, `<N>`, `<rung>` interpolated AND the
same `[from process:tightbeam]` first-line stamp the delivery prepends
(escalations are direct wakes delivered with `sender: wake.origin`
exactly as prods are — the oracle compares the STAMPED delivered message,
not the bare template); assert
the guidance comms bullet and the `tightbeam-dispatching` skill body
match §Guidance line + dispatching skill verbatim. A replay after a
`prod_limit` change reproduces the STORED `<N>` (the frozen
`pendingN`), never the new limit.

r13 additions (one per r12-review finding). CONCURRENT RETIREMENT
DURING DELIVERY (finding 1) — race `Org.retire` against `deliver_due`
over a pending direct wake: the two deterministic orderings (retire
committed BEFORE the delivery transaction → no-op for a plain/prod
wake, in-transaction re-resolve for a `reresolve` wake; retire
arriving AFTER → the turn exists and the session retires with work
queued — legal), PLUS a repeated-iteration racer (a spawned process
hammering retire while the tick delivers) asserting that EVERY
interleaving lands in that outcome set and NEVER the r12 bug — a
turn row enqueued by a transaction that began after the target's
retire committed, or a wake marked fired with neither a turn nor
(for `reresolve`) a re-resolved turn. H→S→H CYCLE AT DELIVERY
(finding 2) — holder H spawned by S, S spawned by H; H's escalation
resolves rung 1 = S at dispatch; S retires before the tick: delivery
re-runs `ladder_target(reresolveSeed = H, reresolveRung = 1)` and
enqueues at the owner's MAIN — asserted NOT H (the r12
`lineage_target` outcome — walking the dead target's lineage without
the holder seed lands back on H — is the bug; asserting it is a spec
violation). IN-FLIGHT-WAKE BOUND (finding 3, hardened by r14 —
the r13 version asserted termination only, which is exactly how the
false r13 figure survived its review; asserting the VALUE is the
point) — a slot-consuming supervision wake is created (outbox
cleared, `prodCount` advanced) and left PENDING; its source
assignment then closes (its Φ contribution is gone); the wake is
delivered afterward to a non-Main session S holding a past-sink
(zero-slot) assignment; S's empty terminal claims a past-sink
escalation to Main, and Main's terminal follows — assert the whole
reaction TERMINATES with no fresh external input AND assert the
BOUND VALUE: at t₀ (the moment the source assignment closes, no
further external input) the fixture has Φ(t₀) = 0 and |R(t₀)| = 1
(the one pending wake), so internally-provoked delivered wakes
after t₀ must be ≤ 2·(Φ(t₀) + |R(t₀)|) = 2 — assert EXACTLY two
(the root's own delivery and the past-sink escalation to Main) and
not one more (§Cascade-boundedness: the bound is tight here).

r14 addition (r13-review blocker 2 — frontier completeness).
FIRED-WAKE FRONTIER TOKEN — a slot-consuming supervision wake is
created AND delivered (marked fired, its turn enqueued) but the
turn has NOT yet run at t₀; the source assignment closes and the
recipient S's own assignment is past-sink (Φ(t₀) = 0); the queued
turn then runs and its empty terminal claims a past-sink escalation
to Main, Main's terminal follows — the fired-but-unterminated turn
is neither a pending wake nor an external terminal, yet it is a
frontier token (an in-flight turn, set 2 of R(t₀)) with its own
credit: assert the reaction TERMINATES and the internally-provoked
delivered-wake count after t₀ is ≤ 2·(Φ(t₀) + |R(t₀)|) = 2 with
|R(t₀)| = 1 (here actual = 1 — the past-sink wake; the token's
own-delivery credit went unused, the bound is an upper bound).

r11 additions (Flynn's simplification rulings). DERIVED-STRANDED AS A
QUERY — open an assignment on a holder, retire the holder, emit NO
event and run NO sweep: the join (open assignments × session state,
via `Assignments.list` + `Org.get`) computes the assignment as
stranded — asserted as a QUERY test, with no `supervision_stranded`
row and no `strandedAt` stamp required to exist; then close the
assignment and assert the same query computes nothing. NO test
anywhere asserts reliable stranded-EVENT emission as a correctness
property (the r10 F2/F4 emission tests are REMOVED); doorbell
assertions below are about the doorbell only. SELF-DRIVING CHAIN — a
live holder with an open assignment and an empty terminal: prod 1 is
scheduled; the scheduler tick delivers it; the delivery enqueues a
turn on the holder's lane; that turn's terminal fires `on_terminal`
and (still empty) claims prod 2 — assert the prod→turn→prod chain
advances through the ladder to escalation with NO timer on
supervision's account and NO sweep call between edges. GLOBAL
TERMINATION (r12/r13, replacing the r11 per-assignment-N+1 tests) —
CONTIGUOUS-CHAIN BOUND: with no external input after the first stall
edge, one uninterrupted holder reply-chain delivers at most N+1
wakes (prods 1..N + the escalation that moves off the holder); NO
test asserts N+1 as a per-assignment TOTAL — that r11 wording is
retired. CROSS-ASSIGNMENT RE-ENTRY TERMINATES — the r11-review
counterexample verbatim: n = 0, assignment A held by H escalates to
S; S's reply terminal claims against S's own open assignment B; B's
escalation wakes H; H's fresh terminal claims escalation 2 for A —
assert A's internally-provoked wake count EXCEEDS N+1 AND the whole
reaction still TERMINATES with no fresh external input (every
internally-provoked wake is a link in a chain rooted in the
episode's root set, and each chain's slot-consuming links draw down
the finite Φ(t₀) — §Cascade-boundedness); no
potential-function VALUE is asserted, only termination. DRAIN→IDLE→DEDUPE ORDER
(review finding 4) — a session with NO open assignments and a stale
pending entry on a now-closed assignment, evaluated with its
ALREADY-CLAIMED terminal seq: `evaluate` clears the entry (a write)
and returns `:idle`, NOT `:duplicate` — the watermark must not
swallow the idle determination; a session with no opens and no
pending entry writes NOTHING; a session WITH an open assignment and
an already-claimed seq still returns `:duplicate` (dedupe intact
where it belongs). LIVE-TARGET DELIVERY CONTRACT (review finding 3) —
a wake WITHOUT `reresolve` to a retired target is a gateway no-op
marked fired
(today's observable behavior, decided in-transaction as of r13 —
§Atomic wake delivery — asserted as the boundary; a
`reresolve: "lineage"` wake re-resolves instead — the r12
POST-DISPATCH RE-RESOLUTION tests below): supervision never
counts it delivered on behalf of a dead holder — a pending PROD
entry whose target retired is cleared WITHOUT dispatch at the next
drain, and the obligation surfaces via the derived-stranded query,
not via delivery. RETIREMENT DOORBELL (optional path, best-effort
semantics) — `notify_retired(session_key)` on a holder with two open
assignments emits at most one `supervision_stranded` doorbell row per
assignment (strandedAt-deduped, including for a row-less assignment —
the upsert), with no wake, no claim, no watermark write; a repeat
cast and a subsequent sweep emit nothing further; and a DROPPED cast
changes no behavior — the derived-stranded query still computes both
assignments stranded (the query test above is the oracle, not the
doorbell).

Carried forward from r10 (rewritten to r12 semantics): RETIRED-RUNG
RESOLUTION (the r10 F1 split, upgraded by r12) — a pending
ESCALATION whose intended rung target (a supervisor) retires while
the HOLDER stays LIVE: the drain RESOLVES the rung fresh and
DISPATCHES to the next active ancestor (or the owner's Main) —
delivered, `prodCount` advanced once, entry cleared, NO doorbell and
NO `strandedAt` on the holder's assignment, NOT stuck (the r11
clear-and-wait outcome is exactly the r11-review finding-1 bug;
asserting it is now a spec violation); contrast: a pending PROD
whose target retired (target IS the holder) clears without dispatch
and the holder's assignment is derived-stranded (doorbell optional).
POST-DISPATCH RE-RESOLUTION (r12, re-pinned by r13) — an escalation
wake row scheduled with the `reresolve` triple (`reresolve:
"lineage"`, `reresolveSeed` = the holder, `reresolveRung` = the
rung) to target S; S retires BEFORE the tick: the tick's delivery
re-runs `ladder_target(seed, rung)` INSIDE the delivery transaction
and enqueues the SAME wake_id at S's next surviving rung — and, with
the whole chain retired, at the owner's Main — a turn is enqueued
THERE, the wake is marked fired, and the ladder was never silenced;
assert the recipient equals what dispatch-time `ladder_target` would
resolve with S retired (coherence is now definitional — same
function, same inputs, fresher truth; §ladder). A PROD wake to a
since-retired holder carries NO `reresolve` and still no-ops
marked-fired — the no-op decided inside the delivery transaction
(r13, §Atomic wake delivery) — the derived-stranded boundary
unchanged. The `wake` verb with `reresolve` absent/nil behaves
exactly as today (regression); `reresolve: "lineage"` without BOTH
companions — and either companion without `reresolve` — is rejected
`invalid`; the three `wakes.reresolve*` columns are added additively
(a pre-r13 database boots unchanged). F5 (see the OUTBOX/TOTAL-CATCH clauses below): a RAISING
wake handler → `supervision_dispatch_failed`, entry PENDING; an
EXITING/THROWING handler → `supervision_evaluate_failed` via the
total catch. F6 SELF-TARGET SCOPING — a PROD whose target is the
holder dispatches normally and is NEVER a terminus (assert a prod
fires with N ≥ 1 and `prodCount < n`); the no-wake terminus arises
ONLY from an ESCALATION resolving back to the holder. F8 DELIVERY —
assert the wake is delivered on a SUBSEQUENT scheduler tick and that
the evaluation makes NO `fire_due` call and does NOT block on
delivery; make NO assertion that latency is ≤ `TIGHTBEAM_WAKE_TICK_MS`
(the guarantee is eventual delivery to a live target, not a per-tick
SLA).

r9 additions (adjusted): SCHEMA — `ensure_schema` creates
`assignment_prods.strandedAt` and `supervision_watermarks.pendingK`/
`pendingN`, surfaced by the `prod_state`/`watermark` row readers —
and NO `pendingTarget` column (r12); the
successful clear NULLs all four pending columns. REPLAY — claim,
change prod_limit, restart: the drained wake's text carries BOTH
stored numbers — the original k/rung AND the OLD `<N>` — and the new
limit appears nowhere in the text. RETIRED-TARGET DRAIN — a
pending PROD whose target has retired: the drain clears without
dispatch, no wake row, no `supervision_dispatch_failed` (no dispatch
was attempted); a pending ESCALATION for a since-retired holder: the
drain resolves its rung and DISPATCHES — the live supervisor is
woken about the dead worker.

r7 additions (adjusted): transient-error drain leaves the entry
pending, emits
supervision_dispatch_failed, SHORT-CIRCUITS the new terminal (no
overwrite of the occupied slot), and the next drain retries;
closed-assignment drain clears WITHOUT dispatch, counters untouched;
retired-holder handling UNIFORM in both paths: terminal-driven
evaluation AND sweep each return `:stranded` with NO wake, NO claim,
NO watermark write and NO counter movement (the doorbell, where
emitted, is best-effort and strandedAt-deduped); the DENIED CLEAR is
atomic (crash-injection between
tables impossible by construction — asserted via the single
transaction seam).

Predicate: each conjunct independently suppresses (queued turn; running
turn; pending direct wake; pending role wake pinned to the session; zero
open assignments); all four terminal states trigger evaluation
(delivered, failed, canceled via cancel_current, failed_unknown via
recover_running + reconcile). Executor: prod 1..N exact text (k =
prodCount + 1, N, id, subject interpolated; `[from process:tightbeam]`
stamp on the message delivered by the NEXT TICK — the dispatch passes
`nudge: false`, the wake row exists with dueAt = now, and NO
`fire_due` call is made from the evaluation); OUTBOX — the claim
transaction commits watermark + `attemptCount` + the pending entry
BEFORE any dispatch, pinned with a wake handler that RAISES after
recording its invocation: claim and pending entry present and the
entry stays PENDING (not cleared), no wake row, one
`supervision_dispatch_failed` lifecycle row — NOT
`supervision_evaluate_failed` (F5): a handler raise is caught by
Dispatch and surfaced as `{:error, code: "server_error"}` (dispatch.ex),
which step 9 classifies as a TRANSIENT fault, leaving the entry pending
— server alive; then with the handler RESTORED to a working one the
NEXT evaluation (and, separately, `request_sweep`) DRAINS it —
wake dispatched, `prodCount` advanced exactly once, pending cleared,
`attemptCount` unchanged by the drain; a pending entry whose dispatch
succeeded but whose clear was lost (simulate) re-dispatches → a
second wake row exists and `prodCount` still advances once — the
documented accepted duplicate window; TOTAL CATCH — one handler that
EXITS and one that THROWS (which ESCAPE Dispatch's raise-only rescue
and are caught by supervision's OWN total catch — the path distinct
from a handler raise above), Supervision survives both with one
`supervision_evaluate_failed` lifecycle row each; statute denying `wake` for the process origin →
`{:refused, code}` with the DENIED CLEAR: `attemptCount` advanced,
watermark set, `prodCount`/`lastProdAt` untouched, `deniedStreak`
incremented, no wake row, one `supervision_prod_denied` row (denied
event row present with a working sink — one integration test wiring a
real rule); `max(n, 1)` consecutive denials → exactly one
`supervision_blocked` row; a delivered wake resets `deniedStreak`; a
fully denied assignment retries PROD 1 on every edge and NEVER
escalates; re-delivery of the same terminal → `:duplicate`.
Counter: consecutive empty terminals increment; progress
attest between prods resets `attemptCount`/`prodCount`/`deniedStreak`
to 0 and clears `stalledAt`; scheduled wake
pauses without reset and the counter resumes after it fires; a
progress-filing turn with no continuation still draws prod 1; completion/
surrender close → `:idle`. Oldest-open targeting with two assignments.
Ladder: the claim after N DELIVERED prods (prodCount = N) wakes the
spawner with exact escalation text and sets
`stalledAt` once; retired spawner skipped; rung walk across a 2-deep
chain; chain exhausted → owner's Main; spawned_by nil → Main; lineage
cycle DETERMINISTIC (A-spawned-B-spawned-A, A holds: escalation 1 wakes
B, escalation 2 wakes the owner's Main, no self-target terminus row ever
— the seeded visited set pins this sequence); self-target (Main holding
its own assignment) → no wake, `supervision_terminus` lifecycle row,
stamp set. Config: default 3; env override; `n = 0` escalates on first
stall; negative → boot raises. Serialization + dedupe (the counting
contract): double-cast of ONE terminal (same seq) → one claim, one
action total — one wake row, one counter advance, one event row —
asserted separately for the PROD branch, the ESCALATION branch
(prodCount already at N: holder idle, ladder woken once, never again
at rung+1), and the TERMINUS branch (one `supervision_terminus`
lifecycle row, one attemptCount advance); COALESCING — the reviewer's
exact ordering: T1's cast lost while Supervision is down, restart, T2
arrives and is claimed+acted FIRST, reconcile republishes T1 →
`:coalesced`, watermark unmoved, no action, and the episode was not
silent (T2's claim acted or its outbox entry drains) — one prod per
stall episode, the accepted per-session coalescing; the A1-REVOKED
interleaving — terminal T claimed (prod on A1), operator revokes A1,
T re-delivered → `:duplicate` even though `oldest_open` now selects
A2 (session-scoped dedupe; A2's countdown never starts on A1's
event); direct double `evaluate` with the same seq → second returns
`:duplicate` with zero writes; two DIFFERENT seqs in order → both act
(distinct stall edges). Sweep
(predicate-now semantics + drain): a published terminal whose cast was
never delivered (simulate the restart gap: write the rows, send no
cast) → `request_sweep` acts exactly once; a pending outbox entry on a
session with `last_terminal_seq` nil → the sweep still drains it; an
already-claimed, already-cleared terminal → `:duplicate`, zero new
rows; a terminal once suppressed by a pending
continuation whose wake was then canceled, no new turns → the sweep
PRODS (the session is stalled NOW — correct, not a defect); a last
terminal predating the assignment's opening → the sweep PRODS the
idle holder; a session holding an open assignment, no pending entry,
and no terminal turn ever → skipped. API:
pending_count (ledger, wakes), last_terminal_seq (mixed terminal and
pending fixtures, nil on none), oldest_open, attest_count over mixed
fixtures; the `watermark` and `prod_state` readers over claimed,
pending, and unclaimed fixtures. Composition: a cast fired from a real
LaneManager reconcile completes end-to-end with NO call into
WakeScheduler from the evaluation (the wake rides the next tick);
child order — Supervision is up before LaneManager's
init reconcile runs (a cast during boot recovery is not dropped);
init's `{:continue, :recovery_sweep}` runs before queued casts, and a
Supervision restart runs exactly one sweep; the `wake` verb with
`nudge: true`/absent behaves exactly as today (regression).
Guidance: comms fragment contains
the bullet; `tightbeam-dispatching` materializes into a projected home.
INTEGRATION (the design's full example timeline, one test): worker W
spawned by supervisor S, assignment opened on W → empty terminal → prod 1
→ empty reply → prod 2 → W schedules continuation → no prod (counter
holds at 2) → wake fires, empty terminal → prod 3 of 3 → empty reply →
escalation 1 to S + stalled stamp → another externally-prompted empty
terminal → escalation 2 → owner's Main → W files progress → next terminal
draws prod 1 of a fresh countdown → W attests completion → assignment
closed, further terminals `:idle` — every wake tick-delivered. Assert
every wake row, both counters, the watermark row (outbox cleared after
each act), stamp, and event row along the way.

## Handoff

Gates: `mix compile --warnings-as-errors` clean; full `mix test` green
(cli/ untouched — no cargo gate). Commit on the branch; do not merge.
STOP and report on any conflict with existing code, with attest as
merged, or with this spec.
