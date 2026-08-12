# Concurrency strategy — by failure class

**Status:** DRAFT for Flynn. Evidence: `sample-then-act-audit-2026-07-30.md` (27 findings) and
`topology-probe-2026-07-30.md` (disproof, with measurements). Tree at time of writing: `ec1ab68`.

## The premise this strategy has to satisfy

The codebase already contains correct, commented exemplars of every pattern below — the audit
lists seven by name — and 27 instances got written anyway. **So any plan whose main instrument is
documentation is already disproven by the evidence.** Guidance is the floor, not the plan. The
load-bearing parts must fail loudly with nobody looking: unavailable functions, build-failing
checks, and shapes where the wrong version does not compile.

Corollary, from the same evidence: the mistake is invisible at the moment you make it. Anything
that depends on a future agent NOTICING they are in this situation will fail the same way.

## What was ruled out, and why (so it is not re-proposed)

- **Moving process state into the DB.** Measured: prevents 1 of 27. 22 of 27 already gate on a
  fact in the DB. Where it is most needed it is unavailable — a transaction runs inside the single
  DB owner, so a decision whose act is a harness call or ssh cannot be in one, and holding a
  transaction for T ms delays every other session by T ms (measured 1:1) against acts budgeted
  8 s–600 s. That is a first-order T-CONCURRENCY violation. Reads themselves are free (22 µs p50,
  0.05% of a turn) — cost is not the argument.
- **A shared closure-runner abstraction.** The generic form (run a caller's closure inside an
  owner) is the WEAK form and caused its own defect: it parked a lane on adapter I/O and started
  timing out an unrelated verb. The strong form is named domain operations, domain-specific by
  definition.
- **A general grep guard for the whole class.** The read and the act routinely live in different
  modules, and no syntax marks a read advisory. Narrow guards work; a general one cannot.

---

## Class 1 — The read did not join the transaction the act already opens

**Count:** 9 (F1, F5, F10, F12, F13, F15, F16, F17, F20). **Consequence:** up to a 24-hour
invisible park (F1); a cancelled wake delivered and a turn burned (F5); a session cap breached and
stream order made nondeterministic (F10).

**Signature.** Code reads a fact with `DB.query`, then acts inside a `DB.transaction` that never
re-asserts what it read. Atomicity was available and free; it was not taken.

**Fix.** Move the read inside the transaction that already exists, or re-assert the predicate in
the WHERE clause of the act. No state moves. The repo already does this correctly in the condition-
wake path (`wakes.ex` `fire_candidate`/`fire_in_txn`), which is the exemplar to cite.

**Prevention (mechanical).** Guard A, in the idiom of the two shell guards already shipping: a
transaction that acts on a row read in an EARLIER transaction must re-assert the predicate it read.
Measured against all 87 `UPDATE` statements in `lib/`: **1 true positive, 0 false positives.**

---

## Class 2 — Missing fencing token on a re-enterable lifecycle

**Count:** 8 (F3, F4, F6, F18, F22, F24, F26, and F7 which is blocked at the protocol).
**Consequence:** an alarm closed for a violation nobody fixed (F6); a SIGKILL to a process group
whose pid was already released, killing an unrelated group under pid reuse (F4); the record and the
running agent disagreeing on which model is loaded, with no tiebreak (F3).

**Signature.** An act targets a row or resource by identity but not by generation, occurrence, or
incarnation — on a lifecycle that can be re-entered. **F6 is the clean disproof of the transaction
answer:** its act is already one atomic guarded UPDATE, and it is still wrong, because it closes
the wrong occurrence. Perfect atomicity buys nothing; a fencing predicate buys everything.

**Fix.** Carry the token and name it in the WHERE clause. Two exemplars in-repo: `RailEpisodes`
incarnation tagging, and `apply_model_strict`'s harness-side compare-and-swap (F3 already HAS a
fence — its defect is ordering, not absence).

**Prevention (mechanical).** Guard A extended: for tables whose status can be re-entered, every
mutating statement must name its occurrence token. Measured clean today — every cycling table
already complies except one.

**Not preventable:** F7. ACP `session/cancel` carries only a session id, no turn identity. The
fence does not exist at the protocol. This one gets a named limitation, not a fix.

---

## Class 3 — The decision was made outside the process that owns the fact

**Count:** 5 (F7, F9, F11, F14, F23). **Consequence:** a cancel interrupting the NEXT turn rather
than the intended one (F7); a lane prompting a harness session that was closed underneath it (F11).

**Signature.** Read process-owned state — or a fact whose owner is a process or an external system
— then act outside that owner. No transaction can help: the fact is not in the DB, and the act is
usually external anyway.

**Fix.** Move the decision into the owner as a NAMED operation (not a closure-runner). Exemplars:
`TurnObservations.observe/evidence`, `RailEpisodes.evaluating/summon/recovered`, and now
`SessionLane.at_turn_boundary`.

**Prevention (mechanical).** Guard B — the only form that scales, and it needs a naming convention:
mark every public reader of process-owned or CAS-owned state with a `sampled_` prefix, then freeze
PER-FILE call counts in a checked-in inventory. Adding a sampler call anywhere fails the build
until someone bumps the number, which forces the safe/racy question into review at the one moment
it is decidable, by the person who knows the answer. Surface is ~50 GenServer entry points, of
which ~25 are reads, plus ~20 DB-level samplers.

**Prevention (structural, stronger where available).** Delete the affordance: an owner that does
not export a read of its own fact cannot be sampled. Every one of these 27 began with a public read.

---

## Class 4 — Upward synchronous call between serializers

**Count:** 1 (F2), plus two more cycles in the same component. **Consequence:** the worst in the
set. Guaranteed — not probabilistic — three-process deadlock for 5 s, ending in an adapter crash
rather than a clean stop, with the cleanup silently skipped so a credential revocation records as a
planned teardown. It stalls every session on every harness. A second cycle is a process calling
itself, leaving a wake pending forever and retrying on every tick, visible only as a log line.

**Signature.** A closure stored in one server's state, invoked inside ANOTHER server's callback,
making a synchronous call to a higher tier. The module holding the closures is not a process, so
each closure silently inherits whoever calls it.

**Fix.** The tier rule: `DB` / `Conn` / `ConnRegistry` (leaves) < `Adapter`, `Credentials`,
`ModelCatalog`, `RailEpisodes`, `TurnObservations` < `AdapterCoordinator` < `SessionLane`,
`LaneManager`, `WakeScheduler`, `Supervision`. **A process may call synchronously only to a
strictly lower tier; every upward notification is a cast or a Task.**

**This rule already exists here and is followed two times out of three.** There are exactly three
upward hooks, all state-held closures: `on_adapter_ready` (a Task), `on_terminal` (a cast), and
`on_auth_event` (a call). The third is F2.

**Prevention (mechanical, two options).**
- Cheap, existing idiom: freeze an inventory of `state.<field>.(` invocations reachable from a
  callback, with the required shape (cast / Task / call) beside each. Small and real today. Adding
  a fourth upward hook, or converting one to a call, fails the build. **This alone catches F2.**
- Stronger: the static callback-closure pass. Not shell, but ~60 lines, already written once during
  the probe, and it produces a VERDICT (it found exactly one cycle and no others) rather than
  countability.

---

## Class 5 — Ordinary defects, not races

**Count:** 5 (F18, F19, F21, F25, F27). Missing nil guard where seven sibling sites have one; a
discarded return value; an uncaught exit; two clocks for one budget.

**Fix.** Individually, cheaply. **Prevention:** none special — this is what review is for, and
review caught them.

---

## Class 6 — A documented contract that does not exist in code

**Count:** 1, and it is arguably worse than the races around it. `SessionLane`'s moduledoc states
that a lane will not start the next queued turn until an orphaned ACP request is observed resolved.
`quarantined` is initialised false, read once, and **written nowhere**; the resolver's signals are
dropped by a catch-all. Everyone reading that module believes the protection exists.

**Fix.** Implement it or delete the claim. That is a product decision, not a cleanup.

**Prevention.** Honest answer: no mechanical check proposed. The cheapest real defence is that a
stated safety property gets a test, and a safety property with no test is treated as a proposal.

---

## Class 7 — Global serializer where per-key would do (not a race; a blast-radius amplifier)

Adapter re-adoption is capped at 3 concurrent operations GLOBALLY. A bounce is per key, so one
harness's recovery waits on another harness's — **a live violation of T-CONCURRENCY's second
clause.** Everything else in the coordinator is already per-key; the epoch is minted from a DB
sequence and is compared only within a key, so sharding preserves the ordering invariant.

**Fix.** Shard the semaphore per machine or per harness. It does not fix F2 — a cycle is still a
cycle — but it bounds the blast radius from "every session everywhere" to one machine.

---

## Sequencing

Ranked by consequence, not by class:

1. **F2 and its two sibling cycles** — guaranteed deadlock; one cycle wedges a wake permanently.
   Ship with the tier rule and its inventory guard in the same change, so the fix and its
   prevention land together.
2. **F4** — kills an unrelated process group under pid reuse. Fencing.
3. **F1, F3, F5** — silent, high-consequence: a 24-hour invisible park; record and reality
   disagreeing on the loaded model; a cancelled wake delivered.
4. **Guard A** — cheap, measured clean, and closes Class 1 and most of Class 2 against recurrence.
   Land it with F6, its one true positive.
5. **The quarantine contract** — decide implement-or-delete before anything else touches that
   module.
6. **Class 7 sharding**, then the Class 3 backlog behind Guard B's naming convention, then Class 5.

## What would tell us this is wrong

- If Guard A produces false positives once it runs over the whole tree, the "re-assert in the
  transaction you already have" rule is less mechanical than measured and Class 1 needs review, not
  a check.
- If the static acyclicity pass finds cycles the tier assignment cannot express, the tiering is
  wrong rather than the code.
- If Guard B's naming convention cannot be applied without touching more than ~50 call sites, the
  affordance-deletion route is cheaper and Guard B should be dropped for it.

---

## Post-sizing corrections (measured 2026-07-30, tree `e545f7b`)

Three independent measurement passes over the tree. Where these disagree with the body
above, THESE are the counted numbers and the body is the estimate.

### The affordance surface is 30 production call sites, not 136

The 136 figure conflated three different things. Counted properly:

- **61 GenServer entry points** across 13 modules (74 with `start_link/1`), of which **18
  are reads**, 37 are commands, and 6 are CAS-shaped mixed read-and-write. The strategy's
  "~50 entry points, ~25 reads" over-counted reads by 40% — 30 public functions in those
  modules are pure helpers or direct DB access that never reach the process.
- **23 DB-level samplers, 96 `lib/` call sites** — but `Org.get/2` alone is 47 of the 96
  and is an entity fetch, not a gate; `Archetypes.get/1` and `Application.draining?/0` are
  `:persistent_term` reads, not DB reads at all. True DB samplers: 81.
- **Outside `DB.query/3` (194 sites, obviously not deletable), the entire process-owned
  read surface is 30 production call sites.**

**Consequence: Guard B does NOT trip its own ~50-site abandon criterion once scoped to
process-owned state.** It was tripped only by counting reads that are not gates.

**Four reads have zero production callers** — `AdapterCoordinator.generation/2`,
`Acp.Conn.pending_count/1`, `ConnRegistry.count/1` (all test-only probes), and
`Ledger.prior_adapter_generation/3` (zero callers anywhere — dead code). Deleting these
is the cheapest genuine affordance removal available.

### The txn-handle change has a cheaper shape than adding twins

**28 `foo`/`foo_in_txn` pairs already exist** (21 public/public), across 48 distinct
`*_in_txn` functions with 187 `lib/` call sites. **10 are already read-only**, including
two exact precedents: `SubagentMarkers.stopped_in_txn?/2` (a boolean predicate) and
`WorkItems.state_in_txn/2`, whose doc says it exists *because* it is a gating read.

Three idioms are in tree. The strategy assumed (b), the duplicating form both existing
read pairs use (~10 lines each). But `Roles.create!/4` (`roles.ex:47-70`) demonstrates
**(c): one polymorphic name with a `%Txn{}` clause and a `db` clause** — no second name,
no duplicated SQL, **no caller changes at all**. That is the cheapest shape and the one to
use.

Two caveats the body misses:
- `Adjudication.open_for_session?/2` and `RailRemedy.live?/3` currently swallow
  `{:error, _}` into `false`; a `Txn.q` version raises and rolls back. **Behavior change,
  not just a signature change.**
- **`Application.draining?/0` is `:persistent_term`, not SQLite.** No transaction handle
  can make F20 atomic without first moving the drain flag into the DB — which is exactly
  the move the probe ruled out. F20's fix must take the other route (pass a predicate).

### F27 is a platform-parity break, not a nit — NEW

Measured on macOS with the real binary: a missing check script exits **band 10**
(`sandbox-exec` reports the `execvp` failure and the wrapper survives). On Linux,
`platform::command` is `Command::new(script)`, so the spawn itself fails and the `Err` arm
returns **band 30**.

**The same failing rail check yields a different verdict depending on which OS ran it** —
which `contain.rs`'s own module header and the comment at `:1236-1241` explicitly forbid
("a rail author cannot tell from a verdict which OS ran it"). Reframe F27 from a
refusal-semantics improvement to **parity restoration**, with a shared pre-spawn
existence/executability check landing both platforms on 10. The Linux half is code-reading
only and needs a live run to count.

### Scheduling: F24 and F25 are one pass

Both must thread through the same five ceremony signatures
(`run_provider_onboarding`, `run_api_key_onboarding`, `run_openai_onboarding`,
`run_anthropic_onboarding`, `bank_openai_api_key`). One `Ceremony { endpoint, deadline }`
context is ~50 lines once, versus ~35 + ~35 done separately. F26 is the cleanest single
buy in the Rust set: mechanical, one file, and a genuinely deterministic fail-before via
the existing `FakeIo` FIFO.

`ceremonies.rs run_bounded` shares F4's shape but is **safe** — its `killpg` runs only on
the not-yet-reaped branch.

## Two rulings, so nothing sits blocked

Both were marked "product decision" above. Both are in fact forced by tenets already
written in `tightbeam.md`, so they are ruled here and recorded rather than escalated.

### Class 6, the quarantine claim: DELETE the claim, record the protection as a proposal

`SessionLane`'s moduledoc states that a lane will not start the next queued turn until an
orphaned ACP request is observed resolved. `quarantined` is initialised `false`
(`session_lane.ex:37`), read once (`:196`), and written NOWHERE; the resolver's signals are
dropped by a catch-all (`adapter.ex:514`). The mechanism that would feed it,
`Conn.pending_count/1`, has zero production callers.

Ruled: **delete the claim.** Nobody requested this protection, it was never built, and the
system has run without it. Deleting the comment changes no behaviour — it only stops the
module lying to everyone who reads it, and a false safety claim is worse than a stated
absence because it suppresses the very question that would surface the gap. The protection
itself is recorded as a ROADMAP proposal so the idea is not lost; it earns implementation
if and when an orphaned request is actually observed corrupting a following turn.

This unblocks F20 and the Class 3 work, both of which were waiting on it.

### F3, partial model application: the HARNESS wins, always

The open question was whether a partially-applied harness model may exist. It may exist
transiently, and the tiebreak is already settled by two tenets:

- **T2 — the harness owns conversational truth.** What model is loaded in a running agent
  is the harness's fact, not the substrate's.
- **T-SOURCE — every fact has one owner; ask, don't cache.**

Therefore: the substrate's record is a PROJECTION, the harness is the truth, and on
divergence the record is reconciled FROM the harness — never the reverse, and never by
picking whichever was written last. A transient disagreement is acceptable only if it is
self-healing by re-reading the owner. F3's defect is ordering around a fence that already
exists, not a missing fence.

### Correction to the F26 ruling: a failed identity check is a MALFUNCTION, not an empty result

The original ruling here said an identity check that fails to run should "drop the
candidate, matching Linux." The probe lane implemented that faithfully — and because a
failed `ps` yields no identity data for ANY pid, "drop the candidate" becomes
`raw.processes.clear()`: the probe reports **zero processes** whenever that one 1000 ms
`ps` times out. On a box running parallel lanes (eezo reaches load ~44) that is not rare.

**That is a sensor malfunction reported as a negative reading — the exact failure mode
ruled out earlier this session** ("a timeout must never silently deny work"; dark-factory
doctrine, `rails-mechanism-v1.md` §A3). An empty process list is a positive claim that
nothing is running, and downstream consumers cannot distinguish it from a true absence.

**Corrected ruling — three outcomes, not two:**
- identity check ran, pid present and unchanged → **keep**
- identity check ran, pid absent or start time changed → **drop** (it died or was recycled)
- identity check **did not run** → the process section is **indeterminate**. Surface it as
  a malfunction through the existing `note_failure` path and let the consumer decide. Do
  NOT clear, and do NOT silently retain unverified rows as though they were verified.

The original ruling was under-specified: it named two outcomes for a predicate with three.
This is the same defect class as the findings being fixed — a decision made on a fact
(process identity) that was never actually obtained.

## Ruling: the harness wins on model, always

Flynn, 2026-07-31. The running agent owns which model it is on. The `sessions.model`
column is a CACHE, not a source of truth.

This was never stated anywhere, which is the defect underneath three failed attempts at the
divergence bug: the code treats the record as the SEED
(`Adapter.new_session(adapter, session.model, ...)` at `gateway.ex:1785`,
`Adapter.load_session(adapter, ..., session.model, ...)` at `:2197`), while every fix was
written as though the harness were authoritative. Both behaviours were defensible because
nothing ruled between them.

**What the ruling settles:**
- **In-session swap:** harness confirms, record follows. Already the intent.
- **Reattach / residency reload:** the harness's model wins. Do NOT push the record into a
  harness that already has one.
- **New session creation:** no conflict — the harness has no model yet, so the record or the
  archetype default seeds it. Seeding is not overriding.
- **Adapter restart with an empty cache:** the answer is UNKNOWN and must be reported as
  unknown. Falling back to the record launders a stale value into a recovery decision.

**The dependency:** reattach can only honour this if the harness's current model is
READABLE — returned by the load, carried in session state, or pushed via an update. If the
shipped ACP protocol offers no read path (investigation in flight), then "harness wins" is
unimplementable at that one seam, and the honest response is to record the reattach seed as
a known deviation rather than pretend otherwise.

**Consumers that DECIDE from the cache and must read the owner instead:** the adjudication
brief handed to a mind (`gateway.ex:1533`) is the highest-consequence — a stale premise
produces a confident wrong recovery decision. Then reasoning-level composition (`:3193`)
and the capability check (`:1140`).

## SUPERSEDING RULING: user intent wins; the record is canonical only when known

Flynn, 2026-07-31. This replaces the "harness wins" ruling recorded above, which was
reasoning from an incomplete picture.

**The principle: the user always wins, regardless of our own buggy display.** Our record
may be wrong. That is acceptable. Overriding a user's explicit instruction to keep our
bookkeeping tidy is not.

**The design:**
- The substrate stores model / thinking / fast and treats the stored value as canonical
  FOR WHAT IT PUSHES. We always push — we do not attempt to mirror harness state.
- Push points: session create, reattach, and before a turn. Pushing asserts the value at
  the point of use rather than trying to hold a remote copy in sync, which is impossible.
- **Best-effort capture of in-harness commands.** `/model X`, `/thinking`, `/fast` pass
  through the substrate AS ORDINARY TEXT on their way to the harness (proven by the J6
  client-e2e journey, which posts `/model` as text and asserts it completes). We can parse
  them on the way through and update the record BEFORE any push, so the push carries the
  user's intent instead of reverting it. No protocol support required.
- **When capture is impossible, the record is UNKNOWN and we do not push.** A bare
  `/model` opens an interactive picker inside the harness: we see the command, never the
  choice. Recording `unknown` and leaving the harness alone is what makes the user win. A
  missed capture must degrade our DISPLAY, never the user's selection.
- On a fresh session with nothing specified, the harness picks its default; capture
  whatever the create response reports, else `unknown`.

**Why not the alternatives.** Mirroring harness state is impossible — ACP offers no
owner-read while a session is resident. Pushing without capture is user-hostile: the user
types `/model`, their next turn silently reverts, and it looks like their own action did
it. The frequency of pushing trades our accuracy against their autonomy, and only reliable
capture buys both.

**Known gaps, stated rather than hidden:**
- Bare interactive `/model` — capture impossible, record goes unknown.
- A harness changing model on its own (fallback after error) — invisible to us.
- Seeing a command is INTENT OBSERVED, not STATE CONFIRMED: a harness may reject the
  model the user asked for. The push at point-of-use is what confirms it.
- If ACP later exposes a hook or a model-change event, capture becomes reliable and the
  unknown cases close. Until then this is the best available and the failure is rare.

**Consequence for work in flight:** `model-fence-fix` implemented harness-wins at reattach
— the record's model is ignored and the harness configuration wins. Under this ruling that
is backwards: reattach must push the stored value WHEN KNOWN, and leave the harness alone
when unknown.

## RULING: parking records three states, and always ends dead

Flynn, 2026-07-31.

"Parked" is not a boolean. The record carries which of three things happened:

1. **asked to close** — the close was requested
2. **closed gracefully** — an actual close was DETECTED, not assumed
3. **killed** — the grace period expired and we terminated it forcefully

Grace period: **10 seconds.**

**Why forceful termination is correct, not a fallback.** A harness asked to close may keep
working for a while. But as far as the user is concerned it is dead the moment they see it
parked, so any work it does after that point is unexpected — it can write, spend budget, or
act on a session the user believes is finished. Letting it continue is worse than killing
it. So we kill it and record that we did.

**In all cases we make sure it is dead.** The papertrail distinguishes a graceful close
from a kill, but the outcome is the same: not running.

**Implementation consequences:**

- The current `park_provider_runtime` reports success on ENQUEUE. Under this ruling that is
  legitimately state 1, but states 2 and 3 do not exist yet — there is no detection and no
  kill. That is the gap, not the enqueue itself.
- The 10 s grace is a sanctioned use of a number: it BOUNDS WAITING, it does not decide an
  outcome. The outcome is decided by the observable event (closed / not closed). Compare the
  rail-exec 2000 ms budget, which decides a verdict and is therefore the wrong shape.
- **Verify death, do not merely signal it.** Established tonight: a TERM does not kill a
  shell spin loop, and a signal sent to a pid already released by `waitpid` can hit an
  unrelated process under pid reuse. The kill path must confirm the process is gone and must
  never signal a pid it no longer owns.
- A close that never completes and is never killed is the failure this ruling exists to
  prevent; the absence of a terminal state in the record is itself the alarm.

## PRINCIPLE: record the process, do not abstract it into a verdict

Flynn, 2026-07-31, generalising from the parking ruling.

**Do not abstract a complicated process into a simplified outcome.** Closing a harness is
complicated and fails in several distinguishable ways. So record the whole attempt as
faithfully as we can: asked to close, close detected, grace expired, killed, confirmed dead.
Best-effort throughout, but each step recorded as what it was.

**Why this is the root of tonight's recurrence.** Every defect that came back repeatedly had
the same shape: a multi-step, failure-prone reality collapsed into a single value the
representation could not honestly express.

- "parked" as a boolean, when the real outcomes are asked / closed / killed / never resolved
- "the current model" as one string, when there are three copies and a state where nobody
  knows
- "the event was saved", when it might have been received and then lost with no trace

When the representation cannot express what happened, the code MUST pick something untrue.
Different fixes then pick different untruths, which is exactly why the same defect kept
reappearing under new names. The bug was never in the fixes; it was that the record had no
room for the answer.

**How to apply.** Before fixing a recurring defect, ask what states the underlying process
actually has, and whether the record can express all of them. If it cannot, widen the record
first. A boolean that has to stand for four outcomes will be wrong three ways.

**This is squarely the substrate's job.** The substrate records neutral truth and produces
the papertrail; it does not summarise on the product's behalf. A verdict is a projection,
and projections belong to whoever consumes them — not to the record.
