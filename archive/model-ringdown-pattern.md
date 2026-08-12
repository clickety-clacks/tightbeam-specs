# Model adjudication — model choice is inference at every edge

(Formerly "model ringdown." The filename is kept stable for inbound references; the pattern
is now model *adjudication*.)

> **DEAD AS MECHANISM — banner added 2026-08-12.** Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`).
> Everything mechanical in this file — episodes, holds,
> `sessions.adjudicationHold`, the ladder, the `adjudicate` verb,
> park/recovery wakes, the boot reconciler — was deleted from the tree. The
> PRINCIPLE ("model choice is judgment, done by inference") survives in
> `production-machine-v1.md`; GAP-1 is re-homed to `harness-support.md`.
> Retained as history — do not build from this file. See `adjudication-deletion-amendment.md`.

Status: DRAFT r11 (2026-07-21; applies the whole-lattice hole-hunt findings — ruled park-wake
scope `"<harness>:<identity_name>"`; the pinned owner `adjudicate` verb (auth + per-action
transaction); schedule-then-check for the park wake (no-replay cursor); concrete hold storage
(`sessions.adjudicationHold`) + the W6 fire-transaction arm seam; owner-attributed
`adjudication_block` fact. Completion-clears at r10; pending-keyed boot invariant at r9;
R1/R2/R6 at r7; boot-never-arms at r8; R3/R5/W7 at r6). r1/r2 built a
substrate-driven ringdown (an ordered chain the substrate walked mechanically); r3 deleted
that under Flynn's "inference at every edge" reframe; r4 made it implementable against the real
lifecycle; r5 fixed the parked-execution circularity and the barrier. r6 makes recovery-first
compatible with ledger FIFO (a **filtered claim** on `recoveryWakeId`), splits the episode's two
wake identities (`ownerWakeId`/`recoveryWakeId`) with deterministic `wire_idempotency` keys,
gives `claimed` episodes a real deadline clock, closes the freshness definition hole
(expired-cache/refresh-in-flight ⇒ `stale`), and normalizes every eager `create_spawn` denial
into the exhaustive Edge-1 union. The `gpt-5.6-sol[high] → claude-opus-5` chain here is an
EXAMPLE of preference data, not shipped policy.

## The pattern

Model choice is judgment, so it is done by inference — an adjudicating agent — never by a
substrate mechanism. The archetype's ordered model list survives, but its contract is now
**preference data**: "this is the way I do things," a strong prior the adjudicator weighs
alongside the model-affinity characterizations (`model-selection.md`) and live state
(exhaustion, availability, catalog health). There is no chain iterator, no persisted position,
no condition→action policy the substrate executes.

Model choice happens at two edges, split by the real lifecycle (boot is lazy):

1. **Spin-up (eager checks only).** `spawn` eagerly checks what it can *before* any harness
   session exists — fresh-catalog membership of the requested model, and archetype/host
   validation. A failure returns a **classified denial** to the caller, who is already
   mid-inference and re-adjudicates inline — another model, harness, or plan — or blocks.
2. **Runtime (first turn onward).** Every harness-side refusal — `auth_failed`, `boot_failed`,
   `quota_exhausted`, `model_unavailable` — happens when a turn actually runs (the harness
   session is created lazily at first turn), never at `spawn`. The substrate classifies the
   condition and **wakes the session's owner/spawner** with it plus the preference context.
   The owner adjudicates — in-place swap, cross-harness respawn, a different model, or **block**
   (park when no available mind meets the job's quality floor). On a switch the affected
   session continues via a recovery wake. **Routing to the owner IS the loud failure; the
   substrate still never rings.**

EXAMPLE (illustrative only): a reviewer prefers `gpt-5.6-sol[high]` and lists
`claude-opus-5` as its next preference. On a mid-turn `usageLimitExceeded`, the substrate
does not silently swap to Opus. It fails the turn, holds the session, wakes the reviewer's
spawner with "reviewer exhausted Sol mid-turn; preference tail [claude-opus-5]; here is live
availability," and the spawner decides to move it to Opus. The reviewer is then woken to
re-derive from the facts and continue on Opus.

## Adjudication at every edge — the canonical model

**The substrate's only behaviors** around model choice are: **classify** the condition,
**surface** it, **route it to inference** (return-to-caller at spin-up; wake-the-owner at
runtime), hold the session and hold a **fail-loud floor**, and **escalate through supervision**
when the adjudicator does not answer. It does not choose a model, rank preferences, walk a
chain, or carry a policy that encodes ring-vs-fail. Those are inference.

**The decision space at every edge is {switch to an acceptable mind, block}.** Every job has a
**quality floor** — the least capable mind acceptable for it — an org preference expressed in
the model-affinity characterizations (`model-selection.md`), NOT in the substrate. When an
available mind meets the floor, the adjudicator switches to it. When none does, the adjudicator
**blocks** rather than degrade below the floor: *"I'd rather block than switch to haiku because
it's all that's available."* Blocking is a correct, chosen outcome — not a failure and not a
degrade — always recorded (see Parked state), never silent and never a default. The substrate
does not know the floor; the adjudicator applies it and either switches or parks the work.

**The trade, named honestly.** Recovery costs a **wake round-trip to an inference agent**
instead of zero-inference chain-walking. Accepted deliberately: model choice is judgment, not
a lookup. The failure being designed away is a session dead-ended **silently or by default**
when its adjudicated mind becomes unavailable — not blocking itself. Blocking below the floor
is the right call; what is forbidden is blocking without a decision and without a record.

**Standing guidance can make the decision fast, not mechanical.** An owner MAY carry guidance
(`model-selection.md`) that makes "Sol exhausted → move to Opus" a near-reflex adjudication —
still an inference made with the preference data in hand, fast because the guidance is good,
not because the substrate decided. Guidance may note, as adjudicator advice, that an
`ephemeral` session (per-task, retired after) can be respawned across harnesses cheaply.

## Substrate / product (kungfu) boundary — governing principle

- **Kungfu / inference (product side):** every model choice; the ordered preference list
  (`model_preferences`); the model-affinity characterizations; the **per-job quality floor** (an
  org preference in the characterizations guidance); the owner's adjudication at both edges,
  including the choice to block below the floor. All judgment, all guidance-shaped.
- **Substrate (mechanism only):** classification with precedence; catalog membership with
  freshness; the durable adjudication episode; the session hold; the owner-initiated
  model-swap apply + its serialized/CAS mutation seam and `lifecycle_events` record;
  recovery-wake and barrier-cut semantics; the runtime→wake-owner routing; the parked-block
  self-condition-wake wiring (wake-on-fact S1); the fail-loud floor and supervision escalation.
  No model choice, no chain, no ring/fail policy lives here.

The substrate classifies and routes; it never decides which model runs.

## The preference data (`model_preferences`)

The archetype manifest field is `model_preferences` (implementation renames the shipped
`fallback_models` key and the playground manifests in the same change — a rename, not a
dual-key read); its contract changes from "a chain the substrate
walks" to **an ordered preference list adjudicators read** — a strong prior surfaced to any
agent adjudicating a model choice for that session, weighed against live state and affinity
characterizations. The substrate never iterates it.

```toml
name = "reviewer"

# Adjudicator advice: per-task sessions retired after their work hold little
# context, so an adjudicator may respawn them across harnesses cheaply. A hint
# read by inference, not a substrate branch.
ephemeral = true

# PREFERENCE DATA — the archetype's stated fallback order, read by adjudicators
# at both edges. Not a chain the substrate walks. Top-level (a sibling of
# [defaults], NOT nested inside it — the loader reads only top-level
# `model_preferences`, archetypes.ex:1167). Catalog-valid provider ids only.
model_preferences = ["claude-opus-5"]

[defaults]
harness = "codex"
model   = "gpt-5.6-sol[high]"   # the stated first preference
```

- Entries are catalog-valid provider ids in the existing `name[effort]` syntax
  (`parse_model_ref/1`, `adapter.ex:514`). `claude-opus-5`, not the alias `opus-5` (the
  derived catalog rejects aliases, `derived-model-catalog-v1.md:19`).
- Validation is unchanged in shape (a list of strings). No condition→action policy schema
  exists — nothing for the substrate to execute, nothing to validate beyond the list.
- `ephemeral` is adjudicator advice only (default `false`; `kind='main'` a hard floor of
  long-lived). It authorizes no substrate action.
- **Implementation-lane flag:** the source moduledoc example still nests `model_preferences`
  under `[defaults]` (`archetypes.ex:23`); the loader reads only the top-level key, so that
  propagating example must be corrected to a top-level sibling of `[defaults]`.

## Ground truth today (recon, file:line)

**`model_preferences` is display-only data today.** Declared/validated in `Tightbeam.Archetypes`
(`archetypes.ex:27-31` moduledoc; validate at `:1167-1171` — a list of strings). Its only
consumers are projections: `session_status.display.modelPreferences` (`gateway.ex:661-678`) and
the `list` org-shape (`gateway.ex:1466`).

**Boot is lazy.** `spawn` does readiness checks, creates the logical session, and returns
(`gateway.ex:1627`); the harness session (`Adapter.new_session`) is created only when the first
turn runs (`gateway.ex:1093`). So no harness-side refusal can occur at `spawn` — including
`boot_failed`, which can surface *after* a successful spawn. Model is stored unvalidated at
spawn (`create_spawn` precedence `--model` → `archetype.defaults[:model]` → config default,
`gateway.ex:1635-1641`). Runtime change is `tune set_model` (`gateway.ex:1821-1863`); a lost
harness session enters the generic pointer fallback + context reset (`gateway.ex:1112`).
`tune set_harness` imposes the history barrier, broadcasting `stream_history_cleared` and
clearing through the current max sequence (`gateway.ex:1757-1783`).

**No automatic turn retry exists — and must not.** *"No automatic retries: `failed_unknown`
is terminal; nothing here re-sends"* (`ledger.ex:17`); recovery marks running turns
`failed_unknown`, *"never auto-retried; tools may have executed"* (`ledger.ex:224`). Recovery
is continuation-by-wake, never replay.

**The lane does not hold after a failure.** After a terminal the lane immediately claims the
next queued turn (`session_lane.ex:171`); nothing holds the session until owner action. The
failure path appends `[turn failed]` before any adjudication (`gateway.ex:817`). Terminal
publication is marked before `on_terminal` invokes supervision (`lane_manager.ex:73`) — a
crash-loss window for any reaction.

**The trigger conditions are NOT classified today** — structured terms the lane/event layer
stringifies. Model apply is TWO ACP mutations, base then effort (`adapter.ex:345`);
`load_session` deliberately **swallows** apply refusal because config options populate
asynchronously (`adapter.ex:221`). Gate attestation collapses any refusal/auth to
`:turn_error` → coordinator `:DOWN` (`adapter.ex:180, 397-412`; `adapter_coordinator.ex:154`).
Quota surfaces as a raw ACP term from `prompt_done` (`adapter.ex:297-309`). Auth 401 is not
detected at readiness (presence-only check, `spinup.ex:149-167`).

**The supervision/wake machinery both edges route onto exists.** `Tightbeam.Supervision` is
*"the serialized, durable reaction executor for stalled assignments"* (`supervision.ex:1`);
`ladder_target/3` walks the `spawnedBy` lineage and tops out at the owner's Main
(`Org.personal_session_key`, `supervision.ex:109-117`); escalation survives target retirement
by recording `reresolve_seed`/`rung` (`supervision.ex:370`); `Wakes.schedule/2` is the durable
wake insert and mints a fresh UUID each call (`wakes.ex:94`). **Suppression of a supervision
prod requires pending ledger work OR a pending wake for the *holder*** (`supervision.ex:177`);
a new attest merely resets counters before selecting another prod (`supervision.ex:224`).
`Wakes.pending_count`/`self_pending_count` are keyed by the wake's **target** session
(`wakes.ex:173`) — an owner-targeted wake does not pause the affected holder.

**The events table is CHECK-locked.** `events.kind IN ('verb','denied')` and `append_event`
requires `kind`/`verb`/`origin` (`event_log.ex:38, 84`) — it cannot represent a model swap.
`lifecycle_events` has an open `kind` and `(ts, kind, subject, detail)` columns
(`event_log.ex:133`); that is the swap record.

## Classification precedence (the central mechanism)

Classification runs at the real seam, first-match-wins:

1. **`auth_failed` (first).** Verify credential validity; a 401 / invalid-or-expired credential
   is `auth_failed` regardless of surface, because auth faults masquerade as boot or model
   failures. Diagnosed, never inferred from absence.
2. **`model_unavailable`.** A refused model apply (see the typed apply below). Distinguished
   from the async option-readiness race by bounded retry before classifying.
3. **`boot_failed` (residual).** Boot faults that are neither auth nor model refusal — and,
   because boot is lazy, they can arise at first turn *after* a successful spawn.
4. **`quota_exhausted`.** The runtime usage/limit-exceeded turn error.
5. **`other`.** Unclassified — fail-loud floor, routed to the owner as an opaque runtime fault.

The classified reason is what the substrate **surfaces** — to the caller at spin-up (Edge 1),
and in the owner wake at runtime (Edge 2). It is the input to inference, not to a substrate
branch.

## Catalog freshness

The freshness contract now lives in its authority: **`derived-model-catalog-v1.md`
§"Freshness contract (adjudication requirement)"** (amended by this lane). Membership answers
carry a health state `fresh | stale | unavailable(reason)`, partitioned on the data's age (not
the refresh's fate) for total coverage — any present-but-not-fresh data (a failed refresh OR an
expired cache while a refresh is in flight) is `stale`, and only a total absence of data is
`unavailable`. This spec consumes it: absence is
trustworthy only under `fresh`. Under `stale`/`unavailable`, absence is untrusted — a
Claude-catalog 401 surfaces as `auth_failed`/`unavailable`, never as "model missing" an
adjudicator might read as "just pick Codex." Edge 1 returns `catalog_unavailable` when it
cannot get a `fresh` answer.

## Edge 1 — spin-up: eager checks, classified denial to the caller

`spawn` checks only what it can before any harness session exists, and returns:

- **Fresh-catalog membership** of the requested model, plus the existing archetype/host
  validation AND the eager host-readiness probe `Spinup.ensure_ready` that `create_spawn`
  already runs (`gateway.ex:1645`). Boot is lazy, so `spawn` never creates a harness session
  and never sees a harness-side refusal (`gateway.ex:1093, 1627`).
- The denial union is EXHAUSTIVE over **every eager relay point in `gateway.create_spawn`**
  (`gateway.ex:1610`): `{model_unavailable | catalog_unavailable | unknown_archetype |
  config_denied | placement_denied, detail}`. Each existing relay normalizes into exactly one
  member:
  - `Archetypes.get → nil` → **`unknown_archetype`** (`gateway.ex:1606`).
  - `Archetypes.normalize_overrides → {:error, invalid_overrides}` (`archetypes.ex:671`) →
    **`config_denied`**.
  - `Placement.resolve → {:error, host_not_allowed | unknown_host}` (`placement.ex:406`) →
    **`placement_denied`**.
  - `Spinup.ensure_ready → {:error, host_unready | unknown_host | missing-credentials}`
    (`spinup.ex:199`) → **`placement_denied`** (same member as the placement denials above).
  - Handle creation via `Roles.create_in_txn!` → `{:error, %Roles.TransactionError{}}` relayed
    directly (`gateway.ex:1671, 1683`): `invalid_role_name` / `role_exists` → **`config_denied`**
    (same member as the override denials).
  - Fresh-catalog membership miss → **`model_unavailable`**; membership unverifiable because the
    catalog is not `fresh` → **`catalog_unavailable`** (retry later or escalate; NEVER read
    stale absence as "model missing").
  No `create_spawn` relay escapes the union — the enumerated points (`gateway.ex:1606, 1610,
  1671, 1683`; `create_spawn`'s `Spinup.ensure_ready`) are exhaustive.
- The caller re-adjudicates inline with its guidance and the session's `model_preferences` in
  hand, and either re-issues `spawn` with a new model/harness OR **blocks** (parks — see Parked
  state) rather than spawn below the floor. No context exists yet, so a switch has nothing to
  preserve and no barrier.

The substrate's job here ends at "refuse with a reason the caller can act on."

## Edge 2 — runtime: classify, hold, wake the owner

Any classified runtime condition — **`auth_failed`, `boot_failed`, `quota_exhausted`,
`model_unavailable`, or `other`** (all FIVE; the split from Edge 1 is lifecycle, not condition
kind — `other` is an opaque runtime fault the owner still adjudicates) — routes to the owner.
Routing to the owner IS the loud failure. Sequence, per the durable episode:

1. **Claim a durable adjudication episode (CAS).** Before any side effect,
   `INSERT INTO adjudication_episodes (…) VALUES (…, 'claimed', now) ON CONFLICT DO NOTHING`
   keyed by `(sessionKey, condition)` (schema below). The single statement is the atomic claim;
   a concurrent duplicate classification of the same condition loses the claim and does NOT
   raise a second wake (idempotent).
2. **Fail the turn and take the hold, atomically.** In one transaction: mark the turn terminal
   (`failed`, never replayed, `ledger.ex:224`), set the **session hold** (below), and — because
   this is adjudication-routed — **suppress the generic `[turn failed]` marker**
   (`gateway.ex:817`); the classified terminal and the hold commit together.
3. **Wake the owner/spawner.** Resolve the target via `ladder_target/3` (rung 1 = the immediate
   spawner; climbs to the owner's Main if gone) and `Wakes.schedule/2` a prompt carrying: the
   affected session, the **classified** condition, the current model, the `model_preferences`
   preference data, and live availability/catalog state — the adjudication brief. Thread the
   episode **correlation key** into the wake, and record `reresolve_seed`/`rung`
   (`supervision.ex:370`) so the wake survives target retirement. Episode `claimed → notified`.
4. **The owner adjudicates and acts** — an in-place swap (same harness, context kept), a
   cross-harness respawn (barrier), a different model, or **block** (park). A switch runs through
   the swap seam and, on success, the substrate delivers the recovery wake, enqueuing the pending
   recovery turn whose COMPLETION releases the hold (step below); a park schedules the
   holder-targeted condition wake and the hold persists until that wake's recovery turn completes
   (Parked state). Episode `notified → resolved` in both cases.
5. **Recovery wake to the affected session** (on a switch) once a model is chosen: sender
   `process:tightbeam` — *"Your previous turn failed: <classified reason> mid-turn. You now run
   on <model>. Re-derive state from the facts (work-item, attests) and continue."* Its ledger
   turn is stamped `turns.wakeId = recoveryWakeId`; **dedupe is the stored `recoveryWakeId`**
   (its deterministic `wire_idempotency` key returns the same wake on any recreate), backed by
   `turns.wakeId UNIQUE` at enqueue (`ledger.ex:42`). It is claimed first via the filtered claim
   and its completion clears the hold (Session hold).
6. **Escalation if the adjudicator does not answer.** The episode's `deadlineAt` drives it: on
   a supervision sweep past it with the episode still `notified`, escalate up the `spawnedBy`
   ladder (`ladder_target/3`, rotating `correlationKey` and re-resolving via the recorded
   `reresolve` fields), ultimately to the human's Main (`supervision.ex:225-247`). The
   **fail-loud floor** holds: the turn stays terminal-failed and visible; the held session does
   not silently proceed.
7. **Boot reconciliation** (the `lane_manager.ex:73` crash window — terminal publication
   precedes the supervision hand-off). Because both wakes carry deterministic `wire_idempotency`
   keys, reconciliation never guesses: recreating a wake returns the existing one. On boot,
   reconcile open episodes: `claimed` past `deadlineAt` → escalate (R3); `claimed` with the
   owner wake's idempotency key already enqueued but `status` not advanced → advance to
   `notified`; `notified` with no live owner wake → recreate (same id) and keep `notified`.
   **Boot reconciliation NEVER arms the filter.** The arm committed in the same durable
   transaction as the recovery-turn enqueue (Session hold / R1), so filter state survives restart
   by construction — there is nothing to re-arm. Reconciliation only VERIFIES the invariant
   *filter armed ⟺ its recovery turn is PENDING (enqueued and not yet completed) in
   the ledger* and repairs it in exactly one direction: an armed filter with no matching
   **pending** recovery turn (impossible if the transaction held;
   defensive otherwise) is **DISARMED** and the episode returns to its pre-delivery state so the
   normal delivery path re-runs. This is consistent with the hold-clears-on-completion rule: when
   the `recoveryWakeId` turn completes, the hold clears (the filter disarms) — the completed turn
   persists in the ledger, but it is no longer *pending*, so the biconditional still holds.

### Adjudication episodes (durable, idempotent — mirrors `rail_remedy_episodes`)

```sql
CREATE TABLE IF NOT EXISTS adjudication_episodes (
  sessionKey     TEXT    NOT NULL,
  condition      TEXT    NOT NULL,   -- auth_failed|boot_failed|quota_exhausted|model_unavailable|other
  status         TEXT    NOT NULL CHECK (status IN ('claimed','notified','resolved')),
  correlationKey TEXT    NOT NULL,   -- rotated on every (re)open; the response-liveness predicate
  ownerTarget    TEXT,              -- resolved ladder target at notify time
  ownerWakeId    TEXT,              -- the owner-NOTIFICATION wake (deduped independently)
  recoveryWakeId TEXT,              -- the holder RECOVERY/PARK wake (deduped; drives the filtered claim, F1/R1)
  reresolveSeed  TEXT,
  reresolveRung  INTEGER,           -- reuse supervision's retirement-survival fields
  deadlineAt     INTEGER NOT NULL,  -- set AT CLAIM (claim deadline), updated at notified (response deadline)
  openedAt       INTEGER NOT NULL,
  resolvedAt     INTEGER,
  PRIMARY KEY (sessionKey, condition)
);
```

**Two wake identities (R2).** An episode owns two distinct wakes — the **owner-notification**
wake (`ownerWakeId`) and the **holder recovery/park** wake (`recoveryWakeId`) — separate
columns, separately deduped. Each is scheduled through **`wire_idempotency`** with a key
derived deterministically from `(sessionKey, condition, correlationKey, purpose ∈ {owner,
recovery})`, so a re-schedule after a crash returns the **same** wake rather than a fresh UUID
(`Wakes.schedule` alone mints a fresh UUID each call, `wakes.ex:94`). The durable enqueue dedupe
of the recovery *turn* remains `turns.wakeId UNIQUE` (`ledger.ex:42`).

**Required single transaction (implementation change, not an assumption).** For the
deterministic key to prevent a duplicate wake, the wake insert, the `wire_idempotency` insert,
the episode `wakeId`/`status` UPDATE, and (where a recovery turn is enqueued) the filter update
MUST commit in **ONE** transaction. Ground truth today performs these **separately**
(`gateway.ex:1512`, `:1523`, `:1535`), so a crash between them can still mint another wake — the
adjudication path must fold them into a single transaction. That single transaction is what
makes boot reconciliation guess-free.

**CAS matrix — every transition is a single guarded `UPDATE … WHERE`:**

- **Claim** (`INSERT … ON CONFLICT DO NOTHING`, setting `deadlineAt = now + claim_window`) — the
  atomic claim; concurrent duplicate classifications of the same `(sessionKey, condition)`
  cannot both win (mirrors `rails-mechanism-v1.md §C3`). `deadlineAt` is set **here, at claim**
  (R3), so even a `claimed` episode that never advances has an escalation clock.
- **`claimed → notified`:** `UPDATE … SET status='notified', ownerWakeId=?, ownerTarget=?,
  deadlineAt = now + response_window WHERE sessionKey=? AND condition=? AND status='claimed' AND
  correlationKey=?`. Recreate the owner wake only if `ownerWakeId` is absent (its idempotency
  key makes the recreate return the same wake).
- **`notified → resolved`:** `UPDATE … SET status='resolved', recoveryWakeId=?, resolvedAt=now
  WHERE sessionKey=? AND condition=? AND status='notified' AND correlationKey=?`. The owner's
  response carries the `correlationKey`; a response whose key no longer matches is provably
  ignored. The `recoveryWakeId` recorded here is the switch's recovery wake or the park's
  holder-targeted condition wake; recreate only if absent.
- **Reopen** (a later occurrence after `resolved`): `UPDATE … SET status='claimed',
  correlationKey=<new>, ownerTarget=NULL, ownerWakeId=NULL, recoveryWakeId=NULL,
  reresolveRung=<reset>, deadlineAt = now + claim_window, openedAt=now, resolvedAt=NULL
  WHERE … AND status='resolved'`. Reopen rotates the **correlation key, both wake ids,
  timestamps, owner target, deadline, and rung** — so a stale response from the prior occurrence
  (old `correlationKey`) cannot resolve the reopened episode.

**Deadline protocol (R3).** `deadlineAt` is `NOT NULL` from claim. A supervision sweep past
`deadlineAt` while the episode is still open (`claimed` OR `notified`) escalates one ladder rung
(rotating `correlationKey`, re-resolving `ownerTarget` via the recorded `reresolve` fields,
extending `deadlineAt`) — never a new episode. A stuck-`claimed` episode escalates on the same
clock as a stuck-`notified` one. **Rotating `correlationKey` also rotates `ownerWakeId` (R2):**
because the owner wake's deterministic idempotency key includes `correlationKey`, a new
correlation is a new owner wake — the escalation transaction schedules the new owner wake to the
new `ownerTarget` and **cancels the old `ownerWakeId` in the same transaction**, so a late
response to the superseded wake is provably ignored (its old `correlationKey` no longer matches).

**Resolution does NOT release the hold** — see Session hold (F1/R1). Only COMPLETION of the
recovery turn (enqueued when the `recoveryWakeId` wake delivers) does.

### Session hold — a filtered claim (R1: recovery-first compatible with ledger FIFO)

r5 said "the recovery turn runs first," but the real claim selects the **lowest** `turns.seq`
(`ledger.ex:161`, `ORDER BY seq LIMIT 1`) while a delivered recovery wake **appends** a new
turn at the highest seq (`gateway.ex:526`) — so plain FIFO would run older queued prompts
first (r5 finding 1). The fix is a **filtered claim**, not a plain block:

- **While the hold is set, the lane may claim ONLY the turn whose `turns.wakeId =
  episode.recoveryWakeId`** — the claim SQL gains `AND wakeId = ?` (the recovery id) on top of
  the existing `ORDER BY seq LIMIT 1`. Queued turns, whatever their seq, are unclaimable until
  the hold clears. So the recovery turn runs first even though it has the highest seq, and no
  queued prompt runs on the dead model.
- **The filter arms in the SAME transaction as recovery-turn ENQUEUE — the one authoritative
  boundary, never at episode resolution (R1).** The hold itself (unfiltered — nothing claimable)
  is set atomically with the classified terminal (edge step 2). The filter gains its
  `recoveryWakeId` only at the moment a recovery turn exists to filter for:
  - **Switch:** the owner's swap resolves the episode AND enqueues the recovery turn in one
    transaction, which arms the filter.
  - **Park:** resolution merely records `parked` (no recovery turn yet, so no filter id);
    later, when the condition or timed-fallback wake **fires and delivers**, that delivery
    transaction enqueues the recovery turn and arms the filter. Resolution and arming are
    deliberately at different times for a park — resolution does not arm.
- **The recovery turn's completion clears the hold entirely**, and the lane resumes normal FIFO.

The hold is released only by that recovery turn's completion — never by episode resolution
alone (F1): a resolved-as-parked session still has a dead model, so its queued turns must stay
unclaimable until the park's holder-targeted condition wake (`quota-recovered` or timed
fallback) delivers its own recovery turn, whose completion clears the hold. For a switch, the
recovery wake is the owner's; for a park, it is the condition/fallback wake — either way it is
the episode's `recoveryWakeId`.

**Concreteness (lattice H6/H7).** The hold is not abstract:

- **Where it lives.** A durable column **`sessions.adjudicationHold`** (owner: `Org`, the
  `sessions` table), the single value the filtered-claim predicate reads. Three states: `NULL` =
  not held (normal FIFO); `'*'` = held, unfiltered (nothing claimable — set atomically with the
  classified terminal, before any recovery turn exists); `<recoveryWakeId>` = held, filtered
  (only that wake's turn claimable). The claim predicate is: `NULL → ORDER BY seq LIMIT 1`;
  `'*' → claim nothing`; else `AND wakeId = adjudicationHold` on top of `ORDER BY seq LIMIT 1`.
- **The filter-arm seam.** Arming (the `'*' → <recoveryWakeId>` transition) is a **named
  implementation change to the `WakeScheduler` W6 fire transaction** (`wake-on-fact-v1.md` §4.3):
  the same CAS-gated transaction that transitions `pending → fired` and enqueues the recovery
  turn ALSO sets `sessions.adjudicationHold = recoveryWakeId` — not a generic hook system, one
  extension to the one firing transaction. (For a `swap`, the equivalent write is in the
  `adjudicate` verb's transaction, which likewise enqueues the recovery turn.)
- **Release.** Clearing (`adjudicationHold = NULL`) is wired to the recovery turn's completion on
  the ledger's turn-terminal path — the same transaction that marks the recovery turn terminal.

### Supervision adjudication-hold branch (F2b)

Between classification and park there is a window — the episode is `claimed`/`notified` while
the owner is being adjudicated — in which **no holder-targeted wake exists yet**, so base
`pending_count(holder)` would not pause the holder and supervision could prod it before the
episode's intended deadline (`supervision.ex:177` suppression requires pending work or a
holder-targeted pending wake; a fresh attest merely resets counters, `supervision.ex:224`).

Rule: **supervision gains an adjudication-hold branch.** In its evaluate chain, an **open**
adjudication episode (`status IN ('claimed','notified')`) for the session is a suppression of
the *holder* prod — like a pending holder wake — but the escalation clock is the **episode's
own `deadlineAt`** (the deadline protocol above), which drives owner-escalation up the ladder,
not a prod of the (blocked) holder. Once the episode resolves-into-park, the holder-targeted
condition wake takes over the not-a-stall guarantee via `pending_count`. So the holder is never
prodded from classification through recovery: first by the open-episode branch, then by the
parked condition wake.

### Owner ruling verb — `adjudicate` (lattice H5)

The owner's ruling actions have a pinned verb, decision-complete — they do not happen through
prose:

    tightbeam adjudicate --episode <correlationKey> --action park|swap|respawn|stop \
                         [--model <ref>] [--reason <text>]

- **Auth.** The caller session MUST be the episode's current `ownerTarget`, and `--episode` MUST
  equal the episode's current `correlationKey`. A caller that is not the `ownerTarget`, or that
  presents a rotated/stale `correlationKey` (a superseded owner after a deadline escalation), is
  denied — this is the same response-liveness predicate the CAS matrix enforces (`… AND
  correlationKey=?`). No other principal can resolve the episode.
- **Transaction, per action (one transaction each):**
  - `swap` — run the CAS swap seam apply (base→effort→read-back, below); in the SAME transaction
    resolve `notified → resolved`, enqueue the recovery turn, arm the filter, and emit the
    `lifecycle_events` swap record. Cross-harness composes the barrier here.
  - `park` — schedule the holder-targeted condition wake (schedule-then-check, Parked state),
    resolve `notified → resolved` (parked), and file the `adjudication_block` fact. No recovery
    turn and no arm yet — the condition/fallback wake's later W6 fire does that, or the
    already-recovered branch of schedule-then-check performs the same write on cancel (below).
  - `respawn` — retire the affected session and respawn on the chosen `--model`/harness (the
    cross-harness respawn path), then resolve + recovery wake.
  - `stop` — resolve the episode terminally; the affected session stays failed/retired with no
    recovery; records a stop fact. The held queue is drained per the session's retirement.
- All actions run under the `ownerTarget` principal, so every episode resolution is attributed to
  the owner that ruled it.

### Parked state — the owner parks the holder (fixing the r4 circularity)

r4 said the parked *holder* schedules its own condition wake. That is circular: the holder's
model is dead, so any turn it runs fails — it cannot schedule anything (r4 finding 1). r5 rule:
**the park is performed by the OWNER** (or the substrate executing the owner's park decision) as
part of episode resolution, and the wake it schedules is **targeted at the holder**:

- The owner schedules a condition wake with **target `sessionKey` = the holder**, pattern
  `{kind: "quota-recovered", scope: "<harness>:<identity_name>"}` — the exact-equality scope form
  `wake-on-fact-v1.md` §D rules (lattice H5; a bare `<harness>` never matches the ruled fact
  scope and the wake would never fire) — plus the **mandatory timed fallback**.
- **Schedule-then-check ordering (lattice H10/H6).** Because a condition wake only matches facts
  filed **strictly after** it was created (the no-replay id cursor, `wake-on-fact-v1.md` §4.3),
  a `quota-recovered` filed in the gap between episode resolution and wake creation would be lost
  and the park would silently degrade to fallback-only. So the park applies the SAME
  schedule-then-check the escalation path uses: **create the condition wake FIRST, then check
  whether `quota-recovered("<harness>:<identity_name>")` has already fired; if it has, cancel the
  wake and, in the SAME transaction as the cancel, perform the exact write the W6 fire would
  have performed — enqueue the pending recovery turn and arm the filter.** The cancelled wake
  never fires, so this branch is the only remaining driver of that transition; the recovery
  turn's completion releases the hold as usual. One ordering rule, no coordinator machinery.
- Because the wake **targets** the holder, `Wakes.pending_count(holder) > 0`, and supervision's
  `:continuation` branch short-circuits — a parked block is not a stall. This suppression is
  **target-keyed**, so the owner being the *creator* (creator ≠ holder) is fine (r5 finding 1).
- The **lane hold persists through the parked interval** (Session hold): when the condition or
  timed-fallback wake delivers, its W6 fire transaction enqueues the pending recovery turn and
  arms the filter; that recovery turn runs first and its COMPLETION releases the hold, then the
  held queue resumes. Resolving the episode does not release the hold; neither does the wake's
  delivery — only the recovery turn's completion does.
- The park **files the block fact** — kind `adjudication_block`, subject = the affected
  `sessionKey`, `detail` = JSON `{reason, condition, correlationKey}` — filed by the episode's
  **`ownerTarget` principal** (the owner session, not the holder) inside the `adjudicate --action
  park` verb's transaction (below), as a `lifecycle_events` row. It is NOT a holder attest: the
  owner cannot file the holder's attest (r5 finding 1), so the block fact is an owner-attributed
  lifecycle record, not a progress filing.

When `quota-recovered` fires (or the timed fallback does), the holder wakes and re-adjudicates —
switch if a floor-meeting mind is now available, or re-park (the owner reopens the episode and
reschedules). This retracts r3's claim that a fact + any re-check suffices under
`supervision.ex:614`.

### Owner-initiated model swap — the serialized/CAS mutation seam

The owner's chosen switch executes through ONE serialized path per session (shared by operator
`tune set_model`, adapter-death recovery, and adjudication swaps, so they cannot race blind
writes), with an **expected-version CAS**:

- **CAS key.** The seam reads the session's current `(model, harness)`, applies, and commits
  the DB mutation only if `(model, harness)` is still the expected value. A **duplicate success**
  (the session already resolved to the requested `(model, harness)`) is an idempotent no-op that
  returns the resolved state — not an error.
- **Typed two-mutation apply (strict, adjudication path only).** Applying is base model then
  effort (`adapter.ex:345`); the adjudication path is strict and typed:
  1. apply base model; 2. apply effort; 3. **verify by read-back** of both options.
  - **partial_apply** (base applied, effort refused or read-back mismatched): attempt a base
    rollback to the prior model, and classify the outcome as its own state `partial_apply`,
    surfaced back to the owner (not silently left half-applied and not misclassified as
    `model_unavailable`).
  - **option-readiness race:** because options populate asynchronously, a refusal is retried a
    bounded number of times before classifying `model_unavailable`.
  - **The normal boot/load path is unchanged:** `load_session` keeps its lenient,
    async-tolerant behavior (`adapter.ex:221`) — a loaded session already has a model and a
    refused re-assert must not cost it its memory. The strict read-back path applies ONLY to
    adjudication-driven applies, never to ordinary boot/load.
- **Record.** On success, in the same transaction as the DB mutation, insert a
  `lifecycle_events` row (the `events` table is CHECK-locked to `verb|denied`, so it cannot be
  used): `kind = "model_adjudication"`, `subject = <sessionKey>`, `detail` = JSON
  `{from_model, to_model, from_harness, to_harness, trigger, adjudicated_by, correlationKey,
  harness_crossed, context_discarded}`. Use the in-transaction insert (`Txn.q`), not the
  stand-alone `EventLog.lifecycle/4` which opens its own query. `session_status` surfaces the
  current model as it already does; there is no persisted chain position, because there is no
  chain.

### Barrier cut (cross-harness swap) — one atomic transaction

When the chosen switch crosses harnesses, the history barrier applies. The invariant is
**narrowed (r5 finding 4) to "no reply is visible without its prompt."** The r4 clause "the
recovery marker must be the first post-barrier record" is **DROPPED** — prompts accepted while
the failed turn was running already have committed echoes at sequences *after* the failed
prompt (`gateway.ex:487-526`), so no cut can make the recovery marker first without deleting
legitimate prompts. It is unnecessary: those echoes are **deferred, not orphaned**. Barrier,
marker, and recovery wake commit in ONE transaction:

1. the turn is already terminal-failed (edge step 2), its `[turn failed]` marker suppressed;
2. set the barrier `cleared_through` = the failed prompt's **`messages.seq`** — the projection
   echo's sequence (`gateway.ex:761`), explicitly NOT the independent ledger `turns.seq` —
   clearing THROUGH the failed prompt echo **only**;
3. **already-committed later echoes REMAIN visible.** They do not violate the invariant: a
   queued prompt with no reply yet is fine; only a reply without its prompt would break it. The
   hold (F1) keeps those prompts from running on the dead model, and they receive replies after
   the recovery turn runs — deferred, not orphaned;
4. append a **non-terminal recovery marker** (distinct from `[turn failed]`, `gateway.ex:2022`;
   reuse `append_marker`'s `process:tightbeam` anti-forgery, `gateway.ex:2035`) and the recovery
   wake;
5. broadcast **`stream_history_cleared`** as the existing harness switch does
   (`gateway.ex:1757`) so live clients drop their view.

A same-harness swap keeps the transcript; no barrier.

## Substrate gaps (proposed roadmap items)

- **GAP 1 — Harness error classification with precedence.** Scope: medium. Implement
  `auth → model → boot` at the boot/config seam and runtime `quota`/`model_unavailable`
  classification, BEFORE gate-attestation/config-apply collapse causes to `:turn_error`/`:DOWN`
  (`adapter.ex:180, 397-412`; `adapter_coordinator.ex:154`). The strict, read-back-verified,
  bounded-retry apply is the **adjudication path only**; the normal `load_session` path keeps
  its lenient async tolerance (`adapter.ex:221`) — do NOT blanket-strictify it. Requires
  empirically cataloging each harness's error shapes in `harness-support.md`. RULED
  (Flynn/Fable 2026-07-22): the catalog is OPPORTUNISTIC, not probe-complete — quota and
  recovery envelopes cannot be induced on demand, and auth-fail probes against a live
  org's working harness are forbidden. Therefore the engine builds NOW behind a pluggable
  classify seam defaulting `other`, and the seam's contract includes: every `other`
  classification RECORDS THE RAW ENVELOPE (distinct marker), so the catalog accrues from
  production incidents. Seeded empirically: the codex revoked-refresh-token envelope
  (live incident 2026-07-21, adapter stderr); plus the two safe probes (per-harness
  model-refusal on a scratch session). The classification mapping + quota-recovered
  producer land as a small fast-follow lane once shapes exist. Guessed string-matching
  remains forbidden.
- **GAP 2 — Spawn-time catalog validation + classified spawn refusal.** Scope: small; DEPENDS
  on `derived-model-catalog-v1.md`. Validate the ref against a **fresh** inventory
  (`create_spawn:1635`); on refusal return the classified Edge-1 denial union (incl.
  `catalog_unavailable`), not a generic error. **QUEUED** — the derived-catalog re-do is a lane
  because this recon made it a hard KP1 dependency.
- **GAP 3 — Runtime→wake-owner routing + episode CAS + holds (the wake-on-fact S1 dependency).**
  Scope: medium. Classify (incl. `other`), claim the durable episode, take the hold, wake the
  owner via `ladder_target/3`. Implement the full episode CAS matrix
  (`claimed→notified→resolved` as guarded `UPDATE … WHERE … AND correlationKey=?`; reopen
  rotates `correlationKey`/timestamps/`ownerTarget`/**both wake ids**/rung/deadline). Store
  **two wake identities** — `ownerWakeId` and `recoveryWakeId` — each scheduled through
  `wire_idempotency` with a deterministic key `(sessionKey, condition, correlationKey, purpose)`
  so recreation returns the same wake (no fresh UUID). `deadlineAt` is `NOT NULL`, **set at
  claim** so a stuck-`claimed` episode escalates on the same clock as a stuck-`notified` one.
  Boot reconciliation is guess-free via the deterministic keys. Add the **supervision
  adjudication-hold branch** (an open episode suppresses the holder prod; the episode deadline,
  not a holder prod, drives escalation). The parked-block continuation is `wake-on-fact-v1`'s S1
  mechanism — but the
  **owner** (not the dead-modeled holder) schedules the **holder-targeted** `quota-recovered`
  condition wake + timed fallback, recognized via target-keyed `pending_count` (creator ≠ holder
  is fine); reference wake-on-fact's durable creator-identity stamp where its `self_pending_count`
  path is used. The condition scope is the ruled `"<harness>:<identity_name>"` (`wake-on-fact §D`),
  scheduled **schedule-then-check** (create wake, then check for an already-fired
  `quota-recovered`, cancel-and-proceed if so — the §4.3 no-replay cursor makes the gap lossy
  otherwise). Add the **`adjudicate` verb** (`--episode <correlationKey> --action
  park|swap|respawn|stop`, authed to the episode's `ownerTarget`, one transaction per action) and
  the owner-attributed **`adjudication_block` `lifecycle_events` fact** for park. Depends on S1
  landing.
- **GAP 4 — Owner-initiated swap seam + record + recovery + hold.** Scope: medium. One
  serialized/CAS seam (shared with operator tune and adapter-death recovery) with an
  expected-version key on `(model, harness)`, duplicate-success no-op, the typed two-mutation
  apply (base→effort→read-back; `partial_apply` with base rollback; bounded readiness retry), a
  `lifecycle_events` record (exact shape above — NOT the CHECK-locked `events` table),
  **recovery-wake dedupe on the episode's stored `recoveryWakeId`** (backed by `turns.wakeId
  UNIQUE`, `ledger.ex:42`), and the atomic barrier/marker/wake + `stream_history_cleared` cutting
  on `messages.seq` — with **already-committed later echoes left visible (deferred, not
  orphaned)**. Adds the **filtered-claim hold** at lane claim (`session_lane.ex:171` /
  `ledger.ex:161`): the durable column **`sessions.adjudicationHold`** (`Org`-owned; `NULL` |
  `'*'` unfiltered | `<recoveryWakeId>`) is read by the claim SQL (`'*'` → claim nothing;
  `<recoveryWakeId>` → `AND wakeId = ?`); the recovery turn's completion clears it on the
  turn-terminal path. Arming is a **named extension to the `WakeScheduler` W6 fire transaction**
  (`wake-on-fact §4.3`) — the fire that enqueues the recovery turn also sets the column, no generic
  hook. Suppresses the pre-adjudication `[turn failed]` marker (`gateway.ex:817`).
- **GAP 5 — `ephemeral` as adjudicator advice.** Scope: small. Add `ephemeral` to the archetype
  schema/validate (`archetypes.ex`), default `false`, `kind='main'` a hard floor. Surfaced to
  adjudicators (and taught in `model-selection.md`); it authorizes no substrate action. (No
  consent field and no condition→action policy exist — they dissolved with the chain-walker.)
- **GAP 6 — Catalog freshness contract — DONE in the catalog spec.** The
  `fresh | stale | unavailable(reason)` contract (failed refresh with last-known ⇒ `stale`;
  membership answers carry the state) is now written directly into `derived-model-catalog-v1.md`
  §"Freshness contract (adjudication requirement)" by this lane. The catalog-implementation lane
  builds it; this spec and Edge 1's `catalog_unavailable` consume it.
- **GAP 7 — Token/quota/cost observable (investigate-then-expose).** Scope: unknown until
  investigated. Whether the harnesses expose a continuous usage / rate-limit / remaining-token
  gauge is **UNVERIFIED** — recon did not establish it, and the derived catalog carries
  inventory/capability metadata only, not quota or price (`derived-model-catalog-v1.md:36`).
  Investigate what each harness exposes, then surface it (if anything) as a readable observable
  WITH unknown-state semantics, so an adjudicator can choose *around* a nearly-spent budget
  instead of only reacting *after* zero. Until then those adjudication inputs do not exist and
  must not be assumed.

**Companion reconciliation (done).** The companions are already aligned to adjudication:
`agentic-engineering-guidance-spec.md` no longer calls ringdown a "mechanical backstop," KP1 in
`rails-and-guidance-roadmap.md` now specifies inference/adjudication (not ordered fall-through),
and `model-selection.md` is elected by **every engineering archetype** — so any archetype that
can receive an adjudication wake carries the quality-floor characterizations it must apply. No
cross-spec contradiction remains.

Tuning hook: the characterization doc's truth is measurable — remedy-rate / first-pass-clean
sliced by model (`self-tuning-rails-core-FUTURE.md §6g`, which explicitly slices RR by model)
is the eval that will propose amendments to `model-selection.md`, closing the loop from observed
model performance back to the guidance adjudicators read.

## Implementation rulings (2026-07-22, LKP1 questions — these pin the semantics)

1. **Durations are config, never CLI.** `config :tightbeam, :adjudication_claim_window_ms
   / :adjudication_response_window_ms / :adjudication_park_fallback_ms`, env overrides
   `TIGHTBEAM_ADJUDICATION_*`, threaded exactly like the escalation-deadline seam.
   Defaults: claim 5m, response 24h (the owner-decision class), park-fallback 4h. The
   adjudicated party never sets its own deadline.
2. **Respawn mints a NEW session** (new sessionKey; archetype/owner/spawnedBy inherited
   from the retired one); the recovery wake targets the NEW session; the old session's
   episode resolves terminally and its hold releases via the existing retirement drain
   path. ADDITIONALLY (completing the read): in the same transaction, (a) roles bound to
   the retired session REBIND to the new one — the role is the office, the session the
   officeholder; addressing survives the respawn — and (b) open assignments held by the
   retired session RE-HOLDER to the new session — respawn is explicitly a continuation
   of the same obligations, so no interruption rows and no strands. (Contrast cascade
   retirement, which is termination and does write interruption rows.)
3½. **Retirement drain (CORRECTED 2026-07-22: no prior drain existed — LKP1 MINTS the
   canonical one, shared by ALL retire paths).** `Ledger.drain_queued_for_retire_in_txn`,
   called by both the retire verb and the adjudication respawn: the retired session's
   queued turns → `canceled` (retired-class reason; never-executed ≠ failed), in the
   same transaction as retire(+respawn+transfers), published via the existing
   turn-terminal publication path. This also closes the pre-existing orphan gap
   (retires never drained; claim_next never filtered retired sessions). Invariant
   stated at the seam; flagged as a minted pattern.
4. **STANDING META-RULING (operational defaults):** wherever this spec leaves an
   operational default unpinned, MATCH THE EXISTING SUBSTRATE PATTERN VERBATIM — retire
   semantics, env-config seams, CAS vocabulary, publication paths. Pause ONLY where no
   existing pattern exists or two conflict. Pattern-conformance is the default
   resolution; novelty is the exception that escalates.

3. **Target harness is DERIVED from `--model` via the derived catalog's per-harness
   inventories** — no `--harness` flag. Ref in the current harness's inventory =
   same-harness swap (transcript kept); ref in another harness's inventory =
   cross-harness respawn (compose the barrier). A ref appearing in multiple inventories
   (practically impossible — provider-namespaced ids) denies classified `ambiguous_ref`
   rather than guessing.
