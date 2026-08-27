# Notice batching V2 — opt-in agent-message eligibility amendment

Status: FROZEN FOR OWNER-OPENED INDEPENDENT REVIEW

Canonical base: `notice-batching-v1.md` at reviewed-clean commit
`fa7836e464d7b94b566d63ce1031ff1f37f8a81e` (SHA-256
`a1a6deadce7d49dfa996e637a9bba9a12e1bff31e6883612666c38669ed6e00c`).

Authority: Mike order `art_516d07ed` (SHA-256
`a8c0598e3df1113c1788de77cabe272b05a2875aa58e6a23a2bfed04652132b3`).

## Goal

V2 makes an agent-to-agent source message envelope-eligible solely when it has
the sender's durable `class=information` marker.

## Non-Goals

- V2 incorporates the V1 base unchanged and restates no V1 rule.
- V2 leaves user messages, untagged agent messages, and interrupt-class agent
  messages on their existing pass-through paths.
- V2 leaves V1 eligibility for source notices that are not agent-to-agent
  messages unchanged.
- V2 adds no inference, adoption gate, target, API, implementation, or runtime
  mutation.

## Terms

- **Agent-to-agent message** — a durable source message whose existing sender
  and recipient principal kinds are agents.
- **Information marker** — `class=information` written with the authenticated
  sender by the existing Phase 1 `wake --class information` seam.
- **V2-eligible message** — an agent-to-agent message with an information marker.

## Assumptions

1. Phase 1 preserves the information marker and its sender provenance on the
   durable source row before V1 evaluates envelope eligibility.
2. V1 supplies the routine envelope lane for a V2-eligible message.

## Invariants

1. The V1 batcher admits a V2-eligible message through this added alternative,
   then applies the existing V1 `fyi` envelope mechanics without changing its
   source-row class marker.
2. The batcher sends an agent-to-agent message without an information marker,
   including an interrupt or another explicit class, through its pre-V2 path.
3. The batcher reads the marker and sender provenance from the durable source
   row; it does not infer eligibility from payload text or a caller override.

## Architecture

After Phase 1 persists an agent-to-agent source row, V2 evaluates its durable
marker before V1 eligibility. `class=information` invokes the unchanged V1 batch
seam and routine lane. Each other state uses the existing pass-through path. V1
owns the resulting envelope and later edges.

## Acceptance

1. Given an agent sender uses `wake --class information` to an agent recipient,
   when Phase 1 persists the row, then V1 creates one member and retains the
   source's information marker and sender provenance.
2. Given an agent message without `--class information`, or with
   `--class fyi`, when it is persisted, then its pre-V2 delivery path receives
   it and no V1 batch member exists.
3. Given an agent message with an interrupt class, when it is persisted, then
   its pre-V2 delivery path receives it and no V1 batch member exists.
4. Given a source row whose marker or marker provenance is missing, when V2
   evaluates it, then V2 creates no member and leaves the source row unchanged.

## Open Questions

None. Kungfu teaching line, non-blocking: POs, patrols, and orchestrators tag a
routine agent report with `wake --class information` for opt-in eligibility. Seven-day
basis: agent traffic 54%; 80% in same-class floods above 10 per day; opt-in tags
address roughly 12,000 weekly flood turns.
