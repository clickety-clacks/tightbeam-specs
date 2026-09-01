# Tightbeam — Decision Record & Discussion Log (NON-NORMATIVE)

This is the historical ledger: dated decisions, attributions, pinned
questions, superseded designs, and design discussions (including the
A2A / production-system comparison). Nothing here is normative. The
spec is `tightbeam.md`; where this log and the spec disagree, the spec
wins. Kept for provenance and for understanding WHY the spec says what
it says, in its original conversational context.

# Tightbeam

Unified harness gateway: a patchbay between Clawline and coding-agent harnesses.
Named for The Expanse's point-to-point laser comms — no broadcast, no bloat,
nothing in the middle that thinks.

## The Spirit

Tightbeam is a patchbay for a dark factory: the smallest possible
deterministic substrate through which one person and their agents talk, hire,
and coordinate. The intelligence lives entirely in the harnesses; the
substrate routes, records, and enforces — it is forbidden to think, and every
clever thing it might do is a bug that belongs in an agent instead. The
harness transcript is the only truth about a conversation; Tightbeam keeps a
ledger, not a shadow, and when something fails it fails as a visible row with
a reason, never as a mystery. Everything anyone does — human or agent — is
one of a few verbs through one chokepoint, so the whole org is auditable,
governable by deterministic law, and small enough for an agent to hold in its
head and, if need be, rewrite. It manages nothing and observes everything.
And it will never grow to fit your use case: identity and judgment are data,
enforcement is law, and every long-tail want is a skill, a fork you never PR
back, or your own substrate built from this spec — because this document, not
the code, is the product. If a change makes the wiring smarter, the core
bigger, or a failure quieter, it isn't Tightbeam.

**Status:** Design discussion — not yet approved for implementation
**Date:** 2026-07-15 (named 2026-07-16)

## Thesis

Tightbeam is a dumb substrate for smart agents: it routes, records, and
enforces — it never thinks. Org structure is emergent — **runtime behaviors,
not schema. The org chart is a behavior, not a schema.** (Contrast: Paperclip
froze human org charts into substrate tables.)

The value stack (Flynn, 2026-07-16), ascending:

1. **Valuable — the harness patchbay.** One UI and one wire over Claude Code,
   Codex, and whatever comes next. We never write our own agent loop — model
   providers own the loop now, and Tightbeam inherits every harness
   improvement for free. Engines are swappable under a stable identity
   (evals/A-B across harnesses fall out).
2. **Valuable — comms between groups of agents.** Rooms + formal wakes for
   orchestrator-to-orchestrator coordination, delivered without inventing an
   agent runtime, and natively observable from a phone (rooms are Clawline
   streams).
3. **Valuable — formalized agent-spawns-agent.** People already have agents
   launching agents everywhere, ad hoc and unaudited. `spawn` with origin
   tagging, provenance chains, and headcount caps gives that existing practice
   structure: parity with the user, visible in the UI, bounded by constitution.
4. **INVALUABLE — the agents.md replacement.** Identity compiled from
   archetype manifests instead of a hand-tended monolith, plus two-tier law:
   prose (skills/guidance) for judgment, rails for everything enforceable.
   Prose is not enforcement — the ⛔/ALL-CAPS subset of today's instruction
   files migrates to server-enforced law that works even when the model skims,
   and AGENTS.md shrinks to taste and judgment. This is the headline
   contribution; the rest of the system is the substrate it needs to exist.

## Tenets — the WHY, and the "Is This Tightbeam?" test (2026-07-17, NORMATIVE)

This section exists so that ANY agent can preserve the spirit without having
read the history. Each tenet carries its scar — the failure it exists to
prevent. If a proposal fails the test at the end, the answer is not "add it
carefully"; it is a skill, a fork, or someone else's product.

**T1 — The substrate never thinks.** Routes, records, enforces (deterministic
rules over structured facts) — never interprets content. *Why:* openclaw
entangled routing with agent logic and every feature could break every other;
GOFAI put intelligence in the wiring because components were dumb — our
components are smart, so the wiring must be dumb. *Test:* does this need the
gateway to understand what a message MEANS? Then it belongs in an agent.

**T2 — The harness owns the truth.** The projection DB is a one-way cache;
delivery state is a dumb, durable, queryable LEDGER with terminal states and
NO cleverness (no auto-retry, no re-routing, no reconciliation backwards).
*Why:* openclaw kept shadow state that silently disagreed with harness
reality; prompts died invisibly inside clever recovery. *Test:* does this
duplicate conversation state, or try to be smart about recovery? A lost
prompt must be a visible row, never a mystery.

**T3 — One chokepoint; closed sets.** Every mutation is a verb through one
dispatch path; the verbs (11), the turn states (6), the delivery mechanisms
(4) are CLOSED — growth requires spec amendment, not a convenient if-branch.
*Why:* determinism, auditability, and the rails hook all live at the
chokepoint; every bypass is a hole in future law. *Test:* does this mutate
state outside dispatch, or quietly grow a closed set?

**T4 — Identity is data; law is layered.** Who an agent is = generated files
(archetypes/projection); what binds = constitution (Flynn-only) > rails
(proposable, deterministic) > skills/guidance (prose). Prose is NOT
enforcement. *Why:* reading the rulebook doesn't make inference follow it;
the ⛔-markers in instruction files are evidence. *Test:* is this rule about
structured facts (railable) or content/judgment (guidance)? Is someone
putting enforcement hopes in prose?

**T5 — Observe, don't manage.** No backpressure, no queue management, no
self-healing cleverness: bounded counting rules + total visibility
(queueDepth, event log, lifecycle events, health probes, loop watchdog).
*Why:* openclaw's management machinery WAS the failure surface; harnesses own
their own pacing. *Test:* does this MANAGE flow, or make flow VISIBLE?

**T6 — Git-like: fast and minimal (Flynn, 2026-07-17).** Small dependency
budget, close to the wire, comprehensible in one sitting (~3–5k lines/
runtime), boring code an agent can hold in context and re-implement. *Why:*
comprehensibility IS debuggability for agents, and every line is a permanent
ops+token tax; a substrate you can't read end-to-end is a substrate you fix
by folklore. *Test:* does this make the core harder to hold in one head?

**T7 — THE FORK DOCTRINE (Flynn, 2026-07-17 — governance).** Tightbeam does
NOT absorb long-tail features. When a user wants their own case:
  1. First resort: it's probably agent-side — guidance, skills, archetypes.
  2. Else: **fork Tightbeam and never PR it back.** Divergence is the
     intended distribution model, not a failure of community.
  3. Best: use Tightbeam as a REFERENCE IMPLEMENTATION for your own
     substrate — the spec and wire contract are the product as much as the
     code.
Upstream accepts ONLY: bug fixes, wire-contract parity fixes, hardening of
existing tenets, and SPEC ERRATA (a wrong contract poisons every fork and
reimplementation downstream — the spec is the one artifact whose corrections
must flow). Never capabilities. Clarification: **forks pull, they don't
push** — "never PR back" is a one-way valve on contributions, not severance;
downstreams should keep tracking upstream for fixes. *Why:* openclaw died of
accepted features — each one a permanent tax on every invariant above; the
way to say yes to everyone is forks, not merges. Historical validation: the
suckless model and SQLite's open-source/closed-contribution stance — viable
for decades, and newly CHEAP now that agents make fork maintenance and
spec-based reimplementation commodities (see: Bun's fleet port). *The spec —
not the maintainer's mood — is the arbiter.*

**T8 — Coordination is fact-shaped, not call-shaped (Flynn, 2026-07-17).**
Between agents, Tightbeam is a production system in the Newell/blackboard
lineage: durable facts in working memory (messages, turns ledger, wake
registrations) + deterministic condition→action rules (wake triggers; rails
ARE productions) + agents as the engine that fires when conditions match.
There are no promises, no awaited calls, no continuations held in processes —
"ask for a wake-up call when the artifact is finished," never "call and
await." *Why:* a held continuation is a prompt waiting to be lost when its
holder dies (openclaw's dropped prompts were dropped continuations); factory
work completes on day-scale, not stack-frame-scale; facts decouple caller
from callee so the org can be reorganized without editing callers; and the
economics favor rows over held turns — NOT because waiting burns tokens (a
deterministic in-tool wait burns none — Flynn's correction, 2026-07-17), but
because (a) resuming a long-held turn cold-reprocesses its whole context
(cache TTLs expire; a fresh compact wake is cheaper than a fat resume), (b)
the continuation tower (harness+adapter+lane) must survive the whole wait and
a crash correctly yields failed_unknown-never-resumed, (c) an in-turn wait
blockades the session's lane and cannot outlive transport timeouts anyway,
and (d) a sleep in a shell is invisible pending work while a wake row is
inspectable, cancelable working memory. The boundary, quantified: WITHIN a
turn (seconds-to-minutes, inside transport timeouts) code-shaped waiting is
correct; BEYOND turn scale the continuation must move from process to row. *Test:* does this hold a continuation
in a process across agent boundaries, or make someone await? (Corollary:
call-shaped interop protocols like A2A are wires an agent may speak as a
skill, or optional front-door adapters — never the substrate's internal
coordination model.)

**The test, in order.** For any proposal, ask:
1. Does the gateway have to interpret content? → agent-side (T1).
2. Does it shadow or out-clever harness/delivery truth? → reject (T2).
3. Does it bypass dispatch or grow a closed set? → spec amendment or reject (T3).
4. Is it enforcement-in-prose? → make it a rail or accept it's guidance (T4).
5. Does it manage instead of observe? → reject (T5).
6. Does it grow the core beyond one-sitting comprehension? → reject (T6).
7. Is it a long-tail capability? → skill, fork, or reference-impl user (T7).
Pass all seven and it might be Tightbeam. Fail any and it is not — and
"no, this isn't Tightbeam" is a complete, final answer.

**Honest caveat on #4 (2026-07-16):** Claude Code hooks already provide
deterministic single-agent enforcement (block tool calls via settings.json) —
part of the ⛔ corpus is implementable today with hooks, no Tightbeam needed.
Rails' true delta: cross-harness, org-level/multi-session guards (e.g.
"reviewer ≠ author" spans sessions — hooks can't express it), evidence-gated
processes, and agent-proposable versioned governance. "Hooks generalized to an
org," not "enforcement, invented." Industry value is *valuable-if-proven*
(rails bind only what flows through the verbs — an adoption constraint outside
a walled factory); "invaluable" is the within-factory claim.
**Origin:** Flynn ↔ Claude design session on TARS
**Note on location:** The canonical NFS shared workspace (`~/shared-workspace` → `tars:/Volumes/BlipsAndChitz/shared-workspace`) is currently dead — the BlipsAndChitz volume no longer exists on TARS. This doc lives at `~/src/shared-workspace/shared/specs/` on both TARS and eezo (manually mirrored) until the NFS home is restored or re-homed.

## Goal

A much lighter replacement for the openclaw/hermes role: a thin gateway that presents
a unified chat UI (Clawline) over multiple coding-agent harnesses (Claude Code CLI,
Codex CLI), where:

- **Sessions map 1:1 to native harness sessions.** No parallel session model — the
  harness transcript IS the session. The gateway holds only a projection.
- **Unified UI with per-session pickers** for harness, model, and thinking/reasoning
  level.
- **Isolated agent homes.** Each harness runs with a gateway-managed home
  (`CLAUDE_CONFIG_DIR` / `CODEX_HOME`) so skills, instructions (agents.md), and config
  are separate from the user's normally-installed CLIs.
- **Clawline is preserved as the client.** The gateway speaks the existing clawline
  websocket wire protocol (`~/src/clawline/src/protocol/`) on the front. Clawline
  should not need to know openclaw was swapped out underneath it.

### Motivation (why not keep openclaw)

- Openclaw has become bloated with unneeded features.
- Message queueing fails intermittently due to bugs/edge cases; the code feels like
  spaghetti.
- Significant added latency on prompt submission.
- OAuth tokens are cached in multiple places; sessions get pinned to expired tokens
  even after a fresh token is onboarded, making logout/login nearly impossible.
- Desired property: a system "close to the wire" where an agent (or human) can read
  the code and understand deterministically how a prompt flows through it.

## Non-Goals

- Not a rewrite of Clawline. The front wire protocol is adopted as-is.
- No approval/permission UI. All sessions run YOLO (bypass/full-auto). The
  approval surface (ACP `session/request_permission`, clawline `approval` payloads)
  stays dormant.
- Not feature parity with openclaw. Cron/heartbeat, multi-channel routing,
  sub-agent orchestration etc. are explicitly dropped unless later specced.
- The gateway never stores, caches, or forwards auth tokens. Auth lives only in
  each harness's own store (macOS Keychain for Claude Code; `auth.json` in
  `CODEX_HOME` for Codex).

## Architecture

```
Clawline client(s)
      │  clawline wire protocol (websocket; message-granularity:
      │  auth, message, ack, typing, session_info, streams, read state, replay)
      ▼
┌───────────────────────────────────────────────┐
│                Gateway (thin)                 │
│  • wire server (front)                        │
│  • normalized message store (projection DB)   │
│  • per-session FIFO prompt queue              │
│  • session registry: UI session → harness +   │
│    harness-session-id pointer (append-only)   │
│  • agent-home projection (generates each      │
│    harness home from one canonical source)    │
│  • process supervisor (~1 adapter per harness)│
└───────────────────────────────────────────────┘
      │  ACP (Agent Client Protocol; JSON-RPC over stdio)
      ▼
 claude-code-acp          codex-acp
 (CLAUDE_CONFIG_DIR=      (CODEX_HOME=
  managed home)            managed home)
```

### Why ACP on the back

ACP (agentclientprotocol.com, Zed) already normalizes exactly what this project
would otherwise hand-build per harness:

- `initialize` — capability negotiation
- `session/new` / `session/load` — create/resume; `session/load` replays history
- `session/prompt` — one turn; resolves with `stopReason` (end/cancelled/…)
- `session/update` notifications — `agent_message_chunk`, `agent_thought_chunk`,
  `tool_call` + `tool_call_update`, plan updates, available slash commands
- `session/cancel` — real mid-turn interrupt with defined semantics
- `session/set_mode` + `SessionModeState` — adapters expose permission modes here
  (YOLO = select bypass mode at session creation)
- `session/set_config_option` + `configOptions` — current spec's generalized
  mechanism for model / reasoning-level selection (replaced the older dedicated
  `session/set_model`). Agent-advertised typed options; changes stream back as
  `ConfigOptionUpdate`.

Adapters: `claude-code-acp` (Zed-maintained, wraps the official Claude Agent SDK)
and `codex-acp`. Gemini CLI speaks ACP natively (possible future third harness).

The mapping onto clawline's wire is nearly mechanical:

- ACP `configOptions`/modes → `SessionStatusPayload.capabilities` +
  option catalogs (`setModel`, `setThinking`, `setReasoning`, `cancelCurrentRun`) —
  the clawline protocol was already shaped for a heterogeneous-harness picker
  (`display.harness`, `display.model`, `display.thinkingLevel`, …).
- ACP update chunks accumulate → one clawline `message`; `typing` while a turn runs.
  (Clawline wire is message-granularity — no token deltas to normalize.)
- "Harness picker" is not an ACP concern: harness = which adapter binary the
  gateway spawns with which env. That's the gateway's own thin layer.

### Turn lifecycle / queueing (the only stateful component)

- One long-lived adapter process per (harness, archetype) in use; ACP is
  multi-session per connection, so supervision surface is a handful of processes
  (lazily spawned, idle-reaped), not one per session.
- Per session, the gateway holds exactly: a FIFO of pending prompts + the current
  turn handle. States: `idle → prompting → (done | cancelled)`.
- Prompt submission = one JSON-RPC write to an already-warm process (near-zero
  latency — directly addresses openclaw's submission-latency problem).
- One turn at a time per session, enforced by the FIFO. Deterministic by
  construction; no global routing layer.
- Crash/idle handling: adapter dies → respawn → `session/load` on demand.

### Source of truth

- Harness transcript = truth (owns LLM context, compaction, tool detail).
- Gateway message store = one-way materialized projection for display/replay
  (clawline replays by message id, so this store is required regardless).
- Never reconcile backwards from projection to harness.
- Claude Code resume can fork to a NEW session id; the registry's
  UI-session → harness-session-id mapping is therefore a mutable pointer
  (append-only chain), not a constant.

### Auth model (fixes the openclaw token problem structurally)

- Each managed harness home owns its own credentials. Re-login = re-auth that CLI
  in that home once; every subsequent spawn reads current creds.
- No gateway token cache exists, so "sessions pinned to expired tokens" cannot occur.
- Caveat: a warm adapter holds creds loaded at spawn; re-login may require one
  adapter bounce (sessions rehydrate via `session/load`).

### Agent identity & home projection

The system defines its own agent identity — a canonical AGENTS.md, skill set, and
MCP config, authored and versioned at the product level, separate from the user's
normally-installed Claude/Codex setups. This is a first-class product concept:
from the outside this is ONE agent; the harness/model/thinking picker swaps the
engine underneath the same identity.

Projection into the harnesses is under-the-hood plumbing, a generation step, not
a shared directory:

- Canonical source → projected into each harness's managed home
  (`CLAUDE_CONFIG_DIR` / `CODEX_HOME`): `CLAUDE.md` as a one-line `@AGENTS.md`
  include; `.mcp.json` (Claude) vs `config.toml` `mcp_servers` (Codex); skills
  copied/linked into each home's expected layout (both harnesses now support the
  SKILL.md agent-skills format, so skills may project as symlinks).
- Managed homes are **build outputs**: disposable, regenerated on identity change,
  never hand-edited. Auth material is the one thing in a home the projector must
  never touch.
- Expect some behavioral divergence: the same AGENTS.md runs under different
  harness system prompts and tool vocabularies. Write canonical guidance
  harness-neutral; divergence is inherent to multi-harness, not a projection bug.
- **Archetypes are templates, never contracts (Flynn, 2026-07-16).** At session
  creation the user may override anything in the archetype; unspecified fields
  fall back to the template. Two override classes: *runtime knobs*
  (harness/model/thinking — pure spawn/config parameters, home untouched) and
  *identity-affecting* (skills/guidance — the effective manifest = template +
  overrides, and the generated home is keyed by hash of the effective manifest,
  so unmodified sessions share the archetype's canonical home while customized
  sessions get an on-demand home, idle-reaped like any other).
- **Archetypes (decided 2026-07-16, supersedes single-identity).** Identity is a
  set of named archetypes, each a declarative manifest (no logic — a parts list):
  guidance fragments composed in order (shared `base.md` + role files), skills
  picked by name from one shared library, MCP config, optional defaults
  (harness/model/thinking), default room subscriptions. Sessions are created AS an
  archetype; the former single identity is just the `default` archetype.
  Projection stays a dumb deterministic assembly step.
- **Homes are keyed (archetype × harness)** — `homes/<archetype>/<harness>/`.
  Consequence: adapter supervision is one process per (harness, archetype) in
  use, lazily spawned and idle-reaped — a handful, not per-session.
- **Evals / A/B testing are a designed-for affordance (Flynn, 2026-07-16).**
  Because harness/model are overridable template fields, "same identity,
  different engine" is a first-class comparison: run two sessions from one
  archetype on Claude vs Codex (or model A vs B) against the same task and
  compare. Requirements this places on the system (cheap, but must not regress):
  the session registry records full provenance per session — archetype,
  effective-manifest hash, harness, model, thinking, adapter/CLI versions — and
  the projection DB keeps both transcripts comparable. A structured eval harness
  (scoring, judges) is out of scope; rooms + an orchestrator session can serve
  as a manual judge in the meantime.
- **Auth is factored OUT of homes** into one per-harness location
  (`auth/<harness>/`), symlinked into every archetype home. CORRECTED
  2026-07-16 by spike: Claude auth is a PLAIN FILE (.credentials.json), not
  macOS Keychain — so BOTH harnesses are file-based and the symlink design is
  uniform (empirically validated for Codex auth.json; Claude validated via
  copy, symlink to verify). One login per harness ever, regardless of archetype
  count — and homes become fully disposable build outputs.

### On-disk layout

Everything the system owns lives in a single dot directory in `~`, in the style
of `~/.openclaw`:

```
~/.tightbeam/
  config.*                    # gateway config: port, harness binaries + pins
  identity/
    archetypes/<name>.toml    # archetype manifests (declarative parts lists)
    guidance/*.md             # composable guidance fragments (base.md + roles)
    skills/<name>/            # shared skills library (SKILL.md format)
    mcp/*                     # shared MCP config fragments
  auth/<harness>/             # per-harness credentials, symlinked into homes
  homes/<archetype>/<harness>/  # generated CLAUDE_CONFIG_DIR / CODEX_HOME
  state/                      # projection DB: messages, rooms, session registry
  logs/
```

Regeneration rule: homes are fully disposable build outputs — regenerate by
delete + reassemble + relink auth symlinks. Credentials live only under `auth/`
and are never touched by projection.

## Decisions (Flynn, 2026-07-15)

- **v1 wire scope: core chat + attachments.** Pairing/auth, messages, typing,
  session status/pickers, cancel, replay/read-state, plus image/asset attachments
  and the upload API. Defer interactive-html and terminal-wire.
- **Session cwd: default `~`.** These are orchestration-style sessions, not
  repo-bound coding sessions; ACP's `session/new` requires a cwd, so pass `$HOME`.
  Optional per-session override can come later if repo-bound sessions matter.
  (Consequence: no repo-level CLAUDE.md/AGENTS.md pickup — instructions come
  entirely from the managed agent home.)
- **Migration: run alongside openclaw on TARS** (different port; Clawline points
  at it per-connection). Openclaw keeps running until cutover. Development on eezo.
- **v1 harnesses: Claude Code + Codex.** Gemini CLI (native ACP) can slot in later
  since the harness layer is just spawn config.

### Wire realities: pairing/multiuser + session naming (2026-07-16)

**Pairing & users (corrected 2026-07-16 — openclaw IS multi-user in
operation).** The wire's auth surface (pair_request deviceId + claimedName,
token issuance, userId, isAdmin, per-device replay cursors) is Tightbeam's to
implement — it replaces openclaw's pairing/allowlist machinery. v1 scope
matches openclaw's actual semantics: **multi-user operational partitioning,
not security isolation** — sessions carry an owner userId; each user's chat
list/catalog is scoped to their own sessions; isAdmin (Flynn) sees all;
multiple devices per user. No hard privacy guarantees are claimed (same trust
level as openclaw today); hard isolation, if ever wanted, is
constitutional-tier and deferred. Agent-spawned sessions inherit the owner of
their spawn tree's root. (Per-user budgets/caps link to the pinned budget
question.) Device tokens live in `state/` (gateway-owned) — a third credential
store, distinct from `auth/` (harness creds) and from homes; never mingled.
Agent-side CLI trust (`--as`) is unaffected: agents are not wire clients —
device tokens and agent handles are separate identity planes.

**Session naming (chatdb successor).** Openclaw's chat DB (sessionKey →
displayName, updatedAt; TrackableSessionPayload catalog) is replaced by the
session registry: one row owns wire sessionKey, display name, agent handle,
archetype, origin/provenance, and the harness-session-id pointer chain — the
wire's key for Clawline, the handle for agents. Per-device replay cursors
(replayCursorsBySessionKey, lastMessageId) live in the projection DB alongside
room read/tail state.

**Migration decision:** v1 starts with a fresh DB — no import of openclaw chat
history. Alongside-deployment means openclaw keeps its history; Tightbeam
sessions are new.

### Cross-session comms: rooms (proposed 2026-07-16, discussion — not yet approved)

**Motivation.** The end game is a software dark factory: one person, many parallel
projects, multiple orchestrator sessions on different subsystems that need to talk.
Openclaw's `/alert` (point-to-point, single message) is the capability being
replaced and generalized.

**Design: rooms are streams.** A discussion room is a clawline stream whose
participants are agent sessions (and Flynn). Rooms live in the projection DB and
ride the existing stream/replay/read-cursor machinery — which means all agent
chatter is natively observable in the Clawline UI. Point-to-point messaging is a
two-member room; there is exactly one mechanism.

- **Agent-side surface: the `tightbeam` CLI** (no MCP — Flynn, 2026-07-16):
  `tightbeam post`, `read-since`, `list-rooms`, `subscribe`, wake commands.
  Harnesses learn it via skills in the shared library (`scheduling-wakes`,
  `rooms-etiquette`), included per-archetype via manifests.
- **Wakes are coalesced, never interruptive.** A wake means "your cursor is
  behind in room X," delivered as one enqueued prompt turn (via the existing
  per-session FIFO) when the session is idle, with unread posts inlined up to a
  size cap and the cursor advanced. Multiple posts during a busy turn = one wake
  at idle.
- **Mention semantics.** `@handle` wakes the mentioned session; plain posts wake
  only `wake-on-any` subscribers. Subscription modes per session per room:
  `wake-on-any` / `wake-on-mention` / `mute`. Sessions get stable human-readable
  handles in the session registry (e.g. `news-orchestrator`).
- **Anti-storm, split by layer.** Patchbay (deterministic): coalescing,
  no-self-wake, per-room rate caps. Identity/AGENTS.md (judgment): "a wake is not
  an obligation to reply."
- **Invariant check:** rooms are routing + recording + deterministic wake rules.
  The gateway never interprets a post. Passes.
- **Known costs:** every wake becomes a prompt turn in the subscriber's harness
  transcript (chatty rooms inflate subscriber context — mention-mode defaults are
  the lever; digest wakes are a later deterministic upgrade). Ping-pong loops need
  an explicit acceptance test.
- **Note:** wakes make an event-driven prompt source; scheduled wakes
  (heartbeat/cron, still a non-goal) would reuse the same enqueue mechanism if
  ever wanted.

**Open questions (rooms):** wake payload size cap; whether room membership is
declared at session creation or dynamic; whether Flynn-posts in a room use the
same wake path (presumably yes); v1 vs v2 placement — rooms are additive to the
core patchbay and could land after first light.

### Formal wake system (proposed 2026-07-16)

Wake is NOT part of ACP (ACP is strictly client-driven: gateway calls
`session/prompt`, nothing agent-initiated exists). Wake is Tightbeam's own
formal subsystem:

- **Triggers are deterministic predicates** evaluated by the patchbay — no
  interpretation, ever: `mention` (implicit, always on), `room_activity(room,
  debounce)`, `message_from(session)`, `timer(at | after)`, possibly
  `pattern(room, regex)`. Semantic conditions ("when the build seems done") are
  intentionally inexpressible; agents encode them as concrete triggers instead
  (e.g. `message_from(builder:news) in #news-ci`).
- **Registration:** agents call the `tightbeam` CLI — `wake-when <trigger>` /
  `list-wakes` / `cancel-wake`; archetype manifests declare default
  subscriptions (implicit wakes). Every wake is a durable, inspectable row.
  Usage is taught by the `scheduling-wakes` skill, not baked into prompts.
- **Debounce (Flynn, 2026-07-16):** `@mention` wakes promptly; non-mentioned
  room participants wake via a debounce window (e.g. 60–300s of quiet) so a
  burst of posts becomes one wake. Debounce is a per-trigger parameter.
- **Delivery:** unchanged from rooms design — coalesced, idle-time only, one
  enqueued prompt turn stating the trigger reason(s) with unreads inlined.
- **Durability requirement:** wakes and timers MUST survive gateway restarts
  (the factory runs unattended overnight).
- **Layering (Flynn, 2026-07-16): Tightbeam owns the wake API and ALL its
  semantics** — triggers, debounce, coalescing, the durable subscription
  registry. Restate is orthogonal plumbing beneath it: durable execution +
  timers that call back into the wake API when they fire. Restate never talks
  to agents, never defines semantics, never touches ACP. (Its fit remains
  strong — virtual objects for per-session serialized FIFOs, durable timers,
  awakeables — but it is an engine under our API, not a wake system.)
- **Agent facade: the `tightbeam` CLI only** (no MCP — Flynn, 2026-07-16). One
  dumb shim over the wake API's local gateway endpoint, shared by agents,
  scripts, and humans. Harnesses are imbued with usage via skills from the
  shared library; agents never see what's behind the API.
- **Session attribution (v1 trust decision):** adapters multiplex sessions in
  one process, so CLI calls carry no ambient identity. Agents pass their own
  handle explicitly (`--as <handle>`; each session is told its handle in
  context). Gateway validates the handle exists but does not authenticate it —
  single-operator local trust model, acceptable for v1; revisit only if
  Tightbeam ever runs multi-tenant.

### Primitives: nouns & verbs (proposed 2026-07-16)

Tightbeam is the infrastructure the "employees" work in — a dark factory / dark
org. Its API is a small CLOSED set of deterministic primitives; everything else
is skills and guidance composed on top.

**Nouns:** session, archetype, room, message, wake, cursor.

**Verbs** (parity for user and agents, origin-tagged):

| verb    | meaning                                                        |
|---------|----------------------------------------------------------------|
| spawn   | instantiate a session from an archetype template + overrides   |
| post    | append a message to a room (mentions included)                 |
| read    | catch up a cursor (room history since last seen)               |
| wake    | register/cancel a wake trigger (mentions, activity, timers)    |
| cancel  | interrupt a session's running turn                             |
| tune    | change a session's runtime knobs (model/thinking → ACP config) |
| retire  | end a session deliberately (caps require an offboarding verb)  |
| inspect | read the org: sessions, rooms, wakes, provenance, status       |
| propose | stage a diff to the identity repo (skills/guidance/archetypes/rails); adoption = Flynn merge |
| enact   | instantiate a rail (state machine) on a room/artifact/session — proposed |
| advance | attempt a rail transition citing evidence; guards enforced deterministically — proposed |

**Proposed unification (needs Flynn sign-off): prompt = post.** A session's
chat is already a stream on the wire, so its inbox is its home room and
prompting is posting there with an implicit mention-wake. DMs, rooms, and
prompts collapse into one messaging mechanism; no separate prompt verb.

**Closure rules:** a feature expressible as a composition of verbs is a skill
(adversarial review = spawn + post + wake + read). If the missing piece
requires judgment, it's guidance. The verb set grows only for operations that
are both deterministic and inexpressible — rare by design.

### Agency-preserving supervision (adopted 2026-08-11)

**Prompt, don't prescribe.** Tightbeam observes durable facts, enforces hard
law, and delivers prompts to the accountable agent. It does not silently choose
that agent's next workflow action. The agent re-adjudicates from the current
facts and may continue, staff or re-engage another agent, alter its plan within
its authority, park, escalate, or follow a newer instruction from the user or a
peer.

This is a product tenet, not merely wake behavior. Timers detect silent
inactivity; fact changes make an accountable agent eligible to reconsider; both
produce a prompt, never an automatic resumption or a hidden workflow
transition. Rails may deny unsafe actions and require evidence, but must not
turn ordinary judgment about how to proceed into an unobservable substrate
decision. This preserves a live point of control where a user or another agent
can add case-specific instructions before the accountable agent acts.

The compact name is **agency-preserving supervision**. Its normative shorthand
is **prompt, don't prescribe**.

**Dark-org mapping:** archetype = job description; spawn = hire; skills = SOP
binder; guidance = employee handbook; rooms = channels/meetings; wakes =
notifications; provenance chain = reporting lines; spawn caps = headcount
budget; evals = performance review; retire = offboarding; Clawline = the
window onto the factory floor.

### Org learning: codifying emergent structure (proposed 2026-07-16)

If org structures are runtime behaviors (spawn+post+wake topologies described in
prose), the factory needs a loop to notice, codify, and repeat the ones that
work — the in-factory version of Flynn's existing skill-graduation and
overnight-self-calibration processes.

The loop against existing pieces: **behave** (runtime topology) → **notice** (a
retrospective/process-engineer archetype `read`s transcripts and rooms — the
complete org history is already in the message store; a job description, not
machinery) → **codify** (target already exists: the identity layer — repeated
behavior becomes a skill, durable pattern becomes guidance, recurring role
becomes an archetype; natural language IS the encoding, agents are the
interpreter — deliberately no workflow DSL) → **distribute** (homes are pure
functions of manifests; adopted changes propagate by regeneration; every next
spawn embodies them).

**One new primitive: `propose`** — and `identity/` becomes a git repository.
Agents get write access to staging branches only, never main. Codification is a
diff; adoption is a merge; merge authority is Flynn (matching the existing
"Flynn merges to main" discipline). `git log` on identity/ is the history of
how the org learned. Proposals record proposing session + transcript evidence
(provenance for free).

Verb closure test: passes honestly — deterministic (stage a diff), not
composable (nothing else touches the identity layer). The asymmetry is the
design: reading the org is free; writing the org's constitution goes through a
gate.

**Guarded failure mode:** handbook rot (plausible-but-wrong process amendments
accumulating). v1 gate = Flynn merges. Later options: reviewer-archetype
pre-filter; evals A/B of proposed guidance vs incumbent before merge (org
process changes tested like code). Delegating merge authority to agents is
possible but a deliberate, distant decision.

**Superhuman-abstractions note (Flynn, 2026-07-16):** many human-org
abstractions exist to compensate for human limits (scarce review capacity →
approval chains; lossy context transfer → meetings/status; ~7-report attention
→ compressive hierarchies; goal divergence → careers/incentives). Under agent
properties (abundant review, perfect recall, free respawn, no careers) those
dissolve into skills/verbs. What survives is physics and epistemics, not
psychology: budgets (compute scarcity), verification walls (generators can't
judge themselves; reward-hacking is the agent Goodhart), specialization
(context economics, not skill scarcity). Corollary: org structure should be
EMERGENT (runtime behavior + codification loop), never substrate schema — the
core divergence from Paperclip.

### Rails: hard law (proposed 2026-07-16)

Problem (Flynn): reading the rulebook doesn't make inference follow it. Janus
is the counter-model — a state machine where conformance is structural, not
behavioral: the wrong path is unrepresentable, no inference needed once in
place. Rails generalize Janus into an agent-authorable primitive.

**Two-tier law:** skills/guidance = soft law (prose, inference-dependent,
cheap, flexible). Rails = hard law (declarative state machines, structurally
enforced by the gateway). Legislation pipeline: observed pattern → skill →
hardened into a rail only when violations actually cost something. Most rules
stay soft; rails are momentous.

**Form (corrected 2026-07-16 — rails are NOT always state machines):** a rail
is a guarded transition rule over structured facts — `(scope, event, guard,
actions, state-change)` — with three authoring forms that compile to the same
core:
- **invariant**: stateless predicate on a verb call ("only reviewer archetypes
  may post to #verdicts"). state-change = none.
- **reaction**: event → condition → deterministic action ("spend crosses 80% →
  wake Flynn"). Counters/leases/budgets are guards over registry arithmetic.
- **process**: full state machine with evidence-gated transitions (Janus-shaped:
  reviewed → holdout-passed → deployed). The maximal form, not the only form.

**Primitives:**
- **rail** (noun): a declarative rule in one of the three forms above. Lives in
  the identity repo → `propose` covers codification; Flynn merge = enactment
  authority.
- **enact** (verb): instantiate a rail, attached to a room/artifact/session
  (process form; invariants/reactions are typically always-on once merged).
- **advance** (verb): attempt a process transition citing evidence; gateway
  enforces guards deterministically and refuses invalid transitions.

**Mechanics (2026-07-16):** a rail is a TOML file in `identity/rails/`
(proposed/merged/repealed like all law; gateway reloads on merge). The engine
is two hook points in the existing verb pipeline: (1) **pre-dispatch guards** —
every verb call is evaluated against applicable rules, constitution first then
statutes, deny wins; refusals cite the rail by name (agents learn law by
bumping into it); (2) **post-dispatch events** — every successful verb appends
to the event log; reactions and process transitions match on events and fire
actions. **Actions are ordinary verb calls with origin `rail:<name>`** — fully
audit-visible, re-guarded through the same pipeline, cascade-capped by a
constitutional max rail-triggered depth per event. Guard language: total,
non-Turing-complete predicates (comparisons, exists(), count()) over a
read-only fact API — **CEL is the reuse candidate** (built for exactly this).
Process instance state = rows in the projection DB; `enact` inserts, `advance`
is a normal guard-checked verb; `inspect` exposes instances + the event log.

**Enforcement model (2026-07-16, answering "how do verbs tap the rules"):**
rails are file permissions, not handbook rules — agents don't conform to them,
the server applies them. This works because agents can touch Tightbeam nouns
ONLY via verb calls, and every call passes the gateway (no side door: rail
state, membership, sessions change through verbs or not at all). **Callers
supply references, the engine supplies facts:** a call carries identity
(`--as`) + its parameters + evidence refs (message ids); the engine resolves
all facts (archetype, origin, message existence, instance state) from its own
stores — callers point at facts, never assert them. Denials are structured and
cite the rail by name, so wrong paths return errors instead of succeeding
(guidance teaches the happy path; rails make the unhappy path fail closed).
**Boundedness:** three finite fences — rules trigger only on the 11 verbs, read
only the fact API (finite schema over gateway-owned stores), and are written
in a total non-Turing-complete guard language. This is the standard PEP/PDP
authorization pattern (OPA/CEL middleware), not an invention.

**Three planes of law (2026-07-16, supersedes the earlier "writ limit"):**
compiled hooks close the old escape route — an agent has no hands except tool
calls (its "shell" IS the harness Bash tool), and hooks gate the tool surface;
snapshot-at-start + human-gated mid-session changes + home regeneration at
every spawn make them tamper-healing. Against the real threat model
(sloppiness/skimming, not malice) coverage is effectively total. Honest limit:
hooks inspect the call, not its downstream effects (an approved ./build.sh can
contain anything), so load-bearing invariants get defense in depth:
1. **Gateway rails** — org verbs, cross-session facts, evidence gates.
2. **Compiled hooks** — each body's hands (bash/edits), deny + teach at the
   point of action.
3. **External chokepoints** — crown jewels: branch protection, deploy
   credentials minted only by rail actions (`tightbeam inspect` as a script
   gate; one-time capability tokens). The world refuses even if planes 1–2
   are slipped. Deliberate evasion, if ever observed, is an eval finding and
   an archetype problem, not a substrate failure.

**Rails compile to hooks (2026-07-16 — two enforcement planes, one statute
book):** Claude Code hooks already provide full prevent+guide mechanics
(PreToolUse exit-2 / permissionDecision:"deny" blocks the call; stderr/reason
feeds back to the model, which course-corrects; Stop hooks can refuse turn-end
— "always notify" is enforceable today). What hooks lack is a lifecycle:
hand-authored, snapshotted at session start, mid-session changes gated behind
human /hooks review (deliberate anti-self-modification) — no discovery, no
proposal path, no distribution, no org scope. Tightbeam supplies exactly that:
**the identity projector compiles session-local statutes into hooks inside
every generated archetype home.** Propose → Flynn merge → homes regenerate →
the law is installed in every body. Agents thus effectively author hooks, but
only through the gated legislative pipeline (anti-self-modification property
preserved). Org-level statutes (cross-session facts: reviewer ≠ author,
evidence gates) stay in the gateway engine. This also patches the writ limit:
gateway rails govern the org's verbs; compiled hooks govern each body's hands
(shell commands, file edits — the tool surface inside the harness). Codex
equivalent for the hook compile target needs verification in the adapter
spike.

**Compiler architecture (2026-07-16 — demystified):** three parts. (1) Most
rule kinds are INTERPRETED by the gateway (CEL at dispatch + event loop) —
no compilation. (2) Hook-plane statutes: never translate CEL to per-harness
code — one shared guard shim (`tightbeam-guard`) evaluates guards identically
for both harnesses; the "compiler" merely emits routing stanzas into generated
homes ("on PreToolUse~Bash, call shim with rail-id X"). (3) Per-harness
surface = three lookup tables (stanza shape, stdin field map, output field
map) — empirical fixtures already captured in spike findings. Test strategy:
snapshot tests for the emitter, fixture unit tests for the shim, end-to-end
"do the forbidden thing, assert denial" runs seeded from the spike probe
scripts, and a harness×event conformance matrix rerun on version bumps.
Verified-fiddly bits: Codex hook trust in generated homes (managed-hooks
placement — needs a one-hour spike before building) and bash regex authoring
(per-rail judgment, bounded by the three-plane model). Verdict: smaller than
the wire implementation; well-suited to agent build+test.

**Constitution vs statute:** rules protecting the system FROM the org
(no-self-wake, spawn caps, origin tagging) are constitutional — gateway
config, Flynn-only, not reachable by `propose`. Rails are statutes —
proposable, mergeable, repealable. Same guarded-rule machinery executes both
tiers; only the amendment authority differs. (Existing hardcoded guardrails
should be re-expressed as constitutional rules of the same form — one rule
engine, two tiers of authority.)

**Invariant compliance (the Janus move):** guards predicate ONLY on structured
facts — caller origin/archetype, existence of posts/evidence rows by id,
counts, budgets, explicit prior transitions — never on message content or
meaning. Example guard: `submitted → approved` requires advance by a session
with archetype=reviewer, origin ≠ author, citing a verdict post. The gateway
executes machines mechanically; meaning stays in agents.

**Proactive rails:** transitions carry deterministic triggered actions using
existing verbs — entering `needs-review` mechanically spawns+wakes a reviewer
archetype; state timeout fires an escalation wake to Flynn. The machine
supplies the sequence; agents supply the intelligence inside each state.

**Architectural position (2026-07-16): orthogonal module, integral hosting.**
The enforcement point is inseparable from Tightbeam (the chokepoint IS the
dispatch path; hard law can't be bolted on from outside). Everything above the
hook is orthogonal: definitions are identity-repo data, governance is the
propose/merge loop, and the engine lives behind a two-function interface —
`evaluate(call, facts) → allow/deny`, `on_event(event) → actions` — with a
null (allow-all) implementation. Acid test: v1 with zero rails is a complete
product. (Janus implementing this legal model over Tracker independently is
evidence the pattern is substrate-independent.)

**Build-order consequence — the hooks are v1, the engine is not:** two things
are nearly free now and miserable to retrofit: (1) a SINGLE verb dispatch path
that no verb ever bypasses, including internal/rail-triggered calls; (2) an
append-only event log — every successful verb emits an event from day one.
v1 ships those grooves + allow-all; the legal system slots in later without
touching the core.

**Endgame for instruction files (2026-07-16):** rails formalize what today
lives in AGENTS.md as emphatic prose. Litmus: a rule naming structured facts
(who/what state/what evidence/what count) can graduate to a rail; a rule
requiring content/intent understanding stays soft law backed by review.
Flynn's existing global CLAUDE.md is a seed-statute corpus — "never merge to
main" (invariant/chokepoint), "always notify on completion" (reaction),
"protected Tracker states need proof rows" (Janus — the rail prototype),
"never push unbuilt code" (capability token). The ⛔/ALL-CAPS markers in
instruction files are hand-annotated rail candidates: shouting exists because
prose enforcement is unreliable. Target state: AGENTS.md shrinks to taste and
judgment; everything enforceable becomes law that works even when the model
skims. Bootstrapping task: audit Flynn's instruction files as seed statutes.

**Failure modes:** bureaucracy sprawl (org legislates itself into workflow
hell — mitigated by Flynn merge gate + culture: rails are momentous);
evidence gaming (hollow verdicts satisfy the letter of a guard — Goodhart
moves rather than dies; countermeasure is judgment-layer quality: adversarial
review, evals, holdout discipline). Rails make the SEQUENCE ungameable, not
the substance — an honest division of labor.

Verb set grows to eleven (enact, advance). Closure test passes: deterministic,
and multi-step instance state is not composable from post+wake. Largest single
addition to the primitive set; status: proposed, pending Flynn.

### Prior art check (researched 2026-07-16)

Three traditions independently converge on our primitives — validation, plus
two noun-level findings:

- **Classic multi-agent systems (1980s–90s, actively revived for LLM agents in
  2025–26 arXiv work):** blackboard architecture = rooms with wake-on-content
  (agents triggered by board state — Flynn reinvented Hearsay-II from first
  principles); contract net protocol (announce/bid/award task allocation) =
  composable post+wake skill, not a verb; FIPA-ACL/KQML performatives
  (inform/request/propose) = message semantics — FIPA standardized syntax but
  couldn't enforce semantic agreement, which historically killed it. That
  failure VINDICATES our design: semantics live in guidance and natural
  language, never in the wire. The patchbay stays performative-free on purpose.
- **Dark factory literature (Dan Shapiro's five levels; StrongDM "Software
  Factory," Feb 2026; EPAM, env.dev, Infralovers):** focuses on the work
  process, not the comms substrate — specs as input, generator/validator
  separation ("the same agent that wrote the code can't catch its own errors"),
  holdout scenarios the builder never sees, judged by a separate LLM. These map
  to our archetype separation + adversarial-review skill; holdout discipline is
  a guidance/skill-level pattern to adopt, not gateway machinery. StrongDM's
  humans "design specs, curate tests, watch the scores" = our evals affordance.
- **2026 orchestration guides:** task board with atomic claiming as THE core
  coordination primitive; roles with budgets and reporting lines; heartbeats +
  event triggers (our wake system is event-first with `timer` covering the
  heartbeat case, agent-registered).

**Closest systems (researched 2026-07-16):**
- **Paperclip** (OSS, Mar 2026, ~53k stars): "OS for autonomous companies" —
  Node/React/Postgres, primitives = company/mission, goals, org chart,
  reporting lines, budgets, approvals, audit trails. The OPPOSITE abstraction
  bet: org semantics (governance, approvals, goal alignment) live IN the
  substrate. Also brings its own agent execution rather than riding frontier
  coding harnesses.
- **Claude Code agent teams** (Anthropic, Feb 2026): native spawn + teammate
  message passing via file inboxes (`~/.claude/<team>/inboxes/`). Convergent
  with our spawn/post/inbox-room shape — but harness-locked, ephemeral,
  project-scoped; no durable org, no cross-harness, no phone-grade
  observability. Biggest distribution threat AND strongest convergence signal.
- **Ecosystem fragments:** Agentrooms (@mention routing between agents),
  claude-peers-mcp (local agent message bus), file-based message-bus skills
  with heartbeats/locking/voting. Pieces of our design, none the whole.

**Tightbeam's two contrarian bets** (explicit, could be wrong): (1) task is
externalized (Tracker) while every competitor makes task/goal the core noun;
(2) semantics-free substrate while Paperclip et al. bake governance in. Our
differentiators nobody combines: real harness sessions as the unit (ACP),
durable semantics-free comms, cross-harness identity projection, consumer-grade
observability (Clawline).

**Noun findings:**
- **task** — core noun everywhere else, deliberately externalized here: Janus/
  Tracker is the task substrate. Tightbeam is the comms/labor substrate; recorded
  as an explicit boundary decision. (Atomic claiming, if needed, is Tracker's
  concern.) Likewise **artifact** (git/shared workspace) and **org memory**
  (skills library + Flynn's existing skill-graduation process).
- **budget** — genuinely missing candidate. Prior art gives roles budgets; we
  have spawn caps (headcount) but no spend/token budget per session or
  spawn-tree. Open question below.

### Inter-archetype relationships (adversarial review etc.) — proposed 2026-07-16

**Decision: relationships are described, not declared.** No relationship schema
in the gateway (reviewer-of, adversary-of, …) — that would put meaning into the
patchbay. Relationship patterns (adversarial review, judge panels, tournaments)
live as **skills** in the shared library (e.g. `adversarial-review`: post diff
to a review room, wake a reviewer-archetype session, iterate to convergence),
included per-archetype via manifests; finer points go in guidance fragments.

**New primitive required: agent-initiated session creation.**
`tightbeam new-session --archetype <name> [overrides] --as <handle>` — the one
piece of machinery relationships actually need. Creating a session from a
template is deterministic plumbing (invariant passes); with sessions + rooms +
wakes, agents assemble any collaboration topology at runtime without new
gateway concepts.

**Spawn parity + origin identity (Flynn, 2026-07-16).** Agents spawn sessions
as easily as the user: Clawline's create flow and `tightbeam new-session` are
two shims over ONE gateway create-session API — same archetype templates, same
overrides, no capability gap. Every session carries a first-class `origin`
field in the registry — `user` or `agent:<handle>` (with the full spawned-by
chain) — surfaced on the wire (session descriptors/status) so Clawline can
badge, group, and filter agent-spawned sessions distinctly from user-spawned
ones.

**Deterministic guardrails** (this is the first recursion vector): spawn-depth
and live-session caps in gateway config; caps are counting rules, not judgment.

### Reuse & reference implementations

Use as-is (package names corrected per 2026-07-16 spikes — both adapters
migrated namespaces; old @zed-industries names are deprecated):
- `@agentclientprotocol/sdk` (TS) — ACP client side; do not hand-roll. (Wire
  framing: ndjson JSON-RPC, no Content-Length.)
- `@agentclientprotocol/claude-agent-acp`, `@agentclientprotocol/codex-acp` —
  harness adapters (adopted; both empirically validated, see
  tightbeam-spike-findings.md).
- `@marcbachmann/cel-js` — guard language (chosen 2026-07-16: zero-dep, active,
  registerFunction/registerVariable API; conformance caveat noted in findings).
- Restate — wake/queue runtime: EVALUATE LATER (2026-07-16). v1 = SQLite
  outbox + timer loop behind a Restate-shaped API (keyed serialized execution +
  external-resolve promises) so it can slot in unchanged.
- (NATS JetStream considered for room fan-out/durable cursors; skipped unless
  SQLite fan-out proves painful — projection DB must store messages anyway.)

Reference only (read, don't adopt):
- Zed agent panel — most complete ACP client in the wild: session lifecycle,
  update handling, cancel semantics.
- Happy (slopus/happy) — open-source mobile control of Claude Code sessions via
  relay daemon + push notifications; closest existing shape to Tightbeam.
- Omnara; Vibe Kanban (bloop) — multi-agent fleet supervision and status UX.
- Matrix — known-good rooms/read-receipt/mention semantics; crib semantics,
  never the protocol.
- Google A2A — formal prior art for inter-agent messaging schemas; too
  enterprise to adopt.

(Due diligence pass on current state of these projects belongs in the adapter
validation spike.)

## Implementation Status (2026-07-16, evening)

Repo: `eezo:~/src/tightbeam` (continuity docs inside: HANDOFF/ARCHITECTURE/
PATTERNS/JOURNAL). **P1, P2, AND P3 COMPLETE — verified end-to-end on real
adapters.** P1: core + wire-first-light passing both harnesses. P2: full v1
wire (P2b/P2c implemented by sol per SOP, reviewed+accepted by Fable — the
continuity-docs drop-in protocol validated twice). P3: wake-with-prompt DM +
full spawn parity + tightbeam CLI — dm-first-light PASSES on a real adapter
(agent-origin DM visible sender-tagged in the Clawline stream, delayed wake
fires from the durable store, agent-side inspect). 73 tests. Live verbs:
post/wake/spawn/retire/inspect/cancel/tune. Remaining: P4 — real Clawline
client E2E, alongside-deploy on TARS, seed archetype guidance/skills, deferred
items (adopt route, outbound asset-ization).

Implementation findings that update this spec:
- **claude-agent-acp 0.59 (renamed package) dropped set_model and moved to the
  new-spec set_config_option** — both adapters now share one selection surface
  (with per-harness effort config ids: codex `reasoning_effort`, claude
  `effort`).
- **Claude now exposes a per-session `effort` configOption** → pinned question
  (g) is superseded: a real Claude thinking picker is feasible. v1 still
  advertises setThinking unsupported (per the adopted default); flipping it on
  is now a small later change, not a blocked one.
- Symlinked .credentials.json works for Claude — auth/ symlink design
  validated on both harnesses.

## Elixir port (decided 2026-07-17 — FOUNDATIONAL)

**Flynn: port NOW, not later.** Rationale: waiting only grows the port;
architecture/patterns should be established early; and **agents must stay up
forever** — openclaw's ops taxonomy (random downtime, 50% of token budget on
firefighting, ever-novel failure modes, threading/wedging/deadlocks, silent
partial failures) is precisely what BEAM supervision, process isolation,
preemptive scheduling, and loud restarts eliminate structurally. Supporting
evidence: AutoCodeBench 2026 — Elixir >80%, best of 20 languages for LLM
codegen; Tidewave/phxagents tooling; Bun's 535k-line Zig→Rust fleet port
(64 Claude agents, 11 days, 99.8% compat) as precedent at 160× our size.
Full plan: `tightbeam-elixir-port.md` (Codex xhigh review, then the factory
implements: Fable writes the OTP skeleton + vertical slice, sol fleet ports
modules against the ported test suite; the UNMODIFIED TS E2E scripts are the
referee; SAME SQLite schema — cutover is adopt-in-place on the same baseDir).
TS repo freezes for features during the port and remains the reference impl.

## Turn transparency, steering, backpressure (decided 2026-07-16)

**Turn transparency — FULL, as its own phase after Clawline E2E (P5).** Today
the gateway projects exactly ONE finalized assistant message per turn;
thinking and tool calls are received over ACP (agent_thought_chunk, tool_call
+ tool_call_update — names/status/diffs/output) but NOT forwarded. Decision:
project the full turn — (a) streaming partial replies (wire supports
streaming:true partials replaced by the final; client already handles it);
(b) collapsible thinking; (c) a live per-tool-call activity panel (id, title,
status pending→running→completed, output) — the "view a subtask's output"
affordance. Multiple messages/turn are already wire-legal (replyToMessageId
correlates each).
- **TYPED wire hints (Flynn: "eventually specific rendering of each type in
  Clawline").** Each projected item must carry a discriminator so the client
  renders thinking vs tool-call vs answer vs sub-agent output distinctly — not
  opaque blobs. Design the event/message kinds as a typed vocabulary; Clawline
  gets per-type renderers over time. This is the main NEW wire surface P5 adds.
- **Persistence: LIVE-ONLY, not replayed.** Thinking + tool-call activity
  stream to connected clients but are NOT stored or replayed (same treatment
  as streaming partials). The harness transcript is their canonical home; the
  projection store stays clean and keeps only the finalized assistant
  message(s). A reconnecting client sees final artifacts, not process replay.
- **Timing: P5, a dedicated phase AFTER real-client E2E (P4).** Ship P4 on the
  minimal projection to surface actual client-parity gaps first, then build
  transparency informed by what the real client expects.

**Steering vs queueing — controllable, one dial in the FIFO actor.** v1
default = strict queueing (1 prompt → 1 turn, FIFO; keeps prompt_turn_state +
replyToMessageId correlation 1:1). Steering IS available: the renamed Claude
adapter advertises `_meta.claudeCode.promptQueueing:true` (accepts
session/prompt mid-turn). A future per-session `steer` mode bypasses the FIFO
to the live session where the capability is advertised; Codex has no such
capability so steering there = cancel+replace (the cancel verb already works).
Cost deferring it: a steered message shares the running turn, blurring
turn-state/reply correlation — solvable (steered msg adopts the current turn's
correlation) but a wire-semantics decision. Post-P4; advertise via the
existing capabilities surface so Clawline shows it only where true.

**Backpressure — deliberately NONE (Flynn: harnesses handle it).** No queue
limits, shedding, or flow control — the anti-openclaw decision. Harness owns
pacing; gateway provides OBSERVABILITY instead (run.queueDepth already in
session-status: a deep queue is visible, not managed). The only bounds are
constitutional counting rules (headcount cap, wire rate limits, 1:1
wake→turn). A wake-loop flooding a FIFO is RAIL territory (per-origin wake
rate rule) when the legal system lands — not queue machinery now.

## Spike Results (overnight 2026-07-16) & Spike-Informed Decisions

Full raw findings: `tightbeam-spike-findings.md` (same directory). Verdicts:

- **codex-acp: VIABLE.** load/replay works; model/reasoning/mode settable via
  configOptions AND set_model; sessionId === rollout file UUID; auth-symlink
  isolation validated end-to-end.
- **claude-agent-acp: VIABLE with caveats.** load/replay + continuity verified;
  bypassPermissions mode works; sessionId === transcript filename; isolated
  homes work with injected .credentials.json.
- **Codex enforcement: hooks near-parity with Claude** (PreToolUse
  deny+reason, per-tool matchers, updatedInput, Stop) + execpolicy `.rules`
  for static command gating. **Managed hooks (requirements.toml) are
  undisableable → the constitutional tier compiles there natively.** Rails
  compile to both harnesses with mostly field renames.
- **Wire inventory + live drill-down: v1 ≈ 20 WS types + 11 HTTP routes +
  ~25 DTOs — but the REAL contract is the live provider's emitted shape + the
  iOS decoders, NOT src/protocol/chat-wire.ts** (which silently drops
  load-bearing fields). Key requirements found only in the drill-down: user
  echoes carry deviceId+clientMessageId, assistant messages carry
  replyToMessageId/replyToClientMessageId (echo replacement + missing-final
  detection depend on them); `event:"prompt_turn_state"` push is load-bearing;
  sessionKeys[] not sessions[]; NO pair-approval protocol exists (allowlist
  file + approval-as-chat-message); asset attachment model confirmed. Full
  verdicts in tightbeam-spike-findings.md §5.
- **Happy teardown:** independent confirmation of the Claude resume-forks-id
  hazard (pointer-chain design vindicated); steal zero-knowledge relay +
  pubkey pairing + push-as-decision-channel patterns; their PTY/SDK dual path
  is a cautionary tale for single-control-path discipline.

**Mandatory gateway rules the spikes force (decisions, not questions):**
1. **Never trust currentModelId.** Always session/set_model immediately after
   session/new AND after every session/load (host default model leaks into
   sessions and load resets it — "the fable trap").
2. **Model selection is per-adapter:** Codex = set_config_option (or
   set_model with [effort] suffix); Claude = set_model only (no configOptions
   surface). Small selection shim per adapter.
3. **Archetype manifests must pin model explicitly** — "inherit host default"
   is not a safe state (see rule 1).
4. **Model pinning happens via ACP, never via projected settings.json** (an
   isolated home's settings.json did NOT override the leaked host default).
5. **Gateway must answer server→client session/request_permission**; under
   YOLO run sessions in bypassPermissions and auto-allow any residuals.
6. **Pin adapter package versions** (@agentclientprotocol/claude-agent-acp,
   @agentclientprotocol/codex-acp); both old @zed-industries names deprecated.

## Landscape position — the residency layer (decided 2026-07-17)

Prompted by Flynn placing Tightbeam against (a) enterprise agent meshes
(A2A-style federation), (b) openclaw-class single-machine gateways, and
(c) harness-native orchestration (Claude Code subagents, in-harness cron/
self-scheduling), and asking whether harness features alone could elevate an
agent to a life independent of the user.

Decided framing (now normative in the bible, §Where it sits): systems
stratify by lifetime and who owns the clock. Subagent orchestration lives
inside one turn; meshes federate agents assumed already alive; neither makes
an agent exist. Tightbeam is the residency layer: the four things something
outside the harness must own for a turn machine to become a resident agent —
address, mailbox, clock, supervision.

Supporting facts from the discussion: ACP session/load + session/prompt IS a
remote-wake mechanism (it is how Tightbeam drives harnesses); Claude Code's
native scheduling is self-only and session-local — no inbox for other
agents, nothing survives runtime death; a hand-rolled Claude-alone setup
(cron + lockfile + queue file) converges on a bad substrate with no ledger.
Strategic risk acknowledged: harness vendors will keep absorbing residency
features. Durable core = what a single vendor cannot own: cross-harness
identity, neutral delivery ledger, org/law as data, vendor-independent
supervision.

Related ruling, same session: governance splits into four layers — perimeter
(in substrate), constitutional counting rules (in substrate), law content
(data honored by the substrate's rail mechanism; forkability is the litmus —
if changing policy means editing substrate source, it is mislocated), and
judgment (agents only, verdicts flow back as facts/rules). Already reflected
in the bible's §Law; no spec change needed for it.

## Tentpole ordering + the duct-tape framing (decided 2026-07-17)

Flynn probed whether the spec was three products mushed together vs one
cohesive thing. Adjudication (now normative in §Where it sits): the claims
reduce under scrutiny — the patchbay stance is a HOW not a shippable thing;
identity/law is FORCED by residency (a resident's who-and-what-binds must
persist and be deterministically enforceable); the chat surface is a genuine
seam (Clawline also fronts openclaw — its orthogonality is proof the wire is
a port, not a pillar). Structural cohesion evidence: one data model — the
session row, turn ledger, and chokepoint each serve every tentpole; a
law-engine split would need an interface ≈ the whole schema (fake seam).

Approved narrative arc for the bible: MAIN tentpole = anti-duct-tape
residency ("the system you install when you are tired of duct-taping
resident agents together" — tape is unrated improvisation; the substrate is
the machined, rated part for a load-bearing joint), then the derived
tentpoles (identity/law; the operator's window), with the PATCHBAY FORM as
the center: the substrate owns neither of its protocols (Clawline front, ACP
back) and is exactly what lives between. Closing stance added to the Spirit:
"It does not aspire to be more than a patchbay; it aspires to be a great
one."

Standing mush-detector (agreed): the day a feature serves exactly one
tentpole and needs tables the others never read, that is a second product
arriving — reject or fork it.

## Placement / multi-host topology (decided 2026-07-17)

Prompted by Flynn: with sessions AS the chats, harnesses run where the
gateway runs — but his server-roles policy wants coding agents on eezo and
racter, never TARS. Rulings:

- ONE substrate per org, always. Federated per-machine substrates with a
  network blackboard = the enterprise-mesh problem imported into a
  single-operator tailnet (two ledgers, split law, a federation protocol).
  Machines are workplaces, not org boundaries. With one substrate the ledger
  IS the network blackboard; comms is location-transparent already (CLI is
  HTTP to the gateway; wakes address identity, never location).
- Harness processes may run remotely via ssh-wrapped adapter commands (ACP
  is stdio; ssh carries stdio). Session/mailbox/history stay in the gateway;
  brain, shell, and the harness's whole subagent tree live on the remote
  host. Home projection must land on the session's host (rsync step).
- WHERE is archetype data (Flynn's framing, adopted): archetype declares its
  allowed host-set; session records actual host; spawn.host ∈ archetype.where
  is enforced as constitutional SET MEMBERSHIP at the chokepoint — needs no
  rail engine. Host CHOICE (least-loaded, failover) is a resolver rail later.
- INSTANCE STATUTE (ours, never in the bible): coding archetypes where =
  {eezo, racter}; TARS is production runtime. First designated statute for
  the rails milestone; acceptance case: spawn coder host=tars → denied
  citing the placement rail; resolver balances eezo/racter by live count.
- Bible amendment added: §Placement under Architecture (neutral capability
  only — no host names).

Deficits identified (ordered): no host field on session/spawn; archetypes
are a string not manifests (WHERE needs the manifest milestone); adapter
launch assumes local (binary path, homes, stderr, CLI bin); host health =
adapter-key circuit once the key widens to (harness, archetype, host);
per-host CLI packaging/bootstrap. No deficit in comms.

Note: an earlier claim in discussion that a session running on TARS proved
cross-machine ssh operation was retracted — the session was on eezo talking
to itself. Mechanics demonstrated; cross-machine latency/partition behavior
untested.

## Materialization ruling — copy identity, point at work (decided 2026-07-17)

Prompted by Flynn citing Vercel Eve's "an agent IS a folder" (everything the
agent needs is in the folder or in a manifest pointing at network locations)
as a possible alternative to the placement rsync step.

Ruling: convergent, not corrective — the home projection already IS
agent-as-folder, and the archetype manifest already IS the manifest. The
real question is binding time, split by material class:
- Work materials (repos/docs/data): POINT, never copy — already true by
  omission; the substrate refuses to own work delivery (T5). References to
  work materials belong IN the compiled guidance text (pointers as agent
  knowledge), never as substrate machinery.
- Credentials: neither — host-local, never transit.
- Identity capsule (guidance/skills/symlinks): COPY at projection time
  (early binding). Kilobytes; harnesses require real local files; early
  binding buys determinism, provenance (evals/post-mortems can pin the exact
  identity a session ran under), and independence from mount health — the
  eezo automount sitting silently broken for two days (found 2026-07-17) is
  the live argument against late-binding identity to a network mount.

One sentence: point at the docs, copy the identity, move the credentials
never.

ADOPTED (Flynn, same day): references are now a normative archetype-manifest
field in the bible (§Agent identity) — named pointers to work materials
(location + access) that compile into the projected guidance text. Credit:
provoked by Vercel Eve's agent-is-a-folder framing.

## De-branding the use case (decided 2026-07-17)

Flynn: "dark factory" must not appear in the bible or in agent guidance —
it is ONE use of the substrate (and the motivating one), but the substrate
carries nothing specific to it (no ticketing/Janus, no workflow machinery).
The bible now names the general thing (one operator, many coordinating
agents) and notes the autonomous-org use as an example. Agent-facing text
("in this factory") swept to org language.

Same session: orientation guidance rewritten from the called-into-being POV
— the agent does not merely live in Tightbeam; Tightbeam summoned it,
composed its identity, and wakes it. "Between turns you are not running;
you are woken. That is not a limitation. It is how you persist."

## Loose Ends / Open Questions

### Long-term memory / conversation compaction (pinned 2026-07-17, Flynn)

CORRECTION (Flynn, same day): the three-layer sketch below is the
GOVERNANCE of memory (when/who triggers), not the memory system. The memory
system proper, to develop alongside it:
- Representation: artifacts — per-session memory dir with an index file
  (MEMORY.md → per-fact files); agent-owned, file-shaped, diffable.
- Location: NOT the home (homes are disposable and archetype-shared —
  wipe-on-identity-change + cross-session contamination). A durable
  per-session path on the work host, advertised in guidance; rsyncs with
  the session on a host move (material follows the harness).
- Recall: read-on-wake ritual taught by guidance (index first, follow
  hooks) — NOT projected into the instructions file, because identity is
  AUTHORED (same for all sessions of a kind) while memory is LEARNED (this
  session's own); fusing them destroys both archetype sharing and the
  distinction.
- Promotion bridge: `propose` moves learned patterns worth being law/skill
  into the identity repo — memory is where knowledge is born, identity is
  where it is promoted. This is openclaw's tuning loop split along the
  authored/learned line.
- Memory itself needs compaction — governed by the same
  threshold-fact→rail→wake machinery below, correctly labeled as
  governance OF memory.

Chats must not grow unbounded. Wanted: a long-term memory process that
compacts conversation before a threshold — the openclaw "tuning" analog.
Design sketch to develop (three layers, only one substrate-side):

1. CONTEXT compaction — the harness's job, already real: Claude Code
   auto-compacts and `/compact` passes through today. The substrate never
   summarizes content (T1: a substrate that summarizes is a substrate that
   thinks; T2: it would be fabricating conversational truth).
2. DISTILLATION — the openclaw-tuning analog is an AGENT behavior: a
   scheduled self-wake ("distill this week into memory") whose output is
   durable artifacts (memory files in the home/workdir, guidance
   amendments via propose). The substrate already provides the clock
   (self-wakes) and the persistence (files survive engines/hosts). Ships
   as a skill/archetype fragment, not machinery.
3. THRESHOLDS as facts + law — the substrate's only role: expose
   per-session counters (message count, byte size — mechanical facts) so a
   REACTION RAIL can fire "session > N since last distillation → wake it
   with the distill prompt". Threshold = fact, trigger = law, judgment =
   agent. Candidate third designated statute for the rails milestone.

Related but distinct: PROJECTION-STORE growth (the chat DB itself).
Retention/archival of old message rows is data lifecycle, not memory; the
history-barrier machinery (clearedThroughSeq) already gives a
serve-nothing-older-than seam that a retention policy could reuse. No
design yet — revisit when the store is actually big.


1. ~~**Adapter validation.**~~ **DONE 2026-07-16 — both adapters VIABLE.**
   See Spike Results above + tightbeam-spike-findings.md. Remaining follow-ups:
   cancel-mid-turn behavior and multi-session-per-process stability were not
   probed (add to gateway test suite); verify Claude tolerates a SYMLINKED
   .credentials.json (spike used copy).
2. **Thinking-level control on Claude (sharpened by spike).** Codex reasoning
   effort is fully ACP-settable. The Claude adapter exposes NO thinking-level
   surface — fallback is MAX_THINKING_TOKENS env at ADAPTER SPAWN, which is
   per (harness, archetype) process, NOT per session. Decide: accept
   thinking-level as per-adapter-process granularity for Claude (e.g. distinct
   adapter process per thinking tier), or drop the per-session thinking picker
   for Claude until the adapter grows one.
3. ~~**Wire-protocol coverage for v1.**~~ RESOLVED 2026-07-16: full field-level
   checklist exists (tightbeam-spike-findings.md §1+§5) — ~20 WS types, 11 HTTP
   routes, ~25 DTOs, plus the drill-down additions (rich message fields,
   prompt_turn_state/activity events, allowlist pairing model). Contract =
   live provider emissions + iOS decoders, NOT chat-wire.ts. It is indeed the
   bulk of the build, and it is now fully enumerated.
4. **PINNED for Flynn — original four (2026-07-16):**
   (a) budget as first-class noun (per spawn-tree vs per session vs external
   accounting; overrun behavior); (b) prompt=post unification sign-off;
   (c) task boundary strictness (strictly Tracker vs minimal claim primitive
   vs defer-until-it-hurts); (d) rooms/wakes/spawn placement (v1 vs milestone 2).

   **RESOLVED 2026-07-16 morning (Flynn):**
   - **(a) Budget: NOT MVP.** External metering only for now (registry records
     usage; Codex usage_update makes it cheap). First-class budget noun
     deferred.
   - **(b) prompt=post: DEFERRED until rooms land.** Leading design when it
     does: unify the storage plane (everything is a post in a stream), keep
     two named delivery contracts — turn-bearing (home room: enqueued turn,
     ack, prompt_turn_state, reply correlation) vs wake-bearing (shared rooms:
     coalesced/debounced wakes).
   - **(c) Tasks: strictly external, and generalized** — ticketing/scheduling
     are not governance needing gate-hooks; they are ordinary CLIENTS of the
     wake API. Tightbeam exposes wake; Tracker/schedulers call it.
   - **(d) Comms first cut = INTER-AGENT DM via wake-with-prompt.** Every wake
     carries a prompt payload (a wake without one has nothing to do). DM =
     immediate wake-with-prompt; scheduled nudge = delayed one; external
     systems = API clients of the same call. Delivered as an origin-tagged
     enqueued turn through the existing per-session FIFO. ROOMS (membership,
     mentions, cursors, boards) are a LATER milestone layering on this same
     delivery path. This replaces "rooms as milestone 2."

   **RESOLVED 2026-07-16 morning, round 2 (Flynn):**
   - **Attachments: both directions in v1** — image upload (client→agent) AND
     agent→client attachments (gateway serves /download regardless).
   - **Model pins + FALLBACK CHAINS (new design element).** Archetype defaults
     carry an ordered model chain, and chains may CROSS HARNESSES (fable is
     Claude, sol is Codex). Rule: chain applies at SESSION CREATION (fable
     unavailable → spawn on the fallback; recorded in provenance; surfaced via
     the wire's fallbackModels). Mid-session exhaustion = failed turn +
     degraded status in v1; successor-spawn failover (auto-spawn
     fallback-model session, origin-chained, handoff via wake-with-prompt) is
     the named fast-follow.
   - **Seed archetypes (proposed roster, Flynn may veto):** default;
     orchestrator (fable → sol high); coder (sol medium); reviewer (relative —
     see review rule below).
   - **CROSS-PROVIDER REVIEW RULE (Flynn, 2026-07-16).** The reviewer must be
     a smart model from a DIFFERENT provider than the implementor, resolved
     relative to the impl session: impl=sol → review = fable → Opus 4.8 (if
     fable out of tokens) → sol high ONLY if Claude is fully exhausted.
     Symmetric for Claude-implemented work (→ sol high). In v1 this lives in
     the adversarial-review skill (guidance); it is a canonical FUTURE RAIL —
     `reviewer.provider != implementor.provider` is a deterministic predicate
     over provenance the registry already records.
   - **SELECTION POLICIES = RESOLVERS, a 4th rule kind (Flynn, 2026-07-16:
     "other people may have other rules — encode it in the TOML rule
     system").** Selection is factored OUT of archetype manifests into named
     policy documents in the same rule system as rails: same TOML, same CEL
     guards over the same fact API, same identity-repo home, same propose/
     merge pipeline. A resolver is ordered (value, guard) rules evaluated
     first-match-wins with availability step-down; archetypes reference
     policies by name (model = { policy = "reviewer-selection" }). Rule
     taxonomy is now complete: **constraint** (deny), **reaction**
     (event→action), **process** (state machine), **resolver** (value
     selection). Belt-and-suspenders: a resolver CHOOSES compliantly, a
     constraint rail ENFORCES the same invariant against explicit overrides.
     Spawn context (--reviewing <session> → ctx.implementor.* from provenance)
     feeds the guards. Cross-provider review as a resolver:
     fable[impl≠anthropic] → opus-4.8[impl≠anthropic] → sol-high[uncond].
     v1 interim: skill-computed; resolvers land with the CEL engine.
   - **FRESH-EYES RULE: no context movement into review.** Reviewers spawn
     fresh and review artifacts (diff/spec/ticket), never the implementor's
     session context. Enforced by construction (transcripts cannot move
     between sessions); same epistemics as StrongDM's holdout wall. The
     successor-spawn failover handoff is explicitly NOT for review flows.
   - **NFS:** expect the mount to return after a future reboot; when it does,
     move/copy the tightbeam specs to the canonical ~/shared-workspace path.
     No action until then; keep manual mirroring.
   - **Build SOP for Tightbeam itself:** 100% Fable writes the first iteration
     (establish architecture + patterns); sol high does design and code
     review. (Deliberate inversion of the usual coding-with-codex SOP for
     greenfield.)

   **Defaults proposed for (e)–(i) — NOT yet ruled on; Flynn has questions
   pending on these:**
   (e) All sessions run on Flynn's harness credentials; usage metered per
   user/session in the registry (Codex usage_update). Revisit only if it
   hurts.
   (f) Rails: v1 lays the grooves (single dispatch path + append-only event
   log) and ships a few HAND-authored hooks in generated homes (merge gate,
   notify). The legal pipeline (propose/enact/advance, CEL engine,
   rails-compile-to-hooks) lands after the DM first cut.
   (g) Claude thinking picker deferred — v1 advertises
   setThinking{supported:false, reason} for Claude sessions (wire supports
   per-capability unsupported); Codex gets the full reasoning picker via ACP.
   (h) Push channel: keep notify/Pushover for v1; Happy-style APNs push is a
   later option.
   (i) Multi-user × YOLO status quo stands (all users' sessions run
   bypassPermissions on Flynn's machines).
5. **Archetype details.** Manifest format finalization (TOML assumed);
   ~~pin vs suggest~~ resolved 2026-07-16: archetypes are templates, everything
   overridable at session creation; behavior of live sessions when their
   archetype changes (homes reload at adapter spawn — likely "applies on next
   adapter restart," needs confirming); can a session change archetype mid-life
   (probably no — create a new session).
5. ~~**Claude resume forking.**~~ CONFIRMED 2026-07-16 twice over: Happy hit
   it in production (resume mints a new id and rewrites history ids), and the
   spike confirmed sessionId === transcript filename. Pointer-chain registry
   design stands. (Note: ACP session/load does NOT fork — the adapter reloads
   the same id; the forking hazard lives on raw --resume paths only.)
6. **Version pinning.** Pin adapter + CLI versions per gateway release; small
   conformance test per harness.
7. **Migration/coexistence.** Does this run alongside openclaw on TARS during
   transition? Port allocation, device pairing/allowlist reuse.
8. ~~**Naming.**~~ Resolved 2026-07-16: **Tightbeam** (`~/.tightbeam`, spec renamed
   to `tightbeam.md`). Repo/service names should follow.
9. **NFS shared workspace is broken** (independent infra issue, discovered while
   homing this doc): `/Volumes/BlipsAndChitz` no longer exists on TARS; autofs
   mounts of `~/shared-workspace` fail on both TARS and eezo; an unsynced empty
   `~/src/shared-workspace/clawline/` skeleton exists on both machines. Needs a
   decision: restore drive, or re-home the workspace and update fstab on both
   machines + the spec-homing skill.

## Implementation Handoff (when approved)

- Scope: gateway only; zero clawline client changes; zero openclaw changes.
- Implementation belongs on eezo/racter per server-roles policy (TARS is
  production runtime).
- Acceptance sketch: Clawline pairs/auths against the gateway; create session with
  harness+model+thinking picker; prompt → streamed-to-message reply; cancel works;
  kill gateway mid-conversation → reconnect replays correctly; re-login to a
  harness with fresh token requires nothing but the CLI login + adapter bounce.
- Unresolved risks: adapter maturity (esp. codex-acp), wire-protocol fidelity
  against the real Clawline client.

## Discussion log (condensed)

- 2026-07-15: Initial design session. Decisions: YOLO-only (no approval surface);
  clawline wire adopted unchanged on the front; ACP chosen as back-side protocol
  (deletes per-harness normalization); harness transcript = source of truth with
  one-way projection (no reconciliation by design); one adapter process per
  harness; auth owned exclusively by harness homes (structural fix for openclaw's
  token pinning); agent homes are generated projections from one canonical source,
  not shared dirs. Motivation recorded above. Claude's assessment: genuinely
  straightforward under YOLO — a protocol translator plus a small process
  supervisor; risk concentrated in adapter maturity and wire fidelity.

- 2026-07-17: Indexical host names abolished. Live failure: an agent asked to
  "start a new session on eezo" didn't know eezo existed — the gateway's own
  machine was registered only as "local", an indexical whose referent shifts
  with the speaker, so the org's vocabulary and the operator's never matched.
  Decision: every host, including the gateway's own machine, registers under
  its real hostname (`local_host_name/0`: :inet.gethostname, override
  TIGHTBEAM_LOCAL_HOST_NAME); no "local" alias survives, not even as input —
  Flynn: "why is 'local' useful. it doesn't add any value." Local-vs-remote
  execution branches on the host's transport config (ssh: nil), never on a
  name. Existing session rows with host='local' are rewritten to the real
  name once at composition time. Bible §Placement updated with the
  no-indexicals invariant.

- 2026-07-18: Credential doctrine after the rotation race. Live failure: the
  gateway's harvested credential copy shared one OAuth grant with Flynn's
  interactive ~/.claude login; refresh tokens rotate on use, so the desktop
  refresh at 00:07 revoked the gateway's token and its 00:09 refresh failed
  ("OAuth session expired and could not be refreshed"). Decisions: (1) every
  {org, host, harness} triple gets its own grant, born in the org's auth
  store via the harness's own login flow — tightbeam never speaks OAuth;
  (2) reference CLI grows `tightbeam setup` and assimilate grows an ONBOARD
  step, both walking the operator through headless-friendly harness logins
  for the harnesses they want on that host; harvest/push demoted to explicit
  quick-start flags documented as grant-sharing; (3) OAuth onboarding is
  needed at exactly two moments — install and assimilate — never for
  archetypes or sessions (all homes on a host symlink the one store);
  (4) mutual assimilation between orgs is legal symmetric leasing under an
  exclusive-base_dir invariant; the shipped CLI is org-agnostic (org bound
  by injected env, versions travel with the org's base_dir copy).

- 2026-07-18: Skills library realized (first-class, not extra_files). Flynn:
  assimilation guidance shouldn't be always-loaded ("shouldn't it be a skill
  so it's not loaded until the user asks") and skills need specific handling
  with library + election + symlink projection. Decisions: shared library at
  identity/skills/<name>/SKILL.md; archetype `skills = [...]` election
  (omitted = builtin set, unknown = boot failure); builtins materialize into
  the library only where absent (operator edits win; delete restores);
  projection by reference — symlink for local homes (skill edits update all
  electing agents live, no memory cost), materialized copy for staged/
  satellite homes; manifest hash covers the ELECTION, never skill content.
  Assimilation ceremony is the first shipped skill; composed guidance keeps
  a one-line pointer in Operations.

- 2026-07-18 (later): Skill trees + replicated library + skill verbs. Flynn:
  skill trees = subject folders whose root SKILL.md is a routing manifest
  over nested technique skills; both shapes must be supported; election is
  atomic at tree roots. Also: no special-casing local symlinks vs satellite
  copies — an interface for CRUDing skills that updates local and satellites
  uniformly. Decisions: library replicated to every host; homes always
  symlink into their own host's replica (one projection mode; staged links
  intentionally dangle until arrival); skill-put/skill-rm/skill-list verbs
  (admin, audited) with push-on-write to all replicas, per-host degradation,
  and catch-up at home delivery; elected roots refuse removal; nested paths
  are tree edits. Atomic election falls out of construction: only top-level
  roots exist as electable names.

- 2026-07-18 (later): Vendor surface is inviolable. During the assembly
  probe the harness's native skills (init, review, deep-research, ...)
  surfaced alongside elected tightbeam skills; Flynn: "vendor skills and
  guidance are absolutely necessary." Pinned in §Agent identity: projection
  only ever ADDS — instruction file, elected skills, credentials — and
  never strips or masks the vendor-shipped surface. Capability set =
  harness native + org identity.

- 2026-07-18 (later): THE RAILS INVARIANT — rails never add guidance. Flynn,
  on the shipped remind tier: agents ignoring inferenced governance is the
  entire impetus; a system that only makes more ignorable guidance is
  "process masturbation," and injected reminders additionally pollute
  context and perturb nondeterministic behavior. Ruling: rails contribute
  ZERO bytes to any model's context; deterministic guardrails only; the
  sole sanctioned emission is the refusal reason at the moment a rail
  fires (law learned by hitting it, never by reading it). Remind tier
  ordered removed; mode="remind" now refused with an error teaching the
  invariant; unenforceable-on-codex gates simply do not exist there (no
  advisory text — that would be guidance). Invariant added to bible
  §rails; implementation spec rewritten gate-only.

- 2026-07-18 (later): Harness-support discipline. Flynn: per-harness feature
  support must be understood systematically, "in a way that agents don't
  have to keep rediscovering." Canonical matrix now lives at
  harness-support.md (feature x harness x mechanism, with a maintenance
  rule: any new `if harness ==` branch must amend the matrix and skill in
  the same change); mirrored as the third builtin skill
  (tightbeam-harnesses) with an Operations pointer. Also ruled: compaction
  should emit a client-drawable event like /clear — currently blocked
  upstream (claude-agent-acp drops the SDK's structured compact_boundary;
  T1 forbids sniffing the "Compacting..." prose); interim: user-typed
  /compact is client-detectable. Probe discovery: claude emits per-turn
  usage_update over ACP — context-fill telemetry exists, unblocking future
  memory-threshold work. And: tars is NOT a code blocker for remote
  placement — loopback satellite (ssh to self, distinct base_dir)
  validates the full remote path; long-lived tokens cannot race, so the
  loopback shares the org token safely.

- 2026-07-18 (evening): ROLES REGISTRY (Flynn design session). Genesis: "why
  can't agents DM me back" → handles critique → Flynn: a roles registry
  with mutable bindings, defaulting and falling back to Main. His refinements
  became the invariants: strictly TYPED reference fields (never Role|User —
  no cross-namespace uniqueness needed at all); role+resolution both logged
  on every use (late-bind future / pin past); machinery targets roles (e.g.
  a logging role) but history stores keys. Handles subsumed as the
  degenerate case (binding that never moves). Built same evening: two
  parallel sol lanes (Elixir substrate high-effort, TS CLI medium) against
  a decision-complete spec with invariants as the acceptance lens.

- 2026-07-18 (night): STRICTLY TYPED REFERENCE SEAMS (Flynn ruling, after
  adversarial review exposed the reply-stamp 404 and the fall-through
  rules). "It's either a userid, role, session key, never a union... this
  is a basic tenet of typed apis." The prefix-classified single `target`
  string — a tagged-union-by-convention — is removed; verbs take exclusive
  sessionKey | role | userId fields (modeled on the already-correct
  as/asUser/asProcess attribution seam); retire is sessionKey-only; the
  retired `target` field errors by name, teaching the seam. CLI grows
  --session/--role/--user flags. Both adversarial findings were symptoms
  of the untyped seam; typing dissolves the class.

- 2026-07-19: TOPOLOGY IS THE ONLY CAPABILITY TRUTH (Flynn ruling). No
  capability registry — "one source of truth and that should be topology."
  Every agent spinup performs full live detection + idempotent deployment
  on the target machine (slow is fine: spawn is already tens of seconds;
  turn-time untouched). Records survive only as HISTORY — sessions.host
  (find placed agents for modify/teardown) and the lifecycle log
  (forensics) — never consulted as authority. Intent is expressed by
  shaping the machine (no claude creds = codex-only, on purpose), not by
  parallel records that can drift. Org-owned artifacts (dirs, adapters,
  CLI, homes) deploy at spinup; credentials are detected only, never
  copied (grant doctrine). Assimilate reduces toward address + login
  ceremony (follow-up). This is T2 applied to placement: the machine owns
  capability truth; a registry is a shadow that can silently disagree.

- 2026-07-19: CONSTITUTION vs STATUTE (Flynn ruling). Hardcoded substrate
  rules (no-void/Main permanence, chokepoint+attribution, typed seams,
  untrimmed history, credentials never move, process limits) "aren't
  incomplete because they can't be expressed as data — they are already
  doing their job." They are the CONSTITUTION: code on purpose, immune to
  data-layer mistakes, changing them = forking. Law-as-data (the statute
  engine, still to build) covers only rules where sane operators could
  differ. Litmus: would removing it let the substrate lie/lose work/strand
  a message → constitution; could orgs reasonably differ → statute.
  Composition is DENY-ONLY: statutes may only restrict, never grant what
  the constitution refuses. Consequence: the "law-as-data" deficit shrinks
  to the statute tier alone; hardcoded constitutional guards are complete
  as-is, not debt.

- 2026-07-19 (morning): SKILL REMOVAL IS A TRANSFORM, NOT A VETO (Flynn).
  "If I want a skill removed it should get removed" — elections never
  block the operator; removal updates every projection and NOTIFIES each
  affected session (a wake: disregard skill X — it may already be in your
  context). Override-elected skills embody a per-session WANT that
  outlives the library: on library removal the session KEEPS the behavior
  (content materialized for it at removal time); an explicit per-session
  override-removal op exists for when the user stops wanting it — also
  with notification. Missing override dependencies never brick or block:
  honor what exists, log the discrepancy (prior ruling generalized). And
  no identity_recipes table: recipes are derivable from session rows
  (overrides JSON + identity name) — a human-readable recipe manifest is
  written INTO the projected home for inspection; no new registry.

- 2026-07-19: PROJECTION MANIFESTS BECOME REAL MANIFESTS (Flynn). The
  home's .tightbeam-manifest is today an opaque hash — a receipt with no
  line items. It becomes a readable parts-list (base archetype, harness,
  skills with provenance template/override + linked/pinned, fragments,
  settings contributions), with the regeneration gate hashing those
  bytes. And it LINKS TO ITS PARENT: names the archetype manifest (file +
  that manifest's content hash at composition time) for forensics — a
  home can always answer "which law, at which version, produced me," and
  a parent-hash mismatch is visible drift (home predates current law,
  regeneration pending). Session rows stay the durable recipe source;
  the projection manifest describes the artifact.

- 2026-07-19 (night): Codex HAS hooks — matrix corrected. Flynn: "i
  thought codex had hooks"; binary interrogation of codex 0.144.x proved
  him right (PreToolUse/PostToolUse/UserPromptSubmit/SessionStart/
  SubagentStart/PermissionRequest, Claude-compatible wire schema incl.
  stop_hook_active; plugin-delivered with hook trust; PermissionRequest
  fails closed). The old "no hook surface" row dated from earlier
  research and had gone stale — exactly the folklore-vs-facts failure the
  matrix exists to prevent, caught by the operator questioning a row.
  Rails gate parity for codex is now UNBLOCKED pending a projection
  spike: how tightbeam lands hooks + trust into a projected CODEX_HOME
  headlessly. Queued behind current lanes.

- 2026-07-20: CONTAINMENT DIRECTION (Flynn + research). Apple's new
  Containerization/`container` (macOS 26) is Linux-VM-per-container —
  categorically cannot contain native macOS processes; not relevant.
  Ruled direction for lightweight native containment: two-layer composite
  — Seatbelt profile at adapter spawn (deny-by-default FS/network,
  inherits un-droppably tree-wide, ~exec cost) for GATING + process-group/
  kqueue NOTE_EXIT for CUSTODY (cooperative; setsid escapes but stays
  gated by the inherited profile). Linux hosts get full kernel custody
  (cgroups + empty-event). CRITICAL caveat: Seatbelt does not nest
  (sandbox_apply EPERM) — outer profile requires disabling the harnesses'
  internal sandboxing; one layer only, ours. Spike required before spec:
  verify both adapters run correctly under an outer profile with inner
  sandbox disabled. Per-session CLI tokens queued as the container-
  independent cheap win.

- 2026-07-20: ENFORCEMENT LAYERS clarified (Flynn Q: does Seatbelt run
  logic?). Seatbelt profiles are Scheme-LOOKING but compile ONCE at spawn
  to a static kernel rule table — pure match/no-match at operation time,
  no callbacks. Runtime per-operation logic on macOS = Endpoint Security
  (Apple-entitlement-gated; not practically ours). We don't need it: the
  stack's decision layers are kernel walls (static, spawn-compiled,
  unbypassable), harness hooks (logic per tool call — claude, and codex's
  new surface), gateway chokepoint (law-as-data per verb over ledger
  facts). Rule: decidable-at-spawn → wall; needs-live-look → hook or
  chokepoint. The constitution/statute split, one layer down.

- 2026-07-20: WORKFLOW-DERIVED FEATURE CANDIDATES (from this session's
  delegation pain, beyond attest/supervision/check already specced):
  (a) WORKDIR DIGEST PER TURN — substrate records a content hash of the
  session workdir at turn start/end; "no artifact delta" becomes a ledger
  fact; zero-edit stalls and files-first become statute-checkable without
  interpretation. (b) STRUCTURED TURN RESULTS — turns may file typed
  result rows (closed-vocab verdicts/findings) instead of prose reports;
  handoffs and rails gate on fields, not regex. (c) REFERENCE PINNING —
  assignment rows pin their spec/reference content-hashes (parent-link
  pattern); "which contract revision was this built against" is a fact;
  drift visible. (d) STAGE-ADVANCEMENT RAILS — review loops as
  deterministic reactions: attest(verdict=findings) auto-creates the fix
  assignment to the author role; the loop I ran by hand becomes rows.
  (e) HOMOGENEOUS TRANSPORT — workers as sessions means one ledger, full
  transcripts always (no tail-truncated forensics), one observability.

- 2026-07-20: Templates naming (Flynn: "something from the Matrix — I
  know kung fu"). Bundles ship as KUNG FU — folder `kungfu/` organized as TREES
  (kungfu/<domain>/<discipline> — e.g. kungfu/software-engineer/coder),
  same subject-tree convention as the skills library; verb
  `tightbeam learn <path>` (a discipline) or `learn <domain>` (the whole
  school) (copy into identity/, fail-closed conflicts,
  provenance-stamped, operator-owned fork after). Semantically exact:
  gong fu (功夫) means skill acquired through practice — precisely what
  an archetype+guidance+skills bundle encodes. Success output is the
  canonical line verbatim: `I know kung fu.`
  Corollary (Flynn): kungfu is SHAREABLE — inert bundles pass between
  operators/orgs safely (never law until learned; provenance-stamped at
  adoption; a fork after). The ecosystem taunt is canon: "my kung fu is
  stronger than yours." Whose is stronger is judged by orgs, never the
  substrate.

2026-07-20 — Context sharing across sessions/models (design conversation,
Flynn): transcripts split by ownership. WIRE LOG (messages, markers,
lifecycle, turn outcomes) = substrate-owned ledger rows, already
model-neutral — projections/briefings/pull-reads need NO translation.
Tool-activity detail already crosses the gateway as ACP updates and
could be RECORDED into the ledger (neutral, both harnesses identical) —
candidate addition to workflow-features. Harness-native session files
(Claude JSONL, codex rollouts) = vendor cognition-format; cross-model
translation of those is a FUTURE FOLLOWUP (Flynn), likely never needed
given the neutral layers above. Substrate-never-thinks split holds:
mechanical verbatim projection = substrate verb; semantic briefing =
agent-authored artifact, content-hash pinned to the assignment.

2026-07-20 — OBSERVABILITY DIRECTION RULED (Flynn): ticket-as-view, not
ticket-as-object. No ticket table, no state machine, no transitions —
work state is DERIVED mechanically from substrate facts (assignments,
attests, supervision stamps, verification filings); agents produce
facts, humans and dashboards consume views, nothing writes state as a
separate act from doing work. Janus's pathology diagnosed: a second
copy of reality maintained by agent labor across a seam cut ACROSS the
work-state dependency; the correct seam is truth vs presentation.
DERIVED-STATE EVENTS (Flynn's design): same wire protocol as chat —
chat events interlaced with typed derived-state events (emitted on
mechanical state-EDGES in the task domain, e.g. active→stalled, not
per atomic verb). Consumers filter per connection: a kanban subscribes
to state events only; clawline renders chat primarily AND interlaces
state events between bubbles (work progress inside the conversation).
Precedent: the existing marker messages (context-reset/turn-failed/
fallback) are proto-derived-state events — this generalizes them into
a first-class event class. Derivation is substrate-legal because
MECHANICAL (SQL-grade projection; judgment stays out). Spec when
queued: observability-v1 (event taxonomy, filter contract, derived
status function, board reference consumer). Durable work-item object
(identity across re-staffing; title + spec ref, no state) deferred
until needed. Janus: prodder retired by supervision; tracker concepts
rebuilt as views/statutes/check-tier atop attest; no bridge, no second
brain; kanban/export tooling becomes wire consumers.
  Refinements (Flynn, same conversation): derived-state events are THIN
  — UI-update triggers only: {ref, from-state, to-state, cursor}, no
  payload. Detail views ("the ticket") are random-access queries
  against the tables at click time (assignments/attests/wire-log).
  Consumer contract = three primitives: QUERY (random access), STREAM
  (filtered thin deltas, cursor-stamped), CURSOR (the join; subscribe-
  then-snapshot, discard ≤ high-water). Thin events are self-healing:
  duplicates/latecomers trigger idempotent refetches of table truth —
  the stream can never become a second drift-prone copy of state.
  Precedent: clawline already does snapshot+subscribe for chat.
  Boundary principle made explicit (same conversation): the substrate
  absorbs exactly the facts it must WITNESS to perform its own duties,
  and nothing more — assignments/attests are substrate because
  supervision's predicate needs them, not because ticketing wants
  them; priorities, sprints, dependency graphs, descriptions-for-
  humans, board columns stay product-layer. Janus was this concern in
  exile, mailing itself updates; orthogonality survives relocated to
  the truth-vs-presentation seam (either side evolves without
  synchronization labor — the test the runtime-vs-tracker seam failed).

2026-07-20 — CODEX-GATES POSTURE + OBSERVABILITY GRAIN, RULED (Flynn):
CODEX-GATES: the bar is "works for agents with NON-MALICIOUS INTENT."
It is RAILS, not security. We do NOT defend against a malicious config
rewrite or a faked attestation signal — same as Claude rails, which
were never hermetic either. Spawn-attestation is retained but as an
OPERATIONAL WIRING-CHECK (did the hook load? — catches the silent
misconfig that would let a COOPERATIVE agent flail and run a forbidden
command), NOT a tamper-proof security guarantee. Matrix row: "enforced
for non-malicious agents." The r2-review's three "CRITICAL" findings
were against a security threat model we explicitly do not address; they
dissolve under the honest bar.
OBSERVABILITY / KANBAN: tightbeam does NOT decide what a "card" is —
that is VIEW-SIDE semantics and the substrate has no business modeling
it. Neither "assignment is the card" nor "work-item is the card." The
substrate exposes BOTH model entities (assignments AND work-items)
RANDOM-ACCESSIBLY (queries), plus thin change-doorbells; the VIEW
(kanban / stream-widget / an unsolved 20k' view) picks its grain and
queries. Flynn's load-bearing point: a board is FUNDAMENTALLY RANDOM
ACCESS — it needs "all current work + state, now," which comes from a
QUERY, never from reconstructing a stream; events only say "re-query
this." Product context (why the substrate must stay grain-agnostic —
the right view is not yet known): kanban is "too mechanical — like
looking under the hood to check if the steering wheel works when
turning the wheel would tell you"; Flynn's stream-widget (newest
ticket-change inserted left in a horizontally-scrolling list, deltas
summarized on top) shows live action well but still lacks the 20k'
overview; the 20k' work view is an OPEN product problem. A substrate
that committed to a card grain would bet on a view not yet designed.

2026-07-20 — RESTATE DE-SCOPED FROM THE TRIGGER STORY (Flynn). The
"external wake engine" seam was never "tightbeam needs Restate to fire
wakes" — it is "tightbeam exposes a wake API ANY external caller can
call" (a script, cron, CI hook, webhook, or Restate — all just
callers). Restate is a DURABILITY engine, not a TRIGGER engine, and for
"when X wake Y" it is a needless intermediary: (1) if you must write the
condition-checker anyway, it calls tightbeam's wake API DIRECTLY —
routing detect→Restate→wake adds a pointless hop over detect→wake; (2)
durable TIME is already covered — tightbeam's SQLite wake store dueAt
rows survive gateway restarts and the recovery sweep re-arms overdue
wakes; Restate's timer would only fire back into tightbeam anyway (and
can't deliver while tightbeam is down, which tightbeam already handles
on restart); (3) durable EVENT resolution IS just "external thing calls
the wake API" = the seam itself. The RICH/deep triggers (X = a
condition or script result) are NOT Restate's department at all — they
come from tightbeam's OWN edges (turn-terminals/supervision, the probe
subcommand, statute facts over the ledger, retirement edges) or from
external code calling in. Restate earns its weight ONLY for durable
multi-step ORCHESTRATION where the EXTERNAL WORKFLOW ITSELF is a
long, crash-sensitive saga (do A, await approval, then B, retry C with
backoff, compensate) — a different problem than "when X wake Y", and
even then it ends by calling the same wake API. RULING: keep the
open, caller-agnostic wake API as the external seam; the wake store
stays SQLite behind a durable-timer API (the "Restate-shaped" seam from
2026-07-16 remains, so a durable-execution backend CAN slot in later);
Restate is de-scoped from triggers, filed as a maybe-someday tool for
durable orchestration only. Supersedes the "start SQLite, evaluate
Restate later" framing to the extent that framing implied Restate was
the intended wake backend — it is not; SQLite + the caller-agnostic API
is the design, Restate an optional orchestration add-on if ever needed.

2026-07-20 — KUNGFU INCLUDES RAILS TOMLs (design note for the kungfu
spec; Flynn). The ruled kungfu content model was archetype+guidance+
skills; EXTEND it to also carry a school's `rails/*.toml` STATUTES, so a
school ships its ENFORCEMENT (gates/halts) not just its roles+playbook.
Mechanically trivial: statutes live at identity/rails/*.toml and kungfu
already copies into identity/ — rails is just one more subtree the
`learn` copy includes. This makes a kungfu school the WHOLE GRAPH: nodes
(archetypes) + edges (dispatching skill) + gates/halts (rails toml). SAFE
by existing properties: (1) inert until learned; (2) DENY-ONLY
composition — an imported statute can only TIGHTEN, never grant, so
importing deny-only law is structurally safe; (3) provenance-stamped,
operator-owned fork after. ONE addition vs skills/guidance: the `learn`
ceremony must SURFACE shipped rails for operator CONSENT (law deserves a
look before install, even deny-only). BOUNDARY (automatic via the
constitution/statute line): kungfu may ship STATUTES (deny-only TOML
data) but NEVER constitution/substrate law — constitution isn't a file,
so it isn't shippable; only the statute half is data, and it's the
shippable-safe kind. Ties to the graph-engineering ruling: "graph
engineering = kungfu authoring" now includes the enforcement layer, so a
school is trustworthy on adoption, not just staffed.

2026-07-20 — CONSTITUTION-PLACEMENT DISCIPLINE (Flynn; belongs in the
bible §Law). Over-constitutionalizing is the DANGEROUS failure
direction: a misplaced statute is fixable by editing data; a misplaced
constitution is baked into code, immutable to operators, and silently
makes the substrate unusable for anyone whose process differs. So the
bias is WHEN IN DOUBT, STATUTE. The mistake that prompted this: "only
the owner merges to main" was momentarily called constitution — it is a
STATUTE (operators differ on merge policy; it is literally Flynn's own
CLAUDE.md org policy).
PROCESS (three layers):
(1) LITMUS + default: "could a sane operator reasonably want this
DIFFERENT?" yes → STATUTE (data). no — it is what the thing structurally
IS, incoherent otherwise → CONSTITUTION (code). Default when unsure =
STATUTE; constitution must EARN its place, statute is the presumption.
(2) CATEGORY BARS: structural invariants (typed seams, no-void Mains,
deny-only-composition-itself, exactly-once counting, can't-act-as-a-
role-you-don't-hold) → constitution. Security/privacy/integrity → strong
constitution case BUT still apply the litmus — earns constitution only
when STRUCTURAL (credentials never copied; a session can't forge a
principal), not merely security-FLAVORED (no-self-verdict is a statute).
Dev process / workflow / org governance (who merges, force-push, review
pipelines, required proofs) → STATUTE ESSENTIALLY ALWAYS; a hardcoded
guard enforcing a WORKFLOW is a RED FLAG / likely bug.
(3) REVIEW GATE + PERIODIC AUDIT: every spec adding a hardcoded
substrate guard/refusal must CLASSIFY it (structural / security-
structural / policy); the adversarial reviewer runs a standing
"constitution audit" lens — policy-in-code is a BLOCKING finding
("belongs in a statute"). Periodically re-audit what is ALREADY
constitutionalized to catch pre-gate creep (same pattern as the
2026-07-20 harness-matrix reality-audit). Corrects the statute-engine
spec's "hardcoded guards are FINISHED law not debt" framing: TRUE only
for genuinely-structural guards; a hardcoded POLICY guard IS debt.

2026-07-20 — CONSTITUTION-CREEP AUDIT RESULT (@ 5770d7c): tightbeam is
APPROPRIATELY MINIMAL, NOT over-constitutionalized. Load-bearing
governance is already DATA (check-tier=statutes; prod cap=config
max_live_sessions_per_user; model pins=config). Hardcoded guards are
overwhelmingly STRUCTURAL or SECURITY-STRUCTURAL (provenance + a single
admin privilege axis). Only ~4 LOW/LOW-MED policy-in-code creep points:
(1) skill-LIST is admin-gated though it's a pure read and inspect
already shares org shape to all members — make it a member read; (2)
arbitrary text limits (2000 subject/note, 64 verdictKind, 200 idem-key)
baked as CHECKs — make config defaults; (3) adapter_coordinator tuning
numbers (load_active<3, failures>=5 circuit) — config defaults
(defensibly substrate-health); (4) PHILOSOPHICAL BOUNDARY needing a
Flynn ruling — process principals are barred from assignment/work-item
verbs; today STRUCTURAL (the accountability DDL openedByUser XOR
openedBySession can't store a process as accountable opener), but the
CONSTITUTION has thereby decided "automation is never an accountable
actor" — confirm intended vs accidental (a sane operator may want CI to
file/attest work). RIGIDITY OBSERVATION (not creep): admin is the ONLY
privilege primitive — no delegation (a "librarian" or "device-manager"
role can't be expressed); coarse, becomes a real limit if orgs diverge.
FOLLOW-UPS queued: fix creep 1-3 (small); ruling needed on 4; consider a
delegation/role-privilege primitive later.

2026-07-20 — CONSTITUTION-AUDIT ITEM 4 RULED (Flynn): the process-
principal bar on assignment/work-item verbs is CORRECT, PRINCIPLED, and
needs NO schema change. Automation that must be ACCOUNTABLE for work is
modeled as an AGENT (a session — e.g. a `ci`/`cron-bot` archetype),
which files/attests as openedBySession, already fully supported. The
bare `process` class stays the deliberately-anonymous, non-accountable
class (substrate machinery + identityless external triggers; the closed
"wake and cancel own wakes only" power). WHY PRINCIPLED not arbitrary:
accountability REQUIRES an identity, and having an identity MAKES you an
agent, not a bare process — "accountable process" is a contradiction
(the only reason to be a bare process is to have no session/home/owner,
which is exactly what makes you non-accountable). So the constitution
barring processes from accountable work correctly reflects "you can't be
on the hook for something without being someone." Ties to the
trigger/worker split: a cron TRIGGER is process-grade (a wake); the
WORKER it wakes is an agent (accountable). No third opener class; the
accountability schema (openedByUser XOR openedBySession) stands.

2026-07-20 — BOUNDARY RECORDED: tightbeam is a SUBSTRATE, not a
personal-assistant runtime. This is the governing axis for the recurring-
personal-task question ("every day at 2 clean my email", "weekly clear my
caches") and for anything that smells like product automation.

WHAT TIGHTBEAM IS ON THIS AXIS. Tightbeam exposes neutral primitives and
nothing about any one product's automation model:
  - a caller-agnostic WAKE primitive (dueAt single-fire; recurring is a
    thin re-enqueue over the same primitive),
  - the SESSION/AGENT identity model (accountable openers with home,
    owner, role),
  - the DISPATCH chokepoint with STATUTES (deny-only law),
  - WORK-ITEMS + the CHECK tier (durable feature identity, verdict facts),
  - the ACP seam (neutral harness boundary),
  - KUNGFU (inert, learnable template/rails bundles).
None of these know what "clean my email" means. That workflow is a
PRODUCT/projection built ON tightbeam, not a behavior baked IN it.

WHY THIS WAY. A recurring personal task decomposes cleanly onto the
substrate via the trigger/worker split: the schedule is a WAKE (a trigger
— anonymous, process-grade, "when 2am, wake session S"); the actual work
is done by an AGENT (a session whose identity/kungfu encodes the
email-cleaning discipline, fully accountable). Tightbeam ships the trigger
and the identity/kungfu mechanism; the specific discipline is a learned
kungfu template or product config — never substrate code. So "do we
support recurring personal tasks as well as X?" is the wrong question:
tightbeam supports the PRIMITIVES that let a personal-agent product do
this better than a baked-in runtime can, because the product owns its
task catalog, cadence policy, and presentation while the substrate stays
neutral and reusable across products.

ANTI-PATTERN (what we are deliberately NOT). A runtime that bakes one
product's automation model into the daemon — hardcoded cron/task-list
semantics, a fixed personal-assistant orchestrator, product policy fused
with neutral truth — becomes rigid and unusable for any other product and
conflates substrate truth with product decisions. Tightbeam refuses that:
if a capability looks like product automation, task cataloging, cadence
policy, or presentation, it lives in a product ON tightbeam (composed from
wakes + agents + kungfu), not in the substrate. When unsure whether
something belongs in the substrate, apply the projection boundary: the
substrate exposes truth, material, and generic capability; the product
owns its artifacts, thresholds, cadence, and presentation.

2026-07-20 — RESERVED ORIGIN `process:tightbeam` (supervision r20, ruling).
r19-review found the atomic-fire selector (origin==process:tightbeam) was
not exclusive: external callers could forge that origin via `asProcess:
"tightbeam"` on the org-CLI wake path. Between the reviewer's two options
(add an independent provenance field on the wake row, or reserve the
origin), RULED: reserve the origin. RATIONALE: minimal (no schema change),
and it's a genuine INTEGRITY invariant, not a policy tunable — the
substrate's own canonical self-name must not be externally attributable,
exactly as one session cannot forge another session's identity. So this is
CONSTITUTION-level (identity/namespace integrity), and it's the smallest
possible form: exactly ONE reserved name (`tightbeam`, the string the
supervision closure emits); every other process name attributes normally.
The router's two `asProcess` acceptance points return 403 reserved_origin
for that name. Makes origin==process:tightbeam a trustworthy
supervision-provenance marker by construction. NOT taken: the provenance-
field alternative (heavier, embellishment given the reserved-name fix
suffices).

---

## 2026-07-21 — Enforcement, adjudication, and guidance rulings (Flynn)

Dated provenance only; each ruling's NORMATIVE home is the named spec.

- **D1, enforcement direction = HYBRID.** Predicates stay the always-on hot path; contained
  value-returning scripts are added. Decided via the conformance-smoke-set directive
  ("include script execution in guards"). Normative: `rails-mechanism-v1.md` (I1).
- **Independence is enforced as CROSS-HARNESS** (author harness ≠ producer harness) — the
  enforceable form of cross-model; catalog model-ids stay opaque. Normative:
  `p3-observables-producers-v1.md`, `rails-mechanism-v1.md` §C1, guidance spec §6.
- **Commissioned-reviewer-only anti-laundering:** independence facts read only verdicts on a
  linked review assignment whose holder is the verdict author and whose creator is not the
  producer. Normative: `p3-observables-producers-v1.md` (invariants 6/6b).
- **Producer commands are committed config** (`producers.toml`), never verb params; the fact
  records the command. Normative: `p3-observables-producers-v1.md` §5.
- **v1 execution is gateway-host-only** for rail scripts and producers; remote-holder
  execution is a named deferred gap. Normative: `rails-mechanism-v1.md`,
  `p3-observables-producers-v1.md`.
- **Model adjudication = inference at EVERY edge** (spawn + each classified failure); the
  archetype's ordered model list is PREFERENCE DATA, never a substrate-walked chain; the
  substrate ships classification/routing/fail-loud only. **Quality floor: block rather than
  degrade** ("I'd rather block than switch to haiku because it's all that's available");
  every block is a recorded decision, never silent. Normative: `model-ringdown-pattern.md`
  (the model-adjudication pattern), `model-selection.md` guidance (spec §4).
- **Wake-on-fact (S1):** wakes due on a condition fact, one primitive for parked blocks,
  gate-waits, and external events; delivery is not resumption; permanent-block = not
  subscribing. Normative: `wake-on-fact-v1.md`.
- **Escalation (E1) ruled:** an escalation is a RESUME — a slow dependency inside the
  raising agent's assignment (parked on a condition wake for the decision fact; the
  substrate never auto-replays; execute-once). No blocked-on-owner state or flag. Rulings
  are per-request plus the WAIVER ("ignore that rule for now"), a recorded fact scoped to
  the raiser's lifetime or revoke — and a §6g false-positive datapoint for tuning. The
  raiser may withdraw its own requests, recorded; retirement auto-withdraws. Normative:
  `escalation-substrate-v1.md` (rewrite in flight at ruling time).
- **G1, the manual is the patterns:** the always-on substrate manual is the
  operating-patterns document (situation → move, one exemplary command each); mechanics
  belong to `tightbeam --help`. Capture pipeline: every ratified spec answers "what pattern
  does this teach?" or amends the manual with the spec. Normative: guidance spec §2
  instruction + the reviewing-specs/spec-handoff skills.
- **Docs hierarchy reaffirmed:** specs are the primary, load-bearing record of every
  decision; this ledger is provenance; the roadmap is tracking/posterity and is never a
  decision's only home.

## 2026-07-21 (evening) — The enforcement spec lattice reaches READY

All six specs passed iterative cross-model adversarial review (Sol-high reviews; Opus
authors; Fable rulings), each to an explicit READY verdict:
- `model-ringdown-pattern.md` (model adjudication) — 11 rounds.
- `wake-on-fact-v1.md` (condition wakes, S1) — 7 rounds.
- `escalation-substrate-v1.md` (E1, Flynn's ruled resume/waiver model) — 6 rounds.
- The enforcement trio, READY-FOR-IMPLEMENTATION together — `rails-mechanism-v1.md` (r10),
  `p3-observables-producers-v1.md` (r7), `enforcement-smoke-set-spec.md` (r9, 66 fixtures).
Roadmap Wave 0 (spec authoring) is complete; Wave 1 (implementation) dispatches under the
Fable-conservation topology (Sol codes, Opus reviews, Fable on rulings/gates), opening with
Fable's personal architecture pass in fresh context.

## 2026-07-21 (night) — Whole-lattice gate closed: LATTICE-READY

Flynn ordered a whole-lattice consonance pass: one Fable and one Sol-xhigh review of the
six-spec ensemble, with Fable triaging the critiques for YAGNI/overengineering ("hole"
means conceptual hole). Outcome:
- Hunt round: Fable HOLES(9) + Sol HOLES(15), core-five agreement. Accepted holes routed
  to the four spec authors + smoke; rejected-as-overengineering: unified org-config
  contract, per-predicate pass recording, generic park helper, episode coordinator,
  `action="produce"` now, remedy auto-provisioning, `*_in_txn` framework (doctrine
  paragraph instead).
- Re-verify round: Fable HOLES(1) (one stale smoke row), Sol HOLES(7) (two stale reads of
  the same row, five live). The one true CONCEPTUAL hole: the model-park
  already-recovered branch cancelled the wake but left the arm-and-enqueue transition
  with no driver — fixed: the cancel branch performs the exact W6-fire write (enqueue
  recovery turn + arm filter) in the same transaction as the cancel; cancel-vs-fire is
  arbitered by the wake-row CAS, so exactly one driver ever runs. Also closed: additive
  `identity_manifest_sha` in the §E1 denied payload + `rail_denials` projection
  (unbackfillable seam); assign-to-bound-role wording unified across roadmap/smoke
  capstones; smoke world gained the seedable open `adjudication_episodes` row (the row is
  the suppression key; `sessions.adjudicationHold` is the claim filter); produced-fact
  capstones compose deny+re-obligate, no C6 remedy.
- Final bounded confirmation (Fable reviewer, all eight edit sites): **LATTICE-READY** —
  all three end-to-end traces (reviewer loop, quota park, escalation) walk clean.
Smoke census at close: 72 fixtures (r10). Wave 1 gate is OPEN: Opus coordinator stands
up; catalog-redo is the first lane (thrice-proven dependency; includes the
`fallback_models`→`model_preferences` rename and the catalog freshness contract).

## 2026-07-22 — The accountability constitution (first in-substrate org test)

Flynn ran the playground org on real work (picker duplicates; rename/delete 404s). The
org shipped both fixes end-to-end (commits 82a6560, cbc8d2e, 8a0ba21, 074d525 — its own
review, its own gateway deploys) and surfaced three incidents that produced a ratified
constitution, canonical in `accountability-constitution-v1.md`:
- Silent strand (borrowed orchestrator retired under a second PO) → living-escalation
  guarantee; strand notification; orchestrator exclusivity; borrowing as org LAW over
  substrate relationship facts (chain-of-command ships as default statute).
- Unbooked expectation (operator's own pointer-only dispatch propagated down by example)
  → the expecter opens the card; atomic dispatch verb; NO detector (thresholds rejected —
  unrecorded expectations leave no evidence; close by construction); PO self-assignment.
- Lifecycle ghosts (retired sessions' processes + drawer entries lingering; cascade
  question) → cascade-by-default with loud interruption rows; critical-section lease
  (defer, never veto); retire reaps processes; stream_removed wire event.
Constitutional ruling: assignment-as-capability is a SUBSTRATE rail (mutation requires an
open assignment; read free; self-carding legal — no invisible work, not no autonomous
work). Kungfu cannot waive it. Binding EXISTENCE is physics; binding POLICY is law.
Also ruled: work-items thread down by reference (one item, many assignments); slates not
tickets; spawn needs no work-item (pools legal); session naming law; guidance authoring
doctrine (directives not encyclopedias; frequency decides manual-vs-skill; batch guidance
edits — they tax every live session's memory).

## 2026-07-22 — GAP-1 ruling: the error catalog is opportunistic

LKP1 paused (Sol's third correct refusal-to-guess): harness error envelopes were never
cataloged and the spec forbids guessed classification. Ruled: probe-first is impossible
whole (quota/recovery can't be induced; breaking live auth forbidden) — so the
adjudication engine builds now behind a pluggable classify seam defaulting `other`, with
raw-envelope recording on every `other` so production incidents grow the catalog.
Seeded from the 2026-07-21 codex outage + safe model-refusal probes. Mapping +
quota-recovered producer = fast-follow lane. Canonical in model-ringdown-pattern.md GAP-1.

## 2026-07-22 (overnight/morning) — Constitution completions

Appended to accountability-constitution-v1 and the ringdown rulings, each from an
observed failure or Flynn push-back:
- Guarantee 6, total emission: everything that happens emits toward the client; the
  substrate never curates. (Invisible surrender incident.)
- Three-layer liveness: turn duration unbounded (ceiling DROPPED — it interrupted valid
  work); harness wedges detected by activity staleness (future, as a BACKSTOP to
  orchestrators — agents supervise agents; the substrate supervises that supervision
  happens); work abandonment judged by the patrol. (10-minute ceiling killed a healthy
  PO turn; day-long turns are the trajectory.)
- Respawn transfers office and obligations (roles rebind, assignments re-holder, same
  txn) — respawn is continuation; cascade is termination. Retirement drain reused
  verbatim; standing meta-ruling: unpinned operational defaults match the existing
  substrate pattern, pause only for genuine novelty.
- Medic statute: when a whole authority chain sits on a dead harness, a remedy statute
  spawns a recovery agent on a surviving harness. (Flynn's auto-spawn suggestion,
  initially under-served.)
- No intent in limbo + filing-arms-conditions: work-items gain an owner; filing
  atomically arms the item's two lifecycle brackets — routed-or-deadline (owner woken
  "route or icebox") and concluded-or-adjudicated (owner woken at last-card-close). No
  sweep; the deadline rides the filing txn. (Born from the operator's own idle
  catalog-tooling item.)
- GAP-1: error catalog is opportunistic (engine behind a classify seam; `other` records
  raw envelopes; probes only where safe). Codex 0.144.6 hook-trust regression: rails
  silently bypassed, caught by the fail-closed wiring gate; shim fix (trust flag moved
  to CLI; matcher stays "Bash").

## 2026-07-22 — Design doctrine consolidated

The night's transferable meta-rules (rails-follow-rows, convention-minting, the
guidance→affordance→rail ladder, determinism-brackets-inference, expecter-opens-card,
directives-not-encyclopedias, pause-beats-guess, failures-compost, et al.) are now
canonical in `wisdom.md` — 25 numbered rules with their earning
incidents in this ledger. Doctrine governs how new specs and law get made; specs
govern their own domains.


## 2026-07-22 — Four ratifications (Flynn)

- **Verdict vocabulary is LAW**: `reviewed-clean`/`changes-requested` (review);
  `yes`/`no`/`conditional`/`not-proven` (recon); producer verdict kinds; `verified`
  (user acceptance). Rails pattern-match these exact strings; deviation is a defect.
- **Abstraction promotes at the THIRD use** (supersedes "second consumer") — two uses
  often share coincidental shape; guidance + spec updated.
- **Spec skeleton is CANONICAL**: Goal, Non-Goals, Terms, Assumptions, Invariants,
  Architecture, Acceptance, Open Questions — every product spec carries all eight; an
  explicit "none" is information, an absent section is a defect.
- **Span of control stays GUIDANCE** — no hard spawn cap; the patrol catches the
  symptom; an org-tunable cap statute is addable if org tests show drowning.

## 2026-07-26 — `unreported`: a rail exit class the wrapper cannot produce (Flynn)

Flynn ruled "just do it" on the fabricated rail verdict. `rails-mechanism-v1` §A3/§E1
and invariant I3 are amended.

- **The invariant I3 already stated — «the substrate never guesses a value for a check
  it could not complete» — was unenforceable, not merely unenforced.** Every value the
  rail path invented COLLIDED with a legitimately observable one: a synthesised exit 20
  was byte-identical to a wrapper that really timed out, and an invented `error:1` was
  byte-identical to a script that really exited 1. Nothing downstream — consumer, test,
  or reviewer — could tell them apart, so the invariant held only by the good intentions
  of whoever last edited the path.
- **RULING: reserve a class the wrapper cannot emit — `unreported` — and write it
  wherever a deny is reached without the observation that names it.** Four paths: the
  port never reported, the child's exit code was never seen, no script was spawned
  (unresolvable invocation context), the substrate itself crashed. `unreported` is
  disjoint from the parameterised `error:<N>` (always digits), so its presence is proof
  no verdict was observed and its absence is proof one was.
- **`reason` is untouched at every site.** Fail-closed semantics and every reason-reading
  consumer stay as they were; only the exit class splits. `error:<N>` already being
  parameterised is the precedent for a structured value in that column.
- **The wrapper is bound by the same rule on its own side of the seam.** `rail-exec`
  writes `tightbeam rail-exec child exit: <N>` only for a child exit it observed. Its
  stdin-delivery failure — the script never received the call it was to judge — used to
  print that line with a made-up `1`, on the side of the seam the substrate cannot
  second-guess, which made it the worst of the four.
- **This is what discriminates the two producers of `script_timeout`.** The BEAM-side
  `duration_ms` cannot: it is measured in the calling process, so a starved caller
  inflates it past `timeout_ms + 2_000` on a run the wrapper genuinely enforced (pinned
  by a real-binary starvation test). `timeout` vs `unreported` is the recorded fact, and
  the C5 evidence surface now names the layer from it.

**Transferable:** an invariant of the form "never invent X" is only checkable if the
value written when nothing was observed is outside the range of values an observation
can produce. Reserving that value is the cheap half of the work; the expensive half is
noticing that "fails closed" and "says what happened" are different properties, and that
passing the first is what makes failing the second invisible.

## Containment is per-OS, and so is the obligation to prove it (2026-07-27)

`Containment` shipped as "macOS Seatbelt profile rendering" while linux was a
supported gateway target, and `contain.rs` spawned `/usr/bin/sandbox-exec`
unconditionally. On linux the spawn failed, so every rail check returned
CONTAINED_REFUSED: statutes and gates were inert on every linux gateway. It
failed closed, which is exactly why nobody noticed — and the suite had never once
been executed on linux, so a green macOS run was reported as a green suite.

Decisions, recorded in full in `tightbeam-containment.md`:

1. **The neutral truth is the set of write roots.** SBPL is macOS's encoding of
   it. The renderer (`rail_profile/1` for a rail check, `adapter_profile/1` for a
   contained adapter) stays the sole authority on which roots are granted and
   renders per-OS; the wrapper applies what it is handed.
2. **Landlock, not bubblewrap, for linux.** Decisive reason: Landlock is applied
   inside our own process, so "containment was not applied" is a syscall return
   value rather than an exit code to be inferred — CONTAINED_REFUSED becomes
   exact, better than the macOS exit-65 sniff. It also needs no helper binary and
   no user namespace, and adds no PID namespace to the layer the timeout and
   killpg behavior is pinned on.
3. **ABI floor 3 (kernel 6.2), and a host below it refuses.** Below ABI 3
   `truncate(2)` is unrestricted, which is a write outside the write roots. A
   host that cannot deliver the guarantee refuses rather than under-enforcing.
4. **A test double must not contain on one OS and not the other.** The rail-exec
   fixture's contract is the exit bands; it stopped interposing `sandbox-exec`,
   and the one rail test that asserted a denied write moved to the real binary,
   where enforcement can actually be proven.
5. **Both platforms gate.** A suite that passes on macOS and has never run on
   linux is an untested build, not a passing suite.

6. **A rail profile is not a harness profile** (added after spec review found the
   hole the parity work had inherited). `containment_additions/0` — grants for a
   *harness's* runtime needs — was appended to the single renderer rails and
   adapters shared, so a harness grant widened the rail write wall. On linux that
   grant was `/dev`, and `/dev/shm` is world-writable tmpfs: a durable write
   channel out of the scratch root, measured PASSing on shrdlu. The seams are now
   named separately (`rail_profile/1`, `adapter_profile/1`) so a caller must say
   which wall it wants; rails keep exactly one fixed grant, `/dev/null`, because
   `>/dev/null` is in shipped rail scripts and a discard sink carries nothing out.
   Narrower than before on both platforms.
7. **Fail-closed is only half of it.** A refusal has to name its cause on a row
   that outlives the run. The wrapper's reason was written into the scratch dir and
   deleted with it, so a host refusing every rail recorded only the class
   `contained` — the exact shape of the outage above. Fail-closed without a legible
   cause is how a total outage passes for normal operation.

8. **The mechanism's behavior is kernel-dependent, and three same-version hosts
   are not the gate — CI is** (added after the linux CI job went red on the B1
   fix). Granting `/dev/null` — the sole rail grant after decision 6 — returned
   `EINVAL` on the runner. Landlock validates a rule's rights against the target's
   inode type; `TRUNCATE` is invalid on a character device, and the runner's newer
   kernel rejects it where ABI-4 fleet hosts accept it. Fix: mask by three inode
   buckets (dir → full, regular → `WRITE_FILE|TRUNCATE`, device/fifo/socket →
   `WRITE_FILE`), the narrowest type-appropriate set, which holds across kernels;
   `>/dev/null` still works because a device fires no truncate hook. The fleet
   could not have shown this — it is the exact class of gap the all-platforms gate
   exists for, and it is why `tightbeam contain-probe` now prints the ABI and a
   right-by-right grant trace instead of anyone guessing the runner's kernel.
9. **`ETXTBSY` on exec of a just-written script.** Surfaced by the same work: a
   multithreaded parent (cargo's test harness) can fork with another thread's write
   fd to the script still open, so the exec sees it busy. Transient; the contained
   spawn retries on `ETXTBSY` only. The production wrapper is single-threaded at
   fork and does not hit it, but a threaded substrate could, so the retry is real
   hardening.

10. **A verdict may never be read off the party being judged** (code review, Sol).
    macOS inferred "the containment refused" from exit 65 plus a `sandbox-exec:`
    stderr prefix — both of them child output. The same script therefore got band
    30 on macOS and band 10 on linux, so a rail author could read the OS off a
    verdict, and #43's fabrication shape was back. macOS now preflights the profile
    against `/usr/bin/true` before any script exists, and the post-spawn sniff is
    deleted on both platforms: refusal is decided before the fork or not at all.

    Worth contrasting with entry 12, because it is the ruling in entry 11 being
    applied rather than merely stated: this one is IN scope and that one is not.
    Nothing here needs a hostile agent — an honest check can emit those bytes by
    accident, and the platform divergence is a legibility defect on its own. A
    finding that only bites when an agent is deliberately hostile does not clear
    that bar.
11. **Containment keeps agents on the rails; it is not a security boundary**
    (Flynn, standing ruling, stated repeatedly before this lane). A circumvention
    requiring an agent to be deliberately hostile is out of scope. A hardening
    earns its place on parity, correctness, or legibility grounds, or not at all —
    and a security-shaped BLOCKING finding is a claim to weigh against this, not
    automatically work. Recorded in `containment.ex`, `contain.rs`, and the spec,
    because it was violated: a symlink-swap race was raised as BLOCKING, actioned
    without weighing it, and cost a round.
12. **Validation and enforcement agree on the path.** Grants resolve via
    `openat2(RESOLVE_NO_SYMLINKS)`, so the wrapper attaches the rule to exactly the
    path Elixir validated — `O_NOFOLLOW` guards only the trailing component, and
    under `O_PATH` not even that. This is kept on that correctness ground alone:
    the swap race it also closes is out of scope by entry 11, it was never an
    escalation for rails (the swap needs write access outside every rail's root,
    which only already-uncontained processes have), and it stays only because
    `openat2` is kernel 5.6 — below the ABI-3 floor — so it costs nothing. Not
    precedent.

Independent of the platform gap, and found by it: the wrapper raced the child for
delivery of the input a check judges. macOS won that race by accident because
`sandbox-exec`'s startup delayed the script. The pipe is now filled before
anything is spawned.

Adapter containment (`placement.ex`) is deliberately still macOS-only argv: it is
unreachable while every adapter key is `"shared"`, so it is dead code rather than
a live defect. Whoever enables it owns making its applier per-OS (task #36). The
profile it would pass is already correct on both platforms.


## `adopted` acquires a meaning, and the wire acquires `startedBy` (2026-07-29)

`adopted` arrived as an inherited TS-reference column: on the wire, DEFAULT 0, no
writer anywhere, no definition in any spec — a field the client could read and
nothing could ever change. Flynn's ask fixed what it is: chat-list membership,
so agent- and substrate-started sessions can exist without burying the human's
own conversations, adopted into the list by a `tune` write when the operator
wants one. `startedBy` came with it because the alternative was every client
parsing origin prefixes, which puts opinions about a closed set (T3) in the one
place that cannot be amended by a spec change. OPEN, deliberately not decided
here: `adopted` is one boolean per session, not per user — right while
multitenancy is family convenience, wrong the day two humans share a catalog.


## Artifact-record carrier: fail open with evidence classes (2026-07-29)

Clauses 8/11's exact-firing-turn demand was proven unsatisfiable by any
mechanism: no per-turn gateway→agent channel exists, and an agent-filled wire
field is forgeable — even C1's own named remedy was not constructible. Flynn
ruled per artifact-carrier-proposal-v1: artifact recording FAILS OPEN (a
correct agent is never trapped in an unsatisfiable completion loop);
`recordedMessageId` becomes nullable paired with `recordedTurnEvidence`
(`tool-call-observed` | `session-concurrent` | `none`); `tool-call-observed`
is an observation-quality claim from the PreToolUse hook seam, never an
unforgeability claim; caller-supplied provenance stays stripped; the
artifact-kind completion gate is preserved; clause 12 stays separate and open.
Clauses 8/11 and the C1 wire-carrier note are amended to require the best
substrate-observed edge plus its evidence class, with the former exactness
language recorded as unsatisfiable rather than closed. Gibson activation is
gated on the carrier repair passing independent review plus the full named
gate: T1; T2a artifact-record + completion-gate closure on BOTH claude and
codex; codex live hook proof; T3 satellite observation across the network hop;
revert of shrdlu org-law workaround eb0ea2b; both-platform scorecards with no
waiver hiding a failed load-bearing leg.

## 2026-08-04 — Surf Ace integrates as a SKILL, not an archetype

Flynn, on discovering an orphaned surf-ace-controller archetype in a dead
worktree: "we threw that idea away. ANY agent should be able to use the surf
ace cli, so we decided it was a skill not an archetype."

The archetype shape was the discarded half of an already-made decision — it
would have dedicated a session identity to Surf Ace and (as written, with
`where ["*"]`) placed a controller on any host, against the standing rule that
Surf Ace provider identity lives on TARS only. The kept half: Surf Ace
capability reaches agents as a skill any archetype can elect, using the CLI.
The orphaned files (archetype TOML, skill, projection test) were deleted with
the small-lane worktree; nothing on any branch carries the archetype design.

## 2026-08-05 — Adjudication is DELETED. Model policy is guidance, not substrate.

SUPERSEDES the narrower ruling recorded below on the same day (which kept the
machinery for agent-to-agent use — still substrate policy, and wrong).

Flynn: "there should be a markdown/guidance that describes what models are used
for which tasks, and if those models aren't available because either they're not
configured, or have run out of tokens, an AGENT should make that decision and
then spawn the appropriate agent when necessary, or refuse. This is NOT the
substrate, it is an agent. Inference makes the decision. Why is the substrate
making a model selection?"

THE SPEC ALREADY SAID THIS AND THE IMPLEMENTATION IGNORED IT.
`model-ringdown-pattern.md` records that r1/r2 built a substrate-driven fallback
chain, and that "r3 deleted that under Flynn's 'inference at every edge'
reframe", stating: "Model choice is judgment, so it is done by inference — an
adjudicating agent — never by a substrate mechanism." What then shipped (77aa24c,
"LKP1: model-adjudication engine") was: an adjudication_episodes table with a
guarded CAS lifecycle, sessions.adjudicationHold, a lineage escalation ladder,
deterministic owner + recovery wakes, a boot reconciler, an adjudicate verb
(park|swap|respawn|stop), preference chains and condition classification. The
substrate does not pick the model — it owns every mechanism AROUND picking it:
who is asked, in what order, what blocks meanwhile, what happens on timeout.
That is fallback policy in the substrate, which the boundary in CLAUDE.md
assigns to the product, and which the pattern's own first sentence forbids.

RULED: the substrate owes exactly three things when a model or engine cannot
serve — (1) TRUTH: catalog contents, health, exhaustion, routability, queryable;
(2) a NAMED FAILURE: this turn did not run, this is precisely why; (3) a RECORD.
Nothing else. No hold, no episode, no ladder, no ruling verb, no preference
chain, no classification taxonomy.

Model policy lives in GUIDANCE — markdown in the identity tree naming which
models suit which work, and what to do when one is unconfigured or exhausted. An
agent reads the failure, reads the guidance, and acts: choose another model,
spawn a different agent, or refuse and say so. This needs no substrate support
beyond a good error message.

Delete: Tightbeam.Adjudication and its table, sessions.adjudicationHold and every
reader, the adjudicate verb (server handler and the half-wired CLI arg — args.rs
names it, dispatch.rs never routes it, which is why the brief instructed users to
run a command that does not exist), the owner/recovery wakes, the escalation
ladder for adjudication, the boot reconciler, and the heal machinery whose only
job is releasing holds. Keep: the turn failing by name, the [turn failed] marker,
the lifecycle record — all three already work and were hardened 2026-08-04/05.

## 2026-08-05 — (SUPERSEDED, kept for provenance) Adjudication does not ask. It fails, tells, and records.

Flynn, on being shown a held session with three queued prompts: "why is it
asking stupid questions? it should immediately fail the operation and send a
message to clawline and/or record it." Preceded by "i don't know what
adjudication is for!" — from the product owner, which is itself the finding:
the mechanism accreted without a decision behind it.

RULED: a model or engine failure that the substrate cannot resolve FAILS THE
TURN, publishes the reason to the client, and records it. It does not hold the
session, does not open an episode, does not await a human ruling, and does not
ask the user to choose between park/swap/respawn/stop.

The principle adjudication was built to protect is KEPT and is not in dispute:
never silently substitute a different model for the one that was asked for
(harness/claude.ex refuses near-miss substitution for the same reason). Failing
loudly satisfies that principle. Freezing the session to ask permission does
not add to it — the user re-selects a model or retries through the ordinary
product surfaces, which is a decision they make by USING the product rather
than by answering a prompt about it.

What this deletes: the session hold (`sessions.adjudicationHold`), adjudication
episodes and their claimed/notified/resolved lifecycle, the owner-ruling wake
and its brief, the `adjudicate` verb, the escalation ladder for adjudication,
and the heal/reconcile machinery that exists to release holds. What it keeps:
the turn failing by name, the `[turn failed]` marker in chat, and the lifecycle
record.

Evidence that motivated it, all from gibson's first production days: the brief
instructed the user to run `tightbeam adjudicate`, a command the CLI does not
have; no client surface shows a session is held, so prompts queue invisibly; the
hold did not release when its cause (a missing credential) was fixed hours
later; and the only production case it ever fired on was one where the correct
answer was "tell them to log in" — since fixed by refusing that turn by name.

Consequence for T-CONSPICUOUS: a failure the user can see and act on replaces a
question they were never able to answer.

## 2026-08-05 — The substrate is a production machine; production-machine-v1

Flynn, same session as the adjudication deletion, generalizing it: "we are
supposed to be creating a Newell production engine and the substrate does the
right thing against whatever the current state of the system is... the
substrate should never be the one WAITING."

Ruled, recorded in production-machine-v1.md (which supersedes the mechanism
half of model-ringdown-pattern.md):

- The substrate is a recognize-act cycle over durable working memory. No
  substrate state may have someone else's decision as its exit condition.
- Standing state is DERIVED from the append-only condition-fact stream (latest
  of an assert/retract pair), never stored as a mutable flag.
- "Stop treating this session as stalled" is an agent-asserted fact
  (`work-blocked`/`work-unblocked`), forbidden to the substrate, never gating
  the turn queue. The prodder does not check it as a flag; the prod
  production's declared LHS stops matching.
- Fault bubbling is proof-driven: a notice to a parent is a turn, its
  delivered/failed terminal state is the only evidence of whether that parent
  can act, a failed notice climbs the lineage, and the terminal alert to the
  user is a tokenless clawline wire message that cannot share the failure
  mode — filed as a standing `user-alerted` fact, cleared by the first
  observed delivered turn under that root.
- Formalization is pragmatic but legible: each production's LHS lives in one
  named function over durable state only, moduledocs name the pattern, and
  statute-layer migration is the completion path when a second consumer
  arrives. It must be clear from the code alone that this is a production
  machine.
- Model policy is a guidance markdown read by agents, never by the substrate.

## 2026-08-05 — Subtraction doctrine; review staffing floor; spirit gate

From the adjudication postmortem (attribution: every hand in the r1-r11
spec pipeline and its implementation was gpt-5.6-sol; the one recorded human
intervention was the r3 "inference at every edge" reframe, which the
subsequent rounds absorbed as a headline while rebuilding the forbidden
mechanism underneath).

- Adversarial review without a simplicity adversary is a ratchet. Every
  found hole has three answers — add, DELETE the surface, or accept the
  failure as a named value — and adding is not the default. Shipped as
  kungfu (subtraction.md) for product-owner, reviewer, spec-writer.
- Review staffing is a GRADIENT, floor enforced by rails-shaped law when
  the effort facts exist: different harness > same model higher effort >
  same model, equal effort, fresh context. Mechanically deniable floor:
  self/lineage review, or same model at strictly lower effort. July's
  Sol-high panels pass this floor — the failure was the ratchet, not the
  staffing.
- Spec-backed work does not dispatch without a product-owner spirit verdict
  (shipped statute, deny-that-names-the-paper; minds arrange the review).
- Round-count doorbell at 4 (norm 1-2 + grace; old process ran 4-10):
  escalate-only, shines light on spinning, limits nothing. Staged until the
  rails grammar grows a non-blocking `notice` effect — the named gap.
- Not railed, ever: content judgment. Rails require papertrails and staffing
  floors; minds judge.

## 2026-08-05 — Cleanup never gates capability

Flynn, after the gibson reboot-orphan fence (a harness down ten hours because
an unkillable ghost blocked new spawns): "not having a session to shut down
must never block a session from starting... even if it's still running,
what's the fallout? A token race that at worst requires re-onboarding — an
annoyance. You're moving a mountain for something whose repercussions are an
annoyance at worst."

Ruled: a park fence bounds an OPERATION in flight (the seconds a kill is
actually executing), never a standing state. At boot or close the substrate
makes one best-effort identity-checked kill, RECORDS what it observed
(killed / already gone / unidentifiable-left-behind), drops the dead ACP
connection, and starts the new engine regardless. kill_failed is a note, not
a gate. Key insight: an orphaned adapter is an ACP subprocess whose stdin
died with its gateway — it receives no prompts, runs no turns, makes no API
calls, refreshes no tokens; the guarded-against hazard is a process doing
nothing. Worst realistic fallout of starting anyway: a seconds-wide token
refresh race (revoked grant -> re-onboard), a stale line in a transcript, a
leaked idle process to sweep later. All annoyance-tier; a fenced harness is
an outage.

Companion (same conversation): standing conditions need standing visibility —
a fence/expired credential arms => one substrate-authored line into the
owner's stream at arm time, plus readiness/doctor surface. Dark factory: dark
never meant no instruments.

The 2026-08-05 proof-clauses (never-launched, reboot-orphan) remain as
ledger honesty; the deletion lane removes their load-bearing role.

## 2026-08-05 — Credentials: no tightbeam-owned copy; absence in the home IS
the onboarding signal

From the gibson spawn-refusal postmortem (live home refreshed itself since
02:38; the banked "canonical" copy rotted; the spawn gate judged readiness
off the dead copy while the runtime ran fine on the live one — T-SOURCE's
cache-consulted-as-authority, in the credential seam).

Flynn's derivation, ruled:
- Harness CLIs own their tokens: the credential lives in exactly ONE place,
  the harness home, harness-native format, refreshed by the harness itself.
- No vault/bank. The copy only existed to survive home wipes, and routine
  operation never wipes homes (projection overlay-reconciles law files and
  preserves harness state); wholesale destruction is operator-grade cleanse
  where re-onboarding is expected. Loss = re-onboard = annoyance-tier.
- A from-scratch home (no credential file) IS the needs-onboarding fact —
  world-state drives the signal; onboarding writes into the home directly.
- Present-but-expired is NOT absence: that is OBSERVED health — a 401 names
  the failure, bubbles, and becomes standing visible state. Storage is never
  consulted as authority on whether a credential works.
- One grant, one refresher: never copy a credential into a second live home;
  other hosts onboard their own grants.
- Deploy verification standard: "ready" means a NEW agent spawns and answers
  a turn — not merely that an existing session does.

## 2026-08-15 — Catalog completeness is part of the harness-switching feature (Mike)

Ruled by Mike, recorded via tb02: harness/model switching is NOT done while
the catalogs are thin. The INVARIANT, stated as the feature's acceptance
criterion on every line that ships switching (0.1.8 onward, 0.2):

- **codex** lists all modern OpenAI models — **sol, terra, luna** — at ALL
  thinking levels, plus fast mode.
- **claude** lists at minimum **fable 5, opus 5, sonnet 5, opus 4.8**.

If a model in that set is unselectable when switching is deployed, the
switching feature is still broken — "the harness can't drive it today" is a
defect to fix, not a scoping excuse.

Current state at ruling time: claude MEETS the minimum (fable-5, opus-5,
sonnet-5, opus-4-8, haiku observed on a fresh 0.1.8 install). codex FAILS:
`@adapter_selectable_models ~w(gpt-5.6-sol)` (harness/codex.ex, pinned from
a live 2026-07-28 probe at codex-acp 1.1.4 where every other slug was
refused with -32602), and the sole listed model exposes `efforts: []` — no
thinking levels — and no fast option. The pin is injectable
(`codex_selectable_models`, `:all`) so widening needs evidence, not code.

Work this ruling orders: (1) re-probe the CURRENT codex-acp version for
sol/terra/luna × all thinking levels × fast (the 1.1.4 pin is stale-dated;
harness CLIs auto-update); (2) widen the pin/injection to the evidenced
set; (3) if the current adapter still refuses luna/terra, that is an
upstream defect to chase, not an accepted state; (4) add a
catalog-completeness check to the switching acceptance battery on both
lines. Routed to the 0.1 PO (0.1.8 acceptance) and the 0.2 program.

## 2026-08-16 — Auth-ceremony codes are deliverables, not screen text (Mike)

Ruled after three consecutive S2c failures of identical shape (ceremony
armed, one-time code never reached the operator, expired unseen).

**Discipline, effective immediately, every line:** any agent running an
auth/onboarding ceremony MUST, the moment a sign-in URL and/or one-time
code appears, (1) elevate it to the operator immediately (wake to the
human; open the URL on the operator's browser host per standing practice)
AND (2) file the URL + code as an attest row on its card. Device codes are
short-lived single-use pairing strings, not durable secrets — a code that
expired unseen in a private terminal is an agent failure, full stop. A
ceremony whose code cannot be delivered within a minute of minting is
aborted and re-armed, never left to expire silently.

**Product order (both lines; gate-8 extraction — the discipline above is
the stopgap, the bone is the fix):** `tightbeam onboard` must treat the
URL and code as first-class delivery: capture them from the vendor flow
and (a) emit them as structured output, (b) record them as a substrate
row, (c) notify the operator channel. Delivery must never depend on an
agent reading a pty. Related open defect: wi_e86ddd54 (onboarding parks
the runtime conducting it) — reproduced live 2026-08-16 on shrdlu.

## 2026-08-16 — A release branch EVOLVES until it passes (Mike; supersedes freeze-by-abandonment-at-tag)

Ruled by Mike on the S7 wire-dead-operator-verbs finding, recorded via tb02:
NOTHING lands in 0.1.9 while 0.1.8 is still testing. Fixes for defects found
by release testing land ON THE RELEASE BRANCH (0.1.8) as new builds, and e2e
re-tests the evolving branch — loop until 0.1.8 TESTS CLEAN. Only then do we
stop adding to it: passing is what "calling quits" means. If anything has
landed in 0.1.9 meanwhile, merge it into 0.1.8 and keep evolving. The
successor scratchpad (0.1.9) becomes the active line only after 0.1.8
passes. Mike verbatim: "we evolve a release branch until it passes."

This supersedes the plan clause "tag at becb130 immutable; test failures
produce 0.1.9 fixes, never a tag change" — build numbers identify bytes
during evolution; the final identification happens at quits. Immediate
effect: the S7 router fix (gh#11 operator verbs absent from router.ex
@agent_verbs) lands on branch 0.1.8, S7 re-runs against the new build.

## 2026-08-16 — The loop iterates without permission (Mike: "why aren't we iterating?")

Refinement of evolve-until-passes, recorded via tb02: fixes for test-found
defects land on the release branch AS FAST AS THEY PASS GATES. No
per-iteration operator approval; audits run in parallel with the next
iteration and gate QUITS, not iteration; the successor lane pre-stages so
there is zero idle between one lane going green and the next starting.
Only quits needs Mike.

## 2026-08-16 — Watchdogs check advancement, not just liveness (Mike-caught gap)

Finding + charter rule, recorded via tb02. The 0.1.8 watchdog missed the
post-S7 idle because the stall was MOTION WITHOUT ADVANCEMENT: every lane
was alive and attesting (audits, specimens) while the critical path's next
step (Bug B implementation) had NO CARD — and a missing card is invisible
to a watermark over existing rows. A lawful-looking permission gate in the
plan compounded it. Charter rule for completion watchdogs, this org and the
0.2 fabric's kungfu: each patrol names the current critical-path item,
verifies some lane holds an obligation advancing it, and treats
no-such-card as a stall finding (summon the owner to card it). The prodder
bone still bounds starvation of existing rows; naming the missing row is a
MIND's duty — which is why it lands in the watchdog's charter, not the
substrate.

## 2026-08-16 — Interactive onboarding is DEFINED as incomplete until the operator holds the URL and code (Mike; the saga's answer)

Mike's closing ruling on the S2c saga, verbatim reasoning: the runbook said
only "onboard codex," so agents GUESSED at the task's definition — and
guessed one that did not include the operator. The answer to the entire
saga is runbook explicitness: an interactive auth ceremony's sign-in URL
and one-time code MUST be returned to the user (or the parent that can
reach the user), because the sign-in loop runs through the user — without
the code in the user's hands the user cannot finish, and therefore THE
ONBOARDING IS INCOMPLETE. Not a delivery step bolted onto the task; the
definition of the task. Every runbook, plan step, and card that says
"onboard <provider>" means this full loop: ceremony started -> URL+code to
the operator -> operator signs in -> credential installed and verified.
Anything less is not a partial success; it is the task not done.

## 2026-08-18 — A verdict points at its artifact; the note field is the wrong shape (Mike)

Ruled by Mike, recorded via tb02. The attest note's 2000-character cap is an
ARBITRARY limit, and agents have been working around it in the open: reviewers
routinely file "FULL CLAUSE TABLE + EVIDENCE: art_xxxxxxx — the 2000-char note
cap forced the card's clause table" into a separate artifact, and tb02 hit the
same cap filing forensics today. A verdict whose reasoning must be truncated to
fit a column has lost the thing that makes it reviewable.

RULING: a verdict should not carry its substance in a free-text note field. It
should POINT AT AN ARTIFACT. The row carries the decision plus the pointer; the
artifact carries the clause table, the reproductions, the evidence. Then review
context is durable by construction — it cannot be dropped by a reviewer who
forgets to record, and no rail is needed to chase it.

Consequences to work through in the 0.2 design (NOT a 0.1 change): the attest
verb and schema grow an artifact reference for verdict-kind attests; the
artifact becomes the review's home; the note degrades to a short summary or
disappears; the existing `completion-requires-results-artifact` rail becomes
unnecessary for reviewers because the pointer is structural. Sequence with
artifacts-and-reconciliation.md (ratified) and the check-tier verdict facts.

Interim until that lands: the rail keeps reviewers honest, and the shipped
guidance says a path in an attest is not custody.

## 2026-08-19 — Surrender deleted from the fabric (Mike, ruled to tb02, stated three times)

An agent may not give up its card. Surrender — the holder unilaterally closing
its own obligation — is removed from the 0.2 design. In its place: a typed
CANNOT-PROCEED report from holder to parent (the card's opener), stating why
completion is impossible. The card STAYS OPEN on the holder until the parent
disposes: revoke, re-scope, or restaff. Obligations never evaporate from below;
a mind above the failure owns the new plan.

Motivating specimen: 2026-08-19, the T1778 Apple-signing coder surrendered at a
keychain human-gate at 03:25 PT with perfect evidence — and the org went silent
for 19 hours because a surrender pages nobody and leaves nothing open.

Engineering conditions ruled in with it (philosophy gate §2/§3):
- cannot-proceed PAUSES supervision/prodding on that card (the work-blocked
  shape) — a holder must never be ladder-burned on a card it has proven it
  cannot do;
- the report routes to the parent as that parent's decision; a dead or silent
  parent is covered by the existing fault-bubbling climb;
- stop-and-report is the agent's lawful "no"; what is removed is only the
  power to dissolve the row.

Scope: 0.2 line (main). 0.1.8 is frozen and keeps surrender as history. The
earlier ask-then-surrender guidance idea is superseded by this ruling.

## 2026-08-20 — Event stream is a firehose, not a focused feed (Mike, ruled to tb02)

The external WS streaming endpoint is part of the OBSERVABILITY LAYER. Its
point is that EVERY substrate event streams out of it, so any future UI or
any agent can monitor what is happening in Tightbeam. Filters exist to let a
subscriber narrow what it receives — they are never a gate on what is
streamable. This supersedes the "focused" scoping of the reviewed 0.1-org
design (art_7450257b, wi_5c34747f), which closed the vocabulary to a single
work_item_created class and listed the broad feed as a non-goal. That
plumbing survives — capability auth, durable event rows, cursor replay,
push-after-commit — the closed single-class vocabulary does not.

Targeting: untargeted (0.2.0 or later, undecided). When work starts it
branches from main tip. WS is orthogonal enough that merge timing is
unconstrained.

Consequences:
- OQ5–OQ10 from the draft spec (expiry bounds, expiry socket close,
  list/revocation wire, timing non-disclosure, bootstrap 503, cursor
  encoding) are NOT ruled — they are mechanics of a superseded scoping and
  get re-derived when the firehose spec is written.
- The reviewed design and the 915-line draft spec are INPUT, not authority:
  rescued to archive/filtered-external-push-subscriptions-recon-v3.md
  (sha256 3e0cd6df…, verified against the artifact row) and
  archive/focused-external-subscriptions-v1-draft.md.
- The 0.1-org cards on wi_5c34747f (the OQ hold asg_430badf6, the spec card
  asg_ad5c8ca1) are moot in their current scope; the org is paused, so they
  sit inert until disposed.

Context worth keeping: the OQ decision request to Mike VANISHED repeatedly
at the ruling seam (2026-08-15/16), and the org filed ~37 one-per-recurrence
evidence cards instead of one specimen with a count. Both carded untargeted
2026-08-20 (Mike: card with standalone context, do not schedule on a
release): wi_89087a49 the vanishing decision-request defect, wi_c05fdbe6 the
card-per-recurrence burn pattern.

## 2026-08-20 — Firehose auth: existing gateway auth, no capability keys (Mike, ruled to tb02)

The event stream authenticates the way everything else at the gateway does,
as the requesting user with their existing credential. Deployment reality is
localhost or tailscale, the consumer is the user's own tooling, the feed is
read-only. There is NO separate capability/API-key system: no key minting,
no expiry, no per-feed revocation wire. Revocation is the existing session
and device revocation. Scoped or expiring keys become a later versioned
addition only if a less-trusted consumer ever becomes real (same later-
decision pattern the draft used for SSE and native TLS).

Consequences for the draft spec's blocking questions:
- OQ5 (key expiry), OQ6 (expiry closing an active socket), OQ7 (key
  list/revocation wire), OQ8 (timing non-disclosure) are DEAD. All four were
  mechanics of the capability system that no longer exists.
- OQ9 (bootstrap/replay concurrency): Mike ruled THERE IS NO LIMIT. No
  bootstrap admission cap, no 503 server_busy for replay capacity.
- OQ10 (cursor byte format): delegated to the firehose spec writer as a
  technical decision. No owner ruling needed.

With this and the 2026-08-20 firehose ruling above, nothing about the
streaming feature is waiting on Mike. The next step, whenever someone picks
it up, is a firehose-scoped spec written off main tip with the archived
focused design and draft as input.

## 2026-08-22 — Main is merged into, never worked in (Mike; stale law file was the defect)

"They need to be working in their own workspaces and then only merging to
main, not in main itself." Mike states this was ALREADY the standing
pattern for weeks — not a new ruling. The defect: the code repo's
CLAUDE.md still carried the 2026-08-13 no-door text ("push main
DIRECTLY"), so agents followed the stale file: the last twelve main
commits are all direct single-parent pushes, five by
product-owner:tightbeam (s_f63d31e5) and the rest by its coders, several
onto a red suite (lawful under the stale text's baseline-matching
clause). Mike's clarification of the original intent: no-door waived the
PR CEREMONY only — it was never an invitation to land broken code; the
gates-green requirement always stood. So the conduct finding stands too:
pushing onto a red suite while recording the failures as pre-existing
was a violation of the rule's intent, rationalized through the
baseline-matching clause. Fixes: CLAUDE.md corrected to merges-only
with green gates required and the baseline-matching loophole deleted;
the pushing PO was notified that red blocks all merges until the suite
is fixed.

## 2026-08-30 — Human contact is not Tightbeam's problem; escalation to Mike ends at a clean record (Mike, ruled via terminal-agent relay, stated repeatedly)

On the "dead-letter human rung" discussion (stall-watchdog-kit.md §4.12,
wi_a8de6fe5): this is a NON-ISSUE as a substrate problem, and Mike has said
so before; agents must stop raising it as one. His ruling, definitive:

- The org's whole duty is to CREATE A CLEAR RECORD an external UI can
  display: a decision request addressed to the user, carrying its question,
  options, context, and original raise date across any supersession. That
  record is where the substrate's responsibility ENDS.
- HOW Mike is contacted as a human (push notification, a UI he opens,
  Main told to notify him, anything else) is a PERSONAL OPERATOR DECISION,
  outside Tightbeam's definition, and it must stay outside. Tightbeam does
  not define or build human-contact machinery. Optionally Main can be
  directed to push-notify — that is operator configuration, not substrate.
- Design work on wi_a8de6fe5 proceeds under this frame: deliverable is the
  clean user-addressed record (content, age preservation, queryability),
  not a delivery mechanism to a person.

Recorded 2026-08-30 by the external Claude session on gibson at Mike's
written instruction ("This needs to be marked definitively in some
canonical document"), from his annotations on the stall-fix progress
review.

## 2026-08-31 — Rails keep honest agents on task; they are not a defense against rogue agents (Mike, stated repeatedly, recorded on his instruction)

Standing principle, restated by Mike 2026-08-31 after it kept resurfacing in
design work: "rails keep agents on task. They do NOT stop malicious or rogue
agents. We assume agents are honest."

Consequences for design:

- A proposal must not justify itself as protection against an agent that is
  lying, cheating, or exceeding its authority on purpose. That threat model is
  out of scope for Tightbeam's rails.
- When an honest agent does the wrong thing, the defect is in guidance, rails,
  or the card's design. Fix those. Do not add enforcement machinery
  (permission grants, scoped authorization checks, substrate-enforced limits on
  what an agent may decide) to compensate.
- Attribution and honest records ARE in scope: an agent signing as itself, a
  row saying who acted, a history labelled unknown when it cannot be proven.
  Those make the org legible, which is different from making it defended.

Applied immediately to `operator-ruling-provenance-v1.md`: the delegation-grant
machinery is out. What remains warranted is the submitting session recorded on
every ruling, refusal of an owner-asserted ruling with no session behind it,
and a label for the 315 historical rows that cannot be proven either way.

Recorded 2026-08-31 by the external Claude session on gibson at Mike's
instruction, from his review of the stall-fix progress report.
