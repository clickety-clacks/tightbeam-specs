# Golden jobs — whole-system evaluation corpus — v1

Status: DRAFT r1 (Opus-authored 2026-07-25). SPLIT from job-eval-v1: this is the CORPUS
half (the substrate-observability half is `job-trace-observability-v1`, which this
depends on — it scores from that spec's `work-item-trace` artifacts). Sequenced AFTER
both job-trace-observability-v1 AND work-item-brackets-v1 (Tier A evals the silent-
dropper bracket pathology). Carries the three r3-gate findings that were the hard,
non-converged part of the original spec (F6 stall carrier, F7 script schema, F8 probe
trust boundary) — to be resolved in THIS spec's own gate.

## Law 0 — no ceremony (inherited, binding)

Same as job-trace-observability-v1: nothing an agent must remember; no eval artifact an
agent can produce instead of the work. The Tier-B outcome probe (below) is the sharp
edge of this law — correctness scored from an IMMUTABLE out-of-band oracle, never the
agent's own attest/worktree.

## Part 3 — golden jobs (the fixture-problem corpus)

A corpus at `priv/golden_jobs/` (problems + oracles + expected envelopes), run by one
driver against a fresh org (feature_smoke provisioning doctrine), scored from
`work-item-trace` artifacts. Two tiers:

- **Tier A — deterministic, evals the SUBSTRATE.** Requires a SCRIPTED ACP FIXTURE
  BINARY (gate F6 — `Harness.Fixture` today is selection scaffolding expecting an
  external `fixture-acp` that does not exist; this lane ships it): a small
  script-driven ACP implementation (the `fixture-acp` binary this lane ships,
  replacing the missing external one Harness.Fixture points at) driven by a PINNED
  SCRIPT SCHEMA: a corpus entry's `script.json` maps ACP request types
  (session/new, session/prompt) to programmed responses — emit N text chunks then a
  stop_reason; emit a tool_call that touches / does-not-touch the worktree; end the
  turn without filing; surrender. The pathology is SELECTED by the corpus entry
  naming its script; the driver injects it via the fixture harness's launch env. The
  schema covers exactly the ACP methods the lane paths exercise; anything outside it
  is a hard error, not a default. This emits pre-programmed behavior per pathology — the staller (turns
  without worktree effect → expect effort check-in at horizon, request at the right
  expecter), the surrenderer (→ escalation), the prod-ignorer (→ ladder climbs), the
  silent-dropper (item never routed → bracket 1 nags), the bad-worker (wrong output
  → reviewer verdict). Because behavior is scripted, oracles are EXACT and asserted
  from the trace alone; CI-able; prompts/models cannot affect it. This tier is
  regression armor for the substrate.
- **Tier B — live minds, evals the SYSTEM.** Small real problems with an INDEPENDENT
  OUTCOME PROBE (gate F7 — the load-bearing anti-Janus rule): correctness is scored
  from `{trace, outcome_probe}` where the outcome probe is OUT-OF-BAND and IMMUTABLE
  (gate F8 — running the test inside the agent's own worktree lets the agent edit or
  delete the test and manufacture green; changing who runs it does not fix the trust
  boundary). Mechanism: the ground-truth oracle (the seeded failing test + its config)
  is stored in the CORPUS, not the candidate worktree; the probe takes the agent's
  produced diff, applies it to a FRESH checkout of the original repo, OVERLAYS the
  corpus's immutable oracle on top (so any agent edit to the test is discarded), and
  runs it in a trusted sandbox the agent never touched. The agent's worktree is
  evidence of what it did; the score comes from the agent's OUTPUT re-tested against
  the untouchable oracle. The completion attest is NOT the correctness
  oracle (an attest requires inference and can honestly be wrong; using it AS the
  score would let self-report substitute for work). The attest is still recorded and
  scored ALONGSIDE the probe as the calibration signal above — kept, not distrusted,
  its DELTA from reality being the useful measurement. Problems: a repo with a seeded bug + a failing test the fix must green;
  a bounded spec with acceptance tests; an AMBIGUOUS ask whose correct behavior is
  escalating to the user (the trace's escalation record is the oracle there — the
  one case the trace alone can judge, because "did it raise to the user" IS a
  substrate event). Scores are ENVELOPES (ranges); the harness's product is the
  ENVELOPE DIFF across a guidance/prompt/model change. Operator-invoked, never CI.

Corpus entries are DATA: `problem.md` (the job as dispatched), `setup/` (repos,
plants), `oracle.exs` (scoring against the trace artifact), `envelope.json` (expected
ranges, updated deliberately). Adding a problem is additive; no substrate changes.


## Open gate findings to resolve in this spec's rounds (carried from job-eval r3)

- **F6 — worktree-effect progress needs a trace carrier.** Stall counts a worktree
  effect as a timestamped progress event, but effort-probe evidence is per-generation
  row data, not a per-effect timestamp. Pin how "a worktree effect at time T" reaches
  the trace (a causal_events `worktree_effect` row at probe time, or read the
  generation's baseline-change timestamp) so stall is computable.
- **F7 — pin script.json fully.** Name every ACP method the lane paths exercise (not
  just session/new, session/prompt), the exact response grammar per method, and the
  hard-error-on-unlisted rule.
- **F8 — close manufactured-green fully.** The immutable overlay stops test DELETION,
  but a candidate can still edit application code the oracle imports, or the oracle's
  own dependencies. Pin the trust boundary: the oracle runs against the candidate's
  DIFF applied to a pristine tree with the oracle files RESTORED from corpus after the
  diff, in a network-isolated sandbox; anything the candidate changed that the oracle
  transitively depends on is part of what's under test (that's correct — a fix that
  breaks the oracle's real dependencies IS a failure), but the oracle test FILES
  themselves are always corpus-authoritative.

## Component touches

NOTE (2026-07-25): job-trace-observability-v1 descoped to already-attributable
families; the fine-grained supervision-internal transitions (adjudication reopens, rung
climbs, prod edges) moved to the deferred job-forensics-v2. Golden-jobs Tier-A oracles
that need those fine transitions depend on v2; the pathologies expressible from v1's
trace (staller via effort generations, surrenderer via decision requests, silent-dropper
via bracket dispositions, bad-worker via verdicts) proceed on v1. State each pathology's
trace dependency.

The scripted `fixture-acp` binary; the Tier-B out-of-band probe harness + sandbox;
priv/golden_jobs corpus + driver; envelope-diff tooling. NO substrate changes (consumes
job-trace-observability-v1's trace verb + brackets' dispositions as black boxes).
