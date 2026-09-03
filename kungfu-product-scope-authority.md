# Kung Fu product-scope authority

Status: ready for one independent review; not implementation authority. This
specification is based on Tightbeam
`3e1dc56e1bd27854487228c05f4b2e1c9dd4fb22` and tightbeam-specs
`9437c920272dd3ec22d972af6faa695a5c4c211b`. Product-authority source:
work item `wi_b145b076-e2d4-4c6f-bb1e-5949485f1385` and its user-authored durable
trace. This specification amends the product-scope, spec-review, and
spec-dispatch clauses of `agentic-engineering-guidance-spec.md`.

## Goal

Keep product-scope decisions with the requesting user or the product owner. A
reviewer can report scope drift. A reviewer cannot require a product expansion.
A spec-writer cannot change a product boundary without a ruling from one of those
two authorities.

Before Tightbeam opens implementation work for a spec-backed product change, it
must have two separate facts: the spec's current independent review is
`reviewed-clean`, and the requesting user or product owner accepted the exact
current scope. Review continues to enforce law, correctness, and quality floors.

## Non-Goals

- No new product-discovery, rumination, adjudication, or review ritual.
- No attest for each engineering tenet.
- No review-round count, elapsed-time gate, or review timeout.
- No scope authority derived from reviewer, spec-writer, coder, orchestrator, or
  administrator status. A process principal and an unbound product-owner session
  have no scope authority.
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
- **Product owner**: the active session currently bound to the `product-owner`
  role. The role's `ownerUserId`, the session's `ownerUserId`, and the work item's
  `ownerUserId` are equal. An archetype name, an earlier role binding, or role
  fallback does not confer this authority.
- **Product authority**: the requesting user or the product owner, as defined
  above.
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
  latest verdict row by attest time and SQLite `rowid`. Its assignment holder differs
  from the spec assignment holder. Its verdict is `reviewed-clean`. Its spec
  verdict binding equals the work item's current spec binding. A later
  `changes-requested` verdict or a spec-binding change makes the review
  non-qualifying.
- **Scope acceptance**: a `scope-accepted` verdict filed on the open spec
  assignment by product authority after a current qualifying spec review exists.
  The filing captures the work item's current `specRefName` and
  `specRefSha256` as typed data in the same transaction as the attest.
- **Current scope acceptance**: the scope acceptance whose captured work item,
  spec ref, and SHA-256 equal the implementation dispatch's current work-item
  binding.
- **Authorized spec package**: one spec assignment with a current qualifying spec
  review and a current scope acceptance. Facts from different spec assignments
  do not form a package.
- **Spec-backed product implementation dispatch**: a `dispatch` call on a work
  item with a spec ref. The feature cycle continues to use `assign` for spec
  production and linked review cards.
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
- Role binding and principal typing continue to be substrate facts rather than
  claims in attest notes.
- The rules engine continues to run at the dispatch chokepoint before an
  assignment or wake is created.

## Invariants

1. Only product authority can create a `scope-accepted` fact.
2. Scope acceptance authorizes product scope. It does not approve review quality
   or waive law, safety, correctness, or a quality floor.
3. `reviewed-clean` approves review quality. It does not accept product scope.
4. A spec-backed product implementation dispatch needs a current qualifying spec
   review and a current scope acceptance on the same spec assignment.
5. A review or scope acceptance for one spec hash cannot authorize another spec
   hash.
6. A reviewer's proposed expansion cannot become a blocking requirement without
   a product-authority ruling recorded in the canonical spec.
7. A spec-writer cites a product-authority ruling in the canonical spec before
   changing product scope.
8. The existing product-owner rumination and spirit duty supplies the judgment
   used for scope acceptance. The change adds no second thought process.
9. Spec production and linked review assignment remain available before the two
   implementation-dispatch facts exist.
10. The spec-backed scope gate replaces the current `spirit-approved` existence
    gate. The spec-less substantial-work spirit review remains unchanged.
11. The substrate records principals, bindings, links, hashes, and verdict values.
    It does not decide whether product authority should accept the scope.

## Architecture

### Authority at the filing seam

The `attest` mutation seam captures a spec verdict binding when a linked review
holder files a verdict on a spec assignment. This binding identifies the exact
spec version judged by that verdict.

The Kung Fu authorization rule at the same edge recognizes `scope-accepted` as an
authority-bearing verdict. In the attest transaction the edge verifies the open
spec-assignment target, the typed principal, the owner-matched current
product-owner role and session when the signer is a session, the current
qualifying spec review on that assignment, and the current work-item spec
binding. It then records the attest plus its captured work-item id, spec ref, and
SHA-256 atomically. A refusal records no attest or scope-acceptance row.

The implementation may extend the attest schema or add one attest-owned relation
for typed spec verdict bindings. Neutral substrate facts expose principal,
work-item-owner, active role-binding, assignment-link, and spec-hash
relationships. The Agentic Engineering rule names `product-owner` and
`scope-accepted`; substrate code does not judge the proposed scope. The
implementation must not infer authority, review identity, or spec identity from
free-text notes. `attest` remains the sole mutation seam for these verdict
bindings and scope acceptance.

### Facts at the dispatch seam

The rules engine exposes one neutral fact for an authorized spec package. It also
exposes the review and scope components so a denial can name the missing or stale
component. The Kung Fu dispatch policy denies a spec-backed product
implementation dispatch when the package is absent. A denied dispatch creates no
assignment and schedules no delivery wake. The `assign` verb remains the pre-gate
path for spec production, linked review, and evidence cards.

When review and scope components exist on different spec assignments, the denial
names that mismatch instead of claiming either component is absent.

The assignment-opening transaction revalidates the authorized spec package used
by the rules decision. If the spec binding or latest review verdict changes before
the assignment opens, the call is refused. A successful idempotent replay returns
its previously authorized assignment under the existing replay semantics.

### Guidance projection

The implementation makes one coherent doctrine visible in these existing homes:

- `product-owner` guidance reuses its product-discovery, rumination, and spirit
  duty for the final scope signoff after independent review.
- `reviewer` guidance and `reviewing-specs` permit scope-drift reports, prohibit
  reviewer-mandated expansion, and route proposed boundary changes to product
  authority.
- `spec-writer` guidance and `spec-handoff` require a cited product-authority
  ruling before a scope change, then require exact candidate binding, independent
  review, and final scope acceptance before implementation handoff. The
  spec-writer keeps the spec assignment open until scope acceptance lands, then
  completes it.
- `feature-cycle` orders spec drafting, exact candidate binding, independent
  review, scope acceptance, and implementation dispatch. Binding the candidate
  before review does not authorize implementation; the two verdict facts do.
- `engineering-tenets` states the separation between product authority and review
  authority.
- `subtraction` keeps ADD, DELETE, and ACCEPT available to product authority. A
  reviewer cannot turn ADD into a requirement by filing a quality verdict.
- `agentic-engineering-guidance-spec.md` adds `scope-accepted` to the canonical
  vocabulary and replaces its spec-backed spirit-gate description with this
  contract.

This change does not add a skill or include to an archetype manifest. It projects
the doctrine through the reviewer homes selected by the canonical review-guidance
contract at implementation time. No neutral operating-manual amendment is needed;
this is an agentic-engineering Kung Fu pattern.

`review-guidance-restructure-2026-09-03.md` landed on specs `origin/main` after
the pinned baseline for this draft. If its reviewer split reaches Tightbeam before
this change, the reviewer clauses above belong in `review-common.md` and
`reviewer-spec.md`; the implementation must not restore the retired review skills
or the single `reviewer` archetype.

### Existing rows

The migration does not turn an existing free-text `scope-accepted`,
`spirit-approved`, or unbound `reviewed-clean` verdict into a typed spec verdict
binding. Those rows remain history but do not satisfy the new dispatch policy. An
in-flight spec-backed item obtains fresh exact-bound verdicts through its existing
spec assignment or a lawful reopened or replacement card. The pre-gate `assign`
path keeps that recovery available.

### Subtraction decision

ADD wins because it extends the existing attest and dispatch seams; DELETE would
remove spec-backed product delivery, while ACCEPT would leave unauthorized scope
changes representable and undiscoverable at dispatch.

## Acceptance

1. **Requesting-user signer.** Given an open spec assignment with a pinned spec and
   a current qualifying spec review for that hash, when the user principal matching
   `ownerUserId` files `scope-accepted`, then Tightbeam records one scope acceptance
   with the current work-item id, spec ref, and SHA-256.
2. **Product-owner signer.** Given the same state and an active `product-owner`
   binding whose role owner and session owner match the work item's user, when
   that bound session files `scope-accepted`, then Tightbeam records the same typed
   scope fields.
3. **Unauthorized signer.** Given the same state, when a reviewer, spec-writer,
   coder, orchestrator, non-owner administrator, process principal, user-owned agent,
   unbound product-owner session, former binding, or product owner for another user
   files `scope-accepted`, then Tightbeam returns `not_authorized` and records no
   attest.
4. **Invalid target.** Given any principal, when it files `scope-accepted` on a
   review assignment, a non-spec assignment, a closed spec assignment, or an
   assignment without a spec-backed work item, then Tightbeam refuses the filing
   with the applicable target or state error and records no attest.
5. **Final ordering.** Given a product-authority signer and an open spec
   assignment, when no current qualifying spec review or complete spec binding
   exists, then Tightbeam refuses `scope-accepted` and records no attest.
6. **Unbound spec review.** Given a review linked to a spec assignment whose work
   item has no complete spec binding, when the review holder files a verdict, then
   Tightbeam refuses the filing because it cannot identify the reviewed spec
   version and records no attest.
7. **Review-only denial.** Given a spec-backed product implementation dispatch with
   a current qualifying spec review and no current scope acceptance, when the
   caller dispatches, then Tightbeam denies it for missing `scope-accepted`, creates
   no assignment, and schedules no wake.
8. **Acceptance-only denial.** Given a historical scope acceptance and a current
   review whose latest holder verdict is `changes-requested`, when the caller
   dispatches, then Tightbeam denies it for missing `reviewed-clean`, creates no
   assignment, and schedules no wake.
9. **Non-independent review denial.** Given a linked review held by the spec writer
   or a verdict filed by someone other than the review holder, when the caller
   dispatches, then that verdict does not qualify and Tightbeam denies the
   dispatch.
10. **Latest review wins.** Given an older `reviewed-clean` verdict and a newer
   holder-filed `changes-requested` verdict, when the caller dispatches, then the
   older clean verdict does not qualify and Tightbeam denies the dispatch.
11. **Hash mismatch denial.** Given a qualifying review and scope acceptance for
    spec hash A, when the work item binds spec hash B and the caller dispatches,
    then Tightbeam denies the dispatch for missing current review and scope
    acceptance.
12. **Same-assignment conjunction.** Given a qualifying review for spec assignment
    A and scope acceptance for spec assignment B on the same work item and hash,
    when the caller dispatches, then Tightbeam denies the dispatch because no
    authorized spec package exists.
13. **Decision race.** Given an authorized spec package, when the work-item binding
    changes or a newer `changes-requested` review lands before assignment creation,
    then Tightbeam creates no assignment and schedules no wake.
14. **Successful conjunction.** Given an authorized spec package for the current
    work-item binding, when the caller makes a spec-backed product implementation
    dispatch, then Tightbeam opens one assignment and schedules its normal
    delivery wake.
15. **Pre-gate cards.** Given a spec-backed work item without an authorized spec
    package, when the orchestrator uses `assign` for spec production, linked review,
    or evidence work, then the new dispatch policy does not deny that assignment.
16. **Reviewer boundary.** Given a reviewer sees a useful feature outside the
    authorized Goal, when the candidate can satisfy the current Goal without that
    feature, then the reviewer does not make the feature a blocking finding and
    routes the proposal to product authority.
17. **Scope-drift correction.** Given a candidate contradicts an authorized Goal
    or enters a Non-Goal, when the reviewer files its verdict, then it can require
    the candidate to return to the authorized boundary and can separately ask
    product authority whether the boundary should change.
18. **Spec-writer boundary.** Given review feedback proposes a change to Goal,
    Non-Goals, product-observable behavior, or product stance, when no
    product-authority ruling exists, then the spec-writer leaves that scope
    unchanged and requests the ruling.
19. **Ruling trace.** Given product authority approves a named scope change, when
    the spec-writer incorporates it, then the canonical spec cites the durable row
    that carries the ruling before the candidate is reviewed.
20. **Independent floors.** Given valid scope acceptance and a blocking statute,
    safety, correctness, or quality-floor failure, when implementation dispatch or
    completion reaches that floor's existing enforcement edge, then scope
    acceptance does not release it.
21. **No duplicate ceremony.** Given the final reviewed spec, when the product
    owner evaluates scope, then the documented flow uses the existing rumination
    and spirit duty and produces the required `scope-accepted` filing for that
    exact hash.
22. **Regression boundary.** Given substantial work without an owner-gated spec,
    when it reaches the existing spirit-review edge, then the existing
    `spirit-accepted` flow remains unchanged.
23. **Projection coherence.** Given the shipped Agentic Engineering bundle, when a
    reviewer compares the served product-owner, reviewer, spec-writer, and
    orchestrator identities, then each teaches the same review-before-signoff and
    signoff-before-implementation order without granting scope authority to a new
    actor.
24. **Open signoff target.** Given a `reviewed-clean` verdict on a spec assignment,
    when the scope signoff is still absent, then the served spec-writer and handoff
    guidance keep that assignment open so product authority can file the signoff.
25. **No invented migration.** Given a database with `spirit-approved`, free-text
    `scope-accepted`, or `reviewed-clean` verdicts that lack an exact spec verdict
    binding, when the migration runs, then it preserves those rows as history and
    none qualifies an implementation dispatch.

## Open Questions

None.
