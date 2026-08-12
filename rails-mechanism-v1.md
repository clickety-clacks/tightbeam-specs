# Rails substrate-mechanism v1 — script guards, remedies, turn-end sweep, legibility, satisfiability

Status: DRAFT r9 (Claude/Opus; hardened through the ensemble adversarial-review
rounds). This is the substrate-mechanism spec referenced by
`agentic-engineering-guidance-spec.md` §6
(«Substrate mechanism (separate spec)») and by `rails-and-guidance-roadmap.md`
§8. It makes roadmap phases **P4** (script effect), **P5** (remedies + rail-set
satisfiability), and **P6** (turn-end sweep) implementable by focused agents. It
is written against the roadmap **D1 = hybrid** ruling (Flynn, 2026-07-21):
predicates remain the always-on hot path; scripts are added.

Ground truth was read from the merged `main`: `lib/tightbeam/rules.ex`,
`dispatch.ex`, `event_log.ex`, `supervision.ex` (`evaluate/5`,
`notify_terminal/3`, `ladder_target/3`), `containment.ex` (`rail_profile/1`),
`assignments.ex` (`oldest_open/2`, `open_count/2`, `verdict_kinds/2`,
`list_attests/2`), `work_state.ex`, `wakes.ex`, `ledger.ex`, `placement.ex`,
`gateway.ex`. Sibling authorities this spec composes with, unchanged unless named:
`statute-engine-v1.md` r6 (the predicate engine), `check-tier-v1.md` r4 (verdict
facts), `escalation-substrate-v1.md`
(ratified to Flynn's model — the `escalate` outcome, `resolve/3`/`escalate/4`/
`consume/2` seam), `p3-observables-producers-v1.md` (verdict-independence facts +
producers), `wake-on-fact-v1.md` (durable `creatorSessionKey`),
`model-ringdown-pattern.md` (model-adjudication episodes / the session hold — the
ADJUDICATION-HOLD branch of the turn-end order, §D2), `observability-v1.md` r4 (the
derived-not-stored event model), `supervision-v1.md` / `supervision-impl-v1.md` r20
(the turn-terminal edge). Where this spec is silent, those govern.

Containment is a rails mechanism: adapter-level containment was ruled out
(Flynn, 2026-07-28; `containment-impl-v1.md` is reduced to that ruling's stub).
The containment profile template, the per-seam renderers, and the wrapper
contract are contractual HERE (§A3–§A4) and in the code
(`lib/tightbeam/containment.ex`, `cli/src/contain.rs`).

The dispatch-tier statute engine (`rules.ex` / `dispatch.ex`) is where every
mechanism below lives. The harness PreToolUse tier (`rails.ex`) is a separate
accident-grade tool-layer tranche (destructive-git matchers); this spec does NOT
touch it and adds no harness effect (§Non-goals G2).

---

## Invariants (the acceptance lens)

A conforming implementation satisfies every one of these. They are the review
lens; §Design and §Seams exist to make them true.

**I1 — HYBRID, PREDICATE-FIRST.** The predicate engine (statute-engine r6
`deny_when` over the closed fact registry) is unchanged and remains the
always-on evaluation for every statute. A script runs for a statute only after
that statute's predicate (if any) matches; a statute with no predicate runs its
script unconditionally on its verb. No statute change makes a predicate-only
gate slower or differently-ordered than today. Zero statutes carrying a
`[rule.check]` or `[rule.remedy]` ⇒ observably identical to statute-engine r6 (I extends r6
invariant 8 to the new fields).

**I2 — SCRIPTS ARE SYNCHRONOUS, CONTAINED, TIME-BOXED, VALUE-RETURNING.** A rail
script runs kernel-contained under the host OS's mechanism — Seatbelt on macOS,
Landlock on linux (§A4) — receives the dispatch call as JSON on
stdin, and returns exactly one token from a **declared** set on stdout with exit
0. It is time-boxed by a substrate default with a per-statute override; the box
is a pathology detector, never a limit on real work. A script NEVER blocks on
inference or on another session — a judgment is a predicate fact-gate plus a
remedy (I5), not a blocking script.

**I3 — FAIL CLOSED ON THE CHECK, AND NEVER FABRICATE THE VERDICT.** Every way a
script fails to return a declared token deterministically denies and names
itself: nonzero exit or crash → `script_error`; exceeding the time-box (process
group killed) → `script_timeout`; stdout not exactly a declared token →
`script_out_of_set`; the sandbox refusing to apply → `script_contained_refused`.
A denial never depends on any observability row landing (statute-engine r6
invariant 4, inherited).

«The substrate never guesses a value for a check it could not complete» is a
constraint on the **exit class**, and it is checkable only if the class the
substrate writes when it observed nothing is a value the wrapper cannot produce.
So `unreported` is reserved: it is written wherever a deny is reached without the
observation that would name it — the wrapper never reported a status, the child's
exit code was never seen, no script was spawned at all, or the substrate itself
crashed — and it is never written by the wrapper. Its presence is proof no verdict
was observed and its absence is proof one was. The `reason` is unchanged on every
such path, so fail-closed semantics and reason-reading consumers are untouched;
only the class splits. A class that collides with a legitimately observable one is
undetectable by construction — an `error:1` written because nothing was observed
reads exactly like a script that really exited 1 — so no consumer, test, or
reviewer can tell a fabricated verdict from a real one, and the invariant holds
only by the good intentions of whoever last edited the path.

**I4 — DENY / REMEDY / ESCALATE, NEVER ALLOW-REWRITE.** A statute's outcome
vocabulary at the dispatch tier is `allow | deny | remedy | escalate`. `allow`
is the silent pass. `deny` is statute-engine r6's refusal, unchanged. `remedy`
denies now and originates a producer (I5). `escalate` **delegates** to
`escalation-substrate-v1`: its **effect-free `resolve/3`** is the four-shape
in-fold read — `:allow` (waiver-sourced) | `{:allow, ruling_id}` (ruling-sourced →
the statute passes, the fold continues; `ruling_id` collected into `to_consume`) |
`{:deny,…}` (ruled-deny) | `{:needs_request, dr_id|nil}` — and the effect
`escalate/4` (called by the actor only when `dr_id == nil`) halts +
opens a decision-request + delivers to the owner, returning **only**
`{:decision_pending, id}`; on an already-open `dr_id` the actor re-returns
`{:decision_pending, dr_id}` without opening. No outcome mutates or rewrites the caller's arguments; no outcome grants a
call the constitution denies (r6 invariant 1, inherited — a rail may pre-empt a
constitutional denial, never reverse one).

**I5 — REMEDIES ORIGINATE PRODUCERS, ASYNC AND IDEMPOTENT.** A `remedy` effect
dispatches a `spawn`/`wake`/`assign` verb under a **substrate-reserved remedy
principal** the target verb constitutionally admits for that action (§C2 — incl.
`opener/1` and `serialize_principal/1`), denies the gated verb now, and returns
without waiting; the produced fact releases the gate on a later re-dispatch. The
episode lifecycle is a **CAS state machine** in `rail_remedy_episodes`
(`claimed→dispatched→live→closed`, atomic single-row UPDATEs fenced by `claimToken`,
TTL reclaim, §C3): only the claimant (after winning the pre-dispatch lease)
dispatches, a concurrent reader treats `claimed`/`dispatched` as in-flight, a `live`
producer is re-woken not re-spawned, and — the r6 invariant — there is **at most one
external dispatch effect per OCCURRENCE**: the dispatch's `wire_idempotency` key is
the occurrence key (which bumps on any terminal-state exit — `closed` reopen or
dead-`live` replacement — and is PRESERVED by a TTL-stale reclaim), so a
same-occurrence racing re-dispatch collapses to one producer (§C3).

**I6 — TWO FIRING EDGES; THE SWEEP HAS NO FALSE POSITIVES.** A turn-end-edged
statute fires both at its boundary verb (commission) and at the turn-end step
(omission), which is **folded into `Supervision.evaluate`** — one adjudicator, one
reaction per terminal, dedup'd by supervision's own watermark (§D1). The step acts
only when the base stall predicate holds (no running/queued turn, ≥1 open
assignment) AND the obligation is gate-unsatisfied, with **remedy XOR prod** (§D2).
The no-false-positive observable is a **self-scheduled continuation**
(`Wakes.self_pending_count > 0`, a pending wake with `sessionKey =
creatorSessionKey = holder` on wake-on-fact-v1's durable `creatorSessionKey`
column, not the mutable origin), not any pending wake — a user reminder or
supervision prod does not suppress the step.

**I7 — SILENT WHEN SATISFIED; EVERY NON-PASS AND EVERY SCRIPT/REMEDY/SWEEP IS
LEGIBLE.** A satisfied gate emits nothing to the agent (no context injection, no
acknowledgment — `rails.ex` THE INVARIANT, inherited). Every non-pass emits an
`events` `kind="denied"` row whose payload names the statute, edge, reason, and
gated ref. Every script invocation, remedy fire, and sweep decision — pass or
fail — emits one `lifecycle_events` row (open CHECK, no migration). Rating is
derived, never stored (observability-v1): firing rate, remedy rate, and sweep
outcomes are queries over these rows.

**I8 — RAIL-SET SATISFIABILITY IS A LOAD GATE.** At load the full statute set is
checked (§F): F1 rejects a verdict-fact gate whose required kind has no producer in
the **closed static 3-source registry** — in-statute remedies ∪ `producers.toml`
entries ∪ gates annotated `external_producer=true` (no blanket "any agent-created
review counts") — the true dead fact (naming the single gate + kind); F2 rejects a
remedy
whose action a handler cannot constitutionally admit, or that a pure-deny statute
provably blocks, or that forms a producer cycle (naming both statutes). Either
rejects the boot, loudly. Single-statute validation cannot catch the joint
classes. Runtime-state deadlocks (a quota exhausted at the instant a remedy fires)
are explicitly out of load scope, caught at runtime by the loud `blocked`
`rail_remedy` outcome + remedy-rate signal and by the turn-end step's escalation
(§F states this bound).

**I9 — RAILS ARE SOFTWARE, RESTART-PICKUP.** Statutes and their scripts are
git-tracked artifacts in the identity repo; a change is a reviewed, attributed,
revertable, bisectable diff. Loading is boot-time and fail-closed (r6 inherited);
there is no live reload — a rail change is picked up at the next gateway restart,
exactly as statute and rail loading works today.

---

## Non-goals (do not build)

- **G1 — No live reload.** Restart is the pickup mechanism (I9). No file-watch,
  no `reload` verb, no hot-swap of `:persistent_term`.
- **G2 — No allow/rewrite at the harness tier.** `rails.ex` PreToolUse is
  vendor-limited to refuse (exit 2); this spec adds no harness effect and does
  not touch `rails.ex`. The `allow | deny | remedy | escalate` vocabulary is the
  **dispatch tier** only.
- **G3 — No review-gate-on-guidance-change.** Requiring a verdict before a
  guidance/rail change loads is an org-authored rail shipped **off**
  (guidance-spec §6 «Changing guidance is an org policy»). The mechanism must not
  hardcode it.
- **G4 — Remedy idempotency splits across two tables by role.** The
  `rail_remedy_episodes` CAS table (§C3) owns the episode *lifecycle*
  (`claimed→dispatched→live→closed`, TTL reclaim, verdict-landed close) — which the
  `wire_idempotency` forever-ledger cannot express. The producer *dispatch* is
  deduped through `wire_idempotency` normally, keyed on the episode key (finding
  2d — one ledger, normal semantics). Two tables, two roles, no conflict. (Revised
  across r1→r4: r1 "no new table" → r2 episodes-only → r4 episodes + wire ledger.)
- **G5 — No blocking judgments.** Scripts never await inference or a session
  (I2). The async judgment is predicate-gate + remedy.
- **G6 — No per-operation containment telemetry.** Kernel denials inside a
  script are EPERM in the script's own output, never substrate-parsed
  (§A3). The substrate observes only the script's exit
  class.
- **G7 — No new escalation policy or engine.** The `escalate` effect delegates
  to `escalation-substrate-v1`; this spec defines the effect token and the
  hand-off, not which conditions escalate, and not that engine's internals.

---

## A. Script guards (P4)

### A1. The statute grammar extension (dispatch tier, `rules.ex`)

A `[[rule]]` in `identity/rules/*.toml` gains three optional constructs. The
existing `name`, `verb`, `deny_when`, `text` keep their r6 meaning exactly.

```toml
[[rule]]
name  = "reconcile-before-build"
verb  = "attest"
text  = "your branch is behind main; reconcile before building on it"
edges = ["verb"]                 # default ["verb"]; may add "turn-end" (§D)

# optional predicate PRE-FILTER (r6 deny_when, unchanged). When present, the
# script runs ONLY if every condition holds; when absent, the script runs on
# every call to `verb`. Predicates stay the hot path (I1).
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  { fact = "assignment.holder_archetype", op = "eq", value = "coder" },
]

# NESTED under the [[rule]] element — TOML subtable headers, NOT root tables.
# `[rule.check]` / `[rule.check.effects]` attach to the [[rule]] immediately
# above; written as root `[check]`/`[check.effects]` they would be rejected by
# the loader's unknown-root-key validation and the rule would carry no check.
[rule.check]
script  = "reconcile-before-build"   # basename under identity/rails/scripts/
returns = ["reconciled", "behind"]   # the DECLARED set (non-empty, unique)
timeout_ms = 5000                    # optional; default 5000; 1..60000
[rule.check.effects]                 # maps EACH declared return to an effect
reconciled = "allow"
behind     = "deny"                  # or "remedy" (needs [rule.remedy]) or "escalate"
```

Every nested table in this spec is written as a `[rule.…]` subtable header
(`[rule.check]`, `[rule.check.effects]`, `[rule.remedy]`, `[rule.remedy.params]`);
a bare `[check]`/`[remedy]` is a root table and a load error. The conformance
smoke set's C5 fixtures use `[[rule]]` with these nested subtables (not
`[[statute]]`, not flat `script`/`deny_when_return`) — the two specs are aligned
on this grammar.

Check scripts are sensors: they read state that already exists
(verification-papertrail-v1 §Ruling 1's work-vs-checking line). A script
that performs work to learn its answer — a `git fetch`, a build, anything
that brings new state into existence — is work in the sensor slot, not a
slow check. The reconcile example reads the refs as they stand (a stale
`origin/main` only makes the check more conservative, never wrong);
fetching remains the holder's work. This is also what keeps `timeout_ms`
honest: local reads finish in milliseconds, so the default bounds a
malfunction, not a cost estimate.

Rules for the extension (validated at load, fail-closed, r6 §Validation regime —
file-and-rule-named errors):

- A statute MUST carry at least one of `deny_when` or `[rule.check]`. A statute
  with neither is a load error.
- `edges` is a non-empty subset of `{"verb","turn-end"}`; unknown members are a
  load error. `"turn-end"` is legal only on statutes whose `verb` is an outcome
  verb the sweep can synthesize (§D3: `attest`); `"turn-end"` on any other verb
  is a load error.
- `[rule.check].script` matches `^[a-z0-9][a-z0-9-]*$` and MUST resolve to an
  existing, executable regular file at `<base_dir>/identity/rails/scripts/<script>`
  at load; a missing or non-executable script is a load error (bad law stops the
  boot). The scripts directory is the identity repo, git-tracked (I9).
- `[rule.check].returns` is a non-empty list of unique strings matching
  `^[a-z0-9][a-z0-9-]*$`.
- `[rule.check.effects]` MUST map **every** member of `returns` to exactly one of
  `allow | deny | remedy | escalate`; a return with no effect, or an effect for a
  non-declared return, is a load error. An effect of `remedy` requires a
  `[rule.remedy]` table (§C); an effect of `escalate` requires the escalation
  engine (`escalation-substrate-v1`, ratified to Flynn's model) to be present —
  statute loading gates on that spec's adversarial review landing clean (a load
  error naming the dependency until then), not on ratification (which is done).
- `[rule.check].timeout_ms`, when present, is an integer in `1..60000`.
- Predicate-only statutes MAY carry `effect = "deny" | "remedy" | "escalate"`
  (default `"deny"`) selecting the effect on predicate match — this generalizes
  r6's implicit deny-on-match without changing the default. `remedy`/`escalate`
  carry the same table requirements as above.

**Script gates carry no verdict fact (the script-K rule).** A script-effect
statute is satisfied by the script returning an `allow`-mapped token, NOT by a
verdict fact landing. A script gate whose effect is `remedy` therefore does NOT
declare a `produces` verdict kind (§C1) and is EXEMPT from the F1
producer-existence check (§F): its remedy runs a producer that changes what the
script re-reads on the next dispatch (e.g. a reconcile remedy merges main so the
ancestry script then returns `reconciled`). Only verdict-fact gates
(`deny_when` over an `assignment.*verdict_kinds` fact) participate in F1.

### A2. The invocation contract

**V1 execution scope (finding 10, RULED).** Rail scripts (and p3's producer
verbs) execute on the **gateway host only**. Containment is applied locally where the
gateway runs, so a holder whose workdir lives on a **remote** host is a **named
deferred gap** owned by placement — the gate fails closed (`script_error`) rather
than executing against a checkout it cannot see; v1 ships with holders co-located
on the gateway host. Remote-holder rail execution is future work.

When a statute's script fires (predicate matched or no predicate), the substrate:

1. Creates a fresh per-invocation scratch dir `<base_dir>/rails/scratch/<uuid>`
   (mode 0700), `File.rm_rf!/1` on the way out regardless of outcome.
2. **Resolves the invocation context.** A script cannot find the assignment's code
   from the raw call alone (finding 11), so the substrate resolves, from the call's
   `$assignment` (check-tier's cached dependency) joined to the holder session row:
   `holder_key`, `holder_workdir` (via **`Placement.holder_workdir/2`** — p3's
   single public workdir seam; the r3 `Gateway.session_workdir/2` promotion is
   dropped, finding 10), the `host` the holder runs on, and
   `holder_harness`/`holder_archetype`. For a call with no assignment these are
   `null`. If `host` is not the gateway host, the script is not run (the deferred
   gap above).
3. Computes the profile `Containment.rail_profile([scratch_dir])` — read-anywhere
   (covers the holder's checkout), write only the scratch dir plus the rail
   seam's one fixed grant, `/dev/null` (§A4). The renderer is named per seam:
   its grant list is deliberately not shared with any other caller's, so no
   other seam's grants can widen the rail wall (`containment.ex`). (Network
   posture: §X6 — v1 rides the only implemented posture, open.)
4. Runs the script through the Rust custody wrapper (§A3), which spawns the
   contained child **in its own process group** (`setpgid`) — on macOS via
   `/usr/bin/sandbox-exec -p <profile> -- <scripts>/<script>`; on linux the
   script itself is the restricted child, the staged Landlock ruleset imposed
   in `pre_exec` (§A4, no helper binary) — stdin/stdout/stderr piped (not inherited — the
   script is not an ACP speaker), **CWD = `holder_workdir`** when resolved (else
   the scratch dir), env scrubbed to a minimal allowlist (`PATH`, `HOME`=scratch,
   `TIGHTBEAM_RAIL`=statute name; nothing else). CWD-at-the-checkout plus
   read-anywhere is what lets an ancestry / tests / files-touched / real-run check
   target the assignment's code; the write-wall keeps the check side-effect free.
5. Writes the call **and the resolved context** to the script's stdin as one JSON
   object, then closes stdin:

   ```json
   {"verb":"attest","origin":"agent:coder-3",
    "principal":"session:s_9f…","session_key":null,
    "params":{"assignment_id":"a_123","kind":"completion"},
    "context":{"holder_key":"s_9f…","holder_workdir":"/…/work/…",
               "host":"gateway","holder_harness":"claude",
               "holder_archetype":"coder"}}
   ```

   `principal` is serialized as `"<kind>:<value>"` or `null` (EventLog's
   convention). `params` is the raw params map. `context` is the resolved read
   (no `repo`/`repo_path` key — the checkout IS `holder_workdir`, at CWD); the
   script computes its own observables from the checkout at CWD.
6. Reads stdout to EOF; the wrapper enforces the time-box and returns the class.

### A3. The return contract and the fail-closed matrix (I3, normative)

**The custody wrapper (`tightbeam rail-exec`).** BEAM Ports cannot `setpgid` or
`killpg`, and `sandbox-exec`'s own nonzero cannot be told apart from the child's
(finding 11). So scripts run through the Rust `contain` module
(`cli/src/contain.rs`):

`tightbeam rail-exec --profile <SBPL> --timeout-ms <N> -- <script-path>`

The wrapper owns the process group and the kill, and **encodes the outcome class
in its OWN exit code** (disjoint from the child's), so the substrate classifies
from the wrapper's exit alone:

| wrapper exit | meaning |
|---|---|
| `0` | child exited 0; child's trimmed stdout is on the wrapper's stdout |
| `10` | the check produced no usable verdict. Normally the child exited nonzero and its code is on the wrapper's stderr — a child failure. The wrapper also uses `10` when it could not run the check to a verdict at all (it failed to deliver the call on the child's stdin, could not read its own stdin, or could not wait), in which case it writes no child-exit line and the substrate classifies `unreported` |
| `20` | `--timeout-ms` elapsed; wrapper `killpg(SIGKILL, -pgid)` — timeout |
| `30` | the containment could not be staged or applied (decided in `stage()`, before any child ran — §A4) — a containment refusal, distinct from `10` |

The wrapper: **stages the containment before the fork** (`stage()` — on macOS a
preflight of the SBPL against `/usr/bin/true`; on linux the Landlock ruleset
build, §A4), and a staging failure is exit `30` — refusal is a fact the wrapper
observed while nothing was spawned, never one parsed from output the judged
script controls. It then installs the signal discipline, `setpgid(0,0)` in
`pre_exec`, spawns the contained child (macOS: `sandbox-exec -p <profile> --
<script>`; linux: the script directly, restricted in `pre_exec`), waits with an
internal `--timeout-ms` timer; on timeout `killpg(-pgid, SIGKILL)` and exit
`20`. Once a child has run, no band-30 path exists. The substrate reads the
wrapper's exit + its stdout:

| Wrapper result | Class | Effect | Reason code | `script_exit_class` |
|---|---|---|---|---|
| exit 0 AND trimmed stdout ∈ `returns` | **pass** | per `[rule.check.effects]` | — | `returned` |
| exit 0 AND trimmed stdout ∉ `returns` (incl. empty) | fail | **deny + escalate** | `script_out_of_set` | `out-of-set` |
| exit 10 AND a `child exit: <N>` line on wrapper stderr (child nonzero, incl. an in-sandbox EPERM) | fail | **deny + escalate** | `script_error` | `error:<N>` |
| exit 20 (timeout) | fail | **deny + escalate** | `script_timeout` | `timeout` |
| exit 30 (profile-apply refusal) | fail | **deny + escalate** | `script_contained_refused` | `contained` |

Note the precise split (finding 4/C5): an **in-sandbox** denied write is EPERM
inside the child → the child exits nonzero → wrapper exit 10 → `script_error`.
`script_contained_refused` (exit 30) means the sandbox could not be applied at
all — a host mis-provisioning, not a script action. A "containment escape"
attempt therefore classifies as `script_error`, not `contained`.

**When the wrapper reports nothing (I3).** Every row above reads an observation.
Four paths reach a deny without one, and each records `unreported` rather than the
value the missing observation would have carried:

| Substrate-side outcome | Effect | Reason code | `script_exit_class` |
|---|---|---|---|
| wrapper exit 10, no `child exit: <N>` line on its stderr — the child's code was never seen | **deny + escalate** | `script_error` | `unreported` |
| the port never reported a status by `timeout_ms + 2_000`; the substrate closed it | **deny + escalate** | `script_timeout` | `unreported` |
| the invocation context could not be resolved (holder absent, non-local, or its workdir would not open) — no script was spawned | **deny + escalate** | `script_error` | `unreported` |
| the substrate itself raised or exited while running the check | **deny + escalate** | `script_error` | `unreported` |

**No sensor malfunction silently decides against work (Flynn's ruling,
2026-07-29; generalized the same day under dark-factory doctrine).** A bare
deny is reserved for the one case where the sensor actually answered "deny"
— a declared token mapped to `deny` by `[rule.check.effects]`. Every other
non-pass outcome — timeout, script crash, containment refusal, out-of-set
token, and all four `unreported` paths — is a malfunction: a clock, a
crash, or a misconfiguration decided, not a mind, and in a dark factory a
silently recurring deny is a stall nobody is watching. The call still fails
closed (every deny above stands, and never depends on any observability row
landing), but the substrate additionally hands the event to the escalation
engine exactly as an `escalate` effect would (G7's hand-off, no new policy
or engine) — naming the statute, the reason code, and the
`script_exit_class` — so a mind adjudicates the sensor: raise the ceiling,
fix the script, repair the host, reclassify the check as work. Two
dark-factory constraints on the hand-off: at most ONE live escalation
episode per (statute, `script_exit_class`) pair — a repeated identical
malfunction attaches to the open episode rather than duplicating it, so a
retry loop cannot storm the escalation engine — and the episode CLOSES
AUTOMATICALLY when a later evaluation of the same statute's check yields an
observed verdict (pass or genuine deny): recovery is automatic when the
cause heals, with no operator verb in the loop. A timeout may bound
waiting; a malfunction may bound a call; neither may be the last word on
work.

`unreported` is disjoint from every wrapper-produced class, including the
parameterised `error:<N>` (always digits). The wrapper therefore cannot emit it,
and its presence in a `rail_script` row is the recorded fact that no verdict was
observed. This is what separates the two producers of `script_timeout`: `timeout`
means the wrapper ran its own timer to expiry and killed the process group,
`unreported` means it never answered. The BEAM-side `duration_ms` does NOT
separate them — it is measured in the calling process, so a starved caller inflates
it past `timeout_ms + 2_000` on a run the wrapper genuinely enforced.

The wrapper is bound by the same rule on its own side of the seam: it writes the
`tightbeam rail-exec child exit: <N>` line ONLY for a child exit it observed. Its
stdin-delivery failure — the script never received the call it was to judge — is a
diagnostic in its own words plus exit 10, which the substrate classifies as
`unreported` by the first row above.

Only the `allow` effect passes silently. `deny`/`remedy`/`escalate` proceed to
§E (legibility) and, for `remedy`/`escalate`, to §C / the escalation engine.

### A4. Containment integration

Scripts run under `Containment.rail_profile([scratch_dir])` (`containment.ex` —
a pure template, identical-inputs-identical-bytes). The rail seam has its own
renderer, deliberately split from every other grant list so another seam's
grants can never widen the rail wall; beyond the scratch dir its only fixed
grant is `/dev/null` (shipped rail scripts redirect to the discard sink, and a
discard sink carries nothing out of the scratch root). `containment.ex` stays
the single authority on WHICH roots are granted; only the encoding is per-OS,
and the profile rides argv inline, never written to disk:

- **macOS — Seatbelt.** The profile is SBPL: deny-default writes, `allow
  file-read*` (covers the holder's checkout and the scripts directory; CWD is
  the checkout, §A2.4), open egress. The wrapper preflights the profile in
  `stage()` by applying it to `/usr/bin/true`, then spawns
  `/usr/bin/sandbox-exec -p <profile> -- <script>`.
- **linux — Landlock LSM**, via raw syscalls in `cli/src/contain.rs` (no
  library, no helper binary — the check script itself is the restricted child).
  The profile is a JSON grant envelope
  (`{"tightbeam_containment":1,"write_roots":[…]}`); the wrapper builds the
  ruleset in `stage()`, **before the fork**: ABI floor 3 (kernel 6.2+ — the
  lowest ABI that restricts `truncate(2)`), a fixed handled-rights set (no
  by-ABI masking, so every accepted kernel enforces identically), per-inode-type
  right masks (directories: the full write family; regular files:
  `WRITE_FILE|TRUNCATE`; device nodes: `WRITE_FILE` only — `/dev/null` is a
  character device, so this is the production arm), grant roots opened with
  `openat2(RESOLVE_NO_SYMLINKS)`. Any failure there is the exit-30 refusal,
  decided while nothing has been spawned. In `pre_exec` the child sets
  `PR_SET_NO_NEW_PRIVS` and `landlock_restrict_self`, then execs the script.
  Read, directory-read, execute, and network rights are left unhandled —
  unrestricted everywhere — the linux expression of the SBPL's `(allow
  file-read*)`/`(allow process-exec)` and the v1 open-egress posture.

A misbehaving script is itself contained and fails closed (guidance-spec §6
«Containment»).

---

## B. Hybrid dispatch — one dry decision function, two actors

**The three roles, pinned (finding 1).** There is exactly ONE decision function
and exactly TWO places a decision becomes an effect:

1. **`Rules.decide(db, call) :: {decision, to_close, to_consume}`** — THE decision
   function. It is **effect-free on enforcement**: it runs check scripts (§A) and
   writes their `rail_script` lifecycle rows (observability, §E3), but it fires **no
   remedy and no prod, opens no decision-request, consumes no ruling, and mutates no
   domain/work state** — those are the two actors' job (below). It selects the
   statutes for `call.verb`, filtered by `call[:edge]` (`:verb` default | `:turn_end`,
   §D), evaluates them in filename-then-table order (r6), and returns the first
   non-`allow` `decision`: `:allow | {:deny, error} | {:remedy, statute, ref, error}
   | {:escalate, statute, ctx, dr_id} | {:deny_escalate, statute, ctx}` — the fifth
   shape is the sensor-malfunction outcome (§A3: every non-pass script class): the
   denial stands AND the actor summons — (`dr_id` from `resolve/3`'s
   `{:needs_request, dr_id|nil}`), plus two pure-read lists **of the evaluated prefix**
   (the statutes evaluated up to and including the deciding one): **`to_close`** —
   statutes that INDIVIDUALLY passed AND have a `live` remedy episode for the subject
   (§C3.5), plus `{:episodes, statute, position}` entries for statutes whose check
   rendered an observed verdict (pass or token-deny) while a malfunction episode is
   open (§A3 auto-close — the actors hand recovery to the episode writer, which
   withdraws as `sensor-recovered`; nothing was decided, the question expired).
   Episode lifecycle ordering is owned by a SINGLE WRITER: every open, attach,
   and withdrawal is decided inside one serialized process, in arrival order —
   never in SQL, never across a process gap. The `position` is minted by the
   writer BEFORE the check runs (`decide` requests it at evaluation start;
   minting touches no episode state and is not an enforcement effect), and the
   actor's recovery hand-off withdraws only episodes whose newest summons the
   writer holds as OLDER than that position. Anchoring the cutoff before the
   observation is the load-bearing property: a verdict authorizes closing only
   episodes that existed when its check started, so a summons landing during or
   after the check — fresh or attach — is outside the authorized set by
   construction. Ordering state lives in the writer's serialized decision-plane
   state; `lifecycle_events` remains observability-only (§E3) and is never a
   decision input. Writer unavailability degrades safely: denials never depend
   on it, the summons hand-off fails soft as ruled, and recovery simply does not
   occur that evaluation — it resumes when the writer returns, recorded either
   way. The symmetric interleaving —
   a delayed summons opening after the sensor has already recovered — is ACCEPTED
   BOUNDED STALENESS, not a defect: the malfunction genuinely occurred and denied a
   call, so the summons is truthful, and the next healthy evaluation closes it; **`to_consume`** — the `ruling_id`s collected from every `{:allow,
   ruling_id}` (ruling-sourced allow) `resolve/3` returned in the prefix (a
   waiver-sourced bare `:allow` contributes none). Per statute: predicate first,
   script second (below).
2. **`Rules.evaluate(db, call) :: :ok | {:deny, error}`** — the LEGACY contract,
   byte-unchanged from statute-engine r6, a thin wrapper over `decide` that drops
   `to_close`/`to_consume` and maps the `decision`: `:allow → :ok`; `{:deny, e} →
   {:deny, e}`; and — for safety at any caller that is not an actor — `{:remedy, _,
   _, e} → {:deny, e}`, `{:escalate, …} → {:deny, deny_form}`, and
   `{:deny_escalate, _, _} → {:deny, e}` (the malfunction deny) **without firing**
   (closing and consuming nothing). Existing callers keep today's `:ok | {:deny,…}`
   behavior; only the two actors below enact effects, closures, or consumptions.
3. **The two actors.** `Dispatch.dispatch/3` (the **verb edge**) and
   `Supervision.evaluate/5` (the **turn-end sweep**, §D) are the ONLY places a
   decision becomes an effect. Both call `Rules.decide` and **close each episode in
   `to_close`** (§C3.5 — Dispatch at the verb edge, Supervision at the sweep,
   regardless of `decision` — a passed statute closes even when a later one denies).
   **Consumption is VERB-EDGE-ONLY (lattice H9): the SWEEP NEVER consumes.** A
   whole-fold `:allow` at the turn-end edge has **no handler to run**, so consuming a
   ruling there would spend it (`ruled→consumed`) with no execution behind it — a lost
   authorization. So `to_consume` is **ignored at the sweep** (§D2/§D3); only the verb
   edge consumes. At the verb edge, **only on a whole-fold `:allow`, consume each
   ruling in `to_consume`** before invoking the handler. `to_consume` is a list of
   **ruling row ids**; the consume is escalation's **`consume/2`** — a single-statement
   CAS per row (`UPDATE … SET status='consumed' WHERE id=? AND status='ruled'`).
   **CAS-loss behavior (escalation r4/r5, verbatim-compatible):** the actor CASes EVERY
   `to_consume` row; **any loss → the verb is DENIED** (fail-closed; a concurrent
   consume/withdraw/auto-withdraw or a vanished ruling), and **already-consumed
   entries stay consumed** — consumed-on-attempt covers the whole batch, so a retry
   re-escalates the still-unconsumed rulings and finds the consumed ones terminal.
   Only when every row CAS-wins does the handler run. Then act on the `decision`:
   `:allow` → run the handler; `{:deny, e}` → deny (extended payload §E);
   `{:remedy, …}` → fire the remedy exactly once (§C2/§C3), then deny with
   `reason="remedy_fired"`; `{:escalate, statute, ctx, dr_id}` → on `dr_id == nil`
   call `escalate/4` (open the decision-request, deliver to the owner; returns
   **only** `{:decision_pending, id}`); on `dr_id != nil` (already-open) re-return
   `{:decision_pending, dr_id}` without opening; `{:deny_escalate, statute, ctx}` →
   deny exactly as `{:deny, e}` — payload, rows, and caller error byte-identical to
   the bare malfunction deny — and ADDITIONALLY hand the summons to `escalate/4`.
   The summons is SUBORDINATE to the deny: if the hand-off cannot complete (e.g. no
   accountable owner resolves for the caller's principal/origin), the deny still
   returns and the failed summons is recorded as observability — a summons failure
   never raises into the call path. The engine's one-open partial index IS the §A3
   dedup: a repeat malfunction re-finds the open request and opens no second; a
   malfunction arriving after a resolved-but-unhealed request opens a fresh one — a
   ruling on the work does not fix the sensor, and silent recurrence is what §A3
   forbids.

**Escalation is a STATUTE-LEVEL resolver, never a dispatch-level authority
(FRESH-1, CRITICAL).** An escalate statute is folded EXACTLY like any other
statute — no special-casing. When `decide` reaches an escalate statute it reads
the engine's **effect-free `resolve/3`** (escalation-substrate-v1 §9.1), whose
**unified public union is four shapes: `:allow | {:allow, ruling_id} | {:deny, e} |
{:needs_request, dr_id|nil}`** — a pure read, opening/consuming/firing nothing:
- `:allow` (**waiver-sourced** — an active waiver authorizes it) → **this statute
  passes; the fold CONTINUES over later statutes** exactly as any predicate/script
  `allow`. Nothing to consume (a waiver is not consumed).
- `{:allow, ruling_id}` (**ruling-sourced** — a prior `ruled`-allow authorizes it) →
  the statute passes and the fold continues, AND `decide` collects `ruling_id` into
  `to_consume`. The actor consumes it via `consume/2` (`ruled→consumed`, execute-once)
  only when the whole fold allows and the handler is about to run (item 3). `decide`
  consumes nothing.
- `{:deny, e}` (a prior `ruled`-deny) → a non-`allow` statute outcome; first
  non-`allow` wins and `decide` stops, returning `{:deny, e}`.
- `{:needs_request, dr_id}` → a non-`allow` outcome; `decide` stops, returning
  `{:escalate, statute, ctx, dr_id}`. The actor branches on `dr_id`:
  - `dr_id == nil` (no open request) → call `escalate/4` to OPEN a fresh
    decision-request and return `{:decision_pending, id}`.
  - `dr_id != nil` (**already-open** — the caller is already parked on this exact
    action) → the actor **re-returns `{:decision_pending, dr_id}` WITHOUT opening**
    a duplicate. `decide` itself opens NOTHING (effect-free on enforcement).
The handler runs **only when the whole fold yields `:allow`** — an escalate
statute's `:allow` never short-circuits past a later `deny`/`remedy`/escalate.

Per statute, `decide` computes the outcome:

1. **Predicate first (hot path).** If the statute carries `deny_when`, evaluate
   it exactly as r6 does (demand-driven facts, cached per call, nil-never-fires,
   total-catch → `rule_error` deny). If the predicate does NOT match, the statute
   yields `allow` and evaluation moves on — the script never runs (I1).
2. **Script second (only if reached).** If the statute carries `[rule.check]` and
   either has no predicate or its predicate matched, run the script (§A2–A3) and
   map its return to an effect via `[rule.check.effects]`; a fail-closed class
   denies (§A3).
3. **Effect → fold.** The statute's effect is `allow` (continue the fold),
   `deny`/`remedy` (non-`allow`, first wins, stop), or `escalate` (resolve
   statute-level per the principle above: `:allow` continues, `{:deny}`/`:needs_request`
   stop). The fold's result is the first non-`allow`, or `:allow` if all pass.

The smoke C6 runner drives effects through the **actors** (a real `Dispatch`
call, or the folded supervision step), never by expecting `evaluate/2` to perform
a remedy — `evaluate/2` is dry-and-collapsing by contract.

A predicate-only statute is exactly r6 with an optional non-default `effect`. A
script-only statute runs the script on every call to its verb. A statute with
both uses the predicate as a cheap guard on an expensive script. Concurrency,
snapshot-grade facts, and the deny-only monotonicity guarantee are r6's,
unchanged — a decision can only deny/remedy/escalate, never grant, so ordering
before the handler still cannot bypass a constitutional check.

---

## C. Remedies / active gates (P5)

### C1. The remedy schema

A statute whose deny path (predicate match, or a `[rule.check.effects]` value of
`remedy`) should originate a producer carries a `[rule.remedy]` table:

```toml
[[rule]]
name  = "completion-needs-independent-review"
verb  = "attest"
text  = "completion requires a reviewed-clean verdict from an independent, cross-harness reviewer"
edges = ["verb", "turn-end"]
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  # CROSS-HARNESS independence, keyed on p3-observables-producers-v1.md's
  # registered fact (p3 invariant 6, LINK-ONLY): reads verdicts filed on a
  # review assignment R with R.reviewsAssignmentId = A — a commissioned reviewer,
  # never a verdict filed directly on A — whose author session ≠ holder AND
  # author harness ≠ holder harness. Harness is substrate-known: no model-id
  # parsing, catalog opacity preserved (§X1).
  { fact = "assignment.cross_harness_verdict_kinds", op = "not_in", value = ["reviewed-clean"] },
]
effect = "remedy"

[rule.remedy]
action   = "assign"                 # spawn | wake | assign (existing verbs)
produces = "reviewed-clean"         # the verdict kind the producer files (§F)
target_role = "reviewer"            # top-level TARGET (per-action required, below)
[rule.remedy.params]                # the assign verb's non-target params
subject = "review of assignment {assignment_id}"   # string param: embedded {token} ok
reviews = "{assignment_id}"         # p3's typed review-of link — WHOLE-TOKEN
work_item = "{work_item_id}"        # WHOLE-TOKEN
```

`reviews = "{assignment_id}"` is load-bearing (finding 3): it sets p3's
`reviewsAssignmentId` on the review assignment, so the spawned reviewer's verdict
is **reachable** from the producer assignment and enters
`cross_harness_verdict_kinds`. Without it the reviewer's `reviewed-clean` would
never release the gate — and per p3's round-2 **anti-laundering invariant** (p3
invariant 6) the independence facts (`independent_`/`cross_harness_`/
`cross_provider_verdict_kinds`) read ONLY verdicts on review assignments `R` with
`R.reviewsAssignmentId = A`; a verdict filed **directly** on `A`, by anyone,
NEVER lights an independence fact. So the review-link is the sole path for these
gates: there is no direct-verdict bypass, and a review remedy MUST carry
`reviews`. A user override of such a gate is the escalation/ruling path
(`escalation-substrate-v1`), not a verdict lighting the fact.

**The review remedy's only composable action is `assign` to a BOUND reviewer role
(lattice H3/H2).** A `spawn` remedy **cannot carry the `reviews` link** (spawn
creates a session, it does not create the review assignment that carries
`reviewsAssignmentId`), so the flagship review remedy is necessarily `action =
"assign"` targeting an **existing, bound** reviewer role — resolved bound-or-fail
(§C2, no owner-Main fallback). Standing up that bound reviewer role (spawning the
reviewer session and binding the role) is **org/orchestrator setup**, not something
this remedy does; the remedy only assigns the review to a reviewer that already
exists.

The independence property is **cross-harness**; the same-harness fallback (a
fresh session at a higher thinking level) is **guidance-level, not rail-enforced**
(§X1).

**`external_producer` (statute field, finding 4).** A verdict-fact gate whose
required kind arrives from an agent/user workflow the substrate does not itself
originate — e.g. a plain `assignment.verdicts` gate an org fills by a human
reviewer, or a review gate whose reviewer is created outside this statute's
remedy — declares `external_producer = true` (bool, default `false`). This is the
**documented intent** that the fact has a producer F1 cannot see in the loadset;
it makes the gate satisfiable at load without an in-statute remedy or a
`producers.toml` entry (§F1). It is the ONLY way a non-substrate-originated
producer counts — there is no blanket "any agent-created review assignment
counts." `external_producer` is meaningful only on a verdict-fact gate; on any
other statute it is a load error.

- `action` ∈ `{spawn, wake, assign}` — the existing dispatch verbs. No new verb.
  **`run-tests`/`run-smoke` are NOT legal remedy actions (lattice H9/H3
  narrowing).** So a **mechanical-producer gate** (over `assignment.produced_verdict_kinds`,
  whose only producer is a `producers.toml` verb, §F1) **cannot originate its
  producer**: it has no remedy, so it **denies at the verb edge and, at the sweep,
  re-obligates the holder** (§D2), who runs `run-tests`/`run-smoke` **deliberately**
  (a mechanical producer must run against real code the holder controls, not be
  spawned by the substrate). An `action = "produce"` that would let a remedy invoke a
  producer verb is **named future work, NOT built in v1**.
- **Per-action target schema (top-level, required).** The verb's target is a
  top-level `[rule.remedy]` field, validated at load per action; the rest go in
  `[rule.remedy.params]`:
  - `assign` → `target_role` (required). Optional params: `subject` (required),
    `reviews`, `files`, `work_item`.
  - `wake` → exactly one of `target_role` / `target_session` (required). Params:
    `prompt` (required), `after`/`at`.
  - `spawn` → `name`, `harness`, `model` (required top-level), `archetype`/`host`
    optional. Params: `display`.
  A missing required target/param, or a param not in the action's allowed set, is
  a load error.
- `produces` is a `verdictKind` (check-tier lexicon) — the fact the producer
  files that satisfies THIS gate, and the load-time producer-graph edge (§F1). It
  is validated to be a member of the gate's `not_in [..K..]` list (any of the
  `assignment.*verdict_kinds` independence facts); a `produces` the gate does not
  require is a load error (dead remedy). **Omitted for a script-effect remedy**
  (the script-K rule, §A1) — a script gate has no verdict fact.
- **Interpolation (pinned):** the string-typed `subject`/`prompt`/`display`
  params allow **embedded** `{token}` substitution (each token replaced by its
  resolved string value). Every other field (`target_role`, `target_session`,
  `reviews`, `work_item`, `name`, `harness`, `model`, `archetype`, `host`,
  `after`, `at`) is **whole-token-or-literal**: its value is exactly one `{token}`
  or a literal, replaced by the resolved value. A partially-interpolated
  non-string field is a load error.
- An unresolvable token at fire time (the datum is absent for this call) fails
  the remedy closed: the gate still denies (`reason="remedy_fired"`, outcome
  `unbound`), a `rail_remedy` row records the unbound token, nothing is
  dispatched.

**Binding-token vocabulary (closed):** `{assignment_id}`, `{work_item_id}`,
`{holder_key}`, `{holder_role}`, `{holder_archetype}` — resolved from the call's
`$assignment` (check-tier's cached pseudo-fact) and its params. `{caller_origin}`
— the raw origin. Any other token is a load error.

### C2. Remedy authority — the reserved remedy principal (F5)

Remedies do **NOT** dispatch as `process:tightbeam`: `assign` and `spawn`
constitutionally reject process principals (assignments.ex `principal_allowed`;
gateway.ex spawn `owner_user_id: nil → forbidden`), so a process-origin remedy
could dispatch only `wake` — the flagship review remedy would be inert. Instead:

- **A substrate-reserved remedy principal** `{:remedy, %{statute: name,
  action: verb, owner: owner_user_id}}` and origin class `remedy:<statute>`. The
  `owner` is resolved from the gated assignment's holder → `owner_user_id`, so the
  producer belongs to the correct org. **Transports never construct it** — the
  WS/HTTP/CLI seams only ever set `user`/`agent`/`process`; the `RailRemedy`
  executor inside the dispatch tier is the sole constructor, so the principal
  cannot be forged by a caller.
- **Constitutional acceptance seam — the exact ground-truth deltas (finding 2).**
  The remedy principal is admitted per-action, never generally:
  - `assignments.ex`: `principal_allowed({:remedy, %{action: "assign"}}) → :ok`;
    `principal_id({:remedy, %{owner: o}}) → "user:" <> o`; **and `opener/1` gains
    `opener({:remedy, %{owner: o}}) → {o, nil}`** (the review assignment's opener
    columns attribute to the owner user, `{byUser, bySession}` — the review found
    `opener/1` had no remedy clause; assign creation calls it).
  - `gateway.ex` spawn: admits `{:remedy, %{action: "spawn", owner: o}}`, using
    `o` as the `owner_user_id` the handler reads (bypassing `resolve_caller`'s
    `owner_user_id: nil → forbidden`).
  - `wake`: admits `{:remedy, %{action: "wake"}}`.
  A remedy principal whose `action` ≠ the verb it reaches is rejected exactly as a
  process principal is.
- **Serialization (finding 2).** `EventLog.serialize_principal/1`
  string-interpolates a `{kind, value}` tuple and cannot render a map. Add
  `serialize_principal({:remedy, %{statute: s, action: a}}) → "remedy:" <> a <>
  ":" <> s` — the stable audit string form (e.g. `"remedy:assign:completion-needs-
  independent-review"`). Every `remedy:` dispatch's events row carries it.
- **Role→session resolution — REQUIRE A BOUND REVIEWER, fail loud on unbound
  (lattice H3/H2).** `RailRemedy` resolves `target_role` via
  `Roles.resolve(db, target_role)` (roles.ex:166-179) but **rejects the owner-Main
  fallback**: `resolve/3` returns `{:ok, key, fell_back?}`, and the remedy proceeds
  **only** on `{:ok, key, false}` (a real, active BOUND session). `{:ok, _, true}`
  (the silent owner-Main fallback — an unbound role resolving to the owner's Main) OR
  `{:error, unknown_role}` **fails the remedy LOUD** (`unbound`, no dispatch, a
  `rail_remedy` `unbound` row). A review must go to a real reviewer, never silently to
  the owner's Main. **Provisioning the bound reviewer role is org/orchestrator setup**,
  stated honestly — the mechanism does not create it. On success the remedy populates
  the resolved `session_key`/`target_role` exactly as the agent-dispatch path does.
- The producer verb still runs through the **full statute tier** (auditability):
  a `remedy:` dispatch appends its own `verb`/`denied` events and is itself
  gate-able. Its `caller.origin_class` is the new class `remedy` — existing quota
  rails keyed on `origin_class = "agent"` do **not** match it (a property F2
  relies on).

### C3. Idempotency — remedy episodes with explicit CAS states

> ERRATA (Fable review, 2026-07-23): the TTL-reclaim CAS below must pin `occurrence`
> in its WHERE clause (`AND occurrence = <observed>`), not only status+openedAt. Without
> it, if an episode cycles close→reopen (occurrence bumped) between the reclaimer's read
> and its UPDATE, the reclaimer wins the row at the new occurrence but dispatches under
> the spent occurrence key → the spent key replays the OLD producer → the episode is live
> at N+1 with a producer whose ledger entry lives under N → dead-live reclaim can never
> confirm → permanent silent block. Pinning occurrence still PRESERVES the value (TTL
> reclaim does not bump); it only makes the reclaimer lose the race when the row moved.
 (F3, F6)

The `wire_idempotency` ledger has no episode/status/close and races on
get→act→put, so it cannot own the episode lifecycle. A new episodes table owns it,
as an explicit CAS state machine (finding 3: the old `open`+NULL-producer window
let a concurrent loser see an open row with no producer and dispatch again):

```sql
CREATE TABLE IF NOT EXISTS rail_remedy_episodes (
  statute     TEXT    NOT NULL,
  subject     TEXT    NOT NULL,   -- the gated ref (assignment_id | work_item_id)
  status      TEXT    NOT NULL CHECK (status IN ('claimed','dispatched','live','closed')),
  producerKey TEXT,               -- the producer session/assignment id (set entering 'live')
  occurrence  INTEGER NOT NULL,   -- the OCCURRENCE#; derives the dispatch wire key;
                                  -- bumps on ANY terminal-state exit (closed/dead-live); TTL preserves
  rewakeCount INTEGER NOT NULL,   -- re-wake counter within an occurrence (each wake lands)
  claimToken  TEXT    NOT NULL,   -- ROW-fencing nonce ONLY, fresh at every claim/reclaim
  openedAt    INTEGER NOT NULL,   -- claim time; the TTL clock for a wedged claimant
  closedAt    INTEGER,
  PRIMARY KEY (statute, subject)
);
```

**Two key families close the two-external-effects hole (r6 LEASE/TTL ruling).**
`claimToken` fenced the row transitions but NOT the external dispatch: a TTL reclaim
mints a new `claimToken` while the ORIGINAL claimant's `spawn`/`assign` may still be
running, so two producers could be created. The fix splits the keys:

- **`claimToken` = row-fencing nonce ONLY.** Fresh at every claim/reclaim; the CAS
  transitions carry `AND claimToken=<mine>` so a superseded claimant cannot advance
  the ROW. It never touches `wire_idempotency`.
- **Dispatch wire key = the EPISODE OCCURRENCE**, `"rail-dispatch:" <> statute <>
  ":" <> subject <> ":" <> occurrence`. **THE OCCURRENCE RULE:** `occurrence`
  increments on **any transition OUT OF A TERMINAL episode state** — a `closed`
  reopen (fact landed) or a dead-`live` replacement (producer confirmed dead, its
  current-occurrence `wire_idempotency` entry inspected) — and the **TTL-stale-claim
  reclaim PRESERVES it** (the original action may still be running under it). THE
  INVARIANT this buys: **at most one external dispatch effect per occurrence.** A
  TTL reclaim while the original still runs re-dispatches under the SAME occurrence
  key, and the forever-scoped `wire_idempotency` ledger makes the second dispatch a
  no-op (returns the first producer); a terminal-exit reclaim bumps `occurrence` → a
  new key → a legitimately new producer (neither the dead one nor the spent
  `closed` key's old one). The lease CAS (`claimed→dispatched WHERE claimToken=<mine>`)
  still fences the row and gates who calls dispatch; the occurrence key guarantees
  that even a racing re-dispatch under the same occurrence collapses to one effect.
- **Re-wake wire key = occurrence + rewake counter**, `"rail-rewake:" <> statute <>
  ":" <> subject <> ":" <> occurrence <> ":" <> rewakeCount`. Each re-wake
  increments `rewakeCount` so every re-wake LANDS (a fresh key), unlike the dispatch
  which must dedupe.

**States and transitions** — each transition is a single
`UPDATE … WHERE … AND status=<prior> AND claimToken=<mine>` whose rows-affected = 1
means this actor won the CAS; a 0 means it was superseded and it backs off,
performing no side effect:

- `claimed` — slot won, no lease yet, no producer. **Transient; a reader treats it
  as in-flight and does nothing.**
- `dispatched` — the **lease** is won and the external dispatch is in progress
  (`producerKey` NULL until it returns). **Transient; a reader treats it as
  in-flight.**
- `live` — steady state, `producerKey` set, awaiting the satisfying verdict. A
  reader may re-wake here.
- `closed` — the satisfying fact landed.

Firing a `{:remedy, statute, ref}` decision:

First read the current row (if any) to route; then act by CAS.

1. **Claim (atomic, before any side effect).** Mint a fresh `token`. Try, in order,
   the first that affects a row; a win makes THIS actor the claimant. **THE
   OCCURRENCE RULE (r9): any transition OUT OF A TERMINAL episode state bumps
   `occurrence`; only the TTL-stale pre-`live` reclaim preserves it.** Terminal
   states are `closed` (fact landed) and dead-`live` (producer confirmed dead) —
   the spent occurrence's dispatch wire key is done, so a NEW occurrence is required
   or the re-dispatch would return the OLD (dead/stale) producer through the forever
   ledger. A stale `claimed`/`dispatched` is NOT terminal (the original action may
   still be running), so its reclaim preserves the occurrence to dedupe with it.
   - fresh: `INSERT … (statute, subject, status, occurrence, rewakeCount, claimToken,
     openedAt) VALUES (?, ?, 'claimed', 1, 0, <token>, now) ON CONFLICT DO NOTHING`.
   - reclaim-closed (terminal exit → **BUMP occurrence**, r9 fix): `UPDATE … SET
     status='claimed', producerKey=NULL, occurrence=occurrence+1, rewakeCount=0,
     claimToken=<token>, openedAt=now WHERE (statute,subject)=(?,?) AND status='closed'
     AND occurrence=<observed>` — the bumped occurrence gives a fresh dispatch wire
     key so the reopen produces a genuinely NEW producer (`reopened-dispatched`), not
     the spent key's old one.
   - reclaim-stale-claim (NON-terminal, TTL → **PRESERVE occurrence** — the original
     action may still run): `UPDATE … SET status='claimed', producerKey=NULL,
     claimToken=<token>, openedAt=now WHERE (statute,subject)=(?,?) AND status IN
     ('claimed','dispatched') AND openedAt < now − TTL` (**TTL = 60_000 ms**).
     Occurrence unchanged, so a re-dispatch reuses the same wire key and collapses
     with a still-running original to one producer.
   - reclaim-dead-`live` (terminal → **BUMP occurrence**, finding 3a): when the read
     showed `status='live'`, `producerKey` resolves **dead** (session retired /
     review assignment closed/revoked without the satisfying verdict), **AND** the
     current occurrence's dispatch `wire_idempotency` entry has been inspected to
     confirm it points at that dead producer, `UPDATE … SET status='claimed',
     producerKey=NULL, occurrence=occurrence+1, rewakeCount=0, claimToken=<token>,
     openedAt=now WHERE (statute,subject)=(?,?) AND status='live' AND
     occurrence=<observed>` — one reclaimer wins, the bumped occurrence yields a NEW
     dispatch key (`reopened-dispatched`).
   - If none affects a row, the slot is held by another actor: go to step 3.
2. **Lease-then-dispatch (claimant only — fences the external side effect).** FIRST
   win the pre-dispatch lease: `UPDATE … SET status='dispatched' WHERE
   (statute,subject)=(?,?) AND status='claimed' AND claimToken=<mine>`. Rows-affected
   0 → superseded → do NOT dispatch (provable no-op, DB-layer fence). Rows-affected 1
   → dispatch the producer verb under the remedy principal (§C2) with **`--key =
   "rail-dispatch:"<>statute<>":"<>subject<>":"<>occurrence`** — the occurrence key,
   so a same-occurrence racing re-dispatch (e.g. a TTL reclaim that stole the row
   while THIS dispatch still ran) collapses to one producer through the forever
   ledger (the r6 invariant: ≤1 external effect per occurrence). On the return:
   - **success:** `UPDATE … SET status='live', producerKey=? WHERE
     (statute,subject)=(?,?) AND status='dispatched' AND claimToken=<mine>`.
   - **denied dispatch (finding 3b):** the producer verb returned `{:error, …}` (the
     runtime blocker, §F). Release the lease so a later edge retries — `DELETE …
     WHERE (statute,subject)=(?,?) AND status='dispatched' AND claimToken=<mine>` —
     and record `rail_remedy` outcome `blocked`. **Retry timing (precise):** the row
     is now absent; the gate stays denied so the obligation persists, and the NEXT
     firing edge for this (statute, subject) — the holder's next dispatch of the
     gated verb, OR the next turn-end sweep of the holder — decides `{:remedy,…}`
     again, finds no row, INSERTs a fresh claim (occurrence resets to 1) → fresh
     lease → fresh dispatch. No timer: re-fire is edge-driven.
3. **In-flight (slot occupied in step 1, not reclaimable).**
   - `live` + live producer → **re-wake**, no new producer (`rewake`): `UPDATE … SET
     rewakeCount=rewakeCount+1 WHERE … AND status='live' AND claimToken=<observed>`,
     then `wake` under the remedy principal with `--key =
     "rail-rewake:"<>…<>occurrence<>":"<>rewakeCount` (each re-wake lands, no dedupe).
     **Target choice (lattice H2/H4) — wake the party that must ACT:**
     - **latest linked verdict is NON-satisfying** (a `changes-requested` verdict is
       the newest verdict reachable via `reviewsAssignmentId = A`) → wake **`A`'s
       HOLDER** (the producer/coder — it must iterate on the findings), NOT the
       reviewer.
     - **no verdict yet** (the reviewer has not ruled) → wake the **reviewer** (the
       review-assignment holder — it must review).
     One branch, keyed on the latest reachable verdict for `A`.
   - `claimed`/`dispatched` (another actor mid-lease/dispatch) → do nothing; the
     gate still denies. That claimant will reach `live`.
4. **Deny the gated verb now** (I4/I5): `{:deny, %{code: "rule_denied", rule: name,
   reason: "remedy_fired", ref: ref, producer: producerKey, message: text}}`. No wait.
5. **Close — per-statute-pass, actor-owned (finding 3d).** Closure is NOT
   conditioned on the overall bare `:allow` (the review's defect: an earlier passed
   statute could not close when a later statute denied). Instead, as `decide` folds,
   it collects a **`to_close`** list — every statute that INDIVIDUALLY passed
   (`allow`) AND has a `live` episode for this `subject` — and returns it alongside
   the decision (a pure read; `decide` writes nothing). The **actor** closes each,
   regardless of the final decision: at the verb edge **`Dispatch`** closes; at the
   sweep **`Supervision`** closes; each is `UPDATE … SET status='closed',
   closedAt=now WHERE (statute,subject)=(?,?) AND status='live'`, scoped to that ONE
   statute. Proof two statutes over one subject never close each other: each close
   names its own `statute` in the WHERE, and a statute enters `to_close` only when
   IT individually passed — so when S1 passes and S2 denies (overall `{:deny}`), S1
   closes E1 and S2's E2 stays `live`; when both pass (overall `:allow`), each
   closes its own. `changes-requested` does not satisfy a gate, so that statute
   never enters `to_close`; its `live` episode re-wakes (step 3), never re-dispatches.

**Release** remains the ordinary re-evaluation of a now-satisfied fact (I1/I7):
the producer files `reviewed-clean` on its `reviews`-linked assignment, the fact
becomes reachable, the holder's next `attest completion` decides `:allow`, passes
silently, and closes the episode. Reviewer teardown is a separate org rail, not
this mechanism's concern (roadmap P7 records this; §X-note F12).

---

## D. Turn-end sweep (P6) — one adjudicator, folded into supervision

### D1. Single terminal-edge adjudicator (F8)

The sweep is **not** a second GenServer racing supervision (finding 8: two
independent casts to two servers let scheduler order change enforcement, and let
supervision prod while the sweep spawns a remedy for the same holder). Instead the
sweep is a **step inside `Supervision.evaluate/5`** — supervision already owns the
turn-terminal edge (its `:on_terminal` cast), so there is one adjudicator, one
reaction per terminal, no race by construction. Supervision.ex IS modified in P6
(the earlier "not modified" claim is retired by this ruling); `Rules` exposes the
dry decision API (§B) that supervision's new step calls. No `RailSweep` GenServer,
no second `:on_terminal` cast.

Supervision's existing predicate primitives are reused as-is: `turn just terminal`
(the cast), `Ledger.pending_count == 0` (`:busy`), `Assignments.oldest_open`
(open obligation), its `lastEvaluatedTerminal` **watermark/dedupe** (a re-delivered
terminal is `:duplicate`, an older one `:coalesced` — the rail step inherits this,
so no separate rail watermark is needed, closing finding 10's dedupe gap), and its
outbox-drain recovery contract.

### D2. The ONE total supervision order (F8, F9, F10, lattice H1/H8)

**§D2 owns the single total order that integrates EVERY branch** — supervision's own
(`supervision-v1`/`supervision-impl-v1`), the escalation park
(`escalation-substrate-v1`), and model ringdown (`model-ringdown-pattern`, a sibling
authority whose re-dispatch appears here as a queued Ledger turn or a self-scheduled
continuation, not a new branch). The ruled order, top to bottom (each branch that
acts writes `lastEvaluatedTerminal` — no branch may skip the watermark):

```
with :new <- dedupe(…) do                                    # (1) dedupe / :duplicate / :coalesced
  cond
    Ledger.pending_count(db, session_key) > 0 -> :busy       # (2) queued-Ledger continuation
    holder_state(db, session_key) == :retired ->             # (3) liveness — retired first
      doorbells_for_holder(db, session_key); :stranded       #     existing doorbells path
    true ->                                                  #     LIVE holder:
      case adjudication_hold(db, session_key, terminal_seq) do  # (4) ADJUDICATION-HOLD
        {:held, tag}  -> {:held, tag}                        #     open model-adjudication episode → suppress rail+prod
        :fallthrough  ->
          case rail_step(db, session_key, assignment, terminal_seq) do  # (5) rail step
            {:acted, tag} -> {:acted, tag}                   #     remedy/escalate (FRESH-5, unmodified)
            :fallthrough  ->
              if Wakes.pending_count(db, session_key) == 0,   # (6) generic pending-wake
                do:  <is_nil(terminal_seq) ? :idle : claim_and_act (prod)>,  # (7) prod ladder
                else: :continuation
          end
      end
  end
```

> **AMENDED 2026-08-12:** position (4) below — and its branch in the code
> sketch above — died with adjudication. Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`).
> The live turn-end order runs (1)(2)(3) then (5)(6)(7) with no hold branch.
> Retained as history. See `adjudication-deletion-amendment.md`.

**(4) ADJUDICATION-HOLD (lattice H1/H8).** When the LIVE holder has an **open
model-adjudication episode** — an `adjudication_episodes` row for this session with
`status IN ('claimed','notified')` (`model-ringdown-pattern`, the durable session
hold while the owner adjudicates a model exhaustion/unavailability) — the session is
HELD, so the sweep suppresses BOTH the rail step and the prod: the holder is not
idling, it is parked awaiting a model decision, and that episode's **own `deadlineAt`
drives escalation** (model-ringdown's supervision-sweep-past-deadline ladder, which
this branch defers to — it does not re-prod or re-escalate that episode here). The
branch **writes the watermark** and returns `{:held, :adjudication_hold}` (tag added
to the `Supervision.evaluate/5` return union) — the ruled "every acting branch
watermarks" rule. On `terminal_seq == nil` (recovery) it does not act, `:fallthrough`.
(The ESCALATION decision-request park is a distinct concern, handled inside the rail
step's escalate branch by `parkWakeId` idempotency — §D2.4.)

**Named supervision change:** liveness is checked before `Wakes.pending_count`
(finding 7 — the rail step must run before the generic pending-wake so a non-self
wake cannot suppress the remedy; FRESH-1 r6 — only a LIVE holder acts). A **retired**
holder now yields `:stranded` even when a wake is pending (the deliberate consequence,
a retired holder cannot act on a wake). The `:live` prod path is otherwise
byte-unchanged.

`rail_step/4` takes `terminal_seq` (FRESH-3): **on `terminal_seq == nil` (a recovery
path) it does NOT act and returns `:fallthrough`**, mirroring supervision's existing
`is_nil(terminal_seq)` guard, so no acted branch attempts a NULL watermark write
(the column is NOT NULL, supervision.ex ~20). `rail_step` returns `{:acted, tag}`
(`:rail_remedy`, or `:rail_escalate` once an `escalate`-bearing turn-end statute
loads — §D2.4) only when it acts, writing `lastEvaluatedTerminal = terminal_seq`
itself; `evaluate_terminal` returns that `{:acted, tag}` **unmodified** so
`Supervision.evaluate/5`'s result is `{:acted, :rail_remedy | :rail_escalate}` (the
shape escalation-substrate-v1's acceptance expects — FRESH-5). Otherwise
`:fallthrough`, leaving the pending-wake suppression and prod ladder unchanged. A
non-self wake cannot suppress the remedy (the rail step runs first, uses
`self_pending_count`); it still suppresses the *prod* on the fallthrough.

The rail step, for the oldest open assignment `a`, with strict precedence —
remedy XOR prod, never both:

1. **Self-scheduled continuation suppresses everything (I6, F10).** If a pending
   wake targeting the holder was **scheduled by the holder itself** —
   `Wakes.self_pending_count(db, session_key) > 0`, counting pending wakes where
   **`sessionKey = creatorSessionKey = holder`**, keyed on wake-on-fact-v1's
   **durable `creatorSessionKey`** column (§4.2, its owner), NOT the mutable
   `origin` string (an owner-created or supervision-created park has
   `creatorSessionKey ≠ holder` and does NOT count) — the agent is coming back on
   its own clock: the rail step does nothing and supervision's own path is
   unchanged. This is the **no-false-positive guarantee**, keyed on the durable
   creator identity (finding 10: `Wakes.pending_count` of *any* wake proved the
   wrong statement; the mutable `origin` is not a sound self-scheduling proof).
2. **Compute the dry decision** for the obligation (§D3). It is one of `:allow`,
   `{:deny,…}`, `{:remedy, statute, ref, …}`, `{:escalate,…}`.
3. **`{:remedy,…}` → run the remedy, XOR the prod.** Gate-unsatisfied with a
   runnable remedy = reviewable work by definition (finding 10 ruling:
   reviewable-work is the **gate-unsatisfied state itself**, not a self-attested
   `progress` row). Fire the remedy once via §C3's episode claim (idempotent —
   if the verb edge already claimed this episode, this is a re-wake, not a second
   producer), record `rail_sweep` decision `run-remedy`, **write supervision's
   `lastEvaluatedTerminal` watermark for this terminal_seq** (finding 7 — the
   remedy branch advances the watermark exactly like every other supervision
   branch, so a re-delivered terminal is `:duplicate` and never double-fires), and
   **return `{:acted, :rail_remedy}` without prodding**.
4. **`{:escalate, statute, ctx, dr_id}` → the sweep opens the request AND parks the
   holder, watermark, XOR the prod.** By the FRESH-1 principle (§B), `decide` has
   ALREADY resolved any active waiver or prior ruling in-fold — a `:allow`
   resolution continued the fold (so a waived/ruled-allow escalate statute never
   reaches here as `{:escalate}`), and a `{:deny}` resolution is handled by §D2.5.
   The only `{:escalate}` `decide` returns is `resolve/3`'s `{:needs_request,
   dr_id|nil}` (no waiver, no ruling). On `dr_id != nil` (already-open) the sweep
   re-returns the parked DR idempotently, opening nothing (below). Per
   `escalation-substrate-v1` (its §4 + case 17, which OWNS this text): E7 splits into
   two edges, and the **raiser-self-park rule is scoped to the VERB edge only**. At
   the **turn-end edge the SWEEP**, on `dr_id == nil`, does both: it calls
   `escalate/4` to open the decision-request with **raiser = the holder principal**,
   then **parks
   the holder itself** with a substrate-created, holder-targeted `{escalation-ruled,
   id}` condition wake (creatorSessionKey = nil, target-keyed so the holder reads
   `:continuation` without self-scheduling), whose fallback **`dueAt = deadlineAt`**
   — the decision-request's org-configurable owner-decision deadline, **NOT** a
   supervision prod cadence (supervision prods fire at `after_ms: 0`,
   supervision.ex:370; there is no resident deadline clock). The park is
   **idempotent** via the DR's stored `parkWakeId` (a sweep over an already-parked
   open DR re-returns it, never double-parks). The sweep records `rail_sweep`
   decision **`escalate-park`** (FRESH-2 r6), writes `lastEvaluatedTerminal`, and
   returns `{:acted, :rail_escalate}` without prodding. Moot in v1 regardless: no
   `escalate`-bearing turn-end statute loads until escalation's review lands clean
   (§A1).
5. **`{:deny,…}` with no runnable remedy → re-obligate.** A turn-end statute that
   denies but declares no remedy (or a fail-closed script) leaves the obligation
   unsatisfied but unremediable: `:fallthrough` to supervision's existing prod →
   ladder → Main terminus, unchanged (that path writes the watermark as today).
   Record `rail_sweep` `re-obligate`. (Finding 9's fix: the sweep never "runs the
   offending statute's remedy" when none exists.)
6. **`:allow` (no gate-unsatisfied obligation) → supervision's normal path.** If
   `a` is merely abandoned with nothing owed to a gate, `:fallthrough`; supervision
   prods as today (writing the watermark on its branch). Record `rail_sweep` `none`.

Because the decision and the action are separated (§B dry API) and the rail step
fires at most once under the episode claim, there is no double-effect (finding 9):
`Rules.evaluate` never fires a remedy; only this step (or the verb edge) does.

### D3. Evaluation mechanics (synthesizing the obligation)

For the oldest open assignment `a`, the step synthesizes a completion pseudo-call
and asks the **dry** decision API (§B) for the `turn-end`-edged statutes:

```elixir
Rules.decide(db, %{verb: "attest", origin: "remedy:sweep",
  principal: {:session, a.holder_key}, session_key: nil, edge: :turn_end,
  params: %{assignment_id: a.id, kind: "completion"}})
```

`Rules.decide` (arity 2) reads `call[:edge] == :turn_end`, runs the same
predicate/script machinery as the verb edge (§B) filtered to `turn-end`-edged
statutes, and **returns `{decision, to_close, to_consume}` without firing**.
Supervision, the sweep actor, closes each `to_close` episode but **IGNORES
`to_consume` — the sweep NEVER consumes** (lattice H9: no handler runs at the
turn-end edge, so consuming would spend a ruling with nothing behind it; §B item 3).
It then acts on `decision` per §D2. Scripts fire here identically to the verb edge (time-boxed, contained,
fail-closed via `rail-exec`). The synthesized call NEVER mutates: the step
evaluates statutes and, at most, the leased remedy dispatches; it never dispatches
the synthesized `attest completion`.

Finding 10's dropped branches: the old "≥1 `progress`/`completion` attest = work
landed" predicate is **removed** — a self-attested `progress` does not prove a
commit, and a `completion` attest cannot coexist with an open assignment (the real
handler closes it), so that half was unreachable. Reviewable-work is now exactly
"the gate decided `{:remedy,…}`" (§D2.3). Only `attest` is a synthesizable outcome
verb in v1; `edges=["turn-end"]` is restricted to it at load (§A1).

---

## E. Legibility (P8 hooks — the event/fact schema)

Two audiences, two records (I7). The **agent** sees only the refusal reason at
the moment a gate fires (never on pass). The **substrate** records every
invocation for the derived-not-stored tuning corpus (observability-v1).

**The one legibility contract (finding 17).** Guidance/smoke call these
"self-naming facts"; this mechanism realizes each self-naming fact as a **row** —
there is no separate fact object. The mapping is explicit: a non-pass's
self-naming fact IS its `events(denied)` row (agent-facing, §E1); a script/remedy/
sweep's self-naming fact IS its `lifecycle_events` row (observability, §E3). "Emit
a fact that names the rail, the dispatch, and why" (guidance §6) is satisfied by
these rows and the query path in §E2.

### E1. Agent-facing: the `denied` event (extends today's convention, additively)

Every non-pass appends one `events` `kind="denied"` row (dispatch.ex's existing
best-effort append; the schema CHECK `verb|denied` is unchanged — no new kind, no
migration). The **payload** is extended from r6's `%{code, rule, message}` — the
extension is **additive** (new keys only; `code`/`rule`/`message` unchanged in
name and meaning):

```elixir
%{code: "rule_denied",             # or rule_error (r6, fact compute failure)
  rule: statute_name,
  edge: "verb" | "turn-end",
  reason: "rule_denied" | "script_error" | "script_timeout"
          | "script_out_of_set" | "script_contained_refused"
          | "remedy_fired" | "escalated",
  script_exit_class: "returned" | "out-of-set" | "error:<N>"
                     | "timeout" | "contained"          # observed (§A3)
                     | "unreported"                     # no verdict observed (I3, §A3)
                     | nil,                             # nil for predicate gates
  ref: assignment_id | work_item_id | nil,              # the gated ref
  producer: producer_id | nil,                          # set on remedy_fired
  identity_manifest_sha: "<sha>",                       # the identity-manifest commit the
                                                        # evaluation ran under (guidance §6;
                                                        # unbackfillable — recorded at denial)
  message: "<statute text>"}
```

**I1 vs E1 reconciled (finding 17).** I1's "predicate-only behavior observably
unchanged" scopes to the denial **outcome** (still one `denied` row, same
`code`/`rule`/`message`, no mutation, same hot path) and the pre-existing payload
keys — NOT to the absence of additive keys. The new keys are additive-compatible:
a pre-r6 consumer reading `code`/`rule`/`message` sees exactly what it saw before;
the hot path still writes one row. Additive payload extension does not violate
observable-equivalence of behavior. Stated so no reviewer reads a conflict.

### E2. The legibility query path (finding 17: the public feed omits payload)

`EventLog.events_after/3` projects only `id, ts, kind, verb, origin, principal,
sessionKey` — **not `payload`** — so the promised rail/reason are not retrievable
through today's feed. P8's «point at the failure without forensics» query
therefore uses a **new** read that projects the payload:
`EventLog.rail_denials(db, since_id, limit) :: [%{id, ts, rule, edge, reason,
script_exit_class, ref, identity_manifest_sha, origin, principal}]` — SELECTs `payload` for
`kind='denied'` rows and decodes the §E1 keys. This is the single query behind the
two P8 questions («which rail, which dispatch, why» and «is a bad rail one revert
away»); the `lifecycle_events` reads (§E3) back the tuning-corpus queries. The row
`events.id` remains the dispatch-legibility cursor.

### E3. Substrate-facing: `lifecycle_events` rows (open CHECK, no migration)

`lifecycle_events` has no CHECK (event_log.ex — «new observations never need a
migration»). Three open kinds carry the tuning corpus; each is a
`EventLog.lifecycle(db, kind, subject, detail)` call, `detail` a JSON string:

- `rail_script` — subject = statute name; detail
  `{edge, ref, verb, return|reason, exit_class, duration_ms, origin}`. Written on
  **every** script invocation, pass or fail — so firing rate per rail is a query,
  never a stored counter. `exit_class` carries the §E1 vocabulary, `unreported`
  included: this row is where "the wrapper rendered no verdict" is recorded, and
  the only place a reader can tell an enforced time-box from an unanswered one
  (`duration_ms` cannot — it is BEAM-side, so a starved caller inflates it).
- `rail_remedy` — subject = statute name; detail
  `{edge, ref, action, producer_id|null,
  outcome: "claimed-dispatched"|"rewake"|"reopened-dispatched"|"unbound"|"blocked",
  origin}` — the episode-claim outcomes of §C3 (`rewake` = existing live producer
  re-woken, no new; `reopened-dispatched` = dead producer replaced; `blocked` =
  the producer dispatch was itself denied, the runtime-deadlock signal of §F).
  Written on every remedy fire. `remedy rate` (guidance-spec §6g) = `rail_remedy`
  rows per gated outcome, sliced by statute/archetype/model/guidance-SHA.
- `rail_sweep` — subject = session_key; detail
  `{ref, statute, decision: "run-remedy"|"re-obligate"|"escalate-park"|"none"}`. Written on every
  sweep trigger evaluation.

Predicate-only gates do NOT write a per-invocation lifecycle row (recording every
cheap predicate eval would defeat the hot path, I1); their firing is already
legible via the `denied` event row (E1). Lifecycle rows are observability only —
no code path reads them to make a decision (event_log.ex, inherited; the
derived-not-stored invariant).

All lifecycle writes are best-effort and total-caught (observability-v1 emission
discipline): an emission failure never fails the verb, the remedy, or the sweep,
and a denial never depends on a row landing (I3).

---

## F. Rail-set satisfiability (P5 load gate)

`Rules.load!` gains `identity/producers.toml` as a **load input** (finding 4):
`Rules.load!(base_dir, valid_verbs, producers)` where `producers` is the parsed
producer registry (the same file p3's Lane C loads — `{kind → command}`, e.g.
`tests`/`smoke`). After per-statute validation and the r6 duplicate check, the
**full set** is checked against a **CLOSED, STATIC producer registry** for two
decidable deadlock classes. A failure raises and stops the boot (I8).

**F1 — PRODUCER EXISTENCE (dead-fact deadlock).** Applies only to **verdict-fact
gates** — a `deny_when` condition of the form `<VF> not_in [K1..Kn]` where `<VF>`
is one of p3's canonical verdict facts, each with its `assignment.` prefix:
`assignment.verdicts`, `assignment.independent_verdict_kinds`,
`assignment.cross_harness_verdict_kinds`, `assignment.cross_provider_verdict_kinds`,
`assignment.produced_verdict_kinds` (**`assignment.verdict_kinds_any` is purged —
p3 deleted that fact**, finding 4). Script-effect gates are exempt (the
script-K rule, §A1). A `not_in [K1..Kn]` gate is **satisfied by producing ANY one
Ki** — so F1 requires a producer for **at least one** Ki, not all.

The valid producer set is a **closed, static union of exactly THREE sources**
(finding 4 — no blanket "any agent-created review assignment counts"; that made
almost every kind theoretically producible and defeated the check):

1. **In-statute remedies:** a statute whose `[rule.remedy].produces` is one of the
   gate's Ki (and, for an independence-fact gate, the remedy carries
   `reviews="{assignment_id}"` — the review-link the fact requires, p3 invariant 6).
2. **`producers.toml` entries:** the load-input registry. For a
   `produced_verdict_kinds` gate, a registered producer verb whose stamp emits Ki
   (p3's `run-tests`→`tests-passed`, `run-smoke`→`real-run-passed`). This is the
   ONLY producer for `produced_verdict_kinds` (substrate-written `producer` column).
3. **`external_producer = true` on the gate:** the statute's documented intent
   (§C1) that Ki arrives from an agent/user workflow the loadset cannot see — the
   escape hatch for plain `assignment.verdicts` gates an org fills manually, or an
   independence gate whose reviewer is commissioned outside this statute. There is
   NO implicit "open attestation always produces" rule; the annotation is required.

F1 rejects a gate iff **none** of the three sources covers **any** Ki. The error
names the **single gate statute** and the missing kind(s) (finding 4/7 — it cannot
"name both statutes"; only the gate exists). F2's error names two. (A user override
of a review gate is the escalation/ruling path, not a verdict that lights the fact;
it counts only if the gate declares `external_producer=true`.)

**F2 — REMEDY REACHABILITY (blocked-producer deadlock).** For each statute with a
remedy `R` dispatching verb `W`, two checks:

- **(a) Constitutional acceptance (finding 5).** `W`'s handler MUST admit the
  reserved remedy principal for `R`'s declared `action` (§C2's per-action
  acceptance seam). A remedy whose `action` a handler does not admit — e.g.
  `action="assign"` where `principal_allowed` does not accept `{:remedy,
  %{action:"assign"}}` — is rejected at load (a constitutionally impossible
  producer, which the old F2 could certify reachable). The admitted set is fixed
  by §C2: `assign`, `spawn`, `wake` each admit their own action; nothing else.
- **(b) Provable pure-deny blocker.** Let `A` be the attributes `R` fixes: `verb =
  W` and `caller.origin_class = "remedy"` (the reserved class, §C2). Those two ARE
  the closed attribute→fact mapping — nothing else (narrowed by Flynn ruling,
  adjudication #4, 2026-07-24: the earlier text also promised literal
  remedy-target/param values mapping to `target.*`/params facts, a dictionary
  that was never defined and that no statute has needed — role literals need
  runtime resolution, spawn fixes no target session, list params have no fact
  shape. If a real statute ever needs finer blocking analysis, the per-action
  mapping table is designed THEN, as its own spec change). A statute `S'` is a
  **provable blocker** iff `S'` guards `W`, is pure-deny (no remedy), every
  condition is over an `A`-fixed fact, and all evaluate true under `A`. Because
  remedy dispatches carry `origin_class="remedy"`, a quota rail keyed on
  `origin_class="agent"` does NOT match (§C2) — so ordinary agent quotas never
  block remedies, by construction. A rail explicitly `deny_when=[{origin_class eq
  remedy}]` on `W` is a provable blocker → rejected, naming both `S'` and the
  remedy's statute.
- **(c) Bounded producer chain.** If `W` is itself a gated **verdict-producing**
  verb whose own gate carries a remedy dispatching `W'`, the walk recurses on `W'`
  with a visited set; a cycle in which every node is gated-with-no-escaping-
  producer is rejected (the roadmap's producer-chain requirement). The walk is
  bounded by the finite statute set and terminates on the visited set.

**Bound, stated honestly.** F2 is conservative: it rejects only *provable*
deadlocks over attributes the remedy fixes plus the constitutional-acceptance
check. A rail that forbids the producer on *runtime state* the remedy does not fix
— a rail keyed on `caller.verb_count_24h` for the `remedy` origin class, say — is
NOT rejected at load, because the count is unknown at load and the deadlock is
conditional (it may not be hit). Such runtime deadlocks are caught where they
occur: the producer dispatch denies loudly (its own `denied` row + `rail_remedy`
outcome `"blocked"`), the remedy-rate signal spikes (guidance-spec §6g), and the
turn-end step escalates the still-open obligation to the orchestrator via
supervision's ladder (§D2.4). Load catches the static class (dead facts,
constitutionally impossible producers, provable pure-deny blockers, producer
cycles); runtime + observability catch the conditional class. Neither is silent.
This is the "single-statute validation cannot catch this" guarantee (I8) for the
statically-decidable class, with the runtime class explicitly out of load scope.

---

## Per-phase implementation seams (real files) and acceptance contracts

Each phase names the real modules it touches and keys its acceptance to the
conformance smoke-set classes (C5 = script guards, C6 = remedies, C7 = sweep;
the smoke-set spec is drafted in parallel — reference the classes, do not define
fixtures here).

The three phases are **sequential on `rules.ex`/`dispatch.ex`**, not parallel
lanes (finding 16): P4 adds the grammar + dry decision + script effect, P5 adds
remedy grammar + firing + satisfiability, P6 adds the turn-end filter + the
supervision fold. Each depends on the prior. They are one implementation stream.

### P4 — Script effect (+ the dry decision API)

**Seams.**
- `lib/tightbeam/rules.ex` — `@rule_keys` gains `edges`, `check`, `effect`;
  nested `[rule.check]`/`[rule.check.effects]` validation; `validate_rule!`
  enforces §A1. Introduce **`Rules.decide(db, call) :: {decision, to_close,
  to_consume}`** — THE decision function (§B), **effect-free on enforcement** (runs
  scripts + writes `rail_script` rows, but fires no remedy/prod, opens no
  decision-request, consumes no ruling, mutates no domain/work state): reads
  `call[:edge]` (`:verb` default | `:turn_end`), predicate-then-script order, returns
  the `decision` `:allow | {:deny,…} | {:remedy,…} | {:escalate,…}` plus the
  evaluated-prefix `to_close`/`to_consume` lists (§B). `Rules.evaluate/2` KEEPS its
  exact `:ok | {:deny,…}` contract,
  reimplemented as a wrapper over `decide` that collapses remedy/escalate to a
  plain deny **without firing** (§B — legacy/non-actor callers).
- NEW `lib/tightbeam/rail_script.ex` — the contained executor: scratch lifecycle,
  invocation-context resolution (§A2.2, via `Placement.holder_workdir/2`),
  `Containment.rail_profile/1` (the rail-seam renderer, §A4), invokes the Rust
  `rail-exec` wrapper, decodes its
  exit-band class (§A3), stdin call+context JSON, stdout token. Unit-testable
  against fixture scripts.
- NEW Rust `tightbeam rail-exec` — a form in the `contain` module
  (`cli/src/contain.rs`): `setpgid`, per-OS containment staging + contained
  spawn (§A3/§A4), `--timeout-ms` timer, `killpg(-pgid, SIGKILL)` on timeout,
  the four-way exit-band encoding (0/10/20/30, §A3). This is the process-group +
  profile-vs-child custody finding 11 requires.
- `lib/tightbeam/placement.ex` — `holder_workdir/2` is p3's pinned public workdir
  seam (finding 10); §A2.2 resolves the holder workdir through it. NO
  `Gateway.session_workdir/2` promotion.
- `lib/tightbeam/dispatch.ex` — **switches from `Rules.evaluate` to `Rules.decide`**
  and acts on the full decision (the verb-edge actor, §B); threads the additive
  `{:deny, error}` payload (§E1).
- `lib/tightbeam/event_log.ex` — `lifecycle/4` writes `rail_script` rows (open
  CHECK, no schema change); NEW `EventLog.rail_denials/3` (§E2, payload-projecting
  read).
- Identity repo: `identity/rails/scripts/` (git-tracked, executable);
  `identity/rules/*.toml` statutes gain `[rule.check]`.

**Acceptance (C5).** A `[[rule]]` with `[rule.check]` names a script that runs
contained (CWD = holder workdir, write = scratch) and gates the verb. The
fail-closed matrix (§A3) holds via the `rail-exec` exit bands: pass / out-of-set /
`script_error` (child nonzero, incl. in-sandbox EPERM = exit 10) / `script_timeout`
(exit 20) / `script_contained_refused` (profile-apply failure = exit 30, NOT an
in-sandbox denied op). Each non-pass denies with its named reason and
`script_exit_class`, writes a `rail_script` row, and (on deny) a `denied` row
retrievable via `EventLog.rail_denials`. A deny reached without the wrapper's
observation records `unreported` (§A3), and no path records a class the observation
would have carried but did not — including on the wrapper's own side, where the
child-exit line is written only for a child exit it saw. A satisfied gate is agent-silent. The
predicate pre-filter gates the script (a would-crash fixture behind a non-matching
predicate never runs — r6 laziness, extended). `Rules.decide` returns the decision
without firing (dry API).

### P5 — Remedies + rail-set satisfiability

**Seams.**
- `lib/tightbeam/rules.ex` — `[rule.remedy]` grammar + per-action target/param
  validation + interpolation typing + the `external_producer` field (§C1);
  **`Rules.load!(base_dir, valid_verbs, producers)`** takes `identity/producers.toml`
  as a load input (finding 4) and runs the §F pass (F1 closed-3-source producer
  existence; F2 (a) constitutional acceptance, (b) provable pure-deny blocker, (c)
  bounded chain), raising and naming statutes.
- NEW `lib/tightbeam/rail_remedy.ex` — resolves binding tokens (§C1) and the
  role→session via `Roles.resolve/2` (§C2), runs the **CAS episode claim + the
  pre-dispatch lease** against `rail_remedy_episodes` (§C3:
  `claimed→dispatched→live→closed`, atomic single-row UPDATEs guarded by the
  row-fencing `claimToken`, TTL/dead-`live` reclaim; the lease `claimed→dispatched`
  fences the external dispatch). Dispatches the producer verb under the **reserved
  remedy principal** (§C2) through `Dispatch.dispatch/3` with `--key = the
  OCCURRENCE key` (`"rail-dispatch:"<>statute<>":"<>subject<>":"<>occurrence`, §C3 —
  NOT the claimToken; ≤1 external effect per occurrence), and re-wakes with the
  occurrence+rewakeCount key. On denied dispatch releases the lease (`blocked`,
  §C3.2). Returns the episode outcome for the `denied` payload + `rail_remedy` row.
  Owns `ensure_schema/1` for `rail_remedy_episodes` (registered in
  `Gateway.children/1`). The **episode closure** on a passed statute (§C3.5) is
  performed by the ACTOR (Dispatch or Supervision), not here.
- `lib/tightbeam/assignments.ex` — `principal_allowed` admits `{:remedy,
  %{action:"assign"}}`; `principal_id` maps it to `"user:"<>owner`; **`opener/1`
  gains `opener({:remedy, %{owner: o}}) → {o, nil}`** (finding 2 — assign creation
  calls `opener/1`). No other authorization change.
- `lib/tightbeam/event_log.ex` — **`serialize_principal({:remedy, %{statute,
  action}})` → `"remedy:<action>:<statute>"`** (finding 2 — the map cannot ride the
  tuple interpolation).
- `lib/tightbeam/gateway.ex` — the spawn handler admits `{:remedy,
  %{action:"spawn", owner}}` (owner as `owner_user_id`); `wake` admits `{:remedy,
  %{action:"wake"}}`.
- `lib/tightbeam/rules.ex` (fact) — `caller.origin_class` computes `"remedy"` for
  a `remedy:` origin (a new closed value; existing quota rails keyed on `"agent"`
  do not match it, §C2/§F2).
- `lib/tightbeam/dispatch.ex` — a `{:remedy,…}` decision at the verb edge fires
  `RailRemedy` then denies with `reason="remedy_fired"`.
- `lib/tightbeam/idempotency.ex` — **reused normally** for the producer dispatch
  (episode key as the idempotency key, finding 2d); the `rail_remedy_episodes` table
  owns the episode *lifecycle* (claim/CAS/close/reopen), `wire_idempotency` owns
  dispatch-level dedup. Two roles, no conflict.

**Acceptance (C6).** A gate with an absent required fact dispatches the producer
under the remedy principal (proving `assign`/`spawn`/`opener` accept it — findings
2/5), claims an episode + wins the pre-dispatch lease, blocks the verb, and the
ACTOR closes the episode (`live→closed`) when the producer files `reviewed-clean`
on its `reviews`-linked assignment and the holder re-dispatches. **≤1 external
effect per occurrence (r6):** a fixture where a TTL reclaim steals the row while the
ORIGINAL claimant's dispatch still runs asserts exactly ONE producer — both dispatch
under the SAME occurrence key and the forever `wire_idempotency` ledger dedupes the
second; the TTL-stale-claim reclaim does NOT bump `occurrence`. **Terminal-exit
occurrence bump (r9):** a `closed`-episode **reopen** and a dead-`live` replacement
each BUMP `occurrence`, proven by a fixture that closes an episode, then re-fires and
asserts a genuinely NEW producer (a distinct wire key) — NOT the old producer the
spent key would return. **Stale-claimant row fencing:** a superseded claimant loses
the `claimed→dispatched` lease CAS and performs no external dispatch.
**Denied-dispatch retry (finding 3b):** a `blocked` producer dispatch releases the
lease and the NEXT firing edge re-claims and re-dispatches (across two edges).
**Multi-statute closure (finding 3d):** with S1 passing and S2 denying over one
subject, S1's episode closes and S2's stays `live`. **Re-wakes land:** each re-wake
bumps `rewakeCount` for a fresh key.
An unbound token/role fails closed (`unbound`, no dispatch). Satisfiability:
`produces` a gate does not require → load error; `produced_verdict_kinds` with no
`producers.toml` entry → F1 load error naming the single gate + kind; a gate over
any verdict fact with none of the 3 producer sources → F1 load error; a remedy
`action` a handler cannot admit, a provable pure-deny blocker, or a producer cycle
→ F2 load error naming both. Runtime conditional blockers **load** and surface as a
loud `blocked` outcome.

### P6 — Turn-end sweep (folded into supervision)

**Seams.**
- `lib/tightbeam/supervision.ex` — **MODIFIED** (the fold, finding 8): the
  `evaluate_terminal` `with` chain (supervision.ex ~177) is **restructured** so
  `holder_state` is hoisted above `Wakes.pending_count` and the rail step nests in
  the `:live` branch (§D2's exact ordering — finding 7 + FRESH-1 r6: after liveness,
  before pending-wake). Reuses `lastEvaluatedTerminal` dedupe/watermark and drain.
  Calls `Rules.decide(db, synth_call)` (`edge: :turn_end`) and, on `{:remedy,…}`
  with `Wakes.self_pending_count == 0`, `RailRemedy` (episode-claimed).
  **Named return-signature change (FRESH-3):** `Supervision.evaluate/5` today returns
  one of `:idle | :busy | :continuation | :duplicate | :coalesced | {:prodded, k} |
  {:escalated, rung, target} | :terminus | :stranded | {:refused, code}`; this fold
  ADDS `{:acted, :rail_remedy} | {:acted, :rail_escalate} | {:held,
  :adjudication_hold}` to that union (the acted branches + the model-adjudication hold,
  §D2). Call sites already ignore the tag (it is test-only), so the addition is
  source-compatible; it is documented here as an explicit ground-truth signature
  change, not a silent one. **Named ordering consequence (FRESH-1 r6):** a retired
  holder with a pending wake now yields `:stranded` (doorbell) where the old order
  yielded `:continuation` (§D2). No second GenServer, no second `:on_terminal` cast
  (finding 16's "omitted RailSweep in children" is moot — there is no RailSweep).
- `lib/tightbeam/wakes.ex` — NEW `Wakes.self_pending_count(db, session_key)`:
  pending wakes where `sessionKey = creatorSessionKey = holder`, on wake-on-fact-v1's
  durable `creatorSessionKey` column (§4.2), NOT the mutable `origin` (§D2.1,
  finding 10). The existing `pending_count/2` is unchanged (supervision's
  fallthrough prod path keeps it).
- `lib/tightbeam/event_log.ex` — `rail_sweep` lifecycle rows.
- `lib/tightbeam/gateway.ex` — **no change** (the `:on_terminal` closure already
  casts to `Supervision`; the fold needs no new wiring).

**Acceptance (C7).** An agent that finishes-and-idles with an open,
gate-unsatisfied obligation (the reviewable-work observable is the gate-unsatisfied
decision itself, not a `progress` attest — finding 10) runs the remedy XOR the
prod, once, via the episode claim; `rail_sweep` records `run-remedy`. An agent
with a **self-scheduled** continuation wake triggers neither remedy nor prod
(`Wakes.self_pending_count > 0`, finding 10) — the no-false-positive guarantee
(I6); a user reminder or supervision prod does NOT suppress it. A gate-unsatisfied
obligation whose turn-end statute has **no remedy** re-obligates via supervision's
prod (finding 9); a merely abandoned obligation with nothing owed to a gate takes
supervision's normal path. One adjudicator, one reaction per terminal, dedup'd by
supervision's watermark (finding 8).

---

## Composition notes and open dependencies

- **Escalation (`escalate` effect).** The effect token and the §B act-step
  hand-off are defined here; the engine is `escalation-substrate-v1`, whose seam is
  a **three-part split** (its §9): **`resolve/3`** is the in-fold, effect-free read,
  unified four-shape union `:allow | {:allow, ruling_id} | {:deny, e} |
  {:needs_request, dr_id|nil}` (`{:allow, ruling_id}` = ruling-sourced, its id
  collected into `to_consume`; `dr_id` non-nil = already-open → the actor re-returns
  `{:decision_pending, dr_id}` without opening), which `Rules.decide` folds; **`escalate/4`** is the effect (open
  the decision-request, deliver to the owner) called only on `dr_id == nil`, and
  returns **only** `{:decision_pending, id}`; **`consume/2`** is the actor's
  per-ruling CAS. Plus `decision_requests` +
  `escalation_waivers`, ruling facts, waivers, owner delivery. It is **rewritten to
  Flynn's ruled model** (Q1–Q4 resolved). The roadmap's sequencing is **satisfied**;
  statute loading of an `escalate` effect gates on that spec's adversarial review
  landing clean, not on ratification. P4–P6 do not depend on it; it composes now.
- **Producer strength.** This mechanism enforces fact **existence**, never
  quality (check-tier T1, inherited). Producer strength (self-attested < judge <
  mechanical < exogenous) is a property of WHICH fact a gate requires and WHO the
  remedy spawns — expressed in the org's rail TOML, not in this mechanism. The
  mechanism gives every strength the same machinery (guidance-spec §6 «both are
  the same mechanism»).
- **Restart pickup (I9).** A rail or script change is picked up at gateway
  restart via the existing boot-load of `identity/rules/*.toml` and the
  home-manifest hash that already makes a law change an identity change
  (rails.ex). No live reload (G1).

---

## §6 model tensions — surfaced, and their team-lead rulings (2026-07-21)

Seven places the merged substrate met the guidance-spec §6 model at an edge were
surfaced for adjudication rather than resolved silently. Each now carries its
ruling; this spec is written to the ruling. Kept in the spec because they are the
load-bearing decisions an adversarial reviewer must see justified.

**X1 — Independence is CROSS-HARNESS, not cross-model. RULED.** §6's original
enforcement-mapping row said «`reviewed-clean`, author ≠ producer, cross-model»,
but `derived-model-catalog-v1.md` rules model ids **opaque, never parsed into
family** — so cross-**model** is not substrate-expressible. RULING: independence
is enforced as **cross-harness** — author session's `harness` ≠ producer
session's `harness`. Harness is substrate-known, so no model-id parsing and the
catalog's opacity ruling is preserved. This is exactly
`p3-observables-producers-v1.md`'s registered fact
`assignment.cross_harness_verdict_kinds`; the two specs are **coupled** and the
§C1 worked example gates on it (`reviewed-clean` + author-independence +
cross-harness). The guidance spec's «cross-model» wording is being updated to
«cross-harness» to match (team-lead's edit, not this spec's). The same-harness
fallback (a fresh session at a higher thinking level) is **guidance-level, not
rail-enforced** — the rail gates only on the cross-harness fact.

**X2 — Agent-silence + substrate-recording is the design. RESOLVED.** §6's
red-tape test («silent when satisfied») and its accountability requirement
(«every invocation is a recorded event») are not in tension — they address two
audiences. RULING: the split is intended and canonical — silence is agent-facing
(no context injection; `rails.ex` THE INVARIANT), recording is substrate-facing
(an observability row). §E implements exactly this: satisfied gates emit nothing
to the agent and a `rail_script`/`rail_remedy`/`rail_sweep` row to
`lifecycle_events`.

**X3 — Scripts are sync-only; judgment is gate-on-fact + remedy. RESOLVED.** §6's
«a judgment the script delegates by spawning a session — both are the same
mechanism» read literally against «async judgment is never a blocking call» was
the only genuine contradiction. RULING: this spec's narrowing is now the
canonical model — the guidance spec §6 has been amended (team-lead's edit) to
state scripts are **sync-only** and judgment is **gate-on-fact +
remedy-originated**. A script may only *trigger* a remedy (return a
`remedy`-mapped token), never *await* a judge (I2). No open item remains.

**X4 — `escalate` sequencing: SATISFIED.** `escalation-substrate-v1` is now
rewritten to Flynn's ruled model (Q1–Q4 resolved). The multi-shape resolution lives
in the **in-fold, effect-free `resolve/3`** (unified four-shape union `:allow |
{:allow, ruling_id} | {:deny, e} | {:needs_request, dr_id|nil}`, folded by
`Rules.decide`, §B); the effect `escalate/4` returns **only** `{:decision_pending,
id}`; and `consume/2` is the actor's per-ruling CAS. So the roadmap's sequencing
(escalation before any org escalate-rail) holds. Remaining gate: statute loading of
an `escalate` effect is a load error only **until that spec's adversarial review
lands clean** (§A1) — not "unratified," which is done. The effect vocabulary (I4) is
unchanged; only the delegation's return handling carries the four shapes (at
`resolve/3`).

**X5 — Denied-payload extension + `lifecycle_events`. ACCEPTED.** The `events`
CHECK admits only `verb|denied`; widening it is a rebuild migration. RULING:
accepted as designed — the agent-facing record extends the denied row's
**payload** (§E1, no migration) and the per-invocation corpus lives in
`lifecycle_events` (open CHECK). Denied rows are the agent-facing legibility;
lifecycle rows are the tuning corpus. Two tables by design.

**X6 — Network-open scripts; git-tracked law is the v1 compensating control.
ACCEPTED.** Only the `open` network posture is implemented (`containment.ex`:
the SBPL allows `network-outbound`; the linux seam leaves network rights
unhandled, §A4), so v1 rail scripts run network-open — the write-wall (scratch-only) and time-box
hold, the network-wall does not. RULING: accepted, with the trust model stated
explicitly — **rail scripts are reviewed, git-tracked law from the identity
repository, not arbitrary agent-supplied code** (I9); that review is the v1
**compensating control** for the network-open posture. The network-denied rails
profile is future hardening, landing when the loopback posture lands.

**X7 — Predicate-first + time-box is the v1 mitigation; worker pool is future
work. ACCEPTED.** `dispatch.ex` runs `Rules.evaluate` in the caller's process, so
a synchronous script blocks that transport process for up to `timeout_ms`.
RULING: accepted for v1 — the predicate pre-filter (I1, scripts run only on a
cheap predicate match) plus the time-box is the mitigation. Moving script
execution to a bounded worker pool off the caller process is **named as future
work, out of scope** for v1 (it changes the dispatch shape).
