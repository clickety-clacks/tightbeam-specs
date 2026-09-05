# Org heat v1 — spend the tokens on the work that matters

Status: PROPOSAL, 2026-08-31. Recorded from Mike's design conversation so the
idea survives outside a chat session. This document authorizes no
implementation, deployment, identity change, or live mutation. It needs a
reviewed successor before anyone builds it.

Author's note: this is a product sketch, not an implementation contract. The
clause-level design belongs in a successor written by whoever picks the card up.

## The problem

Token capacity is finite and sometimes scarce. Today every card in the
organization competes for it on equal terms. A priority 8 release blocker and a
priority 1 cleanup both get turns at whatever rate their wakes fire, so a quiet
period of heavy low-priority churn can spend the budget the important work
needed. The operator has no dial. The only lever is stopping the gateway, which
stops everything.

## What heat is

One organization-wide number. Turn it down and low-priority cards get their
turns spaced further apart, or stop getting turns at all, while high-priority
work keeps running at full speed. Turn it back up and the held work resumes from
its durable rows, exactly where it stopped.

Heat 1.0 is today's behavior: nothing is held. Lower values stretch the gap
between turns for low-priority cards. The stretch scales by priority, so the
higher the card's priority, the less heat touches it.

**Starving low-priority work is the intent, not a defect.** When tokens are
scarce the operator is choosing what does not run. A low-priority card that
takes no turns for a day under low heat is heat working correctly. Do not add a
floor, a fairness rule, or a minimum service rate. The organization already has
a way to say a card must run: raise its priority.

## What it builds on

Priority shipped on 2026-08-29 on both lines, main/0.2.0 `e9184ff` and 0.1.9
`0a14945`. Every work item and card carries a priority from 0 through 8,
defaulting to 4, inherited from the item by its cards, with an organization
default in `org_settings`. Priority already scales the card inactivity window by
halving and doubling around the default. Heat reads the same number, so an
operator who has already prioritized the backlog does not prioritize it twice.

## The mechanism

Every turn in Tightbeam starts from a wake, and every wake carries a `dueAt`.
Heat scales that one number as a function of the card's effective priority. High
priority keeps `dueAt = now`. Low priority under low heat gets a `dueAt` pushed
out, or no rearm at all until heat rises.

This keeps heat inside the scheduler. It changes no statute, no rail, no attest
vocabulary, and no completion rule. It writes no judgment: the operator sets the
number, the substrate does arithmetic on rows.

Wakes are durable, so a held card survives a gateway restart and resumes on its
own when heat rises. Nothing is dropped and nothing needs replaying by hand.

## Held by policy is not stalled

A card the operator is deliberately holding must not read as a card that broke.
The inactivity check shipped with priority fires on cards that have gone quiet;
patrols hunt stalls; both would see a heat-held card as a problem and try to
revive it.

So a heat-held card carries that fact in its rows. The inactivity check treats
it as not quiet. Patrols leave it alone. Anyone reading `toplines` sees the card
is waiting on heat rather than wondering who dropped it.

This is the one part of heat that is not optional. Without it the feature
manufactures the alerts it was built to avoid.

## Open questions for Mike

1. **The curve.** How much does one step of priority change the hold at a given
   heat, and does the lowest tier reach zero turns at some heat, or only at heat
   zero?
2. **Where heat lives.** An `org_settings` row like `default-priority`, set with
   `config set heat <value>`, or something with a schedule so it can drop
   overnight and recover in the morning.
3. **Who can set it.** Owner and admin only, or may a product owner turn its own
   subtree down.
4. **Whether heat is global or per line.** One number for the organization is
   the simplest thing that works; a per-owner or per-subtree number is a bigger
   design.

## Not in scope

Predicting what a turn will cost. Turn cost is variable and unknowable in
advance. Heat controls how many turns each priority tier gets, which is the only
lever that reliably moves spend. No token accounting, budget, or forecast is
required to build it.

## Related work not yet filed

- The stranded work item: an item with zero open cards has no holder, so nothing
  prods it and nobody is told there is more to do. The card-level inactivity
  check does not cover it.
- Snooze: a sanctioned "not important, come back in a week" for a work item.
  Today that means filing a blocker plus a scheduled wake, two verbs and a
  pairing the user has to remember, and the return depends on a single wake
  surviving.
