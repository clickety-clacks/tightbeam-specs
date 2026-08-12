# Tightbeam Elixir Port — v3 (IMPLEMENTATION UNDERWAY)

**Review disposition:** three adversarial spec rounds (all archived as
`-review-{1,2,3}.md`) hardened the design; per operator ruling, spec
iteration is CLOSED and proof moves to code. Round-3's six defects are
carried as REQUIRED acceptance items, not prose solutions: (1) reconciler
liveness incl. lane-startup ownership + status-leading index; (2) terminal
publication = exactly-one durable transition + at-least-once publish attempt
(no stronger claim); (3) orphan quiescence must be provable (turns carry
adapter generation + request ref; quarantine until observed resolution or
durable generation recycle); (4) no blocking GenServer.call in the turn path
(async request/receive protocol); (5) ordered publication seam (publish in
commit order from the single writer) — a committed message may NEVER be
filter-dropped; (6) executable packaging (correct npm artifact names; doctor
via release eval). Every one lands as a kill-matrix or acceptance test that
the implementation must pass; code review (cross-provider, per SOP) resumes
on the Elixir code itself.

**Status:** Spec v3 — revised per adversarial review rounds 1+2 (both REJECT;
archived as `tightbeam-elixir-port-review-1.md` and `-review-2.md`). Round-2
defects 1–9 addressed below; TS-side findings fixed in commits e446bc6,
136519e, 649a02e (adapter-rule text fully reconciled — SOURCE OF TRUTH is the
executable `src/acp/harness.ts` setModel(); package.json reconciled with the
lockfile). For re-review, then implementation.
**Date:** 2026-07-17
**Decision (Flynn):** Port NOW — uptime is a product requirement; establish
architecture/patterns early; waiting only grows the port.

## Why (unchanged from v1, claims tempered per review §6)

Openclaw's ops taxonomy (random downtime; 50% of tokens on firefighting;
ever-novel failure modes; threading/wedging/deadlocks; silent partial death)
maps to BEAM mechanisms — supervision with logged reasons, no shared memory,
preemptive scheduling, introspection. **These are mechanisms, not guarantees**:
GenServers can still block, mailboxes can grow, NIFs and child processes can
stall, and supervisors give up past restart intensity. v2 therefore states no
absolute uptime claims; reliability is expressed as MEASURABLE health criteria
and fault-injection acceptance (§Acceptance). Staffing evidence (AutoCodeBench
Elixir >80%; Bun's 535k-line fleet port) supports who implements — it is not
evidence of correctness; the acceptance wall is.

## Invariants

1. Patchbay invariant: routes, records, enforces — never interprets.
2. Wire contract: behaviorally identical to the TS reference against the
   black-box referee suite (§Referee). "Byte-identical" applies to frame
   FIELD SHAPES and ORDERING per the differential traces, not incidental JSON
   key order.
3. Verb chokepoint + event log preserved.
4. **SQLite: ADDITIVE-ONLY schema evolution.** Existing tables/indices are
   never altered (the TS gateway must be able to reopen the DB untouched);
   the BEAM gateway may ADD tables (`turns`, `lifecycle_events`) that TS
   ignores. This supersedes v1's "same schema, no migration" and resolves the
   review's schema-vs-recovery contradiction: crash/lifecycle records go to
   the NEW `lifecycle_events` table — the existing `events.kind` CHECK
   (`verb|denied`) is untouched.
5. Adapter rules: **source of truth is `src/acp/harness.ts` + PATTERNS.md as
   corrected in commit e446bc6** (set_config_option with bare model name +
   per-harness effort config id; 0.59 dropped set_model). The port must NOT
   follow any older rule text.

## The keystone: a durable turn pipeline

One new table resolves ordering, lane recovery, wake delivery semantics, and
turn lifecycle in a single mechanism:

```sql
CREATE TABLE turns (
  seq        INTEGER PRIMARY KEY AUTOINCREMENT,  -- authoritative order
  sessionKey TEXT NOT NULL,
  messageId  TEXT NOT NULL,                       -- the persisted user echo
  wakeId     TEXT UNIQUE,                         -- non-null iff wake-originated (dedupe)
  origin     TEXT NOT NULL,
  prompt     TEXT NOT NULL,
  status     TEXT NOT NULL DEFAULT 'queued'
             CHECK (status IN ('queued','running','delivered','canceled',
                               'failed','failed_unknown')),
  createdAt  INTEGER NOT NULL, startedAt INTEGER, endedAt INTEGER,
  error      TEXT,
  publishedAt INTEGER            -- terminal state published to sockets
);
CREATE INDEX turns_session ON turns (sessionKey, status, seq);
CREATE INDEX turns_unpublished ON turns (publishedAt) WHERE endedAt IS NOT NULL;
```

**Liveness — the Reconciler (round-2 defect #1).** Commit-then-crash windows
(doorbell never sent; lane process not remembered by a restarted
DynamicSupervisor) are closed by an explicit reconciliation responsibility:
at boot AND every 5s, the LaneManager scans `turns WHERE status IN
('queued','running')`, ensures a SessionLane exists for each sessionKey
(starting one if absent), and nudges it. The doorbell is an optimization;
the scan is the guarantee. THIS is the mechanical enforcement of the prompt
conservation law — a committed turn cannot strand because liveness never
depends on a volatile message having been delivered.

**Terminal semantics corrected (defect #2):** the guarantee is **exactly-one
durable terminal TRANSITION** (the guarded UPDATE). Publication to sockets is
**at-least-once**: the publisher sets `publishedAt` after broadcasting; the
Reconciler re-publishes any terminal row with `publishedAt IS NULL`.
Duplicate terminal frames are harmless by wire semantics (client keys turn
state by messageId; a repeated terminal for the same messageId is idempotent
UI-wise) and are covered by a referee assertion.

**Orphan quarantine (defect #3):** when recovery marks a running turn
`failed_unknown`, the session is QUARANTINED: its lane will not start the
next queued turn until quiescence — either (a) Acp.Adapter confirms the
orphaned request ref has resolved (response/error arrived, or its cancel
completed), or (b) the adapter generation has been recycled (the process tree
that ran the orphan is dead). One-prompt-per-session holds even across
recovery.

- **Enqueue is transactional**: message insert + turn insert commit together.
  `turns.seq` (assigned by the store, in-transaction) is THE execution order —
  multi-producer BEAM message reordering (review §1a) cannot affect it. The
  lane's mailbox is a doorbell, never a queue.
- **Lane recovery**: a restarted lane reads `status IN ('queued','running')`
  for its session. A found `running` turn has UNKNOWN outcome → set
  `failed_unknown`, broadcast one failed terminal state, **never auto-retry**
  (tools may have executed — review §1c). Queued turns resume in seq order
  after adapter adoption.
- **Exactly-once terminal broadcast**: terminal transition is
  `UPDATE turns SET status=? WHERE seq=? AND status='running'`; only the
  caller with rows-affected=1 broadcasts.
- **Wake commit point** (review §1k): WakeScheduler delivers by executing the
  SAME transaction (message + turn insert with `wakeId`) and marks the wake
  fired IN THAT TRANSACTION. Crash before commit → wake still pending, retry
  is safe (the `turns.wakeId UNIQUE` constraint dedupes); crash after → turn
  is durable. At-least-once attempts, exactly-once enqueue, 1:1 wake→turn
  preserved. A target retired between schedule and fire → wake marked
  `canceled` (not silently fired) + lifecycle event.
- Concurrency correctness for dedupe/idempotency/uniqueness (review §3):
  every check-then-insert becomes INSERT with constraint + error adjudication
  inside a transaction (message `c_` dedupe by existing unique index; spawn
  idempotency PK; handle UNIQUE; first-user bootstrap wrapped in one
  transaction).

## Anti-openclaw commitments (Flynn gut-check, 2026-07-17 — BINDING)

Openclaw lost prompts inside clever shadow machinery (retries, requeues,
channel logic) that could silently disagree with harness reality. The turns
table is a delivery LEDGER, not shadow conversation state: one fact per
prompt, six states, one-way, terminal, never re-interpreted, never reconciled
against harness transcripts. To keep it that way:

1. **Prompt conservation law (acceptance invariant, mechanically checked):**
   every accepted prompt (c_ or wake) reaches EXACTLY ONE terminal state; no
   row may remain non-terminal beyond a bounded age. The soak audits this.
   Losses are impossible-silent by construction.
2. **No automatic retries, anywhere.** The pipeline never re-sends a prompt;
   failed_unknown is terminal (tools may have executed). Retry belongs to the
   SENDER (client resend-on-no-ack; agents decide for themselves).
3. **The turn state machine is FROZEN** (queued/running/delivered/canceled/
   failed/failed_unknown) — like the verb set, growth requires spec amendment.
4. **Mechanism budget:** the delivery path owns exactly four mechanisms —
   ledger, lanes, adapter coordinator, conn registry. Needing a fifth means
   STOP and re-spec, not accrete.

## Process architecture

```
Tightbeam.Application
└── Tightbeam.Supervisor (rest_for_one — DB first; everything depends on it)
    ├── Tightbeam.DB          (owner of the write connection + txn seam)
    ├── Tightbeam.Lifecycle   (lifecycle_events writer; monitors subtrees)
    ├── Tightbeam.ConnRegistry(socket registry: owner-scoped fan-out, device
    │                          takeover atomicity, GLOBAL device-keyed rate
    │                          limits (review §1h), replay watermarks)
    ├── Tightbeam.WakeScheduler
    ├── Tightbeam.AdapterCoordinator
    │     └── AdapterSupervisor (DynamicSupervisor)
    │           └── Acp.Adapter (one per harness×archetype; OWNS its Port —
    │                            conn+adapter are one work unit, review §4)
    ├── LaneManager (owns the Reconciler scan; starts lanes on demand)
    ├── LaneSupervisor (DynamicSupervisor; max_restarts 50 / 10s)
    │     └── SessionLane (GenServer per active session)
    ├── TurnTaskSupervisor (Task.Supervisor — TurnTasks live HERE, not under
    │                       lanes; explicit in the tree per round-2 #4)
    └── Bandit (wire endpoint; WebSock handler per connection)
```

Restart intensities (defect #9): root supervisor 3/30s (rest_for_one — DB
restart deliberately restarts dependents); LaneSupervisor 50/10s;
ConnRegistry, WakeScheduler, LaneManager, DB: 5/60s each; Acp.Adapter
children are coordinator-managed (:temporary — the AdapterCoordinator owns
all restarts/backoff, so `normal` exits and crashes take the same path).

**Task topology, precisely (defect #4) — monitors only, NO links:**
- Lane starts TurnTask via `Task.Supervisor.async_nolink` and MONITORS it.
  Task crash → lane gets :DOWN, transitions the turn, lives on.
- TurnTask's first act is to MONITOR its lane. Lane :DOWN → task issues
  session/cancel through the adapter and exits. (Lane death does not leak a
  running task; no bidirectional link exists to take the lane down.)
- Acp.Adapter MONITORS each requester (the TurnTask): requester :DOWN with a
  request outstanding → adapter sends session/cancel and drops the pending
  entry.
- Acp.Adapter NEVER blocks in handle_call: requests are `{:noreply, state}`
  with `from` stored; replies happen on Port response arrival; per-request
  timeouts via Process.send_after. Port frames and cancels are therefore
  always processed promptly.

**Lifecycle proof, implementable (defect #9):** a `boot_epochs` table (epoch,
bootedAt, cleanShutdownAt). Clean shutdown stamps the epoch; at boot, a NULL
cleanShutdownAt on the prior epoch synthesizes a `dirty_exit` lifecycle event
for it — so DB-owner death and `kill -9` are RECORDED BY INFERENCE at next
boot rather than impossibly at crash time. Tightbeam.Lifecycle makes no claim
to log its own dependency's death in real time.

- **DB ownership (review §3)**: ONE writer connection owned by Tightbeam.DB;
  all writes are `DB.transaction/1` calls through it (true single-writer, not
  convention). Read pool separate; EVERY connection pinned on checkout:
  `journal_mode=WAL, foreign_keys=ON, synchronous=NORMAL, busy_timeout=5000`
  (busy_timeout is an acknowledged, deliberate addition over TS — recorded
  here per review §6). No Ecto; module named `Tightbeam.DB` (not Repo).
- **Lanes never link to adapters and never blocking-call them** (review §1e):
  the TurnTask (not the lane) calls Acp; the lane monitors the task. Adapter
  death → lanes receive :DOWN via monitors → current turn transitions per the
  turns table → lanes LIVE ON. The restart-storm vector is removed by
  isolation, not by tuning.
- **TurnTask semantics (review §1c)**: lane spawns TurnTask under a
  Task.Supervisor, monitors it, stays responsive (cancel/status handled
  mid-turn). Lane death kills its TurnTask (link); Acp.Conn detects the
  requester's :DOWN and issues session/cancel for the orphaned request.
- **Adapter lifecycle (review §1d)**: AdapterCoordinator owns a monotonic
  GENERATION per adapter key. On Port exit (any reason — children are
  coordinator-managed, not supervisor-auto-restarted, so `normal` exits are
  handled too): generation++, publish; restart with exponential backoff
  (1s→60s cap); after 5 consecutive failures → circuit OPEN: adapter marked
  degraded, affected sessions' turns fail fast with a clear reason, /health
  reflects it, gateway stays up. Re-adoption is LAZY (parent-spec rule): a
  lane discovers a stale generation at next turn start and performs
  session/load on demand, bounded by a coordinator semaphore (max 3
  concurrent loads — no thundering herd). session/load failure → session
  degraded + turn failed with reason; planned idle-reap is a coordinator
  action flagged as such (distinguished from crashes in lifecycle_events).
- **Port framing (review §1f)**: binary stream mode + hand-rolled buffer
  (NOT {:line,N} — avoids :noeol reassembly limits), UTF-8-safe splits,
  malformed-line tolerance (drop + lifecycle event). Adapters spawned via
  `sh -c 'exec ... 2>>stderr.log'` (stderr never merges into ndjson stdout).
  Child lifetime: adapters exit on stdin EOF; acceptance verifies no orphan
  survives BEAM death (kill -9 the VM, assert adapter exit).
- **Replay vs live delivery (round-2 defect #5)**: every published message
  carries its per-session store seq. Each connection maintains a PERSISTENT
  per-session `lastDeliveredSeq` filter for its ENTIRE lifetime (not only
  during drain): any push with seq ≤ lastDeliveredSeq is dropped. Auth flow:
  register (pushes begin arriving and are buffered) → replay from store to
  head (advancing the filter) → drain buffer through the filter →
  sync_complete → live pushes continue through the same filter. Late
  publications of pre-watermark commits are thereby suppressed forever, not
  just during drain. Referee: reconnect-under-write asserts no gap, no dupe.
- **Takeover (defect #5b)**: registrations are generation-tagged. Takeover =
  ConnRegistry atomically swaps the device slot to the new (gen+1)
  registration, THEN asynchronously sends session_replaced/close to the old
  socket; the old connection's unregister compares generations and cannot
  delete its replacement.
- **Wire behavior parity notes**: rate limits stay GLOBAL per deviceId in
  ConnRegistry (per-connection state would reset on reconnect — review §1h).

## Referee (replaces v1's impossible "unmodified scripts" gate — review §2)

**E0 (work in the TS repo, before any Elixir):**
1. Convert the three E2E scripts into BLACK-BOX drivers: accept
   `TIGHTBEAM_URL` **and `TIGHTBEAM_TOKEN`** (the CLI requires both — round-2
   #6), plus optional baseDir for auth seeding; never import startGateway;
   nonzero exit on failure (fixed, e446bc6). TS gateway passes them via a
   launcher; BEAM is driven by the identical binaries.
2. Golden differential traces recorded against the TS gateway **using a
   DETERMINISTIC scripted ACP adapter binary** (promoted from the existing
   test fake — never a live model), normalized (UUIDs/timestamps/ports),
   stored under `test/golden/`; a comparator replays the same script against
   any URL and diffs frame shapes AND ordering.
3. Exact frame-order assertion for the canonical turn, **matching the TS
   implementation as-built** (round-2 #6; cite gateway.ts/server.ts):
   echo → accepted → running → typing(on) → activity(on) → ack (after
   dispatch returns) → assistant → **terminal state** → typing(off) →
   activity(off). The oracle is what TS DOES, not what reads nicely.

**Acceptance wall (ALL must pass on the BEAM gateway):**
- ExUnit port of the TS suite's cases + these ADDITIONS: concurrent
  multi-socket posts + wake to one session (store seq == execution order, no
  overlap); concurrent same-c_id retries (one echo/turn; re-ack same content;
  conflict+no-ack different content; scope stays (sessionKey, deviceId,
  clientMessageId)); replay-under-write (no gaps, no dupes, sync_complete
  terminates); large ndjson line / split-UTF-8 / many-lines-one-read / EOF
  mid-line / malformed JSON; multi-session interleaved ACP notifications
  route by sessionId.
- Kill matrix (fault injection, scripted): lane during turn & with queue;
  adapter during initialize/load/prompt/cancel/after-tools-before-result;
  WakeScheduler before delivery / after enqueue-before-mark (must not lose or
  duplicate — turns.wakeId proves it); DB owner restart under load; VM kill -9
  (adapters die too; restart adopts state). Each: assert recovery behavior,
  exactly-one terminal state per turn, lifecycle events present.
- Black-box: the three E0 drivers + golden-trace comparator vs TS reference.
- Sim E2E: real Clawline client pair/chat/reply.
- **Adopt-in-place protocol** (review §3, verbatim): TS creates+populates all
  tables incl. pending wakes + high AUTOINCREMENT; BEAM opens same dir, runs
  integrity_check/foreign_key_check, alters nothing pre-existing; BEAM
  mutates all row types; TS REOPENS and reads BEAM's writes; repeat with
  unclean TS shutdown (WAL/SHM sidecars present); compare table_xinfo/
  index_xinfo/FKs/user_version/application_id/sqlite versions; assert no
  framework metadata; verify per-connection PRAGMAs.
- **Soak, 24h with thresholds** (not "zero unexplained restarts"): injected
  faults only sources of restarts (audited via lifecycle_events); missed
  wakes = 0; duplicate turns = 0; p99 enqueue→accepted < 150ms; process
  mailboxes < 1k msgs sustained; BEAM RSS growth < 10%; DB busy errors = 0;
  scheduler run-queue p99 < 10.

## Telemetry & health (review §5.4)

- `/version`: `{protocolVersion: 1, build: {version, otp, elixir, gitSha}}`.
  The Node-specific `loopLagP99Ms` is NOT faked; if a jitter-equivalent is
  exposed it ships as `timerJitterP99Ms` (new, versioned field).
- `/health`: db read/write probe, wake-scan age, per-subtree restart counters
  (windowed), scheduler/run-queue summary, degraded adapters + circuit
  states, active lanes/connections. Adapter degradation degrades sessions,
  never global readiness.

## Packaging (review §5.3, node deps §9)

Mix release with ERTS included; OTP/Elixir pinned. **Node ≥24 is a declared
host dependency** (adapters + retained TS CLI are Node). Concrete layout
(round-2 defect #8):

- The release ships `priv/runtime/{package.json, package-lock.json}` — the
  SHIPPED manifest pins `@agentclientprotocol/claude-agent-acp`,
  `@agentclientprotocol/codex-acp`, and `tightbeam-cli-<ver>.tgz` (an `npm
  pack` of the TS repo's compiled CLI: dist/cli/ + its runtime deps).
- Deploy step: `npm ci --prefix <baseDir>/runtime` against that manifest.
  Resulting paths (the gateway's ONLY bin discovery roots):
  adapters `<baseDir>/runtime/node_modules/.bin/{claude-agent-acp,codex-acp}`;
  CLI entry `<baseDir>/runtime/node_modules/tightbeam-cli/dist/cli/main.js`;
  the projected `<baseDir>/bin/tightbeam` wrapper execs node on that entry.
- Doctor is a real release command: `bin/tightbeam_gateway doctor` (mix
  release commands/eval) — verifies node presence+version, the runtime tree
  paths above, opens a PROBE connection asserting journal_mode/foreign_keys/
  synchronous/busy_timeout, and asserts the configured checkout PRAGMAs in
  app config. (Acknowledged limit per review: a preboot probe proves the
  probe connection and the CONFIG, not future pool checkouts; a runtime
  /health assertion re-verifies a sampled pool connection.)

## Build SOP (unchanged) + phasing (E0 added)

- Fable: E0 referee hardening (TS repo) + OTP skeleton/spine + ONE vertical
  slice as production architecture (review §6: the skeleton IS the product,
  not a prototype) + Elixir continuity docs.
- Sol fleet: module ports per coding-with-codex, one focused goal each, gated
  on that module's ExUnit port.
- Cross-provider review per SOP; this spec re-reviewed (sol xhigh) before E1.
- **E0**: black-box drivers + golden traces + frame-order assertions, proven
  against the TS gateway. **E1**: mix skeleton, DB owner, turns table,
  Dispatch/EventLog/Lifecycle, one SessionLane+TurnTask+Acp.Adapter slice —
  exit: supervised prompt round-trip + kill-matrix rows for lane/adapter.
  **E2**: wire (Bandit/WebSock/Plug + ConnRegistry + replay watermark) —
  exit: golden traces + black-box wire driver. **E3**: wakes/homes/devices/
  assets/verbs — exit: remaining drivers + kill matrix complete. **E4**:
  adopt-in-place + sim E2E + soak → cutover of eezo serve (same baseDir) →
  TARS deploy via release + doctor.

## Open questions resolved (per review §5)

Bandit (registry/broadcast ownership explicitly ours, in ConnRegistry). Raw
exqlite via Tightbeam.DB owner (no Ecto, no migrations metadata). Mix release
(+ node host dep + doctor). Telemetry split as above.
