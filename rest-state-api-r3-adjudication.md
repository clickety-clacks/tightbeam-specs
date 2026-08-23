# REST state API r3 — durable adjudication ledger

Status: normative adjudication companion for canonical r3, 2026-08-22;
updated 2026-08-23 for SQ4.

This file makes the REST findings inspectable in the canonical spec set. The
short `review-gate-observability-2026-08-21.md` routes ownership but does not
contain the finding bodies.

## Source identity

- Mike dispatch message `s_db3f12e6-d69d-45aa-94ba-b88d2baf9e69` assigns
  REST findings F1, F8, F9, F13, F14, F16, F21, and F22 and requires alignment
  with firehose r6 V4a, R8, and R9.
- Mike charter message `s_a1b7f24f-334c-4487-a83f-09317be412a5` preserves
  review-before-land and removes the extra blessing step for mechanical doc
  iteration.
- Operator decision `dr_bd47c1d7-23bb-4c47-a93c-23f663db356a` rules SQ2
  “Expose all admin reads.” Its ruling adds first-class archetype, kungfu,
  rail, and guidance content to the admin-only read set.
- Exact r3 review `att_71210c7b-a2cc-4b11-98fb-e7e264d78a6f` and report
  `art_9e7e568a`, SHA-256
  `ca57a6fa1f038f91fd8ea21549a7f6c3ff6c67c1c0497c8048c55e43c731799e`,
  identify the first revision's closure gaps.
- Superseding companion ruling `art_4a1cce6e`, SHA-256
  `5db8aab3496747d008fb8c024a4f1617f92695d144c89481bca3a1f20842550a`,
  adopts both missing firehose mappings and supersedes fact-only
  `art_5d8bacb2`.
- Joint successor review `att_45676d30` is reviewed-clean. Canonical merge
  `c84b1b8dc856861baeaa7b5ff781317ded568cb1` lands the exact reviewed REST
  bytes.
- Mike's SQ4 ruling `dr_96055b44-b18b-47b6-81f8-f2d64f709a2a` selects
  REST-first: M2 REST provides rebuildable state before the M3 firehose adds
  freshness. It changes sequencing only.

## Assigned findings and required effect

| Finding | Required REST effect | Normative closure |
|---|---|---|
| F1 | Per-resource projection fields are normative, not examples. | Main spec R7/R7a fixes exact top-level keys; the wire-schema companion fixes types, nullability, nested keys, enums, and ordering. |
| F8 | Cursors encode the complete immutable ordering tuple and never a live row id. | T3 and R5/R5a bind opaque cursors to immutable tuples and reject `rowid`, offsets, and live-row resolution. |
| F9 | Read markers use composite identity and lossless pagination. | R5a/R5b use `(userId, scopeKey)` for identity and order; A9 proves collision-free paging. |
| F13 | Visibility runs before subscription filters. | AU6 fixes the order for upsert and delete; A11 proves the filter matcher is not invoked for hidden rows. |
| F14 | Visibility is an explicit per-resource allow matrix. | AU4 is closed-world; A10 tests every allow row and an owner-related denied session. |
| F16 | Safe values use an explicit allowlist and default deny. | SR5 exposes only `default-archetype`; other config values and all host-environment values are null. SR6 separately bounds ruled admin content. |
| F21 | Nested resources and `/download` apply visibility at every hop and use the same 404. | AU5 authorizes parent, child, and asset metadata before bytes; A12 tests both denied-hop directions and no byte open. |
| F22 | A session token is session-scoped by default. Owner reads exist only where a spec grants them. | AU1 and AU4 separate session from user authority; A15 proves no owner or admin-bit borrowing. |
| V4a | Stored projections carry a monotonic version for last-version-wins application. | R7, R10, SR4, and A4 define version allocation through delete and recreation. |
| R8 seed | Each state mutation maps to resource, op, primary refs, serializer, and visibility. | Main spec R8 and A1 own the mapping seed. |
| R9 dependencies | Every composed view enumerates the state classes that invalidate it. | Main spec R9 and A14 own the closed dependency lists and digest proof. |

## Review-round closure map

The first exact r3 review found ten defects. F1–F3 and F5–F10 are corrected
inside the REST r3 set. Review F4 exposed absent companion state classes for
facts; the same audit exposed critical-lease state. `art_4a1cce6e` adopts both
R8 rows with no conflict. The firehose registry amendment must land with this
REST set; no implementation may start while either canonical spec omits its
side.

| Review finding | Successor closure |
|---|---|
| F1 missing structure | Main spec adds Spec homing, Goal, Non-goals, Assumptions, Invariants, Architecture, and an Open Questions register with blocking labels. |
| F2 incomplete resources and schemas | R3, R5a, R6, R7, R7c, and the wire-schema companion complete facts, critical state, bounded-time filters, and every item type. |
| F3 mutable cursors | R5a orders host environment by `(host,harness,name)` and read markers by `(userId,scopeKey)`; A5 mutates rows during paging. |
| F4 missing fact notice | R8 and A18 require `condition_fact.filed`; `art_4a1cce6e` adopts it and `critical_lease.updated` with shared serializers, visibility, commit timing, and versions. |
| F5 config contradiction | SR5 keeps every live key as admin metadata with `value:null` unless allowlisted; A13 requires the identical notice item. |
| F6 version incarnation | R10 gives versions resource-key lifetime across delete, restart, and recreation; A4 proves the same-name role case. |
| F7 unsafe admin content | SR6 fixes source paths, allowed kungfu documents, path grammar, redaction, and shared sanitized bytes; A16 supplies hostile fixtures. |
| F8 missing provenance | This file carries the finding text, exact source message ids, decision id, review ids, and closure map in the candidate canonical set. |
| F9 cursor and timing ambiguity | AU7 fixes error precedence and principal binding; AU8 defines a measurable in-process timing class; A6 tests each case. |
| F10 nondeterministic nested data | The wire-schema companion fixes nested keys, enums, nullability, object-key order, array order, serializer bytes, and dependency digest input; A17 randomizes source order. |

## Joint REST and firehose review disposition

The exact-revision joint review `att_8580ca4f` and immutable report
`art_4301a934` found three remaining cross-plane defects in REST commit
`72b1f9b` and firehose commit `c4eb42e`.

| Finding | Mechanical disposition |
|---|---|
| J1 resource-name conflict | REST R8 now uses the authority's exact `condition facts` firehose resource value and states that `/api/facts` is the route for that resource. |
| J2 `factId` type conflict | R8, SR4, A18, and the wire schema make item `id`, notice `refs.factId`, and `rowVersion` positive JSON integers with equal numeric values; decimal strings are invalid. |
| J3 A1/A6 authority-proof gap | REST A18 proves shared AU4 authorization and per-resource last-version-wins behavior for both companion classes. The matching firehose successor must make its A1/A6 proof and both R8 coverage cells explicit before joint review. |

This ledger records authority and required effects. It does not replace the
main product contract, the wire schema, or the firehose registry.
