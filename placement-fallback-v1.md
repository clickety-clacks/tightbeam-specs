# Placement fallback — a denial must not be a dead end

Status: **DECIDED 2026-08-02 by Flynn, not yet implemented.**

## The problem, in Flynn's words

> "there should be a fallback! at any time any model or harness could run out of tokens. we
> can't let substrate stop all work because this happens. if this was just agents without a
> substrate the orchestrator would literally just pick a different model and harness from the
> fallbacks, or even ask the user"

Raised after a live install where `spawn` refused twice in a row and stopped everything:

- `placement_denied: claude on eezo needs onboarding: :in_progress` — chose a harness with no
  credential while a fully onboarded one (codex/openai) sat available on the same host.
- `catalog_unavailable: cannot validate model "claude-sonnet-5[medium]" for codex on host
  eezo` — the archetype's default model is an anthropic ref, so pinning `--harness codex`
  fails on a default that harness can never offer.

Both refusals are correct about the fact and useless as an outcome. The operator had a
working credential and a populated catalog the whole time.

## What already exists, and does not work

`archetype.model_preferences` is **declared, stored, and projected to clients**
(`gateway.ex:1136`, `:1182`, `:2765`; `archetypes.ex:22`, `:598`) and **never consulted at
placement time**. It is a ratified-unconsumed field: the mechanism intended for exactly this
was built and left inert, and every seed archetype leaves it `[]`.

## The ruling

**The substrate does not invent fallback policy, and it does not dead-end either.** Three
parts, in order:

1. **Honour recorded intent.** When an archetype declares `model_preferences`, placement
   walks them in order. This is not the substrate choosing — a mind recorded that order, and
   honouring a recorded preference is substrate work. See
   `substrate-records-inference-acts`.
2. **Never silently.** Whatever is placed, the result names which preference was used and why
   the earlier ones were skipped. A substitution the caller cannot see is worse than a
   refusal, because it makes a model change look like a model choice.
3. **Make the denial actionable.** When nothing is declared, or every declared option is
   unavailable, the refusal must carry the healthy alternatives — the harnesses and model
   refs that WOULD work on that host right now. Today `classified_denial/2`
   (`gateway.ex:3154`) returns a code, a message, and a detail map with none of that, so a
   mind must make a second round-trip to `list` and re-derive what the substrate already
   knew. Then a mind picks, or asks the user, which is a legitimate terminal branch.

**Out of scope, deliberately:** the substrate does not retry, does not rank models by quality
or price, and does not decide when a fallback is "good enough". Those are product judgements
and belong to the mind receiving the alternatives.

## Also to fix, same area

The default model on a seed archetype is an anthropic ref, so `--harness codex` fails on the
default. Either defaults are per-harness, or the default is resolved against the chosen
harness's catalog rather than assumed.

## Why this matters beyond convenience

A token exhaustion, an expired credential, or a vendor outage is an ordinary Tuesday, not an
exceptional condition. A substrate whose response is to stop all work converts a routine
supply problem into an outage. The point of recording preferences is that the recovery needs
no human present — see `dark-factory-doctrine`.
