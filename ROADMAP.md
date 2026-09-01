# Tightbeam roadmap — living queue (updated 2026-08-21)

One page so nothing lives only in a conversation. Order is the ruled priority; each
line points at its spec. History and rationale: [tightbeam-decisions.md](tightbeam-decisions.md) and
[v0.2-program-2026-08-12.md](v0.2-program-2026-08-12.md). The pre-flip 0.1-era queue is preserved at
[archive/ROADMAP-0.1-era.md](archive/ROADMAP-0.1-era.md); 0.1.8 is frozen history and main is the only line.

## Now — the 0.2.0 MVP core (Mike's first-cut ruling, 2026-08-21)

Mike's stance, verbatim: "not looking for perfect operations, but a good core that we
can apply other work items to fix various bugs. just enough that the system could work."

The core is 28 items, elected and tiered by Product owner — Tightbeam 0.2.0
(spec: [0.2.0-spirit-and-work-sweep.md](0.2.0-spirit-and-work-sweep.md), the source of record for membership).
An item is core only if the truthful end-to-end work loop needs it, it closes a
security or data-loss critical, or it unblocks development itself.

First, the development blocker — nothing gates trustworthily until it lands:

- `wi_8f90c5b3` — the full Elixir suite is red on current main.

Then the loop and the criticals, in the PO's grouping:

#### Truthful work loop — 20 items
- `wi_c4450c8d` — Work cannot start truthfully while passive routing affinity can masquerade as staffed execution custody.
- `wi_7f068d0c` — Session-targeted assignments must retain the accountable role or the work record carries a false identity.
- `wi_032f11a6` — Completion must require evidence that matches the producer's real output, not fabricated or impossible artifacts.
- `wi_f6b4b8ad` — A blocked worker needs one durable handoff that returns the unresolved decision to its parent.
- `wi_236e5efa` — A terminal child must reactivate its open parent or completed and failed work strands below the owner.
- `wi_ecd8cd9d` — Cannot-proceed must remain a typed assignment state that routes upward instead of erasing custody through surrender.
- `wi_174a2b8b` — When unfinished work loses its repair holder, it must route upward immediately or the basic chain strands without execution custody.
- `wi_809821f8` — Child completion needs a durable parent disposition so the end-to-end chain reaches an accountable conclusion.
- `wi_113d569f` — An accepted work wake must reach delivery or a visible failed terminal state; otherwise work disappears at entry.
- `wi_c01e8f20` — An unrunnable target must fail visibly at send time so accepted work does not vanish into a dead turn.
- `wi_0abae0fd` — A canceled wake must retain requester, cause, and disposition so the substrate cannot erase accepted intent.
- `wi_7efb0887` — Process-submission and harness-execution failures must return as typed facts to the accountable owner.
- `wi_55b9755b` — The typed-failure contract needs this current-main path to preserve each known safe execution cause on the owning assignment.
- `wi_d018d4ed` — A dead-role delivery must never become text falsely attributed to Mike; identity and failure state must stay true.
- `wi_d8363deb` — Every Codex turn needs a truthful terminal outcome or execution state remains unknowable.
- `wi_24028d10` — A fresh org must choose an onboarded, runnable harness and model or no work can begin.
- `wi_a57dee58` — Supervision must derive its population from open assignments or live work can disappear from accountability.
- `wi_5870f52e` — An open live assignment must remain in the prod-and-turn transaction until a lawful exit.
- `wi_e27eb1a6` — Retry exhaustion must route upward with durable provenance instead of leaving failed work in limbo.
- `wi_62f23012` — Artifact digests must come from the referenced bytes or durable completion evidence can assert a false result.
#### Security and data-loss criticals — 7 items
- `wi_b8802849` — Workspace credential discovery must not let a child act as its parent session.
- `wi_9970877d` — Raw gateway calls must not impersonate Mike or bypass accountable identity.
- `wi_893b0503` — Review facts must not be fabricated or leak content across tenants.
- `wi_ddbf576f` — Operator shell state and cross-system details must not leak into agent prompts.
- `wi_38df6905` — Retirement must not delete dirty worktrees or uncommitted user work.
- `wi_472aa5d8` — Git-aware preservation is the mechanism that makes retirement unable to destroy work.
- `wi_609e19b9` — Released artifacts must retain retrievable content or completed deliverables are lost.

## Next — post-core (45 items, elected, deferred)

Land as ordinary work-item flow once the core exists. Full list and one-line
descriptions in [0.2.0-spirit-and-work-sweep.md](0.2.0-spirit-and-work-sweep.md) §TIER POST-CORE. Flagged dissent,
unruled: the kill/park primitive (`wi_6937890c`) is post-core, so the core
can see a wedged turn but not kill one — the 2026-08-20 nineteen-hour stall was
exactly this. Mike accepts or amends.

## Untargeted — specced and owned, not elected (no release target)

The observability read/notify program, ruled by Mike 2026-08-20/21 as
untargeted (0.2.0 or later; work branches from main tip when it starts;
none of it is in the 0.2.0 core election):

- [event-firehose-v1.md](event-firehose-v1.md) r5 — ws state-change notices: live-only doorbell,
  no history on the socket, canonical public projections shared with REST.
- [rest-state-api-v1.md](rest-state-api-v1.md) r1 — the formal REST read plane (r2 mechanical
  amendment reviewed-clean, canonical-adoption pending Mike dr_52456ca8;
  SQ2 admin-reads pending dr_bd47c1d7).
- [rest-vs-cli-adjudication.md](rest-vs-cli-adjudication.md) r2 — the ruling: REST is the read plane,
  verbs the write plane, the CLI is sugar. [rest-state-api-recon.md](rest-state-api-recon.md) is
  the adopted evidence.
- `wi_cb5734eb` — standing spec ownership: product-owner:rest-state-api,
  under product-owner:tightbeam-codex-sol-relief.
- `wi_9fdc0c07` — client-buildability recon (chat-client litmus over
  queries + notices), uncarded-out, unstaffed.
- `wi_bdf9a537` — gateway behind tailscale serve (localhost bind, tailnet
  front, identity headers; kin to security critical wi_9970877d).
- Substrate findings awaiting owners: `wi_89087a49` (decision requests
  vanish at the ruling seam), `wi_c05fdbe6` (card-per-recurrence burn).

## Standing rules that bound this queue

- Gibson runs RELEASE CUTS only — tagged, published, hash-verified (Mike, 2026-08-20).
  A release that cannot serve is a defective release: raise the re-cut question at
  discovery, never work one box around it.
- Specs are durable only in this repo (served guidance "Where specs live", 2026-08-21).
  Workdirs are scratch; artifact rows are pointers, not custody.
- Election boundary is actionable-only: open and iceboxed items may be entries;
  closed and failed items are evidence (Mike, 2026-08-20).
- Election recommends membership. It moves no custody, changes no assignment,
  overrides no release target, and does not guarantee an item ships.
