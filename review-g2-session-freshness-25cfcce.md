# Independent G2 F1-successor specification review

Verdict: **REVIEWED CLEAN**

Reviewed assignment: `asg_f743e40c-903f-47ca-be4e-68c2eee532fe`  
Review assignment: `asg_053a1329-d51d-43a7-8dab-be5e161d6d8b`  
Exact candidate: `25cfcce494bafd3c66dc2d7954200cfb28d222f1`  
Reviewed at: 2026-08-27 00:11 PT

This verdict is bound only to the exact candidate above. It does not authorize a
target, landing, implementation, merge, deploy, or release.

## Evidence boundary

- A new reviewer-owned clone fetched the canonical remote. Remote branch
  `spec/firehose-g2-session-freshness` resolves exactly to
  `25cfcce494bafd3c66dc2d7954200cfb28d222f1`.
- The candidate parent is exactly the previously reviewed commit
  `99881b02e46222498dfcb09feb5ce2d86c127db7`.
- The successor changes exactly `event-firehose-v1.md`,
  `rest-state-api-v1.md`, and `rest-state-api-v1-wire-schema.md` from that
  parent. The delta is 55 insertions and 12 deletions, and
  `git diff --check 99881b02 25cfcce` passes.
- Exact file SHA-256 values match `art_619cf5c6`:
  - `event-firehose-v1.md`:
    `da9b36717050053f2d15669db8f43353475c3608f3b48eb9baf680bfd721835a`
  - `rest-state-api-v1.md`:
    `853b11b885ccff2070aa1463ee2fbc65d32c04636964a76295edb1dcf15b42ed`
  - `rest-state-api-v1-wire-schema.md`:
    `1729c7864904524150afa2983b3999627be8bcd18b0a7c3f977fc51752b9061a`
- The complete three-file successor was reread. The prior exact-commit verdict
  `att_bb77ae81-d433-4cc4-891b-e359ff837687`, immutable report
  `art_c35b0568`, and product-owner disposition
  `att_3218fa0a-975d-40a3-a9b8-8839373f51f0` were reread from durable state.
- The prior report file independently hashes to
  `94a7ebd2b7c4cf45216d81b3505d2982e4af5ac46096ef7e055661f1ac7459af`,
  matching its artifact evidence.
- The repository contains no root `AGENTS.md`, `CLAUDE.md`, or
  `CONTRIBUTING.md` at this commit.

This is a specification-only review. Product tests and a `tests-passed` receipt
belong to the later implementation card under REST SQ8. These checks prove
candidate custody, exact text integrity, and specification decidability. They
do not claim implementation behavior.

## F1 successor disposition

The successor closes the sole prior blocker without changing another reviewed
outcome.

- Firehose T8 and REST I9 name the existing shared
  `Tightbeam.Gateway.session_status/2` `run.state` projection.
- T8, I9, and the wire companion close `mechanicalStatus` to exactly `idle` and
  `running`. Its sole mutable input is the committed count of the session's turn
  rows whose status is `queued` or `running`.
- Zero maps to `idle`; positive maps to `running`. Only a zero-to-positive or
  positive-to-zero crossing changes the session item.
- REST I10 and the wire companion require the crossing transaction to store the
  changed status and next session `rowVersion` atomically before post-commit
  notice publication. Positive-to-positive changes are silent at the session
  seam.
- REST A40/A40a and firehose A1 finitely cover `0→1`, `1→0`, `1→2`,
  `2→1`, `queued→running`, and outside-set to outside-set changes. They also
  reject a bypassing turn writer, direct session writer, extra input, extra
  value, or read-time derivation.

The exact successor diff confines every changed clause to that F1 closure. It
adds no resource, route, field, serializer, credential, grant, error shape,
write contract, replay mechanism, target, or release authority.

## Clause table

| Clause / required outcome | Status | Evidence |
|---|---|---|
| Exact successor custody, parentage, three hashes, and three-file homing | satisfied | Remote tip, exact parent, hashes, name-status, and diff check verified; firehose spec homing 85-96; REST spec homing 105-119. |
| F1-only delta from reviewed `99881b02` | satisfied | Exact parent-to-successor diff changes only T8/A1, I9-I10/architecture/A40-A40a, and the matching wire rule. |
| Existing shared status seam; no second projection | satisfied | Firehose T8 223-227; REST I9 196-201 and architecture 220-225. |
| Sole committed mutable input | satisfied | T8 223-227; I9 196-201; wire 23-32 name only the committed qualifying-turn count and reject any other input. |
| Closed value domain and exact mapping | satisfied | `idle` iff count is zero; `running` iff positive; no other value is valid in T8, I9, and wire 26-29. |
| Exact crossing behavior | satisfied | REST I10 203-209 and A40 1432-1438 cover zero-to-positive and positive-to-zero transitions. |
| Atomic item/version publication | satisfied | I10 208-209; R8 778-787; A36 1408-1416; wire 23-31. The stored item and greater version precede the exact post-commit notice. |
| No-change silence | satisfied | I10 206-207; R8 784-785; A36a; A40/A40a. Positive-to-positive and outside-set changes do not advance session bytes or emit a session notice. |
| Finite A40/A40a completeness | satisfied | A40 covers both crossings and multi-turn `1→2`/`2→1`; A40a covers `queued→running`, outside-to-outside, bypass, extra input/value, and read-time derivation. |
| Additive `session.updated`; no second resource shape | satisfied | Firehose R3/R8 and REST R8 keep the one `sessions` resource, `upsert` operation, and exact R7 serializer. |
| Exact event-to-row correlation | satisfied | R8 maps equal `refs.sessionKey`, payload `sessionKey`, and REST `sessionKey`; A6/A36 enforce byte identity and correlation. |
| Last-version-wins convergence and deduplication | satisfied | Firehose V4a/M1/A4/A6 and REST SR4/A4/A37 apply `(sessionKey,rowVersion)` in either arrival order. |
| Spawn/update/retire selection and soft-retire behavior | satisfied | Firehose R8/A1; REST R8/A35-A36a. One changed item selects one class; unchanged bytes select none. |
| Cold-start and paginated read authority | satisfied | REST R2/R5/R5a preserve `GET /api/sessions` and `(createdAt,sessionKey)` keyset pagination; firehose AS3/M1/A4 rebuild from it. |
| Reconnect and detected-gap recovery | satisfied | Firehose P3/M2/D1b/A5 and REST A38-A39 use the single resubscribe-before-snapshot path. |
| Retention and history authority | satisfied / G5 out of scope | Firehose N1-N3 retain no socket replay, event storage, or notice retention. The successor changes no transcript pagination or history barrier. |
| Authentication, visibility, filters, and denied-row behavior | satisfied | Existing in-band firehose auth and REST AU1-AU7 remain unchanged; session classes reuse AU4 visibility before filtering. |
| Errors, protocol, and compatibility | satisfied / G4 out of scope | No route, protocol version, close code, error envelope, compatibility alias, or public field changes. |
| Shared serializers and settled wire behavior | satisfied | Firehose V3/R8/A6, REST I4/R7/SR1/SR4/A36, and wire 23-43 preserve one stored R7 item and serializer across REST and notices. |
| Deterministic acceptance | satisfied | Firehose A1/A3-A6 and REST A35-A40a decide class selection, correlation, convergence, crossings, silence, and bypass rejection. |
| G2-only scope and YAGNI | satisfied | The exact diff contains only the authorized F1 repair and no product code, target, merge, deploy, or release action. |

## Verdict

No blocking or non-blocking finding remains. The exact successor
`25cfcce494bafd3c66dc2d7954200cfb28d222f1` is reviewed-clean for the assigned
G2 F1-successor specification gate.
