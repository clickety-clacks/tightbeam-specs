# Existing-session re-parent MVP

Status: proposed for one independent cross-harness review  
Work item: `wi_a78f6a03-cb0b-4b75-9c89-d13507d55a5d`  
Writer assignment: `asg_1aa2ce01-425e-42bf-9b26-57ba77ce7775`  
Research base: direct `origin/0.1.x` at `dd1b77f27dbd4fe642ec491eb04a4ce57cd6359b`  
Scope ruling: relief product owner response to `w_68437173`; preserve existing Toplines and role-fallback meanings.

## Goal

Add one `session-reparent` operation. An owner acting as a user can use it to set the current parent of one active custom session. The same transaction sets the current coordination parent of that session's one direct open assignment.

The operation does not require a turn, wake, or acknowledgment from the new parent. It preserves the session, assignment, work item, attests, artifacts, transcript, queued work, and running turn.

Flynn's first use is:

```text
tightbeam session-reparent \
  --session 'agent:main:clawline:mike:main s_e15f8ee6' \
  --parent 'agent:main:clawline:mike:main' \
  --assignment asg_ac32b22c-babe-4f16-bbdb-b502a3af9ff7 \
  --key lachesis-under-main-1 \
  --as-user mike
```

## Non-Goals

- The MVP does not change a session's `origin` or `spawnedBy` creation facts.
- The MVP does not change an assignment's `openedByUser`, `openedBySession`, holder, state, work-item link, or review link.
- The MVP does not change a work item's creator or creation-turn context.
- The MVP does not change Toplines causal nesting or role fallback rules.
- The MVP does not detach a session, bulk-move sessions, or edit an arbitrary graph.
- The MVP does not retune a live session's harness, provider, model, effort, context, or host.
- The MVP does not retire, respawn, pause, restart, wake, or message a session.
- The MVP does not correct closed work or sessions with multiple direct open assignments.

## Terms

- **Origin parent:** The immutable `sessions.spawnedBy` value recorded at session creation.
- **Current parent:** The session that current lineage routing uses. It is the latest successful correction parent, or the origin parent when no correction exists.
- **Origin opener:** The immutable `assignments.openedByUser` or `assignments.openedBySession` principal.
- **Current coordination parent:** The session that current work-coordination reads show for the corrected open assignment. It is the latest successful correction parent, or absent when no correction exists. The origin opener remains a separate historical field.
- **Correction event:** One append-only row that records both current-topology changes, their prior values, the user principal, cause, request fingerprint, and commit time.
- **True lineage consumer:** Product code that walks session parentage to authorize, route, escalate, supervise, notify, or retire.

## Assumptions

- Direct `origin/0.1.x` at the research base stores session creation parentage only in `sessions.spawnedBy`.
- The live Lachesis session is active, custom, owned by `mike`, and has `spawnedBy = NULL`.
- The live Lachesis assignment is open, is held by that session, and directly names the open Lachesis work item.
- The current database transaction seam serializes the validation and write set.
- `toplines --tree` derives causal work-item edges from immutable creation-turn evidence. It does not consume `sessions.spawnedBy`.
- Role fallback resolves an absent or retired role binding to the owner's Main. It does not consume `sessions.spawnedBy`.

## Invariants

1. The gateway keeps origin parent, origin opener, and work-item creation context byte-identical after a correction.
2. The gateway commits one correction event and one idempotency result in one database transaction.
3. The gateway derives both corrected values from the same correction event.
4. The gateway accepts the operation only from a user who owns the child session, parent session, assignment holder, and work item.
5. The gateway keeps the current session-parent relation acyclic.
6. Each true lineage consumer reads parentage through one current-parent resolver.
7. The gateway returns only after the correction event and idempotency result commit.
8. The operation leaves existing runtime and work rows unchanged.
9. Each successful correction leaves a durable event that names the cause and user principal.

## Architecture

### Public contract

The CLI adds this command:

```text
session-reparent --session <childSessionKey> --parent <parentSessionKey>
                 --assignment <assignmentId> --key <idempotencyKey>
```

The gateway verb is `session-reparent`. The four parameters are required. The caller must use a user principal, such as `--as-user mike`. A session principal and a process principal receive `user_principal_required`.

On success, the response contains:

```json
{
  "eventId": "trp_...",
  "session": {
    "sessionKey": "...",
    "originParent": null,
    "previousCurrentParent": null,
    "currentParent": "..."
  },
  "assignment": {
    "assignmentId": "asg_...",
    "workItemId": "wi_...",
    "originOpenerRef": "user:mike",
    "previousCurrentCoordinationParentRef": null,
    "currentCoordinationParentRef": "session:..."
  },
  "appliedAt": 0
}
```

The response exposes both origin and current values. It does not relabel an origin field as current topology.

### Validation

The gateway validates these facts again inside the write transaction:

1. The idempotency key is non-blank text of at most 200 characters.
2. The child session exists, is active, is custom, and belongs to the caller.
3. The parent session exists, is active, differs from the child, and belongs to the caller.
4. The assignment exists, is open, is held by the child, and directly names an open work item owned by the caller.
5. The assignment is the child's only direct open assignment.
6. Following current parents from the proposed parent does not reach the child.
7. At least one existing current parent or current coordination parent differs from the requested state.

A validation refusal writes no correction event and no idempotency result.

### Durable model

Add one append-only `session_reparent_events` relation. Each row contains:

- `eventSeq`, a monotonic integer primary key;
- `eventId`, a unique public identifier;
- `ownerUserId`;
- `childSessionKey`;
- `assignmentId` and `workItemId`;
- `originParentSessionKey`;
- `previousCurrentParentSessionKey`;
- `newCurrentParentSessionKey`;
- `originAssignmentOpenerKind` and `originAssignmentOpenerRef`;
- `previousCurrentCoordinationParentSessionKey`;
- `newCurrentCoordinationParentSessionKey`;
- `cause = owner_topology_correction`;
- `principalKind = user` and `principalRef`;
- `idempotencyKey`, request fingerprint, and `createdAt`.

The current-parent resolver selects the committed event with the greatest `eventSeq` for a child. It falls back to `sessions.spawnedBy` when no event exists. The current-coordination-parent resolver selects the committed event with the greatest `eventSeq` for an assignment. It returns no current coordination parent when no event exists. The immutable assignment opener remains available only as origin history.

The existing idempotency seam stores operation `session-reparent`, owner, key, request fingerprint, event ID, and canonical response in the same transaction. A retry with the same key and fingerprint returns the canonical response. Reuse of that key with another fingerprint returns `idempotency_conflict`.

The append-only event is the audit record and the current override. Database triggers reject update and delete operations on this relation. The MVP does not add a mutable parent column or rewrite an origin row.

### Read and routing integration

`Org.current_parent` becomes the only session-parent read for true lineage behavior. Direct `spawnedBy` walks in authorization, artifact ancestry, effort escalation, supervision, bubble routing, and retirement subtree traversal must use it. New routing after the commit follows the corrected parent. A wake or turn that already names a target keeps its recorded target.

Read surfaces expose the distinction:

- Session list entries keep `spawnedBy` and add `currentParent`.
- Work-item trace assignment entries keep `openerRef` and add `currentCoordinationParentRef`.
- `toplines --tree` keeps its causal `parent` block and nesting. Each work-item node adds `currentCoordination`, a deterministic list of its open assignments with `assignmentId`, `holderKey`, and `currentCoordinationParentRef`.
- Role entries keep `boundSessionKey` and `fallbackTarget`. A bound role adds `boundSessionCurrentParent`. Role resolution still falls back directly to the owner's Main.
- The correction event appears in the affected work-item trace timeline with its event ID, principal, cause, previous values, and new values.

The operation does not enqueue a turn on the child or parent. It does not alter a session lane, a harness pointer, a pending wake, or a claimed turn.

### Traceability

| Requirement | Implementation seam | Acceptance |
|---|---|---|
| Owner can correct the live pair without parent action | CLI, gateway authorization, one transaction | A1, A2 |
| Origin stays truthful | Append-only correction event and origin/current response fields | A1, A3 |
| Current routing is consistent | `Org.current_parent` and current-coordination-parent resolver | A3, A4 |
| Cycles are rejected | Transactional ancestry validation | A5 |
| Retries are safe | Existing idempotency seam plus fingerprint | A6 |
| Partial correction cannot commit | One database transaction | A7 |
| Live work continues | No runtime or work-row mutation | A8 |

This spec teaches no new agent operating pattern. It adds an owner maintenance command and truthful read fields.

## Acceptance

### A1 — Flynn's correction succeeds

Given the live Lachesis child has origin parent `NULL`, one direct open assignment, and immutable origin opener `user:mike`, when `mike` runs the example command, then the gateway commits one correction event. The event sets both current values to Main. The origin parent and origin opener remain unchanged.

### A2 — The new parent does not act

Given Main has no runnable credential and takes no turn during A1, when the command commits, then Main's turn count, wake rows, session lane, and harness pointers remain unchanged. The command still succeeds.

### A3 — Each read tells origin from current topology

Given A1 committed, when `mike` reads the session list, work-item trace, Toplines tree, and role list, then each surface reports the corrected current value. The session list still reports `spawnedBy = null`. The work trace still reports `openerRef = user:mike`. The Toplines causal `parent` block and nesting remain unchanged. The role binding and fallback target remain unchanged.

### A4 — New lineage work uses the correction

Given A1 committed, when a later authorization, escalation, bubble, supervision action, artifact ancestry check, or retirement traversal resolves the Lachesis parent, then that consumer resolves Main through `Org.current_parent`. A pending row that already names a target keeps that target.

### A5 — Unsafe topology is refused

Given the proposed parent is the child or a current descendant of the child, when the owner calls `session-reparent`, then the gateway returns `cycle_detected`. The database contains no new correction event or idempotency result.

### A6 — Authorization and retry behavior are deterministic

Given a caller who does not own one required row, when that caller invokes the verb, then the gateway returns `not_authorized` and writes nothing. Given a successful request, when the owner repeats its key and fingerprint, then the gateway returns the byte-equivalent canonical response and keeps one event. Given the same key with a different fingerprint, the gateway returns `idempotency_conflict` and keeps one event.

### A7 — The pair commits atomically

Given fault injection before either durable write or before commit, when the operation fails, then neither the correction event nor the idempotency result exists. Given commit succeeds, both records exist and name the same event ID.

### A8 — Live work remains live

Given the child has a running turn, durable transcript, attests, artifacts, pending wakes, and the open assignment, when A1 commits, then those rows and the assignment holder remain unchanged. The running turn can finish under the same session key.

## Open Questions

None. The relief product owner ruled that the MVP preserves existing Toplines causal-tree and role-fallback semantics. It adds truthful current-topology fields and changes only true lineage consumers.
