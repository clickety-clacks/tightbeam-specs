> **SUPERSEDED 2026-08-21.** This queue is the pre-flip 0.1-era roadmap, frozen at
> its 2026-08-12 import (content last updated 2026-07-20). It is history, not the
> plan. The living program state is:
> - `v0.2-program-2026-08-12.md` — the 0.2 program: rulings, staffing, phases, ledgers
> - `0.2-build-ledger.md` — one entry per landing on main
> - `0.2.0-spirit-and-work-sweep.md` — the 0.2.0 election: 67 elected, 28-item MVP core

# Tightbeam roadmap — living queue (updated 2026-07-20)

One page so nothing lives only in a conversation. Order is the ruled
priority; each line points at its spec. History/rationale:
tightbeam-decisions.md. Deficits framing: constitution/statute ruling
means hardcoded substrate guards are FINISHED law, not debt.

## In flight (concurrency batch updated 2026-07-31; entries below it still carry their 2026-07-20 dates)
- CONCURRENCY BATCH — MERGED 2026-07-31, 18 lanes, main green (Elixir 1155, Rust 165)
  and verified on shrdlu at 1111/152 on an idle box. Covers: all four upward
  synchronous-call deadlocks plus the wake self-cycle; the model-swap fence and
  reconciliation; rail occurrence fencing; per-machine adapter sharding; four
  transaction re-assertions; skipped-park redrive; four dead readers and their raw
  handlers; kernel-based Darwin process identity; the sandbox pid-kill fix; bounded
  ceremony waits with failures kept distinguishable; the false quarantine claim
  removed; the command seam; the CLI version handshake
  (cli-gateway-versioning.md). BOTH DEPLOY BLOCKERS CLOSED: the deadlock reachable
  from `tightbeam onboard`, which a fresh gibson install runs first, and model
  divergence.
- PARK / durable process identity (F4) — MERGED to main 028af86, 2026-08-01, seven
  review rounds to PASS; gates on the reconciled tree 1201/0 both platforms with a
  zero census. Originally IN REVIEW @ 13239b9, green at Elixir 1176 / Rust 171 with a zero
  orphaned-fixture census before and after. Spec: harness-park-lifecycle.md.
  Design SIMPLIFIED 2026-07-31 on Flynn's ruling ("if we attempted to kill it, it's
  killed"): post-kill death confirmation is DELETED — a group SIGKILL cannot be
  refused, so the check had one possible answer and was where three rounds of
  blocking findings lived. Review then correctly caught that the deletion went too
  far and removed PRE-kill target authorization too, which is a different question
  and necessary (group ids recur across reboot; restarts are routine). Restored with
  a boot identity. Promise ruled BEST EFFORT with two accepted residues, not chased:
  a descendant that calls setsid, and one running under other credentials (a harness
  invoking sudo) which survives while killpg still reports success.
- YAGNI SWEEP — MERGED to main becbbfc, 2026-08-01, review PASS after seven rounds. Scan of
  main found the deletions; two candidates were EXCLUDED for having live authority
  and are Flynn's call, not cleanup: probe.rs's ~300 lines of hand-rolled JSON,
  which cf83361 wrote deliberately to drop the serde derive dependency, and
  cli_compatibility's post-1.0 branch, which implements the ruled policy in
  cli-gateway-versioning.md. RULED 2026-08-01 (Flynn,
  verbatim): "dev/test dbs are disposable. the entire installation is expendable."
  The ~1,388-line pre-release migration stack AND the schema shims Fable's design
  review found (~230 more lines: wakes/idempotency/escalation/ledger/effort_checkin/
  adjudication try-ALTER archaeology) are being DELETED on branch drop-schema-shims;
  every schema collapses to its final CREATE TABLE; dev/test DBs reset; ONE
  versioned-migration discipline (PRAGMA user_version) arrives with the Gibson
  deploy, when a durable DB first exists.
- FLAKY PAIR, load-driven: test/lane_test.exs:106 and test/adapter_heal_test.exs:1250
  fail together at load >=13 with a concurrent lane and pass in isolation and on
  re-run at load ~10. Observed on TWO independent branches (durable-process-identity
  and yagni-dead-code), so it is not either branch's change. Same class as the rail
  script timeouts: a subprocess budget that load blows through. Not yet mechanized —
  the merge gate is an idle shrdlu run, which is a workaround, not a fix.
  MECHANISM PARTLY FOUND 2026-08-01: the park suite was LEAKING fixture process trees —
  100%-CPU spinners surviving their tests. Swept 77 stale groups off eezo (oldest 14h)
  and 16 off shrdlu (they drove it 0.08 -> 17 during characterization runs). So the
  chronic "lane load" driving the pair red was substantially self-inflicted by the
  leak, and every pre-2026-08-01 load-attributed red deserves suspicion. Fixed on the
  park branch: group-kill teardown + after_suite zero-leak census
  (scripts/harness_process_census.exs --assert-zero). The pair may prove stable once
  boxes stop accumulating spinners; re-characterize AFTER park merges before touching
  the tests themselves. NOTE: the old ad-hoc censuses grepped names no fixture ever
  had — macOS pgrep ALSO missed real ones — so "zero orphans" claims from before this
  date were unmeasured, and cleanup swept only what its pattern could see (noisy-helper
  sweeps missed the exec'd harness-exec spinners entirely).
- FLEET UPDATER — MERGED to main cb47dc2, 2026-08-01, review PASS after four rounds. Closes the
  cli-gateway-versioning gap where the exact-match connect check shipped but the sweep
  that makes it tolerable did not, so every gateway upgrade refused every satellite
  until each was re-assimilated by hand. `update-clients` enumerates from
  Placement.hosts, runs each remote CLI's explicit `version` command, ships only on a
  mismatch, and reports per host (updated / already current / unreachable / refused).
  It ASKS — the spec forbids inferring a remote CLI's identity from exit codes or boot
  probing. NAME UNRATIFIED: cli-surface-v1 enumerates neither `update-clients` nor
  `client-update` and the spec alternates; needs the enumeration amended.
- NEUTRAL SEED — branch neutral-seed, BUILDING against neutral-seed-v1.md (Flynn's
  verbatim ruling, complete design incl. learn/unlearn verbs). Reconfirmed 2026-08-01:
  "it needs to be neutral, but the kungfu has to be readily available so you can
  tightbeam learn it" — both halves load-bearing.
- SHRDLU GATING REQUIRES PROVISIONING — found 2026-08-01, recipe corrected. shrdlu moved
  asdf -> mise (no ~/.asdf, no elixir on default PATH); one PATH export replaces the old
  install-root recipe. It had NO rust, so /usr/bin/cargo 1.75 won and cannot build
  edition 2024 — `mise use -g rust@stable` fixed it in ~1 minute. There is no git
  checkout there either; ~/src/tightbeam_ex is a stale rsync with no .git, so gate by
  rsyncing the worktree. The suite's fail-fast preflight declares THREE prerequisites
  (git committer identity, harness CLI on PATH, the release binary) and refuses rather
  than reporting an unearned verdict — good design, and it is what surfaced all of this.
- NO END-TO-END DEADLINE PROPAGATION, Adapter -> Conn. Named 2026-08-01 after FOUR review
  rounds on one shape, which is the signal that this is a missing design contract rather
  than a defect: every layer re-derives its own relative timeout at SEND time, and every
  layer has a mailbox whose wait nobody counts. The four instances, each a smaller version
  of the same thing: a retry that could not deliver; effort and rollback requests left on
  Conn's 60s default; Adapter mailbox delay excluded from the budget; and now (a) the
  shared Adapter can sit blocked on ANOTHER caller's 60s Conn request so a queued strict
  call exits at 30s before its handler ever runs, and (b) Conn arms its timer only after
  dequeuing, so Conn's own mailbox delay is outside the budget too.
  THE CONTRACT THAT IS MISSING: an ABSOLUTE deadline minted at the public call and carried
  through every layer, with each layer checking it ON DEQUEUE rather than converting it to
  a relative timeout on the way in. That single rule kills all four instances and any
  fifth.
  NOT INTRODUCED BY yagni-dead-code — main has apply_model_strict at a 30s caller timeout
  over an unbounded 60s-default Conn request, i.e. no inner bound at all. That branch is
  strictly better and is deliberately NOT chasing this further; a 9-line YAGNI deletion
  must not turn into timeout architecture. Fix this as its own piece of work.
- F3 DIAGNOSED 2026-08-01: TEST DEFECT, NOT A PRODUCT RACE. In BOTH interleavings the
  product denies the ruling correctly, the heal probe keeps the hold, and no park wake is
  left behind. Only the test's claim about WHICH correct denial path ran is unstable: the
  July 31 lock refactor replaced a read interlock with spawn-then-immediately-release, and
  Task.async gives no "child has read the episode" guarantee, while the nil-healToken
  assertion stayed. When the heal commits first, the ruling legitimately takes the
  already-healed branch and logs the current row (healToken "7:2") — a branch another test
  explicitly expects. Fix is a ruling-side query barrier in the test; no production
  change. A week of "flaky under load" was the wrong diagnosis and cost real gate time —
  the tell was that it never reproduced in isolation UNTIL it did.
- (superseded) F3 REPRODUCES IN ISOLATION AS OF 2026-08-01 EVENING — upgraded from flake to
  diagnosable bug. On IDLE shrdlu, `mix test test/adapter_heal_test.exs` alone fails
  roughly 1 run in 2 (45 tests, 1 failure), where every earlier sighting needed the full
  suite and passed in isolation. That kills the load explanation outright and gives a
  cheap reproduction. Rust green alongside (186/0). Investigate at the reproduction, not
  by sampling.
- F3 IS A REAL INTERMITTENT RACE ON MAIN, not load. test/adapter_heal_test.exs:1331
  ("a ruling queued behind a winning heal is DENIED, not a crash"), always the same
  assertion: superseded.detail retains a healToken that should be nil. Four sightings
  2026-08-01: eezo@load13 (park tree), shrdlu under leak-load (park), eezo@load7 (yagni
  tree), shrdlu IDLE with the fixture leak fixed and census 0 (park @ 047ef0e). Failed
  on two DISJOINT trees whose only common code is main lineage -> attributed to main,
  not to either branch; yagni has since merged, so main @ becbbfc carries it. Rate
  roughly 1-in-5 to 1-in-10 full runs. Shape matches sample-then-act: the supersede
  write racing the detail serialization. NEEDS ITS OWN INVESTIGATION (post-merges);
  do not hold branches hostage to it, and do not re-blame load — the leak sweep
  removed that explanation.
- ONBOARDING DOES NOT REFRESH THE MODEL CATALOG (found 2026-08-01, eurisko api-key
  proof). After a successful api-key onboard, the boot-time missing-credential catalog
  stays cached; models flip selectable only after a gateway RESTART. Dark-factory
  violation: the cause healed, recovery was not automatic. First-boot family experience:
  onboard succeeds, then models mysteriously absent until restart. Fix: credential
  install triggers a catalog refresh for that provider. Not a Gibson blocker; IS the
  first-boot journey.
- SPEC STATUS MARKERS ARE UNRELIABLE — found 2026-08-01. Classifying all 87 specs by
  their own status blocks yields CURRENT 7 / FUTURE 59 / RECORD 17 / MIXED 4, which is
  false: transcript-verb-v1 says "DRAFT r5", topline-map-v1 "DRAFT r7", and
  work-item-brackets-v1 "READY", while `transcript`, `topline`, `toplines`, and
  `work-item-trace` all ship and work. A spec marked DRAFT can be live law. CONSEQUENCE:
  the first conformance scan scoped itself to the 7 and wrote off 59 as unbuilt, so its
  coverage was ~8% — its three findings stand but its silence proves nothing. Re-running
  inverted, from shipped code to governing spec. The markers themselves need a sweep, and
  "what does DRAFT mean once it ships" needs a ruling.
- CONFORMANCE GAPS, inverted scan 2026-08-01 (code -> governing spec, since status
  markers are unreliable). SEVEN gaps; most need a RULING, not a fix. Ranked:
  1. FICTION — dispatch.ex:3 states "nothing mutates registry/store/devices except
     through a verb handler." Four do: Projection.set_read_state (socket.ex:199),
     Devices.pair (:238), Org.create (:453), Assets.put from /upload
     (router.ex:343). They bypass statute evaluation, verb/denial audit, and any
     future chokepoint enforcement. Either route them or stop claiming the property.
  2. CONTRADICTED — derived-model-catalog-v1 says "the SUBSTRATE exposes the full
     derived inventory... the client projects it." gateway.ex:1153 collapses
     effort-qualified entries with uniq_by(base_ref) and :1237 publishes only
     id/ref/name/provider, dropping efforts, context, and capabilities;
     gateway_test.exs:2861 locks the lossy shape in. Substrate presentation policy
     has replaced client policy — a direct substrate/product boundary violation.
  3. NOT-IMPLEMENTED — accountability-constitution-v1 §6: "Read/query is free;
     mutation requires an open assignment." Neither the verb nor the tool chokepoint
     has an unconditional gate; spawn/wake/retire/identity/config/artifact-record all
     work with no open assignment. Rails are replaceable org law, so an optional
     statute cannot implement a non-waivable constitutional check.
  4. PARTIAL — artifact `--work-item` is optional in the CLI (args.rs:816) and
     rejected server-side (artifacts.ex:145), so the usage text teaches a form that
     cannot succeed. NOTE the spec itself leaves this open (artifact-carrier-proposal
     clause 12 "stays open") while artifacts-and-reconciliation calls workItemId a
     load-bearing exact FK — the tension is in the specs, so this needs a ruling
     before either side is changed.
  5. PARTIAL — Artifacts.release/2 exists (artifacts.ex:351) but no verb, handler,
     CLI command, or route reaches it, so moving an archived file leaves a stale
     `archived` row falsely asserting custody.
  6. NOT-IMPLEMENTED — the required custody-handoff guidance ("before moving
     artifacts out of the archive it must tell the user plainly") is absent from
     lib/, cli/, priv/guidance, and archetype material.
  UNGOVERNED SHIPPED BEHAVIOR: `contain-probe` and `contain-stage` (main.rs:25,
  routed before parsing) appear in no non-archived spec — the CLI surface divergence
  is worse than cli-surface-delta records. Also `GET /harnesses` (router.ex:104) plus
  the harnesses.json disk-first/route-second fallback and its schema
  (harnesses.rs:105): assimilation coverage is governed, this path is not.
  COVERAGE: load-bearing invariants only for the large rails/supervision/probe/e2e/soak
  specs; Mix tasks and most private gateway helpers not audited.
- DESIGN-TACTIC REVIEW (Fable, two passes, 2026-08-01) — adjudicated dispositions.
  DOING NOW: F2 last-begin-wins onboarding lease + F5a/b strict-apply trim (lane
  in flight); F1+G1 as ONE change — schema archaeology deleted (Flynn ruled dev/test
  DBs disposable, installation expendable) AND the runtime table-existence guards on
  production write paths go with it (ledger.ex:183+, escalation.ex:581/721,
  wakes.ex:829, gateway table?/1) since fixtures then build full schema; G1 is the
  purest "failing would be better" instance — Ledger.finish half-skips cross-table
  invariants only in tests, the mock-divergence signature, and effort_checkin.ex:964
  already states the correct doctrine; G4 decorative in-txn archetype recheck +
  duplicate idempotency pre-check (gateway.ex:3117/2672/3013, roadmap-00 shape in
  miniature); G2 probe.rs ordered-JSON writer (~125 lines) — REVERSES pass-one's
  exclusion: the cf83361 trade dropped serde DERIVE, serde_json stays available, and
  the writer silently drops unknown keys, which a diagnostics tool must never do;
  plus dual lineage encodings collapse to b64.
  RULED KEEP (do not re-flag): F5's third lock (enforces "user intent wins");
  toplines totality-over-corrupt-rows; supervision evaluate/ladder (1:1 to ruled
  semantics); effort_checkin generation-CAS; cli_compatibility exact-match;
  args.rs hand-parsing (4-dependency posture is a standing choice); probe's
  Epistemics block; contain.rs run_with_input kill path (the ruling in code).
  DEFERRED: F3 heal doorbell+sweep (needs formal re-ruling of s4-operability-v1,
  biggest single prize ~300 lines); G3 contain stdin file-redirect (post-Gibson,
  verify fd-across-imposition caveat first); F4 screen reassembly (keep pin, never
  extend, delete only if touched); F6 + placement.ex:1237 silent :subscription
  default (server-mediated credential reads — when it next bites); probe.rs G2b
  verdict: pid-identity mandate satisfied, no action.
- CLI SURFACE DELTA — analysis at cli-surface-delta-2026-08-01.md, AWAITING FLYNN.
  10 families ship unratified (identity, onboard, attend, topline/toplines, four
  work-item verbs, artifact-record); 3 are ratified with NO shipped consumer
  (run-smoke, run-tests, skill — and skill put/rm already exist as
  `identity edit --skill`). An earlier scan called the 3 a code gap; that is backwards —
  by cli-surface-v1's own demand rule they do not belong in the surface. The test
  `help_enumerates_exactly_cli_surface_v1` claims exact conformance and asserts neither
  list. Recommendation in the analysis: amend the enumeration, fix the test, and rule
  separately on whether rails should dispatch mechanical evidence at all.
- MAIN @ 35e314e: merged — ...ATTEST, WORK-ITEM, CHECK-TIER, CONTAINMENT-WALL (macOS Seatbelt gating, posture-off default), SUPERVISION (r20: reaction executor + prod ladder + atomic-fire + reserved-origin), CODEX-GATES (r5: harness-neutral rails + fail-closed codex spawn wiring-check; harness-support matrix Rails rows → ✅). Manual harness-under-wall gate is pre-first-use before turning containment on. Remaining: observability (building — unblocked by supervision merge).
- ATTEST: built + reviewed CLEAN on branch attest (f739c07; principal seam verified unforgeable; both race tests genuine). MERGE-READY, awaiting Flynn — unblocks the supervision build. Two advisory test nits recorded in the review (revoked-CHECK negative row; role-filter e2e) — non-blocking.
- SUPERVISION: spec at r8 (8 adversarial rounds; exactly-once counting / at-least-once delivery, outbox + pendingK, tick-delivery, counter split, retired holders stranded-never-woken). r8 confirmation review in flight. Builds after attest merges.
- CONTAINMENT: r3 (local-host-only scope) NOT-READY with 6 blockers that are genuine OS limits (POSIX exit-code bits, Darwin signal races). RECOMMENDATION pending Flynn: park the build, bank the design as the honest-90% boundary. Surfaced real debt: bare remote paths in deliver_home/ensure_dir (own hardening ticket).

## Queue (ruled order)
00. SAMPLE-THEN-ACT — DE-ESCALATED 2026-07-30 AFTER SEVERITY ANALYSIS.
   Flynn's ruling: "the races eventually recover because of a mind, and such
   races are recoverable, so by definition the system is USABLE... this weighs
   against getting to production install as an MVP quicker than solving every
   little problem as long as the core loop works." He is right, and the earlier
   escalation was made on a COUNT (27) rather than on severity — gating on a
   proxy instead of the edge, the very error T-guidance now forbids.

   THE CORRECT FILTER IS NOT RECOVERABILITY, IT IS NOTICEABILITY. A race that
   recovers loudly costs a retry; a race that recovers SILENTLY 24h later is an
   undiagnosable incident, because the dark factory's minds are in the recovery
   path but cannot be summoned by a failure that leaves no trace.

   PRODUCTION GATE (small, does NOT block gibson):
   - MUST FIX — unrecoverable by any mind: F3 (model swap leaves record and
     running agent disagreeing, no tiebreak) and F4 (SIGKILL to a process group
     by a released pid — reaches OUTSIDE the system, which minds-in-the-loop
     cannot cover).
     STATUS 2026-07-31: F3 CLOSED — model fence and reconciliation merged in the
     concurrency batch; the ruling that settled it is user intent wins, the record
     is canonical only when known (concurrency-strategy-2026-07-30.md). F4 CLOSED —
     merged 028af86 2026-08-01. THE MUST-FIX LIST IS EMPTY.
   - MUST BECOME LOUD (cheaper than fixing): F1's 24h invisible park, the Wakes
     self-call that retries forever as a log line, and F2 recording a credential
     revocation as a clean teardown. Visibility restores the property that makes
     the rest tolerable.
   - EVERYTHING ELSE — fix as encountered. 15 of 27 are legibility or narrow
     availability; they are recorded in the audit and not worth a day each
     before a production install exists.

   The strategy document (concurrency-strategy-2026-07-30.md) stands as the
   class analysis and the prevention mechanisms; its SEQUENCING is superseded by
   this ruling. Guard A stays worth landing opportunistically — it is cheap,
   measured clean, and closes the class against recurrence rather than chasing
   instances.

   TOPOLOGY PROBE RUNNING (2026-07-30): testing whether the answer is structural
   rather than disciplinary. Three hypotheses: (H1) gating facts are DUPLICATED
   across process state and the DB — "a turn is running" exists as both
   SessionLane.task_ref and turns.status, which is why the identity-apply fix
   needed a DB read AND a lane call; (H2) THE LOAD-BEARING COUNT — for each of
   F1-F27, would the defect have been impossible to write if the gating fact lived
   in the DB and the decision were one transaction? High count = topology is the
   answer; low count = discipline is; (H3) feasibility and MEASURED cost of moving
   gating facts to the DB, plus the layering rule that would forbid F2's call cycle
   and whether AdapterCoordinator's globality (the reason F2 stalls every session
   on every harness) is load-bearing or incidental. A disproof is an acceptable and
   valuable outcome.
   (Flynn, 2026-07-30: "6 different race incidents is dangerous and concerning
   because our system makes these likely.")

   SIX races in two days, one shape: code reads a fact it does not own, then acts
   on that reading elsewhere — another process, or the same one after a yield —
   and the fact changes in between. Instances: Rules.decide sampling episode state
   with the actor enacting later; an observation window and a ledger read not being
   one operation; identity-apply sampling "is a turn running" then bouncing the
   adapter; that fix's own :no_lane fallback, where a lane could be BORN in the
   window; an abandoned request still mutating state after its caller timed out;
   and Dispatch.dispatch/3's three-way return mishandled at 4 of its 6 consumers.

   WHY THE SYSTEM MAKES THEM LIKELY (the indictment, stated so it is not mistaken
   for six unlucky bugs): the decision layer is deliberately effect-free, so every
   decision is enacted by someone else, later — the gap exists BY CONSTRUCTION.
   Effects here are slow (adapter I/O, ssh, model turns), so the gap is wide. The
   DB owner serializes individual queries, not decide-plus-enact. And there are
   many owners, so there are many gaps. Every future feature that decides then acts
   inherits this unless something stops it.

   RULED NOT TO DO: generalize the owner pattern into a shared closure-runner. The
   generic form (run a caller's closure inside an owner) is the WEAK form and
   caused a separate defect — it parked a lane on adapter I/O and started timing
   out an unrelated verb. The strong form is named domain operations inside the
   owner, which are domain-specific by definition and cannot be generalized.

   AUDIT COMPLETE 2026-07-30 — full report: sample-then-act-audit-2026-07-30.md.
   THE POPULATION IS ~27, NOT 6. Six Tier-1 findings, all silent and
   high-consequence: an escalation answered in seconds can park a session for 24h
   invisibly (cursor minted after the fact it waits for); a credential event on one
   harness can DEADLOCK the shared adapter serializer, stalling every session on
   every harness, with the cleanup silently skipped so a revocation records as a
   clean teardown (direct T-CONCURRENCY violation); an operator model-swap mutates
   the live harness BEFORE the ruling CAS so the record and the running agent
   disagree with no tiebreak, and the code comment claiming rollback covers it is
   false; the containment wrapper SIGKILLs a process group by a pid it already
   reaped, so under pid reuse it can kill an unrelated group; a canceled wake is
   still delivered because the guard runs after the enqueue; and one remedy
   transition is missing the occurrence token every sibling carries — a
   one-predicate fix. Plus 6 Tier-2 and 15 Tier-3, and a NON-RACE finding worth its
   own attention: SessionLane's documented quarantine-after-orphan contract DOES
   NOT EXIST IN CODE (never set true; the resolver's signals are dropped by a
   catch-all), i.e. a stated safety behavior that is fiction.
   GUARD VERDICT: a general grep ban is IMPOSSIBLE (the read and the act routinely
   live in different modules; no syntax marks a read advisory) — but three narrower
   guards are feasible, and Guard A (every mutating statement on a re-enterable
   lifecycle must name its occurrence token) measured ONE true positive and ZERO
   false positives against all 87 UPDATEs in lib/ today. Guard B (marker-prefixed
   samplers + frozen per-file call counts) is the only form that scales and forces
   the safe/racy question into review at the one moment it is decidable.
   NEXT: (2)
   DELETE THE AFFORDANCE — owners stop exporting reads of their own facts, so the
   racy version cannot be written rather than merely being discouraged. (3) GUARD —
   a build-failing check in the idiom of the two the repo already ships, so a
   seventh instance fails CI instead of a review round. Guidance already landed at
   both altitudes (spec-writer "Detect the event, not a proxy for it" + "Say whether
   a check and its action are one step"; coder "Detect the event, not a proxy for
   it" incl. read-and-act-in-the-same-place).

   OPEN WITH FLYNN: extend T-SOURCE with the enactment half — decisions about a fact
   are made AND enacted where the fact lives; where no single owner exists the
   enactment carries a conflict check or a fencing token, never a re-read. That one
   sentence would have prevented all six.

0a. ARTIFACT-RECORD CARRIER — FIXED AND FRESHLY PROVEN LIVE (landed 982686c
   2026-07-30; shrdlu A2 walk clean with NO workaround: all four gates in
   order, real CLI artifact-record SUCCEEDED with recordedTurnEvidence =
   tool-call-observed and a genuine non-null message edge; eb0ea2b REVERTED
   as identity 83dc134, org law byte-identical to bundle again; fence proven
   deadline-dominated under load, 4ms spread. 0a2's artifact-record entry
   closes with this. R7 CODEX LIVE HOOK PROOF: ANSWERED 2026-07-30 12:12Z —
   codex-recorded artifact art_0f26ec21 reads recordedTurnEvidence =
   tool-call-observed with a resolving non-null message edge, honest grounded
   lifecycle (verified byHarness=codex, assignment closed/completed). BOTH
   legs now read tool-call-observed through the journey path (claude
   art_85425764, codex art_0f26ec21). T2a SUBSTANCE (artifact-record +
   completion-gate closure on both harnesses) is substrate-proven; the
   journey's group-12 DENIAL ASSERTION still fails on the known
   capable-holder race (P2 redesign in progress — assertion scaffolding, not
   substance). T2a BOTH LEGS 13/13 (2026-07-30 13:44/13:47Z, main 16b82d1): all five
   must-confirm items on BOTH harnesses; four symmetric rows — A1 negative
   controls art_a5af8bad (claude) / art_09245ad1 (codex) both session-concurrent
   releasing the evidence-blind gate, A2 carrier proofs art_f9096c99 (claude) /
   art_042283d4 (codex) both tool-call-observed with non-null edges; four
   denials in order both legs; holder outcomes never abandoned; margin reported
   as 2 materialized / 1 started, the healthy steady state. Obtained as TWO runs
   on one SHA and org (see the parity blocker below), disclosed not laundered.
   T3 ANSWERED 2026-07-30 12:30Z: the hop is
   LOSSLESS — satellite-recorded art_8a59aa6d on eurisko reads
   tool-call-observed with a resolving non-null edge, full satellite chain
   closed (cross-harness cross-host review, holder placement proven live). A/B
   proof: the earlier degrade (art_919a7929 session-concurrent) was a STALE
   SATELLITE CLI, not the hop — one variable, binary md5. REMAINING GIBSON
   GATE: group-12 assertion redesign (P2, in review), one full-parity journey
   rerun on linux, a macOS T2a run (both-platform scorecards require the
   carrier era proven on both platforms), scorecards, no waiver hiding a
   failed load-bearing leg.) Original ruling record (Flynn, 2026-07-29; R1–R7 in
   artifact-carrier-proposal-v1's status block and the decisions ledger).
   IMPLEMENTATION ACTIVE: fail open; nullable recordedMessageId +
   recordedTurnEvidence (tool-call-observed | session-concurrent | none);
   hook-seam observation; clauses 8/11 + C1 note amended (former exactness
   recorded unsatisfiable, not closed); completion gate preserved; clause 12
   separate and open. GIBSON ACTIVATION GATE (R7, verbatim): carrier repair
   passes independent source/spec review, then T1; T2a artifact-record +
   completion-gate closure on BOTH claude and codex; codex live hook proof; T3
   satellite observation across the network hop; revert eb0ea2b; both-platform
   scorecards with no waiver hiding a failed load-bearing leg.)
   PROVENANCE, condensed: the running-turn derivation was built and REJECTED
   against core-causality-fixes-v1 §C1 (concurrency ≠ causality); the ruled
   design replaced exactness with substrate-observed evidence classes; the
   old parked branch remand/artifact-record-firing-turn (83b3602, local to
   scratch/wire-seam-lane) is SUPERSEDED by the landed carrier — prune it
   with the end-of-phase lane sweep, do not revive it.
0a2. E2E-FOUND DEFECTS (linux run, 2026-07-29, main 73d5817):
   (The artifact-record entry that lived here CLOSED 2026-07-30 with 0a's
   landed carrier; eb0ea2b reverted as ruled — retired together.)
   - SILENT REMEDY NO-OP on retired-session role binding — dark-factory class.
     REPRODUCED AGAIN 2026-07-30 (same org, same binding); aggravated: the
     handle is permanently consumed (UNIQUE constraint + no role-bind verb =
     the org can never recover that role binding). Priority up.
   - NEW BEHAVIORAL HAZARD (2026-07-30 walk): an agent meeting a gate it
     cannot satisfy may SURRENDER the assignment, closing it permanently
     (outcome=surrendered) — later verdict filings fail assignment_closed;
     recovery = fresh assignment only. Will bite unattended runs; wants a
     guidance line and/or a named refusal path.
     A completion denial recorded reason=remedy_fired but a role bound to a
     RETIRED session produced NO episode row and NO assignment, silently. Spec
     already makes unresolvable targets fail LOUD (`unbound-reviewer-remedy`
     fixture); a retired-session binding is a third case that must join it.
     Aggravator: no role-bind/role-rm in the CLI, so the state is operator-
     unrecoverable without git surgery.
   - spawn --name collision leaks a raw SQLite UNIQUE-constraint 500 instead of
     a named refusal. NARROWED by follow-up: legibility-only — the insert rolls
     back cleanly, no session row is written, no orphans exist. Fix the error
     surfacing, do not hunt partial writes.
   - CLI gaps: `identity edit` cannot touch rules/ (org-law edits require git
     surgery replicating publish_live! semantics); no role-bind/role-rm verbs.
   - IDENTITY-APPLY BOUNDARY SEMANTICS (2026-07-30 smoke blocker, design
     question): identity_apply_sessions (gateway.ex:2048) counts queued+running
     as busy, so a headless org's Main — which queues indefinitely with no
     client, the NORMAL state per TEST-HOSTS §3a — makes org-wide apply
     permanently impossible. The crisp question: a session with N queued and 0
     running turns is arguably AT a turn boundary (nothing is mid-turn; a
     queued turn starting later under newer identity is indistinguishable from
     any turn started post-apply). Candidate fix: filter on running, not
     pending. Needs spec adjudication, not a rush job — but ESCALATED IN
     WEIGHT 2026-07-30: the wedge REGENERATES within a single smoke run (25
     drained at 09:37; one partial run rebuilt 9 by 10:30 from its own bracket
     nags and DR notifications). Every smoke run manufactures its own wedge;
     the running-not-queued filter is what makes the smoke repeatable at all,
     not a nicety. HARD BLOCKER AS OF 2026-07-30 13:47Z: single-invocation FULL
     PARITY IS STRUCTURALLY IMPOSSIBLE — measured, leg 1 manufactures the wedge
     that kills leg 2 (drain at 13:43:25 → Main 0; claude leg 13:43:43; 8
     process:tightbeam turns queued 13:44:04-13:45:10 from its own bracket nags
     and DR notifications; codex leg wedged on identity-apply ~13:45:1x). A
     pre-run drain cannot help: the backlog is created BETWEEN the legs, inside
     the invocation. Parity was obtained as two runs on the same SHA/org
     (claude from the parity invocation, codex from a filtered one) —
     defensible but not one invocation. This adjudication now gates the gate's
     own parity requirement. Interim: STANDING pre-run drain on the shrdlu test org
     (stop/backup/mirror-cancel/verify, the authorized procedure) before every
     smoke attempt until adjudicated.
   - STALE-POINTER APPLY DEFECT (2026-07-30, fix lane active): identity apply
     on any session whose harness pointer survived a gateway restart dies with
     raw -32603 "Session not found" — the pointer's adapter session no longer
     exists. Proven: never-started sessions succeed; any started-then-restarted
     session fails; Main always qualifies and cannot be retired. Net: `identity
     apply --all` is broken on ANY org after ANY restart until every session is
     resumed. Fix shape per §Sessions doctrine: a pointer whose adapter session
     is gone = never-started (:noop — the session materializes from
     tightbeam/live at next start, so identity is current by construction).
   - DECISION-PENDING WIRE GAP (2026-07-30 smoke group 12, fix lane active):
     dispatch_response/4 (router.ex:782) cases on two of Dispatch.dispatch/3's
     three declared returns — {:decision_pending, id} hits no clause,
     CaseClauseError, empty body, CLI EOF. The EFFECT still applies (DR opens,
     assignment closes) — only the response dies, so DB-asserting tests pass
     while every real CLI caller of an escalating verb hard-fails. Third
     passing-test/real-caller gap of the night.
   - RETIRE STRANDS QUEUED TURNS (2026-07-30, same trace; now THREE retired
     sessions holding stranded turns — one per smoke run, reproducing exactly
     as described): retiring a session does not terminalize its queued turns — a check-in turn queued at retire
     time sits queued/startedAt-NULL forever with no lane to run it. This is
     the GENERATOR of the Main 25-turn wedge drained earlier tonight. Joins
     the boundary-semantics adjudication cluster (the substrate structurally
     cannot terminalize queued turns — retire needs a sanctioned path to close
     what it strands).
   - DECISION-PENDING CONSUMER CONTRACT (one ticket, band-aid gate: one
     contract, five readers, four wrong): Dispatch.dispatch/3's three-way
     return is mishandled at 4 of its 6 call sites. Fixed 2026-07-30:
     router.ex dispatch_response (the smoke-found crash). Remaining, each
     needing its own semantic answer: control_response :793 crashes on
     escalated cancel/tune; socket.ex :433 crashes a LIVE WebSocket handler on
     escalated post (rail_script_test's own escalate fixture uses verb post);
     supervision.ex :687 crashes the sweep on escalated wake; rail_remedy :228
     silently mislabels an escalation as outcome "blocked". Root shape: the
     return has no enforced contract at consumers — consider one shared
     response-shaping seam or an exhaustive-match struct so a missing clause
     is a compile error, not a runtime crash. None are reachable by the
     current shrdlu org's law (no statutes on post/wake/cancel/tune).
   - CLI STALENESS = SILENT OBSERVATION LOSS — THREE SURFACES (2026-07-30 T3 +
     macOS pre-check, dark-factory class, PRIORITIZE). Scope widened by the
     macOS run: it is NOT satellite-only. (1) satellite bin/ via assimilate;
     (2) the GATEWAY HOST's own org bin/ (found stale pre-carrier on eezo,
     md5 023a8f70, answering "unknown command: tool-call-observed" — caught by
     pre-check, would have made both macOS legs read session-concurrent and
     produce the false conclusion "macOS loses the observation"); (3) CORRECTED by the fix lane's code read: local sessions do NOT
     use the gateway's launch PATH (they get config.cli_bin prepended,
     placement.ex:954, installed fresh each boot by install_cli_bin — the eezo
     staleness was cargo not rebuilt before restart, with nothing comparing
     artifact to tree). The real third surface: a REMOTE hosts row with null
     cliBin yields PATH=:$PATH, so that satellite resolves `tightbeam` from
     ambient PATH or not at all. No enforced coupling on any of the three. Mechanism:
     assimilate ships the CLI once; nothing re-ships on gateway upgrade.
     PRESERVED SPECIMEN, do not "clean up": eliza's CLI on the shrdlu org is
     deliberately left stale as a natural reproduction case for this defect
     (nothing places there; 30s to heal by re-assimilating when the fix lane
     wants a before/after). Likewise the eezo gateway pid 59119 on 11373 and
     its org ~/.tightbeam-e2e-mac-0729a stay up: the macOS scorecard evidence
     lives in that org's DB (TEST-HOSTS §5 — the installation stays); the projected hook calls a subcommand a
     stale binary lacks ("unknown command: tool-call-observed") and its
     fail-open swallows the error invisibly — artifacts silently downgrade to
     session-concurrent on every org whose satellites predate the last
     upgrade, i.e. eventually all of them. Fail-open is RIGHT (agents must not
     block on a broken hook); the missing piece is the coupling: version-check
     at assimilate/boot, re-ship on mismatch, and/or a doctor check that
     compares satellite CLI identity to gateway. Healed on eurisko by
     re-assimilation (md5 now byte-identical).
   - ADVERTISED-URL SCHEME UNVALIDATED (2026-07-30 T3): ws:// in
     TIGHTBEAM_ADVERTISED_URL propagated into every satellite gateway.json and
     adapter env, breaking the ENTIRE satellite CLI surface ("Unknown Scheme");
     docs say http://, nothing normalizes or validates, doctor's
     advertised_url_check asserts non-empty only. Fix: validate/normalize
     scheme at config load + doctor check. Healed on shrdlu via drop-in
     20-advertised-url-scheme.conf.
   - CLI gap, fourth instance: assignment-get is in router agent_verbs but not
     the Rust CLI (holder routed around via work-item-trace). Joins
     role-bind/role-rm, rule, cancel.
   - Satellite artifact originPath lacks host prefix (bare ./relative where
     gateway rows carry host:/abs/path) — ambiguous about which machine holds
     the file.
   - ERROR-BOUNDARY SEAM (one ticket, FIVE instances): raw internal errors
     reaching operators — spawn --name UNIQUE constraint; artifact-record
     invalid --kind SQL CHECK; identity-apply JSON-RPC -32603 (twice);
     artifact-record missing required param surfaces a raw Elixir KeyError in
     server_error AND ECHOES THE ENTIRE PARAMS MAP back to the caller (harmless
     on this verb, a shape to kill before any verb carries anything sensitive).
     Different call sites, same missing seam: no boundary converting internal
     failures into named refusals.
   - Evidence for the boundary-semantics adjudication above: the substrate
     structurally CANNOT terminalize a queued turn (Ledger.finish_in_txn
     matches WHERE status='running'; SessionLane.cancel_current returns
     :not_running with no lane) — the 2026-07-30 drain had to close 25 such
     rows by hand, honestly marked canceled-never-started.
   - SHAPE (2026-07-30 census, 11 git shell-out sites audited, zero live
     defects): Identity.git!/3's `author \\ nil` default means a future
     commit-creating caller that forgets the argument silently inherits the
     bare-commit bug (host-dependent "Author identity unknown" crash). Close
     the shape: require author on the commit path, or make git_env(nil) raise
     for commit-shaped invocations.
0a3. GUIDANCE-NEUTRALITY LEAK (macOS e2e run mac-0729a, needs its own ticket):
   operator user-scope ~/.claude/CLAUDE.md reaches satellite sessions — claude
   resolves user memory from the real $HOME even though the projected home
   redirects the config dir. Guidance Tightbeam never composed reaches the
   model, and enforcement results on any host with an operator CLAUDE.md become
   unfalsifiable (the tars agent self-declined a gated command "not the
   runtime, me"). Platform-general in principle. Riders from the same run:
   archetype-not-in-live-rev kills the FIRST TURN as :task_crash instead of
   refusing at SPAWN (message text is good, timing is wrong); no verb advances
   tightbeam/live (publish_live! private — hand-placed identity content needs
   git surgery); ASSIMILATION-E2E §3 hosts.json and SMOKE step 20 spawn-vs-turn
   projection claims are stale docs. UPDATE (tars-gw-0729b): the first-turn
   crash and the no-verb-advances-live gap BOTH reproduced independently on
   tars — confirmed gaps, not one-offs. Also: Elixir 1.20.2/OTP 29 builds and
   runs clean (new type warnings only) — README's 1.19/OTP-28 pin should be
   stated as a floor; enforcement rows byte-identical across gateways on
   different OTP majors.
0b. WIRE-VOCABULARY CONTRACT (missing design contract, band-aid gate fired 2026-07-29):
   three independent wire-word→handler-atom maps disagree — router `atomize_params`/
   `@param_aliases`, `control_call`'s hand-built camelCase atoms, and
   `rail_remedy.ex` `rename_param` — confirmed by two independent censuses. Root fix:
   one per-verb vocabulary authority + a read-set contract test (every wire key a verb
   emits must be read by its handler under the atomized name). Riders found in
   passing: latent `tune` reasoningLevel mismatch on /agent/dispatch (loud, no emitter
   today); `artifact-record` invalid --kind returns a raw SQL 500 instead of a
   refusal; dual reviews/reviewsAssignmentId keys collide last-wins (undefined, unspecced).
1. Deploy merged main to the gateway (one-time global home regen fires) — needs Flynn's go.
2. SMOKE MATRIX full run — docs/SMOKE.md; 4/32 done, one harness of two; scorecard per run (docs/smoke-runs/). Loudest debt.
4. ATTEST primitive + SUPERVISION build — supervision-v1.md (stall predicate, prods, ladder). Needs its implementation spec.
5. Per-session CLI tokens — containment-v1.md §cheap win.
6. Containment build — spike PASSED 2026-07-20 (containment-spike-report.md); impl spec being authored.
7. Codex gate projection spike (codex 0.144+ hooks confirmed; harness-support.md rails row) — wire rails gates for codex homes.
8. Rust CLI follow-ups: `tightbeam probe` subcommand (supervision diagnostics); TS repo retirement decision (Flynn).

## Waiting on Flynn specifically
- ATTEST merge (f739c07) — gates the supervision build lane.
- SMOKE shape: satellite-form (test gateway on eezo, shrdlu assimilated as session host, clawline sim on eezo e2e — recommended) vs gateway-on-shrdlu (needs Elixir installed there). Plus two shrdlu credential ceremonies (~5 min total: claude setup-token + codex device-auth).
- Zombie-droppings discard in tightbeam_ex-idv2 (git restore needs explicit OK).
- Kungfu guidance (first-party school content — Flynn's process distillation).
- Periodic safety sweep (Janus-style 5-min) — adopt into supervision or defer; restart recovery sweep is already in.
- Containment: park vs continue after r3.
- Tars claude ceremony (3 min) — makes tars a full satellite.

## NEAR-TERM (Flynn ruling 2026-07-20 — need, not difficulty, sets priority)
- Codex gate projection — PROMOTED from deferred. Rails/statutes compiled into codex homes. NOT parity-cosmetic: codex is the PRIMARY coder (the harness running git/rm/builds), so rails-on-Claude-only is the guardrail on the parked car missing from the driving one. Same need as rails, more consequential surface. codex 0.144+ has the hook surface; this is projection work.
- Containment WALL — PROMOTED (the gating half only). Kernel deny-writes-outside-workdir (Seatbelt, spike-PROVEN, r3-confirmed). The literal rails extension one layer down: gates EFFECTS regardless of tool/subprocess/harness/enumeration — the backstop rails structurally cannot be (an unenumerated shell-out escapes rails, not the wall). Flynn: if rails matters this does. Build from containment-impl-v1 r3's gating sections; the 6 r3 blockers clustered in CUSTODY, which is separable.
- Containment CUSTODY — stays BEST-EFFORT (90%, supervision-flavored). Process reaping / tree-emptied detection; the hard OS-wall half (Darwin signal races, POSIX exit bits). NOT the rails-extension concern; honest at 90%, not chased to kernel-perfection.
- Check tier — report-done gated on required fact rows (builds on attest).
- Observability-v1 — derived-state events + query surface + board consumers.
- Work-item-v1 — durable feature identity across re-staffing.

## Later / design-ready but unqueued
- work-item-v1 (SCHEDULED 2026-07-20, Flynn): the durable work-item object — id + title + spec ref, NO state (states stay derived); successive assignments reference it (workItemId on assignments, nullable — assignments without one remain legal), giving work identity across re-staffing and threading revoke+reassign eras into one history. Extends attest's schema additively; spec after attest merges, build after supervision (small lane). Feeds observability-v1: work items are the natural kanban card unit (falling back to bare assignments for cardless work).
- observability-v1 (RULED 2026-07-20, decisions ledger): derived-state events interlaced on the same wire as chat, per-connection filters; kanban/dashboards as filtered consumers; clawline interlaces state events between bubbles. Generalizes the marker mechanism. Spec after supervision lands (its stamps feed the derived status).
- Transcript projection (one mechanism, three consumers: harness-switch continuity replacing the history barrier, spawn-with-context, peer pull-reads) + recording ACP tool-activity updates into the ledger. Ruled follow-up 2026-07-20; decisions ledger has the ownership split.
- Rooms (deferred by Flynn), interop/mesh (deferred).
- Memory skill (long-term memory follow-up; substrate half exists via durable workdirs).
- Check tier (report-done gated on fact rows) — builds on attest + statute machinery; claims-vs-facts design in decisions ledger.
- Reaction rails beyond supervision (fallback switching etc.).
- Org templates: review-pipeline-as-archetypes, tightbeam-dispatching skill (delegation playbook as shipped skill).
- 24h soak (driver merged; run it: `mix run scripts/soak.exs -- --minutes 1440`).
- Kill matrix on satellites / multi-host chaos (soak v2).
- openclaw migration (after Flynn lives in the system; guidance moves via archetypes).
- npm packaging (Flynn 2026-08-02): publish tightbeam so a test install is `npm install` rather than clone + `mix deps.get` + `mix compile` + `cargo build --release`. Drivers: the README install is the path under test and it is long; a family member's machine should not need a toolchain. Open questions Flynn has raised and not ruled: how elixir gets bundled, whether bun is better than npm, and whether codex/claude come along or stay a prerequisite (they are already required on PATH before install). Note the harness CLIs are already npm packages and the ACP adapters are installed via npm into `<base_dir>/adapters`, so npm is already in the runtime contract — this makes distribution match how the dependencies already arrive.

## Codex parity (from the 2026-07-20 harness-matrix reality audit — codex was systematically undersold; corrected in harness-support.md)
- NATIVE SKILL PROJECTION (real parity upgrade, retires a workaround): tightbeam currently ships codex skills as read-on-demand (guidance says "read SKILL.md at this path"). Codex has NATIVE progressive-disclosure skills at parity with Claude — project each skill into `$CODEX_HOME/skills/<name>/SKILL.md` (tightbeam controls CODEX_HOME) so codex agents get the native `### Available skills` catalog + lazy body load, same as Claude. LOAD-BEARING detail: codex STRICTLY rejects unknown frontmatter keys — the projection must translate/strip to codex's allowed set (name, description, optional metadata, disable-model-invocation:false; keep descriptions tight, ~2% skills budget). Also correct the `tightbeam-harnesses` builtin skill + the operations guidance pointer (archetypes.ex) that tell codex agents to "read on demand" — describe codex skills as NATIVE, parallel to Claude.
- CODEX TOKEN-ENV parity: codex has env-token auth (CODEX_API_KEY/OPENAI_API_KEY, `codex login --with-api-key`/`--with-access-token`) — the "rotation-war immunity is claude-only" claim was false. LIVE-TEST NEEDED: does it give the same ChatGPT-subscription rotation immunity as CLAUDE_CODE_OAUTH_TOKEN, or only API-billing/short-lived? If yes, codex gets the same rotation-proof grant treatment as claude.
- CODEX COMPACTION VISIBILITY: codex is AHEAD of claude — codex-acp emits STRUCTURED compaction over ACP (thread/compacted, contextCompaction item). The deferred compaction-indicator work (blocked on claude dropping structured compaction) is DOABLE for codex now. LIVE-TEST: consume it end-to-end into the tightbeam client.
- MATRIX LIVE-TESTS still owed (not demotions): codex cancel/queueing/restart re-adoption over ACP; the token-longevity nuance above; codex compaction end-to-end.


## From the 2026-08-03/04 hardening push (findings + retro items; tracking only — mechanisms and rulings live in gibson-work-plan-2026-08-03.md and the session's findings)

Product, post-Gibson, in rough priority order:
- STALE ARCHETYPES AT SPAWN (found T3a re-run, CONTROLLED evidence): `identity apply --all` reports success + a revision, yet NEW spawns keep placing against the pre-edit archetype until the gateway restarts — where=["eurisko"] placed on the gateway pre-restart, on eurisko post-restart, all else pinned. Placement itself exonerated (it acts on what it is shown). Either apply must refresh whatever serves archetypes to spawn, or it must refuse/say it did not. T-CONSPICUOUS either way. Also retro-explains the lnx-0803-b confound (restart, not credential projection, did the work).
- CREDENTIAL TRANSPORT ASKS LOUDLY (Flynn ruling 2026-08-03): SATELLITE.md's flat ban becomes a named confirmation gate — what, from-host, to-host, why, explicit human yes — so the operation is recorded in-product instead of done by hand around it.
- CONSPICUOUSNESS SWEEP P1 (second half): promote the three private swallow-but-write helpers into EventLog.best_effort/3, sweep the 52 self-declared best-effort sites, delete the privates; after the sweep a naked error-swallowing arm is a one-grep review finding.
- T-CONSPICUOUS residue from the G5 audit: ~35 lifecycle call sites hold no human audience in lexical scope — that absence is the finding (task #20's ledger); revisit when the entities they key on (wakes, waivers, rules) grow user-facing surfaces.
- TOOL-CALL VISIBILITY (T-INTEGRATOR consequence 3, Flynn 2026-08-03): ACP tool_call titles/content are fully parsed for gates and shown to humans as a spinner; surface them as low-attention persisted markers once the G5 attention plumbing is client-supported. First consumer of the attention tiers.
- CLIENT-SIDE ATTENTION FILTERING: no client hides low-attention markers yet; the substrate half shipped with G5.
- CLIENT'S HALF OF THE DELIVERY-IS-A-HINT CONTRACT (ruled 2026-08-04; substrate half shipped at 71df27f): message frames now carry `seq` (store commit order), and the server never filters or deletes — so in the rare race a frame arrives late or twice instead of never. Nothing breaks unupdated, and the client's half is SMALLER than first recorded (Flynn caught the overreach): clients already anchor replies adjacent to their prompts via `replyToClientMessageId`, which places a late reply correctly with no seq at all — do NOT "sort by seq", that would fight the anchoring, which is a deliberate view choice over interleaved store order. What remains for whoever next touches clawline: drop a frame whose id is already shown (dedupe), and use `seq` to place the UNANCHORED frames — substrate markers, credential notices, another device's echoes — which have no prompt to sit beside. Until then the worst case is a doubled or oddly-placed marker bubble in a race never observed in testing.
- ORDERED CROSS-PROCESS PUBLICATION — RETIRED 2026-08-04: THE DEFECT IT EXISTED TO FIX WAS DELETED INSTEAD (71df27f, "delivery is a hint, the store is truth"). ConnRegistry no longer filters or deletes anything; the socket drain drops only literal re-sends by {session, seq} set membership; frames carry the store seq; the e2e oracle asserts seq fidelity rather than arrival order; codex leg PASS all rows on the real wire. The ratified after-COMMIT-publish-in-order design is NO LONGER LOAD-BEARING — publication order remains unguaranteed and now merely produces out-of-order hints the client settles (replies already anchor to their prompts via replyToClientMessageId; seq places the unanchored frames). Do not build the ordering design without a NEW motivating defect. Historical record follows, kept because its corrections carry the method:
  (was) REAL IN CODE, AND UNCOVERED BY ANY TEST. The defect: publication happens post-commit from the caller's process (projection.ex:95-97 commits; gateway.ex:1701/:1043/:5767 and event_log.ex:324 publish afterwards), so two writers to one stream can publish out of commit order, and ConnRegistry drops a frame at or below its per-session cursor forever for a connected client. G5's narrowing at event_log.ex:332-342 is the only mitigation today. NOT the cause of the row 10 failure it was promoted from — lane G8 instrumented append->publish->ConnRegistry on the failing leg and measured org_get 0ms, registry 0ms, publish->client 0ms, with commit order (seq 19, 20, 21) equal to publish order equal to arrival order: nothing was delayed, reordered or dropped. Row 10 was premise-fragile, not broken by the merge — its oracle inferred "the client should have seen X by now" from a fact that does not DATE X, and the merge only shifted timing until a trivial prompt (20.4s in a fresh stream) reliably outlived a deliberately-slow one (12.6s). SEVERITY RAISED 2026-08-04, AND A CLAIM RETRACTED — this entry twice said things that were false, both corrected by lane G8 against the code:
  (a) THE DROPPED FRAME IS NOT DELAYED UNTIL RECONNECT, IT IS PERMANENTLY LOST FROM THAT CLIENT'S VIEW. "Replay repairs it" was wrong. Replay serves rows after the CLIENT's own cursor (wire/socket.ex:319, `Projection.list_after/5` selecting `seq >`, with `after_seq` derived from the cursor the client supplies), so it restores the dropped row only while that cursor still sits behind it. A client that received the LATER frame has advanced past the earlier one and never sees it again — not on reconnect, not on a re-auth of the same socket (wire/socket.ex:299-303). Verified independently in `list_after/5`. The row REMAINS IN THE STORE, so this is lost DELIVERY, not lost data: a client connecting with no cursor still sees it, and `transcript` still shows it.
  (b) "J5 STRUCTURALLY CANNOT COVER IT" WAS FALSE. A session's lane serializes its TURNS, not the writes to it — a client post's echo and a running turn's reply are two independent writers to one session from two processes, with nothing ordering them against each other, and J5 creates both on its Main stream. The ingredients are present. The weaker follow-on claim (immune by timing) was also wrong, since nothing synchronizes those echoes against the first turn's reply. NOTHING IS CLAIMED IMMUNE: no reproduction has been observed, and whether J5's commits and publishes interleave badly is uncontrolled and unmeasured.
  (c) THE WINDOW IS NOT SIMULTANEITY. It is one publisher pausing between its commit and its publish while another completes BOTH inside that gap. A reproduction must hold that gap open; "make the writes simultaneous" chases the wrong thing.
  NOT RE-RULED AS A GIBSON BLOCKER, on this reasoning: never observed across a 60-minute soak, both e2e legs and the full journey suite; the window is narrow; the data survives in the store so the failure is a client view missing a message, recoverable by connecting without a cursor. If Flynn weighs a permanently-missing live reply higher than that, it moves — the facts above are what the call should be made on. DESIGN RATIFIED 2026-08-04 (Sol xhigh REJECTED the team-lead's per-session-publisher proposal — five factual errors, incl. an invented T-CONCURRENCY constraint): after COMMIT in DB.handle_call, send publications to the already-running ConnRegistry in list order, then reply; migrate ALL publication sites so the owner is the sole sender; keep the filter unchanged; no ticket/buffer/timeout/new process. Full design in ordered-publication-proposal-v1.md under RATIFIED DESIGN.
- TWO WRITERS OF ONE CREDENTIAL (watch, not fix): Claude Code and catalog-probe both refresh .credentials.json (atomic renames, lost-rotation self-heals). Standing rule: no third writer without a design pass.
- interrupted vs failed_unknown rename: internal status name says less than we know; user-facing text already right. CHECK-constraint change — free only while no prod DB exists. Do immediately post-merge-train, pre-Gibson-data.
- DOCTOR'S FIFTH COPY of the tier/absent rule (named by lane G3): fold into ModelCatalog.route when doctor gains a catalog server to read.
- EVENTS SCHEMA / kind registry: decide before any dashboard GROUP-BYs on the open string set — not before.

- A PARK DEATH ARRIVING AFTER THE GRACE EXPIRES IS STILL DISCARDED (reviewed, deliberately unfixed, merged 2026-08-04 with G7). `:grace_expired` means only "no :DOWN yet", not "the adapter is alive"; the adapter can die during `HarnessProcess.park/2`'s writes, and `retire_adapter/2`'s `demonitor(..., [:flush])` then throws that death away unread. Predates G7 and G7 does not widen it. TWO THINGS MUST BE TRUE BEFORE IT IS CLOSED, and the first is why the obvious fix is wrong: (1) `park/2` is "Deliver SIGKILL to a parked process group" — after grace expiry the coordinator kills the harness ITSELF, so a naive "record any late non-normal exit" files the coordinator's own planned kill as a fault, which is the false-record failure inverted; the fix must distinguish our SIGKILL from a genuine fault first. (2) a zero-timeout receive before the flush is NOT atomic with it, so it narrows the window rather than closing it. An attempt doing exactly that was written and reverted (340afb2 → 86f5189). DETERMINISTIC TEST EXISTS, contrary to what that attempt's commit claimed: `park/2` invokes the configurable process helper and performs several writes, so a helper wrapper that delegates `harness-exec` but signals and blocks on `harness-group` gives a real barrier — with grace zero, suspend the adapter, start the close, wait on the barrier, kill it, wait until the coordinator's monitor `:DOWN` is queued, then release the helper.
- CONN_REGISTRY'S MODULEDOC ASSERTS THE PRECONDITION IT DOES NOT HAVE (named by lane G8; fix first, whatever the ordering design turns out to be). conn_registry.ex:22-26 states the ordering requirement as already met — "guaranteed by publishing from the single-writer commit path (Tightbeam.DB)" — and it is not: every message publication reads as happening AFTER its transaction returns, from the caller's own process (projection.ex:95-97 commits; gateway.ex:1701 agent reply from the TurnTask, :1043 client echo via complete_delivery, :4142, :5195, :5767 through the helper at :5772; event_log.ex:324 after the DB.transaction block at :296-314). Publishes for ONE session originate in at least three process types — the TurnTask, the socket process, and whatever calls EventLog.notice or Assignments — which is the shape that makes commit order and publish order separable at all. A comment asserting a safeguard the code does not implement is worse than no comment: it stops the next reader looking. (Scope note: G8 checked the message path, not all 77 transaction sites.)
- TWO RELEASE GATEWAYS CANNOT SHARE A HOST, and the refusal is in the wrong vocabulary (found 2026-08-04 while proving the npm release). The bundled release takes a fixed Erlang node name, so a second instance dies with `Protocol 'inet_tcp': the name tightbeam_gateway@<host> seems to be in use by another Erlang node` — which names neither Tightbeam, nor the port, nor the base dir, nor the other instance. Not a Gibson blocker (Gibson runs one), but it is a T-CONSPICUOUS defect on the exact path a second tenant hits, which is the TARS shape ([[tars-boundary-is-openclaw-scoped]]): a test gateway beside another install. Either derive the node name from the base dir/port, or refuse by name in Tightbeam's own words.

Open questions (measured, mechanism NOT established — do not act on a guess):
- THE CLIENT-E2E CLAUDE LEG BLOCKS AT PREFLIGHT ON AN INTERMITTENT `ETIMEDOUT` (2026-08-04, lane G8 + team-lead). Post-repair ledger: 4 runs, 1 through, 3 blocked with `{:transport_exit, 70, "ETIMEDOUT: fetch failed"}` — a name visible only because d29a2da stopped both probes reporting every transport failure as the bare string "fetch failed". Blocked runs never boot, so all 20 rows read INCOMPLETE(preflight-blocked).
  RULED OUT by measurement, not argument: the grant (the same credential file returns 200 from the probe's exact request); the credential-store copy (`File.cp_r!` preserves the absolute symlink into the template's auth store, verified with dummy files); load saturation and host egress generally (40 consecutive curl connects at load average 11.14 — inside the 8.95–11.87 band where the timeouts happened — returned 40/40 in ≤0.52s, slowest connect 0.03s).
  ALSO RULED OUT, and this retires an earlier entry in this file that said the opposite: there is NO established template-vs-provisioned asymmetry. G8 retracted it against its own data — a provisioned leg PASSED outright (whole claude leg green, row 10 included), which a base_dir defect cannot do, and the template side was n=1, which at the observed failure rate passes by luck about a quarter of the time. ETIMEDOUT is a TCP connect failure, not a credential-read failure, so a bad base_dir could not produce it anyway.
  MEASURED FACTS ABOUT THE PATH, for whoever picks it up: node's `fetch` to that endpoint DOES fail intermittently from eezo — 2 ETIMEDOUT in 400 attempts (~0.5%), each completing in ~282ms — while curl over IPv4 never failed in any run. `api.anthropic.com` advertises an AAAA record (2607:6bc0::10), node resolves BOTH families, and **IPv6 egress to it is dead from eezo** (`curl -6` returns nothing, connect 0.000s). The ~282ms failure duration sits suspiciously close to node's 250ms happy-eyeballs attempt timeout. A controlled test of that idea was INCONCLUSIVE and must not be quoted as support: 400 attempts with family autoselection on gave 2 failures, 400 with `--no-network-family-autoselection` gave 0 — 2 vs 0 is not a result.
  RATE GAP CLOSED 2026-08-04 (lane G8, independently reproduced by the team-lead). THE AMPLIFIER IS ONE COLD CONNECT PER PROBE, and the fault underneath is IPv6 family autoselection against an eezo box whose IPv6 egress to that host is dead. Four arms, fabricated invalid token throughout, no credential copies:
    A  the leg's own probe path, as shipped            71/100 fail (37/100 in an earlier run)
    B  identical + --no-network-family-autoselection    0/100 fail
    C  100 fetches inside ONE node process              0/100 fail
    D  100 SEPARATE node processes, one fetch each     35/100 fail
  A and B were interleaved pair by pair, so drift cannot produce the split. C vs D is the same code differing only in process count, so the amplifier is the cold connect, not the leg: D (35%) lands on A (37%), meaning the leg's path adds nothing of its own — not the BEAM, not System.cmd, not the outer bounded_call, not concurrency (the failing runs ran one harness). Team-lead reproduced C vs D independently at 1/40 vs 15/40. Failures cluster at a ~313ms median against ~745ms for successes. "Happy-eyeballs" is the CONSISTENT EXPLANATION, not a proven mechanism: what is proven is that the flag removes the failure and its absence restores it.
  WHY THE FIRST CONTROL MISSED IT: 400 fetches through ONE process is roughly ONE cold connect, not 400 — a single draw that happened to yield 2 failures. The control's own caveat had named the hazard ("40 sequential connects is not what a leg does; connection-pool behaviour would not show up") and it was exactly right.
  BLAST RADIUS IS THE TEST TIER ONLY, established by reading: `credential_live?` is the sole node-`fetch` path (claude.ex:352, codex.ex:308) and its only callers are client_e2e.ex:222 and the fixture. Every PRODUCT network path — catalog derivation and the token refresh that rides with it — goes through `Support.catalog_probe_argv/2`, which is `sh -c` around CURL (support.ex:47-59), and curl did not fail once in any run. That is why the gateway derived catalogs and stayed READY all night while e2e preflight blocked 3 runs in 4. NOT a Gibson risk and not a product defect.
  FIX SPACE LEFT OPEN DELIBERATELY (measurement lane, no fix proposed): the node flag, an address-family preference, connection reuse across probes, or repairing IPv6 egress on the box — the last being an infrastructure question, not a code one. Choosing among them is a lane with its own review.
- GATEWAY SIGTERM TOOK 91s UNDER LOAD (2026-08-04 soak, merged main + G7): "SIGTERM received - shutting down" at 23:19:27.330, process gone at 23:20:58.6. Clean exit, status 0, nothing lost. Measured against it the same night: an IDLE gateway on the same tree exits in 1.09s, and the pre-merge soak measured 3927ms under comparable load. So the latency is load-dependent and MAY have regressed across the six merged lanes — suggestive, not conclusive (different arenas, single observation each). NOT a Gibson blocker: it exits cleanly and nothing on Gibson auto-restarts the gateway; the 91s only became fatal because the soak arena abandoned its restart. To pursue: boot with live sessions and adapters, SIGTERM, identify which supervision child blocks. Resist the arithmetic that 91s ≈ 18 children × 5s default shutdown — that is a hypothesis, and this codebase has been wrong three times in one night by preferring an inferred mechanism to a measurement.

Tooling/evidence-pipeline retro items (none touch core operations; each ~half a day, consolidate cold):
- THE ARENA SCORED ITS OWN ABSENCE AS THE PRODUCT'S FAILURE (fixed 2026-08-04, 66f6e9a — kept as the pattern). The soak's recovery oracle could not tell "my replacement is up" from "the process I just signalled has not finished dying", because the dying gateway serves correctly right until it stops; and when the restart was abandoned, the arena RECORDED `unexpected_exit` and carried on, so 27 of 29 kills and 53 of 60 minutes ran against a closed socket and verdicted FAIL against the product. Both halves are the house defect class, in the instrument rather than the substrate. Generalisation worth more than the fix: EVERY harness needs a liveness precondition on the thing it is measuring, checked each cycle — an instrument that cannot detect its own subject is missing does not report nothing, it reports zero. Same family as the ONE PROVISIONER item below.
- ONE TEST WIRE CLIENT: the x-tightbeam-cli-version header was patched into three hand-rolled HTTP clients (feature_smoke, soak, SimClient). Next wire gate breaks three things again until they share one client.
- ONE PROVISIONER: the soak arena needed five fixes in one night, each re-learning what client_e2e's template provisioning already knew. Soak should consume the same provisioning path.
- SATELLITE TRANSPORT CONTRACT: five gateway->satellite requirements discovered by face-plant (keys, ssh-config, scp/SFTP, advertised URL, credential projection) live as runbook prose; write the one-page contract and back it with a doctor check so the list stops growing by injury.
- TIER STALENESS AS A MERGE GATE (promoted from dashboard-idea after the 2026-08-04 sequencing slip): every tier records last-passed SHA; a merge whose diff triggers a map-required tier blocks until that tier ran against the candidate tree. The night's own lesson applied to process: unrun and failed must not look alike, and "verified" is the tier map's word, not the unit suite's.
- G5's e2e driver (adapter-kill -> [adapter down] marker -> replay) promoted into the smoke tier permanently.

## Salvaged from the retired gibson-deploy-checklist (Flynn ruling 2026-08-04: no special docs or tools for gibson — install per README like any user; the checklist is archived)
- VERSIONED MIGRATIONS arrive with the first durable DB (ruled 2026-08-01): adopt PRAGMA user_version in its own small commit at the first deploy that creates a database anyone keeps. Not gibson-specific — it is the first-prod-data rule.
- DEPLOY GATE (ruled 2026-08-01, stands independent of any host): the deploy artifact is main's HEAD, and THE gate is that commit full-smoked on the SMOKE machines (shrdlu gating, eurisko real-harness turns) — eezo is advisory under lane load. Note 2026-08-04: the doc's "shrdlu has no harnesses" is stale (codex onboarded there today); tonight's coverage on the deploy commit = T1 on shrdlu + real satellite turns driven from shrdlu via eurisko; the T2 journey runs were on eezo. WAIVED by Flynn 2026-08-04: tonight's mixed evidence suffices; "if shit doesn't work on gibson it's not the end of the world, we simply iterate."
- T2a still owes LEARN-IN-FORCE coverage (post-onboard, needs inference): guidance composed into what an agent is served, a rail gating a real turn, a rule denying one. T0/V0 proves mechanics only; proving knowledge requires an agent to act.

- A HOLD THAT ONLY A RULING CAN RELEASE IS NEVER ENTERED WHEN NO RULING CAN ARRIVE — SHIPPED (fc3cd15, 2026-08-04; Flynn's rule from mid-soak: "why queue at all if there's nowhere to deliver... if there's nothing to deliver to, log it and be done with it"). The gateway resolves the lineage ladder BEFORE holding: nobody to notify → log by name (session, condition, cause), no hold, no episode — the turn has already failed with its own reason. Somebody → the old path unchanged. The unclassified-fault lifecycle record is unconditional (it is the "log it" half; a fault with no one to tell is still a fault that happened). Supervision's escalation path already behaved this way; adjudication now matches. Red-first tested against the injected old behaviour.
- FIRST REAL PRODUCTION TOUCH (gibson, 2026-08-04): "hi" ON AN UN-ONBOARDED ORG ESCALATES TO ADJUDICATION INSTEAD OF NAMING THE REMEDY. Flynn's first clawline message reached Main before any credential existed; placement let the turn through, the adapter faulted, and the owner received the full adjudication brief (episode id, CLI syntax) whose own live_catalog said `needs_onboarding, :missing` for both harnesses. The plumbing was CORRECT end to end — ladder resolved the new admin, delivery worked, the hold healed path stood ready — but the words were hostile: the system KNEW the cause was a missing credential and still asked the user to adjudicate a model swap. Two-part fix: (1) placement should refuse a turn by name when the harness's catalog health is `needs_onboarding` — the same sentence boot prints, "no credential for anthropic on gibson; run `tightbeam onboard anthropic --as-user <id>`" — rather than spawning an engine that cannot start (same shape as G2's host refusal); (2) when an adjudication brief's cause resolves to a missing credential, the brief must LEAD with the onboarding remedy, not with park|swap|respawn|stop. T-CONSPICUOUS includes saying the RIGHT thing, not just saying something.
- ONE TERMINAL PUBLISHER (next lane, found by Flynn 2026-08-04 on the second production touch: "isn't there a single call used to bubble up errors to clawline?"). There is not, and the divergence IS the defect: `terminal_publisher/1` (gateway.ex:1993) appends the `[turn failed]` marker before publishing state and clearing indicators; the turn runner's own `failure_publish` (gateway.ex:1756) publishes state and clears indicators and appends NOTHING. Which one runs depends on whether the outcome happens to carry its own publish function — so the same event has two visible behaviours, and in-flight failures take the silent one. It only ever looked fine because the adjudication brief happened to be the message; suppressing the brief for missing-credential faults exposed a gateway that showed "agent progress interrupted" and never said why. `publish_turn_state` additionally has 7 call sites, each hand-assembling the same typing/activity broadcasts around it. FIX: one `publish_turn_terminal(db, session_key, correlation, state, error, opts)` owning marker + state + typing + activity in that order, with marker suppression an EXPLICIT opt for the adjudication-brief case (the one place another message legitimately speaks). No site can then silently omit the bubble, because there is no way to.
- HARNESS #3 (opencode) IS ADDITIVE EVERYWHERE EXCEPT credentials.ex (Flynn's question, 2026-08-04: "are our seams sharp or a spaghetti of conditionals"). Measured: exactly 7 harness-name references exist in lib/ outside lib/tightbeam/harness/, and ALL SEVEN are in credentials.ex — provider→store-path and provider→harness-name as hardcoded clauses (`harness_name(:openai), do: "codex"`, the auth.json / .credentials.json paths, the `System.cmd("codex", ["login", ...])` device-auth call). Adding a harness therefore means editing one unrelated module in four places, and missing one writes a credential to a path nothing reads. Everything else is already clean: `Harness.all()`, `module.credential_provider()`, `module.cli_binary()`, and now `module.default_model()`. FIX: move those three facts onto the behaviour (credential store path, harness directory name, login command). NOT so that adding a harness needs no code — it obviously does, and Flynn corrected that framing: an adapter mapping vendor-specific launch, session config, credential harvest and event classification onto Tightbeam is irreducible work. The standard is that ALL of it lives in ONE module implementing the behaviour, with nothing outside it naming the harness, so harness #3 is a bounded job the conformance suite can grade (it already refuses a new callback that the vector contract does not declare). Not urgent while there are two harnesses; do it BEFORE adding a third, because the cost of not doing it is paid as a bug hunt rather than a refactor.
- WHY IS SONNET THE DEFAULT? (Flynn, 2026-08-04 — no answer exists.) `claude-sonnet-5` was a literal in the boot path with no recorded decision behind it; the honest reading is "the model we were developing against". The 2026-08-04 change moved it from a system-wide constant to claude's own declared `default_model/0`, which fixes the codex-only breakage but does NOT answer the question — it relocated an undecided constant. Wants a real decision recorded in tightbeam-decisions.md: which model a fresh org runs on per harness, or whether the product should refuse to guess and require the operator to choose at first boot. Do not let this settle by inheritance a second time.
- ONBOARDING MUST NOT HALF-SUCCEED (gibson, 2026-08-04): `tightbeam onboard anthropic` wrote the credential to disk and THEN failed starting the provider runtime, leaving the store reporting `needs_onboarding` with a valid credential in it. Worse, the runtime that failed was CODEX's — an unrelated harness, unrunnable for its own reasons — so onboarding a working provider was blocked by a broken one. Two fixes: the verification step must be scoped to the provider being onboarded, and a failed verification must either roll the write back or record the credential as present-but-unverified with the cause, never as absent.
- READINESS DESCRIBES AN UNRUNNABLE HARNESS AS MERELY UN-ONBOARDED (gibson, 2026-08-04): with codex installed but unable to execute, the NOT READY summary said "Tightbeam has no credential for openai" — true and useless, since onboarding one cannot help. Boot now warns separately (see the harness_binary_readiness fix), but the readiness summary itself should name the executability failure as the gap, because that is the one an operator can act on.
- **[MOOT — 2026-08-12 amendment: adjudication holds were deleted 2026-08-05; this gap no longer exists. See `adjudication-deletion-amendment.md`.]** A HELD SESSION IS INVISIBLE TO THE CLIENT (Flynn, 2026-08-05: "where is that hold raised in clawline, how am i supposed to know"). `sessions.adjudicationHold` blocks every turn, and `Payloads.stream_session/1` does not carry it — the payload has name/kind/order/timestamps/origin and nothing about being blocked. So a held session is byte-identical to a working one in the stream list; the ONLY signal is the adjudication brief pushed once at hold time, which scrolls away, is missed if the client is closed, and (per the same night's finding) reads as CLI grammar rather than a state. Measured on gibson: two sessions held on stale `adapter_fault` episodes from the pre-onboarding period, three turns queued behind them, nothing in the client saying so. FIX: publish the hold as SESSION STATE (hold + cause + the ruling that would release it) so a client can mark it, explain it, and offer the decision — the same rule as the typing indicator, derived from durable truth rather than narrated once. This is the top-level T-CONSPICUOUS gap: the substrate knows the session cannot run and does not say so.
- STALE HOLDS ARE NOT HEALED BY THE FIX ARRIVING (gibson, 2026-08-05): both held sessions cite `adapter_fault:claude:shared@gibson` from before anthropic was onboarded. The credential landed, the adapter now boots clean, the catalog is fresh — and the holds remain `notified`, with turns queued behind them. The heal path (adapter recovery releasing a hold, observed as `adjudication_hold_healed` during the soak) did not fire for this shape. Either credential-arrival is not a heal trigger, or the trigger requires an adapter READY event this path never emits. Worth reproducing before designing: a hold whose stated cause has demonstrably cleared should release itself, or say why it cannot.

## From the production-machine push (2026-08-05/06)
- rails grammar: non-blocking `notice` effect (record + summon + allow) — arms
  the staged review-rounds doorbell in rules/engineering.toml
- rule facts: reviewer/author model+effort exposure — arms the review-staffing
  floor statute (gradient ruled 2026-08-05, floor = self/lineage or same-model
  strictly-lower effort)
- harness_processes: 'launching' rows claim a process across the whole
  Flight.await window; if the ledger wants "never started" distinct from
  "exited", that is a new terminal state + schema decision (finding from
  SMOKE 43, fix chose exited + lifecycle event instead)
- evals runner: docs/EVALS.md scenarios are TODOs until a driver exists
  (client-e2e journey machinery, eval mode)
- engram: codex ingestion is CWD-scoped and July backfill never ran; rebuild
  blocked on Flynn approving a bounce of ai.engram.watch-openclaw-sessions
  (125 GiB index bloat is the grep hang)
- `file-written` condition-fact convention (+ possible `tightbeam watch`
  sugar) if Flynn wants fs-event wakes blessed
- macOS build ignores SIGTERM/SIGINT (deploy-lane, 2026-08-05): no graceful
  stop on tars — C-c and kill -TERM both no-ops, and the release's own `stop`
  breaks once npm has overwritten the cookie on disk. Linux/systemd path traps
  TERM fine. Needs: signal handling parity + a stop path that survives an
  on-disk upgrade.
