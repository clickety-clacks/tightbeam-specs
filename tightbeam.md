# Tightbeam

A patchbay between chat clients and coding-agent harnesses. Named for The
Expanse's point-to-point laser comms — no broadcast, no bloat, nothing in the
middle that thinks.

This document is the specification and the product. It states what Tightbeam
is, why it is, how it works, and what it refuses to be. The reasoning, spikes,
and dated decisions that produced it live in `tightbeam-decisions.md` (non-
normative); where that record and this spec disagree, this spec wins.

## The Spirit

Tightbeam is a patchbay: the smallest possible deterministic substrate through which one person and their agents talk, hire,
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
bigger, or a failure quieter, it isn't Tightbeam. It does not aspire to be
more than a patchbay; it aspires to be a great one.

## What it is, and what it replaces

Tightbeam presents one unified chat surface over multiple coding-agent
harnesses (Claude Code, Codex, and whatever comes next), where each session
maps 1:1 to a native harness session and carries its own harness / model /
thinking-level selection. It is the substrate for one operator running many
agents that talk to each other, hire each other, and coordinate — with the
operator watching from a phone. (A fully autonomous "dark" org is one thing
you can build on it; the substrate itself carries nothing specific to that
use — no ticketing, no workflow system — and does not presume it.)

It exists because the prior generation of this role (a monolithic gateway that
hosted the agent runtime itself) failed in a characteristic way: it entangled
message routing with agent logic, kept shadow state that silently disagreed
with the harnesses, lost prompts inside its own recovery machinery, wedged its
single thread, and grew without bound as features accreted. Every tenet below
is, in part, a refusal of one of those failures. Tightbeam writes no agent
loop of its own — the model providers own that now — and inherits every
harness improvement for free.

Within that role, the most novel piece is not the chat gateway; it is the
replacement for the hand-tended agent instruction file. Identity is compiled from declarative
archetype manifests, and rules are split into two tiers: prose (skills and
guidance) for judgment, and deterministic law (rails) for everything
enforceable — because prose is not enforcement, and the emphatic all-caps
rules people bury in instruction files exist precisely because inference
skims them.

## Where it sits

Agent systems stratify by lifetime and by who owns the clock. Below this
substrate sits the harnesses' own orchestration: subagents fan out inside a
single turn and evaporate with it; harness-native scheduling continues a
session's own life only while its runtime survives, and only for itself.
Above it sit inter-organization agent meshes: call-shaped federation between
agents assumed to be already alive. Neither layer makes an agent exist. A
harness is a turn machine — prompt in, turn out, inert between — and a mesh
connects lives that something else sustains.

Tightbeam is that something: the residency layer. Plainly — it is the system
you install when you are tired of duct-taping resident agents together. The
improvised version is well known: a cron script to wake the session, a
lockfile so two wakes don't collide, a queue file for prompts that arrived
mid-turn, retry logic for when the queue file lies. That is adhesive with no
ratings, and the joint fails under load precisely because it is load-bearing.
This substrate is the machined part for that joint. It owns the four things a
turn machine cannot own for itself — an **address** (identity that survives
processes), a **mailbox** (prompts accepted while the agent is not running),
a **clock** (wakes scheduled by the agent, by others, or by external
systems), and **supervision** (death detected, restarted, recorded) — and
each carries a rating where the tape had none: exactly-once enqueue with
terminal states, wakes as durable cancelable rows, deaths that leave a row
and a reason.

The other tentpoles follow from residency rather than standing beside it. A
resident must *be someone* and *be governable*: identity and law as data
(T4) — the substrate's most novel piece — exist because a resident's
who-and-what-binds must persist across turns, sessions, and harnesses, and
because a substrate forbidden to think can enforce only deterministic law.
And an operator needs a window into the org: the chat wire, adopted as-is
and never owned, is that window — a port on the substrate, not a pillar of
it.

The center that holds it all is the patchbay form. The substrate owns
neither of its faces — the client wire on the front is another product's
contract, ACP on the back is the vendors' — so everything it *is* lives
between two protocols it does not own: the ledger, the org, the law, the
supervision. The layers above and below compose rather than compete: a
session's turns may use harness orchestration freely inside themselves, and
a mesh may front the factory per §Interop. Harness vendors will keep
absorbing residency features natively; what no single vendor can own is
exactly the between — identity that spans harnesses, a neutral ledger of
what was said and delivered, org structure and law as data, supervision that
outlives any one vendor's process. The ambition is not to be more than a
patchbay. It is to be a great one.

## Tenets (normative)

T-CONCURRENCY (Flynn ruling 2026-07-30, PRIME INVARIANT): Tightbeam exists
because single-threaded agent runtimes were intolerable. Sessions run
concurrently: no session's work ever waits on another session's, and no
harness's work ever waits on another harness's. Only a session's OWN lane
serializes its own turns. Corollary for anything org-wide: an operation may
wait on work that is RUNNING (mid-turn — its world must not change under it),
NEVER on work that is merely QUEUED — a queued turn has not started and
composes its world when it starts, so quiescence demands against queued work
protect nothing and block everything. *Prevents:* the single-threadedness this
product was built to escape re-entering through admin verbs and global
barriers (worked example: `identity apply --all` counting queued-as-busy made
two-harness smoke parity structurally impossible, twice, by independent
mechanisms). *Test:* does this make anyone wait on work that has not started,
or on another session's work at all? Then it violates the reason Tightbeam
exists.

COROLLARY — LIFECYCLE NEVER BLOCKS PROMPTS (Flynn, 2026-07-30): adapter and
session lifecycle — spawn, bounce, close, heal, credential events — is
genuinely sensitive and deserves careful serialization. It must NEVER sit on
the path of a prompt to an already-running agent. "Every other prompt blocks
or caches behind something else" is the OpenClaw failure this product exists
to escape, and it is reproduced today: the turn path calls the adapter
coordinator, one global process, so a lifecycle stall there queues every
prompt on every harness (worked example: the F2 credential-event deadlock
stalls 5s across every session on every harness). The shape that satisfies
this: LOOKUPS are concurrent reads with no process in the path; only
MUTATIONS — boot, bounce, close — traverse the serializer. *Test:* can any
lifecycle operation, or any FAILURE of one, delay a prompt to a session that
is already running? Then it is on the wrong path.

T-RECOGNITION (Flynn ruling 2026-08-05): THE SUBSTRATE NEVER WAITS. Tightbeam
is a production machine in the Newell sense: a recognize-act cycle over the
current durable state of the system. No substrate state may have someone
else's decision as its exit condition — anything shaped like waiting is
either a fact an agent asserted and will retract, or it is a defect. Judgment
— model choice, parking, halting, redirecting work — belongs to inference;
agents express those decisions to the substrate as facts (asserted and
retracted by the same authority), and substrate behaviors are productions
whose declared conditions either match the current state or do not. "Stop
prodding this session" is not a flag the prodder checks; it is a standing
fact that makes the prod production stop matching, exactly as it would not
match a session with no open assignment. Standing state is DERIVED from
append-only assert/retract pairs, never stored as a mutable flag. On any
failure the substrate owes exactly three things — the truth (a failed row),
the named reason, the record — and then tells someone who can act, where
"can act" is never guessed: a notice to a parent is a turn, its terminal
state is the proof, a failed notice climbs the lineage, and the terminal
alert to the user is a tokenless wire message that cannot share the failure
mode. Full design: production-machine-v1.md. *Prevents:* adjudication, the
worked example this tenet was carved from — a substrate-owned session hold
whose only exit was a human ruling, entered when a model was unavailable;
it froze the queue behind it, re-raised itself within minutes of being
cleared by hand, told the user to run a CLI verb that was never wired, and
livelocked production on gibson's first week. 5,700 lines, deleted the day
the tenet was ruled. *Test:* does this put the substrate in a state that
only someone else's decision can exit? Then it is the defect this tenet
names. Is this behavior's condition readable in working memory by anything,
or is it a flag with one reader? The former is a production; the latter is
procedure wearing a fact's clothes.

T-INTEGRATOR (Flynn ruling 2026-08-03): TIGHTBEAM IS NOT A HARNESS. It runs no raw
model of its own; it INTEGRATES with harnesses and leaves the work to them. Three
consequences, and they pull against each other on purpose:

(1) Tightbeam does not replace a harness's own faculties. A harness that delegates
internally — subagents, its own task list, its own tooling — is doing its job, and
tightbeam neither mirrors that machinery nor demands it be routed through session
spawns instead.

(2) A harness running INSIDE tightbeam should be a good citizen and use tightbeam's
faculties: file work items, take assignments, attest. That is a property of the AGENT
(guidance, kungfu), not a mechanism tightbeam enforces — minds bridge, no mechanical
tokens.

(3) Tightbeam is NOT beholden to report everything internal to a harness — but neither
does it want to be a leaky abstraction sitting on top of one. WHERE WE CAN PROVIDE
OBSERVABILITY INTO A HARNESS'S INTERNAL WORKINGS, WE SHOULD. The test is capability,
not obligation: if the information is already crossing the seam, spending it on
machinery while showing a human a spinner is a choice, and the wrong one.

*Worked example, 2026-08-03:* ACP `tool_call` updates arrive with title, kind and full
content. `gate_update_output` (acp/adapter.ex) JSON-encodes the WHOLE payload so rails
can inspect it, while `progress_status` reduces the same update to a title or the string
"Using a tool", persists nothing, and the human sees a spinner. The data was in hand and
already parsed. *Test:* is tightbeam holding information about a harness's work that a
human would want and cannot see? Then (3) applies.

T-CONSPICUOUS (Flynn ruling 2026-08-03): CONSPICUOUS OPERATIONS. Everything the
system does on a user's behalf is visible to that user WHILE it happens. It is
not the waiting that erodes trust, it is the silence: a prompt may legitimately
sit behind another turn, behind an adapter coming back, behind a credential
renewing — provided it SAYS SO. What may never happen is a submitted prompt with
no account of itself. This is why substrate operations are elevated onto the
clawline protocol rather than logged beside it: the system's own work is narrated
on the same channel as an agent's, so a user reading one stream sees everything
acting on their behalf. A state that means both "about to run" and "will never
run" violates this tenet even when nothing is lost, because the user cannot tell
which one they have. *Prevents:* the OpenClaw failure Flynn names as the reason
for this product — "I'd send prompts and the agent turn would just fail, or I'd
get no response and wouldn't know what happened to my message." *Reproduced
today:* a 60-minute soak lost 3 of 148 turns to gateway SIGKILL — left `queued`
with startedAt NULL and error NULL, indistinguishable from turns about to start,
while `lane_manager` publishes terminals for turns that STARTED and died and has
nothing to say for turns that never started. *Test:* if this operation stalls or
fails right now, can the user see what became of their message without reading a
log? If not, it is not conspicuous, and shipping it spends trust the product
cannot re-earn cheaply.

T-SOURCE (Flynn ruling 2026-07-30): SINGLE SOURCE OF TRUTH. Every fact has
exactly one owner, and the owner is wherever the fact physically lives — the
harness owns conversational truth (T2 is this tenet's conversational case), the
adapter process owns session residency, a machine owns which binary it carries,
a git tree owns its own revisions. Anything else holding that fact holds a
CACHE: one-way, marked as such, never consulted as authority, and free to be
wrong without consequence. When the substrate needs a fact it does not own, it
ASKS the owner; it does not keep a copy and reconcile. *Prevents:* two copies
that can disagree with no tiebreak, which is how state silently rots — and the
subtler failure, a record that cannot describe reality it was created after
(worked example: a proposed hosts.cli_build column would have read NULL for
every satellite that already existed, so the fix could not have healed the
field it was built for, and could only have been demonstrated by writing a
synthetic history into the DB). *Test:* does this store a fact whose reality
lives somewhere else? Then either it is a cache that may be wrong without
consequence, or it is a defect. If you would have to fabricate its past to
demonstrate it, it is a defect.

T-PARITY (Flynn ruling 2026-07-25): parity on EVERYTHING between registered
harnesses is an invariant. Every harness touchpoint goes through the polymorphic
`Tightbeam.Harness` interface (N-ary, never two-ary); every capability is
parity-complete or carries a named divergence with a negative test in
`harness-support.md`; the complete new-harness obligation bundle is enumerated in
ONE place (`harness-adapter-seam-v1.md` §Adding a harness, mirrored in the
behaviour moduledoc) and enforced by the shared per-harness conformance suite plus
the per-harness smoke matrix.

Each tenet states an invariant, the failure it prevents, and a test to apply
to any proposal. A proposal that fails a test is not admitted "carefully" — it
is a skill, a fork, or another product.

**T1 — The substrate never thinks.** It routes, records, and enforces
(deterministic rules over structured facts); it never interprets content.
*Prevents:* routing entangled with agent logic, where every feature can break
every other. *Basis:* the components are intelligent, so the wiring must be
dumb — the inverse of systems that placed intelligence in the wiring because
their components could not think. *Test:* does this require the substrate to
understand what a message MEANS? Then it belongs in an agent.

**T2 — The harness owns conversational truth.** The projection store is a
one-way cache of it. Delivery state is a dumb, durable, queryable ledger with
terminal states and no cleverness: no auto-retry, no re-routing, no backward
reconciliation. *Prevents:* shadow state that silently disagrees with harness
reality, in which work dies invisibly inside recovery logic. *Test:* does this
duplicate conversational state or try to be clever about recovery? A lost unit
of work must be a visible row with a reason, never a mystery.

**T3 — One chokepoint; closed sets.** Every state mutation is a verb through a
single dispatch path. The verb set, the turn-state set, and the delivery-
mechanism set are closed; growth requires a spec amendment, not a convenient
branch. *Prevents:* holes in auditability and in any future enforcement layer,
which all depend on the chokepoint being total. *Test:* does this mutate state
outside dispatch, or quietly grow a closed set?

**T4 — Identity is data; law is layered.** Who an agent is = generated files
(archetypes projected into harness homes). What binds = constitution (owner-
only substrate mechanics) over rails (proposable, deterministic rules) over
skills and guidance (prose). Prose is not enforcement. *Prevents:* reliance on
inference obeying a rulebook it may skim. *Test:* is this rule about structured
facts (railable) or about content and judgment (guidance)? Is enforcement
being placed in prose?

**T5 — Observe, don't manage.** No backpressure, no queue management, no self-
healing cleverness — only bounded counting rules plus total visibility (queue
depth, event log, lifecycle events, health probes, loop/scheduler watchdogs).
*Prevents:* management machinery becoming the failure surface; harnesses own
their own pacing. *Test:* does this MANAGE flow, or make flow VISIBLE?

**T6 — Fast and minimal.** Small dependency budget, close to the wire,
comprehensible in one sitting (a runtime on the order of a few thousand
lines), boring enough for an agent to hold in context and re-implement.
*Prevents:* a substrate too large to read end-to-end, which can only be fixed
by folklore; comprehensibility is debuggability, and every line is a permanent
operational and token tax. *Test:* does this make the core harder to hold in
one head?

**T7 — Divergence over accretion (the fork doctrine).** The substrate does not
absorb long-tail features. A user who wants their own case: first looks agent-
side (guidance, skills, archetypes); else forks and does not contribute the
change back; best, uses the substrate as a reference implementation for their
own. Upstream accepts only bug fixes, wire-contract parity fixes, hardening of
existing tenets, and spec errata — never capabilities. Forks pull, they do not
push: not contributing back is a one-way valve, not severance, and downstreams
should keep tracking upstream for fixes. *Prevents:* death by accepted
features, each a permanent tax on every invariant above; the way to say yes to
everyone is forks, not merges. The spec, not a maintainer's judgment, is the
arbiter. *Test:* is this a long-tail capability? Then it is a skill, a fork, or
a reference-implementation derivative.

**T8 — Coordination is fact-shaped, not call-shaped.** Between agents, the
system is a production system: durable facts in working memory (messages, the
turn ledger, wake registrations) plus deterministic condition→action rules
(wake triggers; rails are productions) plus agents as the engine that fires
when conditions match. There are no promises, awaited calls, or continuations
held in processes across agent boundaries — one asks for a wake when a
condition holds; one does not call and await. *Prevents:* continuations lost
when their holder dies; work that must complete on human/day timescales bound
to process lifetimes; caller-callee coupling that freezes the org chart.
*Basis:* beyond turn scale, resuming a long-held turn cold-reprocesses its
whole context, the continuation tower (harness/adapter/lane) must survive the
entire wait, a held turn blockades its session's lane and cannot outlive
transport timeouts, and an in-process wait is invisible where a wake is an
inspectable, cancelable row. (A deterministic in-tool wait consumes no
inference; the cost is in holding, resuming, occupying, and hiding — not in
waiting per second.) *Boundary:* within a turn (seconds to minutes, inside
transport timeouts) code-shaped waiting is correct; beyond turn scale the
continuation must move from process to durable row. *Test:* does this hold a
continuation in a process across an agent boundary, or make an agent await a
result rather than be woken by a fact?

**The test, in order.** For any proposal: (1) must the substrate interpret
content? → agent-side (T1). (2) Does it shadow or out-clever harness/delivery
truth? → reject (T2). (3) Does it bypass dispatch or grow a closed set? → spec
amendment or reject (T3). (4) Is it enforcement-in-prose? → make it a rail or
accept it as guidance (T4). (5) Does it manage rather than observe? → reject
(T5). (6) Does it grow the core beyond one-sitting comprehension? → reject
(T6). (7) Is it a long-tail capability? → skill, fork, or reference-impl
derivative (T7). (8) Does it hold a cross-agent continuation or force an await?
→ make it a fact/wake (T8). Pass all and it may be Tightbeam; fail any and it
is not. "No, this isn't Tightbeam" is a complete and final answer.

## The org chart is a behavior, not a schema

Organizational structure is not modeled in the substrate. Hierarchies, review
boards, contract-net auctions, and the like are runtime behaviors composed
from the primitives (spawn, post, wake) and described in prose (skills and
guidance) — never tables the substrate branches on. The substrate provides the
verbs; the shape the org takes is emergent and revisable by editing the
handbook, not by migrating a schema. This is the deliberate opposite of freezing
human org charts into substrate data.

Because org structure is behavior, the substrate can also help the org *learn*
its structure: an agent that discovers a durable pattern proposes it into the
identity layer (a skill, a guidance amendment, an archetype, or a rail), which
the operator merges. The substrate's history — the message store, the event
log, the identity repo's version control — is the org's memory of how it came
to work the way it does.

## Goal

A single long-running daemon that:

1. Speaks the existing chat client's wire protocol on the front, unchanged, so
   that client works against it without modification.
2. Speaks ACP (Agent Client Protocol) to harness adapters on the back, so the
   substrate never parses harness-specific output and inherits harness
   improvements for free.
3. Maps each UI session 1:1 to a native harness session, exposing a
   harness / model / thinking-level picker per session.
4. Compiles one canonical agent identity into isolated, disposable harness
   homes, so the substrate's agents carry skills and instructions distinct
   from any normally-installed harness.
5. Lets agents talk to and hire each other through the same small verb set the
   operator uses, with full provenance.

## Non-Goals

- Not a rewrite of the chat client; the front wire is adopted as-is.
- No approval/permission UI in the agent loop. Sessions run in the harness's
  bypass/full-access mode; the substrate does not adjudicate tool use.
- Not feature parity with the monolith it replaces. Capabilities beyond the
  core (rich schedulers, multi-channel routing, embedded agent runtime) are
  agent-side, forks, or explicitly-scoped later milestones behind optional
  interfaces — never accreted into the core (T7).
- The substrate never stores, caches, or forwards harness auth tokens. Auth
  lives only in each harness's own credential store.
- No inter-agent orchestration protocol as the internal coordination model
  (T8); coordination is fact-shaped (wakes over a ledger).

## Architecture

```
chat client(s)
      │  client wire protocol (websocket, message-granularity: auth, message,
      │  ack, typing, session status, streams, read/tail state, replay)
      ▼
┌────────────────────────────────────────────────┐
│                the daemon (thin)               │
│  • wire server (front: WS + HTTP, one port)    │
│  • single verb dispatch path + event log       │
│  • session registry (provenance + pointer chain)│
│  • projection store (one-way cache of truth)   │
│  • per-session serialized turn lane            │
│  • durable wake store (fact-shaped comms)       │
│  • identity projection (homes from manifests)  │
│  • adapter supervisor (~1 per harness×archetype)│
└────────────────────────────────────────────────┘
      │  ACP (Agent Client Protocol; JSON-RPC over stdio)
      ▼
 harness adapters (each spawned with a managed home + symlinked auth)
```

### ACP on the back

ACP normalizes exactly what would otherwise be hand-built per harness:
`initialize` (capability negotiation), `session/new` and `session/load`
(create/resume, with history replay), `session/prompt` (one turn, resolving
with a stop reason), `session/update` notifications (message chunks, thought
chunks, tool calls, plan and command updates), `session/cancel` (mid-turn
interrupt), `session/set_mode` (permission mode — bypass selected at session
creation), and `session/set_config_option` with agent-advertised typed
`configOptions` (model and reasoning/effort selection). The substrate never
parses harness stdout; it speaks one protocol to every harness.

The mapping onto the client wire is mechanical: ACP config options and modes
project into the client's session-status capabilities and option catalogs;
ACP update chunks accumulate into one client message with a typing indicator
while a turn runs; "which harness" is simply which adapter binary the daemon
spawns with which environment — the daemon's own thin layer, not an ACP
concern.

**Adapter selection rule.** Both adapters select a model via
`session/set_config_option` with a bare model name; effort rides as a
`model[effort]` suffix applied through a per-harness effort config option.
Model selection is applied immediately after `session/new` and after every
`session/load`, and the advertised current model is never trusted (a harness
may default a session to a model the account cannot use). This rule is
load-bearing; it belongs to the adapter layer and nowhere else.

### The turn lane (the only stateful runtime component)

Per session, the daemon holds exactly a serialized lane: a FIFO of pending
prompts and the current turn. One turn runs at a time per session; ordering is
authoritative and deterministic. Prompt submission is a single write to an
already-warm adapter process (no per-prompt spawn latency). Adapters are long-
lived, one per (harness, archetype) in use, lazily spawned and idle-reaped —
a handful of processes, not one per session (ACP is multi-session per
connection). Adapter death is recovered by respawn and `session/load`.

### Source of truth and the delivery ledger

The harness transcript is the truth (it owns context, compaction, tool
detail). The projection store is a one-way materialized cache for display and
replay; it is never reconciled backward into the harness. A session's
identity may map to a *new* harness session id on resume in some harness
paths, so the registry keeps the UI-session → harness-session-id mapping as an
append-only pointer chain, not a constant. When re-adoption fails and the
chain falls back to a fresh harness session, the memory loss must be visible
where it happened: the substrate appends a marker message — a
substrate-authored notice in the stream, distinguishable from agent speech by
its sender — at the reset point, so a reader of the chat can see where the
model's working memory begins. A terminally failed turn gets the same
treatment: a marker carrying the human-readable reason stands where the
reply would have been, because a failure that exists only as a state frame
reads as a prompt that silently vanished. The chat history itself is never
trimmed to match the model's context: the log is the operator's record; the
context is the model's working set.

Delivery is tracked in a durable ledger with a closed, one-way state machine —
`queued → running → (delivered | canceled | failed | failed_unknown)`. The
ledger is dumb: it records where each accepted prompt is, never re-interprets
it, never auto-retries, and never reconciles against the transcript. Two
invariants follow and are enforced by acceptance tests:

- **Prompt conservation.** Every accepted prompt (from a client or a wake)
  reaches exactly one terminal state; none may remain non-terminal beyond a
  bounded age. A lost prompt is therefore impossible-silent — it is a visible
  ledger row with a reason.
- **No automatic retries.** The pipeline never re-sends a prompt. A turn found
  interrupted after a crash is terminal (`failed_unknown`) and is never
  auto-resumed, because its tools may already have run. Retry is the sender's
  decision.

The ledger is a delivery record, not shadow conversation state — the
distinction that separates it from the failure mode it replaces. It holds one
fact per prompt, with terminal states, and nothing clever.

### Auth model

Credentials are STORE ROWS, not loose files: each provider has one Tight-Beam-
owned store backing file (`auth/<harness>/…`), a metadata record
(`.tightbeam/credential.json` — onboarded/terminal/expiry), and a symlink from
each `{harness, machine}` home to the store. Onboarding is a serialized guided
ceremony per provider (`tightbeam onboard openai|anthropic`); Claude uses the
NON-ROTATING setup token (raceless under N subprocesses), Codex's rotating
`auth.json` has a single writer authority with harvest-before-wipe on
regeneration. A credential proven dead (`account/updated.authMode` terminal
evidence) PARKS the provider's sessions rather than restarting them, gates new
spawns, and emits per-session parking visibility on the stream; successful
re-onboard resumes with the counterpart signal. The daemon holds no token
cache. Contracts: `tightbeam-credential-onboarding-v1.md`,
`served-identity-home-projection-v1.md` §9-§10, observability addendum
closure 2.

### Agent identity and home projection

The substrate defines its own agent identity — a canonical set of guidance,
skills, and MCP config, authored and versioned at the product level, separate
from any normally-installed harness. From the outside this is one agent; the
harness/model/thinking picker swaps the engine underneath a stable identity.

The identity is SERVED, not installed (contract:
`served-identity-home-projection-v1.md`). It lives in a three-ref git tree —
`tightbeam/upstream` (source snapshots), `main` (working + org customization),
`tightbeam/live` (the publication ref sessions read, resolved ONCE per
provisioning so no session straddles a publication) — edited through identity
verbs (`identity edit / relearn / status / apply`; `relearn` merges the next
shipped snapshot and preserves org customizations). Composed guidance reaches
the session as the HARNESS'S OWN instruction channel over ACP `_meta` (codex
`developerInstructions`; claude `systemPrompt` preset-append) — not as a home
file — and elected skills materialize at the SESSION CWD under the reserved
`tightbeam__*` namespace, which org identity may not claim. Each session
stamps the live revision it materialized from; `identity apply` is the
explicit bounce-and-resume onto current live, and staleness is visible in
`identity status`. Shared `{harness, machine}` homes carry only credentials,
rails, `.tightbeam/`, and substrate baseline skills — harness-owned durable
state survives regeneration byte-identical.

Identity is a set of named **archetypes**, each a declarative manifest (a parts
list, no logic): guidance fragments composed in order, skills chosen by name
from one shared library, MCP config, optional defaults (harness, model,
thinking, default wake subscriptions), an allowed host-set (§Placement), and
**references** — named pointers to the work materials the agent operates on
(a repo and its remote, a docs tree, a data source: location plus how to
access it). References compile into the guidance text of the projected home:
they become knowledge the agent reads and acts on, never substrate machinery.
The substrate does not fetch, mount, sync, or serve work materials — the
agent gets at its own materials the way any worker does. Point at the docs;
copy the identity; move the credentials never. Sessions are created *as* an
archetype.

Guidance composes from a shared fragment library (`identity/guidance/*.md`)
via an include directive — a line of the form `#include "fragment.md"`,
resolved recursively at projection time. Includes are parts-listing written
in-text, and that is ALL they are: no variables, no conditionals, no logic —
a template that can compute is an agent that can't be audited. Resolution is
validated at identity load: a missing fragment or an include cycle fails the
boot. The substrate ships built-in fragments for its own operation (the
operating manual; the engineering-guidance set) which every archetype's
composition can include; the operating manual is SUBSTRATE LAW and cannot be
overridden by an org fragment of the same name (other built-ins materialize
into the library only where absent, so an operator edit wins for those).
Because composition precedes the projection hash, a fragment edit
changes the manifest hash and regenerates exactly the homes that include it.

Skills are the on-demand tier of the same identity: always-loaded guidance
carries a one-line pointer, the procedure loads when invoked. They live in
one shared library (`identity/skills/<name>/SKILL.md`); an archetype ELECTS
skills by name (omitted = the built-in set; named = exactly that list; an
unknown name fails the boot). Built-in skills (assimilation is the first)
materialize into the library at load only where absent — an operator's edit
always wins, and deleting the file restores the built-in.

The harness's own native surface — vendor-shipped skills, commands, and
guidance — passes through UNTOUCHED and is necessary: the projection only
ever adds (the instruction file, elected skills, credentials), never
strips or masks what the vendor ships. An agent's capability set is the
harness's native surface plus the org's elected identity; suppressing the
vendor layer would forfeit exactly the free harness improvements this
substrate exists to inherit.

Skills come in two shapes under one mechanism. A ONE-SHOT skill is a
directory with its `SKILL.md` (plus any resources). A SUBJECT TREE is a
directory whose root `SKILL.md` is a routing MANIFEST — a parts-list in
prose naming the technique skills nested beneath it ("structured
concurrency → `concurrency/SKILL.md`") — with the techniques as
subdirectories carrying their own `SKILL.md`. Election is ATOMIC at the
root: electing a subject takes the whole tree; nested nodes are not
electable (they are unknown names to election). Harness skill discovery
surfaces only top-level entries, so a hundred-technique subject costs one
line of always-visible surface — progressive disclosure at every level:
pointer → parent manifest → technique, each loaded only when routed to.

Every projected home carries a PROJECTION MANIFEST — a readable
parts-list of what the home actually is (base archetype, harness, each
skill with its provenance and linkage, fragments composed, settings
contributions), not an opaque stamp: manifests tell you what is in
them. The regeneration gate hashes the manifest's bytes, so description
and fingerprint can never disagree. It links its PARENT for forensics —
the archetype manifest's name and content hash AS OF COMPOSITION — so a
home always answers "which law, at which version, produced me," and a
parent-hash mismatch is visible drift awaiting regeneration. The
projection manifest describes the ARTIFACT; recipes' durable inputs
live upstream (the archetype manifest; a session's override record) —
output never doubles as input.

The library is REPLICATED: every host — gateway and satellite — holds a
replica at `identity/skills/`, and homes everywhere project skills the
same one way, a symlink into their own host's replica. Skill mutation goes
through the chokepoint like every other law change: skill verbs
(put/rm/list, admin-gated, audited as verb rows) write the gateway's
library and push every remote replica immediately; a host unreachable at
push time is a per-host visible degradation healed by the replica
catch-up in its next home delivery. Removal is a TRANSFORM, never a
veto: the operator's `skill rm` always proceeds — elections exist to
know who is affected, not to refuse the operator. Removal updates every
projection and NOTIFIES each electing session by wake ("this skill was
removed; disregard it" — its content may already be in a context only a
message can reach), and names any archetype manifests still electing the
skill so the operator can edit them before the next boot's fail-closed
validation. Pruning inside a tree is a content edit. Only the election is part of the manifest
hash — skill CONTENT deliberately is not, so improving a skill never
costs a session its memory, while changing WHICH skills an agent carries
is an identity change like any other.
Archetypes are **templates, not contracts**: at session creation any field may
be overridden. Runtime-knob overrides (harness/model/thinking) leave the home
untouched; identity-affecting overrides (skills/guidance) produce an effective
manifest whose content hash keys a generated-on-demand home, so unmodified
sessions share the archetype's canonical home and customized sessions get their
own, idle-reaped like any other. The override is recorded ON THE SESSION'S
ROW — it is an attribute of the hire, like its host and model — and that row
is the durable input from which a lost home is recomposed; no separate
registry exists. An override election is a PERSONAL want with its own
lifecycle, distinct from a template election: it live-links the shared
library while the skill exists (edits flow to it like anyone), but when the
skill is REMOVED from the library the session KEEPS the behavior — the
content is materialized for it at removal time, because the operator asked
for that behavior at spawn and library housekeeping is not a revocation.
Stopping the behavior is its own explicit act: a per-session override
removal, with the session notified. A missing override dependency
(fragment or skill deleted since spawn) never bricks a session and never
blocks a boot: the identity composes from what exists and the discrepancy
is logged — the want is honored to the extent reality allows, visibly.

Projection compiles a manifest into each harness's managed home
(`CLAUDE_CONFIG_DIR` / `CODEX_HOME`): the instructions file per harness, the
MCP config in each harness's format, and the shared skills. Homes are
**build outputs** — disposable, regenerated on identity change, never hand-
edited — keyed `homes/<archetype>/<harness>/`. Auth is the one thing in a home
projection never touches. Some behavioral divergence between harnesses is
inherent (same guidance, different system prompts and tool vocabularies) and
is not a projection bug; canonical guidance is written harness-neutral.

Because harness and model are overridable identity fields with full provenance
recorded per session (archetype, effective-manifest hash, harness, model,
thinking, adapter/CLI versions), "same identity, different engine" is a first-
class comparison — A/B and evals fall out of the design. A structured eval
harness is out of scope; the comparison affordance is not.

### On-disk layout

Everything the substrate owns lives in a single dot directory:

```
~/.tightbeam/
  config.*                      # port, harness binaries + version pins
  identity/                     # the canonical agent (version-controlled)
    archetypes/<name>.toml      # declarative manifests (parts lists)
    guidance/*.md               # composable guidance fragments
    skills/<name>/              # shared skills library (SKILL.md format)
    rails/<name>.toml           # deterministic rules (see Law)
    mcp/*                       # shared MCP config fragments
  auth/<harness>/               # per-harness credentials, symlinked into homes
  homes/<archetype>/<harness>/  # generated harness homes (disposable)
  state/                        # SQLite: projection, registry, ledger, wakes,
                                #   devices, event log, lifecycle
  bin/                          # projected CLI wrapper for agent shells
  logs/
```

Regeneration rule: homes are disposable build outputs — regenerate by delete +
reassemble + relink auth symlinks. Credentials live only under `auth/` and are
never touched by projection.

### Placement

An agent's residency and its labor need not share a machine. The substrate,
its stores, and its ledger run in exactly one place per org: one substrate is
the org's spine, and machines are places work happens, not org boundaries — a
second substrate is a second org, not a second site. A session's harness
process, by contrast, may run on any host: the adapter boundary is stdio, and
a remote host is reached by wrapping the adapter command in a transport that
carries stdio — in practice ssh, which every host already runs, and which
adds no new daemon, protocol, or credential class. The substrate remains
unaware of the difference beyond the argv it was handed. The orphan rule is
inherited, not re-implemented: adapters exit on stdin EOF, and a dropped
transport IS stdin EOF, so a substrate death reaps its remote adapters
exactly as it reaps local ones; a host that dies presents as an adapter that
died, and the existing generation/re-adoption machinery is the recovery path.
The division of movement: the transport moves the pipe; material sync moves
the files — homes and harness credentials live on the work host and
credentials never transit; the ledger never moves at all. Home projection
follows the harness: a session's home materializes on the host the session
inhabits.

Placement is identity data (T4). An archetype declares the set of hosts its
sessions may inhabit; a session records the host it actually inhabits; the
host of a spawn must be a member of the spawning archetype's set. "Anywhere"
is an explicit grant — a set of exactly `["*"]`, admitting any configured
host — and never an accident: an empty set is a load-time error, not a
grant, because law fails closed and in set logic an empty where is nowhere. That
membership check is constitutional mechanics — set membership of data against
data at the chokepoint, requiring no rule engine. WHICH member to choose
(balancing, failover, affinity) is a resolver rail; WHY a host set contains
what it does is the operator's statute, written in the identity repo and
never in this spec. Coordination is unaffected by any of it: wakes and the
CLI address identity, never location, so every topology — one machine or
many — runs the same comms model unchanged.

Hosts are declared in an instance registry (a hosts file beside the state,
seedable and overridable by environment), mutated only through an
admin-gated verb — but the registry records ADDRESSING ONLY (a name, how
to reach it, where the org's lease lives). CAPABILITY is never recorded:
topology is its sole source of truth, and every spinup asks the machine
live — detecting what is there, idempotently deploying what the org owns
(directories, adapters, CLI, homes), and only ever DETECTING credentials,
never moving them. A spawn denial cites what the machine actually lacked
at that moment. Intent is expressed by shaping the machine — a host with
only codex credentials is a codex-only host, on purpose — never by a
parallel record that can silently disagree with reality (T2, applied to
placement). What persists is history, not authority: which host each
session inhabits (for modification and teardown) and the lifecycle log of
what was detected and failed (forensics). Every
host — including the gateway's own machine — appears under its real
hostname; there are no indexical names ("local", "here", "self") in the
registry, in `where` sets, or on session rows. The org's vocabulary must
match the operator's: "spawn on eezo" has to resolve on eezo, including
when asked on eezo. Which machine is the gateway's own is carried by the
host's transport config (no ssh destination), never by a special name.
Onboarding a satellite is a client-side ceremony — `assimilate` in the
reference CLI — in which the operator's CLI prepares the machine over the
transport (directories, adapter runtime, the agent CLI, harness
credentials), then registers the host through the verb. The substrate
performs no remote setup itself; it records that setup happened, and an
incompletely-assimilated host simply degrades as a failing adapter until
finished — visibly, since a turn that fails on auth stands in the chat as
a failure marker naming the reason.

Credentials follow one doctrine: **every {org, host, harness} triple gets
its own grant, born inside the org's auth store.** Tightbeam never speaks
OAuth itself — the install ceremony (`setup` in the reference CLI) and
`assimilate` both walk the operator through the HARNESS'S OWN login flow
with its config dir pointed at `<base_dir>/auth/<harness>`, once per
harness the operator wants supported on that host. Where a harness offers a
long-lived non-refreshing token (claude's `setup-token`), the store records
it (`auth/<harness>/oauth-token`) and the substrate injects it as the
harness's own token env — the strongest form of the grant, since a token
that never refreshes has no rotation to race. This is the only moment
onboarding is ever necessary: archetypes never carry credentials (every
home on a host symlinks the one store), sessions never do, and adding
archetypes or sessions is pure data. Copying an existing login into the
store ("harvest" from the machine's own logins, or pushing the operator's
— both explicit flags, never defaults) is a quick-start that SHARES a
grant, and shared grants race: OAuth refresh tokens rotate on use, so two
stores holding one grant silently revoke each other at every refresh.
A dedicated grant per triple is what makes the race structurally
impossible, including between two orgs that assimilate the same machine.

Two orgs may assimilate each other's machines freely — each gateway is a
sovereign org, and its footprint on a host (homes, auth, workdirs, its
shipped CLI) lives entirely under the base_dir it registered, so mutual
assimilation is symmetric leasing, not federation: sessions, wakes, and
truth never cross orgs. The invariant that keeps it clean: **base_dirs are
exclusive** — an org must not register a base_dir another org (including
the host's own gateway) already occupies, or their home projections fight
over the same paths and wipe each other's nested harness state. The
shipped CLI is org-agnostic — which org it addresses comes entirely from
the injected environment (TIGHTBEAM_URL/TIGHTBEAM_TOKEN), never from the
binary — so per-base_dir CLI copies exist to keep versions traveling with
their org, not to separate identities.

## Primitives: nouns and verbs

The substrate's API is a small closed set (T3). Everything else is skills and
guidance composed on top.

**Nouns:** session, archetype, role, room, message, wake, cursor, rail.

A ROLE is a durable name for an office with a mutable session binding —
the org's stable vocabulary for "the reviewer," "the ops log," "the
operator," independent of which incarnation currently holds the office.
References are strictly TYPED, and the type is carried STRUCTURALLY —
by the field, never inferred from a string's shape: an API seam takes a
sessionKey (an incarnation), a role (an office), or a userId (a human's
Main, derived, never stored) as distinct, mutually exclusive fields,
exactly one present. Nothing in the substrate ever classifies a
reference string; a request that offers none, several, or an untyped
target is refused naming the fields. Because no field ever admits a
union of types, a role and a user may share a spelling without the
engine ever confusing them. Resolution is total and judgment-free: a
role delivers to its bound session if active, else to its owner's Main —
a message to a role can never fall into the void, and fallback is
recorded, never disguised. Standing references (scheduled wakes, config,
guidance) hold role names and re-resolve at each use — late-bind the
future — while history records both the role and the concrete key it
resolved to at that moment — pin the past. Bindings change only by verb;
acting AS a role requires currently holding it; deleting a role makes
its name error by name, never silently reroute. Handles were the
degenerate ancestor of roles (a binding that could never move) and are
subsumed: `spawn --name X` registers role X bound to the new session.

**Verbs** (identical for operator and agents, origin-tagged):

| verb    | meaning |
|---------|---------|
| post    | append a message to a stream (a session's chat is its home stream) |
| read    | catch a cursor up on stream history since last seen |
| wake    | register or cancel a wake (a fact-triggered, prompt-bearing turn) |
| spawn   | instantiate a session from an archetype template + overrides |
| cancel  | interrupt a session's running turn |
| tune    | change a session's runtime knobs (model/thinking) or rename a stream |
| retire  | end a session deliberately |
| inspect | read the org: sessions, wakes, provenance, pending devices (admin) |
| enact   | instantiate a rail on a scope (process-form rails) |
| advance | attempt a rail transition, citing evidence |
| propose | stage a diff to the identity repo (skills/guidance/archetypes/rails) |

Closure rule: a feature expressible as a composition of verbs is a skill (e.g.
adversarial review = spawn + post + wake + read). A feature that needs
judgment is guidance. The verb set grows only for operations that are both
deterministic and not composable — rarely, and only by spec amendment.

**Origin and parity.** Every call carries an origin: `user:<id>` or
`agent:<handle>` (with the spawned-by chain). Agents and the operator invoke
the identical verbs; an agent DM is a wake with a prompt, an agent hiring a
worker is `spawn`, and agent-created sessions are visibly attributed and
traceable to the root of their spawn tree.

**Provenance and adoption on the client wire.** A session's `origin` is its
detailed provenance and stays exactly that; beside it every stream carries
`startedBy` — `user`, `agent`, or `substrate` — the origin's class already
collapsed server-side, because a client that parses provenance strings has
opinions about a closed set it does not own. Classification is TOTAL: a
`user:` origin means a human started the session, `agent:` means a colleague
hired it, and `process:`/`remedy:` mean the substrate stood it up on nobody's
ask; an origin outside the class set is a substrate defect, and it reads as
`substrate` rather than as nothing. `adopted` is chat-list membership and
nothing else — not a permission, not a lifecycle state. Agent- and
substrate-started sessions exist, are addressable, hold history, and appear in
`inspect` whether or not they are adopted; the chat list simply hides them
until their owner adopts one, so an org that hires busily does not bury the
human's own conversations. User-started sessions are always shown. Adoption is
a `tune` write (`adopt`/`unadopt` through session-control), gated by the same
ownership every other control on a session is, and it pushes `stream_updated`
so live catalogs converge without a reconnect.

## Coordination: wakes (fact-shaped comms)

Current beliefs layered on the primitive: `dueAt` is MANDATORY on every wake —
conditions are an optimization over the timeout, never a replacement, so no
intent is ever lost to a missed event (`firedBy` names condition vs fallback).
Harness-internal subagent fan-out is parent-owned opaque machinery the
substrate may SEE but never EXPECT anything of: START/STOP markers attribute
to the parent, a parent can wake on its own spawn's stop (with the mandatory
timeout as capture-gap fallback), and `subagent_*` facts are observability-only
at the registration boundary (contract: `subagent-markers-v1.md`). In draft:
the effort-without-effect check-in — a dispatch-armed bracket that probes the
holder's WORKTREE (effect, not effort) and routes an evidence-first decision
to the assignment's opener (`effort-without-effect-checkin-v1.md`).

Every wake carries an origin from a CLOSED class set (T3): `user:<id>` (a
human), `agent:<handle>` (a session), `process:<name>` (automation — cron,
CI, webhooks — named but not authenticated, with standing to wake and
cancel its own wakes and nothing more). The origin is stamped into the
model-visible prompt as a return address; provenance is orthogonal to
authority — guidance forbids treating any class as noise.

Between agents there are no calls and no awaited promises (T8). The unit of
coordination is the **wake**: a durable registration that delivers a prompt to
a target session when a condition holds. Immediate delivery is a direct
message; a delayed wake is a scheduled nudge; an external system is simply
another caller of the same verb. Every wake carries a prompt — there is no
content-free ping, because a wake with nothing to say has nothing to do.

Delivery is coalesced and idle-time only: a wake becomes one enqueued turn
through the session's lane when it is idle, and multiple triggers while a turn
runs collapse into a single wake. Wakes are durable — a pending wake survives a
daemon restart and fires on recovery — and delivery is at-least-once with
exactly-once enqueue (a wake is bound to the turn it generates, so a crash on
either side of the delivery window yields exactly one enqueued turn, never
zero, never two).

Rooms (multi-participant streams with membership, mentions, and read cursors)
are a designed layer over this same delivery path: a room is a stream, a
mention is a wake trigger, and posting to a room is `post`. Rooms make agent
chatter natively observable in the chat client, because a room is just another
stream on the same wire. Ticketing, scheduling, and similar external systems
are clients of the wake verb, not substrate features.

## Law: constitution, rails, guidance

Rules bind in three tiers (T4), strongest first:

- **Constitution** — substrate mechanics that protect the system from the org
  (dispatch chokepoint, no-self-wake, spawn/headcount caps, origin tagging).
  Owner-only; not reachable by `propose`.
- **Rails** — deterministic rules over structured facts, authored as
  declarative files in the identity repo, proposable by agents and merged by
  the operator. A rail is a guarded rule in one of three forms: an *invariant*
  (a stateless predicate on a verb call), a *reaction* (event → action), or a
  *process* (an evidence-gated state machine, `enact`/`advance`). All compile
  to one guarded-transition core the daemon executes; a resolver form selects a
  value (e.g. which model or reviewer) rather than allow/deny. Guards predicate
  only on structured facts — caller identity, origin, existence of referenced
  messages/evidence, counts, prior transitions — never on message content.
- **Guidance and skills** — prose for judgment, where the rule requires
  understanding content or intent. Prose is not enforcement.

INVARIANT — rails never add guidance. A rail contributes ZERO bytes to any
model's context: no standing sections, no reminders, no injected
obligations. Inference is nondeterministic and finite-attention; feeding it
more prose both pollutes the context and changes behavior it cannot
guarantee — which is the exact failure this system replaces (inferenced
governance that agents simply ignored). The ONLY text a rail ever emits is
the refusal reason at the moment it fires, delivered by the enforcing
mechanism itself (a denied verb, a refused tool call) — the agent learns
the law by hitting it, never by reading it. Anything an agent is meant to
read belongs in guidance or a skill; a "rule" that works only if the model
reads and honors it is guidance wearing a uniform, and rails refuse to
carry it.

The enforcement point is the verb dispatch path: guards run pre-dispatch
(deny wins, refusals cite the rail by name so agents learn the law by hitting
it), and successful verbs append to the event log, which reactions and process
rails match against. Rail-triggered actions are themselves origin-tagged verb
calls, re-guarded through the same path and cascade-bounded. The guard
language is total and non-Turing-complete (comparisons and existence/count
predicates over a finite fact API) — the standard policy-enforcement /
policy-decision pattern, placed at a chokepoint the daemon already owns.

Enforcement extends to the harness's tools by compiling local statutes into
the harness's own hook mechanism inside each generated home (deny-and-explain
on tool calls), and to the outside world through capability chokepoints
(external actions gated on rail state or on tokens minted by rail actions).
The result is defense in depth: gateway rails govern the org's verbs, compiled
hooks govern each agent's hands, external chokepoints guard the crown jewels.
Judgment stays with the agents; the substrate makes the *sequence* ungameable,
not the substance.

The litmus between tiers: a rule that names structured facts (who, what state,
what evidence, what count) can be a rail; a rule that requires understanding
content or intent is guidance. Instruction files shrink to taste and judgment;
everything enforceable becomes law that works even when the model skims.

Above all of it sits a line that must never blur: CONSTITUTION versus
STATUTE. The constitution is the set of rules that make the substrate BE
the substrate — messages cannot fall into the void, every mutation passes
the chokepoint attributed, reference seams are typed, history is never
trimmed, credentials never move, processes cannot mutate identity. These
are CODE, welded in on purpose, and they are not law-as-data waiting to
happen: they are already doing their job, and their inexpressibility as
data is a feature — no operator mistake, confused agent, or compromised
admin can write a file that turns them off. Changing the constitution is
forking the product. Statutes are everything where two sane operators
could rule differently — quotas, placement sets, tool gates, who may
retire what — and THOSE are data, fail-closed, refusing by name. The
litmus: if removing the rule would let the substrate lie, lose work, or
strand a message, it is constitution; if reasonable orgs could differ, it
is statute. And the composition rule that keeps the tiers safe together
is DENY-ONLY: a statute may add restrictions, never grant a permission
the constitution refuses. Data law can tighten the walls; nothing written
in a file can drill through one. The worst a bad statute can do is
over-restrict — loudly, safely — never under-restrict.

## Multi-user and devices

Users own identity and admin-ness; devices are approvable credentials attached
to a user (a device pairing with a claimed name is a request to join that
user; approval is the authentication ceremony). The first user is admin; every
approved device of an admin user is an admin device — admin follows the person,
not the hardware, so a wrong first device is recoverable. Admin grants
management verbs (approve/deny/revoke devices, promote users, control foreign
sessions), not a merged feed: chat catalogs, replay, and broadcast are owner-
scoped for everyone. Device tokens are a substrate-owned credential class,
distinct from harness auth and never mingled with it. This is operational
partitioning at the same trust level as a single-operator household — not
cryptographic isolation; stronger authentication, if ever needed, is per-device
key challenge-response, not passwords.

## Interop protocols

Call-shaped inter-agent protocols (request/response task delegation with held
continuations) are not the substrate's internal coordination model (T8). They
enter only two ways. **Outbound:** an agent may speak such a protocol as a
skill to reach an agent outside the factory; the substrate is unaware and
nothing is added to it. **Inbound:** a call-shaped protocol may be offered as
an optional front-door adapter, peer to the primary client wire, if and only if
it is a dumb translator (inbound task → verb through dispatch) whose task state
is a projection of the turn ledger, never a second source of truth — and, being
a capability, it ships as an adapter or fork per T7, never in the core. Such
protocols express no governance; the substrate's constitution, rails, and
ledger supply exactly what they lack.

## Runtime and reliability posture

The substrate does no work that must be fast except routing and recording;
inference is remote, tool execution lives in the harness processes, and the
agent-facing CLI runs in the agents' own shells. The daemon therefore stays
small and refuses management machinery (T5): no backpressure, no queue limits,
no self-healing beyond deterministic recovery. Bounds are counting rules
(headcount caps, wire rate limits, one turn per session). Everything is
observable — queue depth in session status, an append-only event log, lifecycle
events, health probes, and a scheduler/loop-lag watchdog — so that a stall is a
number and a reason, never a silent wedge. Reliability is expressed as
measurable health and fault-injection criteria, not as absolute claims; the
runtime provides uptime structurally (supervised, isolated, loudly-restarting
processes) rather than by manual firefighting.

## Reference implementation and portability

The specification and the wire contract are the product; any conforming
implementation is Tightbeam. The reference implementation is small by mandate
(T6) and carries its own continuity docs (architecture, patterns, handoff,
journal) so that an agent can hold it in context and, if needed, re-implement
it. Portability across runtimes is expected and cheap by design: the invariants
above, the wire contract, and the acceptance suite are the portable artifact,
and a runtime chosen for structural uptime (process isolation, preemptive
scheduling, supervision) is a valid and encouraged target. Historical spikes,
comparative analyses, and dated decisions that grounded these choices are kept
in `tightbeam-decisions.md` for provenance and for any future whitepaper.

## The document system (index and conventions)

This directory is a SYSTEM of documents with four kinds, and this section is its
map. Convention (binding): a capability spec that clears its review gate lands its
belief update in THIS file and its row below IN THE SAME CHANGE — the hub may not
lag the satellites.

- **Core (this file)** — beliefs about what the system IS. Mechanisms live in
  capability specs; history lives in the decisions ledger.
- **`tightbeam-decisions.md`** — dated decisions and their grounding; provenance,
  not current-state.
- **Capability specs (`*-v1.md`)** — one contract per capability: mechanism,
  invariants, required proofs. They gate (adversarial Sol-high review to READY),
  then implement, then merge.
- **Spikes, conformance, patterns** — investigation reports and cross-cutting
  doctrine; advisory unless promoted into a contract.

### Capability spec status

| Spec | Status |
|---|---|
| served-identity-home-projection-v1 | READY (5 rounds) — IMPLEMENTED, merged `9a84163` |
| tightbeam-credential-onboarding-v1 | READY — IMPLEMENTED with served identity, merged `9a84163` |
| subagent-markers-v1 | READY (7 rounds) — IMPLEMENTED, merged `cf83b4e` |
| observability-v1 (+ emission addendum) | RATIFIED; addendum READY (5 rounds) — IMPLEMENTED, merged `5ae730c` |
| harness-adapter-seam-v1 | READY (10 rounds) — IMPLEMENTED, merged `09028a0`, e2e smoke 8/8 |
| effort-without-effect-checkin-v1 | SUPERSEDED by `effort-checkin-v2.md` (v1 implementation merged `816f724`; v2 replaced its dispatch-anchored git-motion semantics) |
| adjudication-deletion-amendment | RECORD (2026-08-12) — banners the 2026-08-05 adjudication deletion across the corpus; GAP-1 re-homed to `harness-support.md` |
| derived-model-catalog-v1 | landed (see decisions ledger) |
| escalation-substrate-v1, attest-v1, check-tier-v1, work-item-v1 (in accountability family) | landed |
| containment-v1 family, codex-gates-v1, rails-mechanism-v1 | landed |
| agentic-engineering-guidance-spec | living (guidance CONTENT blocks; conformance via archetypes tests) |
| client-e2e-v1 | READY (4 rounds) — implementation queued (clawline repo driver + identifiers) |
| production-machine-v1 | spec review (Fable, REVISE→amended) + code review (Opus 5 distinct, REVISE→revised) — IMPLEMENTED on branch production-machine-v1 at 7ecf02a; suite 1297/0 eezo+shrdlu; e2e smoke 7/7 on shrdlu twice; T-RECOGNITION is its tenet; awaiting Flynn verification |
| assignment-lifecycle-fallback-escalation-v1 | MVP contract — exact-hash independent `reviewed-clean` required before implementation |
| assignment-revocation-reason-v1 | implementation authority — candidate pending independent review |

Superseded or historical documents move to `archive/`; `wisdom.md` here is a
pointer — the working wisdom index ships in the kungfu bundle
(`wisdom-core.md`/`wisdom-meta.md`).
