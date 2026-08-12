# wake-on-fact — condition wakes (v1)

> **AMENDED 2026-08-12:** this spec's citations of `model-ringdown-pattern.md`
> (the parked-state exit, W7 park precedent) refer to machinery deleted
> 2026-08-05. The condition-wake primitive itself is unaffected; read those
> citations as history. See `adjudication-deletion-amendment.md`.

Status: DRAFT r6. Hardened through six adversarial review rounds (r1 blockers
1–13 + F7 `creatorSessionKey` addendum; r2 F1–F8 mechanical seams; r3–r6 the
SQL-reality firing/watermark model — valid-SQLite fact-ordered candidate query,
forced index plans, pure-Elixir watermark advance); companions rails-mechanism-v1
r9+ and escalation-substrate-v1 r5+. Makes roadmap phase
**S1** (`rails-and-guidance-roadmap.md`
§S1) implementable. Authority: this spec is the sole authority for the condition
form of a wake — the durable "deliver this prompt when a fact matching P is
filed" primitive — its matchable fact stream, its delivery/consumption/
cancellation semantics, the first substrate-observed condition (`quota-recovered`),
and its supervision interaction. Parents govern where this spec is silent:
`wakes.ex`'s moduledoc (timed-wake delivery + the `turns.wakeId` dedup this spec
reuses as its crash backstop; NOTE condition/fallback fires use the CAS-gated
transaction of W6, which supersedes deliver-then-mark for them),
`model-ringdown-pattern.md` r3 (the parked-state exit this
primitive serves, the classification seam and GAPs it depends on),
`rails-mechanism-v1.md` r-current (§I6/§D2, the turn-end step and its
`self_pending_count` no-false-positive rule), and `p3-observables-producers-v1.md`
r1 (the literal-fact doctrine every matchable field obeys).

Ground truth read on `main`: `lib/tightbeam/wakes.ex` (the wake table, DDL,
`schedule/2`, `cancel/3`, `pending_count/2`, the tick and `deliver_due`,
deliver-then-mark), `lib/tightbeam/event_log.ex` (the `events`/`lifecycle_events`/
`boot_epochs` tables and their CHECKs), `lib/tightbeam/assignments.ex` (attests,
verdict kinds), `lib/tightbeam/supervision.ex` (`evaluate_terminal`'s
`Wakes.pending_count` continuation branch at :185/:206, `ladder_target/3`),
`lib/tightbeam/gateway.ex` (the `wake` handler at :308, `wake_result/3` at :1509,
`deliver_prompt/4` at :494, the `deliver` fn at :224, `fire_due` nudge at :1544),
`lib/tightbeam/wire/router.ex` (`@agent_verbs` allowlist at :46).

---

## 0. The primitive in one paragraph (read first)

A wake becomes due on a **condition** as well as a time. The condition form of a
wake carries a **literal fact pattern** and a **mandatory timed fallback**: it
delivers its prompt to its target when the FIRST of two things happens — a fact
matching the pattern is filed, or the fallback deadline arrives — and is then
consumed. This is one wake row, `pending → fired | canceled`, delivered through the
same turn pipeline a timed wake uses, but fired by **one CAS-gated transaction in
the scheduler** (W6) so the row-state transition arbiters and gates the enqueue
(no cancel-vs-fire race). One unifying substrate capability serves four
consumers that today have no shared mechanism: a **parked quality-floor block**
waiting for token recovery (`model-ringdown-pattern.md`), a **gate awaiting a
producer/verdict fact**, a **remedy awaiting its producer**, and an
**external-event smart wake**. The **hard invariant** governs all four: *delivery
is not resumption.* The substrate never auto-resumes parked work, never
re-decides, never replays the failed turn — it delivers a prompt and the woken
agent **re-adjudicates from the facts** (inference at every edge, per
`model-ringdown-pattern.md`). Permanent block remains a supported policy **by
construction**: it is simply not subscribing (file the block fact + escalate,
no condition wake).

---

## 1. Invariants (the acceptance lens)

**W0 — AGENCY-PRESERVING SUPERVISION.** A condition wake is supervision, not a
workflow transition. A matching fact or timed fallback may make its target
agent eligible to reconsider and delivers the caller's prompt; it never picks
the target's next workflow action, automatically re-engages a reviewer or
producer, spawns a successor, replays a failed turn, or silently changes an
assignment's meaning. The accountable agent re-adjudicates from durable facts
and its current instructions. This is the wake-specific form of the product
tenet: **prompt, don't prescribe**.

**W1 — DELIVERY IS NOT RESUMPTION.** A condition wake, when it fires, does
exactly one thing: it delivers a prompt into the target's turn pipeline via the
same `deliver_prompt` path a timed wake and a user post use. It does not restore
prior state, un-fail a failed turn, re-run a denied verb, or re-decide anything.
The woken agent re-derives from the durable facts (work-item, attests, catalog,
availability) and adjudicates afresh — the same inference-at-every-edge contract
`model-ringdown-pattern.md` holds for the mid-session owner wake. The substrate
carries no "what to resume" state on the wake beyond the caller's own prompt.

**W2 — ONE CANONICAL MATCHABLE STREAM.** Subscriptions match against exactly one
append-only stream: the new `condition_facts` table (§3). Nothing else is
matchable — not `attests`, not `events`, not `lifecycle_events`. Both
substrate-observed condition facts (e.g. `quota-recovered`) and org/script
condition facts land through one append path into this one table.

**W3 — LITERAL PATTERN ONLY.** A subscription pattern is `{kind, scope}` where
`kind` is a required exact string and `scope` is an optional exact string (nil =
wildcard). There are no predicates, no ranges, no regex, no fact-to-fact
comparison — consistent with the engine's literal-only doctrine
(`p3-observables-producers-v1.md` §0). A fact matches iff `fact.kind ==
pattern.kind` **and** (`pattern.scope` is nil **or** `fact.scope ==
pattern.scope`).

**W4 — ONE-SHOT, CONSUMED ON DELIVERY.** A condition wake fires at most once.
The first trigger (matching fact **or** fallback deadline) delivers and
transitions the row `pending → fired`; it never fires again. There are no
standing subscriptions and no replay: a subscription matches only facts filed
**strictly after** it was created (an id cursor, §4.3). To keep waiting after a
re-adjudication, the woken agent files a **new** condition wake.

**W5 — MANDATORY TIMED FALLBACK (a v1 LIMITATION, honestly named, not a virtue).**
Every condition wake carries a finite `dueAt` fallback. This is **not** a claim
that fallback belongs in the substrate — fallback *policy* (whether to fall back,
and when) is a **product concern**, and a mature primitive would let the product
choose an indefinite subscription. v1 mandates a finite fallback **because
`wakes.dueAt` is `NOT NULL` today** (`wakes.ex:47-55`) and this spec deliberately
does not migrate that column. So the mandatory fallback is a **storage-imposed v1
limitation**, disclosed as such. It happens to align with kungfu policy — the
`model-ringdown-pattern.md` parked-state rule independently mandates a **recorded
re-check** for every parked block anyway — so v1 loses nothing real for the
parked-block use case; but the alignment is a coincidence, not the substrate
deciding fallback policy. **Named future migration:** if indefinite one-shot
subscriptions are ever wanted, make `dueAt` nullable (a nil `dueAt` = no fallback)
— a purely additive change behind this same primitive. Until then, "no silent
forever-wait" is a *consequence* of the limitation, not its justification.

**W6 — FIRING IS ONE CAS-GATED TRANSACTION IN THE SCHEDULER; EXACTLY-ONCE ENQUEUE;
":skipped" IS FIRED-WITH-ZERO-ENQUEUE, STATED HONESTLY.** All firing runs in the
`WakeScheduler` GenServer (**one owner**, W-arbitration). A fire is ONE DB
transaction: `UPDATE wakes SET state='fired', firedAt=?, firedBy=? WHERE wakeId=?
AND state='pending'`; **iff `Txn.changes == 1`** the same transaction delivers via
the **new transaction-aware seam `Gateway.deliver_prompt_in_txn/…`** (F1: target
resolution via the now-shared `delivery_target/3`, projection append, and
`Ledger.enqueue_in_txn`, all through the passed `txn`) and writes the one lifecycle
row (via the in-transaction writer, §6), then commits; if `changes == 0` it aborts
with **no enqueue** (the row was already `canceled` or `fired` — the loser of a
cancel-vs-fire or fire-vs-fire race provably no-ops). The wake-row CAS is THE
arbiter and **gates** the enqueue. **The non-transactional tail — publish +
lane-nudge — is owned by the scheduler's firing pass, after commit** (today's
`deliver_prompt/4` at `gateway.ex:494` opens its OWN `DB.transaction` at :510 and
its resolver `delivery_target/3` at :595 is private; F1 requires refactoring that
in-transaction core out so both `deliver_prompt/4` and `deliver_prompt_in_txn`
share it, and calling the current `deliver_prompt/4` from inside the fire txn is
forbidden — it would re-enter the DB owner, `db.ex:49`). This supersedes
"deliver-then-mark" for condition/fallback fires: because "delivery" here is a
transactional DB enqueue (not external I/O), CAS-then-enqueue in one transaction is
atomic and race-safe, with `turns.wakeId` UNIQUE (`ledger.ex:41`) as the crash
backstop (exactly-once enqueue per wake id). The legacy pure-timed-wake paths are
unchanged (process-origin marks fired in-transaction, `gateway.ex:539`;
agent-origin enqueues then the scheduler marks fired, `wakes.ex:254`). **`:skipped`
honesty:** when a fired wake's target is unresolvable (retired session, or a role
that no longer resolves), the CAS still consumes the one-shot row (`pending →
fired`) but enqueues **zero** turns and writes a `wake_unresolved` lifecycle row
**carrying the `firedBy` cause and matched fields** (F4), so the one-row-per-edge
`firedBy` analytics contract is unbroken. "Consumed on delivery" therefore means
*the subscription is spent*, NOT that a turn always resulted — a
fired-with-zero-enqueue outcome is a legal, legible terminal state, not a lost
wake.

**W7 — THE PARKED-SESSION EXIT IS A CONDITION WAKE *TARGETED AT* THE HOLDER; ANY
CREATOR SATISFIES THE BASE GUARANTEE.** `Wakes.pending_count(db, session_key)` is
keyed by the wake's **target `sessionKey`**, not its `origin` or creator
(`wakes.ex:173-182`, `WHERE sessionKey = ?1`); supervision calls it with the
**holder's** key (`supervision.ex:185`). This much is **ground truth**: a condition
wake pauses a parked block's stall countdown **iff its target `sessionKey` is the
holder** — a wake targeting the owner/spawner does not pause the holder (the exact
ringdown r3 failure). **Who created the wake is irrelevant to this base guarantee.**
There are two creation cases, both target the holder, both count for
`:continuation`:
- **Self-creation — the agent-continuation case.** A live agent parks *itself*
  (before its model dies, or a self-check-back) by scheduling a holder-targeted
  wake with `creatorSessionKey = holder`.
- **Owner-creation — the parking case (the ruled ringdown flow).** When the
  holder's model is dead it **cannot run a turn to schedule anything**, so the
  **owner** creates the holder-targeted park wake on its behalf
  (`creatorSessionKey = owner ≠ holder`). This still pauses the holder (target =
  holder) and is the normal parked-block exit.
The **only** thing that distinguishes the two is the *proposed* rail turn-end
step's self-suppression, which is **NOT ground truth**: `Wakes.self_pending_count/2`
does not exist on `main` and supervision has no rail step — both are proposed by
`rails-mechanism-v1.md`. When they land, self-scheduled is decided on the **durable
`creatorSessionKey`** column this spec adds and stamps (F7 addendum, §4.1–§4.2),
NOT the mutable `origin` (role rebinding must not invalidate the proof): a
self-created park counts as self-scheduled, an owner-created park does not (correct
— it is the owner's continuation, not the holder's). The base target-keyed
`pending_count → :continuation` guarantee holds on `main` today with only the
additive wake columns, for either creator.

**W8 — SUBSTRATE-RESERVED KINDS ARE UNFORGEABLE; EVERYTHING ELSE IS OPEN TO ANY
NON-SUBSTRATE PRINCIPAL.** A closed set of condition fact kinds is substrate-owned
(`{quota-recovered, escalation-ruled}` — `escalation-ruled/<decision-request-id>`
is filed by the ruling verb in the same transaction that resolves a decision
request, `escalation-substrate-v1.md` its owner; reserving it closes ruling-fact
forgery, principled under this same invariant — the substrate owns the facts it
observes and produces) and may be filed **only** by the
substrate's reserved `process:tightbeam` principal. Every other kind is
org/product-owned and fileable by **any authenticated non-`tightbeam` principal —
sessions, users, AND org automation processes** (a non-substrate `process:` origin,
e.g. a CI runner or a deploy script). Only the substrate principal is special, and
only for reserved kinds. A non-substrate attempt to file a reserved kind is denied
`reserved_kind`. This keeps the boundary: the substrate owns the facts it observes;
everyone else may file the facts they observe.

**W9 — SILENT WHEN WAITING; EVERY EDGE LEGIBLE.** A pending condition wake
injects nothing into any agent's context. Every state change — scheduled, fired
(by condition or fallback), canceled — and every condition fact filed emits one
`lifecycle_events` row (open CHECK, no migration, §6). Rating is derived, never
stored: subscription counts, time-to-fire, and firing cause are queries over
these rows.

**W10 — NOT A STREAMING SYSTEM; NO MULTI-TARGET ROWS, NO STANDING FEEDS, NO
REPLAY.** Each subscription is a single row with **one** target and fires **once**.
There is no multi-target subscription, no standing feed, no replay of pre-existing
facts, no fan-in aggregation. **What IS intended and inherent:** one filed fact MAY
match and fire **several independent one-shot subscriptions** (e.g. two parked
blocks both waiting on `quota-recovered/codex` both wake) — this is not pub-sub
fan-out from one subscription, it is many one-shot subscriptions each consuming the
same observed fact, and it is correct. The non-goal is a *channel/stream
abstraction*, not the fact that a shared condition can release multiple distinct
waiters.

---

## 2. Decisions A–H (the load-bearing choices)

### A. Which stream subscriptions match against — a new `condition_facts` table

**Decision:** one new append-only `condition_facts` table is the sole matchable
stream (W2). Both substrate-observed and org/script condition facts land through
a single writer, `ConditionFacts.file/3` (§3): the substrate calls it internally for
`quota-recovered` (from the classification seam, §5); org/script producers call
it via the new `condition` verb (§9). **Justification (genuine schema/model/feed
objections — the two weak arguments from r1 are dropped):** the three existing
streams each fail a hard *model* requirement, not a bookkeeping one. `attests` is
FK-bound to an assignment (`assignments.ex:51`) and CHECK-locked to
`{progress,completion,surrender,verdict}` — a `quota-recovered(harness)` fact has
**no assignment** and no valid attest kind, so it does not fit the attest data
model at all; this is the disqualifier, NOT any "consumed marker" concern
(consumption lives on the wake row, exactly as it does for the dedicated table).
`events` is CHECK-locked to `kind IN ('verb','denied')` (`event_log.ex:38`) and is
the **dispatch-verb feed**: a condition fact is not a verb call, so adding a third
kind conflates the feed's semantics and forces a CHECK migration on a shared table
for a non-verb concept (this is a *feed-semantics* objection — note it would NOT
corrupt `verb_count`, which explicitly filters `kind='verb'`, `event_log.ex:113`;
that r1 "muddies backstop counting" argument was wrong and is withdrawn).
`lifecycle_events` is non-decision observability by contract ("nothing consumes
these to make decisions in the core", `event_log.ex` moduledoc) — making it
matchable would break that contract. A **union** view over `condition_facts +
attests` was rejected because a literal matcher wants one `{kind, scope}` shape
(W3), and attest rows carry a different shape (assignment-scoped, verdict-kinded).
Verdict-awaiting is served without a union — see the boundary note below. A
dedicated table also gives condition facts their own monotonic id, which is the
no-replay cursor (W4, §4.3), and keeps the substrate exposing *neutral fact truth*
in its own append-only stream rather than overloading a product-shaped table.

**Boundary note (verdict-awaiting without coupling).** "Gates awaiting verdict
facts" is one of the four unified consumers, but the substrate does **not**
mirror verdicts into `condition_facts` — that would import a product artifact
(the verdict vocabulary) into a substrate table. Two honest paths remain, both
product-side: (1) the P5/P6 machinery (remedy + turn-end sweep re-dispatch)
already serves a verdict gate whose holder has an open turn to sweep; (2) when a
gate wants *condition-wake* delivery specifically (no open turn, e.g. a spawner
waiting on a reviewer it spawned), the **producer script** (P4, kungfu) files a
`condition_facts` row alongside its verdict. The substrate never decides to; the
org's script does. This keeps the verdict vocabulary as bundle data and the
mirror as a product choice.

### B. The pattern language — `{kind, scope}`, literal, closed

**Decision:** a condition fact is `{kind, scope, ts, id}` (§3). A subscription
pattern is `{kind (required), scope (optional)}`. Matching is exact-equality on
`kind` and, when the pattern's `scope` is non-nil, exact-equality on `scope`; a
nil pattern `scope` is a wildcard matching any fact scope including nil (W3).
**Exactly two matchable fields, no more** — `kind` names the condition,
`scope` narrows it to an instance (the harness for `quota-recovered`, a work-item
or deploy target for an org condition). **nil semantics, stated precisely to
avoid the `p3` "nil never satisfies" confusion:** that rule governs *rule
evaluation over a fact*; this is *subscription matching*, a different operation.
Here (i) a pattern `kind` is required and non-nil — a subscription with no kind
is rejected at schedule; (ii) a pattern `scope` of nil is the **wildcard, and that
is its only meaning** — it matches every fact scope, including a fact whose scope
is nil; (iii) a fact whose `scope` is nil (a condition with no instance dimension)
is reachable **only** through the wildcard pattern. **There is deliberately no way
to express "match only facts whose scope is nil"** — nil-pattern-scope is one
thing (the wildcard), never also an exact-nil selector. If exact-nil selection is
ever needed it is a future extension with a distinct representation, out of scope
for v1. No other field is matchable; `ts`/`id` are substrate bookkeeping, not
pattern inputs. **Justification:** two exact-equality
fields is the smallest surface that expresses `quota-recovered(codex:sol)` and a
generic org `deploy-succeeded(prod)` while staying inside the literal-only engine
doctrine and being trivially index-backed (`(kind, scope, id)`).

### C. Delivery semantics — one-shot, CAS-gated single-owner firing, cancel via cancel-wake

**Decision — consumption:** one-shot only (W4). Standing subscriptions are a
non-goal (§8). **Firing owner + arbitration (F1/F2, normative):** every fire — by
condition OR by fallback — is executed by the **one** `WakeScheduler` GenServer as
the **one CAS-gated transaction of W6**. Within a single evaluation of a wake the
condition match is checked **before** the fallback deadline; the check that wins
sets the cause `firedBy ∈ {condition, fallback}` **in the same CAS UPDATE** that
transitions `pending → fired`, and that same transaction enqueues the prompt and
writes the one lifecycle row. There is no separate "deliver then mark," so there is
no window in which a canceled or already-fired row still enqueues: the CAS gates
the enqueue (a cancel that commits first leaves `changes == 0`, the fire aborts;
a fire that commits first leaves a later cancel's `WHERE state='pending'` matching
zero rows). **Mid-turn firing:** the enqueue is `Ledger.enqueue_in_txn`, so the
prompt **queues as the next turn** and never interrupts a running turn, exactly as
a timed wake landing mid-turn does. Re-adjudication happens when the target picks
up the queued prompt. **Fallback composition ("condition OR at time T" as one
wake):** the SAME wake row carries both the pattern and the mandatory finite
`dueAt` (W5); whichever fires first consumes the one-shot row. **Trigger stamp:**
the delivered prompt is the caller's prompt, prefixed with a one-line substrate
trigger stamp — `[woke: fact quota-recovered/codex:<identity>]` or `[woke: fallback
deadline]` — analogous to the existing `[from <origin>]` stamp (`gateway.ex:503`);
fact-stamping for legibility, W1 holds regardless. **Cancellation:** the CLI form
is `tightbeam cancel-wake <wakeId>` (existing command, `args.rs:266` →
`dispatch.rs:279`, wire field `cancelWakeId`); a condition wake is a wake row, so
`Wakes.cancel/3` (wake_id + origin match) transitions `pending → canceled`
unchanged. **Justification:** the only new behavior is the CAS-gated match/fire
(§4.3); everything else reuses proven `wakes.ex` mechanism.

### D. The `quota-recovered` condition — who observes, fields, hysteresis, honest meaning

**Decision — scope is the adapter selection key, coarsened explicitly.** Adapters
are selected by `{harness, identity_name, host}` (`gateway.ex:971`
`checkout_adapter`). A quota/rate-limit pool is a property of the **credential
identity**, not the machine, so v1 sets `scope = "<harness>:<identity_name>"`
(e.g. `"codex:sol-primary"`) and **coarsens away `host`** deliberately: a
credential pool spans hosts, and a success on one host proves the pool recovered
for all. **Ruled explicitly:** a bare harness scope (`"codex"`) is NOT used —
success under one credential pool proves only that pool, and two identities on the
same harness have independent quotas; the identity dimension is mandatory. If a
harness is ever found to meter per-host, `scope` extends to include host — an
additive change to the string, no matcher change. A parked block subscribes with
`scope` = its own session's `"<harness>:<identity_name>"`. Substrate-reserved kind
(W8). **Who observes — GAP 1 is a HARD PREREQUISITE, not present today.** ACP turn
errors are opaque `{:error, e}` on `main` (`adapter.ex:297`); the substrate does
**not** distinguish `quota_exhausted` yet. `quota-recovered` is therefore
**blocked on `model-ringdown-pattern.md` GAP 1** (harness error classification at
the boot/config/runtime seam). The r1 "the classifier already distinguishes"
claim is **withdrawn**. **Debounce / hysteresis (durable, transactional — never a
lifecycle marker as decision state):** the producer is **edge-triggered per
exhaustion episode**, and the episode state lives in a durable `quota_episodes`
table (§5), NOT in `lifecycle_events` (whose contract forbids being read for
decisions). After the substrate classifies `quota_exhausted` for a
`{harness, identity}` it opens an episode; on the next observed success, **one CAS
transaction** closes the episode AND files `quota-recovered` (§5) — atomic, so a
crash cannot duplicate or lose the recovery fact. It files **exactly one**
`quota-recovered` per episode and none until a new `quota_exhausted` re-opens one
(`exhausted → recovered → exhausted → recovered`, never `recovered → recovered`).
Combined with one-shot subscriptions (W4), a parked block receives **at most one**
recovery wake per episode — flapping cannot amplify into a storm from either side.
**Honest statement of what "recovered" means — the unverified part, stated
exactly:** whether any harness exposes a *leading* remaining-quota / rate-limit-
reset gauge is **UNVERIFIED** (`model-ringdown-pattern.md` GAP 7; the derived
catalog carries inventory/capability only, not quota). Therefore v1 defines
`quota-recovered` as a **lagging, use-confirmed** signal: the substrate files it
when it observes a **successful turn or probe on a previously-exhausted harness**
(the classified `quota_exhausted` state for that harness clears on the next
success). This is "investigate-then-expose" per GAP 7: **if** the GAP 7
investigation later surfaces a leading gauge, the producer additionally files on
the gauge crossing back above its floor (a strictly better signal, same fact, no
subscriber change). Until then the honest consequence, spelled out for reviewers:
a parked block's *own* condition subscription most reliably fires when **another**
session on the same harness recovers first and the substrate observes that
success — the block piggybacks on an independently-observed recovery; if nothing
else uses the harness, the block's **timed fallback** is the actual re-check (its
fallback fires, the agent re-adjudicates by attempting the harness, and that
attempt's success is itself what files `quota-recovered` for the next waiter).
v1 does not claim a leading recovery signal it cannot observe.

### E. Supervision interaction — a condition wake is a scheduled continuation

**Decision:** no new predicate, but a **usage invariant that the primitive must
enforce** (W7) — the parked-session re-check wake must **target the holder session**
(by *any* creator; the ruled ringdown flow is **owner-created**, because the
holder's model is dead and cannot schedule). State it against the real code.

(0) **The target-keying trap (the ringdown r3 finding, solved).** The ringdown
r3 review proved "parked-block-not-a-stall" FALSE for its own flow because
`Wakes.pending_count(db, session_key)` counts only wakes whose **target
`sessionKey`** equals the holder (`wakes.ex:173-182`; supervision passes the
holder's key at `supervision.ex:185`). In the r3-analyzed flow the re-check was
targeted at the **owner/spawner** (a different session), so it did NOT pause the
holder — supervision still saw the holder with an open assignment and no
continuation, and prodded/reaped it. This spec's parked-block exit fixes that by
**targeting the holder**: the park wake carries `sessionKey = holder`, which is
what makes `pending_count(holder) > 0`. **Its creator is free** — in the ruled
parking flow the holder's model is dead, so the **owner creates** the
holder-targeted park wake on the holder's behalf (an agent may instead self-create
one before its model dies; both target the holder and both pause it). A wake
targeting anyone *other* than the holder does not pause the holder, exactly as r3
found; §11 case 10c is the owner-created parking proof and 10b the negative
(owner-*targeted* does not suppress).

(1) **Base stall check (GROUND TRUTH on `main`).** Given the target-keying
invariant, `Supervision.evaluate_terminal` returns `:continuation` whenever
`Wakes.pending_count(db, holder) > 0` (`supervision.ex:185`, else-branch :206). A
holder-targeted condition wake is a row in the `wakes` table with `state='pending'`
and `sessionKey = holder`, so `pending_count` counts it **regardless of creator** —
a parked holder with a live holder-targeted condition subscription is
`:continuation`, never `:idle`. **This is the only not-a-stall guarantee that holds
against `main` today**, and it needs only the additive wake columns (§4.1) — no
supervision change.
(2) **Rail turn-end step (DEPENDS ON `rails-mechanism-v1`; NOT ground truth).**
`Wakes.self_pending_count/2` **does not exist on `main`**, and current supervision
has **no rail turn-end step** — both are *proposed* by `rails-mechanism-v1.md`
§I6/§D2. The following is the behavior this spec REQUIRES **when that spec ships**,
not a costless no-op today: the step suppresses on `self_pending_count > 0`.
**Self-scheduled is decided on the durable creator identity, not the mutable origin
(F7 addendum — ringdown r4 hole).** `origin` is a role/user string, so role
rebinding could move a role off the holder and invalidate an origin-based
self-scheduling proof. RULE: a wake counts as **self-scheduled** for the holder iff
`sessionKey = holder AND creatorSessionKey = holder` (§4.2) — the same session
incarnation created and targets it. This survives rebinding and gives the
adjudication/park flow its provable **creator ≠ target** distinction: an
**owner-created, holder-targeted** park wake has `sessionKey = holder` (counts for
base `:continuation`) but `creatorSessionKey = owner ≠ holder` (does NOT count as
self-scheduled) — exactly correct, and now expressible. `rails-mechanism-v1` will
define `self_pending_count` on this column rather than defining its own; this spec
owns the `creatorSessionKey` column and stamping (§4.1, §9). Under it, a parked
holder that schedules its own re-check (`creatorSessionKey = holder`) suppresses
the rail step. (3) A condition wake scheduled **by the substrate or owner** but
**targeted at the holder** (`sessionKey = holder`, per W7) still counts at the base
level (`pending_count` → `:continuation`), so it is not a stall, but does not count
as `self_pending` — moot, because base `:continuation` short-circuits before the
rail step. A condition wake targeted at some **other** session (owner/spawner)
counts for neither the holder's `pending_count` nor its `self_pending_count` and
so does NOT pause the holder — the r3 trap; the parked-block exit must self-target
(point 0, W7).
**The block record vs the recovery condition are distinct rows, deliberately:**
the parked block's *record* is filed with the work's existing attest machinery (a
`progress` attest carrying the block reason), which increments
`Assignments.attest_count` and thereby **resets** supervision's prod counter
(`claim_and_act`, `supervision.ex:229`) — this is `model-ringdown-pattern.md`'s
"a filed fact resets." The *recovery condition* (`quota-recovered`) is a
`condition_facts` row filed by whoever recovers — this is the **matchable**
stream, which supervision does not watch. Keeping them separate is why the block
both resets the prod countdown (attest) and pauses it on a scheduled continuation
(the condition wake), satisfying `model-ringdown-pattern.md`'s parked-state
non-stall definition exactly.

### F. Legibility — self-naming lifecycle events

**Decision:** every edge emits **exactly one** `lifecycle_events` row (open `kind`
CHECK, no migration — `event_log.ex`), per W9. To bind the row atomically with the
state change that produced it (and to avoid the deadlock in F5 below), fire/cancel
rows are written **inside** their CAS transaction via the in-transaction writer
`EventLog.lifecycle_in_txn/4` (§6); the fact-filed and scheduled rows are written
inside the file/schedule transaction likewise.
- `wake_condition_scheduled` — subject `wake_id`; detail `kind=<k> scope=<s>
  fallbackAt=<ms> origin=<origin>`.
- `wake_condition_fired` — subject `wake_id`; detail `firedBy=condition
  matchedFactId=<id> kind=<k> scope=<s>` (bound in the fire CAS).
- `wake_fallback_fired` — subject `wake_id`; detail `firedBy=fallback
  fallbackAt=<ms>` (bound in the fire CAS).
- `wake_unresolved` — subject `wake_id`; detail **carries the firing cause**
  `firedBy=condition|fallback` and, when `condition`, `matchedFactId=<id>
  scope=<s>`, plus `target=<key|role> reason=…` (fired-with-zero-enqueue, W6). It
  is the ONE lifecycle row for this edge, so the `firedBy` analytics ratio (§F
  below) stays complete — an unresolved fire is not a hole in the corpus (F4).
- `wake_condition_canceled` — subject `wake_id`; detail `by=<origin>`.
- `condition_fact_filed` — subject `fact_id`; detail `kind=<k> scope=<s>
  by=<origin>`.

Rating is derived, never stored (observability-v1): live-subscription count,
time-from-schedule-to-fire, and fired-by-condition vs fired-by-fallback ratio
(from the `firedBy` detail) are queries over these rows. The delivered prompt's
trigger stamp (§C) is the self-naming at the agent's edge.

### G. CLI surface — the wake verb's condition form (do not amend guidance yet)

**Decision:** the `wake` verb gains a condition form; a new `condition` verb files
a fact. Flag shape follows the guidance spec's operating-manual teaching style
(`agentic-engineering-guidance-spec.md` §2; `cli-rust-v1.md`:
`--prompt` required, `--after <n>ms|s|m|h`):

```
# condition wake with a mandatory timed fallback (parked-block re-check):
tightbeam wake --session S_… \
  --when-fact quota-recovered --when-scope codex:sol-primary \
  --fallback-after 30m \
  --prompt "Quota may have recovered on codex. Re-derive the block and re-adjudicate."

# org/script producer files a condition fact (non-reserved kind), idempotent:
tightbeam condition --kind deploy-succeeded --scope prod --key deploy-8f2a

# cancel — existing command, unchanged:
tightbeam cancel-wake w_…
```

**CLI + wire mapping (F9 — args.rs/dispatch.rs are in the seam, §10).**
- `wake` gains `--when-fact <kind>` (→ wire `conditionKind`) and `--when-scope
  <scope>` (→ `conditionScope`, optional). `--fallback-after <n>ms|s|m|h` is the
  **canonical** fallback flag; it maps to the **existing** wire field `afterMs`
  (dispatch.rs already emits `afterMs`, `dispatch.rs:97-98`), reused as the
  fallback deadline when a condition is present; `--at <epochMs>` maps to the
  existing `at`. There is NO new wire field for the fallback — it is the wake's
  ordinary due time, reinterpreted as the fallback because a condition is set.
- When `conditionKind` is present the handler (`gateway.ex:308`) **requires**
  `after_ms`/`at`; absent it → `{code:"invalid", message:"a condition wake requires
  a fallback (--fallback-after / --at)"}` (W5).
- New `condition` command → wire verb `condition` with `kind` (required, →`kind`),
  `scope` (optional, →`scope`), and `--key <k>` producer idempotency (→
  `idempotencyKey`, `operation="condition"` in `wire_idempotency`, §9/F4).
- The cancel form is the pre-existing `tightbeam cancel-wake <wakeId>`
  (`args.rs:266` → `dispatch.rs:279`, wire field `cancelWakeId`) — the earlier
  `wake --cancel-wake` form was wrong and is removed.

**Guidance note (do NOT amend now):** the guidance spec's operating manual
(`agentic-engineering-guidance-spec.md` §2) and the kungfu
archetypes gain the condition-wake teaching **only when this ships**; this spec
does not edit `agentic-engineering-guidance-spec.md`. Filed as a follow-up on that
spec, gated on S1 landing.

### H. Scope guard — the non-goals, named

**Decision:** the following are explicitly NOT built (W10):
- **No general pub-sub / message bus.** A subscription is a durable one-shot
  wake, not a channel.
- **No fan-out.** One subscription targets exactly one session or one role; one
  firing produces one wake delivery. A condition that many sessions care about is
  many subscriptions, one per session — not one row delivering to many.
- **No fan-in / aggregation.** No "wake when N facts match" or "when facts A and
  B both filed." One matching fact fires it.
- **No standing subscriptions.** One-shot only; re-adjudication re-subscribes.
- **No replay / history query.** A subscription matches only facts filed strictly
  after it was created (the id cursor, §4.3); it never sees a pre-existing fact.
  `condition_facts` is not a queryable event history for agents — it is the
  substrate's match input.
- **No predicates / regex / ranges.** Two exact-equality fields (W3).
- **No live streaming to a connected client.** Firing is a wake, delivered as a
  turn; there is no push feed.

---

## 3. The `condition_facts` table (new)

Append-only, in `lib/tightbeam/condition_facts.ex`:

```sql
CREATE TABLE IF NOT EXISTS condition_facts (
  id     INTEGER PRIMARY KEY AUTOINCREMENT,
  ts     INTEGER NOT NULL,
  kind   TEXT    NOT NULL,
  scope  TEXT,               -- nil = the condition has no instance dimension
  origin TEXT    NOT NULL    -- who filed it (process:tightbeam or a principal id)
);
CREATE INDEX IF NOT EXISTS condition_facts_match ON condition_facts (kind, scope, id);
```

- `id` is the monotonic match cursor (W4): a subscription created at cursor `c`
  matches only rows with `id > c`.
- `kind` is the fact kind. Substrate-reserved kinds are a closed module constant
  (`@reserved_kinds ~w(quota-recovered escalation-ruled)`); everything else is
  org/product. `escalation-ruled` is owned by `escalation-substrate-v1.md` (its
  ruling verb files `escalation-ruled/<decision-request-id>` as a substrate
  producer in the resolving transaction); reserving it closes ruling-fact forgery
  under W8.
- `scope` is the optional instance dimension (harness for `quota-recovered`).
- `origin` records the filer for legibility and reserved-kind enforcement (W8).
- No CHECK on `kind` — the org owns its kind vocabulary; the substrate validates
  only that a **reserved** kind is filed by `process:tightbeam` (§9).

**Two writer forms, one nudge discipline.** `ConditionFacts` exposes:
- `file(db, scheduler, %{kind, scope, origin})` — the **own-transaction** form: opens
  one transaction, inserts the fact row + the `condition_fact_filed` lifecycle row
  (via `EventLog.lifecycle_in_txn/4`, §6), commits, then nudges the scheduler
  **once** (`Wakes.fire_matching(scheduler)`, §4.3) and returns the row.
- `file_in_txn(txn, %{kind, scope, origin})` — the **caller's-transaction** form,
  mirroring `lifecycle_in_txn` (§6): a `Txn.q` fact insert + `lifecycle_in_txn`
  **inside the caller's already-open transaction**, returning the row. It does
  **not** open a transaction and does **not** nudge — the single post-commit nudge
  is owned by the **outermost caller** (which calls `Wakes.fire_matching` once,
  after its transaction commits). This exists because a producer must sometimes
  file the fact **atomically with its own state change** — the escalation ruling
  resolves the decision-request and files `escalation-ruled/<id>` in ONE
  transaction; `file` opening its own transaction would break that atomicity and
  deadlock the DB owner (the same constraint §6 solved for lifecycle rows).

**Three callers, all single-nudge (F13):** the substrate's `quota-recovered`
producer (§5), the `condition` verb (§9), and the **escalation ruling producer**
(`escalation-substrate-v1.md`, which uses `file_in_txn` inside its resolving
transaction and owns the post-commit nudge). No caller calls `fire_matching` more
than once per filed fact; the scheduler is the sole firing executor (W6).

---

## 4. The wake table extension and match evaluation

### 4.1 Additive columns on `wakes` (migration precedent: the `reresolve` columns)

`wakes.ex` `ensure_schema/1` already ALTERs additively and swallows "duplicate
column" (`wakes.ex:69-79`). Add five nullable columns the same way:

```sql
ALTER TABLE wakes ADD COLUMN conditionKind     TEXT NULL;
ALTER TABLE wakes ADD COLUMN conditionScope    TEXT NULL;
ALTER TABLE wakes ADD COLUMN conditionAfterId  INTEGER NULL;  -- the no-replay cursor
ALTER TABLE wakes ADD COLUMN firedBy           TEXT NULL CHECK (firedBy IN ('condition','fallback'));
ALTER TABLE wakes ADD COLUMN creatorSessionKey TEXT NULL;     -- durable creator identity (F7 addendum)

-- Fact→subscription lookup for the condition branches (§4.3). `state` FIRST so
-- the equality lookup excludes historical fired/canceled rows AT THE INDEX,
-- never examining them.
CREATE INDEX IF NOT EXISTS wakes_condition
  ON wakes (state, conditionKind, conditionScope);
```

The existing `wakes_due (state, dueAt)` index (`wakes.ex:62`) backs the fallback
branch (§4.3). **Ordering key: `rowid` alone.** `wakes` has an implicit integer
`rowid` (the table is not `WITHOUT ROWID`; `wakeId TEXT PRIMARY KEY` does not
displace it), which is **insertion-monotonic per table** — the correct
oldest-first key. `createdAt` **is not** an ordering key: it is
`System.system_time(:millisecond)` (`wakes.ex:313`), wall-clock and
NTP-regressable, so it can move backward between inserts; it stays for display
only. `wakeId` is a random UUIDv4 (`id.ex:4`) and is never an ordering key.

A **timed wake** has the condition/firedBy columns nil (unchanged behavior today).
A **condition wake** has non-nil `conditionKind`, optional `conditionScope`,
`conditionAfterId` = the max `condition_facts.id` at schedule time, and a finite
`dueAt` fallback (W5). `firedBy` is set **in the fire CAS** (W6) to record which
trigger won; nil while pending. `dueAt` stays NOT NULL — the fallback is mandatory
as a v1 storage limitation (W5), not a policy choice.

**`creatorSessionKey` — the durable self-scheduling identity (F7 addendum,
supersedes the origin/role join).** `origin` is a **mutable** role/user string
(`agent:<role>`, `user:<id>`, `process:tightbeam`); role rebinding can move a role
off the holder session, so `origin` cannot prove "the holder scheduled this."
Therefore every wake is stamped at schedule time with `creatorSessionKey` = **the
session key of the scheduling principal when that principal is a session**
(`{:session, key} → key`), and **nil** for user/process principals (which have no
creator session). This is durable: it is the concrete session incarnation that
created the wake, immune to later role rebinding. `origin` is retained unchanged
for cancel authorization and the return-address stamp; `creatorSessionKey` is the
identity supervision reads.

**`schedule/2` gains a `schedule_in_txn/2` seam (F3).** Today `Wakes.schedule/2`
opens its own `DB.transaction` (`wakes.ex:110`), so `wake_result` cannot call it
inside the outer idempotency transaction (§9) without re-entering the single DB
owner and deadlocking (`db.ex:49`). Add **`Wakes.schedule_in_txn(txn, input)`** —
the insert body running on the caller's `txn` — with **`schedule/2` re-defined as
its own-transaction wrapper** (`DB.transaction(db, &schedule_in_txn(&1, input))`),
the same `*_in_txn` pattern this spec uses for delivery (§4.3), lifecycle (§6), and
fact-filing (§3). Both forms accept the new fields (nil-defaulted, as `reresolve*`
are), derive `creatorSessionKey` from the principal, and set `conditionAfterId` to
`SELECT COALESCE(MAX(id),0) FROM condition_facts` **inside the same transaction**,
so the cursor is exactly "everything already filed is invisible to this
subscription" (W4, no-replay).

### 4.2 Counting: the condition columns must stay invisible to the counts (W7)

`Wakes.pending_count/2` exists on `main` and selects on `state`/`sessionKey` only;
the condition columns do not appear in its WHERE clause, so a pending condition
wake counts identically to a pending timed wake — this is the ground-truth
not-a-stall guarantee (§7 point 1). `Wakes.self_pending_count/2` is **proposed by
`rails-mechanism-v1.md` §D2 and does not exist on `main`**; when it lands it must
be defined on the **durable creator identity** (F7 addendum), not the mutable
origin:

```sql
-- self_pending_count(holder): pending wakes the holder itself created for itself
SELECT count(*) FROM wakes
WHERE state = 'pending' AND sessionKey = :holder AND creatorSessionKey = :holder;
```

`creatorSessionKey = holder` proves the *same session incarnation* both created and
targets the wake, and survives any role rebinding — the hole the ringdown r4 review
found in an origin-string test. It must likewise ignore the condition columns. The
invariant for this spec: **do not add any condition predicate to either count** —
supervision sees a condition wake as an ordinary scheduled continuation.

### 4.3 Match evaluation — one owner, set-based query, CAS-gated fire, bounded batch

All CONDITION-wake evaluation runs in the `WakeScheduler` GenServer (one owner,
W6). Two entry points, both executing the **same one bounded candidate query +
per-wake CAS-gated fire (W6)**:

- **the tick** (`deliver_due`, backstop, `wakes.ex:235`),
- **`fire_matching(scheduler)`** — the single eager nudge from `ConditionFacts`
  (§3), owned by the outermost fact-filing caller.

**Legacy timed wakes are untouched (F2).** Pure timed wakes (`conditionKind IS
NULL`) keep the **existing** `deliver_due` path verbatim — deliver-then-mark
(`wakes.ex:232`), `firedBy` stays nil, byte-unchanged. They are **not** in the
candidate query below and never take the CAS path. The `fire_due(scheduler)` nudge
(`gateway.ex:1544`) for already-due timed wakes is likewise unchanged.

**One work-bounded candidate query — valid-SQLite `UNION ALL` of per-branch
subqueries; condition branches FACT-ORDERED, forced index-driven (F1/F2).** SQLite
forbids a branch-local `LIMIT` directly before `UNION ALL`, so each branch is a
**wrapped subquery** with its own `ORDER BY … LIMIT :batch` and each `INDEXED BY`
its index — tightbeam runs **no `ANALYZE`/`PRAGMA optimize`** (nothing writes
`sqlite_stat1`), so without the hint the planner would pick `wakes_due(state=?)`
as the driver for the condition branches. Each row carries a **branch tag** so the
scheduler computes the watermark advance from the returned rows alone (below):

```sql
-- :afterFact from scheduler_state; :ceil = COALESCE(MAX(id),0) FROM condition_facts, read
-- ONCE at pass start (snapshot). The EAGER path substitutes `f.id = :factId`
-- for the `f.id > :afterFact AND f.id <= :ceil` range (one fact).
SELECT * FROM (
  -- C1 — condition, EXACT scope; FACT-ORDERED (filing order), wakes oldest-first.
  SELECT 'C1' AS branch, w.wakeId AS wakeId, f.id AS matchedFactId,
         f.scope AS matchedScope, w.rowid AS rid
  FROM condition_facts f CROSS JOIN wakes w INDEXED BY wakes_condition
  WHERE f.id > :afterFact AND f.id <= :ceil
    AND w.state = 'pending' AND w.conditionKind = f.kind
    AND w.conditionScope = f.scope AND f.id > w.conditionAfterId  -- pure equality
  ORDER BY f.id ASC, w.rowid ASC LIMIT :batch
)
UNION ALL
SELECT * FROM (
  -- C2 — condition, WILDCARD scope; FACT-ORDERED. Pure IS NULL, no OR.
  SELECT 'C2' AS branch, w.wakeId AS wakeId, f.id AS matchedFactId,
         f.scope AS matchedScope, w.rowid AS rid
  FROM condition_facts f CROSS JOIN wakes w INDEXED BY wakes_condition
  WHERE f.id > :afterFact AND f.id <= :ceil
    AND w.state = 'pending' AND w.conditionKind = f.kind
    AND w.conditionScope IS NULL AND f.id > w.conditionAfterId
  ORDER BY f.id ASC, w.rowid ASC LIMIT :batch
)
UNION ALL
SELECT * FROM (
  -- F — fallback, dueAt-driven on the existing wakes_due(state,dueAt) index;
  -- pure rowid order.
  SELECT 'F' AS branch, w.wakeId AS wakeId, NULL AS matchedFactId,
         NULL AS matchedScope, w.rowid AS rid
  FROM wakes w INDEXED BY wakes_due
  WHERE w.state = 'pending' AND w.dueAt <= :now AND w.conditionKind IS NOT NULL
  ORDER BY w.rowid ASC LIMIT :batch
);
```

- **Work-bounded, forced index-driven (F1).** C1/C2 drive from the **facts side**
  (`CROSS JOIN` fixes `condition_facts` as the outer loop over its `f.id` integer-PK
  range, each fact probing `wakes INDEXED BY wakes_condition`), each with a **pure**
  predicate (C1 equality, C2 `IS NULL`) — no `OR` anywhere. F is a `wakes_due`
  range. Each branch is `LIMIT :batch`; there is **no cross-branch final `LIMIT`**
  — the pass fires every returned row (≤ `3·:batch`), so a candidate-selected fact
  is never stranded by a firing cap. **Acceptance criterion (7f):** `EXPLAIN QUERY
  PLAN` shows `SEARCH condition_facts USING INTEGER PRIMARY KEY (rowid>?)` feeding
  `SEARCH wakes USING INDEX wakes_condition` on C1/C2 (never `SCAN wakes`) and
  `SEARCH wakes USING INDEX wakes_due` on F.
- **Fairness model (F2), restated honestly.** Condition wakes are selected in
  **filing order** (`f.id ASC`) — the natural doorbell semantics: the oldest
  unserved fact's fan-out is taken first, wakes within a fact oldest-first by
  `rowid`; the fallback branch stays pure `rowid` order. Within each branch no
  older-eligible item is ever passed over for a younger one (the fact-ordered /
  rowid-ordered `LIMIT` takes the oldest first); an item waits only behind
  older-still same-branch items — backpressure, not starvation. There is no
  cross-branch global order and none is claimed (§11 case 7g proves exactly this).
- **Firing order + advisory rows.** The scheduler fires the returned rows; for
  legibility it fires condition rows sorted by `(matchedFactId, rid)` (filing
  order) — an O(:batch) in-memory sort. A wake matching in both a new fact and its
  fallback appears in ≤ 2 rows; the CAS re-probe (below) is authoritative and the
  first fire consumes the row, so the rest no-op. A branch that returned a full
  `:batch` self-nudges `fire_matching` to drain its remainder.

**The durable fact-watermark (`scheduler_state`) — advance is PURE ELIXIR over the
selected rows, zero SQL at advance time (F2).** `:afterFact` persists in a
single-row table so a restart does not re-scan fact history:

```sql
CREATE TABLE IF NOT EXISTS scheduler_state (
  id        INTEGER PRIMARY KEY CHECK (id = 0),   -- exactly one row
  afterFact INTEGER NOT NULL DEFAULT 0
);
INSERT OR IGNORE INTO scheduler_state (id, afterFact) VALUES (0, 0);  -- migration seed
```

A pass reads `afterFact` and captures `:ceil = COALESCE(MAX(id),0) FROM condition_facts` (0 on an empty table, so a drained-branch boundary can never be NULL against afterFact NOT NULL)
**once, at selection start**. It fires every selected row (selected == fired, so
nothing candidate-selected is stranded). It then computes the new cursor **in
Elixir from the ≤ `2·:batch` condition rows it already holds — no advance-time
table access.** Because each condition branch is fact-ordered, its returned rows
make the boundary trivial; per condition branch `b`:

```
boundary(b) = if count(b_rows) < :batch  -> :ceil                      # branch drained its window
              else                       -> max(matchedFactId in b_rows) - 1   # cut may be mid-fact
afterFact_new = min(boundary(C1), boundary(C2))    # :ceil when a branch had 0 rows
```

then one plain write, value already computed:

```sql
UPDATE scheduler_state SET afterFact = :afterFactNew WHERE id = 0;
```

- **Why it is correct.** Fact-ordering means a branch that returned `< :batch`
  rows exhausted every match in `(:afterFact, :ceil]` → advance to `:ceil` for that
  branch. A branch that returned exactly `:batch` fully consumed every fact **below**
  its max selected fact id (all their wakes sort before that fact's), and may have
  cut that fact mid-fan-out → boundary = `maxFactId − 1`. Taking the **min** across
  C1/C2 advances only past facts fully consumed by **both** condition predicates. A
  fact whose fan-out exceeds `:batch` is the branch's max and holds the cursor at
  its `id − 1`; its remainder drains next pass. Skipping a consumed fact is safe
  permanently — a later subscription's `conditionAfterId ≥` the current max fact id,
  so `f.id > conditionAfterId` is false for any older fact (W4), so a drained fact
  can never regain a match. `afterFact_new ≥ afterFact` always (monotonic).
- **Never a fresh `MAX(id)` at advance time.** The ceiling is the `:ceil` snapshot
  from selection start, never re-read. A fact committing after `:ceil` has
  `id > :ceil ≥ afterFact_new` and is caught next pass — the read/advance pair
  cannot skip an interleaved fact.
- The **eager path** (`fire_matching`) fires one filed fact's fan-out and does
  **not** move `afterFact` — the tick owns the watermark; a wake the eager path
  already fired no-ops when the tick re-selects it.
- A caller that files SEVERAL facts in one transaction (e.g. escalation
  waive-all) passes them to `fire_matching` as **one ordered list**: the
  scheduler serves them strictly in filing order, and a saturation
  continuation carries the whole remaining list — separate per-fact calls are
  forbidden for multi-fact filers because mailbox interleaving with saturation
  continuations lets a later fact's fan-out overtake an unserved earlier
  fact's (violating 7g) once a fact's fan-out exceeds two batches.

**Per-wake fire is the CAS-gated transaction of W6, and it RE-PROBES the cause
(F3).** For each candidate `wakeId`, in one transaction:
1. **Re-probe** the same match predicate for this wake *now* (inside the txn) —
   `SELECT f.id, f.scope … ORDER BY f.id LIMIT 1`. This, not candidate-list
   membership, decides the cause, so batch staleness or a fact filed since
   selection cannot mislabel: `firedBy = condition` iff the re-probe returns a
   fact, else `firedBy = fallback` iff `dueAt <= now`, else **abort** (the match
   vanished and the fallback is not due — nothing to fire).
2. **CAS** `UPDATE wakes SET state='fired', firedAt=?, firedBy=:cause WHERE
   wakeId=? AND state='pending'`. Iff `changes == 1`, in the SAME transaction
   deliver via **`Gateway.deliver_prompt_in_txn/…`** (F1) and write the one
   lifecycle row via `lifecycle_in_txn` (§6): `wake_condition_fired`
   (`matchedFactId` + scope from the re-probe) or `wake_fallback_fired`; or, if the
   target is unresolvable, enqueue zero + `wake_unresolved` **carrying the same
   `firedBy` cause and matched fields** (F4, §F) — so the one lifecycle row per edge
   keeps the cause even when nothing enqueues. If `changes == 0` the row was
   canceled/fired by a racer — no-op.
3. **After commit**, the scheduler's firing pass owns the publish + lane-nudge
   (the non-transactional tail of delivery, F1).

Because the CAS gates the enqueue and the cause is re-probed inside it, there is no
double-fire, no mislabel under batching, and no cancel-vs-fire race (W6).

---

## 5. The `quota-recovered` producer (substrate side)

`quota-recovered` is filed by the substrate at the classification seam, never by
an org script. **It is BLOCKED on `model-ringdown-pattern.md` GAP 1** — the
substrate does not classify `quota_exhausted` on `main` (ACP errors are opaque
`{:error, e}`, `adapter.ex:297`). The primitive (§3/§4/§9) ships without it; this
producer lands with GAP 1.

**Durable episode state — `quota_episodes`, never a lifecycle marker.** Episode
state is a decision input, so it must not live in `lifecycle_events` (whose
contract forbids being read for decisions). Add:

```sql
CREATE TABLE IF NOT EXISTS quota_episodes (
  harness      TEXT NOT NULL,
  identityName TEXT NOT NULL,
  state        TEXT NOT NULL CHECK (state IN ('open','closed')),
  openedAt     INTEGER NOT NULL,
  closedAt     INTEGER,
  PRIMARY KEY (harness, identityName)
);
```

Mechanism, keyed by the adapter selection identity `{harness, identity_name}`
(host coarsened, §D):

- On a classified `quota_exhausted` for `{harness, identity}` (GAP 1), upsert the
  episode `open` (`openedAt=now`) — idempotent; re-exhaustion while already open
  is a no-op.
- On the **next observed success** on that `{harness, identity}` (a completed turn
  or a recovery probe), **one transaction** does both: `UPDATE quota_episodes SET
  state='closed', closedAt=? WHERE harness=? AND identityName=? AND state='open'`;
  iff `changes==1`, `ConditionFacts.file_in_txn(txn, %{kind:"quota-recovered",
  scope:"<harness>:<identity>", origin:"process:tightbeam"})` in the **SAME**
  transaction (the caller's-transaction form, §3 — `file/3` would open its own
  transaction and deadlock the DB owner; `file_in_txn` is the F5-style seam). The
  **single post-commit nudge** (`Wakes.fire_matching(scheduler)`) is owned by this
  producer, after its transaction commits. Atomic close+file → exactly one recovery
  fact per episode, and a crash cannot duplicate or lose it. No further fact until a
  new `quota_exhausted` re-opens the episode (hysteresis, §D).
- If GAP 7 later surfaces a leading gauge, the producer additionally files on the
  gauge crossing; subscribers are unaffected.

The substrate owns this end-to-end: the org writes no poller, and `quota-recovered`
cannot be forged by a non-substrate principal (W8).

---

## 6. Legibility events + the transaction-aware lifecycle writer (F5)

The events of §F write to `lifecycle_events` (open CHECK, no schema change). But
`EventLog.lifecycle/4` issues a fresh `GenServer.call` to the DB owner
(`event_log.ex:133`), and the fire/cancel/file work already runs **inside** a
`DB.transaction` callback executing in that same owner process (`db.ex`), so
calling `lifecycle/4` from within would **deadlock** (the owner calling itself),
and calling it *after* the transaction admits missing/duplicate rows on a crash
between commit and emit. Therefore this spec requires a **transaction-aware
writer**:

```elixir
# EventLog
def lifecycle_in_txn(%DB.Txn{} = txn, kind, subject, detail) do
  DB.Txn.q(txn,
    "INSERT INTO lifecycle_events (ts, kind, subject, detail) VALUES (?1, ?2, ?3, ?4)",
    [now(), kind, subject, detail])
  :ok
end
```

This is the exact in-transaction insert `EventLog.boot/1` already performs against
`lifecycle_events` via `Txn.q` (`event_log.ex:173`) — the precedent exists; this
just names it as a reusable helper. Every schedule/fire/cancel/file transaction
writes its **one** lifecycle row through `lifecycle_in_txn/4`, so **firing cause
(`firedBy`), enqueue/duplicate result, wake state, and the lifecycle row all
commit atomically** — no deadlock, no crash-window duplicate/loss. Rating is
derived (W9).

---

## 7. Supervision interaction, stated against the code (decision E, normative)

- **GROUND TRUTH on `main`:** `Supervision.evaluate_terminal`
  (`supervision.ex:177-209`) `with`-guards `0 <- Wakes.pending_count(db,
  session_key)`, `session_key` = the **holder**, `pending_count` keyed by the
  wake's **target `sessionKey`** (`wakes.ex:173-182`). A pending condition wake
  **targeted at the holder** makes this non-zero, so the else-branch
  (`supervision.ex:206`) returns `:continuation` (or `:busy` if a turn is queued).
  **A parked block with a live holder-targeted condition wake is never `:idle` and
  never reaped, regardless of who created it** (owner-created parking or
  self-created continuation both count) — this holds with only the additive wake
  columns (§4.1); no supervision change. A wake targeted at another session does NOT
  count — the r3 trap (§E point 0).
- **DEPENDS ON `rails-mechanism-v1` (NOT ground truth):** `Wakes.self_pending_count/2`
  and the §D2 turn-end step do not exist on `main`. **Requirement, honored when that
  spec ships:** a condition-subscribed wake counts as self-scheduled **iff
  `sessionKey = holder AND creatorSessionKey = holder`** (§4.2, F7 addendum) — the
  durable creator identity, immune to role rebinding (the ringdown r4 hole).
  `rails-mechanism-v1` defines `self_pending_count` on the `creatorSessionKey`
  column this spec adds and stamps (§4.1, §9), ignoring the condition columns. This
  spec does not claim the rail-step suppression is free against `main`; it states
  the contract and owns the column.
- The block *record* (a `progress` attest) resets the prod counter via
  `attest_count` (`supervision.ex:229`); the *recovery condition* is a
  `condition_facts` row supervision does not watch. Both hold together (§E).

This closes `model-ringdown-pattern.md`'s parked-state requirement: a block that
filed a fact **and** scheduled a continuation is, by supervision's own definition,
not a stall — and a block that filed neither remains the forbidden silent block
that correctly reads as a stall.

---

## 8. Non-goals (do not build) — the scope guard, enumerated

G1 no channel/stream abstraction. G2 **no multi-target subscription row** (one
subscription → one target, one firing). Note the truthful boundary (W10): one
filed fact MAY release several *independent* one-shot subscriptions — that is
intended, not fan-out from a single subscription. G3 no fan-in / multi-fact
aggregation ("when A AND B"). G4 no standing subscriptions (one-shot only). G5 no
replay or history query (the id cursor makes subscriptions forward-only;
`condition_facts` is match input, not an agent-queryable feed). G6 no
predicates/regex/ranges (two exact-equality fields); no exact-nil scope selector
(W3/§B). G7 no live client streaming. G8 no substrate mirroring of
verdict/build/smoke facts into `condition_facts` — a product script files those if
it wants condition-wake delivery (§A boundary note).

---

## 9. The `condition` verb and reserved-kind enforcement

Add `condition` to `@agent_verbs` (`wire/router.ex:46`). **Reserved-kind
enforcement lives INSIDE `ConditionFacts`, not in the Gateway (F8).** `@reserved_kinds`
is module-private to `ConditionFacts`; every writer form (`file/3`,
`file_in_txn/2`, `file_idempotent/3`) applies the internal predicate

```elixir
# ConditionFacts (private): the substrate producer path is the only one that
# may file a reserved kind. origin == "process:tightbeam" IS the token — the
# wire layer already forbids any non-substrate caller from presenting it
# (`wire/router.ex` reserved_origin), so no separate capability is needed.
defp reserved_ok?(kind, origin),
  do: kind not in @reserved_kinds or origin == "process:tightbeam"
```

and return `{:error, %{code: "reserved_kind", …}}` when it fails. The Gateway
handler **calls the API and never references the constant** — it cannot, `@reserved_kinds`
is not exported:

```
"condition" => fn call ->
  p = call.params
  scheduler = Map.get(config, :wake_scheduler, Tightbeam.WakeScheduler)
  if is_binary(p[:kind]) and p.kind != "" do
    # ConditionFacts enforces reserved-kind + idempotency + single nudge itself.
    ConditionFacts.file_idempotent(db, scheduler, %{
      kind: p.kind, scope: p[:scope], origin: call.origin,
      idempotency_key: p[:idempotency_key]
    })
  else
    %{code: "invalid", message: "a condition fact requires a kind"}
  end
end
```

`ConditionFacts.file_idempotent/3` (F4/F5) wraps, in **one** `DB.transaction`
using the **Txn forms** of the idempotency store: `Idempotency.get_in_txn(txn,
origin, "condition", key)` → on hit return the prior fact (replay, no new row);
else `reserved_ok?` check, then `file_in_txn` (fact insert + `condition_fact_filed`
lifecycle) + `Idempotency.put_in_txn(txn, …)` — all committed together (today's
`Idempotency.get/put` open their own DB calls, so **Txn forms are a required
implementation-seam addition**, §10). After commit it nudges the scheduler **once**
(§3, F13). The `operation="condition"` value requires **widening the
`wire_idempotency` CHECK** (currently `('spawn','retire','wake','assign')`,
`idempotency.ex:24`) to include `'condition'` via the existing
`widen_operation_check/1` migration (§10). The substrate's `quota-recovered`
producer (§5) and the escalation ruling (`escalation-substrate-v1.md`) call
`file_in_txn` directly under `process:tightbeam`, passing `reserved_ok?`
by origin — reserved kinds are thus fileable only by the substrate (W8).

`wake` verb, condition-form idempotency + validation (in the `wake` handler cond,
`gateway.ex:308`, before `wake_result`):
- **F4/F5 — exactly-one subscription per request, in one transaction.**
  `wake_result` must do idempotency-get + `Wakes.schedule_in_txn` + idempotency-put
  in **one transaction** via the **Txn forms** `Idempotency.get_in_txn/put_in_txn`
  (today it is three separate DB calls, `gateway.ex:1509-1542`, which lets two
  racing same-key requests both schedule). Mirror `assign` (`assignments.ex:333`):
  open one transaction, `get_in_txn` `wire_idempotency (operation='wake')`; on hit
  return the prior wake; else `Wakes.schedule_in_txn(txn, input)` (F3, §4.1 — NOT
  `schedule/2`, which opens its own txn and would deadlock the DB owner) +
  `put_in_txn` together. The `conditionAfterId = MAX(condition_facts.id)` read
  (§4.1) is inside this same transaction. The CLI `wake --key` field is a required seam
  addition (§10) — `Command::Wake` and its dispatch mapping have no `idempotencyKey`
  today (`args.rs:33`, `dispatch.rs:84`), yet acceptance 12a needs it.
- `condition_kind` present but no `after_ms`/`at` → `{code:"invalid", message:"a
  condition wake requires a fallback (--fallback-after / --at)"}` (W5).
- **Orphan scope is an error.** `condition_scope` present with **no** `condition_kind`
  (`--when-scope` without `--when-fact`) → `{code:"invalid", message:"--when-scope
  requires --when-fact"}`. Scope only narrows a pattern; without a kind there is no
  pattern to narrow.
- **F7 addendum — stamp `creatorSessionKey`.** `wake_result` passes
  `creator_session_key` to `Wakes.schedule_in_txn/2` (F3), derived from
  `call.principal`: `{:session, key} → key`; `{:user, _}`/`{:process, _} → nil`
  (no creator session).
  For a self-continuation (a live holder `H` parking itself), `call.principal =
  {:session, H}` and target `call.session_key = H`, so the row carries `sessionKey =
  H, creatorSessionKey = H` — provably self-scheduled (§4.2), independent of `H`'s
  roles. For the **ringdown parking flow** the owner `O` schedules on the dead
  holder's behalf: `call.principal = {:session, O}`, target `H`, so `sessionKey = H,
  creatorSessionKey = O` — pauses `H` (target-keyed) but is not `H`'s own
  self-scheduling (creator ≠ target), exactly as intended.
- otherwise the row is built with the condition fields (§4.1); the eager `fire_due`
  nudge for an already-due fallback is unchanged; condition matching runs on the
  next tick / `fire_matching`.

---

## 10. Per-phase implementation seam (modules / files)

| Concern | File | Change |
|---|---|---|
| Matchable stream | `lib/tightbeam/condition_facts.ex` (NEW) | `condition_facts` table + `ensure_schema/1`; `file/3` (own-txn + single nudge, §3); `file_in_txn/2` (caller's-txn insert, nudge owned by caller — atomic producers: quota §5, escalation ruling); `file_idempotent/3` (Txn-form idempotency, §9); private `@reserved_kinds` + `reserved_ok?/2` (F8 — enforcement lives here, not in Gateway) |
| Transactional delivery seam | `lib/tightbeam/gateway.ex` | **F1: refactor `deliver_prompt/4`'s in-txn core out** (target resolution via the now-shared `delivery_target/3`, projection append, `Ledger.enqueue_in_txn`) into `deliver_prompt_in_txn/…`, so the fire CAS delivers through the passed `txn`; the post-commit publish + lane-nudge is the scheduler firing pass's (`deliver_prompt/4:494`, own-txn `:510`, private resolver `:595`) |
| Wake condition form + firing | `lib/tightbeam/wakes.ex` | +5 additive columns (`conditionKind/Scope/AfterId`, `firedBy`, `creatorSessionKey`) + `wakes_condition (state,conditionKind,conditionScope)` index + NEW `scheduler_state` single-row watermark table (§4.1/§4.3); **`schedule_in_txn/2` + `schedule/2` wrapper (F3)**; CAS-gated fire with in-txn cause re-probe (W6); **valid-SQLite `UNION ALL` of per-branch subqueries with `INDEXED BY` (CROSS JOIN facts-side driver); condition branches FACT-ORDERED (`f.id, w.rowid`), fallback rowid-ordered; branch-tagged rows; no cross-branch final LIMIT (F1/F2)**; `:ceil` snapshot + **pure-Elixir min/max `afterFact` advance over selected rows → single-row `UPDATE scheduler_state` (no advance-time scan)** (§4.3); `fire_matching/1`; `deliver_due` keeps legacy timed wakes (`conditionKind IS NULL`) unchanged (F2); `pending_count` condition-blind (§4.2) |
| Verbs + idempotency Txn forms | `lib/tightbeam/gateway.ex`, `lib/tightbeam/idempotency.ex` | `wake` condition + orphan-scope validation + **single-txn** get/schedule/put via new `Idempotency.get_in_txn/put_in_txn` (F5) + `creatorSessionKey` derivation; new `condition` handler (calls `ConditionFacts`, never `@reserved_kinds`); **widen `wire_idempotency` CHECK to add `'condition'`** via `widen_operation_check/1` (`idempotency.ex:24`); scheduler ref plumbing |
| Transaction-aware legibility | `lib/tightbeam/event_log.ex` | add `lifecycle_in_txn/4` (F5, precedent `event_log.ex:173`); no schema change |
| Verb allowlist | `lib/tightbeam/wire/router.ex` | add `condition` to `@agent_verbs` |
| CLI | `cli/src/args.rs`, `cli/src/dispatch.rs` | `Command::Wake` gains `--when-fact`/`--when-scope`/`--fallback-after` (→ `conditionKind`/`conditionScope`/`afterMs`) **and `--key` → `idempotencyKey`** (missing today, needed by acceptance 12a); new `condition` command (`--kind`/`--scope`/`--key`); help text; arg tests (F5/F9) |
| quota producer + episodes | classification seam (`adapter*.ex`/coordinator, per **GAP 1**) + NEW `quota_episodes` table | classify `quota_exhausted` (GAP 1, hard prereq); atomic close + `file_in_txn` recovery + producer-owned post-commit nudge (§5); scope `"<harness>:<identity>"` |
| Supervision | `lib/tightbeam/supervision.ex` | none for the base guarantee (§7); `self_pending_count` (on `creatorSessionKey`, §4.2) + rail step are `rails-mechanism-v1`'s to build against the column this spec owns |
| Schema bootstrap | boot `ensure_schema` sequence | call `ConditionFacts.ensure_schema/1`, create `wakes_condition` + `scheduler_state` (seed row via `INSERT OR IGNORE`) in `Wakes.ensure_schema/1`, and the quota-episode schema with the producer |

Dependencies: the **primitive** (§3, §4, §6, §9, CLI, and decisions B/C/E/F/G/H) is
implementable now against `main`, with the sole caveat that the **rail-step**
suppression (§E point 2, §7) lands with `rails-mechanism-v1` — the base
`pending_count` not-a-stall guarantee does not. The `quota-recovered` producer
(§5, §D) is **blocked on GAP 1** (classification) and bounded by GAP 7 (no leading
gauge). Ship the primitive first; the producer follows GAP 1.

---

## 11. Acceptance contract (concrete provable cases)

Each case is silent-when-waiting, legible-on-every-edge, and honors W1
(re-adjudication, never resumption).

1. **Schedule + literal match, exact.** File nothing; schedule a condition wake
   `{quota-recovered, codex:sol}` fallback +1h; assert `pending`, no delivery,
   `wake_condition_scheduled` emitted. File `{quota-recovered, claude:main}` → no fire
   (scope mismatch). File `{quota-recovered, codex:sol}` → fires within one tick / on
   `fire_matching`; the target's next turn prompt carries `[woke: fact quota-
   recovered/codex:sol]`; wake is `fired`; `wake_condition_fired` names the matched
   fact id.

2. **Scope wildcard.** Schedule `{deploy-succeeded, nil}` (no `--when-scope`).
   File `{deploy-succeeded, staging}` → fires (wildcard matches). Separately,
   schedule `{deploy-succeeded, prod}`; file `{deploy-succeeded, staging}` → no
   fire; file `{deploy-succeeded, prod}` → fires.

3. **No-replay cursor.** File `{quota-recovered, codex:sol}`; THEN schedule
   `{quota-recovered, codex:sol}`; assert it does NOT fire on the pre-existing fact
   (`conditionAfterId` excludes it). File a second `{quota-recovered, codex:sol}` →
   fires.

4. **Fallback composition ("condition OR at T").** Schedule `{quota-recovered,
   codex}` fallback +200ms; file no fact; assert it fires by fallback at ~200ms
   with stamp `[woke: fallback deadline]` and `wake_fallback_fired`. Second run:
   file the matching fact before 200ms → fires as condition; assert NOT
   double-fired at the deadline (already `fired`).

5. **One-shot.** After a condition firing, file another matching fact → no second
   delivery (row is `fired`, not `pending`).

6. **Mid-turn firing queues, never interrupts.** With the target mid-turn, file
   the matching fact → the prompt enqueues as the next turn (Ledger), the running
   turn is untouched; on pickup the agent re-derives (W1).

7. **Cancellation + the cancel-vs-fire race (F1, both outcomes).**
   (a) Sequential: schedule a condition wake; `tightbeam cancel-wake w_…` from the
   same origin → `canceled`, `wake_condition_canceled`; a later matching fact does
   not fire it. A different origin cannot cancel it (unchanged `Wakes.cancel/3`
   origin check).
   (b) **Cancel wins the race:** with the CAS as arbiter, drive cancel to commit
   `pending → canceled` first; then run a fire pass for a matching fact. Assert the
   fire CAS finds `changes == 0`, enqueues **zero** turns, and leaves the row
   `canceled` (no queued prompt) — the r1 bug (canceled + prompt queued) cannot
   occur because the enqueue is gated on the CAS.
   (c) **Fire wins the race:** fire commits `pending → fired` + enqueue first; a
   concurrent cancel's `WHERE state='pending'` matches zero rows and no-ops. Final:
   `fired`, exactly one turn enqueued.

7d. **Cause under simultaneous condition + fallback (F3 re-probe).** A wake whose
   fallback deadline has passed AND whose fact has matched: assert exactly one fire
   with `firedBy=condition` — the in-CAS re-probe finds the fact, so cause is
   `condition` regardless of candidate-batch ordering — one lifecycle row
   (`wake_condition_fired` with the re-probed `matchedFactId`), one enqueue.

7e. **Batch overflow cannot mislabel (F3).** With `:batch` = 2 and three condition
   wakes that each both match a fact and are fallback-due, run one pass: assert at
   most `:batch` fire, each `firedBy=condition` (never `fallback`) because each
   fire's own CAS re-probes, and the scheduler self-nudges to drain the third.

7f. **Forced index-driven, work-bounded plan + zero-SQL advance (F1, acceptance
   criterion).** With many thousands of pending condition wakes but few new facts
   and few due fallbacks, `EXPLAIN QUERY PLAN` shows, on C1/C2, `SEARCH
   condition_facts USING INTEGER PRIMARY KEY (rowid>?)` as the outer driver feeding
   `SEARCH wakes USING INDEX wakes_condition` (never `SCAN wakes`), and on F `SEARCH
   wakes USING INDEX wakes_due` — holding with no `ANALYZE`/`sqlite_stat1` present.
   Assert **total per-pass work = the bounded candidate query (≤ `3·:batch` rows) +
   O(:batch) Elixir (fires + the min/max advance computed over the selected rows)
   with NO advance-time table access** — instrument that the watermark advance
   issues only `UPDATE scheduler_state SET afterFact=? WHERE id=0` (a single-row
   write), never a scan.

7g. **Doorbell fairness: condition facts fire in filing order, no same-branch
   passing-over (F2).** File facts f1 < f2 < f3 (filing order), f1 fanning out to
   more matching wakes than `:batch`. Run a pass: assert the selected condition set
   is exactly f1's oldest `:batch` wakes (fact-ordered, wakes within f1 oldest by
   rowid), NONE of f2/f3 yet, and `afterFact` holds at `f1 − 1` (f1's fan-out
   exceeded `:batch`). Next pass drains the rest of f1, then f2, then f3 — newer
   facts never overtake an unserved older fact. Separately, a fallback-branch check:
   fallback wakes fire in pure `rowid` order, oldest-first. State the scope
   honestly: this proves per-branch ordering (condition = filing order, fallback =
   rowid) + backpressure, NOT a strict global order across branches.

7h. **Unresolved fire keeps the cause (F4).** Fire a condition wake whose target
   retired between schedule and fire: assert the row is `fired`, zero turns
   enqueued, and exactly one `wake_unresolved` lifecycle row carrying
   `firedBy=condition` + `matchedFactId`/`scope`; the `firedBy` condition-vs-fallback
   ratio query (case 11) counts it, so the analytics corpus has no hole.

8. **Reserved-kind forgery denied.** A session principal calling `condition
   --kind quota-recovered` → `{code: "reserved_kind"}`, no fact filed. The
   substrate producer filing the same kind under `process:tightbeam` → filed.

9. **Flapping debounce (edge-trigger + one-shot).** Simulate `exhausted → recovered
   → recovered → recovered` observations on codex: assert the producer files
   `quota-recovered(codex:sol)` exactly once (first recovery), and a single parked
   subscription receives exactly one wake. Then `exhausted` again → `recovered` →
   a second fact is filed (new episode).

10. **Self-continuation exit (a live agent parks ITSELF).** A *live*
    assignment-holding agent (holder `H`) elects to wait — e.g. it foresees quota
    pressure, or wants a check-back before its model dies. While still able to run a
    turn, it (a) files a `progress` attest with the reason, and (b) schedules a
    condition wake `{quota-recovered, codex:sol}` fallback +30m **targeted at `H`
    itself** (`sessionKey = H`, principal `{:session, H}` → `creatorSessionKey =
    H`). Assert: `Wakes.pending_count(db, H) == 1` **and**
    `Wakes.self_pending_count(db, H) == 1`; `Supervision.evaluate` on the next
    terminal returns `:continuation`, no prod fires, the rail turn-end step is
    self-suppressed. On recovery the wake fires; `H` re-derives from the facts and
    re-adjudicates (W1). This is a legitimate exit but is **NOT** the ringdown
    parking flow (there the holder's model is dead and cannot self-schedule — see
    10c).

10b. **Owner-*targeted* re-check does NOT pause the holder (the r3 trap, guarded).**
    The re-check condition wake is targeted at the owner/spawner `O`, not `H`
    (`sessionKey = O`). Assert `Wakes.pending_count(db, H) == 0`, so
    `Supervision.evaluate` on `H`'s next terminal does NOT return `:continuation` on
    account of this wake — `H` prods/escalates as a genuine stall. This proves W7's
    target-keying invariant is load-bearing: the re-check must *target* the holder.

10c. **Owner-CREATED, holder-TARGETED parking — the ringdown flagship.** The
    holder `H`'s model is dead (it cannot run a turn to schedule anything). Its
    **owner** `O` adjudicates the park and schedules the re-check **targeted at
    `H`** on `H`'s behalf: `sessionKey = H`, principal `{:session, O}` →
    `creatorSessionKey = O`. Assert `Wakes.pending_count(db, H) == 1` — base
    `:continuation` holds, `H` is **not** a stall — while
    `Wakes.self_pending_count(db, H) == 0` (creator ≠ target: this is the owner's
    continuation of the holder, correctly not counted as the holder's own
    self-scheduling for the rail step). On recovery the wake fires into `H`, which
    re-derives and re-adjudicates (W1). This is the provable creator ≠ target
    distinction the durable column gives, and the canonical parked-block exit.

10d. **Role rebinding does not invalidate the self-scheduling proof (r4 hole,
    guarded).** `H` self-schedules a park wake while holding role `r1`; rebind `r1`
    off `H` to another session. Assert `Wakes.self_pending_count(db, H)` is still
    `1` — it reads `creatorSessionKey = H`, unaffected by the role move; an
    origin-string test (`origin = "agent:r1"`) would now wrongly read 0.

11. **Legibility query (derived, not stored).** After cases 1–10, a query over
    `lifecycle_events` reports live-subscription count, per-wake time-to-fire, and
    the fired-by-condition vs fired-by-fallback split (from `firedBy`) — with no
    stored rating column.

12. **Idempotency, both verbs (F4).** (a) Two concurrent `wake` requests with one
    `--key` schedule **exactly one** wake row (in-txn get/schedule/put); the second
    returns the first's `wake_id`. (b) Two `condition --kind X --key k` calls file
    **exactly one** fact; the second returns the first's `fact_id` and fires no
    additional subscription. Assert a subscription created between the two attempts
    is not double-fired.

13. **Non-substrate principals may file non-reserved facts (W8).** A `session`, a
    `user`, and a non-`tightbeam` `process` principal each successfully file
    `condition --kind deploy-succeeded`; a non-substrate attempt at
    `--kind quota-recovered` → `reserved_kind`, and the substrate producer files it.

14. **Multiple waiters, one fact (W10, intended).** Two parked blocks in different
    sessions each self-schedule `{quota-recovered, "codex:sol"}`. One filed fact
    fires **both** (two independent one-shot consumptions, two enqueues) — asserted
    as correct, not a non-goal violation.

---

## 12. Design note — lineage (restate the smart-wake heritage)

This primitive is the **restate-lineage smart-wake** functionality, landed
deliberately as a **fact-stream subscription** rather than as an external event
system. The earlier "smart wake" idea was "wake me when something happens out
there"; this spec realizes it as "wake me when a fact matching P is filed into
the substrate's own condition stream," where "out there" conditions the substrate
cannot see are filed by org/script producers (§9) and conditions the substrate
*can* see it files itself (§5, `quota-recovered`). The unification the S1 charter
names — parked quality-floor blocks awaiting token recovery, gates awaiting
verdict/producer facts, remedies awaiting producers, and external-event smart
wakes — is exactly the set of consumers of this one primitive: each is "a durable
one-shot wake keyed on a literal fact pattern with a timed fallback," and each
honors W1 (the woken agent re-adjudicates; the substrate never resumes). Landing
it as a fact subscription (not an external bus) keeps it inside the engine's
literal-fact doctrine, inside containment, and inside the git-backed,
restart-pickup, fail-closed operating model the rest of the substrate already
has — no new external dependency, no streaming runtime, no daemon watching the
world.

---

## 13. S1 roadmap "Done" mapping

`rails-and-guidance-roadmap.md` §S1 Done criteria:

- [ ] "wake-on-fact spec written, reviewed, implemented; a parked block exits via
  condition subscription (timed fallback remains available)." → **spec: this
  document.** Implemented = §10 seam green; parked-block exit = acceptance case
  **10c** (owner-created, the ringdown parking flow; case 10 is the self-created
  continuation variant); timed fallback = W5 / case 4.
- [ ] "`quota-recovered` filed by the substrate on observed recovery; a subscribed
  wake delivers; the woken agent re-adjudicates rather than auto-resuming." →
  producer §5/§D; delivery cases 1 & 10c; re-adjudication W1 / case 10c's final
  assertion.

Depends on: KP1 / `model-ringdown-pattern.md` GAP 1 (classification) and bounded
by GAP 7 (no leading quota gauge) for the `quota-recovered` producer; the
primitive itself (§3, §4, §9) is independent and lands first.
