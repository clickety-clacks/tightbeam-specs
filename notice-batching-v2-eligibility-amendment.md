# Notice batching V2 — opt-in agent-message eligibility amendment

Status: FROZEN FOR OWNER-OPENED INDEPENDENT RE-REVIEW

Canonical base: `notice-batching-v1.md` at reviewed-clean commit
`fa7836e464d7b94b566d63ce1031ff1f37f8a81e` (SHA-256
`a1a6deadce7d49dfa996e637a9bba9a12e1bff31e6883612666c38669ed6e00c`).

Authority: Mike order `art_516d07ed` (SHA-256
`a8c0598e3df1113c1788de77cabe272b05a2875aa58e6a23a2bfed04652132b3`).

## Goal

V2 makes an agent-to-agent source message envelope-eligible only with the
sender's durable `class=information` marker.

## Spec-homing

The canonical V2 set is `notice-batching-v1.md` at the reviewed-clean commit
and SHA above, followed by this canonical amendment. V2 supersedes only V1
eligibility for agent-to-agent messages. An owner re-review binds this file's
frozen content hash with the named V1 base; consumers use that pair, not a
filename alone.

## Non-Goals

- V2 retains all V1 text and mechanics.
- User, untagged agent, and interrupt-class messages retain their pass-through paths.
- V1 eligibility for source notices that are not agent-to-agent messages is unchanged.
- V2 adds no inference, adoption gate, target, API, implementation, or runtime
  mutation.

## Terms

- **Agent-to-agent message** — a durable source message with agent sender and recipient principals.
- **Information marker** — `class=information`, with authenticated sender provenance, from Phase 1 `wake --class information`.
- **V2-eligible message** — an agent-to-agent message with an information marker.

## Assumptions

1. Phase 1 preserves the marker and sender provenance on the durable source row before V1 eligibility.
2. V1 supplies the routine envelope lane for a V2-eligible message.

## Invariants

1. The V1 batcher admits a V2-eligible message through this alternative, then applies unchanged V1 `fyi` mechanics without changing its source-row class marker.
2. An agent-to-agent message without the marker, including interrupt or another explicit class, uses its pre-V2 path.
3. The batcher reads the durable row's marker and sender provenance; never payload text or caller override.

## Architecture

After Phase 1 persists an agent-to-agent source row, V2 evaluates its marker
before V1 eligibility. `class=information` invokes the unchanged V1 batch seam
and routine lane. Every other state uses its pass-through path. V1 owns the
resulting envelope and later edges.

## Acceptance

1. Given an agent sender uses `wake --class information` to an agent recipient, when Phase 1 persists the row, then V1 creates one member and retains marker and sender provenance.
2. Given an agent message without `--class information`, or with `--class fyi`, when persisted, then its pre-V2 path receives it and no V1 batch member exists.
3. Given an agent message with an interrupt class, when persisted, then its pre-V2 path receives it and no V1 batch member exists.
4. Given a source row missing its marker or marker provenance, when V2 evaluates it, then V2 creates no member and leaves the row unchanged.

## Open Questions

None. Kungfu teaching line, non-blocking: POs, patrols, and orchestrators tag routine agent reports with `wake --class information` for opt-in eligibility. Seven-day basis: agent traffic 54%; 80% in same-class floods above 10/day; opt-in tags address roughly 12,000 weekly flood turns.
