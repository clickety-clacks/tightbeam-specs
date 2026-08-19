# user-alerted → decision-request escalation (design discussion, parked)

Status: PARKED for a discussion with Mike. Work item wi_ad13e204 (unstaffed by
design — staff it with `assign --files '["user-alerted-decision-request-escalation.md"]'`
when the discussion is scheduled). Written 2026-08-19 by tb02 from the night's
specimens; Mike has ratified NOTHING here.

## The question (Mike's, 2026-08-19)

Should a `user-alerted` episode file a decision-request — and if so, how and
why? Raised after he misread the fact as an attention inbox and asked how he
would find alerts he slept through.

## What user-alerted actually is (verified in c1b0274)

The terminal rung of fault bubbling (productions/bubble.ex): the whole lineage
failed to hear, the substrate sent the owner ONE direct wire message (no model,
no tokens), and the standing fact records "the user has been told" while
suppressing repeat climbs. It retracts on the first delivered turn for that
owner — "recovery is recognized, never declared." It shuts down nothing:
suppression covers alert-climbs only. Dead-harness quarantine is separate
(supervision.ex harness_gate over harness-auth-dead / harness-rate-limit-dead,
scoped per harness+host).

## Specimens

Facts 653/654 (19:19:12→:20) and 655/656 (19:42:30, same second), both during
the 0.1.8 upgrade boot, both self-healed in seconds. Queryable forever; but
nothing obliges anyone to ever look.

## tb02 sketch (NOT ratified)

- No DR per episode: most self-heal in seconds; a DR with nothing to decide is
  ceremony, and auto-filed rows train the operator to rubber-stamp the one
  channel whose value is that everything in it needs him.
- Keep the latch untouched — one page per outage is correct and layer-invariant.
- Escalate PERSISTENCE only: a named org-authored rule watches for the fact
  standing longer than N minutes (episode did not self-heal) and files ONE
  decision-request keyed to the episode (idempotency key = fact id).
- Layering: fact stays physics; threshold + DR-filing is culture/law — a
  statute-engine case on the 0.2 line, not a hardcode in bubble.ex.

## Open questions for the discussion

1. N — and is it one org constant or per-owner law?
2. The DR's verb menu: re-staff, park, waive, acknowledge-only?
3. Auto-withdraw when capacity returns while open, or stays until Mike rules?
   (His stated instinct: things addressed to him stay until HE clears them.)
4. Same threshold pattern for harness-auth-dead / rate-limit-dead standing too
   long? Those quarantine prodding silently.
5. Land in 0.2 statute engine (layer-correct) or backport to 0.1.x?

## Deliverable when staffed

A one-page decision memo Mike can rule on — chosen answers to 1–5 with
rationale — filed as an artifact on wi_ad13e204. Not code.
