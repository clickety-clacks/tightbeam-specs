# Escalation substrate v1 — the `escalate` gate outcome, decision-requests, rulings, waivers

Status: RATIFIED to Flynn's ruled model (2026-07-21), r7 — applies Sol spec-review
blockers r1–r5 (F1–F11), the r6 four-shape-union / tagged-raiserId / waiver-scope /
open-race set, and the Lattice round (digest effect-neutral exclusion, pinned deadline
config home, verb-edge-only consume). This ratification unblocks the `escalate` effect
that `rails-mechanism-v1.md` defines-but-holds-unreachable (§A1/X4). Cross-model
adversarial spec-review continues; no build precedes it landing clean.

Authority: this spec is the sole authority for the `escalate` dispatch outcome,
the decision-request record, the ruling and waiver verbs and their facts, and the
way a raiser waits on a ruling. Parents govern where this spec is silent:
`rails-mechanism-v1.md` (the `escalate` effect token, `Rules.decide`'s
`{:escalate, statute, ctx, dr_id}` decision, the two actors that may enact it, and the
`{:acted, :rail_escalate}` sweep branch), `wake-on-fact-v1.md` (the condition-wake
primitive this spec's wait is built from — the `condition_facts` stream, the
`{kind, scope}` literal match, the mandatory finite fallback W5, the
target-keyed/`creatorSessionKey` supervision reads W7, and the reserved-kind
boundary W8), and `supervision-v1.md` + `lib/tightbeam/supervision.ex` (the
`Wakes.pending_count → :continuation` read that makes a parked raiser
not-a-stall).

Ground-truth read on `main`: `lib/tightbeam/supervision.ex`
(`evaluate_terminal`'s `with 0 <- Wakes.pending_count(db, session_key)` guard at
:185 and its else-branch `:continuation` at :206; `notify_retired` →
`doorbells_for_holder` at :167/:481; `ladder_target/3` + `Org.personal_session_key`
terminus at :109/:117), `lib/tightbeam/wakes.ex` (`pending_count/2` keyed on target
`sessionKey` :173-182; `schedule/2`; `cancel/3`), and `wake-on-fact-v1.md` §3/§4
(`condition_facts`, `ConditionFacts.file`, the `@reserved_kinds` constant).

---

## 0. The model in one paragraph (read first)

An escalation is a **slow dependency inside the raising agent's own assignment**,
identical in kind to waiting on a subagent. When a statute evaluates `escalate`
for a gated call, the substrate **halts that one call without executing it**, opens
a **decision-request** (the neutral record of the pending decision), delivers it to
the accountable owner, and returns `{:decision_pending, id}` to the raiser. The
raiser **does not die and is not re-dispatched.** It **parks**: it schedules a
self-targeted condition wake on the ruling fact for that request (the
`wake-on-fact-v1.md` primitive) and ends its turn. When the owner **rules**, the
ruling is recorded on the decision-request and a `escalation-ruled` fact is filed to
the condition stream; that fact fires the raiser's wake. The raiser **resumes**,
re-derives from the durable facts, and **re-issues the halted action itself** — the
substrate NEVER auto-replays a stored verb. On re-issue the gate consults the
recorded ruling and lets the action through (or refuses it). There is **no
blocked-on-owner state and no flag anywhere**: the open decision-request, the
waiting assignment, and the raiser's pending condition wake are the entire
legibility surface, all already observable, and supervision reads the pending wake
as continuation-not-stall by the mechanism it already has.

---

## 1. Invariants (the acceptance lens)

**E1 — EXECUTE-ONCE, AND A RULING IS A CONSUMABLE AUTHORIZATION.** When a statute
escalates a call, the gated verb **does not run**. The substrate stores the call's
*context* (verb + args snapshot) on the decision-request **for the owner to judge,
never to execute** — no substrate auto-retry, no stored-verb replay, no
default-approve. A ruled-`allow` authorizes exactly **one attempt**: the **engine
never consumes** — it returns `:allow` effect-free; the **actor** consumes, by a
standalone CAS `ruled → consumed` run **immediately before invoking the handler**
(CAS-win = the sole authorization to invoke; §2/§9/F1), so a subsequent identical
call opens a **fresh** request rather than riding the spent ruling. Consumed on
**attempt, not success**: a handler that then fails has spent its authorization and a
retry re-escalates (deliberate fail-closed). The **waiver** (§7) is the deliberately
**non-consumable** form — that is its whole purpose: while a waiver lives, repeated
identical actions all pass without re-escalating. Per-request ruling = one authorized
attempt; waiver = standing authorization for the session's life (F1).

**E2 — DELIVERY IS NOT RESUMPTION (inherited from `wake-on-fact-v1` W1).** Neither
delivery does any resuming. Delivering the decision-request to the owner delivers a
prompt to decide; it resumes nothing. The ruling fact firing the raiser's wake
delivers a prompt to the raiser; it does not restore state, un-halt the call, or
re-decide anything. The woken raiser **re-adjudicates from the durable facts** (the
decision-request status, its own assignment, the catalog) and re-issues afresh.

**E3 — NO NEW STATE, NO FLAG.** There is no `blocked-on-owner` state, boolean, or
work-item condition anywhere in the substrate. A raiser awaiting a ruling is
legible entirely through rows that already exist for other reasons: the **open
decision-request**, the **still-open assignment**, and the **pending self-targeted
condition wake**. Supervision needs **zero change** — the pending wake makes
`Wakes.pending_count(db, raiser) > 0`, which the existing `evaluate_terminal`
short-circuits to `:continuation` (`supervision.ex:185` → `:206`).

**E4 — NEVER SILENT.** Every edge is a row. Opening a decision-request, ruling it,
waiving a statute, revoking a waiver, and withdrawing a request each emit exactly
one `lifecycle_events` row (§10). A decision-request is never opened, resolved, or
retired without a legible record, and a request is never abandoned silently — a
withdrawal always names its reason (§8).

**E5 — A WAIVER IS RAISER-SCOPED; ITS LIFETIME DEPENDS ON THE RAISER KIND (F3).** A
waiver is never global — it is scoped to a single `raiserId` (§3). A **session**
raiser's waiver **dies with the session**: it is consulted only while that session is
active, and is swept-by-revoke at retirement (§8). A **non-session** raiser's waiver
(raiserId = an `agent:`/`user:` origin string) has **no session to die with**, so it
persists **until explicit revoke**. Either way a waiver is prospective-revocable
(§7) and never outlives its stated scope.

**E6 — ACCOUNTABILITY REQUIRES IDENTITY (kept).** A **ruling** and a **waiver** may
be produced ONLY by a principal the **existing admin axis** admits —
`admin_origin?`/`resolve_caller`, the same gate that guards `skill-put` (F3) — never
a bare non-admin `process:`, and never the raiser. A **withdrawal** may be produced
ONLY by the raiser that raised the request (its `raiserId`, F3) **or by the
substrate (`process:tightbeam`) on raiser death** (§8, auto-withdrawal); never
owner-only, never an arbitrary third party. Every ruling, waiver, and withdrawal is
provenance-stamped with the acting principal.

**E7 — WHO PARKS DEPENDS ON THE EDGE (the two-edge split, F4).**
- **Verb edge (a live raiser).** The wait is the raiser's OWN continuation, built
  from the general `wake-on-fact-v1` self-continuation exit (its case 10), not
  bespoke escalation machinery. The substrate does not schedule the wait and does
  not choose its fallback (fallback is product/agent policy, `wake-on-fact-v1` W5).
  The escalate outcome is exactly: halt, pre-check waiver/ruling, open-or-return the
  decision-request, deliver it to the owner, return `{:decision_pending, id}`; the
  raiser then self-parks (§4).
- **Turn-end edge (the sweep; the holder cannot self-schedule).** When escalate
  fires from `Supervision.evaluate/5`'s turn-end sweep, the holder is at a terminal,
  not running a turn, and cannot schedule anything — so the **sweep parks the
  holder**: a **substrate-created, holder-targeted** condition wake (the
  `wake-on-fact-v1` W7 owner-parks/ringdown precedent — not-a-stall is
  **target-keyed**, so a substrate-created wake with `creatorSessionKey = nil`
  targeting the holder still reads `:continuation`). Its fallback `dueAt` is the
  decision-request's **`deadlineAt`** (§3) — an org-configurable owner-decision
  deadline carried on the DR, **not** a supervision prod cadence (supervision prods
  fire at `after_ms: 0`, `supervision.ex:370` — there is no resident deadline clock;
  F4). The park is **idempotent** via the DR's stored `parkWakeId` (§4): a sweep over
  an already-parked open DR re-returns it and never double-parks.

**E8 — A RULED ROW IS ONE COMPLETE FACT (Mike, 2026-08-30).** A
decision-request with `status = ruled` carries a nonblank text `decision`, a nonblank
text `ruledBy`, and an integer `ruledAt`. The transition CAS writes all four members
in one statement. The table itself rejects a future partial ruled row. A reader that
encounters corruption despite that boundary refuses the request or whole response; it
does not render `ruled` with missing detail. A migration never invents a decision,
ruler, or time: it either moves a legacy row through a separately specified repair
transition or stops the upgrade with a remedy that identifies the broken row. Rationale
remains optional.

---

## 2. The `escalate` outcome at the gate — resolve (read), escalate (effect), consume (actor)

`rails-mechanism-v1.md` §B/§D2 pins the seam, and this engine matches it exactly:
the escalate statute is folded like any other, and the work splits into **one pure
read inside the fold** and **two effects owned by the actor** (`Dispatch.dispatch/3`
at the verb edge, `Supervision.evaluate/5` at the turn-end sweep). Every other caller
uses the collapsing `Rules.evaluate` wrapper, where `{:escalate,…}` becomes a plain
deny without firing (rails §B2). The **raiser identity is derived from
`call.principal`, never `call.session_key`** (ground truth: `session_key` is the
delivery *target*, not the actor; F3): at the verb edge the principal is the caller
session; at the turn-end edge the sweep's pseudo-call carries the **holder**
principal.

**(1) `Escalation.resolve(db, call, statute)`** — the **effect-free** resolution
`Rules.decide` reads while folding (rails FRESH-1). A pure read: it consults the
waiver table and the current ruling for this action (§9), **opens nothing, consumes
nothing, fires nothing.** Its **public decision union is FOUR shapes** (F1 — a bare
atom cannot carry a ruling id, so the consumable allow is its own shape): **`:allow |
{:allow, ruling_id} | {:deny, e} | {:needs_request, dr_id|nil}`:**
- `:allow` — **waiver-sourced** (an active waiver). Nothing to consume. The statute
  **passes and the fold continues** over later statutes (an escalate allow never
  short-circuits past a later `deny`/`remedy`/escalate).
- `{:allow, ruling_id}` — **ruling-sourced** (a prior `ruled`-allow for this exact
  action). `decide` collects `ruling_id` into the fold's `to_consume`; the actor
  CAS-consumes it (§9.3). The statute **passes and the fold continues** exactly as a
  bare `:allow`.
- `{:deny, error}` — a prior `ruled`-deny for this action. First non-`allow` wins;
  `decide` stops and returns it.
- `{:needs_request, dr_id | nil}` — no active waiver and no consumable ruling.
  `decide` returns `{:escalate, statute, ctx, dr_id}` (carrying the `dr_id` through,
  rails :414-420) and stops; the actor branches on `dr_id`: **non-nil** = an existing
  OPEN request for this exact action (re-return it, open nothing); **nil** = nothing
  open (open a fresh request). This one member subsumes the former `:already_open`
  atom, which no longer exists.

**(2) `Escalation.escalate(db, call, statute, ctx) → {:decision_pending, id}`** — the
**effect** the actor runs on a whole-fold `{:escalate, statute, ctx, dr_id}` with
`dr_id == nil`: it opens the request (§9), emits its lifecycle row, and returns; owner
delivery (§6) is **post-commit**. On `dr_id` **non-nil** the actor re-returns
`{:decision_pending, dr_id}` itself and never calls `escalate/4` (no duplicate open).
The gated verb **does not run** (E1). `ctx` carries the statute's owner-facing
`question` and optional enumerated `options`.

**(3) The consume batch — the VERB EDGE's authorization step, verb-edge-only (F1 +
Lattice).** **Consumption happens ONLY at the verb edge** (`Dispatch.dispatch/3`),
where a handler is actually about to run — never at the turn-end sweep, which has **no
handler to authorize**, so consuming there would spend a ruling with **zero
execution** (mirrored from rails, which owns the verb-edge-only rule). When the **whole
fold passes** (every statute yielded `:allow` or `{:allow, ruling_id}`), the fold has
already resolved each escalate statute and collected `to_consume` = the **ruling row
`id`s** the `{:allow, ruling_id}` shapes carried (rails' form — no re-resolution). Then
**immediately before invoking the handler** the actor calls
**`Escalation.consume(db, ruling_id)`** for **each** entry: a single-statement CAS
`UPDATE decision_requests SET status='consumed', consumedAt=? WHERE id=ruling_id AND
status='ruled'`. **The engine never consumes; only the actor does** (rails FRESH-1); no
wrapping transaction (rails whole-fold rule). **Batch rule (fail-closed):** the actor
CASes every entry; **if ANY loses, the verb is DENIED** and the entries that already won
**STAY consumed** — consumed-on-**attempt** covers the batch (the attempt spent them; a
re-issue re-escalates each vanished authorization, §9.3).

**A waiver-sourced allow has no row to consume, and there is NO consume-time
revalidation — deliberately.** A waiver `:allow` contributes no `to_consume` entry, so
the actor does **not** re-check the waiver between fold and handler. This is the
correct consequence of **prospective-only revocation (F6):** a call already in the fold
when a `revoke-waiver` lands **proceeds** — the revoke governs only *future* calls.
Re-validating the waiver at consume time would wrongly retro-deny an in-flight call;
rails' no-recheck behavior is right. **Consumed-on-attempt, not on-success:** a handler
that then fails or crashes has **spent** its authorizations — a retry finds them
`consumed` and **re-escalates**. One owner ruling authorizes exactly one attempt.

The turn-end sweep (`Supervision.evaluate/5`) runs the identical **resolve** split but
**never consumes** (it has no handler — verb-edge-only, above): a
`{:allow, ruling_id}` at the sweep means the obligation is already satisfied, so the
sweep treats it as met and **leaves the ruling `ruled`** for the verb edge to consume
when the agent actually re-issues. On `:needs_request` it returns `{:acted,
:rail_escalate}` (rails §D2.4) and, on the effect, **parks the holder itself** (E7
turn-end edge, §4): it schedules a substrate-created, holder-targeted `{escalation-ruled,
id}` wake whose fallback `dueAt = deadlineAt` (§3), so the holder reads `:continuation`
without self-scheduling. A turn-end-edged `escalate` is now
**reachable** — X4's load-error guard lifts on this spec's review landing clean (rails
gates `escalate`-statute loading on review-clean, not ratification; §11).

**Naming disambiguation.** The caller-facing tag is `{:decision_pending, id}`,
deliberately distinct from supervision's own ladder return `{:escalated, rung,
target}` (`supervision.ex:127`), which is stall-escalation to a *spawner* and is an
unrelated concept. "Escalate" here always means "a decision belongs to the owner,"
never "a stall climbs the supervision ladder."

---

## 3. The `decision_requests` table (record shape, reconciled)

The decision-request is the substrate's durable governance record of one pending
decision — the neutral truth "this action needs the owner." It carries no derived
state a client caches and no work-item state (E3). Additive table:

```sql
-- an ordinary rowid table (NOT 'WITHOUT ROWID'): the implicit rowid is the recency cursor (F5-FRESH)
CREATE TABLE IF NOT EXISTS decision_requests (
  id                TEXT PRIMARY KEY,           -- generated request id (identity, NOT recency ordering)
  raiserId          TEXT NOT NULL,              -- CANONICAL raiser identity, domain-tagged: "session:"<>key for a session, else the origin string verbatim (F2/F3)
  raiserSessionKey  TEXT,                        -- park TARGET only: the session key when the raiser is a session; NULL otherwise (F3)
  ownerUserId       TEXT NOT NULL,              -- accountable owner (routing + queue surface)
  assignmentId      TEXT,                        -- the open assignment this action serves (owner context)
  raisedAt          INTEGER NOT NULL,
  deadlineAt        INTEGER NOT NULL,           -- owner-decision deadline; the park wake's fallback dueAt (F4; config seam §11)
  statuteName       TEXT NOT NULL,              -- which rail escalated (waiver + tuning key)
  actionKey         TEXT NOT NULL,              -- substrate digest of the gated call (re-issue match, §9)
  question          TEXT NOT NULL,              -- the rail's owner-facing prompt (from ctx)
  options           TEXT,                        -- enumerated choices, JSON: each {label, effect ∈ 'allow'|'deny'} (F10)
  context           TEXT NOT NULL,              -- halted verb + args snapshot, for the owner to JUDGE (E1)
  status            TEXT NOT NULL CHECK (status IN ('open','ruled','consumed','withdrawn')),
  decision          TEXT CHECK (decision IN ('allow','deny','waived')),  -- closed domain (F10; 'answer' descoped)
  rationale         TEXT,
  ruledBy           TEXT,                        -- owner principal (E6)
  ruledAt           INTEGER,
  rulingFactId      INTEGER,                     -- the escalation-ruled condition_facts row (§5)
  consumedAt        INTEGER,                     -- when the actor spent the ruled-allow authorization (F1)
  parkWakeId        TEXT,                        -- the sweep's substrate-created park wake, for idempotent re-park (F4)
  withdrawnBy       TEXT,
  withdrawnReason   TEXT,
  withdrawnAt       INTEGER
);
CREATE INDEX IF NOT EXISTS decision_requests_owner  ON decision_requests (ownerUserId, status);
CREATE INDEX IF NOT EXISTS decision_requests_key    ON decision_requests (raiserId, statuteName, actionKey);
-- at most ONE open request per (raiserId, statuteName, actionKey): arbitrates concurrent opens (F5)
CREATE UNIQUE INDEX IF NOT EXISTS decision_requests_one_open
  ON decision_requests (raiserId, statuteName, actionKey) WHERE status = 'open';
```

- **`actionKey`** is a substrate-canonical fingerprint of the gated call, computed by
  the substrate (never by the statute — the statute decides only *whether* to
  escalate, never the request's identity). **Normalization (decision-complete, F2):**
  build a canonical JSON object of the call's params with **string keys sorted
  lexicographically**, **nil-valued keys dropped**, and the **EFFECT-NEUTRAL params
  excluded** — the idempotency/`--key` param (wire-dedup) **and annotation params that
  do not change the action's effect, explicitly `note`** (the optional attest annotation
  at `assignments.ex:370/417`). The exclusion is load-bearing: the turn-end sweep
  synthesizes a bare `{assignment_id, kind}` call, but a real re-issued `attest` may
  carry a `note` — if `note` fed the digest, the two `actionKey`s would differ, the
  ruling would never match the re-issue, and the owner would be pinged forever. Then
  `assignmentId` is extracted per the `rules.ex` precedent and included as a **distinct**
  field alongside `verb`; `actionKey = sha256(canonical_bytes)`. The *same* action
  re-issued yields the same key and matches its ruling (§9); a *different* action (the
  raiser re-adjudicated and
  changed course, E2) yields a different key and correctly opens a fresh request.
- **`context`** is the halted call snapshot, present **only** so the owner can judge;
  the substrate never reads it to execute (E1).
- **`raiserId` is the CANONICAL raiser identity (F3): NOT NULL, and DOMAIN-TAGGED to
  avoid collision (F2).** It is **`"session:" <> sessionKey`** for a session principal,
  and the **origin string verbatim** otherwise (a non-session principal — an org token
  acting `--as <role>` — whose origin is already tagged `agent:`/`user:`). The two
  namespaces cannot collide by construction (a session key never begins `agent:`/`user:`
  and an origin never begins `session:`). **All** operations key on it uniformly: the
  current-request lookup (§9), withdrawal authorization (the withdrawing call's canonical
  identity must equal `raiserId`, §8), read visibility (§6), and the `escalation_waivers`
  key (§7). It replaces r1's `raisedBy` for every non-provenance use.
- **`raiserSessionKey` is the NULLABLE park-target column ONLY (F3).** Parking is a
  **session privilege**: only a session raiser has somewhere to park (a wake targets a
  session), so `raiserSessionKey` = the session key for a session raiser, `NULL` for a
  non-session raiser. A non-session raiser gets **no park** — it receives
  `{:decision_pending, id}` synchronously and re-issues later on its own initiative
  (§4). Auto-withdrawal-on-death (§8) scopes to session raisers only (a `NULL`
  `raiserSessionKey` has no session lifetime to end); non-session waivers likewise have
  **no death sweep** — their scope is until-revoke (§7).
- **`deadlineAt`** is the owner-decision deadline (config seam §11); the park wake's
  fallback `dueAt` is set to it, and any owner re-prod rides the same clock (F4). It
  replaces the non-existent "prod cadence."
- **`parkWakeId`** records the sweep's substrate-created park wake so the turn-end
  re-park is idempotent (recreate only if absent — the adjudication-episode pattern,
  F4); it is unused at the verb edge (the raiser owns its own wake).
- **Recency is the implicit `rowid` (F5-FRESH).** The `TEXT PRIMARY KEY` `id` is
  identity, not order; `decision_requests` is an ordinary rowid table, and the "current
  request" for a key is `ORDER BY rowid DESC LIMIT 1` (§9), so a later escalation of the
  same shape supersedes an earlier resolved one.
- A thin doorbell grain `decision_request_event` (subject `id`) mirrors
  observability's pattern for the owner surface (§6). The table never carries derived
  state.

Superseded from r1: the `workItemId` field and the `blocked-on-owner` work-item
condition are **removed** (E3). The `rulingFactId` now points at a `condition_facts`
row (§5), not an attest.

---

## 4. The raiser's parked wait (the resume model)

On receiving `{:decision_pending, id}` a **session** raiser parks by the ordinary
`wake-on-fact-v1` self-continuation exit (its case 10), with **no bespoke
machinery** (a non-session raiser does not park — §3/F3 — it re-issues later on its
own initiative):

```
tightbeam wake --session <raiser> \
  --when-fact escalation-ruled --when-scope <decisionRequestId> \
  --fallback-after <T> \
  --prompt "Decision <id> pending on <statute>. When ruled, re-derive and re-issue the halted action."
```

- **Self-targeted, self-created.** The wake's `sessionKey = raiser` and its
  `creatorSessionKey = raiser` (the raiser is alive at the gate and schedules it on
  its own turn, principal `{:session, raiser}`). By `wake-on-fact-v1` W7/§4.2 this
  makes `Wakes.pending_count(db, raiser) > 0` **and**
  `Wakes.self_pending_count(db, raiser) > 0` — so supervision's base guard reads
  `:continuation` (E3) and the rail turn-end step (when `rails-mechanism-v1` lands)
  self-suppresses. No supervision code changes.
- **No supervision race.** Supervision evaluates only at turn-terminal; the raiser
  schedules the wake *before* ending the turn that received `{:decision_pending, id}`,
  so at terminal the wake is already pending. A raiser that escalated but did **not**
  park has genuinely left work with nothing on the clock and correctly reads as a
  stall — supervision prods it to schedule its continuation (the invariant self-heals;
  the substrate adds nothing).
- **The decision-request and the wake are distinct rows, deliberately** — exactly the
  `wake-on-fact-v1` §E "block record vs recovery condition" separation. The substrate
  stores no link between them; the raiser owns its wake (it holds the `wakeId` and may
  cancel it, §8).

### The park protocol — SCHEDULE-THEN-CHECK (normative, F5)

The ruling fact and the wake subscription race across the no-replay cursor: a
condition wake matches only facts filed **strictly after** it is scheduled
(`wake-on-fact-v1` W4, the `conditionAfterId` cursor). If the owner rules in the
window between the raiser receiving `{:decision_pending, id}` and scheduling its
wake, a naive check-then-schedule loses the ruling — the fact is already filed, the
later wake's cursor excludes it, and the raiser waits out its whole fallback for a
decision that already exists. The **mandatory order closes both gaps**:

1. **SCHEDULE** the `{escalation-ruled, id}` wake first. This pins the cursor
   (`conditionAfterId` = the max `condition_facts.id` at schedule time).
2. **THEN CHECK** the decision-request status (a read strictly after step 1):
   - `ruled` / `consumed` / `withdrawn` (already resolved — the ruling landed before
     the cursor, so the wake will never fire on it) → **cancel the wake** and act now
     (re-issue for a ruling, re-adjudicate for a withdrawal). This closes the
     ruled-before-schedule gap.
   - `open` → the wake is armed; a ruling filed **after** the cursor fires it (the
     ruled-after-schedule case). Idempotent overlap is benign: a ruling that lands in
     the gap between step 1 and step 2 is caught by **both** — the check cancels+acts,
     and if the wake already fired, the redundant delivery re-adjudicates against the
     `consumed`/`ruled` status and no-ops.

The turn-end sweep's substrate-created park (E7) runs the same order inside its
scheduling transaction: schedule the holder-targeted wake, then re-read status.

### The long-wait loop (mandatory finite fallback + re-subscribe)

`wake-on-fact-v1` W5 mandates a finite `dueAt` (the `wakes.dueAt NOT NULL` storage
limitation), so an owner who is slow to rule will hit the fallback before the ruling
arrives. The loop, spelled out and legible:

1. **Ruling arrives first (normal).** The `escalation-ruled/<id>` fact fires the
   wake (`wake_condition_fired`). The raiser resumes, re-issues the action; the gate
   applies the ruling (§9).
2. **Fallback fires first (owner still deciding).** The wake fires by deadline
   (`wake_fallback_fired`), delivering the raiser's own re-check prompt. The raiser
   **re-checks the decision-request status**:
   - `open` → **re-subscribe**: schedule a fresh `escalation-ruled/<id>` condition
     wake with a new finite fallback, and end the turn parked again. This iteration is
     itself a continuation (a fresh pending self-wake), so the raiser never reads as a
     stall across an arbitrarily long wait; each fallback fire is one legible
     `wake_fallback_fired` row plus one re-schedule.
   - `ruled` → re-issue the action (the ruling fact was raced past; the durable status
     is authority, E2). The re-issue consumes it (`ruled → consumed`, §9).
   - `consumed` → already acted on a prior pass; no re-issue.
   - `withdrawn` → the raiser withdrew earlier and has already moved on; no re-issue.

This is the explicit "finite fallback + re-subscribe" long-wait pattern. The session
raiser's own fallback is its choosing (E7 verb edge); the DR's `deadlineAt` (§3) is
the substrate-carried clock the **turn-end** park and any owner re-prod ride (F4). The
owner learns of the pending decision once (§6) and it stays on the owner's open queue
until ruled/waived/withdrawn; no owner re-prod *loop* is mandated in v1 — a future org
policy may re-deliver on the `deadlineAt` cadence, out of scope for this engine.

---

## 5. The ruling — the `rule` verb and the `escalation-ruled` fact

The owner resolves a decision-request with a new `rule` verb (added to the agent
verb allowlist). In **one transaction** it (a) checks accountability (E6), (b)
resolves the request, and (c) files the ruling fact that fires the raiser's wake:

```
tightbeam rule --request <id> --decision <allow|deny|option> [--rationale "…"]
```

1. **Accountability (E6/F3).** `call.principal` must pass the **existing admin axis**
   (`admin_origin?`/`resolve_caller`, the same gate as `skill-put`). A non-admin
   `process:`, or the raiser, is rejected `not_owner`.
2. **Closed decision domain (F10).** `--decision` is `allow | deny`, or an
   **enumerated option label** from the request's `options` (which resolves to that
   option's declared `allow|deny` effect) — the v1 escalation engine gates **actions**
   only. **Re-rule (F10):** re-`rule` of an already-resolved request with the **same**
   decision is an idempotent no-op returning the prior ruling; a **different** decision
   is rejected `not_open`.
3. **Resolve.** `status open → ruled` (CAS on `status='open'`, §8 race rule); record
   `decision`, `rationale`, `ruledBy`, `ruledAt`.
4. **File the ruling fact IN-TRANSACTION (F7).** `ConditionFacts.file_in_txn(txn,
   %{kind: "escalation-ruled", scope: <id>, origin: "process:tightbeam"})` — the
   substrate producer path (`wake-on-fact-v1` §5/§6, the in-transaction writer that
   spec provides), never the public `condition` verb; record its row id as
   `rulingFactId`. A **single post-commit scheduler nudge** (`Wakes.fire_matching`,
   not inside the txn) then lets the raiser's `{escalation-ruled, <id>}` wake fire.
5. **Legibility.** One `decision_request_ruled` lifecycle row, bound in the same
   transaction (`EventLog.lifecycle_in_txn/4`, `wake-on-fact-v1` §6).

**`escalation-ruled` is a substrate-reserved condition kind** (it joins
`@reserved_kinds`, currently `{quota-recovered}`). This is not a defensive add: a
ruling is **substrate-observed governance truth**, and `wake-on-fact-v1` W8's own
principle — "the substrate owns the facts it observes; everyone else may file the
facts they observe" — puts it on the substrate's side of the boundary. The reserved
kind means the public `condition` verb rejects any non-`tightbeam` principal filing
`escalation-ruled`, so a ruling fact cannot be forged to spuriously wake a raiser.
The condition fact is a **doorbell only** — it carries no decision payload (W3: only
`{kind, scope}` are matchable). The **authoritative** ruling is the
`decision_requests` row, which the woken raiser re-reads and which only `rule`
writes (E2/E6). **Coupling to report:** this extends `wake-on-fact-v1`'s reserved-kind
constant by one; see §11.

There is **no ruling attest kind** (r1's `attest kind = "ruling"` is superseded): an
attest is FK-bound to an assignment and CHECK-locked to
`{progress,completion,surrender,verdict}` (`wake-on-fact-v1` §A), which a ruling is
not. Provenance lives on the `decision_requests` row (`ruledBy`/`ruledAt`/`decision`/
`rationale`) plus the `condition_facts` origin and the lifecycle row — three legible,
append-only records, no attest overload.

### 5a. Ruled-decision integrity boundary (Mike, 2026-08-30)

The decision-request table owns E8 for every kind that can become `ruled`. Its exact
database predicate rejects a null, empty, or ASCII-whitespace-only `decision` or
`ruledBy`, and rejects a non-integer or null `ruledAt`. The normal verb edge
normalizes text before its open-row CAS; this predicate is the final write-time
boundary, not a second policy decision.

The canonical readers — direct detail, lists, REST, and firehose serialization — check
the same complete-fact shape before they project a ruled row. A corrupt row yields the
named `decision_request_integrity_invalid` refusal and no partial ruled item. Existing
operator rows also retain their deeper provenance, condition-fact, lifecycle, and wake
audit checks.

The one stamped upgrade from the prior decision-request shape preflights every ruled
row before it rebuilds the table. A row that lacks any E8 field makes that upgrade fail
with `incompatible_ruled_decision_integrity_v1` and a repair message containing its
request id. This is the selected legacy remedy: no migration writes a made-up decision,
ruler, timestamp, or status transition. A repaired source database can retry the
upgrade; until then the new build refuses that database rather than exposing its
partial ruling.

Acceptance:

- A direct ruled write with a blank, whitespace-only, or absent decision/ruler, or an
  absent/non-integer time, fails the table constraint.
- A valid direct or session-mediated ruling still projects unchanged through CLI, REST,
  and firehose; retry and competing terminal CAS behavior remain unchanged.
- A deliberately corrupted ruled row is refused by list, detail, replay, REST, and
  firehose before any ruled payload is emitted.
- A legacy incomplete ruled row fails the stamped upgrade with the named remedy; a
  valid legacy ruling migrates and preserves its original raise time and audit links.

---

## 6. What the owner sees — delivery and the queue surface

Two things happen for the owner when a request opens, both from the escalate outcome
(§2), neither a supervision-ladder stall (the raiser is not stalled, E3):

- **One-shot delivery, POST-COMMIT (kept from r1; F7/F9).** After the open-request
  transaction commits, the engine delivers the decision-request to the owner as a
  prompt carrying `question`, `options`, and enough of `context` to judge, origin
  `process:tightbeam`. Delivery reuses the **existing wake-to-user delivery path**
  (the same seam a timed wake or a user post uses to reach a user's session), **not**
  ad-hoc `personal_session_key` string formatting — the engine hands the owner
  `ownerUserId` + prompt to that path and lets it resolve the target. Delivery is
  never inside the request-open transaction (F7). This is addressed correspondence
  (the comms-clock model), delivered once; it resumes nothing (E2).
- **The queue surface.** Open requests for an owner are the read verb below, with a
  `decision_request_event` doorbell on open/resolve — mirroring observability's
  random-access-plus-doorbell pattern. This is the durable surface the owner returns
  to; if the one-shot delivery is missed, the request is still on the queue until
  ruled, waived, or withdrawn.

### Read surfaces — the `decision-requests` and `decision-request` verbs (F9)

Two read-only verbs (added to the agent verb allowlist) expose the queue; neither
mutates:

```
tightbeam decision-requests [--status open]      # the queue: rows the caller may see
tightbeam decision-request <id>                  # one request, full projection
```

- **Visibility.** An **admin/owner** principal sees all requests for its
  `ownerUserId` (default `--status open`, filterable). A **raiser** principal sees
  **only its own** requests (`raiserId` = the caller's canonical identity, F3). Any
  other principal sees none.
- **Row projection:** `id`, `status`, `statuteName`, `question`, `options`, `raiserId`,
  `raiserSessionKey`, `assignmentId`, `raisedAt`, `deadlineAt`, and — when resolved —
  `decision`, `rationale`, `ruledBy`, `ruledAt` (or `withdrawnReason`, `withdrawnAt`).
  The `context` snapshot is included only in the single-request projection
  (`decision-request <id>`), for the owner to judge; it is elided from the list.
  Visibility keys on `raiserId` (F3): a raiser sees rows whose `raiserId` = its own
  canonical identity.

The owner acts by `rule` (§5), or `waive` (§7) to clear a whole class, or does
nothing (the raiser keeps waiting on its fallback-loop, §4).

---

## 7. Waivers — "ignore that rule for now" (the second ruling form, Q3)

A ruling (§5) resolves **one request**. A **waiver** is the standing form the ruled
model adds so the operator is never forced to context-switch into governance work to
unblock: it says "for this raiser, ignore that statute for now." It keys on the
canonical `raiserId` (F3). Additive table:

```sql
CREATE TABLE IF NOT EXISTS escalation_waivers (
  id                TEXT PRIMARY KEY,
  raiserId          TEXT NOT NULL,     -- the raiser the waiver applies to, domain-tagged: "session:"<>key or origin string (F2/F3)
  statuteName       TEXT NOT NULL,     -- the waived statute
  grantedBy         TEXT NOT NULL,     -- owner principal (E6)
  grantedAt         INTEGER NOT NULL,
  reason            TEXT,
  revokedBy         TEXT,
  revokedAt         INTEGER
);
CREATE INDEX IF NOT EXISTS escalation_waivers_lookup
  ON escalation_waivers (raiserId, statuteName, revokedAt);
```

**Grant** — a new `waive` verb, admin-axis-only (E6/F3):

```
tightbeam waive --request <id> [--reason "…"]          # queue-driven: derives raiserId + statute from the request
tightbeam waive --session <key> --statute <name> [--reason "…"]   # pre-emptive form (raiserId = "session:"<>key)
```

The `--request` form (the ergonomic, queue-driven path) **derives `raiserId` from the
request (never inserts NULL, F3)** and does everything in **one transaction (F6):**
(a) insert the waiver keyed on the request's `raiserId` + `statuteName`; (b) **resolve
every currently-OPEN request** matching that `(raiserId, statuteName)` — not only the
triggering one — as `ruled` with `decision='waived'`, filing an
`escalation-ruled/<reqId>` doorbell for **each** via `ConditionFacts.file_in_txn` (F7)
so every parked raiser wake fires; (c) emit one `waiver_granted` lifecycle row plus one
`decision_request_ruled` per resolved request. A **single post-commit scheduler nudge**
(whose eager pass fires the newest fact's wake; the other resolved requests' wakes fire on
the next scheduler tick via the watermark pass — CAS-guarded, none lost, ≤1 tick of added
latency; this is the intended shape, not a defect)
follows the commit. The pre-emptive `--session`/`--statute` form does (a) + the
`waiver_granted` row only (no open request to resolve yet).

**Gate consultation (§9).** At escalate evaluation for raiser `R` (the canonical
`raiserId`) and statute `X`, the engine first queries `escalation_waivers WHERE
raiserId = R AND statuteName = X AND revokedAt IS NULL`. A live matching waiver → the
engine returns `:allow` (the statute's escalate is ignored; the action passes) —
**non-consumable**, so every subsequent identical action also passes while the waiver
lives (E1). A **session** raiser's waiver **auto-expires on session death** (E5,
swept-by-revoke on retirement, §8) — a retired session never dispatches. A
**non-session** raiser's waiver (raiserId = an origin string, no session lifetime) has
**no death sweep**: its scope is **until explicit revoke** (F3).

**Revoke** — a new `revoke-waiver` verb, admin-axis-only; **prospective only (F6)**:

```
tightbeam revoke-waiver --waiver <waiverId> [--reason "…"]
```

Sets `revokedBy`/`revokedAt`; emits `waiver_revoked`. After revoke, **future** calls
under `X` re-escalate; requests **already resolved `waived`** stay historically
`waived` — a revoke never rewrites past resolutions.

**Self-tuning datapoints — two distinct signals, neither claimed as the other (F6).**
Every waiver emits its legibility rows (E4) so the tuning loop can derive rates
without stored ratings (observability doctrine). But the two grant paths are
**different signals** and `self-tuning-rails-core-FUTURE.md` §6g must read them apart:
- a **request-triggered** waiver (`--request`) is a **denied-then-overridden**
  datapoint — the rail actually escalated and the operator overrode it in place (§6g's
  "rates the rail, not the guidance");
- a **pre-emptive** waiver (`--session`/`--statute`) is a **distinct recorded signal**
  — an operator suppressing a rail *before* it fired; it is **not** a
  denied-then-overridden event and must not be counted as one.
Repeated waivers of the same statute-shape signal that a better rail should be
authored — but **standing rulings beyond the waiver do not exist in v1** (Q3 ruled):
the only two forms are the per-request ruling and the raiser-scoped waiver
(session-lifetime for a session raiser, until-revoke for a non-session raiser).

---

## 8. Withdrawal — the raiser retracts its own request (Q4)

Withdrawal is **raiser-only** (E6); owner-only withdrawal is rejected as
anti-automation — a dark factory must not queue corpses for a human janitor to
dismiss.

**Explicit withdrawal** — a new `withdraw` verb:

```
tightbeam withdraw --request <id> --reason "…"     # --reason REQUIRED (E4: never silent)
```

1. The withdrawing call's **canonical tagged identity ("session:"<>key for a session, else the origin string) must equal the request's `raiserId`**
   (F2/F3 — `"session:"<>key` for a session caller, the origin string verbatim for `--as <role>`); else
   `not_raiser`.
2. Request must be `open`; else `not_open`.
3. `status open → withdrawn` (a **CAS on `status='open'`**, F8); record `withdrawnBy`,
   `withdrawnReason` (required), and `withdrawnAt`; emit `decision_request_withdrawn`.

A withdrawing raiser is alive and re-adjudicating (E2) — it has decided not to wait —
so it also cancels its own parked wake (`tightbeam cancel-wake <wakeId>`, which it
holds; the substrate stores no request↔wake link, §4). A wake left uncanceled is
harmless: it fires on fallback, the raiser re-checks, sees `withdrawn`, and does
nothing.

**Auto-withdrawal on raiser death (kept ruling; the substrate is the second lawful
withdrawer, E6).** A higher orchestrator may judge a wait overtaken-by-events and
retire the waiting raiser; a dead raiser's pending questions are noise. Auto-
withdrawal resolves the retired session's open requests `open → withdrawn` (the same
`status='open'` CAS) with `withdrawnBy = "process:tightbeam"` and `withdrawnReason =
"raiser-retired"`, and **revokes** its waivers (a `revoke-waiver`-with-provenance —
`revokedBy = "process:tightbeam"` — **never a DELETE**; E5/F8). Two triggers, fast
path + durable backstop:
- **Fast path (cast-sweep).** `supervision.ex`'s `handle_cast({:retired,
  session_key}, …)` (:167), which today calls `doorbells_for_holder`, additionally
  calls `Escalation.withdraw_for_retired(db, session_key)`.
- **Durable backstop (boot recovery scan, F8).** At boot, `Escalation` scans for open
  requests whose `raiserSessionKey` is a retired session and withdraws them (and
  revokes their orphaned waivers) — so a cast dropped across a crash still resolves.
**Race with a concurrent `rule` (F8):** the `open → withdrawn` and the `rule`'s `open
→ ruled` are both CAS-on-`open`, so exactly one wins; a `rule` that loses to an
auto-withdraw finds the request `withdrawn` and returns `not_open`. The retired
session's orphaned condition wakes fire-with-zero-enqueue (`wake-on-fact-v1` W6
`:skipped`) and need no cleanup. **Coupling to report:** supervision's retirement
handler gains this one call, and boot gains the recovery scan; see §11.

---

## 9. Gate consultation — resolve (read), escalate (effect), consume (actor)

For **raiser `R` = the canonical `raiserId`** (`"session:"<>key` for a session
principal, else the origin string; derived from `call.principal`, never
`call.session_key`; F3 — at the turn-end edge this is the holder), statute `X =
statute.name`, and `actionKey = digest(call)` (§3). **Current request for the key =
`SELECT … WHERE raiserId=R AND statuteName=X AND actionKey=? ORDER BY rowid DESC LIMIT
1`** (F5-FRESH: the implicit rowid is recency; a later escalation of the same shape
supersedes an earlier resolved one).

### 9.1 `Escalation.resolve/3` — the effect-free read (folded into `Rules.decide`)

Returns the four-shape union `:allow | {:allow, ruling_id} | {:deny, e} |
{:needs_request, dr_id | nil}` (§2 part 1, F1), **opening/consuming/firing nothing**
(rails FRESH-1). Consults, in order:

1. **Waiver.** A live waiver for `(R, X)` (§7) → **`:allow`** (waiver-sourced,
   non-consumable; every identical action passes while it lives, E1). Nothing to
   consume.
2. **Current request** for `(R, X, actionKey)`:
   - `ruled`, `decision = allow` (or an allowing option) → **`{:allow, <this ruling's
     row id>}`** — ruling-sourced; `decide` collects the id into `to_consume` (the actor
     spends it, §9.3).
   - `ruled`, `decision = deny` → `{:deny, deny_form(X, ctx)}`.
   - `ruled`, `decision = waived` → **`{:needs_request, nil}` (F6).** A `waived`
     resolution is **terminal-historical**: the WAIVER was the authorization, and if it
     is now gone (revoked) the historical row confers none. (A *live* waiver is already
     caught by step 1; reaching this branch means the waiver was revoked.)
   - `open` → **`{:needs_request, <that row's id>}`** — the caller is already parked on
     this exact action; the actor re-returns it idempotently (§9.2), opening no
     duplicate.
   - `consumed` / `withdrawn`, or **no** request → **`{:needs_request, nil}`**.

### 9.2 `Escalation.escalate/4` — the effect (actor, on whole-fold `{:escalate,…}`)

`Escalation.escalate(db, call, statute, ctx) → {:decision_pending, id}`. On
`{:needs_request, dr_id}` with **`dr_id` non-nil**, re-return `{:decision_pending,
dr_id}` — the existing open request — opening nothing. On **nil**, in **one
transaction**: `INSERT ... ON CONFLICT DO NOTHING` a `decision_requests` row
(`status='open'`, fields per §3 — `raiserId` = `R`, `raiserSessionKey` = `R`'s session
or `NULL` (F3), `deadlineAt` = now + the configured deadline (§11), `question`/`options`
from `ctx`, `context` = the call snapshot, `ownerUserId` from `R`), then **re-`SELECT`
the open row** for the key. **Concurrent-open safety (F5):** because `resolve` and
`escalate` are separate phases over a non-unique lookup, two callers can both reach the
`nil` branch; the **partial unique index** (`decision_requests_one_open`, §3) admits
exactly one insert, and the loser's `ON CONFLICT DO NOTHING` + re-`SELECT` returns the
**winner's** row — one open request, both callers get the same `{:decision_pending,
id}`. The insert winner emits `decision_request_opened`. Owner delivery (§6) is
**post-commit** (F7). At the turn-end edge the sweep then parks the holder idempotently
via `parkWakeId` (§2/§4).

### 9.3 `Escalation.consume/2` + the batch rule — the authorization (actor, whole-fold `:allow`)

The fold already resolved each escalate statute, so the actor does **not** re-resolve:
it holds `to_consume` = the **ruling row `id`s** `resolve/3` surfaced during the fold
(rails' form). **Immediately before invoking the handler**, for **each** entry the
actor calls **`Escalation.consume(db, ruling_id)`** — a single-statement CAS `UPDATE
decision_requests SET status='consumed', consumedAt=? WHERE id=ruling_id AND
status='ruled'` — no re-resolution by statute/actionKey.

**Batch rule (fail-closed; the partial-spend regression, F1).** The actor CASes every
`to_consume` entry. **If ANY entry loses its CAS, the verb is DENIED**, and the entries
that already won **STAY consumed** (they are not rolled back) — consumed-on-**attempt**
covers the whole batch: the attempt spent them, so a re-issue re-escalates each one
that vanished (`consumed` → `:needs_request`, §9.1) and opens fresh requests. A
waiver-sourced statute contributes no `to_consume` entry (nothing to spend). No
wrapping transaction (rails whole-fold rule): a handler that fails after the batch won
has spent its authorizations and a retry re-escalates.

`digest(call)` is substrate-owned and deterministic (§3 normalization); the statute
never supplies it. "Per-request" ruling (Q3) is exactly this key **plus consumption
(F1):** a ruling authorizes the one action-shape that was escalated, for one attempt;
a raiser that re-adjudicates into a *different* action gets a fresh request, correctly
uncovered by the old ruling.

---

## 10. Legibility events (E4)

Every edge writes exactly one `lifecycle_events` row (open `kind` CHECK, no
migration), bound in-transaction (`EventLog.lifecycle_in_txn/4`):

- `decision_request_opened` — subject request `id`; detail `raiser=<R> statute=<X>
  owner=<O> assignment=<A>`.
- `decision_request_ruled` — subject `id`; detail `by=<owner> decision=<d>
  factId=<rulingFactId>`.
- `decision_request_withdrawn` — subject `id`; detail `by=<raiser|process:tightbeam>
  reason=<why>` (`reason=raiser-retired` for the auto-sweep).
- `waiver_granted` — subject waiver `id`; detail `raiser=<R> statute=<X> by=<owner>
  path=<request|preemptive>` (the `path` distinguishes the two §6g signals, F6).
- `waiver_revoked` — subject waiver `id`; detail `by=<owner|process:tightbeam>`.
- `condition_fact_filed` for each `escalation-ruled` fact is emitted by
  `ConditionFacts.file_in_txn` itself (`wake-on-fact-v1` §6), not duplicated here.

Rating is derived, never stored (observability doctrine): open-request age,
time-to-rule, and withdrawal rate are queries over these rows. Waiver rate is sliced
by `path` — **request-triggered** waivers feed §6g's denied-then-overridden metric;
**pre-emptive** waivers are a distinct signal and are counted apart (F6).

---

## 11. Implementation seam (modules / files)

| Concern | File | Change |
|---|---|---|
| Engine + tables | `lib/tightbeam/escalation.ex` (NEW) | `decision_requests` (rowid table; statuses `open/ruled/consumed/withdrawn`; domain-tagged `raiserId` NOT NULL, nullable `raiserSessionKey`, `deadlineAt`, `parkWakeId`; **partial unique index `decision_requests_one_open` WHERE status='open'**, F5) + `escalation_waivers` (keyed on `raiserId`) + `ensure_schema/1`; `resolve/3` (effect-free read, four-shape union incl. `{:allow, ruling_id}`), `escalate/4` (open via `INSERT … ON CONFLICT DO NOTHING` + re-`SELECT`, F5), `consume/2` (`consume(db, ruling_id)` CAS) — §9; `rule/…`, `waive/…` (resolve-all-matching-open, §7), `revoke_waiver/…`, `withdraw/…`; `withdraw_for_retired/2`; boot recovery scan (§8); `digest/1` (§3); read projections (§6) |
| Deadline config seam (Lattice) | **`config :tightbeam, :escalation_decision_deadline_ms`** — Application env, the same operator-knob home as supervision's prod-limit `N` (`prod_limit`, threaded through `Escalation`'s child spec from `application.ex`) | `escalate/4` reads it at DR creation and sets `deadlineAt = now + it`; overridable at boot by env var **`TIGHTBEAM_ESCALATION_DECISION_DEADLINE_MS`**; default **`@default_decision_deadline_ms = 86_400_000`** (24h) when unset. No new config machinery — it rides the existing Application-env operator knobs |
| Reserved kind | `lib/tightbeam/condition_facts.ex` | add `escalation-ruled` to `@reserved_kinds` (§5) |
| Verbs | `lib/tightbeam/gateway.ex` | `rule` / `waive` / `revoke-waiver` / `withdraw` handlers (admin-axis auth, F3); read handlers `decision-requests` / `decision-request`; post-commit owner delivery via the wake-to-user path (§6, F7/F9) |
| Verb allowlist | `lib/tightbeam/wire/router.ex` | add `rule`, `waive`, `revoke-waiver`, `withdraw`, `decision-requests`, `decision-request` to `@agent_verbs` |
| Retirement + boot | `lib/tightbeam/supervision.ex` + boot | `handle_cast({:retired, …})` also calls `Escalation.withdraw_for_retired/2` (fast path); boot calls the recovery scan (durable backstop) — §8 |
| CLI | `cli/src/args.rs`, `cli/src/dispatch.rs` | `rule` / `waive` / `revoke-waiver` / `withdraw` + read commands `decision-requests` / `decision-request`; wire mapping; help + arg tests |
| Schema bootstrap | boot `ensure_schema` sequence | call `Escalation.ensure_schema/1` |

**Companion reconciliation — NO parent edit pending on this document (verified against
rails as it stands — the four-shape union, consume/2, and the seam are all present).** This spec's engine and
`rails-mechanism-v1.md` are mutually aligned:
- **Seam / union.** rails §B (r9 :405-420) folds this engine's effect-free `resolve/3`,
  collecting ruled-allow ids into `to_consume`, running `escalate/4` (only on `dr_id ==
  nil`) and the per-ruling **`consume/2`** CAS (`consume(db, ruling_id)`, rails r9
  :386/:1278 — arity confirmed, F4). The **four-shape** union `:allow | {:allow,
  ruling_id} | {:deny, e} | {:needs_request, dr_id|nil}` (§2/§9.1, F1 — a bare atom
  cannot carry the id) is carried by rails as it now stands (§B split bullets, I4,
  composition notes, X4). No edit to this document or to rails is pending on it.
- **Turn-end park.** rails §D2.4 (:846-867) has adopted this spec's park text verbatim:
  the sweep parks the holder on `{:escalate, statute, ctx, dr_id}`, fallback `dueAt =
  deadlineAt` (**not** a prod cadence — it cites `supervision.ex:370`'s `after_ms:0`),
  idempotent via `parkWakeId`, recorded `rail_sweep` decision `escalate-park`. The stale
  "prod-deadline cadence" line is gone.
- **Composition / X4.** rails' Composition notes (:1268-1281) describe the three-part
  split (`resolve/3` / `escalate/4` / `consume`), mark the engine "rewritten to Flynn's
  ruled model (Q1–Q4 resolved)," and gate `escalate`-effect statute loading on **this
  spec's adversarial review landing clean, not on ratification**.
- **wake-on-fact.** This spec files rulings through `ConditionFacts.file_in_txn/2` + the
  single outermost-caller post-commit nudge, and reserves `escalation-ruled`
  (`@reserved_kinds` = `{quota-recovered, escalation-ruled}`). Any staleness in
  `wake-on-fact-v1.md`'s own header list of reserved kinds is **that spec author's edit**,
  routed to them — not this document's (F4).

No parent-spec edit remains pending on **this** document; **loading gates on this spec's
review landing clean**, in rails' own form. No cross-spec item is in flight; rails carries
the four-shape union as it stands (above); nothing is in flight.

---

## 12. Acceptance contract (concrete provable cases)

Each case is never-silent (E4), honors execute-once (E1) and delivery-is-not-
resumption (E2), and adds no state or flag (E3).

1. **Halt without deny.** A statute escalates a `merge`. Assert: the verb handler
   does **not** run; exactly one `decision_requests` row opens (`status=open`); one
   `decision_request_opened` row; the owner's Main receives one delivery; the caller
   gets `{:decision_pending, id}` — distinct from any `{:deny,…}`.

2. **Raiser parks; supervision reads continuation.** After case 1 the raiser
   schedules a self-targeted `{escalation-ruled, <id>}` wake with a fallback and ends
   its turn. Assert `Wakes.pending_count(db, raiser) == 1` and
   `Wakes.self_pending_count(db, raiser) == 1`; `Supervision.evaluate` on the next
   terminal returns `:continuation`; no prod fires. Assert there is **no**
   `blocked-on-owner` state or flag anywhere (E3).

3. **Ruling resumes; the ACTOR consumes by id (F1).** The owner runs `rule --request
   <id> --decision allow`. Assert: `status=ruled`, `decision=allow`, `ruledBy` = owner;
   one `escalation-ruled/<id>` `condition_facts` row (origin `process:tightbeam`); the
   raiser's wake fires. The raiser re-issues the merge; `resolve/3` returns **`{:allow,
   ruling_id}`** (effect-free — asserts the request is still `ruled` at that point,
   engine consumed nothing); the fold records `ruling_id` in `to_consume`; then the
   actor's `consume(db, ruling_id)` CAS flips `ruled → consumed` **before** invoking the
   handler; the handler runs **exactly once**. Assert the substrate never executed the
   halted verb between escalate and re-issue.

4. **Consumed ruling does not re-authorize (F1).** After case 3, the raiser re-issues
   the **same** action again. Assert `resolve/3` finds `status=consumed` →
   `{:needs_request, nil}` and opens a **fresh** request, NOT a second silent allow.
   Contrast: a **waiver** (case 9) returns bare `:allow` and re-authorizes identical
   repeats.

4b. **Consume-CAS-lose + batch fail-closed (F1).** (a) Two concurrent re-issues of the
    same ruled-allow request race `consume(db, ruling_id)`: exactly one CAS wins
    (`ruled → consumed`, handler runs), the loser gets `{:deny,…}` and its handler does
    **not** run. (b) **Batch:** an action escalated by two statutes, both ruled-allow;
    the actor CASes both `to_consume` ids — if the second **loses**, assert the verb is
    DENIED and the first entry **stays `consumed`** (not rolled back); re-issue
    re-escalates each vanished authorization. (c) A handler that CRASHES after its
    batch won: the ids stay `consumed`, a retry re-escalates — spent on attempt, not
    success.

5. **Ruling `deny`.** Owner rules `deny`; wake fires; raiser re-issues; gate returns
   `{:deny,…}` (not consumed); the raiser re-adjudicates and does **not** re-park; a
   further re-issue denies again with no new request.

6. **Schedule-then-check race (F5).** Owner rules **before** the raiser schedules its
   wake (ruling fact lands under the wake's future cursor). Assert: the raiser
   schedules first, then reads `status=ruled`, **cancels the wake**, and re-issues —
   the ruling is not lost to the no-replay cursor. Mirror case: owner rules **after**
   schedule → the wake fires normally.

7. **Long-wait fallback loop.** With no ruling, the wake fires by fallback
   (`wake_fallback_fired`); the raiser re-checks (`status=open`) and re-subscribes;
   assert a fresh pending self-wake exists, `Supervision.evaluate` still
   `:continuation`, the request stays `open`. Repeat twice; assert never-a-stall and
   one legible fallback row + one re-schedule per iteration.

8. **Accountability via the admin axis (E6/F3).** `rule`/`waive`/`revoke-waiver` by a
   principal the admin axis rejects, or by the raiser → `not_owner`, no state change.
   `withdraw` by anyone but the raiser (or `process:tightbeam`) → `not_raiser`.

9. **Waiver short-circuits, resolves all open, dies with the session (F6).** With
   **two** open requests for `(raiser, X)`, owner `waive --request <id>` (one of them):
   assert one `escalation_waivers` row; **both** requests resolve `ruled`
   (`decision=waived`) in one transaction and **both** wakes fire; then a subsequent
   same-statute action by the same raiser returns `:allow` with **no** new request
   (non-consumable). Retire the raiser; assert the waiver is **revoked-with-provenance**
   (`revokedBy=process:tightbeam`, not deleted) and a fresh session under `X` escalates
   normally (E5).

10. **Revoke is prospective (F6).** `revoke-waiver`; assert `revokedAt` set; the next
    same-statute action escalates again; assert requests already resolved `waived` stay
    `waived` (revoke rewrites no past resolution).

11. **Withdrawal + reason required.** Raiser `withdraw --request <id> --reason "…"` →
    `status=withdrawn`, reason recorded, `decision_request_withdrawn` row; a withdraw
    with no reason is rejected (E4). After withdrawal a re-issue of the *same* action
    opens a **fresh** request. `withdraw` by the owner → `not_raiser` (E6).

12. **Auto-withdraw on retirement, both triggers + race (F8).** (a) Open a request,
    retire the raiser via the cast path; assert `status=withdrawn`
    (`withdrawnBy=process:tightbeam`, `reason=raiser-retired`), waiver revoked-with-
    provenance, the owner's open queue no longer shows it, orphaned wake fires-with-
    zero-enqueue. (b) Drop the cast, boot; assert the **recovery scan** withdraws the
    still-open request. (c) A `rule` racing an auto-withdraw: exactly one CAS wins; the
    loser returns `not_open`.

13. **Per-request scope (Q3).** After a `ruled=allow`-then-consumed for action A, the
    raiser re-adjudicates into a **different** action B (different `actionKey`); assert
    B escalates a new request, i.e. the ruling authorized A only.

14. **Reserved-kind forgery denied.** A session principal calling `condition --kind
    escalation-ruled --scope <id>` → `reserved_kind`, no fact filed, no spurious wake.
    The substrate's `rule` path files it successfully.

15. **Re-rule idempotency + conflict (F10).** Re-`rule` of a resolved request with the
    **same** decision → idempotent, returns the prior ruling, no second fact. Re-`rule`
    with a **different** decision → `not_open`.

16. **Post-revoke `waived` row confers no authorization (F6).** A request resolved
    `ruled/waived` by a now-**revoked** waiver: re-issue the same action; assert
    `resolve/3` returns `:needs_request` (the historical `waived` row is terminal, the
    waiver was the authorization and it is gone) and a **fresh** request opens.

17. **Turn-end sweep parks the holder, idempotently (E7/F4).** A turn-end-edged
    `escalate` fires from the sweep. Assert the sweep schedules a **substrate-created,
    holder-targeted** `{escalation-ruled, id}` wake with `sessionKey = holder`,
    **`creatorSessionKey = NULL`** and `origin` = the process string (wake-on-fact r3:
    a `process:` principal stamps a nil creator; only a session principal stamps a
    key), and fallback `dueAt = deadlineAt` (asserting the cadence is the DR's
    `deadlineAt`, **not** an `after_ms:0` prod); records `parkWakeId`. Suppression holds
    because it is **target-keyed**: `Wakes.pending_count(db, holder) > 0` →
    `:continuation`; and the wake provably does **NOT** count as self-scheduled
    (`creatorSessionKey nil ≠ holder`, so `self_pending_count` excludes it — the
    correct semantics: this is the substrate's continuation of the holder, not the
    holder's own). Sweep returns `{:acted, :rail_escalate}`. A second sweep over the
    same open DR **re-returns it and does not double-park** (recreate only if
    `parkWakeId` absent). With this spec's review landing clean the statute is **not** a
    load error (rails gates loading on review-clean, not ratification; §11).

18. **Domain-tagged `raiserId` — no collision, across all ops (F2/F3).** A **session**
    raiser's DR has `raiserId = "session:" <> sessionKey`; a **non-session** raiser (org
    token `--as reviewer`) has `raiserId = "agent:reviewer"` (the origin verbatim) and
    `raiserSessionKey = NULL`, receives `{:decision_pending, id}` **synchronously** with
    **no** park wake, and is not targeted by auto-withdrawal-on-death. Assert a session
    keyed `"session:S"` and an origin keyed `"agent:reviewer"` **never collide**. Then,
    keyed on the non-session `raiserId`: (a) a **re-issue** finds the same current
    request via the `raiserId` lookup; (b) after a `rule allow`, `resolve/3` authorizes
    the re-issue with `{:allow, ruling_id}`; (c) **withdrawal** by the same origin
    succeeds (canonical identity == `raiserId`), a different origin → `not_raiser`; (d)
    **read visibility** — the same origin sees the row, others do not; (e) a **waiver**
    for that `raiserId` has **no death sweep** — it persists until explicit revoke
    (E5/F3).

19. **Read surfaces (F9).** `decision-requests` by the owner lists all its open
    requests; by the raiser lists only its own; by an unrelated principal lists none.
    `decision-request <id>` returns the full projection incl. `context` for the owner.

20. **Idempotent open, concurrent open, and rowid recency (F5-FRESH).** (a) Two
    identical re-issues while `status=open` return the **same** request id and open no
    duplicate. (b) **Concurrent open (F5):** two callers both reach `escalate/4`'s `nil`
    branch for the same `(raiserId, X, actionKey)`; assert the partial unique index
    (`decision_requests_one_open`) admits **exactly one** insert, the loser's `ON
    CONFLICT DO NOTHING` + re-`SELECT` returns the **winner's** row, and both callers get
    the same `{:decision_pending, id}` — never two open requests. (c) **Rowid recency:**
    after a consumed request and a fresh open one share `(raiserId, X, actionKey)`,
    `resolve/3`'s `ORDER BY rowid DESC LIMIT 1` reads the **fresh open** row (higher
    rowid) as current — even though its `TEXT` `id` does not sort after the older one,
    proving recency is rowid, not `id`.

21. **Effect-neutral params excluded from the digest (Lattice).** A turn-end sweep
    escalates a synthesized `attest {assignment_id, kind}` (no `note`); the owner rules
    allow. The agent re-issues the real `attest` **with a `--note`**. Assert the
    re-issue's `actionKey` **equals** the ruling's (note excluded), `resolve/3` returns
    `{:allow, ruling_id}`, and the verb edge consumes and runs — **no owner ping-pong**.
    Contrast: changing an **effect-bearing** param yields a different `actionKey` → a
    fresh request (case 13 semantics preserved).

22. **The sweep never consumes (Lattice / verb-edge-only).** With a prior `ruled`-allow
    for a stalled assignment's obligation, run the turn-end sweep: assert `resolve/3`
    returns `{:allow, ruling_id}`, the sweep treats the obligation as met, **does NOT**
    CAS the ruling (`status` stays `ruled`), and runs no handler. Then the agent
    re-issues at the verb edge: assert THAT edge consumes (`ruled → consumed`) and runs
    the handler — the ruling is spent exactly once, at the edge that executes.

---

## 13. Non-goals (the scope guard)

- **NO escalation policy / classifier** — which conditions escalate is rails TOML in
  kungfu (`rails-mechanism-v1`), not this engine. The substrate never knows or
  branches on any specific trigger.
- **NO substrate auto-retry, timeout-auto-approve, or default ruling** — a request
  stays open until ruled, waived, or withdrawn (E1).
- **NO blocked-on-owner state or flag** (E3).
- **NO standing rulings beyond the raiser-scoped waiver** — the only two forms are the
  per-request ruling and the raiser-scoped waiver, whose lifetime depends on the raiser
  kind: **session-lifetime** for a session raiser (dies at retirement), **until-revoke**
  for a non-session raiser (E5/F3, Q3).
- **NO `answer`/judgment-question form in v1 (F10 descope, deliberate/YAGNI).** The v1
  escalation engine gates **actions** only; a decision is `allow | deny | waived`.
  A judgment question to the user stays the manual's `wake --user` pattern; a dedicated
  ask-verb can come later if it is ever needed, but is out of scope here.
- **NO owner-only withdrawal, NO silent withdrawal** (E6/E4).
- **NO ruling attest kind** — provenance is the `decision_requests` row + the
  condition fact + the lifecycle row (§5).
- **NO substrate-scheduled wait or substrate-chosen fallback AT THE VERB EDGE** — a
  live session raiser parks itself with a fallback of its own/its guidance's choosing
  (E7, `wake-on-fact-v1` W5). The turn-end sweep is the sole exception: it parks the
  holder with fallback `dueAt = deadlineAt`, the DR's org-configured deadline — not a
  supervision prod cadence (prods fire at `after_ms:0`; F4).
