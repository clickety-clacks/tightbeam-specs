# Artifact-record firing-turn carrier — v1

Status: **RULED — APPROVED (Flynn, 2026-07-29), stable requirements R1–R7; implementation cycle active.** Fail OPEN (R1); nullable recordedMessageId + recordedTurnEvidence with this doc's exact meanings (R2); tool-call-observed is observation-quality, never unforgeability (R3); clauses 8/11 + the C1 note amended per R4 (former exactness recorded unsatisfiable, not closed); artifact-kind completion gate preserved, no consumer treats lower classes as exact proof (R5); clause 12 separate and open (R6); Gibson remains NO-GO until the R7 activation gate passes. Gibson activation is gated on this
ruling and the fix that follows it (ROADMAP item 0a).

Governing context: `core-causality-fixes-v1.md` §C1 (which names an unforgeable
per-turn request carrier as out of scope and rejects concurrency-derivation as
proof), `conformance-handoff-ledger.md` clauses 8 and 11 (Lane: fix-artifacts),
and `harness-support.md` (the closed capability census).

---

## 1. The decision surface

### 1.1 What is broken right now

`lib/tightbeam/wire/router.ex:114-126` builds the agent call with no
`recorded_message_id` key. `Tightbeam.Artifacts.record/2` requires one
(`lib/tightbeam/artifacts.ex:58-100`) and otherwise returns
`%{code: "invalid", message: "artifact-record requires provenance edges"}`. So
**every `artifact-record` from a real CLI client refuses, unconditionally.**

That refusal is not cosmetic, because org law depends on the verb succeeding.
`completion-requires-results-artifact`
(`priv/kungfu/agentic-engineering/rules/verification.toml:20-35`) denies a coder's
completion attest until a `report` artifact is recorded, and its remedy wakes the
holder with a prompt telling them to run `tightbeam artifact-record`. The verb
refuses, the completion stays denied, the remedy fires again. A correct agent is
held in a loop it cannot exit, which is why the shrdlu run needed the org-law
workaround (`eb0ea2b`) to make progress at all.

### 1.2 The structural fact that decides this

**Tightbeam has no gateway→CLI channel that varies per turn.** Every candidate
was checked against current main (`6fe6062`):

| Channel | Granularity | Why it cannot carry a turn |
|---|---|---|
| `.tightbeam-session` `{url, token, sessionKey}` | per **workdir**, converged at placement | Written by `Placement.holder_workdir/2` (`lib/tightbeam/placement.ex:185-210`) through `ensure_workdir/4` (`:673`, `:690`), which rewrites only on content change. Every turn in the session shares one file, as does any operator shell in that directory. |
| Harness process environment | per **adapter spawn** | `common_env`/`remote_env` are fixed in `prepare_launch` (`lib/tightbeam/placement.ex:1105-1130`). The adapter is keyed `{harness, identity, host}`, so its env cannot even name the session. |
| The projected home (rails artifact) | per **{host, harness}** | `Homes.home_path(base_dir, host, harness)` (`lib/tightbeam/placement.ex:1114`). Shared across every session on that host. |
| The prompt text | per turn, but **model-mediated** | A secret the model can read is a secret the model can copy into another session, paraphrase, or drop. It is not unforgeable and it is not reliable. |
| `PreToolUse` hook | per **tool call** | The only per-call substrate touchpoint. But it flows CLI→gateway as an observation; our projection cannot rewrite the command it observes. |

The consequence is blunt: **the "unforgeable per-turn request carrier" §C1 names
as a wire change does not exist as something the request can carry.** Any new
wire field would be filled in by the agent, which makes it forgeable — precisely
what the forensics-v2 boundary discipline §C1 invokes exists to strip. What the
substrate *can* have is a per-tool-call **observation** whose turn is resolved at
observation time.

### 1.3 The second structural fact: "hookless" is a per-call property

Both registered production harnesses have `PreToolUse` today. The registry is
`[Claude, Codex]` (`lib/tightbeam/harness.ex:72`); Claude receives it via
`settings.json` and Codex via `hooks.json` plus the `CODEX_CONFIG`
`bypass_hook_trust` spawn seed (`lib/tightbeam/harness/codex.ex:170,180,228,242,589-598`).
`harness-support.md` CAP-007 records both as PARITY.

So there is no hookless *harness*. There are, unavoidably, hookless *calls* — an
`artifact-record` the hook does not observe:

- the agent invokes the CLI from inside a script it wrote, so the hook sees
  `bash build.sh` and the command text never appears;
- a non-`Bash` tool path, or a vendor tool-name change after an auto-update;
- an operator shell in the workdir, which is outside any harness;
- Codex hook trust regressing after a version bump (the seam is version-probed,
  not guaranteed — `permission-seam-spike.md`).

**A design that only works when the hook observes the call is a design that fails
on its own default path.** This is what makes the fails-open/fails-closed question
load-bearing rather than a corner case, and it is the single most important input
to the ruling.

### 1.4 What Flynn is being asked to rule

1. **Does `recordedMessageId` keep asserting exactness?** As written
   (`NOT NULL REFERENCES messages(id)`, `lib/tightbeam/artifacts.ex:19`) it claims
   an exact firing turn with nowhere to put a qualifier. Clause 11 demands exactly
   that. Section 1.2 shows exactness is unobtainable for the hookless calls in
   §1.3, and §5 shows it is unobtainable on Codex *at all*.
2. **Fails-open or fails-closed** when the substrate cannot establish the edge
   (§3).
3. **Clause 11 as written is unsatisfiable on the current harness matrix** and
   must be either amended to §C1's standard or left open with a recorded reason
   (§6). This proposal cannot close it honestly by any mechanism.

---

## 2. Recommendation

**Fail open, with the observation quality recorded as a first-class column, and
use the hook seam as the best available observation.** Concretely:

- `recordedMessageId` becomes **NULLABLE**.
- Add `recordedTurnEvidence TEXT NOT NULL` with a closed three-value domain:
  - `tool-call-observed` — a substrate-reserved `PreToolUse` hook observed this
    session executing a `tightbeam artifact-record` command, and the turn was
    resolved from the ledger **at observation time**;
  - `session-concurrent` — no hook observation; a turn was running on the caller's
    session when the request arrived. This is the parked derivation, retained but
    honestly labelled as concurrency;
  - `none` — no hook observation and no running turn. `recordedMessageId` is NULL.
- `artifact-record` **accepts in all three cases** and never refuses on provenance.

Rationale, in the order it matters:

**The substrate records; inference acts.** Refusing produces no row, which is
strictly less truth than a row carrying a weaker, labelled edge. The artifact row
is a pointer plus provenance, not an authorization — nothing in the substrate acts
on `recordedMessageId` today.

**Nothing downstream weakens.** The only gate over artifacts is
`assignment.artifact_kinds` (`lib/tightbeam/rules.ex:1111-1117`), which resolves
through `Artifacts.recorded_kinds/3` (`lib/tightbeam/artifacts.ex:123-133`) on
`kind`, `workItemId`, and `createdBySession`. It never reads
`recordedMessageId`. A weaker turn edge cannot weaken the completion gate.

**The cost of deferring rises.** `recordedMessageId` currently has exactly one
reader — its own index (`lib/tightbeam/artifacts.ex:31`). Nothing joins on it.
Changing its shape is cheap today and expensive once the topology readers clauses
33 and 40 anticipate exist.

**It follows a precedent Flynn already ruled.** §C1 established that a nullable
value paired with an explicit statement of *how the substrate looked* is the
honest shape for a fact the substrate observes but cannot prove. The artifact case
needs three values rather than C1's `createdContextKnown` bit because there are
three distinct observation qualities, not two.

**It is minimum-safe.** No framework, no new table, no carrier protocol: two
column changes, one substrate-reserved hook entry, one short-lived correlation
window. The hook entry reuses the shipped gate shape
(`lib/tightbeam/rails.ex:215-226`), so a Bash call that is not an
`artifact-record` pays one local `grep` and exits — the same cost every statute
already imposes.

**What this recommendation does not do:** it does not close clause 11. See §6.

---

## 3. Fails-open versus fails-closed

### 3.1 The case for fails-closed

`artifact-record` refuses unless a carrier establishes the firing turn.

- The `NOT NULL` exactness claim survives intact. Every artifact row that exists
  is trustworthy without qualification, and no reader has to branch on confidence.
- Clauses 8 and 11 close literally, on the calls that succeed.
- It is the conservative reading of substrate neutrality: a substrate that cannot
  establish a fact should not record a guess.

**The org-law consequence, named.** Under fails-closed, every hookless call in
§1.3 becomes an unsatisfiable obligation.
`completion-requires-results-artifact` denies the coder's completion and wakes
them to record a report; the record refuses; the deny repeats. The holder cannot
progress, cannot surrender the obligation, and has no operator-visible reason —
the refusal says "requires provenance edges", which names a substrate internal,
not anything the agent can act on. Supervision then prods and escalates to the
owner (`escalation-substrate-v1.md`), converting a substrate gap into owner
attention on a work item that is not actually stuck.

That is a **dark-factory violation**: the agent is behaving correctly, the
substrate silently blocks it, and recovery requires an operator to edit org law.
It is also not hypothetical — it is the live linux-run defect (ROADMAP 0a2) and
the reason `eb0ea2b` exists.

Fails-closed also makes the completion gate **harness-dependent** in a way
`harness-support.md`'s framing rule forbids leaving unrowed: on Codex, where no
mechanism reaches exactness at all (§5.2), a fails-closed carrier would make
`completion-requires-results-artifact` permanently unsatisfiable for every Codex
coder. Codex is the primary coding harness (ROADMAP, Codex parity section).

### 3.2 The case for fails-open

`artifact-record` accepts and records the provenance class it achieved.

- The verb works for every agent on every harness on every path, which is what
  makes the artifact-gating statutes operable at all.
- The substrate stops discarding a fact it holds. §C1's own framing — the defect
  is *discarding* what the substrate knows — argues for recording the weaker edge
  with its qualifier over recording nothing.
- Consumers that need exactness filter on `recordedTurnEvidence =
  'tool-call-observed'`. Consumers that need "did this session produce a report on
  this work item" — the only consumer that exists — are unaffected.

**What it costs clauses 8 and 11.** Clause 8 requires the router to "attach the
exact firing `messages.id`"; clause 11 requires the dispatch owner to "bind the
current committed artifact-record turn's `messages.id` onto the call and prove
that exact ID reaches the persisted artifact row." A qualified, nullable column
does not deliver exactness on the `session-concurrent` or `none` rows. **Under
fails-open both clauses remain open unless amended.** The proposal does not
pretend otherwise.

**Is the qualified shape conformant with §C1's precedent?** Yes, structurally. C1
ruled that one nullable column cannot carry two meanings and therefore paired
`createdInTurnSeq NULL` with `createdContextKnown NOT NULL DEFAULT 0`, whose
documented meaning is "the substrate looked" and explicitly *not* "causal truth is
known". `recordedTurnEvidence` is the same move with a three-valued domain, and it
respects the same discipline: the column states the substrate's observation
method, never a causal claim the observation cannot support. Pre-migration rows
land `none` for the same reason C1's pre-existing rows land `known = 0` — they
must be distinguishable from rows where the substrate looked and found nothing.

### 3.3 Why fails-open wins

The deciding argument is §1.3. Fails-closed is defensible only if the carrier
covers the normal path. It does not: the same design must handle script-wrapped
invocations, operator shells, and post-update vendor drift, all of which are
ordinary occurrences rather than adversarial ones. A gate whose refusal path fires
on ordinary correct behavior is a band-aid over the missing channel identified in
§1.2, not a fix for it.

Fails-closed would additionally make a live shipped statute unsatisfiable on the
primary coding harness. That is a product outage justified by a provenance edge
nothing currently reads.

---

## 4. Mechanisms, compared

### 4.1 (i) `PreToolUse` hook-seam correlation — RECOMMENDED as the observation

A **substrate-reserved** `PreToolUse` entry, sibling to the existing Codex spawn
wiring-check probe (`Tightbeam.Rails.probe_entry/0`, `lib/tightbeam/rails.ex:129-131`)
and independent of org law. It reuses the shipped gate body shape
(`lib/tightbeam/rails.ex:215-226`): `grep` the tool input for a
`tightbeam artifact-record` invocation, exit 0 immediately if absent, otherwise
call the gateway and exit 0.

The gateway, on that call, resolves the caller session's running turn from the
ledger and opens a short correlation window holding **the `messages.id` observed
at that moment**. The subsequent wire `artifact-record` binds the window's message
and records `tool-call-observed`.

**What this fixes relative to the parked derivation (§4.3):**

- *False positive closed.* §C1's named false positive is "a SEPARATE request on
  the same session token while a turn runs." An operator shell is not inside the
  harness, emits no hook, and therefore opens no window — it records
  `session-concurrent` or `none`, and is distinguishable in the row.
- *Cancel false negative closed.* Cancel terminalizes before the kill
  (`lib/tightbeam/session_lane.ex:111-116`: `Ledger.finish(…, "canceled")` then
  `Process.exit(task_pid, :kill)`), so a request arriving after cancel sees no
  running turn. The window already holds the message captured at hook time, so a
  legitimate mid-work record is no longer refused or misattributed.
- *Turn-boundary drift closed.* Capturing at observation time, not at request
  time, means a slow command that spans a turn boundary still binds the turn that
  launched it.

**What it does not fix — the join.** The window is correlated to the arriving
request by session and time, not cryptographically. Three joins were considered:

- *Exact command text.* The hook sees the full command (Bash `tool_input.command`
  on both harnesses). Matching it against the wire request's params is fragile —
  quoting, `cd x && …` composition, several records in one command — and is
  rejected.
- *Open window.* Recommended: any `artifact-record` from that session while the
  window is open binds the captured message. This is a narrowed concurrency claim,
  and the narrowing is real (a window exists only because the turn was observed
  invoking the verb), but it is **not proof**, and `tool-call-observed` must be
  read as "the substrate observed this turn invoking this verb", never as
  "unforgeable".
- *Nonce injection.* The hook mints a nonce the CLI then presents. This is the
  only shape that would be genuine proof, and it requires mutating the tool input.
  Unavailable on Codex — `harness-support.md` CAP-008 records Codex 0.144.x
  `PreToolUse` as deny-only, and the 0.145.0 spike confirmed the protocol is
  allow/deny (`permission-seam-spike.md`). Unverified on Claude; the vendor may
  support an updated-input field, but `harness-support.md` maintenance rule 2
  forbids recording that as a capability without proof. **Named here as the probe
  that could later upgrade one harness to real proof, not as an available
  mechanism.**

**Live evidence.** `PreToolUse` fires for Bash and genuinely blocks
pre-execution, attributed by the agent to the runtime rather than to itself, on
Claude on both Linux and macOS
(`~/shared-workspace/tightbeam_ex/smoke-runs/2026-07-29-73d5817-satellite-macos-mac-0729a.md`
and `…-tars-gw-0729b.md`). Codex rests on the 0.145.0 spike, not on a live
Tightbeam e2e leg — see §5.2 and §7.3.

**Unmeasured cost, to be measured before build:** one gateway round trip per
observed `artifact-record` command, blocking pre-execution, over the network on a
satellite. The `grep`-and-exit shape keeps every other Bash call at local cost, so
the round trip is rare by construction, but no number is claimed here.

### 4.2 (ii) A wire-protocol carrier in the dispatch path — REJECTED

Rejected as **not constructible**, which is a stronger objection than a cost
tradeoff. Per §1.2 the CLI process has no per-turn input to put in a wire field.
Any such field would be filled by the agent, making it forgeable and therefore
exactly the class of parameter the boundary discipline strips. A carrier the
caller mints is not a carrier.

Two variants were considered and rejected on their own terms:

- **Per-turn rotation of `.tightbeam-session`.** The gateway rewrites the workdir
  file with a turn-scoped token at turn start. This does shrink the race, but it
  is rejected on three grounds: for satellite sessions `ensure_workdir/4` stages
  and `rsync`s over SSH on every change (`lib/tightbeam/placement.ex:690-728`),
  making a remote copy plus a new failure mode a per-turn event; the CLI reads the
  file at invocation time by walking ancestors (`cli/src/dispatch.rs:694`,
  `:1665`), so a long-running command started in turn N reads turn N+1's token and
  produces a *new* misattribution; and the file remains shared with any operator
  shell in the directory, so the §C1 false positive survives.
- **A turn secret in the prompt.** Model-mediated, therefore neither unforgeable
  nor reliable. Rejected.

**On `turns.requestRef`.** ROADMAP item 0a names it as raw material. It is
declared in the ledger DDL (`lib/tightbeam/ledger.ex:57`) and written and read
nowhere — the only other occurrences are two test-fixture DDL copies
(`test/ledger_test.exs:186`, `test/attention_tier_test.exs:302`). It is a
substrate-side slot on the turn row, so it can record what the substrate observed
about a turn's requests; it is **not** a channel to the CLI and therefore does not
change §1.2. It is available as the durable home for the correlation window in
§4.1 if a durable one is wanted, and this proposal takes no position on whether
the window needs to survive a gateway restart — a window outliving the turn that
opened it has no value.

### 4.3 (iii) The parked concurrency derivation — REHABILITATED, not as proof

Branch `remand/artifact-record-firing-turn` at `83b3602` (checkout
`/Users/mike/src/tightbeam_ex/scratch/wire-seam-lane`) adds
`Ledger.running_turn_message_id/2` and a `firing_message_edge/3` clause in the
router. Its own commit message correctly rejects it against §C1: the request
carries no turn identity, so a separate request on the same session token binds a
turn that did not fire it, and cancel's terminalize-before-kill lets an in-flight
request bind the next turn's message or none.

That reasoning stands and **the derivation is not rehabilitated as proof**. It is
rehabilitated as the **`session-concurrent` fallback**: it is the best the
substrate can do when the hook did not observe the call, it is exactly §C1's
concurrency claim, and under this proposal it is recorded under a label that says
so. The precise defect the remand identified — "`recordedMessageId` is NOT NULL
and asserts an exact historical turn, so it has nowhere to put the qualifier" — is
what §2 fixes by giving the qualifier a column.

### 4.4 (iv) The workdir-file per-turn token — REJECTED

Covered in §4.2. Rejected for per-turn remote `rsync` cost, the read-time
misattribution race it introduces, and its failure to close the §C1 false positive
it was proposed to close.

---

## 5. Exact behavior per harness

The registry is `[Claude, Codex]` (`lib/tightbeam/harness.ex:72`; `Fixture` is
test-only). Every row below is the behavior of `artifact-record` under the §2
recommendation.

### 5.1 Claude

`PreToolUse` is projected into `settings.json` via `Rails.hook_settings/0`
(`lib/tightbeam/rails.ex:117-126`, applied at
`lib/tightbeam/placement.ex:976,1128` and `lib/tightbeam/credentials.ex:459`).

- **Bash tool call whose command text contains the invocation** — hook observes,
  window opens with the turn's `messages.id` captured at observation; the record
  lands `tool-call-observed`. Proven live on Linux and macOS tonight.
- **Invocation hidden inside a script** (`bash deploy.sh`) — grep misses, no
  window; a turn is running, so the record lands `session-concurrent` with that
  turn's message.
- **Operator shell in the workdir** — no harness, no hook, and typically no
  running turn; the record lands `none` with `recordedMessageId` NULL. It is
  accepted, and it is distinguishable from an agent record.

### 5.2 Codex

`hooks.json` is projected with the same compiled `PreToolUse` map plus the
reserved probe entry, and the adapter spawn seeds
`CODEX_CONFIG={"bypass_hook_trust":true}`
(`lib/tightbeam/harness/codex.ex:170,180,228,242,589-598`) — the trust gate is
already handled. The 0.145.0 spike confirms `PreToolUse` fires for both shell and
`unified_exec` with `tool_name` `"Bash"` and the full command in
`tool_input.command`, and that the deny protocol actually blocks
(`permission-seam-spike.md`).

Behavior is therefore identical to §5.1, **with one permanent divergence**: the
nonce-injection upgrade (§4.1) can never reach Codex, because Codex `PreToolUse`
is allow/deny with no input mutation (`harness-support.md` CAP-008,
`DIV-RAILS-FUTURE-RESERVED`). Codex tops out at `tool-call-observed`.

**Not yet live-proven in Tightbeam.** Tonight's runs were Claude-only — the
macOS scorecard records `settings.json` with five gates and *no* `hooks.json`. The
Codex hook path rests on spike evidence at a pinned version. §7.3 makes a Codex
leg a precondition of the gibson gate.

### 5.3 A harness with no hook surface

None is registered, and per `harness-support.md`'s framing rule no such row is
invented here. If one is ever registered, it inherits §5.1's second and third
bullets as its *only* behaviors: every record lands `session-concurrent` or
`none`, accepted, labelled, and never refused. Adding such a harness requires a
`harness-support.md` row and a negative test in the same change (maintenance rule
1); this proposal's fails-open posture is what makes that addition possible
without breaking `completion-requires-results-artifact`.

---

## 6. Spec consequences requiring a ruling

- **Clause 11 as written is unsatisfiable.** It demands the *exact* firing turn.
  §1.2 shows no channel delivers exactness for hookless calls, and §5.2 shows no
  mechanism delivers it on Codex at all. It must be amended to §C1's standard —
  the substrate records what it observed and how — or left open with this analysis
  recorded as the reason. It cannot be closed honestly by any mechanism in §4.
- **Clause 8** requires the router to attach the exact firing `messages.id`. Under
  §2 the router attaches the best observed edge together with its evidence class.
  Same amendment or same open status.
- **§C1's out-of-scope note** says upgrading to proof "requires an unforgeable
  per-turn request carrier: a WIRE change, named here, explicitly out of scope."
  §1.2 finds no such carrier is constructible on the current architecture. §C1's
  sentence should be read as identifying the gap correctly while overstating that
  a wire change would close it; if §C1 is revised, that is the correction.
- **Clause 12** (CLI `--work-item` still optional) is untouched by this proposal
  and stays open: `cli/src/args.rs:810-822` still parses it as optional. It is
  independent and should not be bundled into this ruling.

---

## 7. Migration and test notes

### 7.1 The parked branch

`remand/artifact-record-firing-turn` at `83b3602` is a local branch in the
`/Users/mike/src/tightbeam_ex/scratch/wire-seam-lane` checkout and is not on
`origin`. Reviving it requires, in order:

1. A one-line arity fix at `test/wire_seam_test.exs:78`, which calls
   `Rules.load!(System.tmp_dir!(), Map.keys(handlers), %{})`; main's
   `Rules.load!/2` (`lib/tightbeam/rules.ex:142`) takes two arguments, so the
   trailing `%{}` is dropped. A compile failure there is staleness, not a
   regression.
2. Merging current main into the branch and running the gates there —
   `reconcile-in-branch-before-merge`; main receives only a verified tree.

Under §2 the branch is revived as the `session-concurrent` fallback, not as the
answer. Its `Ledger.running_turn_message_id/2` becomes the fallback resolver, its
`firing_message_edge/3` router seam becomes the place where evidence class is
decided, and the `REMANDED` comment block is replaced by the evidence-class
contract. Its 94 lines of `wire_seam_test.exs` fail-before coverage are reusable.

### 7.2 What the fail-before proof looks like

Each of these must fail on `6fe6062` before the fix and pass after:

1. **The live defect.** An `artifact-record` over the real wire from a session
   caller currently returns `invalid / "artifact-record requires provenance
   edges"`. Fail-before is that refusal; pass-after is a persisted row.
2. **Hook-observed binding.** With the reserved hook installed, a simulated
   `PreToolUse` observation for session S during running turn M, followed by an
   `artifact-record` from S, persists `recordedMessageId = M` and
   `recordedTurnEvidence = 'tool-call-observed'`.
3. **Observation-time capture, not request-time.** Open the window during turn M,
   terminalize M, start turn M+1, then send the request: the row must hold **M**.
   This is the turn-boundary drift closure and it fails against any request-time
   derivation, including the parked branch.
4. **The cancel path.** Open the window during M, cancel (which runs
   `Ledger.finish(…, "canceled")` before the kill,
   `lib/tightbeam/session_lane.ex:111-116`), then send the request: the row holds
   M with `tool-call-observed`, and is neither refused nor NULL. This is the §C1
   false negative, asserted rather than described.
5. **The unobserved path.** No hook observation, a turn running: the row holds
   that turn's message with `session-concurrent`. No refusal.
6. **The no-turn path.** No hook observation, no running turn: the row persists
   with `recordedMessageId` NULL and `recordedTurnEvidence = 'none'`.
7. **Boundary strip.** An agent-supplied `recordedMessageId` or
   `recordedTurnEvidence` in `artifact-record` params is stripped at the router
   and does not land — the §C1 discipline, which is the whole reason a
   caller-selected ID is not proof.
8. **Migration.** Two column changes (`recordedMessageId` to nullable via the
   existing `@rebuild_ddl` path, `lib/tightbeam/artifacts.ex:41-45`; additive
   `recordedTurnEvidence`), existing rows land `none`, and the
   `ensure_table_shape/1` FK and column-shape assertions
   (`lib/tightbeam/artifacts.ex:328,341`) are updated in the same change.
9. **The gate does not weaken.** `assignment.artifact_kinds` returns the same
   kinds for a `none`-evidence row as for a `tool-call-observed` one —
   `Artifacts.recorded_kinds/3` reads neither column
   (`lib/tightbeam/artifacts.ex:123-133`). Preservation proof.
10. **Statute closure end to end.** A coder blocked by
    `completion-requires-results-artifact` records a report and then completes.
    Fail-before is the remedy loop of §1.1.

### 7.3 "Freshly proven" for the gibson gate

**No e2e leg exercises `artifact-record` today.** `scripts/feature_smoke.exs` and
`lib/tightbeam/client_e2e/**` contain no artifact coverage, and the T2a journey
list in `e2e-tier-map-v1.md` does not include it. The linux-run failure was found
by hand. So the gate cannot be met by re-running an existing leg — a leg must be
added.

The named leg: **T2a, a new final journey `artifact-record + completion-gate
closure`**, appended to `scripts/feature_smoke.exs`'s ordered list after the
enforced review loop. It drives a real coder turn to record a report artifact and
then complete, and asserts the persisted `recordedTurnEvidence` and
`recordedMessageId`. It belongs in T2a rather than T2b because it is verb-surface
behavior over real turns, and T2a already runs one leg per registered harness,
which is what forces §5.2's Codex proof to exist.

Gibson activation requires:

1. T1 green.
2. **T2a green on both legs** — Claude and Codex — with the new journey. The Codex
   leg is the load-bearing one: it converts §5.2 from spike evidence into a
   Tightbeam live proof, on the primary coding harness.
3. A **T3 satellite** confirmation that the hook observation survives the network
   hop, since the correlation call crosses SSH from a satellite. One
   satellite-hosted `artifact-record` landing `tool-call-observed` is sufficient.
4. `eb0ea2b`, the shrdlu org-law workaround, **reverted** — ROADMAP 0a2 pins the
   two as retiring together, and leaving it in place would make the shrdlu leg
   unfalsifiable for exactly the statute this fix restores.
5. A scorecard per `e2e-tier-map-v1.md` §Scorecards naming the legs run, the
   platforms, and any waiver.

Per `all-platforms-are-the-test-gate`, green on one OS is not green: the T2a run
must name its platform, and the T3 leg must cover the Linux/macOS pairing the
carrier will actually run on.
