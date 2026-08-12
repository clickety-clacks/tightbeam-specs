# S4 operability — adapter faults heal DARK — v1

Status: READY (gate-cleared 2026-07-26; trajectory 4→4→3→1, final finding was contract-text alignment of the epoch token — folded; reviewer confirmed totality, CAS ruling race, visibility scoping, and restart stability sound. r3 gate NOT-READY(3) folded — totality made normative across all probe terminals, epoch-composed heal tokens restart-stable, visibility/ordering corrected to the code's actual rule. r2 gate NOT-READY(4) folded — total probe-terminal lifecycle, fired-wake/ruling race CAS, episodeId column + visibility/ordering pins, level-triggered heal with generation tokens. r1 gate NOT-READY(4) folded — probe-first atomic transition riding the existing recoveryWakeId invariant, cause encoding + seam-origin rules + model-decision tagging for the load-apply route, decision-requests read-time union pinned, idempotent CAS heal sweep). Task #19; field evidence sat-e2e
lnx-0725d S4. Flynn ruling: "automatically. dark factory. DARK" — recovery is
automatic when the cause heals; no operator verbs for routine recovery; humans only
for genuine decisions. Dark ≠ opaque: full observability stays.

## Defect 1 — adapter-boot failure must produce the DESIGNED reason

Today an adapter whose BINARY fails at spawn (chmod -x, missing, Permission denied)
crashes the adapter GenServer in handle_continue; the crash escapes through the lane
as bare `{:error, :task_crash}` while the designed `{:error, {:adapter_unavailable,
reason}}` path (built for exactly this) never fires; the actionable text sits only in
adapter stderr. Contract: an adapter that cannot BOOT yields `{:adapter_unavailable,
<one-line reason incl the spawn error>}` to the turn — same shape as the existing
designed path — and the turn terminalizes `failed` with that reason. Mechanism note
(gate r1): the boot-call exit itself carries only `{:error, :closed}`; the reason
requires a boot-boundary catch plus ATTEMPT-SCOPED stderr extraction (the last stderr
line of that boot attempt), not a generic crash translation. (The gateway-log
half of this is task #16's lane; this spec owns the REASON reaching the turn row.)

> **AMENDED 2026-08-12 — Defect 2 below is DEAD.** Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`).
> Holds no longer exist, so a defect about holds releasing themselves has
> nothing to attach to. Defect 1 above remains live. Retained as history —
> do not build from Defect 2. See `adjudication-deletion-amendment.md`.

## Defect 2 — adjudication holds release THEMSELVES when the cause heals

Today: repeated adapter-fault turn failures escalate the session into a model-
adjudication hold; when the adapter recovers, the hold persists — session wedged;
the hold is invisible to `decision-requests`; recovery requires a new session.

Contract (dark factory):
1. **Cause tagging (encoding pinned, r1-F2).** The episode gains ONE additive
   nullable column `cause` — encoding `"adapter_fault:"<adapter key>` where the
   adapter key is the canonical coordinator key string (`<harness>:<preset>@<host>`,
   exactly as /version renders it), derived at the hold-open seam from the session's
   adapter identity (available where the failure is in hand). Seam-origin rule: ALL
   adapter-fault forms tag `adapter_fault` — the async boot-call exit, the
   circuit-open degraded failure, and runtime closed/dispatch failures. The
   jobtrace `{:model_apply_failed, _}` route into this hold family is tagged
   `"model_decision"` — a GENUINE decision cause, NEVER auto-released by adapter
   heal (proof 4 uses exactly that failure). Both claim and reopen write/replace
   the cause; legacy rows stay NULL and are never swept.
2. **Auto-release on heal — probe-FIRST, riding the existing invariant (r1-F1).**
   Release is ONE atomic transition per held session: resolve the episode (CAS on
   episode state — see the ruling race below), dispose the owner-adjudication
   request (r2-F2: the owner wake is normally already FIRED with a queued or
   running owner turn by heal time — cancellation of a pending row is the rare
   case; the pinned disposition is: pending wake → canceled; fired wake with a
   queued/running owner turn → the turn is left to complete, and its eventual
   ruling lands on a RESOLVED episode where it is an acknowledged no-op — the
   heal-vs-human-ruling race is decided by the episode-state CAS, first transition
   wins, the loser no-ops with a logged event; proof covers the FIRED/queued case,
   not just pending), create the deterministic probe wake/turn, and set the
   session's hold `'*' → probeWakeId` — the EXISTING recovery filter (ledger claim honors
   only that wake while held) — clearing the hold ONLY when the probe turn
   terminalizes successfully. An older queued real turn therefore cannot jump the
   probe (proof 2 seeds one and proves the probe claims first). Probe failure runs
   the totality rule above (always re-holds, same cause) and, in the SAME
   transaction, arms the probe retry (see Replay identity below) — a re-hold is a
   new hold and owes its own probe.
   **Heal signal — LEVEL-TRIGGERED with EPOCH-COMPOSED tokens (r1-F4 + r2-F4 +
   r3-F2, NORMATIVE):** the heal token is `{coordinatorEpoch, generation}` —
   coordinatorEpoch a STRICTLY-MONOTONIC value minted once at coordinator init —
   cross-review F2: ULID is NOT strictly ordered within a millisecond (random suffix),
   so a fast restart can mint a LOWER epoch and reject its own heal token, wedging the
   hold. Use a persistent monotonic counter (an epoch row incremented at each
   coordinator init, durable across restarts) OR millisecond time with a
   same-ms tiebreak that is monotonic per host — NEVER random-suffixed. Every later
   coordinator init yields a strictly larger epoch, generation
   the counter /version already renders. The ready event carries the full token:
   {:adapter_ready, key, {coordinatorEpoch, generation}}.
   Two triggers, closing both race directions: (a) EDGE — every ready event sweeps
   sessions holding `adapter_fault` on that key; (b) LEVEL — the hold-COMMIT path
   checks current adapter readiness at commit time, and if the adapter is already
   ready (a ready fired before the hold committed — the lost-edge case) schedules
   the probe immediately. Replay identity (restart-stable): each hold records the
   last token that probed it (`healToken`, additive column beside cause, storing
   the epoch+generation pair). Comparison is EPOCH-FIRST, then generation: the
   ready-event sweeps (edge and level) probe ONLY on a strictly larger token; an
   EQUAL token there is a replay and a no-op; a post-restart ready always
   qualifies (new epoch, regardless of its reset generation). A RE-HOLD IS A NEW
   HOLD: "one probe per (hold, token)" therefore grants each re-hold one probe of
   its own, delivered by the probe retry below — never by a replayed ready event.
   One probe per (hold, token). No operator action at any point.
   **Probe retry (ruled 2026-07-28, task #103 — dark-factory liveness):** the
   former clause "a re-held session probes again only on a genuinely newer token"
   assumed a failed probe implies a still-faulty adapter whose next death→ready
   cycle mints the next token. Field evidence falsified that assumption: a probe
   can fail while its adapter stays up and ready (boot-boundary race, task crash,
   cancel), no newer token is ever minted, and the healed session's queued backlog
   wedges forever. Current rule: every non-delivered probe terminal, inside the
   transaction that re-holds, schedules ONE durable retry wake (existing wake
   machinery, internal consumer; delay `adjudication_probe_retry_ms`, default
   30s; idempotent per failed probe wake). The wake is BOUND: it names its
   episode, cause, and the failed probe it retries, and it acts only while that
   re-hold is still current — a superseded one (episode gone, or a newer probe
   in its place) is consumed as a no-op. Arming SUPERSEDES every prior pending
   heal-retry for the session: AT MOST ONE pending heal-retry per session, the
   newest, honoring its own full backoff (a stale retry must never probe a
   newer failure early). At fire time the retry re-reads
   adapter readiness: ready → it probes the re-held session ONCE at the CURRENT
   token, equal permitted — this is the new hold's one probe; not ready → it does
   nothing, and the next genuine ready event owns the wake-up — always a
   strictly newer token, because EVERY adapter death bumps the generation,
   planned teardown (credential stop/start's close_adapter) exactly as a crash:
   a successor's ready must outrank every token stamped against its
   predecessor. Storm suppression is unchanged in intent and force: replayed ready
   events still probe nothing, the level check at re-hold commit still refuses
   the equal token (backoff is what spaces re-probes), a perpetually failing
   probe costs one probe per retry cycle (retry semantics, not a storm), and
   probe wake identity is chained per attempt (the failed probe's wake id
   discriminates the idempotency key) so an at-least-once retry still enqueues
   exactly one probe.
3. **Visibility (dark ≠ opaque; read-time union, r1-F3).** The decision_requests
   TABLE is untouched (its kind CHECK stays locked); the `decision-requests`
   LISTING gains hold rows via a read-time UNION over adjudication episodes. Episodes gain an
   `episodeId` (additive column, ULID stamped at open; existing rows backfill on
   first touch — the composite key stays the uniqueness truth, episodeId is the
   STABLE READ HANDLE r2-F3 required; correlationKey stays mutable and is not used
   for identity). Pinned synthetic shape: `kind: "adjudication_hold"`,
   `id: "hold:"<episodeId>`,
   `status: open` while the session's hold is `'*'` OR `probeWakeId` (a
   probe-in-flight hold is still a hold — resolved episodes whose session still
   holds are LISTED), `cause` verbatim, `disposition: "auto_on_adapter_heal"` for
   adapter_fault / `"awaits_ruling"` otherwise, plus sessionKey and raisedAt.
   Visibility (r2-F3, corrected r3 — the code's ACTUAL rule is owner/raiser/
   effort-expecter with NO admin axis): synthetic hold rows are visible to the
   held session's OWNER (the same owner axis the existing filter applies) and to
   admins — admin visibility applies to SYNTHETIC HOLD ROWS ONLY and does not
   broaden existing decision-request rows. Ordering: holds interleave in the
   EXISTING listing order (newest-first, the rowid DESC direction the code ships)
   keyed by their raisedAt — existing results are NOT reordered. The singular
   `decision-request` fetch accepts the `hold:` id form read-only under the same
   visibility rule. Kind-filtering consumers are unaffected
   (new kind value, additive). Release events are visible as the probe turn in the
   session's history — no new record family.
4. **Genuine decisions stay human.** Nothing here auto-answers a real model-choice
   adjudication; those keep the existing agent-side ruling flow — now visible per
   (3).

## Non-goals

No operator release/ruling verb (dark factory — explicitly rejected). No new health
machinery (the circuit is the heal signal). No new tables FOR HOLD/EPISODE DATA (cause, healToken, episodeId = additive columns on
the episode; probe = ordinary turn). The epoch counter IS a new table by explicit
authorisation of §Defect-2's pinned 'persistent monotonic counter … an epoch row
incremented at each coordinator init' — named here so the two clauses don't read as a
contradiction. No retroactive repair of holds predating the column
(NULL cause = legacy, untouched).

## Required proofs

1. Adapter-boot failure (non-executable binary): turn fails with
   {:adapter_unavailable, reason} naming the spawn error — not :task_crash
   (fail-before/pass-after).
2. Fault → hold → heal → auto-release: induced adapter death holds the session with
   cause adapter_fault:<key>; an OLDER REAL TURN is seeded in the queue; the verified
   ready event fires; the probe turn claims FIRST ('*'→probeWakeId filter), completes,
   the hold clears, then the seeded turn and a fresh turn complete on the SAME session
   (the exact clause lnx-0725d S4 failed); the stale owner-adjudication wake is gone.
3. Storm-freedom + totality + retry-liveness variants: replaying the SAME ready
   token produces zero additional probes; EACH of the four non-delivered probe
   terminals (failed, canceled, task-crash, boot failed_unknown) atomically
   re-holds with the same cause AND arms exactly one probe-retry wake — boot
   reconciliation re-holds rather than clears and arms the same retry; a ready
   sweep still probes a re-held session only on a strictly larger token (exactly
   once); the DUE retry wake probes the re-held session exactly once at the SAME
   token while the adapter is ready, and the queued backlog then drains in order
   with no further heal edge (the task #103 production shape); a due retry
   against a NOT-ready adapter probes nothing and leaves the hold eligible for
   the next heal edge; a post-coordinator-restart ready (new epoch, generation
   reset to a small number) DOES sweep a hold stamped under the old epoch.
4. decision-requests lists open holds (all causes) with cause visible; a genuine
   model-choice hold is NOT auto-released by an unrelated adapter heal.
5. Legacy NULL-cause holds untouched by heal events.

## Component touches

Adapter boot-failure mapping (adapter/coordinator seam); adjudication episode cause
column (additive) + open/release paths; AdapterCoordinator circuit-close hook →
release sweep; probe-retry wake (internal consumer on the existing scheduler,
armed by the probe-terminal writers); decision-requests listing gains hold rows;
probe-turn enqueue via existing machinery; tests. The satellite runbook's S4 oracle flips back to the spec's
original wording once this ships (resident session completes after recovery).
