# Organization development mode v1

Status: proposed revision 4

Work item: `wi_cc890c75-4463-4a19-9c4a-166ac64a7558`

Product baseline: Tightbeam `7a70a2f616363074514237b5bee48ba67c52e2ea`

## Spirit

An organization that is testing Tightbeam itself must preserve Tightbeam failures as
evidence. Its agents must not hide a substrate defect behind an improvised workaround.
One visible organization setting must place that working regime in every served identity,
including identities served after the setting changes.

Development mode changes how agents handle suspected Tightbeam defects. It does not make
the substrate decide what is a defect. It does not authorize an external post. At the top
of an operational lineage, the agent must ask the user for explicit permission for each
proposed GitHub issue and must stop before posting it.

Normal operation remains unchanged when development mode is off.

## Goal

Add one typed organization setting, `development-mode`, that defaults to `off`. When it is
`on`, compose one canonical debugging-regime fragment into every materialized served
identity. Project the setting and each materialized session's actual setting revision in
list and readiness output. Use the existing identity-apply path to refresh present resident
sessions. Use the current setting when a future session first materializes its harness
context.

## Non-Goals

- Do not add a parallel policy store, failure detector, reporting tool, assignment type,
  issue poster, or all-session transaction.
- Do not infer that an observed failure is a Tightbeam defect.
- Do not change credentials, placement, topology, release, deployment, target selection,
  harness readiness, or the identity Git revision.
- Do not interrupt a running turn.
- Do not post a GitHub issue without explicit user permission for that exact issue.
- Do not preserve the legacy debugging-regime blocks defined below after the shipped
  development-mode fragment becomes their canonical replacement.

## Terms

- **Setting row**: the `org_settings` row whose key is `development-mode`.
- **Setting revision**: the setting row's collision-free `rowVersion` from the existing
  `admin_projection_versions` config projection. It advances once for each semantic value
  change. It is not `org_settings.updatedAt`.
- **Materialized session**: an active session for which the resident harness has loaded a
  served snapshot. A session without a harness context is not materialized.
- **Session setting stamp**: the setting revision and value used to compose the resident
  served snapshot that was successfully loaded for one materialized session.
- **Stale session**: a materialized active session whose setting stamp differs from the
  current setting revision.
- **Operational lineage**: the durable spawned-by session chain exposed by Tightbeam.
- **Active ancestor**: the nearest exposed session in that lineage that is active and can
  receive a Tightbeam message. An inactive or retired parent is not an active ancestor.
- **Top of lineage**: a session whose operational parent is itself or is not exposed.
- **Legacy debugging-regime block**: the section that starts with the exact heading
  `## Debugging regime (mike's standing directive, 2026-08-06, until revoked)` and ends at
  the next same-level heading or end of file. At rollout it exists in the live identity
  files `guidance/default.md`, `guidance/coder.md`, `guidance/reviewer.md`,
  `guidance/orchestrator.md`, `guidance/recon.md`, and `guidance/spec-writer.md`; its
  block includes the `Probe boundary (debugging regime)` paragraph.
- **Canonical development-mode fragment**: the product-shipped file
  `priv/guidance/development-mode.md`. It is the sole source of bytes appended by
  development-mode composition; the live organization identity does not copy it.
- **Secret-safe specimen**: a report that contains the failing action, refusal or error,
  identifiers, timestamps, and state-change result, but no credential or secret value.

## Assumptions

1. The existing config projection allocates `rowVersion` inside the same database
   transaction as a semantic setting change. SQLite serializes concurrent writers.
2. The existing identity-apply path can enter each resident session lane at a turn boundary
   and can leave a busy or failed session unchanged without claiming it is current.
3. `artifact-record` is available to an active session without an assignment and can
   preserve a report from that session's owned workdir.
4. Served-identity composition can read the setting value and config `rowVersion` together
   before it builds one session snapshot.

If any assumption is false at implementation time, stop and return the mismatch to product
ownership. Do not invent a replacement mechanism in code.

## Invariants

1. An absent setting is typed `off` with revision `0`.
2. A semantic setting change and its new config `rowVersion` commit atomically. An
   idempotent set advances neither.
3. A session stamp names only bytes that the resident harness successfully materialized.
4. A no-context session has no stamp and is never called stale or current.
5. Knowledge that a failure may be a Tightbeam defect remains agent judgment. The
   substrate neither classifies nor escalates it.
6. The canonical fragment occurs at most once in a served snapshot.
7. Development-mode state never changes the identity Git revision or runnable readiness.
8. No code path posts externally. Each proposed issue requires explicit user permission.
9. Turning the setting off removes the fragment from every subsequently materialized or
   successfully applied snapshot.

## Architecture

### Typed organization setting

The admin CLI accepts only:

```text
tightbeam config get development-mode
tightbeam config set development-mode on
tightbeam config set development-mode off
```

The value is the closed type `on | off`. An absent row means `off`. Any other value is an
`invalid_value` refusal and changes no durable state. The setting keeps the existing admin
authorization, organization-setting row, admin projection, and `config.updated` event.

`config get` and a successful `config set` return the canonical string value, typed boolean
`enabled`, and config `rowVersion` as `revision`. Repeating the current semantic value is
idempotent and does not advance the setting revision or emit a new event. Setting an absent
organization to `off` is a no-op with revision `0`.

`config set` does not reload sessions. Its database transaction linearizes concurrent
semantic sets, commits the setting value and next config `rowVersion`, and returns the
sorted materialized sessions whose stamps now differ, plus this existing remedy:

```text
tightbeam identity apply --all
```

This separation avoids an all-session lock and makes a config change durable even when a
session is running or an adapter is unavailable.

### One canonical guidance fragment

The product ships one guidance fragment. Served-identity composition appends it for every
archetype and supported harness only while the setting is on.

The canonical fragment uses directive role voice:

```text
# Development mode

This organization is testing Tightbeam itself.

When you judge that a Tightbeam substrate command, row lifecycle, adapter, or served-
identity mechanism has failed:

- Do not hide the failure with an ad hoc command, direct database or identity-file edit,
  duplicate work lane, or substitute mechanism.
- Record one secret-safe specimen. If you hold an assignment, file it on that assignment.
  If you hold no assignment and have an active ancestor, send the specimen to the nearest
  active ancestor for durable filing. If you hold no assignment and have no active
  ancestor, including when you are at the top of the operational lineage, write the
  specimen in your owned workdir and record it with `tightbeam artifact-record --kind
  report --title <title> --path <path>`. Add `--work-item <id>` when a work item exists.
- Include the exact command or action, the refusal or error, relevant identifiers and
  timestamps, and whether durable or live state changed. Do not include secrets.
- Continue work that is separable from the failed seam.
- When an active ancestor exists, report the specimen or its durable pointer to the nearest
  active ancestor. When none exists, the recorded artifact is the terminal internal route;
  do not address an inactive parent and do not create a second specimen merely to report it.
- If you are at the top of the operational lineage, prepare one proposed issue for the
  `clickety-clacks/tightbeam` GitHub repository. Ask the user for explicit permission for
  that issue. State the proposed title and secret-safe body. Do not post the issue until the
  user grants that per-issue permission.
```

This fragment teaches existing assignment attests, parent messages, `artifact-record`,
lineage, and user permission. It creates no automatic report, escalation, or GitHub action.

Before an organization first sets development mode to `on`, its rollout owner must remove
every legacy debugging-regime block from the six named live guidance files through the
existing identity edit and relearn process. The pre-enable check searches every
`guidance/*.md` blob reachable from the current `tightbeam/live` revision for both the exact
legacy heading and this exact line-wrapped byte marker, including its newline:

```text
A silent
workaround destroys the evidence this org exists to produce.
```

It refuses enablement while either marker remains anywhere in that search scope. It also
verifies that each installed archetype's fully expanded live guidance contains neither
marker, including content reached through `#include`.

This is a reviewed rollout prerequisite, not an automatic content migration. After
enablement, `priv/guidance/development-mode.md` is the sole byte source for the canonical
fragment. No file under the organization identity tree contains a copied canonical
fragment or a legacy block. The product's conditional composition appends the shipped file
at most once to each served snapshot.

### Present and future served identities

Every new served snapshot is composed from the current live identity revision and one
atomically read pair: development-mode value and config `rowVersion`. A future session
receives the current pair when its harness context first materializes.

A session writes its setting stamp only after its resident harness successfully loads the
composed snapshot. A session with no harness context has no stamp. It first obtains a stamp
when it materializes; no bounce is needed before then.

For present resident sessions, the rollout owner runs `tightbeam identity apply --all`.
For each session, the existing lane boundary reads the current setting pair, composes and
loads that session, and stamps only the pair actually loaded. A running session yields the
existing `turn_in_progress` result and keeps its prior truthful stamp. An adapter load
failure keeps the prior stamp and yields the existing apply failure. Sessions successfully
loaded earlier in the same command keep their new truthful stamps.

A concurrent `config set` may cause one apply command to materialize different revisions
across sessions. This is allowed and truthful. Each session stamps the pair it loaded, and
list/readiness exposes every materialized stamp that is not equal to the final current
revision. A later `identity apply --all` closes the gap. No operation claims atomic
all-session projection.

Turning the setting off follows the same setting and apply paths. A turn already in
progress keeps the identity with which it started.

### Conspicuous truth projections

`tightbeam list` adds a top-level `developmentMode` object:

```json
{
  "enabled": true,
  "value": "on",
  "revision": 3,
  "staleSessions": ["agent:materialized-example"],
  "unmaterializedSessions": ["agent:not-started-example"]
}
```

`staleSessions` contains only materialized active sessions whose stamp differs from the
current revision. `unmaterializedSessions` contains active sessions with no resident
harness context and no stamp. Both arrays are deterministic and sorted. Neither list calls
an unmaterialized session stale or current.

Readiness summary data exposes the same `development_mode` object. Human readiness output
adds this conspicuous line whenever the setting is on, for READY and NOT READY states:

```text
DEVELOPMENT MODE ON: served identities preserve Tightbeam failures as specimens; GitHub
issues require explicit user permission per issue.
```

When stale materialized sessions exist, readiness immediately follows it with:

```text
DEVELOPMENT MODE INCOMPLETE: <n> materialized session(s) need identity apply.
```

Development mode, stale sessions, and unmaterialized sessions do not change harness
runnable readiness. They are conspicuous operating state, not boot gates.

## Acceptance

The implementation must prove:

1. An absent setting reads as typed off with revision `0` and changes no existing served
   guidance or readiness verdict.
2. Only exact `on` and `off` values are accepted. Invalid and unauthorized writes leave
   the setting and session stamps unchanged.
3. Each semantic transition advances config `rowVersion` exactly once. Two opposite writes
   forced into the same millisecond receive distinct revisions. An idempotent set advances
   neither the revision nor the config event.
4. Concurrent set/set operations serialize to one final value and distinct revisions.
   Config set never reloads a session and returns sorted stale materialized sessions with
   the existing `identity apply --all` remedy.
5. With mode on, snapshots for every installed archetype and supported harness contain the
   canonical fragment exactly once. With mode off, none contain it.
6. A materialized session stamps only the setting pair whose bytes loaded successfully.
   A no-context session has no stamp, appears only in `unmaterializedSessions`, and stamps
   the then-current pair on first materialization without a prior bounce.
7. Identity apply enters each resident session lane. Running and adapter-failed sessions
   keep prior stamps. Successfully loaded sessions advance. A set/apply race may yield
   mixed truthful stamps, and list/readiness reports the exact stale remainder.
8. List and readiness expose on, off, stale-materialized, and unmaterialized states in
   deterministic sorted order without changing runnable readiness.
9. An assigned agent can attest a secret-safe specimen. An unassigned session with an
   active ancestor sends one to the nearest active ancestor. An unassigned session with no
   active ancestor, whether top-lineage or stranded below an inactive parent, preserves one
   through the real `artifact-record` command. The artifact remains durable when the user
   denies or has not answered issue permission. Reporting is required only when an active
   ancestor exists.
10. The fragment requires explicit user permission for each proposed top-lineage GitHub
    issue. No code path posts externally.
11. The rollout test begins with the legacy block in each of the six named live guidance
    files. Enablement refuses until identity edit and relearn remove every block. It searches
    all `guidance/*.md` blobs and fully expanded installed-archetype guidance for the exact
    heading and exact line-wrapped byte marker defined above. After removal, it proves
    `priv/guidance/development-mode.md` is the sole source, no organization-identity copy
    exists, and each mode-on snapshot contains its bytes once.
12. Existing identity status/apply behavior and identity Git revision truth remain intact.

Run focused config, identity, list, readiness, same-millisecond collision, set/set,
set/apply, no-context, partial-failure, specimen-path, and one-home tests. Then run the full
Elixir and Rust gates. Keep product work on a pushed non-main branch and submit its exact
revision for independent code review. The work item remains untargeted.

## Open Questions

None. If implementation disproves an assumption, return that concrete mismatch to product
ownership before changing the mechanism.

## Spec-homing

This file is the canonical capability spec in the `tightbeam-specs` repository. Product
code and rollout guidance may point to it; they must not restate its policy in another
home. Any later change follows independent spec review before code custody opens.
