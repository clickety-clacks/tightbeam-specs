# CLI surface: what is ratified vs what ships — 2026-08-01

**Status:** analysis prepared for Flynn's ruling. Decides nothing. The ratified surface is
cli-surface-v1.md; this document only measures the distance between it and the code.

Flynn, 2026-08-01: "i need to know more about differences between the two surfaces."

## The two surfaces

**Ratified** — cli-surface-v1.md, whose demand rule is: *"A command family is in the
surface iff a shipped consumer instructs its use... A verb nothing references is not
shipped, however cheap."* Growing the surface *"means amending this enumeration FIRST."*

**Actual** — what the parser accepts, pinned by the test `help_enumerates_exactly_cli_surface_v1`
(cli/src/args.rs:1482). That test's name claims conformance to the spec. It does not test
conformance to the spec; it pins a different set. That is the FICTION: the suite is green
on a claim it never checks.

## Shipped but never ratified (10)

Each works today and is absent from the enumeration. The spec required amending the
enumeration first; that did not happen.

| Command | What it does |
|---|---|
| `identity` (edit/status/relearn/apply) | manage the org identity tree |
| `onboard <provider>` | this machine's credential onboarding flow |
| `attend [--high]` | elect the attention tier of the reply being given |
| `topline` / `toplines` | read-only roster views over work and assignments |
| `work-item-close` / `-fail` / `-icebox` / `-reopen` | work-item state transitions |
| `artifact-record` | promoted to top level; the spec has it as `artifacts (record/list)` |

These are not accidents — `identity` and `onboard` are load-bearing (a fresh Gibson
install runs `onboard` first), and the work-item verbs are siblings of the ratified
`work-item-create/get/trace`. The defect is procedural: real commands grew without the
enumeration being amended.

## Ratified but absent (3) — and the first scan got this backwards

An earlier scan reported these as a code gap: workflows told to produce mechanical
evidence have no command to call. **That is wrong, and the correction points the other
way.**

- `run-smoke` / `run-tests` — the spec calls them *"producer verbs the rails' remedies
  dispatch."* Searching all of `priv/` and `lib/`: **nothing references them.** No shipped
  kungfu, no rail remedy, no substrate code. The evidence names the spec implies
  (`tests-passed`, `real-run-passed`) appear nowhere either.
- `skill (list / put / rm)` — no wire verb exists. `put` and `rm` DO exist under other
  vocabulary: `identity edit <archetype> --skill <name> [--rm]`. Only `list` is genuinely
  absent.

So by the spec's own demand rule, these three have no shipped consumer and therefore do
not belong in the surface. **The gap is in the enumeration, not the code.** Building them
would add verbs nothing calls — precisely what the demand rule forbids.

## The choice

Three ways to close it, and they differ in what they cost:

1. **Amend the enumeration to match reality.** Add the 10 shipped families, drop the 3
   unconsumed ones, decide whether `artifact-record` is its own family or stays inside
   `artifacts`. Then fix the test to assert the amended list. Cheapest, and it is what the
   demand rule already implies.
2. **Build the 3 missing families.** Contradicts the demand rule unless a consumer is
   written too, which is a larger piece of work than the verbs.
3. **Split the difference** — amend for the 10, and rule separately on whether smoke/test
   producers are wanted as a capability. This is option 1 plus an open question, not a
   third path.

Recommendation: **option 1**, with the smoke/test producers recorded as a separate
question about whether rails should be able to dispatch mechanical evidence at all. That
is a product question about rails, not about the CLI surface.

Whatever is chosen, the test must stop claiming exact conformance until it asserts the
ratified list. A green test making a false claim is worse than no test, because it is
consulted instead of the spec.
