# Supervision v1 — event-driven stall detection, prods, and escalation (design spec)

Status: DESIGN — ratified by Flynn 2026-07-19/20 (conversation: "what
prevents an agent from just giving up"). Implementation spec follows once
the statute engine lands (this builds on the same chokepoint machinery
and introduces the attest primitive). Origin: the week's delegation
retrospective — hand-run Sol lanes stalled silently (one 88-minute
zero-file stall caught only by a manually-armed check), and the question
"would tightbeam have improved this?" produced this design.

## Governing purpose, amended 8 September 2026

The [core operating principle](tightbeam.md#operating-principle-trust-record-and-agent-judgment) governs supervision.
The prodder is a reliability backstop for agents who may miss an obligation or
lose a continuation. It helps restore attention. It does not test obedience,
classify intent or choose the next workflow action.

An open obligation with no observed execution or valid continuation is a reason
to bring the recorded facts to an agent. It is not proof that the agent gave up,
that the work is poor, or that a particular next action is required. The holder
judges how to proceed; supervising agents remain accountable for the broader
outcome and for recovery when the holder cannot act.

## Detection and reminder policy

Detection uses durable execution, obligation, continuation and failure records.
Existing wake coverage must be evaluated at the scope defined by its governing
spec, including the approved Wake Rails obligation-specific coverage. Detection
and notification frequency are separate responsibilities. An uncovered terminal
event can invite reconsideration without requiring a fresh immediate prod.

The prodder states the unmet expectation and available evidence. It may identify
useful supported actions without making them an exhaustive command menu. A
missing record receives a useful explanation and correction path. Ordinary
execution should supply evidence wherever already observable; repeated status
prose is not a substitute for progress and is not the goal of the reminder.

Repeated unchanged reminders become less frequent while the next bounded
reassessment remains covered. Material evidence, an approaching commitment,
failed delivery or an unavailable resolver can renew attention. The mechanical
policy responds to recorded facts and agent-supplied judgments; it does not infer
meaning from prose. The agent evaluates consequences that require judgment.
Valid waiting must not provoke invented activity or duplicate wakes.

If the expectation remains unattended under the applicable bounded policy,
bring the facts to a capable supervising agent through the existing lineage.
This is assistance at a broader scope, not punishment. Supervision records
what prompted the notice, delivery and response. A delivered notice does not
fulfill the obligation or prove that supervision succeeded.

This policy supersedes the former immediate prod-to-turn-to-prod requirement and
its punitive countdown wording. It does not select a universal numeric interval
or claim an installed implementation. Existing durable claiming, deduplication,
coverage and lineage mechanisms remain engineering foundations. Reminder timing
and the acceptance checks below must conform before an implementation can claim
this policy. A fast scan interval is not a mandate to interrupt agents at that rate.

## Reminder content

For an uncovered discrete obligation, the notice conveys these facts:

> Assignment <id>, "<subject>", remains open. The record shows no current
> execution or covering continuation for it. Please reconsider the next useful
> action within your authority. If work is waiting, preserve its resolving
> condition and continuation; if the record is incomplete, correct it through
> the supported path. You remain responsible for the outcome.

Diagnostic counts may remain in the record. They are not an obedience score and
must not become a threat in the agent's prompt. Exact evidence descriptions must
match the observation and the applicable coverage rules.

## Acceptance of the reliability policy

- A missed continuation produces a useful reminder and the agent chooses the
  next action. The system does not automatically restaff, close or resume work.
- An unchanged justified wait retains its coverage. Repeated notices decrease
  without losing bounded reassessment or a route to a capable supervisor.
- New recorded evidence or consequences renew attention to the affected
  obligation. Activity elsewhere does not hide its unmet expectation.
- Failed reminder delivery remains visible and can reach a responsible agent.
  Neither a fired wake nor a recorded response counts as fulfillment.
- Missing or malformed evidence receives a supported correction. Required
  verification and explicit authority boundaries remain intact.

## What the substrate never does

The substrate never concludes why work is idle, judges the work's quality,
punishes missing filings or silently chooses a workflow response. It delivers
discrete addressed reminders and preserves truthful records. Agents decide
whether to continue, revise, wait, arrange recovery or seek a decision.

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
   evaluate the recorded condition and amended reminder eligibility;
   when eligible, deliver an ordinary audited wake. Preserve bounded
   reassessment and the lineage route. Policy determines notice frequency;
   a detection event alone does not mandate an interruption.
3. PROD COUNTER + LADDER: per-assignment counter columns/rows;
   escalation walk over spawned_by with the Main terminus; `stalled`
   stamp.
4. GUIDANCE LINE: own the outcome and keep the next action or resolving
   dependency recoverable, with a supported continuation when work remains.
   The dispatching skill teaches the means without prescribing the approach.
5. LATER (separate specs): check-tier completion gating (report-done
   refused without required fact rows), probe subcommand in the Rust
   CLI, ephemeral watcher, statute-expressed supervision policy.
