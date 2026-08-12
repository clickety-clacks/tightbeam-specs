# Rumination redirect-rail — v1 (design)

Status: RATIFIED (Flynn 2026-07-23). Rumination-before-ORCHESTRATION is a substrate
rail that REDIRECTS into a think-turn rather than denying; rumination-before-handoff
stays guidance (wisdom 3). Trigger ruling: RAIL THE ENTRANCE, TEACH THE RE-ENTRY —
the rail fires ONCE per work-item, on the FIRST dispatch; whether any later change
warrants re-rumination is agent judgment taught in the orchestrator kernel, never a
gate (spirit-change is inference; the substrate cannot classify it). UNBUILT.

## The behavior

When an agent tries to fan work out (a `dispatch` — or `assign`+wake used as a
fan-out) for a work-item it has not yet ruminated on, the substrate does NOT let the
fan-out proceed and does NOT hard-deny it. Instead it DETOURS the agent into a
rumination turn on that work-item, then the fan-out proceeds. The user asked to move,
so we don't block them — we route them through the think-step inline.

Determinism brackets inference: the substrate deterministically forces the detour
(row-visible check + a scheduled digest wake); the agent does the actual thinking. The
rail guarantees a rumination turn EXISTS before fan-out — not that it was good (that's
the agent's job and unenforceable; same shape as "a verdict row must exist before
completion", wisdom-3-safe).

## Where it lives

DISPATCH-VERB HANDLER logic (`Assignments.dispatch_result/2`), NOT a `rules.toml`
statute — a pattern-match rail can only warn/deny, it cannot schedule a wake and
resume a deferred action. This is substrate code in the verb.

## The rumination marker (what "already ruminated" means)

A rumination is row-visible via the `digest:` wake convention. v1 marker: a wake of
kind `digest` carrying the `workItemId`, owned by the caller. So the check is a plain
query: "does a digest wake exist for this workItemId, filed by this caller, since the
work-item was created?" (Once per work-item's life — ruled.) No new inference, no new
fuzzy detection.

RECORDING: when the detour fires, the substrate schedules that exact digest wake
(carrying workItemId + the dispatch intent), so the marker is created by the mechanism
itself — the agent doesn't have to remember to file one. An agent may also ruminate
proactively (its own `digest:` wake tagged with the workItemId), which pre-satisfies
the check and no detour fires.

## The mechanic (recommended: refuse-and-reroute, v1)

On a `dispatch` for `workItemId` W by caller C:
1. If a rumination marker for (W, C) exists → proceed normally (open assignment + wake
   holder). Unchanged path.
2. If NOT → do NOT open the assignment. Instead:
   a. Schedule a `digest:` wake to C carrying W and the original dispatch intent
      (subject/brief/target preserved verbatim), prompt shaped "Ruminate on <W> before
      you dispatch: <intent>. When you're done thinking, re-issue the dispatch."
   b. Return a NON-error response to the dispatch call: `{rumination_required: true,
      workItemId: W, message: "sent you to ruminate first; re-dispatch when done"}` —
      NOT a `code:` denial (this is a reroute, not a refusal).
   c. The agent's next turn is the rumination. At its end it re-issues the dispatch;
      now the marker exists → step 1 proceeds.

This keeps ALL state in rows (the scheduled wake carries the intent), needs no
held/replayed-call machinery, and is the smallest thing that delivers "think first,
then fan out, without a wall."

ALTERNATIVE (enhancement, not v1): substrate HOLDS the dispatch and auto-fires it when
the rumination turn completes (true defer-resume, no re-issue by the agent). More
machinery (persisted pending-dispatch + a completion hook); defer until the simple
version proves insufficient.

## Scope

- Trigger: `dispatch` only (ruled — plain `assign` is bookkeeping, not fan-out).
- Once per work-item per caller, for the work-item's whole life (ruled).
- All fan-out callers — the rule is about the ACT of orchestrating, not the archetype
  (ruled).

## Ruled (Flynn 2026-07-23)

1. RESET: once per work-item for its whole life. The first fan-out is where whole-spec
   spirit gets loaded; one think-turn at the entrance, never again. No per-wave reset.
2. TRIGGER VERB: `dispatch` only. Plain `assign` (card without wake) is bookkeeping,
   not a fan-out moment.
3. SCOPE: all fan-out callers — the rule is about the ACT of orchestrating, not the
   archetype.
4. MARKER: the digest-wake row suffices; no separate rumination verb/row in v1.
5. RE-RUMINATION on later changes: GUIDANCE, not rail. Kernel teaching: a bug fix or
   local modification rarely re-touches the spirit; a feature addition/removal, or a
   change to what the thing IS, does — re-ruminate then. The substrate never attempts
   to classify change kinds (that classification is inference; enforcing it would be
   the wisdom-3 trap). ESCALATION PATH held in reserve, only if the entrance rail
   proves too coarse in practice: agent-DECLARED work-item kind as a row field
   (declaration-as-capability — attributable assertion, gamed at the accountability
   tier, not detected), gate on the declaration. Not built until a real gap shows.

## Depends on

- The `digest:` wake convention carrying a `workItemId` (the wake-prompt fact filed in
  the cultivation lanes). If digest wakes cannot yet be tagged with a workItemId, that
  tagging is the one prerequisite to build first.
