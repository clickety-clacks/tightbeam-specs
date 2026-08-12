# Tightbeam release maintenance lines

Status: implementation contract, 2026-08-11

## Goal

Allow a supported minor line to receive reviewed patches and cut immutable version-tag
releases while `main` advances toward a newer minor line. Preserve the normal release flow:
reviewed feature commits land on `main`, CI packages the exact `main` commit, and a version
tag publishes those exact bytes.

## Contract

1. `main` remains the default development and release source.
2. A concurrent maintenance line is named exactly `release/<major>.<minor>`, for example
   `release/0.1`. Release branches are not candidate branches and are not used when `main`
   is still the source of that release line.
3. CI runs the unchanged Linux and macOS tests on pull requests. It runs those tests and the
   package jobs on pushes to `main`, pushes to `release/*.*`, and
   `v<major>.<minor>.<patch>` tags. Branch pushes produce retained workflow artifacts but
   never a GitHub Release.
4. A version tag is eligible when all of these are true:
   - its name exactly matches `v<major>.<minor>.<patch>`;
   - it matches the version in `cli/Cargo.toml`; and
   - its commit is the current tip of `origin/main`; or
   - `origin/main`'s Cargo major/minor has advanced beyond that tag's line and its commit is
     the current tip of the matching `origin/release/<major>.<minor>` branch.
   No other release branch can authorize the tag. A missing matching maintenance branch is
   ordinary: the tag must then be the current `origin/main` tip.
5. Tag CI reruns the unchanged cross-platform gates and packages the tag's exact SHA before
   publishing. Existing checksum and provenance behavior is unchanged.
   GitHub immutable releases must be enabled for this repository before another release is
   cut; after publication GitHub locks both the release assets and its associated tag.
6. Patches enter a maintenance line through the same independent review discipline used for
   changes entering `main`. This change does not create a second release-candidate branch,
   a new review mechanism, automatic backports, or branch creation/deletion policy.

## Acceptance checks

- `v0.1.8` at `origin/main` tip with Cargo version `0.1.8` is eligible.
- `v0.1.8` at `origin/release/0.1` tip with Cargo version `0.1.8` is eligible even when
  `origin/main` has advanced to a different major/minor line.
- The same maintenance tag is refused while `origin/main` still carries Cargo line `0.1`.
- The same tag is refused at `origin/release/0.2`, behind the matching maintenance tip, or
  at an arbitrary commit.
- A push to `release/0.1` runs the same test/package matrix as a push to `main` and does not
  publish a GitHub Release.

## Non-goals

- Using a release branch as the normal candidate path.
- Allowing a tag from any branch that happens to contain its commit.
- Changing package contents, supported platforms, checksums, provenance, or deployment.
