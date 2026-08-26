# Identity universal-root include resolution

## Goal

Make the identity publication seam deliver fully rendered guidance.  A session
must never receive a literal `#include` directive from either universal root:
`operating-manual.md` or the required `operating-model.md`.

This change uses the already-established exact-line recursive include semantics
for both universal roots and the archetype's guidance. It makes an invalid
include graph fail before it can be committed or published. It also makes the
rendered bytes and renderer contract observable for existing sessions.

The authority for this scope is work item `wi_0c2f48b4-d9cf-46fc-a3e2-e0247b8a2881`.
Its settled rulings are `resolve-both-shared-semantics`,
`preserve-flat-strict-exact-once`, `validate-before-commit-and-live`, and
`stamp-render-contract-and-digest`.

## Non-Goals

- This spec does not change the guidance text, the set of universal roots, or
  the ownership of any fragment.
- This spec does not add include syntax, relative paths, conditional includes,
  a new guidance language, or a second renderer.
- This spec does not automatically reset a resident session. `identity apply`
  remains the explicit refresh seam.
- This spec does not restore Gibson's interim inline copies before an eligible
  fix-bearing release is installed. It does not change Shrdlu.
- This spec does not implement, release, deploy, or change credentials.

## Terms

- **Universal root**: `operating-model.md` or `operating-manual.md`, the two
  fragments composed for each served identity regardless of archetype.
- **Fragment catalog**: the name-to-bytes map built from the candidate identity
  revision's `guidance/**/*.md` files. The namespace is flat: a fragment name
  is its basename, not a path. `operating-manual.md` uses the shipped substrate
  bytes only when the candidate tree has no organization-owned fragment of that
  name; an organization-owned file wins.
- **Include directive**: one complete line matching
  `^#include "([^"/\\]+\.md)"[ \t]*$`. It names exactly one flat fragment.
  A line beginning with `#include` that does not match this grammar is an
  invalid directive, not ordinary prose.
- **Renderer**: the one shared pure resolver that accepts root bytes, their
  origin, and a fragment catalog; expands directives recursively in place; and
  returns rendered bytes plus provenance.
- **Root reachability**: a universal-root fragment occurs in the archetype
  guidance render graph through an explicit include, directly or transitively.
- **Universal-root occurrence**: one resolver traversal into a universal-root
  fragment through an explicit include path. A direct directive and a
  transitive directive path each count as an occurrence; it is not inferred
  from matching rendered prose.
- **Render contract**: the versioned composition rule named
  `universal-root-render-v1`: render archetype guidance first, append the
  engineering activity-table section when that existing feature applies, then
  append each universal root in the order `operating-model.md`,
  `operating-manual.md` only when that root is not already reachable.
- **Render stamp**: the provisioned session's immutable identity revision,
  render-contract name, and lowercase SHA-256 of the final harness-delivered
  guidance UTF-8 bytes.
- **Candidate tree**: the identity working tree or exact Git commit proposed by
  one identity mutation seam before `tightbeam/live` moves.
- **Candidate tree fingerprint**: the lowercase SHA-256 of the candidate tree's
  entries in ascending UTF-8 path order, with each entry encoded as its path,
  one NUL byte, and its raw file bytes. It is calculated without creating a
  candidate commit.
- **Canonical specification set**: this one-file set,
  `identity-universal-root-include-resolution.md`, in the `tightbeam-specs`
  repository. No companion specification is authoritative for this feature.
- **Validation-publication marker**: one durable record at the existing
  `AdminProjection` publication-stamp seam. Its key is the operation invocation
  ID and expected prior `tightbeam/live` OID (or `none` for fresh init). It
  records the candidate commit OID after one exists; before a commit it records
  the candidate tree fingerprint produced by the validator. Its fields include
  principal, validation result, typed cause when denied, and terminal state
  `accepted` or `denied`; it never contains guidance bytes.
- **Include provenance**: the root origin plus every traversed
  `fragment-name`, source path, and one-based line number in include order.

## Assumptions

- `operating-model.md` remains a required organization fragment. Its absence is
  already a repairable identity-state error; this contract makes its validation
  explicit.
- The current source has one recursive resolver for archetype guidance, but
  `Identity.snapshot_at!` reads the two universal-root strings without resolving
  them. Current `main` was inspected at `7a70a2f616363074514237b5bee48ba67c52e2ea`.
- The current Gibson mitigation at identity commit `89a6879` inlines the bodies
  of `specs-home.md` and `dev-on-gibson.md` in the manual. It is content
  mitigation, not resolver evidence.
- `guidance/specs-home.md` and `guidance/dev-on-gibson.md` are the authoritative
  current identity fragments for their respective sections when cleanup becomes
  eligible.

## Invariants

1. A served identity's final guidance contains no line that begins `#include`.
2. The renderer is the only implementation of include parsing, recursion,
   validation, and provenance for archetype guidance and both universal roots.
3. The fragment catalog rejects two different candidate paths with the same
   basename. It does not select a winner by traversal order.
4. The renderer preserves the bytes and relative order of each non-directive
   line. It replaces a directive at that line with the recursively rendered
   named fragment. It trims only the included fragment's terminal newline to
   preserve the existing join behavior.
5. The renderer expands each ordinary include occurrence. It does not globally
   de-duplicate ordinary fragments. Validation rejects a second
   universal-root occurrence of the same root with `identity_include_invalid`;
   the first occurrence remains the only reachable occurrence and is not
   appended again. It does not silently suppress the second directive.
6. The include graph rooted at either universal root must not reach either
   universal-root name. Validation rejects this configuration with the typed
   error rather than creating an order-dependent second composition path.
7. A resolution error names `identity_include_invalid`, the candidate root
   origin, the failing path and line, and the full include chain. For a duplicate
   basename it names both paths. For a missing name it names the requested name.
8. An include cycle is rejected before repeating a fragment in its active
   include stack. The active stack may contain at most ten fragment names;
   resolving an eleventh is rejected. No resolver failure serves a partial
   render.
9. Each identity mutation validates every archetype guidance root and both
   universal roots against one candidate tree before it creates a candidate
   commit. The sole publication gate revalidates the exact candidate commit
   immediately before it advances `tightbeam/live`.
10. A failed validation leaves `tightbeam/live` unchanged. Fresh `identity init`
    creates and validates a candidate repository outside the canonical identity
    path; it atomically exposes that repository at the canonical path only after
    validation succeeds. On failure it removes only the candidate repository,
    leaving no canonical identity repository or initialization marker.
    `identity edit`,
    scaffold, and unlearn restore their pre-mutation working bytes. Learn and a
   non-conflicted relearn abort their uncommitted merge/import. A failed
   `identity relearn --resolve` leaves its conflict open for correction.
11. Each validation-publication marker reaches exactly one terminal result.
    Its terminal result records the acting principal, candidate revision when
    one exists, accepted or denied result, and typed cause. A pending marker is
    not accepted evidence. The marker carries no full guidance body.
12. A session with a missing render stamp, a different render-contract, a
    different identity revision, or a different rendered-guidance digest than
    the expected served render is stale.

## Architecture

### Universal-root render contract

`Identity.snapshot_at!` builds one fragment catalog from its already resolved
identity revision and passes the catalog to the shared renderer for all three
roots. It must not fetch raw universal-root bytes after the renderer is chosen.

The renderer processes the requested root line by line. For each valid include
directive it pushes the named fragment and caller provenance, resolves that
fragment, and pops it after completion. It preserves the directive's position.
An invalid directive, missing fragment, duplicate catalog name, active-stack
cycle, or depth overflow returns the typed error; callers do not catch that
error and substitute raw text.

Universal roots cannot include either universal-root name. The renderer also
rejects a second explicit occurrence of one universal root while tracking
reachability. This is the smallest closure for the otherwise ambiguous
cross-root ordering: rejecting the second directive preserves the fixed
`operating-model.md`, then `operating-manual.md` order; accepting duplicate root
bytes violates the exact-once ruling, while silent suppression would conceal an
invalid candidate.

The composition algorithm is:

1. Render the archetype's guidance root.
2. Add the existing engineering activity-table section when it applies.
3. If `operating-model.md` was not reachable in step 1, render and append it.
4. If `operating-manual.md` was not reachable in step 1, render and append it.
5. Apply the harness's existing final guidance wrapper, then calculate the
   render stamp over those final delivered bytes.

Reachability is renderer metadata, not a substring search. Equal prose in two
fragments must not alter composition. Validation rejects universal-root-to-
universal-root reachability, so the fixed append order has no second path.

### Validation and publication

One validator constructs the candidate catalog, validates the duplicate-name
rule, and renders every archetype plus each universal root. The validator is
called by `identity init`, `identity edit`, kungfu scaffold, learn, unlearn,
relearn, and relearn conflict resolution before their mutable commit boundary.
Fresh init stages its seed repository beside, not at, the canonical identity
path; it creates the seed commit and required refs there, validates that exact
candidate, and then atomically renames the complete candidate into the
canonical path. A failed candidate is discarded before the path is exposed.
The publication seam receives an exact commit OID and runs the same validator
against that OID before it fast-forwards `tightbeam/live`.

Validation failure returns the typed error and the invariant-specific
provenance. It must not create a live revision. A pre-commit caller restores or
aborts as stated in Invariant 9. A publish-gate failure leaves the already
published revision and every session's current context unchanged. This uses the
existing identity mutation seam; no parallel validator or publisher is added.

For a valid publish candidate, the gateway creates or reads the
validation-publication marker keyed by the invocation and expected prior live
OID. Pre-commit validation records its candidate tree fingerprint; the publish
gate adds the exact candidate OID to that same marker. It records `pending` only after validation succeeds,
then calls the existing `Identity.publish_live!` live-ref move with that expected
prior OID, and finally marks the same record `accepted` through the existing
`AdminProjection.stamp_publication` path. Repeating the invocation reads the
same marker: an `accepted` marker is a no-op; a `denied` marker is immutable and
returns its recorded typed denial without validation, Git mutation, a new marker,
or a terminal-state transition; and a `pending` marker reconciles the live ref
before doing anything else. If the ref still equals the expected
prior OID, replay validates the same candidate, advances that ref, and finalizes
the marker. If the ref already equals the candidate OID, replay finalizes the
marker without moving Git again. Any other ref value finalizes the marker
`denied` with a typed publication-conflict cause and leaves the ref unchanged.
Thus a crash after `pending` but before the ref move replays the move, and a
crash after the ref move but before `accepted` finalizes the already-moved
candidate. The marker is the durable validation evidence only in a terminal
state.

### Stamps, status, and refresh

Provisioning writes the render stamp with the existing session identity stamp.
The session status projection reports the live expected revision, contract, and
digest for each session's archetype/harness and reports the stale reason(s):
`missing_render_stamp`, `revision_mismatch`, `contract_mismatch`, or
`guidance_digest_mismatch`. A legacy row with only a revision is stale.

New and reloaded sessions use the live render immediately. A resident session
keeps its existing context until `identity apply` reaches its existing safe turn
boundary. `identity relearn` publishes a new revision after validation; `identity
status` identifies stale sessions; `identity apply` provisions and stamps the
selected session with the new rendered bytes. These flows do not reset the
shared harness runtime.

### Gibson compatibility and cleanup

The `89a6879` inline mitigation remains in the Gibson identity until the first
installed `0.1.9` or `0.2.0` build whose changelog or release ledger names this
work item. Only then may Gibson replace the inline copies with directives.
Before replacement, cleanup compares each inline copy with the current
`specs-home.md` or `dev-on-gibson.md` fragment. The fragment file wins on any
divergence, and cleanup records the divergence and both digests. After cleanup,
completion evidence is a fetched served Gibson identity showing both rendered
sections and no literal include directive. Shrdlu has neither the includes nor
the inline copies and receives no cleanup action.

### Pattern and mutation seam

This establishes the **universal-root render contract** pattern. It applies to
identity snapshot, validation, publication, status, and refresh. It does not
apply to ad-hoc override recovery or arbitrary Markdown outside the identity
fragment catalog. The sole mutation seam is the existing identity seam; the
sole live pointer mutation remains publication of `tightbeam/live`.

## Acceptance

1. Given a candidate identity whose manual includes `specs-home.md` and whose
   model includes `dev-on-gibson.md`, when the same archetype is snapshotted for
   each supported harness, then each expected fragment byte sequence occurs in
   the delivered guidance, in directive position, and no delivered line begins
   `#include`.

2. Given a fixture copied from the current Gibson `specs-home.md` and
   `dev-on-gibson.md` bytes, when the fixture's universal roots include those
   files and a snapshot is served, then the expected byte sequences compare
   equal to the served sections; a test must read the fixture files rather than
   retype their prose.

3. Given archetype guidance that explicitly includes either universal root,
   when the snapshot is rendered, then that root's rendered content occurs once
   and the automatic append omits it. Given a normal fragment included twice,
   when rendered, then its content occurs twice at the two directive positions.
   Given each of a fixture with two direct occurrences of the same universal
   root and a fixture whose direct occurrence and ordinary-fragment path both
   reach that same root, when validation runs, then each rejects with
   `identity_include_invalid`, names both directive provenance paths and lines,
   and returns no partial guidance.

4. Given nested valid includes, when rendered, then the output preserves
   ordinary-line order. Given each of a malformed include-like line, a missing
   flat name, a path-bearing name, a universal root that includes a universal
   root, a cycle, an eleventh active include, or two fragment paths with one
   basename, when validation runs, then it rejects with
   `identity_include_invalid` and the required provenance and it returns no
   partial guidance.

5. Given an invalid fresh-init candidate, when init reaches validation, then no
   canonical identity directory, required identity ref, or initialization marker
   exists. Given a valid fresh-init candidate, when validation succeeds, then
   the canonical path first becomes visible with its complete required refs.
   Given an invalid candidate introduced through each other identity mutation
   class, when the operation reaches its commit boundary, then it reports denial,
   records one denied validation-publication marker containing the candidate tree
   fingerprint and no candidate commit OID, restores or aborts its stated reversible
   state, and preserves the prior `main` and `tightbeam/live` revisions. Given an invalid
   exact candidate at the publication gate, when publication is attempted, then
   `tightbeam/live` remains unchanged. Given a valid publication that crashes
   after its pending marker and before the live-ref move, when the same
   invocation replays, then it advances the expected ref once and leaves one
   accepted marker. Given a valid publication that crashes after the live-ref
   move and before marker acceptance, when the same invocation replays, then it
   does not move Git again and leaves that same marker accepted. Given a replay
   whose ref differs from both expected prior and candidate OIDs, when it
   reconciles, then it leaves the ref unchanged and records one denied marker
   with the typed conflict cause. Given that same denied marker, when the same
   invocation replays, then it returns the recorded typed denial without
   validation, Git mutation, a new marker, or a terminal-state transition.

6. Given an identity revision that is valid and published, when a session is
   provisioned, then its recorded revision, contract `universal-root-render-v1`,
   and SHA-256 equal the delivered guidance. Given a legacy, contract-mismatched,
   revision-mismatched, or digest-mismatched session row, when identity status
   is read, then it reports that row stale with the matching reason; when
   `identity apply` succeeds at a turn boundary, then it writes the live stamp.

7. Given Gibson still uses the `89a6879` inline mitigation, when no eligible
   fix-bearing build is installed, then cleanup does not edit that identity.
   Given the required build is installed and the two inline/fragment pairs
   diverge, when cleanup runs, then each fragment's bytes are retained and the
   divergence is recorded. Given cleanup completes, when an independent reader
   fetches the served Gibson identity, then it sees both named sections and no
   literal include directive.

8. Given the complete implementation and the deterministic tests above, when
   the relevant Tightbeam suite runs in an owned Gibson worktree at the proposed
   commit, then the run reports its baseline and after counts and has zero test
   failures.

## Open Questions

None. The work item's four load-bearing choices are ruled. Implementation may
choose internal data structures only when they preserve every invariant and
acceptance result in this spec.
