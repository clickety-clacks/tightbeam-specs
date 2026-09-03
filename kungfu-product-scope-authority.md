# Kung Fu product-scope authority

Status: candidate for one independent exact-tip review; not implementation or
landing authority. This specification is based on Tightbeam
`42c20cdcee81c632a26b663ab0521642ee4a7b7d` and tightbeam-specs
`e125efe346a51f115785b5e7ad5804355b958a42`.

Product authority comes from work item
`wi_b145b076-e2d4-4c6f-bb1e-5949485f1385` and its user-authored durable trace.
The B1 and B2 corrections come from owner ruling
`dr_6f85d524-aa0b-493b-ac26-427ccaaebac9`. They answer the blocking findings in
verdict `att_61c8f42f-7608-4a14-bd75-64052d92b473` and report
`art_49aff2e0`. This specification amends the product-scope, spec-review, and
spec-assignment-opening clauses of `agentic-engineering-guidance-spec.md`.

## Goal

Keep product-scope decisions with the requesting user or the responsible product
owner. A reviewer can report scope drift. A reviewer cannot require a product
expansion. A spec-writer cannot change a product boundary without a ruling from
one of those two authorities.

Before Tightbeam opens implementation work for a spec-backed product change, it
must have two separate facts: the spec's current independent review is
`reviewed-clean`, and the requesting user or responsible product owner accepted
the exact current scope. The same gate applies to every assignment-opening verb.
Review continues to enforce law, correctness, and quality floors.

## Non-Goals

- No new product-discovery, rumination, adjudication, or review ritual.
- No attest for each engineering tenet.
- No review-round count, elapsed-time gate, or review timeout.
- No scope authority derived from reviewer, spec-writer, coder, orchestrator,
  administrator, role-name prefix, or same-user ownership alone. A process
  principal, role fallback, and an unbound product-owner session have no scope
  authority.
- No classifier that infers implementation purpose from prose, declared files,
  effect kind, holder archetype, role name, or command name.
- No weakening of a statute, safety rule, correctness requirement, or quality
  floor.
- No change to the spirit review for substantial work that has no owner-gated
  spec.
- No product runtime, served identity, credential, release, deployment, or live
  session mutation as part of specifying this change.

## Terms

- **Product scope**: the Goal, Non-Goals, product-observable behavior, and product
  stance recorded in the canonical spec. Product stance selects a position above
  a mandatory law or quality floor. Product scope excludes implementation detail,
  statute compliance, safety, correctness, and the mandatory floor itself.
- **Requesting user**: the user principal whose id equals the work item's
  `ownerUserId`. A session owned by that user is not the user principal.
- **Product-owner-role binding**: the work item's durable
  `productOwnerRole` value. The value is one exact role name. It is not an
  archetype name or a role-name pattern. Only the requesting user can create,
  replace, or clear this binding on an open work item.
- **Responsible product owner**: the session principal that satisfies all of
  these conditions when it files `scope-accepted`:
  1. the work item has a non-null product-owner-role binding;
  2. the exact named role exists and its `ownerUserId` equals the work item's
     `ownerUserId`;
  3. that role is directly bound to the calling session, without role fallback;
  4. the calling session is active, its `ownerUserId` equals the work item's
     `ownerUserId`, and its archetype is `product-owner`.
  A different product-owner role does not qualify, even when its session and the
  work item have the same `ownerUserId`.
- **Product authority**: the requesting user or the responsible product owner,
  as defined above.
- **Product-authority ruling**: a durable Tightbeam row attributable to product
  authority that expressly decides one named product-scope question. The spec
  cites that row when it incorporates the decision. A review suggestion, an
  agent-owned summary, or scope acceptance for an earlier spec hash is not a
  ruling for a new scope change.
- **Spec assignment**: a non-review assignment on the work item whose holder has
  the `spec-writer` archetype.
- **Spec verdict binding**: the work-item id, `specRefName`, and
  `specRefSha256` captured as typed data when a holder files a verdict on a review
  linked to a spec assignment.
- **Current qualifying spec review**: among verdicts filed by the holders of
  assignments linked with `reviewsAssignmentId` to one spec assignment, the
  latest verdict row by attest time and SQLite `rowid`. Its assignment holder
  differs from the spec assignment holder. Its verdict is `reviewed-clean`. Its
  spec verdict binding equals the work item's current spec binding. A later
  `changes-requested` verdict or a spec-binding change makes the review
  non-qualifying.
- **Scope acceptance**: a `scope-accepted` verdict filed on the open spec
  assignment by product authority after a current qualifying spec review exists.
  The filing captures the work item's current `specRefName` and
  `specRefSha256` as typed data in the same transaction as the attest.
- **Current scope acceptance**: the scope acceptance whose captured work item,
  spec ref, and SHA-256 equal the assignment-opening call's current work-item
  binding.
- **Authorized spec package**: one spec assignment with a current qualifying spec
  review and a current scope acceptance. Facts from different spec assignments do
  not form a package.
- **Assignment-opening verb**: either `assign` or `dispatch`. These are the
  complete assignment-opening verb set in the pinned Tightbeam source.
- **Implementation purpose**: the Boolean typed field
  `implementationPurpose` on an assignment-opening call and on its resulting
  assignment. For a spec-backed work item, every `assign` and `dispatch` call must
  provide this field. `true` declares implementation work and invokes the
  authorized-spec-package gate. `false` declares pre-implementation work and does
  not invoke this scope gate. Spec production, linked review, and evidence work
  use `false`. The field is independent of `effectKind`.
- **Spec-backed product implementation opening**: an `assign` or `dispatch` call
  whose work item has a complete spec binding and whose
  `implementationPurpose` is `true`.
- **Scope drift report**: a review finding that identifies a difference between
  the authorized product scope and the candidate. It can require the candidate to
  return to the authorized scope. It can propose a different scope only as a
  question for product authority.

## Assumptions

- Work items continue to bind a canonical spec with `specRefName` and
  `specRefSha256`.
- Review assignments continue to identify their subject through
  `reviewsAssignmentId`.
- A holder-filed verdict on a linked review assignment continues to be the
  substrate's evidence of that reviewer's judgment.
- Role names, direct role bindings, role owners, session owners, session state,
  and session archetypes continue to be typed substrate facts.
- `ownerUserId` continues to identify the requesting-user authority. The new
  product-owner-role binding does not replace it.
- `assign` and `dispatch` continue to share the rules chokepoint and the
  assignment-opening transaction.

## Invariants

1. Only product authority can create a `scope-accepted` fact.
2. A product-owner session has authority only through the work item's exact
   current product-owner-role binding. Same-user ownership, a namespaced-role
   prefix, an archetype name, a stale binding, and fallback resolution do not
   confer authority.
3. Scope acceptance authorizes product scope. It does not approve review quality
   or waive law, safety, correctness, or a quality floor.
4. `reviewed-clean` approves review quality. It does not accept product scope.
5. Every spec-backed assignment-opening call carries one Boolean
   `implementationPurpose`. Missing, null, string, integer, or other values are
   invalid.
6. Both `assign` and `dispatch` deny a spec-backed product implementation opening
   unless the current work-item binding has an authorized spec package.
7. `implementationPurpose=false` keeps spec production, linked review, and
   evidence work before the package gate. No rule infers this value from another
   field.
8. A review or scope acceptance for one spec hash cannot authorize another spec
   hash.
9. A reviewer's proposed expansion cannot become a blocking requirement without
   a product-authority ruling recorded in the canonical spec.
10. A spec-writer cites a product-authority ruling in the canonical spec before
    changing product scope.
11. The existing product-owner rumination and spirit duty supplies the judgment
    used for scope acceptance. The change adds no second thought process.
12. The spec-backed scope gate replaces the current `spirit-approved` existence
    gate. The spec-less substantial-work spirit review remains unchanged.
13. The substrate records principals, bindings, links, hashes, purposes, and
    verdict values. It does not decide whether product authority should accept
    the scope.

## Architecture

### Current source seams

- `lib/tightbeam/work_items.ex` owns the durable work-item record, spec binding,
  owner, and version.
- `lib/tightbeam/roles.ex` owns exact role names, direct session bindings, and
  role owners.
- `lib/tightbeam/dispatch.ex` runs rules for both assignment-opening verbs.
- `lib/tightbeam/assignments.ex` validates and opens both `assign` and
  `dispatch` assignments.
- `lib/tightbeam/rules.ex` exposes typed facts to the Kung Fu rules.
- `lib/tightbeam/wire/router.ex` and `cli/src/args.rs` carry the two new typed
  inputs through the existing wire and CLI surfaces.

### Durable product-owner-role binding

The work-item mutation seam stores one nullable typed `productOwnerRole` value as
part of the work item's durable state. The value stores the exact namespaced role
name. The implementation may extend the existing work-item row or use one
work-item-owned typed relation; it must not create a second work-item authority
model.

The requesting-user principal can set, replace, or clear the value while the work
item is open. A session principal, administrator status without requesting-user
identity, process principal, role holder, or role fallback cannot change it. A
write validates that the exact role exists, that the role's `ownerUserId` equals
the work item's `ownerUserId`, and that the role's current directly bound session
uses the `product-owner` archetype. The mutation records the value and the work
item version atomically. A refusal changes neither.

Rebinding the named role to a different active product-owner session changes who
can act as responsible product owner without changing the work-item value. A
different role never substitutes for the named role.

### Authority at the filing seam

The `attest` mutation seam captures a spec verdict binding when a linked review
holder files a verdict on a spec assignment. This binding identifies the exact
spec version judged by that verdict.

The Kung Fu authorization rule at the same edge recognizes `scope-accepted` as an
authority-bearing verdict. In the attest transaction, the edge verifies the open
spec-assignment target, the typed principal, the current qualifying spec review,
and the current work-item spec binding. For a session signer, it also verifies the
current exact product-owner-role relation defined above. It then records the
attest plus its captured work-item id, spec ref, and SHA-256 atomically. A refusal
records no attest or scope-acceptance row.

The implementation may extend the attest schema or add one attest-owned relation
for typed spec verdict bindings. Neutral substrate facts expose principal,
work-item-owner, product-owner-role, direct role-binding, assignment-link, and
spec-hash relationships. The Agentic Engineering rule names `product-owner` and
`scope-accepted`; substrate code does not judge the proposed scope. The
implementation must not infer authority, review identity, or spec identity from
free-text notes.

### Purpose at every assignment-opening seam

The `assign` and `dispatch` transports both accept
`implementationPurpose: boolean`. Their shared pre-rule validation requires the
field on every call for a spec-backed work item and refuses any non-Boolean value.
The same typed value reaches the rule decision and the assignment-opening
transaction. A successful opening stores it as immutable assignment data.

The rules engine exposes the raw typed purpose and one neutral fact for an
authorized spec package. The Kung Fu rules apply the same package predicate to
both assignment-opening verbs. They deny when the work item is spec-backed, the
purpose is `true`, and the package is absent. They do not deny a purpose-`false`
call. Other existing rules can still deny that call independently.

The assignment-opening transaction revalidates the work-item spec binding,
purpose, latest qualifying review, and current scope acceptance before it inserts
the assignment or schedules a delivery wake. A denial creates no assignment and
schedules no delivery wake. A successful keyed replay returns only the original
assignment and its immutable purpose under the existing replay semantics; replay
does not create a new authorization decision.

### Guidance projection

The implementation makes one coherent doctrine visible in these existing homes:

- `product-owner` guidance reuses its product-discovery, rumination, and spirit
  duty for the final scope signoff after independent review. It acts only for work
  items whose exact product-owner-role binding names its role.
- The elected reviewer guidance and spec-review guidance permit scope-drift
  reports, prohibit reviewer-mandated expansion, and route proposed boundary
  changes to product authority.
- `spec-writer` guidance and `spec-handoff` require a cited product-authority
  ruling before a scope change. They require exact candidate binding,
  independent review, and final scope acceptance before implementation handoff.
  The spec-writer keeps the spec assignment open until scope acceptance lands.
- `feature-cycle` supplies `implementationPurpose=false` for spec production,
  linked review, and evidence assignments. It supplies `true` for every
  implementation opening, whether it uses `assign` or `dispatch`.
- `engineering-tenets` states the separation between product authority and review
  authority.
- `subtraction` keeps ADD, DELETE, and ACCEPT available to product authority. A
  reviewer cannot turn ADD into a requirement by filing a quality verdict.
- `agentic-engineering-guidance-spec.md` adds `scope-accepted`,
  `productOwnerRole`, and `implementationPurpose` to the canonical vocabulary and
  replaces its spec-backed spirit-gate description with this contract.

This change does not add a skill or include to an archetype manifest. It projects
the doctrine through the reviewer homes selected by the canonical review-guidance
contract at implementation time. If the split in
`review-guidance-restructure-2026-09-03.md` reaches Tightbeam first, the clauses
belong in `review-common.md` and `reviewer-spec.md`; the implementation must not
restore retired review skills. No neutral operating-manual amendment is needed;
this is an Agentic Engineering Kung Fu pattern.

### Existing rows and in-flight work

Migration adds a null product-owner-role binding to existing work items. A null
binding gives no session product-scope authority; the requesting user retains
authority through `ownerUserId`. The requesting user can set the exact role on an
open item through the same work-item mutation seam.

Migration does not turn an existing free-text `scope-accepted`,
`spirit-approved`, or unbound `reviewed-clean` verdict into a typed spec verdict
binding. Those rows remain history but do not satisfy the new gate. Existing
assignments retain no invented purpose. They continue under their recorded state;
the new field applies when a later assignment opens.

An in-flight spec-backed item obtains fresh exact-bound verdicts through its
existing spec assignment or a lawful reopened or replacement card. Each later
`assign` or `dispatch` supplies its Boolean purpose. Purpose `false` keeps the
recovery path available.

### Subtraction decision

ADD wins because it adds only the two owner-ruled typed bindings at the existing
work-item, attest, rules, and assignment-opening seams. DELETE would remove
spec-backed product delivery. ACCEPT would leave the two reviewed authority
bypasses in place.

## Acceptance

1. **Requesting-user signer.** Given an open spec assignment with a pinned spec
   and a current qualifying spec review for that hash, when the user principal
   matching `ownerUserId` files `scope-accepted`, then Tightbeam records one scope
   acceptance with the current work-item id, spec ref, and SHA-256.
2. **Responsible product-owner signer.** Given the same state, a work item whose
   `productOwnerRole` is `product-owner:alpha`, and that exact role directly bound
   to an active `product-owner` session with the matching owner, when that session
   files `scope-accepted`, then Tightbeam records the same typed scope fields.
3. **Same-user wrong-product denial.** Given the state in Acceptance 2 and another
   active `product-owner` session bound to `product-owner:beta` with the same
   `ownerUserId`, when the beta session files `scope-accepted`, then Tightbeam
   returns `not_authorized` and records no attest.
4. **Product-owner negative matrix.** Given the state in Acceptance 2, when an
   unbound session, a session bound through fallback, a former alpha binding, a
   session bound to a different exact role, a non-product-owner session, a
   reviewer, spec-writer, coder, orchestrator, process principal, user-owned
   agent, or non-owner administrator files `scope-accepted`, then Tightbeam
   returns `not_authorized` and records no attest.
5. **Role-binding write.** Given an open work item and an existing directly bound
   product-owner role with matching ownership, when the requesting user sets that
   exact role as `productOwnerRole`, then Tightbeam atomically records the role
   and advances the work-item version.
6. **Role-binding write denial.** Given any work item, when a session principal,
   role holder, process principal, non-owner administrator, role with a different
   owner, nonexistent role, or role bound to a non-product-owner session attempts
   to set `productOwnerRole`, then Tightbeam refuses and leaves the work item
   unchanged.
7. **Invalid scope target.** Given any principal, when it files
   `scope-accepted` on a review assignment, non-spec assignment, closed spec
   assignment, or assignment without a spec-backed work item, then Tightbeam
   refuses and records no attest.
8. **Final ordering.** Given a product-authority signer and an open spec
   assignment, when no current qualifying spec review or complete spec binding
   exists, then Tightbeam refuses `scope-accepted` and records no attest.
9. **Unbound spec review.** Given a review linked to a spec assignment whose work
   item has no complete spec binding, when the review holder files a verdict,
   then Tightbeam refuses because it cannot identify the reviewed spec version
   and records no attest.
10. **Missing purpose.** Given a spec-backed work item, when either `assign` or
    `dispatch` omits `implementationPurpose`, then Tightbeam returns
    `invalid_implementation_purpose`, creates no assignment, and schedules no
    delivery wake.
11. **Invalid purpose types.** Given a spec-backed work item, when either opening
    verb supplies null, a string, an integer, an object, or an array as
    `implementationPurpose`, then Tightbeam returns
    `invalid_implementation_purpose`, creates no assignment, and schedules no
    delivery wake.
12. **Dispatch implementation denial.** Given a spec-backed work item with
    `implementationPurpose=true` and no authorized spec package, when the caller
    uses `dispatch`, then Tightbeam denies the call, creates no assignment, and
    schedules no delivery wake.
13. **Assign implementation denial.** Given the same state, when the caller uses
    `assign` with `effectKind=code`, declared files, and
    `implementationPurpose=true`, then Tightbeam denies the call, creates no
    assignment, and schedules no delivery wake.
14. **Policy implementation denial.** Given the same state, when the caller uses
    `assign` with `effectKind=policy` and `implementationPurpose=true`, then
    Tightbeam denies the call. The policy effect kind does not exempt the call.
15. **Review-only denial.** Given `implementationPurpose=true`, a current
    qualifying review, and no current scope acceptance, when either opening verb
    runs, then Tightbeam denies it for missing `scope-accepted` and creates no
    assignment.
16. **Acceptance-only denial.** Given `implementationPurpose=true`, a historical
    scope acceptance, and a latest holder verdict of `changes-requested`, when
    either opening verb runs, then Tightbeam denies it for missing
    `reviewed-clean` and creates no assignment.
17. **Non-independent review denial.** Given a linked review held by the spec
    writer or a verdict filed by someone other than the review holder, when an
    implementation opening runs, then that verdict does not qualify and
    Tightbeam denies the opening.
18. **Latest review wins.** Given an older `reviewed-clean` verdict and a newer
    holder-filed `changes-requested` verdict, when an implementation opening
    runs, then the older clean verdict does not qualify and Tightbeam denies the
    opening.
19. **Hash mismatch denial.** Given a qualifying review and scope acceptance for
    spec hash A, when the work item binds spec hash B and an implementation
    opening runs, then Tightbeam denies it for missing current review and scope
    acceptance.
20. **Same-assignment conjunction.** Given a qualifying review for spec
    assignment A and scope acceptance for spec assignment B on the same work item
    and hash, when an implementation opening runs, then Tightbeam denies it
    because no authorized spec package exists.
21. **Decision race.** Given an authorized spec package, when the work-item spec
    binding changes or a newer `changes-requested` review lands before assignment
    creation, then Tightbeam creates no assignment and schedules no delivery wake.
22. **Successful dispatch.** Given an authorized spec package for the current
    work-item binding, when the caller uses `dispatch` with
    `implementationPurpose=true`, then Tightbeam opens one assignment, stores
    purpose `true`, and schedules its normal delivery wake.
23. **Successful assign.** Given the same package, when the caller uses `assign`
    with `implementationPurpose=true`, then Tightbeam opens one assignment and
    stores purpose `true`. The verb does not bypass the package gate.
24. **Pre-gate spec production.** Given a spec-backed work item without an
    authorized package, when the orchestrator opens spec-production work through
    either opening verb with `implementationPurpose=false`, then this scope gate
    does not deny the assignment.
25. **Pre-gate linked review.** Given the same work item, when the orchestrator
    opens a linked review through `assign` with `implementationPurpose=false`,
    then this scope gate does not deny the assignment.
26. **Pre-gate evidence.** Given the same work item, when the orchestrator opens
    evidence work through either opening verb with
    `implementationPurpose=false`, then this scope gate does not deny the
    assignment.
27. **Effect-kind independence.** Given two calls with the same effect kind and
    different Boolean purposes, when the rules engine evaluates them, then it
    gates the purpose-`true` call and leaves the purpose-`false` call to the other
    existing rules. It does not derive purpose from effect kind.
28. **Replay.** Given a keyed implementation opening already created an
    assignment with purpose `true`, when the same key replays, then Tightbeam
    returns that assignment with purpose `true` and creates no second assignment
    or wake.
29. **Reviewer boundary.** Given a reviewer sees a useful feature outside the
    authorized Goal, when the candidate can satisfy the current Goal without that
    feature, then the reviewer does not make the feature a blocking finding and
    routes the proposal to product authority.
30. **Scope-drift correction.** Given a candidate contradicts an authorized Goal
    or enters a Non-Goal, when the reviewer files its verdict, then it can require
    the candidate to return to the authorized boundary and can separately ask
    product authority whether the boundary should change.
31. **Spec-writer boundary.** Given review feedback proposes a change to Goal,
    Non-Goals, product-observable behavior, or product stance, when no
    product-authority ruling exists, then the spec-writer leaves that scope
    unchanged and requests the ruling.
32. **Ruling trace.** Given product authority approves a named scope change, when
    the spec-writer incorporates it, then the canonical spec cites the durable row
    that carries the ruling before the candidate is reviewed.
33. **Independent floors.** Given valid scope acceptance and a blocking statute,
    safety, correctness, or quality-floor failure, when implementation opening or
    completion reaches that floor's existing enforcement edge, then scope
    acceptance does not release it.
34. **No duplicate ceremony.** Given the final reviewed spec, when the responsible
    product owner evaluates scope, then the documented flow uses the existing
    rumination and spirit duty and produces `scope-accepted` for that exact hash.
35. **Spec-less regression boundary.** Given substantial work without an
    owner-gated spec, when it reaches the existing spirit-review edge, then the
    existing `spirit-accepted` flow remains unchanged.
36. **Projection coherence.** Given the shipped Agentic Engineering bundle, when
    a reviewer compares the served product-owner, reviewer-spec, spec-writer, and
    orchestrator identities, then each teaches the same review-before-signoff and
    signoff-before-implementation order, exact role binding, and Boolean purpose.
37. **Open signoff target.** Given a `reviewed-clean` verdict on a spec assignment,
    when scope signoff is absent, then the served spec-writer and handoff guidance
    keep that assignment open so product authority can file the signoff.
38. **No invented migration.** Given existing work items, assignments,
    `spirit-approved`, free-text `scope-accepted`, or `reviewed-clean` verdicts
    that lack the new typed bindings, when migration runs, then it preserves them
    as history and none gains invented product-owner authority, purpose, review
    qualification, or implementation authorization.

## Open Questions

None.
