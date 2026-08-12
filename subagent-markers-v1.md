# Subagent markers — parent-attributed observability for harness-internal fan-out — v1

Status: READY (gate-cleared 2026-07-25, Sol-high round 7: zero blocking; rounds 1-6 findings
folded — termination-carrier prerequisite, canonical refs, reserved-fact boundary, stop-wins
registration race). Flynn-directed. Small, additive; builds only on existing mechanisms
(markers, wake-on-fact, adapter event streams). Implementation may proceed; the
served-identity lane it was sequenced behind is merged (main `9a84163`).

## Ruling this implements (Flynn, 2026-07-24)

Harness-internal subagents are the parent agent's business — they fan out inside one turn,
evaporate with it, and have no residency (bible §Where it sits; decisions §Landscape
position). That fixes the ACCOUNTABILITY boundary, not the VISIBILITY boundary: tracking
subagents through observable seams (ACP events, process shims) does not violate the
philosophy — it augments it.

**The guard, stated as the invariant:** the substrate may SEE subagents; it may never EXPECT
anything of them. Markers, usage attribution, and parent-stall context: yes. Per-child
assignment rows, attests, gates, prods, or any rule predicating on a subagent behaving: no —
the moment a rule expects something of a child, the child has been promoted to an accounting
unit and this spec has been violated.

## Mechanism

1. **The ACP envelopes (pinned — the wire, not the hook layer).** On **Codex**, subagent
   activity is the `subAgentActivity` thread item, delivered by `codex-acp@1.1.4` to Tight
   Beam as a `tool_call` (start) then `tool_call_update` (terminal), correlated by the shared
   `toolCallId` (= item id), with the child's `agentThreadId` carried separately. On
   **Claude**, `claude-agent-acp@0.59.0` already emits distinguishable `Agent`/`Task` starts
   as `tool_call` with `_meta.claudeCode.toolName` and the terminal `tool_call_update` on the
   same `toolCallId`. The impl pins BOTH accepted envelope shapes against the vendored
   adapter versions with captured fixtures, including a fixture proving the terminal envelope
   denotes CHILD TERMINATION (not completion of a spawn operation).
   **Termination is NEVER inferred from the tool_call lifecycle — at both pinned adapters it
   does not mean child termination** (codex: the `started` activity item completes when the
   SPAWN completes, while the child runs on; claude: an async Agent/Task terminal
   `tool_call_update` can arrive while the child remains in `liveBackgroundTasks`, and true
   settlement — `task_updated`/`task_notification` — emits no correlated ACP update).
   **PREREQUISITE — the termination-carrier adapter patch**, extending the vendored-patch
   mechanism the codebase already maintains (`Tightbeam.CodexAcpPatch` precedent, which
   already surfaces `account/updated`): each adapter is patched to emit one explicit,
   correlated child-termination session update — codex keyed by `agentThreadId` (child agent
   threads are threads; the app-server observes their lifecycle), claude emitted at the
   internal settlement point that currently only clears `liveBackgroundTasks` bookkeeping
   (the correlating id is present there). Classification then is: `started` → `subagent_start`;
   the PATCHED termination update → `subagent_stop`; `interrupted` → `subagent_stop`
   (explicit); everything else → no marker. `session/load` replay of a completed `started`
   item reconstructs the START marker only — never a stop. If, at implementation, either
   patch point proves unable to observe real child settlement, that harness's stop/wake
   support is declared unavailable in `harness-support.md` with the captured semantic fixture
   (pair-exists-but-no-terminal-carrier is the required negative form) — never synthesized.
   Fixtures cover live started/interacted/interrupted, the patched termination update, and
   the load-replay shape.
2. **Identity and attribution (defined, not implied).** ACP guarantees `toolCallId`
   uniqueness only WITHIN a session, so nothing global may key on it alone. The impl defines
   and persists a canonical **`source_session_ref`** — `{harness, machine, harness_session_id}`
   with an adapter/source namespace and reverse-uniqueness (extending `harness_pointers`,
   which today carries neither) — and derives:
   `source_event_ref` = `{source_session_ref, toolCallId}` (the dedup key);
   `subagent_ref` = `{source_session_ref, agentThreadId}` for codex,
   `{source_session_ref, toolCallId}` for claude (globally unique in both cases).
   **Parent binding:** principal is ALWAYS the Tight Beam parent session resolved through the
   persisted mapping, never the raw harness session id; late/replayed events attribute
   through the same persisted mapping.
3. **Canonical marker representation (NEW — no existing schema fits).** Neither transcript
   markers (text+sender), lifecycle rows (no principal/payload), event-log rows
   (verb|denied only), nor wake condition-facts ({kind, scope, origin}) can carry this. The
   impl adds a durable marker append API with:
   `{kind: subagent_start | subagent_stop, principal (parent session), subagent_ref,
   source_event_ref, harness, at}` — cause and principal per wisdom 5 — idempotent on
   `{kind, source_event_ref}` for protocol redelivery, AND **semantically deduplicated for
   STOP: at most one `subagent_stop` per canonical `subagent_ref`**, whichever terminal
   carrier arrives first wins (native `interrupted` vs the patched settlement update — a
   dual-carrier fixture proves the second is a no-op), and the
   `subagent_stop` write atomically files the matching wake condition-fact with a
   deterministic scope encoding: `conditionKind = "subagent_stop"`,
   `conditionScope = subagent_ref` (the globally-unique form above).
   **The `subagent_*` fact prefix is RESERVED at the filing boundary**
   (`ConditionFacts.file_in_txn/2`, origin `process:tightbeam` only — alongside the existing
   `quota-recovered`/`escalation-ruled` reservations): the public `condition` verb cannot
   file it, so no caller can forge a stop and fire a parent's wake through the condition
   path.
4. **Waiting composes with the EXISTING wake primitive — no new wake machinery, and the
   parent CAN name the scope.** The parent never sees the substrate-internal composite ref;
   what it does see is its OWN tool call id for the spawn (present in its context on both
   harnesses). The wake verb therefore accepts the parent-visible form — the substrate
   resolves `{caller session, tool_call_id}` through the persisted mapping to the canonical
   `subagent_ref` at registration time (parent-authorized by construction: a session can only
   name its own tool calls; resolution failure is a legible registration error, not a silent
   never-fires). A parent that ends its turn while an internal subagent runs files ONE wake:
   condition `{kind: "subagent_stop", scope: <resolved subagent_ref>}`, and the schema's mandatory `dueAt` is the
   capture-gap fallback (adapter died before consuming the event → `firedBy=fallback`,
   bounded staleness, never lost intent). The wake predicates on the parent's own telemetry —
   nothing is expected OF the child.
   **Registration is race-free against an already-landed STOP, in ONE transaction.** Wake
   condition matching is forward-only (`Wakes.schedule_in_txn/2` snapshots
   `MAX(condition_facts.id)` at registration and matches only `fact.id > conditionAfterId`),
   so a STOP committed BEFORE registration would be permanently invisible to the condition
   path and the wake would silently degrade to its dueAt fallback. Therefore the wake verb's
   `subagent_stop` registration performs, in the SAME transaction: (1) handle resolution
   `{caller session, tool_call_id}` → canonical `subagent_ref`; (2) existing-STOP inspection —
   query for a `subagent_stop` marker for that `subagent_ref`; (3) if one exists, return
   `subagent_already_stopped` to the caller and insert NO wake (the parent already has its
   answer; an immediate-fire wake would be a second delivery of a known fact); (4) otherwise
   schedule the wake with the snapshot taken inside this transaction. Because the STOP
   marker's write and condition-fact filing are themselves one transaction (Mechanism §3),
   these two transactions serialize: every STOP is either visible to step (2) or matched by
   the forward-only condition path — no interleaving loses the event.
5. **Usage roll-up is OUT of v1.** Neither harness's subagent envelope carries a usage delta
   (claude's adapter strips the Task `<usage>` trailer; `usage_update` is a separate
   parent-level snapshot Tight Beam currently ignores), and no parent-session usage store
   exists. Roll-up returns as its own follow-up with an authoritative carrier,
   delta-vs-total semantics, and a storage destination — not smuggled in here.
6. **Process shims are the same pattern for non-harness workers** and are already available
   ad hoc (wrap-at-launch: worker exit → attest/fact). This spec adds no shim machinery; it
   only notes the equivalence so nobody builds a parallel concept.

## Non-goals (enforced by the invariant above)

- No child assignment rows, work items, or attests. The parent attests its own work.
- No deny/allow of harness fan-out (rejected 2026-07-24 — parent-owned machinery).
- No supervision predicates over subagent facts except as CONTEXT on the parent's own stall
  evaluation.
- No new wake machinery — `dueAt NOT NULL` + condition fields already express
  "wake on stop, with timeout."

## Required proofs (fail-on-revert)

1. **Codex leg — three-way, versioned (same structure as the Claude leg below).**
   (a) positive: a codex session that spawns a subagent yields exactly one `subagent_start`
   and exactly one `subagent_stop` (semantic dedup per Mechanism §3), principal = the Tight
   Beam parent session, correlated by `subagent_ref`, with the patched termination update
   fixtured as terminal-means-child-stop and a replayed completed `started` item yielding a
   START marker only; or (b) a captured SEMANTIC fixture demonstrates no observable
   settlement carrier at the pinned patched version → `harness-support.md` records
   `parity=false` citing it; or (c) a captured fixture demonstrates the activity envelope
   itself is absent (regression), likewise `parity=false`. Documentation alone cannot select
   a branch.
2. A wake registered `{kind: "subagent_stop", scope: subagent_ref}` fires on the condition
   path when the marker lands, and on the `fallback` path (dueAt) when marker consumption is
   suppressed — delivery names which (`firedBy`), END-TO-END from a real parent: the parent
   registers via its own `{session, tool_call_id}` handle and the substrate resolves the
   canonical scope (no test-injected refs). **Stop-wins fixture (registration race,
   Mechanism §4):** a STOP that commits BEFORE the parent registers yields
   `subagent_already_stopped` from the registration call, NO wake row inserted, and no
   fallback fire at dueAt — proven with the STOP landed first and the registration second in
   real transaction order, not by injecting state. Two sessions with colliding raw
   `toolCallId`s neither suppress each other's markers nor fire each other's wakes (the
   globally-unique refs above are asserted, not assumed). An attempt to file a `subagent_*`
   condition-fact through the public `condition` verb is REJECTED while the atomic
   substrate-side write succeeds. A `session/load` replay of a completed `started` activity reconstructs the START marker
   ONLY — the proof asserts no STOP marker, no condition-fact, and no wake fire is
   synthesized from replay; condition-path firing is proven from the live (or explicitly
   specified replayable) patched termination carrier alone.
3. **The guard as a structural test.** PREREQUISITE MECHANISM (named, does not exist yet):
   a reserved-obligation-facts boundary in the shared statute/prod/sweep registration path —
   the `subagent_*` fact prefix is registered as observability-only, and a statute, gate,
   prod, or sweep predicate referencing it is refused at load BY THAT MECHANISM (today's
   loaders reject it only as "unknown fact", which stops protecting the invariant the moment
   the facts are exposed for permitted parent-stall context). The test exercises the shared
   registration boundary, not unknown-fact fallout.
4. **Claude leg — three-way, versioned; documentation alone cannot select a branch.**
   (a) the patched settlement update is proven with a captured fixture and the marker tests
   pass; or (b) a captured SEMANTIC fixture demonstrates pair-exists-but-no-terminal-carrier
   at the pinned patched version and the harness-support row records `parity=false` citing
   it; or (c) a captured fixture demonstrates the pair itself is absent (regression),
   likewise `parity=false`. The positive branch requires the settlement carrier, not the
   tool_call pair alone.

## Component touches

`acp/adapter.ex` (consume envelopes → markers — COLLIDES with the served-identity lane;
sequence after its merge); the NEW canonical marker append API + schema (no existing row
family fits — see Mechanism §3) with its atomic condition-fact write; the harness-session →
parent-session mapping surface (adapter coordinator); the reserved-obligation-facts loader
boundary (prerequisite mechanism, proof 3); the termination-carrier adapter patches for BOTH
vendored adapters (prerequisite, Mechanism §1 — extends the existing `Tightbeam.CodexAcpPatch`
mechanism); the wake-verb scope resolution `{caller session, tool_call_id}` → `subagent_ref`; `harness-support.md` row (fan-out =
normal below-substrate capability, observable via markers, policy see-never-expect); one
`feature_smoke.exs` probe if a user-callable surface is added (none expected — producer-side
only). Usage roll-up: deliberately absent (v1 non-goal with named follow-up).
