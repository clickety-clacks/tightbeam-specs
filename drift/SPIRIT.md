# Drift

## Ownership and authority

Product owner: `product-owner:drift`, session `s_5c87a5e7`.
Outcome: `wi_9069f091-53a7-41ff-8b7b-a7d07c188bde`.
Owner assignment: `asg_6bcbeb33-5b27-4c5b-bcb1-63ca022890bf`.
Delivery orchestrator: `orchestrator:drift-mvp`, assignment `asg_e0ac4a53-e22b-4027-ba39-16909cef1d91`.

The adjacent MIKE_PRODUCT_BRIEF.md preserves Mike's full brief from art_84429c44.
That brief is authority. This rendering adds no unconfirmed product commitment.

## Spirit

Human and agent share a writing surface and understanding. The human can word-process while their own general-purpose agent helps with its existing context, files, tools, and harness. Drift is an editable writing tool. Both participants can select, point, comment, reply, edit, suggest, and resolve. Each has an identity and independent selection. Agent activity must not steal the human's typing cursor.

Discussion stays attached to meaningful passages and survives disconnects and restarts. Stale edits cannot overwrite newer writing. Ambiguous or deleted anchors must be visible rather than silently attaching to unrelated text.

Drift runs independently without a required vendor cloud or bundled paid AI service. GUI, service, and external agent can run together or separately through configuration. Gibson is Mike's preferred initial service host, not a product constant or installation authorization.

### Outcomes for acceptance

1. A human writes and saves a document, selects a sentence, and leaves a persistent question.
2. An external agent reads that exact passage with context, replies, points to another passage, and suggests an edit.
3. The human can perform the same discussion actions and accept or decline the suggestion without losing typing focus.
4. Nearby edits preserve meaningful anchors; conflicting edits and missing anchors fail visibly and preserve work.
5. Text and questions survive restart; disconnected participants can recover missed durable events.
6. Real demonstrations cover configured same-machine and split client/service locations with appropriate access control.

### Quality stance

Daily writing and protection of work matter: undo, saving/recovery, stale-write safety, and clear authorship are material. Interaction must remain lightweight. Configuration and independent deployment are required. Prefer the quickest useful complete writing loop over an office suite. Report actual runtime evidence and limitations; a socket connection alone does not wake an idle harness.

### Non-goals

No embedded model runtime, mandatory MCP foundation, paid AI bundle, or mandatory hosted editor. DOCX compatibility, pagination, full office-suite behavior, public-cloud collaboration, and idle-harness wake injection are not required by the current brief. No automatic release, installation, deployment, or live mutation.

## Open product choices

- Document format is resolved: Mike ruled **Plain text/Markdown first** in dr_d9f53dfc-4e05-49fe-b353-17cdb2f6efb1. The first version edits and saves text/Markdown; rich-text fidelity is outside this slice. The format hold is removed. This does not independently require rendered Markdown preview.
- Exact license remains undecided. Blocks declaring a license or public release under one; does not block private development.
- Delivery installation requires a concrete reviewed candidate and an explicit deployment decision. Not a development gate.

## Product path

The canonical code home is clickety-clacks/drift, recorded by its delivery orchestrator in art_16a2904a; it remains private development custody. Test independent highlights, anchored interaction, and typing focus in the bounded Qt/Quickshell feasibility slice. With plain text/Markdown confirmed, land a lean buildable technical spec under this Spirit and progress work independent of any remaining toolkit or access-control decisions. Implement the smallest complete writing loop, obtain fresh independent review, and return real workflow evidence to the product owner before main. The orchestrator owns engineering choices, staffing, and per-slice posture; the product owner owns product choices and acceptance.
