# Independent G2 session-freshness specification review

Verdict: **CHANGES REQUESTED**

Reviewed assignment: `asg_f743e40c-903f-47ca-be4e-68c2eee532fe`  
Review assignment: `asg_5d445c30-97f2-43cf-adf7-64e454168d15`  
Exact candidate: `99881b02e46222498dfcb09feb5ce2d86c127db7`  
Reviewed at: 2026-08-26 23:44 PT

This verdict is bound only to the exact candidate above. It does not authorize a
target, landing, implementation, merge, deploy, or release.

## Evidence boundary

- A new reviewer-owned clone fetched the canonical remote. Remote branch
  `spec/firehose-g2-session-freshness` resolves exactly to `99881b02e46222498dfcb09feb5ce2d86c127db7`.
- The candidate parent and current remote `main` are both
  `2669ab73152193bf0a7f6d7e8f1906142bbed35b`.
- The commit changes exactly `event-firehose-v1.md`, `rest-state-api-v1.md`, and
  `rest-state-api-v1-wire-schema.md`. `git diff --check 99881b02^ 99881b02`
  passes.
- Exact file SHA-256 values match `art_0613b42a`:
  - `event-firehose-v1.md`:
    `fa645f2e77f44abe674c81b0a64d426ce684b0d775cd0f46294f0d5a6b7d7f50`
  - `rest-state-api-v1.md`:
    `29e28f7c32d0a199005f3c1a53e2b076da0e00ae6e560acaa954ca666ae995a8`
  - `rest-state-api-v1-wire-schema.md`:
    `0b5cd5588fe0f6171e745256fbf46da8f57f242c8564b52b436c5d91c0e335e2`
- `art_42acf5d4` points to the same event-spec bytes and exact remote commit.
- Recon report `art_1d389e8e` was read from its archived immutable carrier and
  independently hashed to
  `dcca35c06a4de8bd640fd74c712b95dd2ee6aec34526706c55cac09a0f3f1161`.
  Recon verdict `att_556f55ae-f1d2-4c83-b55d-9daf06aae929` was read from the
  closed recon assignment.
- Mike's exact ruling message
  `s_fe001c27-c509-4cf6-8866-47defe5eaa21` accepts recon G2 as a read-side
  firehose prerequisite: sessions enter the freshness mapping. It leaves G3 on
  a separate write-surface card and assigns G1, G4-G8 to separate remediation
  cards.
- The three integrated candidate files and the relevant current
  `transcript-verb-v1.md` history/barrier contract were read directly. The
  repository contains no root `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md` at
  this commit.

This is a specification-only review. Product tests and a `tests-passed` receipt
belong to the later implementation card under `rest-state-api-v1.md` SQ8
(lines 1467-1472). The independent checks above prove candidate custody and
deterministic text integrity; they do not claim implementation behavior.

## Finding

### F1 — BLOCKING — the materialized `mechanicalStatus` value has no decidable source contract

The candidate makes `mechanicalStatus` part of the durable, versioned session
item and requires every mutable input to enter one projection-mutation seam:

- `rest-state-api-v1.md:205-210` forbids read-time derivation and requires each
  mutable input to enter the seam.
- `rest-state-api-v1-wire-schema.md:23-27` requires the serializer not to compute
  the field from a mutable input outside that seam.
- `rest-state-api-v1.md:1417-1421` says A40 changes "each mutable input," but it
  does not enumerate those inputs, define the value domain or transitions, or
  name an existing authoritative projection function.
- A repository-wide search finds no other contract that defines
  `mechanicalStatus`; the older recon only promises "current mechanical status"
  (`rest-state-api-recon.md:499-505`).

The clause is therefore not decidable. One implementation can materialize only
harness-process state, another can fold in turns and pending wakes, and a third
can preserve a different existing calculation. All can claim that every input
*they chose* enters the seam. A40 cannot detect the omitted source because the
normative source set does not exist. That leaves the exact G2 symptom possible:
the session row and its notice can remain byte-equivalent to each other while
both carry stale or behavior-changing status bytes.

The recon's G2 repair explicitly requires either a stored/versioned status under
the complete session mutation mapping or a complete R9 dependency set
(`art_1d389e8e`, report lines 86-91). The candidate elects the first architecture
but does not complete its source boundary.

Deletion does not close this finding: the settled R7 projection already exposes
`mechanicalStatus`, and the ruled G2 outcome explicitly includes its freshness.
Accepting arbitrary or stale status bytes recreates G2. The smallest in-scope
closure is to name the existing status-projection seam and enumerate the exact
committed source inputs/value transitions it materializes, so A40 has a finite
table to test. This takes the acceptance-test rung; prose alone is insufficient.

## Clause table

| Clause / required outcome | Status | Evidence |
|---|---|---|
| Exact candidate custody and three-file homing | satisfied | Remote branch, parent/main, exact hashes, and three-file diff verified; firehose `85-96`, REST `105-119`. |
| G2-only scope; no G1/G3-G8, write, product, target, merge, deploy, or release authority | satisfied | Firehose `3-7`, `70-74`, `179-186`; REST `3-7`, `66-70`, `127-145`; exact Mike ruling. |
| Canonical sections, explicit non-goals, assumptions, homing, acceptance, and open questions | satisfied | Firehose headings `85-98`, `113-188`, `223`, `552`, `654`; REST headings `105-196`, `258`, `1128`, `1423`; wire schema is the named normative companion, not a second product spec. |
| Add the exact class identifier `session.updated` without a second resource shape | satisfied | Firehose `299-302`, `341-345`; REST `721-772`; the existing `sessions` resource and R7 serializer remain the sole shape. |
| Exact event-to-row correlation: resource, op, primary ref, payload id | satisfied | Firehose `341-345`, `644-648`; REST `763-772`, `1387-1397`; all use `sessions`, `upsert`, and equal `sessionKey`. |
| Deduplication and ordering convergence | satisfied | Firehose `458-479`, `604-613`, `644-648`; REST `907-914`, `1403-1407`; last-version-wins uses `(sessionKey,rowVersion)`. |
| Atomic version advance and no notice for unchanged bytes | satisfied | Firehose `217-221`, `343`, `568-577`; REST `190-194`, `763-772`, `1393-1401`; wire `23-27`. |
| Spawn/update/retire class selection and soft-retire upsert | satisfied | Firehose `343`, `568-577`; REST `763-772`, `1387-1401`. |
| Complete freshness for every mutable session input, including `mechanicalStatus` | **unsatisfied** | F1. REST `205-210`, `1417-1421` and wire `23-27` require a complete seam but never define the finite source/value contract. |
| Cold start from the canonical paged sessions collection | satisfied | REST `290-310`, `417-457`; firehose `108-111`, `458-468`, `609-613`. Pagination remains the snapshot authority. |
| Reconnect and detected-gap recovery use one resubscribe-and-snapshot path | satisfied | Firehose `477-479`, `521-535`, `615-623`; REST `1409-1415`. No replay cursor or socket history is introduced. |
| Retention/history authority remains unchanged | satisfied / G5 out of scope | Firehose `154-165` keeps no notice storage or retention; transcript rows remain retained behind `clearedThroughSeq` under `transcript-verb-v1.md:39-79`. The candidate does not change G5 pagination/barrier authority. |
| Authentication, visibility, filters, and denied-row behavior | satisfied | Firehose `393-415`, `592-596`; REST AU1-AU7 `957-1081`. The new classes reuse AU4 session visibility and add no credential or grant. |
| Error and protocol compatibility | satisfied / G4 out of scope | Firehose `537-550`; no error envelope, protocol, route, field, or schema version changes. Mike assigned general REST error closure to G4. |
| Shared serializer and existing R7/wire field set preserved | satisfied except F1 source semantics | Firehose `236-249`, `343`, `625-648`; REST `175-176`, `604-617`, `892-914`; wire `9-27`, `158-176`. No second serializer or field shape is added. |
| Deterministic acceptance for class selection, filters, convergence, correlation, and bypass detection | satisfied except F1 | Firehose A1/A3-A6 `552-648`; REST A35-A40 `1387-1421`. A40 is not executable as a completeness proof until F1's source set is normative. |
| YAGNI / necessity gate | satisfied | Every behavioral addition traces to ruled G2. No new route, field, credential, write surface, replay system, target, or release mechanism appears. |

Because F1 is a blocking, load-bearing ambiguity, the exact candidate cannot be
reviewed-clean.
