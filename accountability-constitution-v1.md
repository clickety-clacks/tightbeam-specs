# Accountability constitution & session lifecycle — v1

Status: **RATIFIED DIRECTION** (Flynn rulings, 2026-07-22, from the first in-substrate org
test). This spec is the canonical home of these decisions. Sections marked UNBUILT are
design-complete but unscheduled; implementation lanes deepen them to mechanism grade (and
take adversarial review) when cut. Where this spec assigns a seam to an existing mechanism
spec, that spec governs the mechanism's internals.

## 1. Constitutional guarantees (substrate — kungfu cannot waive these)

1. **Attribution**: every act names WHO (principal) — shipped.
2. **Obligation**: every MUTATION names under what obligation — the assignment-as-capability
   rail (§6). Read/query is free; mutation requires an open assignment.
3. **Patrol**: every open assignment is supervised (prods on silent holders) — shipped
   (attest-hygiene sweep), completed by §5.
4. **Living escalation**: escalation always reaches a living authority — climb the spawner
   chain past dead links; the ORG OWNER (user) is the root and final backstop (§5).
5. **Delivery mechanics** (wakes, mailboxes, chain-walk) are substrate; they carry no policy.
6. **Total emission**: everything that HAPPENS in tightbeam emits an event toward the
   client — verb effects, attest edges, assignment/work-state transitions, spawns,
   retires, wakes fired, denials, turn lifecycle, context resets. The substrate never
   curates; the client may ignore, filter, or organize the stream, but it is TOLD
   everything. Presentation is the client's; omission is not an option the substrate has.

Above the constitution, ORG LAW (kungfu statutes) owns: who may bind whom (§4), review
policy, thresholds, topology. Binding POLICY is law; binding EXISTENCE is physics.

## 2. Work model

- **Work-item = intent.** The durable thread for one user-meaningful piece of work. No
  state, no holder, not patrolled. Optional spec reference (name + sha256) is the body for
  anything larger than an assignment subject.
- **Assignment = obligation AND capability.** Opened per relationship link; holder, opener,
  subject (≤2000 chars), work-item reference.
- **One work-item, many assignments.** Work flows down BY REFERENCE; each link in the tree
  gets its own card with a decomposed subject. Sub-agents never receive the same card and
  never mint new work-items for pieces of an existing one; genuinely new discovered scope
  is raised to the work-item's owner as a proposal.
- **No intent in limbo — the lifecycle brackets (UNBUILT; scheduled as the
  work-item-brackets lane).** Work-items gain `owner` (default: creator) and an
  `icebox` mark. Filing is inseparable from arming the brackets; both reuse existing
  machinery, no new fact kinds:
  - **Bracket 1, routed-or-deadline (rot-at-start):** the work-item-create transaction
    arms a plain TIMED wake targeting the owner (fallback of absence: "route it or
    icebox it"), dueAt = triage deadline (`config :tightbeam,
    :work_item_triage_deadline_ms` / `TIGHTBEAM_WORK_ITEM_TRIAGE_DEADLINE_MS`,
    default 24h), its wakeId stored on the item (`routingWakeId`, the parkWakeId
    pattern). The FIRST assign-txn referencing the item — or the icebox verb — cancels
    it in the same transaction. Healthy path: total silence.
  - **Bracket 2, concluded-or-adjudicated (rot-at-end):** no subscription needed — the
    assignment-CLOSE transaction (completion/surrender/revoke/interruption) checks the
    item's remaining-open count; on last-close of a non-closed item it delivers a
    post-commit owner wake ("slate clear on wi_X: close it, card more work, or rule it
    failed") — the escalation owner-delivery pattern. Re-arms on each later
    assign/close cycle.
  - Both wakes ride the ordinary lattice: an ignored owner is prodded, an ignored prod
    escalates, the org owner roots the chain. Further conditions (verdict-failure
    alerts, staleness) are ORG LAW, not defaults — silent when healthy.
- **The expecter opens the card.** Dispatch = assign FIRST, wake SECOND (wake carries the
  assignment id, one-sentence brief; the rows are the brief). A worker carding itself
  records effort, not the expecter's expectation. There is deliberately NO rail detecting
  a forgotten card (an unrecorded expectation leaves no evidence; thresholds rejected):
  the gap closes by construction — see `dispatch` verb.
- **`dispatch` verb (UNBUILT)**: atomic assign + wake in one transaction; the correct
  dispatch becomes the single easiest action.
- **Spawn needs no work-item** (pools of pre-spawned agents are legitimate; existence needs
  no ticket). `spawn --subject/--work-item` remains the atomic spawn-and-card affordance.
- **Top of chain**: the product owner self-assigns every work item agreed with the user —
  no invisible work at the top; the PO is an ordinary holder under the patrol.

## 3. Session lifecycle

- **Sessions are disposable projections; rows are the truth.** Homes reproject; harness
  working memory is the only unrecoverable layer, and its loss is always disclosed
  (tombstones).
- **Retire cascades by default (UNBUILT).** A hire's output has one consumer — its
  spawner; orphaned subtrees are unconsumable effort. Cascade is LOUD: the result names
  every session taken down; each cascaded open assignment gets a terminal interruption row
  (work-item history stays resumable). Keeping a subtree = reassign those hires BEFORE
  retiring the parent (deliberate; no quiet reparenting).
- **Critical-section lease (UNBUILT).** Mutations belong in the session's workdir; shared
  mutations (main commits, identity repo, gateway restart) are ceremonies. A session doing
  one declares `critical --for <t> --reason <r>` (hard cap, bounded renewal, no
  immortality). Retire/cascade on an unexpired lease DEFERS, never skips: target gets the
  retire-intent as its final instruction with the hard deadline (a scheduled wake);
  retirer is told the deferral. Rails may later REQUIRE a lease for named ceremonies.
- **Retire reaps the harness process (UNBUILT, bug):** today retirement leaves the
  session's harness subprocess resident; retire must end it via the adapter.
- **Retire emits a wire removal event (UNBUILT, bug):** clients currently learn of
  removals only at reconnect.
- **Slates, not tickets:** an orchestrator (any hire) may carry a SET of work items for
  its one owner. Slate-clear is a deliberate fork — hand it more work or retire it; the
  substrate never auto-retires. Idle-with-empty-books is visible and cheap; the crime was
  only ever the unbooked expectation.

## 4. Binding policy as law

- Substrate exposes neutral **relationship facts** as rail predicates: spawner-of,
  same-spawner-chain, owner, archetype, role.
- The DEFAULT bundle ships the chain-of-command statute: a session accepts assignments
  only from its spawner chain or the org owner/admin. Orgs may replace/scope it (shared
  specialist pools; borrowing within a product family). Named agent-groups become an
  org-config fact when a second real topology needs them.
- Conversation wakes are always open (colleague etiquette): strangers talk; law decides
  who binds.
- **Orchestrator exclusivity (default law):** orchestrators are per-owner instruments;
  dispatching to an orchestrator you did not spawn is forbidden — context pollution +
  a lifecycle you do not control. Statute candidate: refuse assignments from outside the
  spawner chain (this is the default statute, above).

## 5. Supervision completions (UNBUILT)

- **Strand notification:** the P6 sweep classifies retired-holder assignments as
  :stranded (mechanism spec); this spec adds WHO IS TOLD — a strand files a fact and
  notifies the first LIVING ancestor up the spawner chain; org owner at the root (via the
  wake-to-user path → client push).
- **The strand condition is a row, not a judgment (Flynn-ruled 2026-07-24, adjudication
  #3):** notification fires iff the retired holder has OPEN ASSIGNMENT rows. A retired
  session with no open assignment was doing nothing anyone is owed — work that is not a
  row does not exist — so routine retirement stays silent (doorbell/stamp only, per
  supervision). This resolves the apparent conflict with supervision's
  "waking is operator judgment": no judgment was ever needed, the assignment row IS the
  condition. Delivery is one addressed notice through the existing owner-delivery seam
  (comms-clock; delivered once; resumes nothing) — no new mechanism.
- **Empty-chain escalation:** the same living-authority rule applies wherever an
  escalation chain is empty (user-created sessions) or dead.
- **Prods for retired holders are skipped, never counted** — dead workers cannot miss
  pokes; strand handling replaces the prod path for them.

## 6. Assignment-as-capability (substrate rail — §1.2; UNBUILT)

- MUTATING tool calls require the caller to hold an open assignment: file writes,
  state-changing shell, tightbeam effect verbs. Read/query tools are free.
- Enforcement points already exist or are in flight: C1 harness hooks (commands), P4-P6
  dispatch layer (verbs). The check is one predicate over the assignments table.
- Self-carding is legal: the guarantee is no INVISIBLE work, not no autonomous work — a
  self-opened card is patrolled, attributed, readable, revocable.
- Admin/user axis exempt as always.
- v2: every tool call tagged with the assignment it serves → full provenance chain
  (mutation → obligation → work item → user agreement).

## 7. Legibility (cluster; partially filed earlier) — implements guarantee §1.6

Two implementation stages of total emission, both tracked on the roadmap:
- **Interim (near-term micro-lane):** work-lifecycle tombstones — attest edges and
  assignment transitions write compact marker rows into the actor's transcript through
  the existing messages projection (the same path [context reset]/[turn failed] already
  use). Zero wire/client changes.
- **Endgame:** the typed, seq-ordered event stream (one interleaved stream, kind tags,
  subscription-side filtering, row-backed kinds replayable) — the wire-full-stream
  emission item, with awaiting-user-input as a first-class attention state rendered from
  open decision-requests.

- Markers carry CAUSE + PRINCIPAL: context-reset tombstones (guidance fingerprint change
  vs failed resume; who restarted/amended), turn failures (what interrupted; which
  ceiling), stalls (credential health), denials (rule + SHA). One doctrine: the substrate
  knew at write time; the human never digs.
- Timeout-as-check-in: on ceiling, mark honestly AND schedule the continuation nudge.
- **Org-health view (UNBUILT):** busy-but-bookless sessions listed, ranked, threshold-free
  — observability without enforcement; judgment stays with the PO/owner.
- Session naming (manual law, shipped): display "<Role> — <specific purpose>", role
  `function:work-slug`; the substrate records provenance, the name carries purpose.
- Wire provenance (UNBUILT): `origin`/`spawnedBy` join the client session payload as
  OPTIONAL fields — absent means user-visible (openclaw compatibility: fail-open to
  visible, never required keys).

## 8. Non-goals (v1)

- No auto-retire on slate-clear; no reparenting flag; no unbooked-work detector; no
  provider-HTML proxying in credential flows; no work-item states (threads stay stateless;
  deployment state is a separate future decision).

## Provenance

Ratified in conversation 2026-07-21/22 during the first in-substrate org test (three
incidents: silent strand via borrowed-orchestrator retirement; unbooked expectation at
two chain links including the operator's own dispatch; retired-session process/drawer
ghosts). Decisions ledger carries the narrative; the roadmap tracks scheduling. Guidance
already shipped: dispatching skill (expecter-opens-card, pointer briefs, threading,
retire duty, bottom-up sweep), product-owner archetype (self-assignment, orchestrator
exclusivity, slates), orchestrator archetype (no source editing), operating manual
(naming). Where those texts and this spec could disagree, this spec governs.
