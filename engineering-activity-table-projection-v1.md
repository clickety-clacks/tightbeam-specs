# Engineering activity-table projection — v1

Status: **PROPOSAL for independent spec review.** Implementation target is unset.

This spec amends only the delivery claim in `agentic-engineering-guidance-spec.md` §1:
the bundle-root `preferred-models.md` activity table is operator-facing material today,
not guidance that an engineering session receives on election. The table remains the
single textual authority. This amendment requires its derived projection into the
sessions already directed to use it.

## Goal

Make the existing agentic-engineering activity table readable in the compiled guidance
of each elected agentic-engineering archetype. A model-selecting agent must receive the
ordered candidates and quality floor that `product-owner.md`, `feature-cycle`, and the
shared table-reading rule already direct it to apply.

The change projects existing policy. It does not choose policy.

## Non-Goals

- Do not add, remove, reorder, rename, characterize, or re-tier a model, including
  `terra`.
- Do not change an activity's quality floor.
- Do not decide whether an activity row or an archetype's `model_preferences` wins when
  they disagree. Decision request `dr_07a9f9f3-34b5-4081-a508-2dc6f343a6eb`
  tracks that enduring policy independently and does not block this amendment.
- Do not make the substrate select a model, walk a candidate list, retry a turn, or
  judge capability.
- Do not add a command, condition kind, assignment state, hold, or fallback mechanism.
- Do not change model-release intake, catalog-diff behavior, archetype manifests or
  preferences, credentials, provider configuration, or host placement.
- Do not repair unrelated stale prose in `agentic-engineering-guidance-spec.md`.
- Do not activate, deploy, release, relearn, or apply an identity revision as part of
  this specification assignment.

## Terms

- **Engineering activity table**: the Markdown document at
  `kungfu/agentic-engineering/preferred-models.md` in an installed identity revision.
  It names each engineering activity, its ordered candidate models, and its floor. It
  remains the only maintained copy of those rows.
- **Engineering archetype**: an archetype manifest recorded in the installed
  agentic-engineering receipt. At the baseline these are `product-owner`,
  `orchestrator`, `spec-writer`, `coder`, `reviewer`, and `recon`.
- **Installed receipt**: `kungfu/agentic-engineering/installed.toml`, whose `paths`
  identify the files installed by that bundle.
- **Compiled guidance**: the immutable guidance bytes that an identity snapshot serves
  to a session after resolving the archetype's guidance fragments.
- **Projection**: derived compiled-guidance bytes sourced from the engineering activity
  table. A projection is not another editable textual home.
- **Activity row**: one table row for the work being staffed.
- **Archetype preference**: one ordered `model_preferences` entry in an archetype
  manifest, projected by `tightbeam list` and session status.

## Assumptions

- The shipped 0.1.8 bundle and canonical Tightbeam source at
  `3fe0e941840ed138a6a285261c0e35687d8d27a3` store the engineering activity table at
  the bundle root.
- `lib/tightbeam/archetypes.ex` builds its fragment library from the operating manual
  and identity `guidance/*.md` files. It does not scan bundle-local documents.
- `lib/tightbeam/identity.ex` stores bundle-local documents and exposes selected public
  documents, but `revision_fragments!/2` reads only identity `guidance/*.md` files.
- Each shipped engineering archetype includes the guidance fragment named
  `preferred-models.md`. That fragment contains the substrate working set, the
  table-reading rule, and substrate activities. It does not contain the engineering
  activity table.
- The installed receipt records the six engineering archetype manifest paths and the
  bundle-root activity-table path.
- `model_preferences` is declared, validated, and projected. The substrate does not
  apply that preference list as a model-selection mechanism.
- New sessions read the live identity revision. Existing sessions keep their served
  revision until an explicit identity apply refreshes them.

## Invariants

### INV-01 — One textual home

The bundle-root engineering activity table is the only maintained copy of its rows.
Compiled guidance derives its projection from those exact revision-pinned bytes.

### INV-02 — Policy preservation

Projection changes no table content, candidate order, effort, model identity, activity
classification, or floor.

### INV-03 — Inference owns selection

The substrate exposes the table. An agent selects a candidate. Projection performs no
availability check, qualification judgment, retry, substitution, or block decision.

### INV-04 — Bundle scope

Only archetypes recorded in the installed agentic-engineering receipt receive this
table. Neutral and unrelated archetypes do not receive it.

### INV-05 — Revision binding

One identity snapshot uses the activity-table bytes from the same identity revision as
the archetype manifest and guidance fragments. It cannot mix revisions.

### INV-06 — No activation by specification

Landing or reviewing this spec changes no live identity or session. Activation remains
an explicit later product action after reviewed implementation.

## Architecture

### ARC-01 — Derived delivery

When Tightbeam compiles guidance for an engineering archetype, it includes the exact
engineering activity-table document from the same installed identity revision. The
document appears once in the compiled guidance.

The implementation may choose the projection seam. It must preserve INV-01 through
INV-05 and must not require an agent to discover an installation path or run an
undocumented command.

### ARC-02 — Membership source

The projection uses the installed receipt to decide whether an archetype belongs to
agentic-engineering. It does not infer membership from an archetype name, role binding,
session lineage, or current assignment.

### ARC-03 — Identity lifecycle

A newly provisioned or explicitly refreshed engineering session receives the projection
from its served identity revision. A session that has not been refreshed keeps its prior
compiled guidance. Unlearning the bundle removes the projection together with the
bundle-owned archetypes and documents.

### ARC-04 — No guidance restatement

The implementation does not copy the engineering rows into
`guidance/preferred-models.md`, an archetype kernel, a skill, or a second bundle
document. Role kernels and skills may continue to point to the activity table without
restating its candidates.

### ARC-05 — Subtraction ruling

ADD wins only as a derived projection: deleting the table removes a required public
intake record, while accepting the failure leaves existing staffing directives without
their required policy bytes. A second maintained table loses because it creates drift.

### ARC-06 — Operating pattern

This feature teaches no new operating-manual pattern. It makes an existing elected
policy readable at the point where agents already apply it.

## Acceptance

### AC-01 — Each engineering archetype receives one exact projection

Given an identity revision with agentic-engineering installed, when Tightbeam snapshots
each of the six receipt-recorded engineering archetypes, then each compiled guidance
contains the exact bytes of that revision's
`kungfu/agentic-engineering/preferred-models.md` once.

### AC-02 — Unrelated archetypes receive none

Given the same identity revision and a neutral archetype not recorded in the installed
receipt, when Tightbeam snapshots that archetype, then its compiled guidance contains no
engineering activity-table projection.

### AC-03 — One source change yields one projected change

Given two identity revisions that differ only by one byte in the engineering activity
table, when Tightbeam snapshots the same engineering archetype at each revision, then
the first snapshot contains only the first table bytes and the second snapshot contains
only the second table bytes. No editable guidance copy requires a matching change.

### AC-04 — Revision consistency

Given revision A and revision B with different table bytes and archetype manifests,
when a snapshot is pinned to revision A, then it contains revision A's manifest-derived
guidance and revision A's table. It contains no table bytes from revision B. The inverse
holds for a revision-B snapshot.

### AC-05 — Session refresh boundary

Given an existing engineering session served at revision A and a live identity revision
B with changed table bytes, when no identity apply targets that session, then the session
keeps revision A. When an explicit apply refreshes it to revision B, then its served
guidance contains revision B's exact table bytes once.

### AC-06 — Policy and manifest bytes remain unchanged

Given the implementation diff, when a reviewer compares the bundle-root activity table
and the six engineering archetype manifests before and after, then those seven files are
byte-identical. The table's candidate models, order, efforts, activity labels, and floors
remain unchanged. The diff introduces no second maintained copy of those rows.

### AC-07 — No selection mechanism appears

Given the implementation diff and focused tests, when a reviewer searches the new path,
then it performs only identity membership, revision, and guidance composition work. It
contains no catalog query, credential probe, model ranking, candidate iteration, spawn,
tune, turn retry, work-blocked assertion, wake scheduling, or assignment mutation.

### AC-08 — Real identity smoke

Given a disposable identity created from the implementation revision, when it learns
agentic-engineering and provisions one engineering session plus one neutral session,
then the engineering session's actual served prompt contains the exact activity table
once and the neutral session's prompt does not contain it. The fixture records the
source table hash, served-prompt hash, identity revision, archetype, and observed count.

## Recorded Separate Findings

These findings require separate authority. They add no requirement or acceptance check
to this amendment.

### FIND-01 — Catalog-diff contract mismatch

The `model-release-intake` skill says uncharacterized live models make
`mix tightbeam.catalog.diff` exit nonzero. Current source and tests report new arrivals
as informational and return success when no characterized model vanished.

### FIND-02 — Intake ceremony has no election

No shipped engineering archetype elects `model-release-intake`. Selecting its detecting
kernel and owning archetype requires separate guidance-placement work.

## Open Questions

None. The independently tracked precedence policy and FIND-01/FIND-02 are outside this
amendment and do not create holes in its visibility requirements.
