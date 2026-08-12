# Supervision v1 — event-driven stall detection, prods, and escalation (design spec)

Status: DESIGN — ratified by Flynn 2026-07-19/20 (conversation: "what
prevents an agent from just giving up"). Implementation spec follows once
the statute engine lands (this builds on the same chokepoint machinery
and introduces the attest primitive). Origin: the week's delegation
retrospective — hand-run Sol lanes stalled silently (one 88-minute
zero-file stall caught only by a manually-armed check), and the question
"would tightbeam have improved this?" produced this design.

## The invariant being supervised

A resident must never end a turn with outstanding work and nothing on
the record: every turn-terminal leaves either a TERMINAL FILING
(completion attest / surrender), a CONTINUATION (pending wake the agent
scheduled), or it is STALLED. This is a residency norm (one line in
orientation/guidance); supervision is its deterministic backstop.

## Core principle: idle is an edge, not a state

Nothing polls. The gateway itself produces the only event needed — a
turn reaching terminal state — and the stall predicate rides that edge:

    stalled(session) :=
        turn just terminal for session
      ∧ no running/queued turn for session
      ∧ no pending wake targeting session
      ∧ ≥1 open assignment held by session

All conjuncts are ledger rows. Zero clocks, zero process inspection,
zero interpretation. Supervision cost scales with activity (quiet org =
zero evaluations); escalation latency scales inversely with misbehavior
(empty replies are themselves the events that advance the counter).

## The prod lifecycle (event → prod → row ∨ counter++ → ladder → Main)

1. Stall event → ONE prod: a wake, origin `process:tightbeam`, neutral
   fact-stating text carrying its own COUNTDOWN: "Your turn ended with
   no filing and no continuation scheduled for assignment <X>. File
   completion, schedule your continuation, or file surrender. This is
   prod <k> of <N>; a reply without a row escalates to your spawner."
2. A prod is satisfied only by STATE (rows), never speech:
   - terminal filing (completion attest / surrender) → assignment closed;
   - continuation wake scheduled → predicate false, prodding pauses (the
     clock is the agent's again; the next stall is a fresh event);
   - neither → the reply-turn's terminal is a new stall event →
     immediate next prod. No spacing: delay would reward empty replies.
3. Counter: per-assignment, counts consecutive prods without new
   PROGRESS FACTS (new attest rows for the assignment; scheduling a wake
   pauses but does not reset — pauses are not progress). Words never
   reset anything.
4. At N (policy; default 3): stop prodding the worker. LADDER:
   a. wake the spawner (`spawned_by` lineage — nearest supervisor, has
      context; judgment about why/what-next happens THERE, in an agent);
   b. if the spawner is itself stalled/retired/unresponsive past its own
      prod cycle → wake the assignment owner's Main (no-void terminus);
   c. stamp the assignment `stalled` (a fact row) at first escalation.
5. Everything — every prod, reply, escalation, stamp — is ledger rows.

## What the substrate never does

Never concludes WHY (no "gave up" state, no inferred intent), never acts
punitively on idleness (re-staffing is the supervisor's verb, by
judgment), never reads reply content (rows or nothing), never injects
standing reminders (prods are discrete addressed correspondence — the
comms clock pillar — NOT the banned remind-tier context injection).

## Forensics: demoted to diagnostics, off the critical path

Detection needs no process inspection — the prodded AGENT is the
authority on its own background work (its harness tracks its own tasks)
and reconciles in one cheap turn. The forensic toolbox exists for
supervisors investigating anomalies (e.g. "still working" × 3 with no
rows), where partial evidence is fine because judgment is already in
the loop:
- LINEAGE MARKER: adapters spawn with TIGHTBEAM_LINEAGE=<identity@host>
  in env; inheritance survives orphaning/double-fork; census = processes
  whose env carries the marker (accident-grade: env is process-owned and
  launderable — deliberately, or innocently via env -i / sudo / ssh /
  containers / hermetic build tools; the probe doc lists these so
  absence reads "possibly laundered," never "definitely gone").
  Kernel-grade custody (cgroups) available on Linux only, if ever needed.
- SESSION ATTRIBUTION ladder (shared adapters blur to identity grain):
  single-session identity → deterministic; cwd-vs-workdir match →
  strong; process-start-time × ledger turn windows → bounded ambiguity.
  Structural fix if ever load-bearing: adapter-per-session as an
  archetype property.
- PROBE, triggered not resident: a `tightbeam probe` CLI subcommand
  (ships with the binary at assimilation — no daemon, no launchd),
  invoked over ssh, returns machine facts as JSON.
- EPHEMERAL WATCHER: when a probe finds live marked work, the gateway
  may spawn (over ssh, on demand) a self-terminating waiter — "wait on
  these PIDs, POST one event on exit, die" — making background-work
  completion event-driven with zero resident software.

## Prerequisites to make this real (build inventory)

Already exists: wakes + scheduling, process: origins + stamps,
spawned_by lineage, personal-Main derivation + permanence (no-void),
turn-terminal processing in the lane/gateway, lifecycle/event log,
per-session workdirs, `[turn failed]`-class marker machinery.

To build, in order:
1. ATTEST primitive (small substrate addition, needs its own mini-spec):
   a generic structured signed act — `attest {subject, kind, verdict}`
   → a row; content-neutral, judgment-free. Enables: assignments
   (kind=assignment open/close), completion/surrender filings, progress
   facts, and later the check tier's review verdicts. Without it there
   is no "assignment open" fact for the predicate.
2. REACTION EXECUTOR (first substrate acts-on-own-facts machinery):
   at turn-terminal, evaluate the stall predicate; on true, perform the
   prod wake as an ordinary audited verb call. Cascade-bounded by the
   counter; all policy knobs (N, ladder shape) operator data.
3. PROD COUNTER + LADDER: per-assignment counter columns/rows;
   escalation walk over spawned_by with the Main terminus; `stalled`
   stamp.
4. GUIDANCE LINE: one sentence in orientation/comms — never end a turn
   with outstanding work and nothing on the clock — plus the dispatching
   skill teaching assignment/attest hygiene.
5. LATER (separate specs): check-tier completion gating (report-done
   refused without required fact rows), probe subcommand in the Rust
   CLI, ephemeral watcher, statute-expressed supervision policy.
