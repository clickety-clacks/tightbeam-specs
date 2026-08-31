# Standalone Toplines Concerns and Multi-Membership Follow-On Candidate

Status: targetless, unbound follow-on candidate. This file has no work item,
Target line, assignment, implementation authority, integration authority, or
release authority.

Provenance:

- `standalone-toplines-v5.md` at specs commit
  `3c83d382968f242ebab660f9b67593aa80a1e84e`, SHA-256
  `1ffc9ee7b984df672b21d46d7a6f3cd3a40b274bd4cec8943377ca47c17881d6`,
  specified Concerns, Concern references, multiple active Topline memberships,
  membership episodes, and their race, relink, corruption, and lifecycle
  criteria.
- Mike's 2026-08-31 MVP ruling, recorded on owner assignment
  `asg_898f7d2d-6d49-4490-833e-53f468fbd015` in
  `att_56ce96c0-554e-448e-abe7-ccad46c76290`, removed that scope from the MVP.
- Reviewed Lane 2 candidates main
  `5adc6f03e0469aa399b14a312985f92ea5036107` and `0.1.9`
  `9c45e34af46aba451ac84ea5795a50a4a16fdafd` contain implementation
  provenance. Review `att_75de3a99-6aca-4f6b-84b9-aa4d43847e62` and report
  `art_32e37248` apply to those exact bytes, not to this candidate.

## Goal

G1. Preserve the removed design as one named candidate that a later product
decision can accept, narrow, or delete.

G2. If authorized later, let one work item belong to more than one Topline
through explicit attributable membership episodes.

G3. If authorized later, let a Topline contain durable Concerns and explicit
references from a Concern to work membership.

## Non-Goals

NG1. This candidate does not change the Standalone Toplines MVP.

NG2. This candidate does not bind a work item or select a product target.

NG3. This candidate does not authorize implementation, migration, integration,
release, or deployment.

NG4. A Concern does not create, end, or imply Topline membership.

NG5. Tightbeam does not infer a Concern, membership, or reference.

## Terms

**Work membership.** One active or ended episode between one Topline and one
work item. Its identifier starts with `tlm_`. Link and unlink actors, reasons,
and times make the episode attributable.

**Multi-membership.** A work item has active Work memberships in two or more
Toplines owned by the same user.

**Concern.** A durable issue or question owned by one Topline. Its identifier
starts with `tlc_`. Its state is `open` or `resolved`.

**Concern reference.** One active or ended attributable episode that associates
a Concern with a Work membership in the same Topline. Its identifier starts
with `tlcr_`.

**MVP direct link.** The `topline_work_links` row keyed by `workItemId` in the
Standalone Toplines MVP. It has no membership identifier or ended episode.

## Assumptions

A1. The Standalone Toplines MVP receives independent review before any product
owner considers this candidate.

A2. A later product decision can supply user evidence that one-link intent is
insufficient.

A3. A later design can migrate from MVP direct links without losing actor,
reason, or time.

A4. The removed 3c83 contract and reviewed Lane 2 bytes remain available as
provenance, not authority.

## Invariants

I1. A Work membership joins objects with the same owner.

I2. One `(toplineId, workItemId)` pair has at most one active Work membership.

I3. An unlink ends the named membership episode. It does not address only the
pair.

I4. A later relink creates a new membership ID.

I5. A Concern belongs to one Topline.

I6. A Concern reference names a Concern and Work membership in that same
Topline.

I7. A Concern reference changes no membership state.

I8. Link, unlink, Concern, and reference mutations carry actor, reason where
applicable, time, event, and idempotency evidence.

I9. Foreign and unknown identifiers remain indistinguishable to a non-admin.

I10. A migration from MVP direct links preserves the original link actor,
reason, and time.

## Architecture

This candidate preserves three possible additions from the superseded 3c83
contract:

1. Replace `topline_work_links` with `topline_work_memberships`, including a
   `tlm_` identifier and complete link/unlink tuples.
2. Add `topline_concerns` with create, update, resolve, and reopen operations.
3. Add `topline_concern_refs` with explicit link and unlink operations against
   a Work membership in the same Topline.

The prior operation names are preserved as provenance:

- `topline-concern-create`
- `topline-concern-update`
- `topline-concern-resolve`
- `topline-concern-reopen`
- `topline-concern-link-work`
- `topline-concern-unlink-work`

The prior response concepts are also preserved: `membershipId`,
`openConcernCount`, `concerns`, Concern-reference IDs, and ended episode
history. A future bound specification must restate exact fields, orders,
refusal bytes, schema constraints, migrations, compatibility, placement
interaction, REST/Firehose boundaries, and acceptance. This candidate does not
make those omitted details build authority.

Subtraction ruling: the MVP deleted these surfaces because one durable ask,
one optional link per work item, intent reads, and placement work without them.
Accepting their absence is cheaper than adding entity, migration, API, race,
privacy, and corruption machinery before user need exists. This candidate
exists only to prevent later rediscovery from losing provenance.

## Acceptance

AC1. Given this file at an exact specs commit, when an orchestrator inspects the
Standalone Toplines MVP work item, then it finds no binding or spec reference
to this file.

AC2. Given no later user evidence and owner ruling, when a builder reads this
candidate, then the builder starts no product assignment and changes no product
byte.

AC3. Given a later owner authorizes Multi-membership, when the future spec is
complete, then it defines an exact migration from one MVP direct link to one
active membership episode without changing actor, reason, time, Topline, work
item, or owner.

AC4. Given a later owner authorizes Concerns, when the future spec is complete,
then each Concern and reference operation has an exact actor, state, schema,
wire shape, refusal map, authorization rule, event, idempotency fingerprint,
and Given/When/Then test.

AC5. Given a future implementation permits two active memberships for one work
item, when a direct SQL fixture inserts a duplicate active pair, then the
database rejects that pair while permitting memberships in two different
Toplines.

AC6. Given a Concern in Topline A and a membership in Topline B, when a caller
or direct SQL fixture creates their reference, then the public seam returns a
same-Topline refusal and the database rejects the cross-Topline row.

## Open Questions

OQ1 — BLOCKING. What observed user task requires one work item to appear in two
Toplines at the same time?

OQ2 — BLOCKING. What observed user task requires a Concern entity instead of
text in the Topline ask or a linked work item?

OQ3 — BLOCKING. Should a future migration replace the MVP direct-link table or
add membership storage beside it? The answer must leave one mutation seam.

OQ4 — BLOCKING. Which product lines and previous-package fixtures would carry
the migration?

OQ5 — NON-BLOCKING. Should a future product retain the six provenance command
names? A later bound spec can rename them before implementation.
