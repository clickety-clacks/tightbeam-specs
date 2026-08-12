# Model identity is structured — packed strings are line formats

Status: **DECIDED 2026-08-02 by Flynn, not yet implemented.**

> "tightbeam should not be using the [] to mean anything. when model names come in they
> should cross a seam and within it tightbeam should be modelling them as a structure or an
> object that breaks out the individual fields that describe a model. only when crossing
> adapter boundaries should identifiers in a format that the harnesses understand be
> constructed, by that adapter, from the internal representation, and vice versa."
>
> "make it multi field. they ARE different fields. other representations are line formats."

## What went wrong, concretely

Two systems use `name[suffix]` to mean unrelated things.

- Anthropic: **context window.** `claude-fable-5[1m]` is Fable with a 1M-token context.
- Tightbeam: **reasoning effort.** `claude-fable-5[high]` is Fable thinking hard.

Because the syntax matches, our catalog read the vendor's suffix as ours: it stripped `[1m]`,
discarded that it existed, and re-attached our five effort levels. Nothing errored — the
1M-context variant simply ceased to exist, and no operator can ask for it. A vendor suffix
that happened to collide with one of ours (`[max]` meaning maximum context, say) would be
read as a reasoning level and be confidently wrong rather than merely lossy.

## The rule

**Inside Tightbeam a model is a structure with named fields.** Nothing but a seam ever sees
a packed identifier, and every packed identifier is a LINE FORMAT — a serialization for a
place that needs one line of text, owned by the code at that boundary.

Three seams, each owning both directions:

| Seam | Outside form | Owns |
|---|---|---|
| Harness adapter | the vendor's identifier (`claude-fable-5[1m]`, `gpt-5.6-sol`) | per-harness parse and render |
| CLI | operator flags | flags ↔ structure |
| Wire | JSON with named fields | payload ↔ structure |

The database is already correct: `sessions` stores `model` and `thinkingLevel` as separate
columns. It is the transport format that leaked inward and became the currency.

## The fields

At minimum, and named because they are different questions:

- **family** — which model (`claude-fable-5`, `gpt-5.6-sol`). The vendor's name for the model
  itself, without decoration.
- **effort** — reasoning level, Tightbeam's vocabulary (`low`…`max`). Ours, not theirs.
- **context** — the context-window variant when the vendor offers more than one (`1m`).
  Absent means the model's default.

Capabilities (supported efforts, max input tokens) stay attached to the catalog entry, not
folded into the identity.

## What moves

`Adapter.parse_model_ref/1` is the seam already — it unpacks right before talking to the
harness — but it sits on the wrong side, so 37 call sites upstream build and parse packed
strings to hand it one. It becomes **adapter-private**, gains a rendering counterpart, and
callers pass the structure.

The catalog stops publishing a packed `ref`. Placement, spawn, and the gateway pass the
structure through. `base_ref/1` disappears: nothing downstream needs to strip a suffix,
because nothing downstream ever receives one.

## Selection, per the ruling

The operator selects fields, not a packed string:

    tightbeam spawn --harness claude --model claude-fable-5 --effort high --context 1m

Stored selections — archetype defaults, preferences — hold the fields, not a rendering. A
packed default is one vendor collision away from reintroducing this bug, and it cannot
express a field the vendor added after it was written.

## Sequencing

This is a real refactor across ~37 sites and it should land on its own branch, after the
current onboarding work is reviewed and merged. Stacking it makes both harder to review.

The migration has a floor that makes it safer than it looks: the DB already separates model
from thinking level, so no stored session data has to be reinterpreted — only the catalog,
the transport, and the selection surface change.

## The test that would have caught it

A vendor identifier whose suffix is NOT one of Tightbeam's efforts must survive a round trip
through the adapter seam without losing information. `claude-fable-5[1m]` in must produce
`claude-fable-5[1m]` out. Today it produces `claude-fable-5`, and that is the whole defect
in one assertion.
