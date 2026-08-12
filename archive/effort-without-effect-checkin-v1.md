# Effort-without-effect check-in — parent-adjudicated progress gate — v1

> **SUPERSEDED — see `effort-checkin-v2.md`**, which replaces this spec's
> dispatch-anchored git-motion semantics. The adjudication-episode machinery
> referenced here was separately deleted 2026-08-05. Retained as history. See `adjudication-deletion-amendment.md`.

Status: READY (gate-cleared 2026-07-25, Sol-high round 9: zero blocking; trajectory 8→6→5→7→4→4→1→1→0 — the r4→r5 descope was the inflection). r9 supersedes r8 after its NOT-READY(1)
gate (trajectory 8→6→5→7→4; the r5 descope held — its four repairs passed — and
exposed four lifecycle/authority holes r6 closes: the action menu now names verbs a
parent can ACTUALLY call — adjudication episodes are turn-failure machinery and not
invocable from a request; workspace-moving transitions re-arm brackets; self-dispatch
routes the check-in one rung up).
Flynn-directed ("a harder timeout that's not based on silence — something that asks a
parent to see if a child is looping out of control"). Additive; composes from landed
machinery with THREE named additive semantics r1 falsely claimed away (internal wake
consumer; effort ruling verb; expecter routing on decision requests). Sequenced AFTER
the harness-adapter seam merges (the probe touches the workdir surface the seam
refactors around). Ground truth: main `5ae730c`.

## The failure this closes

The rework-stall: a dispatched coder burns turns and tokens while never editing its
worktree — reading, planning, narrating. It defeats every existing sensor because they
all measure EFFORT signals, and effort is exactly what the stall produces:

- The turn timeout is a liveness detector. The stall ends turns normally; the timer
  resets every turn. Only true silence fires it.
- The no-filing prod is answered with a sincere progress attest ("still mapping the
  blast radius"). Filings are self-reported; the sensor is satisfied.
- Duration tuning is the wrong axis: shortening the timeout kills legitimate long
  turns; the orbiter still ends turns on time.

The distinguishing observable is EFFECT: the transcript is the agent's account of
itself; the worktree is the world's account of the agent. Separating deep legitimate
study from orbit is a JUDGMENT, which belongs to the party that opened the assignment —
not to the substrate and not to the child.

## Mechanism

### 1. Scope contract — the probe needs an authoritative root (r1 F1)

`dispatch` gains an optional **`workdirRoot`** param: one explicit checkout root,
relative to the holder's session workdir, `..`-free and contained (validated at
dispatch like a file claim; absolute paths rejected). Absent → the holder's session
workdir itself (derived with the PURE `Placement.workdir_path/2`, never the
ensure-writing `holder_workdir/2`). Nested repos inside the root count: effect is
computed over the whole subtree. **Probe-unavailable is its own outcome** — root
missing, SSH unreachable, git errors — reported in the check-in brief as
"unobservable", never conflated with "zero edits" (an unobservable workdir is itself
something the parent should rule on). Remote holders: the probe runs through a
BOUNDED Placement-owned SSH command (stat/git status under the root, fixed timeout) —
a new narrow Placement capability, named here because P3 producers reject remote
holders today.

### 2. Effect definition (r1 F10 — decided, not deferred)

Effect = any of, since the generation baseline: (a) a tracked-file content change
under the root, (b) an untracked file created under the root (build output and editor
droppings INCLUDED — v1 deliberately accepts coarse effect; a coder looping through
commands that touch the tree defeats this sensor and is out of scope), (c) a commit
reachable from the root's HEAD that the baseline lacked. Deterministic, computed from
one snapshot comparison against the generation baseline.

### 3. The bracket — arm at dispatch, generation row, cancel on close (r1 F4, F7)

The transaction that opens an assignment via `dispatch` (bare `assign` arms nothing)
also inserts one row in a NEW table `effort_checkin_generations`:
`{assignmentId, generation (monotonic per assignment), state: armed, baseHorizonMs
(frozen from config at arm time — later config changes touch only future
generations), multiplier (1), armedAt, terminalSeqWatermark (ledger seq at arm),
holderKey, host, root, baseline}` — where `baseline` is a PER-REPOSITORY MANIFEST
(r4 F7): the probe enumerates git repositories under the root (the root itself
and nested checkouts) and records, per repo, {repo-relative path, HEAD, tracked-
state hash} plus one SORTED UNTRACKED NAME LIST for the whole subtree (a LIST,
not a hash: creation = a name present now and absent from the baseline list
COUNTS; deletion is ignored). A root missing/unreachable at arm time records
`baseline: unavailable`, and the first probe reports unobservable` — and arms one TIMED wake (`dueAt = armedAt +
baseHorizonMs * multiplier`) whose id is stored on the row (`wakeId`).

The bracket cancels — via a NEW origin-gated `Wakes.cancel_in_txn/3`, invoked inside
the closing transaction — on EVERY assignment-closing path: completion attest,
**surrender** (r1 F4's omission), revoke, retire-strand. "Cancel" always means the
CURRENT GENERATION; monitoring is per-generation, never permanently lost while the
assignment is open. **Closes and holder-wide resets also terminalize outstanding
requests (r3 F3):** the same transaction marks any OPEN effort request for the
affected assignment(s) `superseded` and cancels its deadline wake — so a request can
never outlive the assignment (close-after-request) and, when a holder-wide ruling on
assignment A resets B's bracket, B's own open request is superseded rather than left
ruleable against obsolete evidence (two-request-holder).

**Ruling → bracket semantics (r4 gate descope — this mechanism owns TWO rulings):**
- `continue` — increments the generation (SAME baselines carried forward, so effect
  since the original arm still counts; multiplier ← min(multiplier*2, 4)); re-arm.
  Per-generation request dedup means a later zero-effect probe opens a fresh request.
- `dismiss` — the parent judges the situation fine or handles it out of band: the
  request terminalizes `ruled(dismiss)`, its deadline wake cancels, and the bracket
  re-arms a FRESH generation (new baselines) at BASE horizon — monitoring continues.
**Stronger action is NOT a ruling of this mechanism — and the menu names only verbs
a parent can ACTUALLY call (r5 F1: adjudication episodes are created by harness-turn
failure and `adjudicate` rejects without a notified episode; they are NOT invocable
from a request)**. The brief's action menu is the parent's ORDINARY powers: `wake`
the child with a pointed question; `revoke-assignment` and re-`dispatch` (to a new
mind, a new brief, or after fixing the spec); `retire` where the parent holds that
authority. Every one of those flows through paths this spec already covers: revoke
and retire CLOSE the assignment (bracket cancels, request supersedes), and a fresh
dispatch arms a fresh bracket. An INDEPENDENT adjudication episode (turn-failure
origin) acting on the holder while a request is open resolves ONE way per action
(r6 F2): actions that leave the workspace and assignment in place (park, swap)
leave the open request PENDING — it remains the monitor, and its ruling or the
assignment's close resolves the bracket. Actions that MOVE the workspace
(respawn's transfer; `tune set_host`) SUPERSEDE the open request in the same
transaction that re-arms the fresh generation — fresh workspace means the old
evidence is void, and a fresh probe re-opens if the stall persists.
The executor/transition touches this spec adds are exactly TWO, both
workspace-motion re-arms (r5 F3): the existing respawn TRANSFER and the existing
`tune set_host` workspace move each re-arm a fresh generation per open assignment —
new holder/host/root baselines — in their own transaction, so an armed generation
never observes a stale tree after the workspace legitimately moves.
A successful (effect-found) probe resets multiplier to 1 with its re-arm.

### 4. The probe — internal wake consumer, transactional, idempotent (r1 F2, F3)

**Additive wake semantic, named as such — WITH its schema change (r2 F4: today's
rows require non-null sessionKey/origin/prompt and the due loop prompt-delivers
every non-condition wake):** the wakes table gains
`consumer TEXT NOT NULL DEFAULT 'prompt'`; the prompt NOT NULL constraint relaxes
to `CHECK (consumer != 'prompt' OR prompt IS NOT NULL)`; `sessionKey` stays
non-null (an internal wake stores the holder key as its subject but is NEVER
delivered to it). The due loop branches on `consumer`: `'prompt'` = today's path,
verbatim; internal consumers dispatch to a registered callback — no turn, no
verdict attest, EXCLUDED from supervision's `pending_count` continuation signal
(so they cannot suppress the no-filing prod) and from owner wake inspection
(filtered by consumer). Two internal consumers exist in this spec: `effort_probe`
(§4) and `effort_deadline` (§5).

At fire, the callback: (1) INSPECTS the filesystem (outside any transaction — slow
I/O, possibly SSH); then (2) runs ONE transaction that: verifies the assignment is
still open AND the generation row's `wakeId` equals this wake AND state=armed;
CAS-marks the generation `probed(generation)`; then exactly one branch —
EFFECT/UNOBSERVABLE-OR-STALL:
- effect → update baselines + multiplier←1 + increment generation + re-arm (new
  wake, id stored); nothing else. Silent (red-tape test): no fact, no request, no
  row any party is shown.
- zero-effect or unobservable → write the evidence INTO the generation row
  (turns-since-armed counted as ledger turns with terminal status
  `delivered|failed|failed_unknown` past `terminalSeqWatermark`; minutes; probe
  outcome) and open the decision-request DIRECTLY in this transaction (r1 F8: no
  condition fact at all — `decision_requests.context` JSON carries the evidence;
  nothing subscribable is filed, so nothing can arm a gate; the reserved-kind
  apparatus is unnecessary and dropped).
Crash redelivery is a no-op by construction: the CAS on
`(assignmentId, generation, wakeId, state)` fails on a second delivery, and the
request insert is keyed `ON CONFLICT DO NOTHING` on `(assignmentId, generation)`.

### 5. Expecter routing and rulings (r1 F5, F6)

**Routing (additive, named — typed per r2 F6):** decision requests gain
`kind TEXT NOT NULL DEFAULT 'statute'`; effort requests are `kind='effort'` and
additionally carry `expecterSessionKey`/`expecterUserId` (exactly one, seeded from
the assignment's `openedBySession`/`openedByUser` — EXCEPT self-dispatch, r5 F4:
when the opener session IS the holder, seeding skips to the first rung ABOVE the
holder — the opener's own opener, else its owning human — so the monitored child
can never be its own expecter; the rung-advance skip rule likewise never lands on
the holder. USER-opened dispatch, r6 F4: `expecterUserId` = `openedByUser`,
`ownerUserId` = the same user, and the chain has ONE rung — the deadline re-arms
against that user until ruled), `lineageRung`,
`assignmentId`, `effortGeneration`, and `deadlineWakeId`. **Complete per-kind row
contract (r3 F1 + r4 F1):** for effort rows — `raiserId` = `process:tightbeam`
(the probe is the raiser; the CHILD is never the raiser and effort rows are
EXCLUDED from every raiser/owner-derived visibility path by kind);
`ownerUserId` = the opener session's owning human (satisfies NOT NULL and is the
deadline chain's terminal rung); `statuteName`/`actionKey` NULL via per-kind
CHECKs; the status CHECK gains `superseded`; decision for effort rows is
`continue|dismiss`. Uniqueness is the partial index
`UNIQUE (assignmentId, effortGeneration) WHERE kind='effort'` — the conflict-noop
key §4 relies on; statute rows keep today's shape untouched. Visibility for
effort rows derives from the CURRENT expecter columns only. The
existing `allow|deny|waived` decision constraint applies ONLY to `kind='statute'`;
effort requests record the effort action as their decision. **Authority is
principal-shaped, not origin-shaped (r2 F6):** a session-token call whose exact
session principal equals `expecterSessionKey` may rule; a user-token call whose
user equals `expecterUserId` (or the current rung's target) may rule; org-token
role calls carry no session principal and CANNOT rule effort requests; the admin
path is unchanged for statute requests. Opener retired or under
`adjudicationHold` at open time → route one rung up immediately.
**Delivery and deadline are one durable mechanism (r2 F7, hardened r3 F2):** the
request-insert transaction ALSO arms an `effort_deadline` internal wake and stores
its id in the request's `deadlineWakeId`. The post-commit notify to the expecter is
best-effort; the deadline wake is the guaranteed fallback. On fire, ONE transaction:
CAS on `(requestId, unruled, deadlineWakeId = this wake)` → advance `lineageRung`
AND ROTATE the expecter columns to the new rung's session/user in the same write
(authority derives from the CURRENT expecter columns, so the advanced-to ancestor
can rule and the skipped/held prior rung no longer can — r4 F3), skipping
held/retired rungs; terminal rung = the opener session's owning human, where it
keeps re-arming. Each rung gets a fresh full deadline interval (same config).
Cancel-and-replace the deadline wake (new id stored) — commit, THEN best-effort
notify the new rung. A
crash anywhere leaves either the old wake armed (redelivery CAS no-ops on wakeId
mismatch after a successful advance) or the new wake armed — intent is never lost,
no sweep. Ruling cancels the CURRENT deadline wake by stored id in the action
transaction.

**Rulings (r4 descope, menu per §3):** the effort-ruling verb is
`effort-rule --request <id> --action continue|dismiss` — the two rulings this
mechanism owns. The brief's action menu is §3's ORDINARY-POWERS list (wake;
revoke + re-dispatch; authorized retire), RENDERED RUNG-AWARE (r6 F3, r7 F1, r8 F1):
the menu is computed PER POWER — each of §3's ordinary powers appears iff THAT
power's own handler authorizes the rung's principal (revoke/re-dispatch iff the
revocation handler authorizes them; retire iff the retire handler authorizes
them; wake and the two rulings always). No lumping: a rung's menu is the exact
set of actions it can execute, derived from each handler's live authority rule,
never from role labels. Authority is never widened to make a menu item
callable: any rung that wants an action it lacks prompts the party that holds
it.

### 6. Boundaries

Harness-INTERNAL subagents stay parent-owned-opaque (subagent-markers invariant):
this mechanism attaches to ASSIGNMENTS; a parent orbiting via internal fan-out is
caught by the check-in on its OWN assignment one level up. Sessions with no
assignment are out of scope. The child is NEVER probed, prompted, informed, or
auto-killed by this mechanism; the parent may wake the child with a pointed
question before ruling — the parent's move, not the mechanism's.

## Non-goals

- No auto-kill, auto-retry, or substrate-decided remediation (determinism brackets
  inference).
- No transcript/token heuristics; the probe reads only the world.
- No periodic sweep; brackets arm/cancel at their events and die with the wake
  machinery if it dies.
- No changes to the turn timeout, the no-filing prod (explicitly shielded by the
  consumer discriminator), or statute escalation's decision shape.
- No fine-grained effect classification (v1 accepts coarse effect; §2).
- **No new ruling executor** (r4 descope): park/swap/respawn/stop stay the existing
  adjudication machinery with their existing semantics, authority, lease behavior,
  and blast radius; this mechanism neither wraps, fences, nor re-validates them.
- Serial wake-scheduler latency under many simultaneous remote probes is ACCEPTED
  for v1 (r2 C10): each probe is bounded by the fixed SSH timeout, and dispatched
  fan-outs at current scale keep the sum small. If probe volume grows, bounded
  async probe workers preserving the per-wake CAS are the named follow-up.

## Required proofs (fail-on-revert)

1. Dispatch (with and without `workdirRoot`) arms exactly one generation row + one
   `effort_probe` wake in the opening transaction; completion, surrender, revoke,
   and retire-strand each cancel in theirs (via `cancel_in_txn`). Bare `assign`
   arms nothing. `workdirRoot` validation rejects absolute and `..` paths.
2. Effect present (each of: tracked edit, untracked create, new commit — three
   cases, real workdir) → silent probe: no request, multiplier reset to 1,
   generation incremented, re-armed. Zero-effect → exactly one decision-request
   with evidence (turns counted only from terminal statuses past the watermark) in
   context JSON. Unobservable root → one request marked unobservable, distinct
   from zero-edits.
3. Idempotence: a redelivered probe wake after a crash-between-effects is a no-op
   (CAS fails / request conflict-noop) — proven by driving the callback twice.
4. The probe wake never creates a turn, never appears in `pending_count` (a holder
   with ONLY a probe wake still draws the no-filing prod), and never appears in
   owner wake inspection.
5. Rulings: continue increments the generation (baselines carried), re-arms at 2x
   then caps at 4x, a subsequent effect-probe resets to base, and a later
   zero-effect probe after a ruled continue opens a FRESH request (dedup is
   per-generation). Dismiss terminalizes the request, cancels its deadline, and
   re-arms a fresh generation at base horizon. An assignment closed by ANY route
   (including an adjudication-executor stop/retire) cancels its bracket and
   supersedes its open request; the existing respawn transfer re-arms a fresh
   generation per transferred assignment in the transfer transaction.
6. Expecter authorization: the opener SESSION (non-admin, session-token principal)
   can rule its own request; an unrelated session cannot; an org-token role call
   cannot rule an effort request; statute requests keep the admin path untouched.
   Opener-retired and opener-held requests route one rung up at open; an unruled
   request past deadline CAS-advances through the spawnedBy chain, skipping held
   rungs, to the owning human (two-level chain test). The deadline wake is armed in
   the SAME transaction as the request insert: a simulated crash between commit and
   the post-commit notify still yields a surfaced request when the deadline fires.
7. Remote holder: the bounded SSH probe path computes effect on a satellite workdir;
   SSH failure yields unobservable, not zero-edits.
8. Red-tape parity: a busy org (N active assignments, all editing) generates ZERO
   check-in artifacts visible to any party over multiple horizons.
8b. Lifecycle ties: completing an assignment with an OPEN effort request
   supersedes the request and cancels its deadline wake in the closing
   transaction. Deadline-advance crash test: kill between advance-commit and
   notify — the new rung's wake fires and surfaces the request; redelivery of the
   OLD deadline wake no-ops on wakeId mismatch; after an advance, the NEW rung's
   session can rule and the prior rung cannot.
8c. Baseline representation: a nested-repo workdir distinguishes an inner-repo
   commit as effect; an untracked DELETION is not effect while a creation is
   (list semantics); a root unavailable at arm yields baseline=unavailable and an
   unobservable first probe.
8d. Migration: a database created by the pre-change wakes/decision_requests
   schema ensures cleanly through the rebuild path and preserves existing rows.
9. feature_smoke probe: dispatch → idle past horizon → decision-request lands at
   the dispatching session → `effort-rule --action continue` widens the horizon →
   a second idle horizon opens a fresh request → the parent rules nothing and
   instead revokes the assignment and re-dispatches to a new mind → the old
   bracket cancels + request supersedes with the revoke; the new dispatch arms a
   fresh bracket.
10. Workspace motion: `tune set_host` on a holder with an armed generation re-arms
   against the new host/root in the tune transaction (probe after the move
   observes the NEW tree); same for respawn transfer. With an OPEN request at
   motion time, the request is superseded in the motion transaction and a fresh
   probe can re-open; park and swap leave an open request pending and ruleable.
11. Self-dispatch: a session dispatching to ITSELF seeds the expecter above the
   holder; the holder session cannot rule the resulting request.
12. User-opened dispatch: a request routes to the opening USER, the deadline
   re-arms against that user (single-rung chain), and the user's ruling
   executes.
13. Menu-authority intersection (per-power, pinned ownership case): for a
   session-opened assignment whose holder is owned by non-admin human H2 while
   the opener chain terminates at non-admin human H1 ≠ openedByUser: H1's menu
   is exactly {wake, continue, dismiss} ∪ {retire iff the retire handler
   authorizes H1 for that session} and NO revoke/re-dispatch; H1's rulings
   execute; H1's revoke attempt is refused by the unchanged handler. The proof
   asserts the exact rendered menu set for this case.

## Migration contract (r4 F2)

Both altered tables need CONSTRAINT changes SQLite cannot ALTER in place
(`wakes.prompt` NOT NULL; `decision_requests` status/decision/nullability CHECKs):
they migrate by TABLE REBUILD following the repository's established
attests-rebuild pattern (create-new, copy, swap, in the schema-ensure path), and
the proofs include an UPGRADE case: a database created by the pre-change schema
ensures cleanly and preserves its rows.

## Component touches

Assignments (arm in dispatch-open txn; cancel_in_txn call sites on all four close
paths; `workdirRoot` param + validation); NEW `effort_checkin_generations` table;
Wakes (`consumer` discriminator + internal callback registry + `cancel_in_txn/3` —
the named additive semantics); Supervision (pending_count exclusion by consumer);
Escalation/decision_requests (expecter columns + rung + deadline-advance wake +
scoped non-admin ruling authority); the effort-ruling verb (continue|dismiss) + the
workspace-motion re-arm hooks (respawn transfer, tune set_host); CLI-surface
amendment (cli-surface-v1.md enumeration + args.rs) adding `effort-rule` and
opening `revoke-assignment` to agent callers whose principal the handler already
authorizes (r6 F3 — the CLI currently rejects the verb for agents even where the
handler would authorize the opener session); Placement (pure-path probe + bounded SSH probe command);
config (`:effort_checkin_horizon_ms` / env, frozen per generation); feature_smoke.
