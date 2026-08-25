# Preferred-owner affinity and assignment birth states

Status: canonical amendment candidate for independent review
Work item: `wi_c4450c8d-cfae-4ee0-9532-df8c24be499b`
Producer assignment: `asg_4f325d11-7e62-4ca0-845e-399e31fb3836`
Supersedes: `art_813cfefc`, SHA-256 `46d38b3bccb8423c1d689ea2045fc709a1f879d3d6d08bc539fe6a0c51fb6179`

## Goal

Represent passive routing affinity separately from active assignment custody.

A work item may name one preferred owner role without creating an obligation, holder,
wake, prod entitlement, or escalation. Each post-activation assignment records exactly one
supervision state in the transaction that creates it. The activation migration assigns a
state to each legacy row before supervision resumes. That state makes the assignment active
for holder effort, scheduled for an exact continuation, blocked on an exact durable
event, or terminal history.

The substrate must use recorded state and state bindings. It must not infer obligation
or waiting from prose, titles, roles, artifacts, session health, or missing activity.

Escalation targeting, staff-loss rerouting, office continuity, and relief must declare
whether each mechanism depends on a role. A mechanism that depends on a role requires an
explicit role binding at its activation seam. A mechanism that does not depend on a role
has no optional role hint at that seam.

## Non-Goals

- The substrate does not prioritize work or choose a holder.
- Preferred-owner affinity does not dispatch, assign, wake, prod, or authorize a role.
- Preferred-owner affinity does not satisfy a required role binding for escalation
  targeting, staff-loss rerouting, office continuity, or relief.
- This feature does not interpret prose or define domain-specific blocker evidence.
- This feature does not decide that a recovery mechanism depends on a role. The canonical
  contract for that mechanism makes that decision.
- This feature does not add a digest, notification, or workflow product.
- This feature does not change model, harness, credential, deployment, or runtime policy.
- This specification does not authorize implementation or migration of live rows.

## Terms

**Preferred owner** is an optional valid role name recorded on a work item. It is routing
affinity only. It is not custody or an obligation.

**Assignment supervision state** is the assignment's total durable liveness projection.
An open assignment stores one mode: `staffing`, `scheduled`, or `blocked`. A closed
assignment projects `terminal` from its existing closing disposition; the feature does not
store a second terminal outcome.

**State binding** is the immutable row written with a `scheduled` or `blocked` mode. It
binds the assignment and generation to the exact wake or typed blocker that makes the mode
true. A blocker may reference a pre-existing decision request, dependency, review, or
evidence row.

**State generation** is a monotonically increasing integer on an assignment. Assignment
creation sets it to 1. Each accepted transition increments it by 1.

**In-org dependency** is a durable row that another Tightbeam actor will produce, such as
an assignment completion, review verdict, artifact, or ruling.

**External boundary** is a system event that Tightbeam cannot observe directly, such as a
provider, device, CI job, or deploy outside its fact stream.

**Operator decision** is an open owner-scoped decision-request row. The request is the one
operator-facing ask for that choice.

**Required role binding** is an explicit registered role name attached to one mechanism
instance because that mechanism cannot target or continue without the role. It is not a
hint, a session choice, or preferred-owner affinity.

**Role dependency declaration** is the value `required` or `none` in the canonical
definition for escalation targeting, staff-loss rerouting, office continuity, or relief.
The substrate validates that declared value. It does not derive the value from prose or
runtime conditions.

## Assumptions

- Work items, assignments, wakes, condition facts, decision requests, attests, terminal
  dispositions, prod entitlements, and authenticated principals already exist.
- Existing assignment authorization and terminal-disposition law remains authoritative.
- A registered role name is a durable address even when no session currently holds it.
- The gateway can write an assignment, its initial state, and any required state binding in one
  transaction.
- The scheduler can start an authenticated holder turn from a bound wake without treating
  the wake text as evidence.
- Patrol-response acknowledgments can bind to assignment and prod identities.

## Invariants

1. A work item has zero or one preferred-owner role.
2. Preferred-owner mutation creates no assignment, holder wake, prod entitlement, or
   escalation.
3. Each assignment created after activation has one supervision state from creation. The
   activation transaction gives each legacy assignment one state before supervision resumes.
4. `scheduled` and `blocked` each have one state binding written in the same transaction as
   the stored mode. `terminal` references the existing closing disposition.
5. Only `staffing` can own an armed prod entitlement.
6. Each prod, patrol check, acknowledgment, and transition binds to an assignment ID and
   state generation.
7. A stale generation cannot change state or deliver an effort prod.
8. Each affinity or state mutation records the authenticated principal, cause, prior
   value, new value, state-binding or closing-row identity, and time.
9. Terminal assignment history is immutable. New work creates a new assignment.
10. Assignment custody may differ from preferred-owner affinity. That difference is a
    projected fact, not a denial condition.
11. An in-org dependency uses a fact subscription. An external boundary uses a timed
    probe. An operator decision uses one decision-request row. The substrate does not
    substitute one wait instrument for another.
12. Each escalation-targeting, staff-loss-rerouting, office-continuity, and relief
    mechanism declares its role dependency as `required` or `none`.
13. A mechanism with `required` role dependency activates only with one explicit valid
    role binding written in the same transaction as that mechanism instance.
14. Preferred-owner affinity, the caller's role, the current holder, prose, and runtime
    vacancy cannot supply or replace a required role binding.
15. A mechanism with `none` role dependency has no optional role-hint field at its
    configuration or activation seam.

## Architecture

### Mechanism choice

This specification adds explicit state because deleting assignment liveness would discard
accountability, while accepting the current ambiguity would preserve false prods against
lawful waiting.

One gateway mutation seam owns assignment creation and supervision transitions. The seam
validates authorization, current generation, state descriptor, state binding, and target
relationship before it writes any effect.

### Preferred-owner affinity

A work item gains nullable `preferredOwnerRole`. The value must name a registered role,
not a session key; the role may be vacant. An affinity event records the work-item ID,
prior role or null, new role or null, principal, required reason, and time. The current
field projects the newest accepted event.

The work-item owner, an authorized owner agent for that principal, or an admin may set or
clear affinity. Naming a role grants that role no authority. Role vacancy, session
retirement, and assignment to a different holder preserve affinity history.

Existing work-item routing deadlines still govern an unstaffed item. Affinity cannot hide
an unrouted work item.

### Required role bindings for recovery mechanisms

The canonical definition for each mechanism in the following set must declare exactly one
role dependency before the gateway can activate an instance:

| Mechanism | Binding point when dependency is `required` |
| --- | --- |
| Escalation targeting | The escalation target definition |
| Staff-loss rerouting | The reroute destination definition |
| Office continuity | The continuity responsibility definition |
| Relief | The relief destination definition |

For `required`, the activation request supplies one registered role name. The gateway
validates the role and writes the role binding with the mechanism instance in one
transaction. Role vacancy does not invalidate the binding; the mechanism's staffing and
waiting law governs a vacant role.

For `none`, the mechanism schema exposes no optional role-hint field. A caller cannot add a
role for possible future use. A later need for role-based behavior first amends that
mechanism's canonical contract to `required` and then supplies the binding.

The gateway does not copy a work item's `preferredOwnerRole` into a required role binding.
It also does not derive the binding from the caller, current assignment holder, title,
brief, attest, artifact, or session state.

When a `required` mechanism lacks its binding, the activation seam returns
`required_role_binding_missing`. The refusal identifies the mechanism kind, mechanism
instance, and missing `roleName`. It writes no mechanism instance or downstream recovery
effect. An invalid or unregistered role returns `required_role_binding_invalid` with the
same no-write rule.

The substrate-automatic open-time stamp proposed by `wi_7f068d0c` is not an optional value
that an agent must remember to set. That stamp remains distinct from this binding. It can
satisfy no required role dependency unless its own reviewed canonical contract defines it
as the exact required binding at the same mechanism seam.

### Assignment creation

The assignment wire request gains one `initialSupervision` tagged union:

```text
{kind: staffing}
{kind: scheduled, wake: {at | condition, fallback, prompt}, cause}
{kind: blocked, blockerKind, blockerRef, expectedPrincipal, reason}
```

New-version callers must supply exactly one member. The gateway refuses a missing member,
multiple members, or an invalid supporting relationship without writing an assignment.

The existing wire version maps an omitted descriptor to an explicit `staffing` record in
the gateway response and audit event. The default is observable; it is not inferred later.
A later specification and release may remove that wire version. This specification does not
use elapsed time or a request threshold to end compatibility.

The create response returns supervision state and generation 1.

### `staffing`

`staffing` means the holder must advance the assignment now. Creation writes one armed prod
entitlement for generation 1. Existing receipt, prod, acknowledgment, and escalation rules
apply only while that generation remains `staffing`.

### `scheduled`

`scheduled` means no holder effort is due until one exact bound wake starts the next holder
turn. The create or transition transaction writes the wake and state together.

The state binding records the new wake ID. The wake kind must match its boundary:

- The holder's own continuation at a chosen time uses a timed self-wake.
- An in-org dependency uses `--when-fact` with an exact kind and optional exact scope. Its
  fallback detects subscription silence; it does not decide an outcome.
- An external boundary uses a timed wake whose prompt names the exact probe and required
  evidence.
- A human choice does not use `scheduled`; it uses `blocked` with an operator-decision row.

For an in-org dependency, the gateway checks the referenced row and creates the condition
subscription in the same transaction. If the dependency is already satisfied, the gateway
creates `staffing` instead. If it is unsatisfied, the subscription starts after the fact
cursor observed by that transaction. A completion concurrent with creation is therefore
either observed as satisfied or delivered through the subscription.

When the scheduler successfully starts an authenticated holder turn for the bound wake, the
gateway atomically changes the assignment to `staffing`, increments the generation, and
arms one fresh entitlement. Cancellation, queue delay, or failed delivery leaves the
assignment `scheduled` and creates no entitlement.

### `blocked`

`blocked` means more effort by the holder cannot produce the required event. The transition
creates one immutable typed blocker row as the state binding. That row records assignment
ID, generation, blocker kind, validated target reference, expected principal or subsystem,
required reason, authenticated ruling principal, cause, and time.

The initial blocker kinds are `operator_decision`, `dependency`, `review`, `capability`,
`infrastructure`, and `external_event`.

An `operator_decision` blocker must reference an open decision request for the same owner.
The blocker row and state transition commit atomically; the decision request may pre-exist.
The decision request remains the only operator-facing ask. The assignment creates no timed
poll and no holder-effort prod while the request remains open.

An in-org `dependency` or `review` may bind a fact subscription to the exact row. An
`external_event` may bind a timed evidence probe. `capability` and `infrastructure` record
the known failing boundary; policy or a supervising mind selects any recheck.

Satisfying, withdrawing, superseding, or invalidating a blocker may wake an authorized
principal. It does not choose the next supervision state. That principal selects
`staffing`, `scheduled`, another `blocked`, or `terminal` through the mutation seam.

### `terminal`

`terminal` means the assignment is immutable history. Existing assignment closure remains
the sole mutation seam: it writes the lawful closing disposition and advances the final
generation in one transaction. The supervision projection then returns `terminal`. The
feature adds no second terminal field, terminal attest, or terminal creation path. Existing
historical import uses the existing closed-assignment import authority.

### State transitions

Each transition compares assignment ID, current state, and current generation. It writes the
new open mode or existing closing disposition, next generation, state binding, and
entitlement cancellation or creation in one transaction.

Allowed nonterminal transitions are:

| From | To | Supporting cause |
| --- | --- | --- |
| `staffing` | `scheduled` | exact bound continuation wake |
| `staffing` | `blocked` | exact typed blocker |
| `staffing` | `terminal` | lawful terminal disposition |
| `scheduled` | `staffing` | successful bound-wake turn start or explicit resume |
| `scheduled` | `blocked` | exact typed blocker |
| `scheduled` | `terminal` | lawful terminal disposition |
| `blocked` | `staffing` | explicit authorized resume |
| `blocked` | `scheduled` | exact bound continuation wake |
| `blocked` | `blocked` | replacement blocker with supersession link |
| `blocked` | `terminal` | lawful terminal disposition |

A stale transition returns the current state and generation and writes no effect.

### Prodder and patrol

The prodder claims an entitlement in the same transaction that verifies the assignment is
open, state is `staffing`, state generation matches, the entitlement is armed and unclaimed,
and existing terminal and acknowledgment guards pass.

If one predicate fails, the scan writes no prod. A claimed prod that loses the generation
race is canceled as superseded before delivery.

Toplines and patrol project preferred owner, assignment holder, supervision state,
generation, state-binding reference, next expected event, responsible principal, and
whether an entitlement is armed. They do not render affinity as staffing or non-`staffing`
state as holder silence.

Acknowledgments bind to assignment ID, prod ID, and state generation. Earlier-generation
acknowledgments remain history and cannot satisfy a later generation.

### Migration

Schema migration adds preferred-owner affinity and history, open-assignment supervision mode,
state generation, immutable state bindings, and generation-aware links for entitlements,
prods, and acknowledgments. It does not add a terminal-state column or duplicate closing
disposition.

The migration makes each closed assignment project `terminal` from its exact existing
disposition. It backfills each open assignment as `staffing`, generation 1, and binds its
existing entitlement to generation 1 while preserving whether that entitlement is armed,
claimed, or absent. It completes this backfill before supervision resumes. It does not infer
affinity or waiting from text, role names, attests, wakes, messages, or artifacts.

A reviewed manifest may convert a named passive owner card. Each entry names work-item ID,
assignment ID, preferred role, terminal disposition, principal, and reason. One transaction
verifies the row is still open and unchanged, writes affinity, disposes the assignment as
`converted_to_affinity`, cancels that assignment's unclaimed effort effects, and preserves
history.

The conversion refuses live child obligations, running work, ambiguous custody, or a state
generation newer than the manifest. No role-wide bulk rule is valid evidence.

### Operating pattern

This feature changes the operating pattern for assignment creators. The same release must
amend the operating manual and dispatching skill to require an explicit initial supervision
choice, explain the existing-wire `staffing` compatibility mapping, and preserve the wait
mapping in invariant 11. Guidance names the choice and commands; this specification remains
the sole home for state mechanics.

### Refusals and recovery

The gateway refuses missing or conflicting birth states, undeclared role dependencies,
missing or invalid required role bindings, role fields on `none` dependencies, invalid
affinity roles, missing supporting rows, target mismatches, wrong-owner decision requests,
stale generations, invalid terminal dispositions, and unsafe manifest conversions without
partial writes.

A missing required binding returns `required_role_binding_missing`. An invalid binding
returns `required_role_binding_invalid`. A supplied role field for a `none` dependency
returns `role_binding_not_allowed`. Each response identifies the mechanism and field. No
response substitutes preferred-owner affinity or another inferred role.

Each refusal returns the current state and the exact lawful remedy. Crash replay returns the
original transaction outcome. It creates no second wake, blocker, affinity event,
entitlement, prod, acknowledgment, or disposition.

## Acceptance

1. Given an unstaffed work item, when an authorized owner sets affinity to a valid role,
   then the response shows that role and the row counts for assignments, holder wakes, prod
   entitlements, and escalations do not change.
2. Given a work item with affinity, when an authorized caller assigns a different holder,
   then creation succeeds and the response shows both the unchanged affinity and new holder.
3. Given an invalid role or unauthorized principal, when the caller sets affinity, then the
   gateway returns a refusal and writes no affinity event.
4. Given a new-version create request with zero or two supervision members, when the gateway
   validates it, then it refuses and writes no assignment or state binding.
5. Given `{kind: staffing}`, when creation commits, then the response shows generation 1 and
   exactly one armed entitlement for that assignment and generation.
6. Given a born-scheduled assignment with a timed self-wake, when the due wake starts an
   authenticated holder turn, then one transaction changes the state to `staffing`, advances
   the generation, and arms one entitlement.
7. Given a born-scheduled assignment waiting on another assignment, when its supporting wake
   is inspected, then it is a fact subscription scoped to the dependency and not a timed
   polling wake.
8. Given an in-org dependency completes concurrently with scheduled assignment creation,
   when the transaction commits, then the assignment is either created as `staffing` from
   the observed completion or created as `scheduled` with a subscription that receives the
   completion fact.
9. Given an external CI boundary, when a holder schedules a recheck, then the wake is timed
   and its prompt names the CI probe and the evidence to record.
10. Given an open operator request for the same owner, when an assignment enters
   `blocked/operator_decision`, then it references that request and creates no timer or
   holder-effort prod.
11. Given an operator request for another owner or a closed request, when the assignment
    tries to use it as a blocker, then the gateway refuses without changing state.
12. Given an unchanged `scheduled`, `blocked`, or `terminal` generation, when prodder and
    patrol scan it repeatedly, then they emit no holder-effort prod or escalation.
13. Given a scan observes `staffing` generation N and a transition commits generation N+1
    before prod claim, when claim runs, then it writes no deliverable prod for generation N.
14. Given a scheduled wake from a turn whose message has no assignment attribution, when the
    assignment transition commits, then the wake remains directly bound to the assignment
    and generation.
15. Given an assignment has reached `terminal`, when a caller requests resume, then the
    gateway refuses and reports that new work requires a new assignment.
16. Given an existing closed assignment and an existing open assignment, when migration
    runs, then the closed row projects `terminal` from its unchanged disposition, the open
    row stores `staffing` generation 1, and no prose or role-name inference creates affinity.
17. Given a reviewed conversion manifest for one unchanged passive owner card, when the
    transaction commits, then it writes affinity and `converted_to_affinity` terminal history
    while preserving prior wakes, attests, artifacts, and escalations.
18. Given a manifest entry with running work, live child obligations, ambiguous custody, or a
    stale generation, when conversion runs, then it refuses and changes neither affinity nor
    assignment state.
19. Given a successful create or transition response is lost, when the caller retries the
    same idempotency key, then the gateway returns the original state and state-binding IDs
    and row counts do not increase.
20. Given an existing-wire create request that omits the descriptor, when the gateway accepts
    it, then the response and audit event explicitly show `staffing`, generation 1.
21. Given a new wire version requires the descriptor, when its create request omits the
    descriptor, then the gateway refuses and names the missing field as the remedy.
22. Given the release contains this feature, when its served operating manual and dispatching
    skill are inspected, then they require the initial supervision choice and preserve the
    three wait instruments without duplicating state mechanics.
23. Given any escalation-targeting, staff-loss-rerouting, office-continuity, or relief
    mechanism declares `required`, when activation omits `roleName`, then the gateway returns
    `required_role_binding_missing`, identifies the mechanism and field, and writes no
    mechanism instance or downstream recovery effect.
24. Given a `required` recovery mechanism and a registered `roleName`, when activation
    commits, then the same transaction writes the exact binding with the mechanism instance.
25. Given a work item has `preferredOwnerRole`, when a `required` recovery mechanism omits
    its binding, then the gateway refuses and does not copy the preferred role.
26. Given a recovery mechanism declares `none`, when its schema and activation seam are
    inspected, then neither exposes an optional role-hint field.
27. Given a recovery mechanism declares `none`, when a caller supplies a role field, then
    the gateway returns `role_binding_not_allowed` and writes no mechanism instance or
    downstream recovery effect.
28. Given the automatic stamp proposed by `wi_7f068d0c` exists on an opened row, when a
    `required` recovery mechanism omits its binding, then the gateway still returns
    `required_role_binding_missing` unless that stamp's reviewed canonical contract defines
    it as the exact binding at that mechanism seam.

## Open Questions

None. Independent review may request changes, but no known product decision is being passed
to the builder.
