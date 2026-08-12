# Ordered publication — technical proposal v1

Status: **REJECTED 2026-08-04 by Sol xhigh review. Do not build §4.** The ratified design
is at the bottom of this file under "RATIFIED DESIGN". §4 contained five factual errors,
recorded below because the errors are more instructive than the design: (1) the isolation
argument was invented — ConnRegistry's delivery functions are local `send/2`, so no wire
I/O ever executes on the commit path, and the danger §3 warns against does not exist;
(2) the proposed per-session publishers would each still call the ONE global ConnRegistry,
isolating nothing; (3) `Txn.publish_after_commit` cannot work as written — `%DB.Txn{}` is
an immutable struct holding only `conn`; (4) the "second latent bug" of publishing past a
rollback does not exist — every cited site already publishes only from its `{:ok, ...}`
branch; (5) a per-session ticket counter would create a SECOND authority for commit order
when `seq` is already monotonic (projection.ex:53) — a T-SOURCE violation inside a
proposal citing T-SOURCE. The gap-buffer timeout was correctly called out as
accommodating dirt. Lesson for the author: a design that invents a constraint then builds
machinery to satisfy it is a lattice, and the reviewer's answer is a `send` in the right
place.

Original status line (kept for the record): §1's MOTIVATING EVIDENCE IS REFUTED (2026-08-04, lane G8, by
measurement). The T2b row-10 failure is NOT this mechanism.** Instrumented publish path,
failing run: publish→client-arrival 0ms on all three frames; commit order == publish
order == arrival order; nothing dropped or reordered. Actual cause: the journey's oracle
(journeys.ex:786) asserts Smoke B's reply lands BEFORE Main's by comparing indices, and
in the full codex leg B's trivial turn took 20.4s against Main's deliberately-slow 12.6s,
so B's reply committed 8.2s after Main's turn ended — the FAIL branch (:824) then names it
"a delayed client frame" by construction. A test defect; G8 is repairing the oracle.
The decisive argument, which the author should have applied before writing this: A DROPPED
FRAME NEVER ARRIVES, and B's frame is present in reply_order.

WHAT SURVIVES: §2's mechanism is still REAL and still LATENT — conn_registry.ex:14-27
documents an ordering precondition that no code provides, and lane G5 flagged it
independently. It has NO known reproduction. Therefore: DEMOTED from in-gate blocker to
post-Gibson item, and this proposal is a design for a latent defect, to be built only if
review judges it worth building before a reproduction exists. Reviewer: judge §4's design
on its merits for the latent defect; disregard §1's urgency framing entirely.

Original status line: PROPOSAL, awaiting review. Authored 2026-08-04 by the team-lead session, for
Sol xhigh review before any implementation. Lane G8 is confirming the mechanism and
building the acceptance test only; no design work is delegated.

## 1. The defect, as a user experiences it

Two agents in one org work concurrently. A user watching clawline sees Main's reply and
never sees Smoke B's — until they reconnect, at which point it appears. T2b's concurrency
journey (row 10) catches this precisely, and its two halves disagree in the way that
names the cause:

    | 10 concurrency | PASS | FAIL | codex: the substrate ran both lanes simultaneously
    (sampled_together=true intervals_overlapped=true widest_sample=2) but the client did
    not see Smoke B's reply during Main's turn (reply order ["c_sim_31_9",
    "c_sim_33_11", "c_sim_32_10"]) — a delayed client frame, not a lane defect

Reproduced twice on merged main (`4da210c`): once under lane load, once on a quiet box.
Green pre-merge. The substrate did the concurrent work correctly; the CLIENT was not told.

This is the OpenClaw symptom the product exists to end — "I get no response and don't
know what happened to my message" — arriving through the delivery layer rather than the
work layer. T-CONSPICUOUS is violated even though nothing was lost: the reply exists, is
durable, and replays later, but at the moment it mattered the user was shown silence.

## 2. Mechanism — and the codebase already documents the invariant being broken

`lib/tightbeam/conn_registry.ex:14-27` states it outright:

> Persistent per-connection delivered-seq filter. Every message carries its per-session
> store `seq`. A connection tracks `lastDeliveredSeq` per session for its WHOLE lifetime
> (not just during replay drain): any push with seq <= lastDeliveredSeq is dropped. This
> suppresses a late publication of a pre-watermark commit forever, closing the
> replay/live race.
>
> **ORDERING DEPENDENCY: the filter is safe ONLY if publications for a session arrive in
> commit (seq) order. That is guaranteed by publishing from the single-writer commit path
> (`Tightbeam.DB`), not by this module. This module enforces the per-connection monotonic
> filter; the caller must not publish out of seq order.**

The filter is correct and is doing its job. The stated guarantee it depends on **does not
exist in the code**. `Tightbeam.DB` has no publish hook (`grep publish lib/tightbeam/db.ex`
→ nothing); publication happens after `transaction/2` returns, in the CALLER's process:

- `lib/tightbeam/gateway.ex:5772` `publish_message/4` — called from at least
  `:1043`, `:1701`, `:4142`, `:5195`, `:5767`
- `lib/tightbeam/event_log.ex:360` — `ConnRegistry.publish_message` from `notice/5`

Two independent processes appending to the SAME session therefore commit in one order and
publish in whatever order the schedulers deliver. Sequence that produces the observed
failure:

1. lane A commits seq 10 (Smoke B's reply)
2. lane B commits seq 11 (Main's reply)
3. lane B publishes 11 first → connection sets `lastDeliveredSeq = 11`
4. lane A publishes 10 → `10 <= 11` → **dropped forever** for that connection

Note the asymmetry that made this survive: the drop is *permanent for live delivery* but
*invisible to storage*. Reconnect replay reads the projection and shows both. So every
durable assertion passes, and only a live client is lied to — which is why unit tests, the
soak, and five review rounds never saw it, and why T2b's client-side half is the only
oracle that could.

Why it appeared now: nothing in the merged lanes broke it. Lane G5 named it explicitly as
pre-existing at every append-then-publish site and deliberately left it (correctly — it
was out of its scope). G5 also *removed* a wide post-commit `Org.get` round-trip from one
path, which plausibly narrowed the window enough to change how often the inversion lands.
The defect is older than tonight; tonight it became reproducible.

## 3. Design constraint that rules out the obvious fix

The obvious fix is "publish from inside the DB owner." **That is forbidden**, and by the
prime invariant:

T-CONCURRENCY (normative, `tightbeam.md`): "no session's work ever waits on another
session's, and no harness's work ever waits on another harness's." `Tightbeam.DB` is ONE
GenServer that deliberately serializes all writes (`db.ex:1-17`). Doing wire work inside
it — `ConnRegistry.publish_message/6` is a `GenServer.call`, so a synchronous round-trip
to a second process, which in turn calls a `deliver` function — would put every session's
publication on the single global write path. One slow or wedged connection would then
delay COMMITS for every other session. That trades a visible ordering bug for an invisible
throughput coupling, which is worse and violates the tenet the product was built around.

So: ordering must be derived from commit order, without publication *executing* on the
commit path.

## 4. Proposal: the DB owner stamps a per-session publication ticket; a per-session
## publisher drains in ticket order

Three parts. Nothing new is created that does not already exist in some form.

### 4.1 Stamp inside the transaction (cheap, in the one place order is known)

`Tightbeam.DB.transaction/2` already runs the callback inside the owner process, strictly
serialized. Publication intents raised during a transaction are collected on the `Txn`
handle rather than sent:

    Txn.publish_after_commit(txn, {:message, session_key, owner_user_id, seq, payload})

On successful commit, and still inside the owner (this part must be O(microseconds) and
must not call another process), the owner assigns each intent a monotonic per-session
ticket and hands them to the session's publisher via `send/2` — an asynchronous message
into a mailbox, never a `call`. On rollback the intents are discarded, which fixes a
second latent bug for free: today a caller can append-then-publish around a transaction
that later fails, publishing a message that does not exist.

Why `send` is safe here where `call` is not: a mailbox write is constant-time and cannot
block on the receiver's state. The commit path gains no dependency on any connection's
health.

### 4.2 Per-session publisher, per-session ordering only

A lightweight process per active session (Registry-keyed, same shape as `SessionLane`,
started on demand, terminating when idle) receives ticketed intents and calls
`ConnRegistry.publish_message/6` in ticket order. Because tickets are assigned inside the
serialized owner, ticket order IS commit order, per session. Because the publisher is per
session, a wedged connection delays only that session's frames — which is exactly the
scope T-CONCURRENCY permits and no wider.

Out-of-order arrival within one session's mailbox is possible in principle (two owner
`send`s to one mailbox preserve order in the BEAM, so in practice it is not) — the
publisher nonetheless buffers a gap rather than publishing past it, with a bounded wait
after which it publishes anyway and records the gap. A silent reorder must not be
possible; a delayed frame is acceptable, an unrecorded reorder is not.

### 4.3 The call sites become declarations

`gateway.ex:5772` and `event_log.ex:360` stop publishing directly and instead declare
intent on the txn they are already inside. `EventLog.notice/5` keeps its one-call
record-and-notify contract (G5's invariant) — the notify half becomes an intent rather
than a synchronous publish, which strengthens it: today a `notice` whose transaction
rolls back has already published.

## 5. What this does NOT change

- `ConnRegistry`'s filter, generations, and drop rule: untouched. They are correct and
  become correct-with-their-precondition-actually-true.
- Replay: untouched. `Projection.list_after/5` + socket cursors already repair history and
  will simply have less to repair.
- Ledger claim/enqueue (G1) and the notice row/message contract (G5): untouched.
- `broadcast/4` (non-message events: turn state, typing, stream) has no seq filter and no
  ordering dependency. NOT in scope. Say so explicitly if review disagrees.

## 6. Risks, honestly

1. **A new process per session.** Mitigated by starting on demand and stopping when idle,
   and by it being a mailbox drain with no state beyond a small buffer. But it is
   additional supervision surface, and this codebase treats new machinery as a defect
   unless earned. The alternative — a single global publisher — is rejected precisely
   because it reintroduces cross-session coupling.
2. **Intents held on the Txn handle** grow memory for a transaction that appends many
   messages. Bounded in practice (a turn appends a handful); worth an assertion rather
   than a guess.
3. **Ordering across sessions is explicitly NOT guaranteed** and never was. If any client
   assumes cross-session ordering, this proposal does not give it to them — and it should
   not.
4. **The gap-buffer's bounded wait is a number**, and numbers are where this codebase
   hides its lies. Prefer a formulation with no timeout at all if review can find one; if
   a bound is unavoidable, it must record when it fires rather than silently publishing
   past a gap.
5. **Scope creep risk:** discarding intents on rollback fixes a real second defect, but
   it is a behavior change beyond the ordering bug. It should be named in the commit and
   in the acceptance tests, not smuggled.

## 7. Alternatives considered and rejected

- **Publish inside the DB owner.** Rejected: global serialization of wire work on the
  commit path; T-CONCURRENCY violation (§3).
- **A single global publisher process.** Rejected: same coupling one step removed — a
  slow connection on session A delays session B's frames.
- **Make `ConnRegistry` tolerate out-of-order arrival** (buffer and reorder centrally).
  Rejected: it is one process for all sessions, so buffering there couples sessions; and
  it would weaken a filter that is currently exactly right, to accommodate callers who
  should not be racing. Fix the violated precondition, do not loosen the invariant that
  depends on it.
- **Sequence numbers assigned by the caller** (e.g. wall clock, or a counter per caller).
  Rejected: the write and its account must not be separated — order must come from the
  commit, and only the owner knows that.
- **Do nothing; rely on replay.** Rejected: it is the product's founding symptom. "You
  will see it if you reconnect" is not conspicuous operation.

## 8. Acceptance

Lane G8's deterministic inversion test (two writers, forced commit/publish inversion, red
on current main) is the unit-level gate, and it must pin the PROPERTY — a connected client
receives both messages, in commit order — not any implementation detail.

The in-situ gate is T2b row 10 green on a quiet box on BOTH legs, plus no regression in
the claude leg, plus the combined soak unchanged.

## 9. Questions for the reviewer

1. Is the per-session publisher justified, or is there a formulation with no new process
   that still keeps wire work off the commit path? (Preferred if it exists.)
2. Is `send/2` from inside the DB owner acceptable at the commit boundary, or does even
   that couple the owner to mailbox growth in a pathological case?
3. Does discarding intents on rollback belong in this change or a separate one?
4. Is the gap-buffer's bounded wait avoidable? If not, what makes its firing loud?
5. Is `broadcast/4`'s exclusion right, or can turn-state frames also invert visibly?
6. Anything in `ConnRegistry`'s generation logic that interacts badly with a per-session
   publisher holding a stale connection reference?


## RATIFIED DESIGN (Sol xhigh, 2026-08-04) — build THIS

The minimum mechanism that makes ConnRegistry's documented precondition true:

- In `DB.handle_call({:transaction, ...})`: execute `COMMIT`, then perform the declared
  publication sends **in list order**, then reply to the caller. On rollback, perform none.
- Publications are asynchronous `send`s to the ALREADY-RUNNING `ConnRegistry`, which gains
  an async handler sharing the existing publication reducer. The intent carries
  `session_key`, the owner captured INSIDE the transaction, the stored `seq`, the payload,
  and the delivery function.
- One sender (the DB owner), one receiver (ConnRegistry) ⇒ BEAM signal ordering gives
  commit-order delivery with no ticket, no buffer, no timeout, no new process.
- **Migrate EVERY production message-publication site** so the owner is the sole sender —
  gateway.ex:1043, :1701, :4142, :5195, :5767 and event_log.ex:359. Leaving even one
  direct caller preserves the race. (Note gateway.ex:5773's post-commit `Org.get/2`
  round-trip widens today's window; capturing the owner inside the transaction removes it.)
- Keep the existing monotonic connection filter UNCHANGED. Add no fallback and no silent
  dead-recipient path.
- Gates: forced two-writer inversion; exact commit-order delivery; rollback emits nothing;
  no-live-connection then replay; register/replay/live interleavings; restart recovery.
  `broadcast/4` inversion tracked separately.

Status: post-Gibson (the defect is latent — no reproduction; T2b row 10 was a test defect).
