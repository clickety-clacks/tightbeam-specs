# Organization development mode v1

Status: proposed

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

## Product boundary

This feature uses the existing organization-setting, served-identity, identity-apply,
readiness, and list seams. It adds no parallel policy store, failure detector, reporting
tool, assignment type, or external-posting mechanism.

It does not change credentials, placement, topology, release, deployment, or target
selection. It does not interrupt a running turn. It does not infer that any observed
failure is a Tightbeam defect.

## Typed organization setting

The canonical key is `development-mode`.

The admin CLI accepts only:

```text
tightbeam config get development-mode
tightbeam config set development-mode on
tightbeam config set development-mode off
```

The value is the closed type `on | off`. An absent row means `off`. Any other value is an
`invalid_value` refusal and changes no durable state. The setting keeps the existing admin
authorization, organization-setting row, admin projection, and `config.updated` event.

`config get` and a successful `config set` return the canonical string value and the typed
boolean `enabled`. Repeating the current semantic value is idempotent and does not advance
the setting revision or refresh identities. In particular, setting an absent/default-off
organization to `off` is a no-op.

Each semantic change has one durable setting revision. The existing `updatedAt` value of
the canonical organization-setting row is that revision. The absent/default-off revision
is `0`.

## One canonical guidance fragment

The product ships one guidance fragment. It does not edit an archetype, learned identity,
or user repository. Served-identity composition appends the fragment for every archetype
and every harness only while the setting is on.

The canonical fragment uses directive role voice:

```text
# Development mode

This organization is testing Tightbeam itself.

When you judge that a Tightbeam substrate command, row lifecycle, adapter, or served-
identity mechanism has failed:

- Do not hide the failure with an ad hoc command, direct database or identity-file edit,
  duplicate work lane, or substitute mechanism.
- Record one durable, secret-safe specimen on your current assignment. Include the exact
  command or action, the refusal or error, relevant identifiers and timestamps, and whether
  durable or live state changed. If you have no assignment, do not invent one; send the
  secret-safe specimen to the session that spawned you or the nearest active parent for
  durable filing.
- Continue work that is separable from the failed seam.
- Report the specimen to the session that spawned you or the nearest active parent in your
  operational lineage. Do not create a second specimen merely to report it.
- If you are at the top of the operational lineage (your operational parent is yourself or
  no parent is exposed), prepare one proposed issue for the
  `clickety-clacks/tightbeam` GitHub repository. Ask the user for explicit permission for
  that issue. State the proposed title and secret-safe body. Do not post the issue until the
  user grants that per-issue permission.
```

The fragment teaches judgment and use of existing assignments, attests, lineage, and user
decision mechanisms. It creates no automatic report, escalation, or GitHub action.

## Present and future served identities

Every served snapshot is composed from the current live identity revision and the current
development-mode setting. A future or not-yet-started session therefore receives the
current setting when its harness context first materializes.

Every session stamps the development-mode setting revision that its resident served
snapshot actually materialized. A session with no harness context may stamp the current
revision without a bounce because its first materialization reads the current setting.
This stamp is separate from `identityRevision`; a configuration transition must not pretend
that the identity Git revision changed.

A semantic setting change invokes the existing apply-all turn-boundary path. The path
recomposes and reloads each active resident session from the current identity revision and
the new setting, then advances that session's development-mode stamp only after the load
succeeds. It never reloads a running turn.

If any selected session has a running turn, the setting change is refused with
`turn_in_progress` before the setting row changes. The response names the blocking session
keys. The caller can retry at a turn boundary.

If an adapter load fails after the setting row changes, the setting remains authoritative.
The response is `apply_failed`, names every session not proven current, and does not claim
complete projection. Successfully reloaded sessions keep their truthful stamps. A later
`identity apply --all` uses the same composition and closes the gap.

Turning the setting off follows the same path and removes the fragment. An agent turn that
already started keeps the identity with which it started.

## Conspicuous truth projections

`tightbeam list` adds a top-level `developmentMode` object:

```json
{
  "enabled": true,
  "value": "on",
  "revision": 1780000000000,
  "staleSessions": ["agent:example"]
}
```

`staleSessions` contains active sessions whose stamped setting revision differs from the
current setting revision. It is deterministic and sorted. It is empty when all active
sessions are current. The default-off/absent revision and an absent session stamp both
normalize to `0`.

Readiness summary data exposes the same `development_mode` object. Human readiness output
adds this conspicuous line whenever the setting is on, for both READY and NOT READY states:

```text
DEVELOPMENT MODE ON: served identities preserve Tightbeam failures as specimens; GitHub
issues require explicit user permission per issue.
```

When stale sessions exist, readiness immediately follows it with:

```text
DEVELOPMENT MODE INCOMPLETE: <n> active session(s) have not materialized this setting.
```

Development mode and projection staleness do not change harness runnable readiness. They
are conspicuous operating state, not a boot gate.

## Acceptance

The implementation must prove:

1. An absent setting reads as typed off with revision `0` and changes no existing guidance,
   list behavior beyond the typed off projection, or readiness verdict.
2. Only exact `on` and `off` values are accepted. Invalid and unauthorized writes leave the
   setting and session stamps unchanged.
3. A semantic change produces one organization-setting revision and one existing config
   projection/event. An idempotent set produces neither.
4. With mode on, snapshots for every installed archetype and supported harness contain the
   canonical fragment exactly once. With mode off, none contain it.
5. Active idle sessions are refreshed through the existing apply seam on both on and off
   transitions. Not-yet-started sessions materialize the current mode without an unnecessary
   harness bounce.
6. A running turn causes a pre-write `turn_in_progress` refusal. A later adapter failure
   leaves truthful per-session stamps and exposes the incomplete projection.
7. List and readiness expose on, off, complete, and incomplete states deterministically.
8. The fragment requires a secret-safe specimen, lineage reporting, and explicit user
   permission for each proposed top-of-lineage GitHub issue. No code path posts externally.
9. Existing identity status/apply behavior and identity Git revision truth remain intact.

Run the full Elixir and Rust gates after focused config, identity, list, and readiness tests.
Keep the product work on a pushed non-main branch and submit its exact revision for an
independent code review. The work item remains untargeted.
