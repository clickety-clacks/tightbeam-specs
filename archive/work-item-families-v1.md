# Work-item families — grouping the substrate DERIVES — v1

Status: SUPERSEDED by topline-map-v1 (2026-07-26) — its grouping is absorbed there alongside per-node telemetry and subtree queries; shipping both would duplicate the same read. Retained for the epistemics analysis (immutable creator axis vs mutable spec pin) which topline-map inherits. Prior status: DRAFT r3 (Opus-authored 2026-07-26; r2 gate NOT-READY(5) folded — creator columns are PRINCIPAL CLASS not human-vs-agent, spec families are a live projection of a MUTABLE pin while the creator axis is immutable, selector/basis contract typed incl a singleton basis, --item authorizes the selector first, proof 6 admits the ordinary Dispatch audit row). Flynn ruling: "i don't want to decide
groupings or anything, it's better if the substrate TELLS me how it's grouped.
otherwise you have two sources of unsync'ed truth again." Then, on r1's proposed
column: "i thought the substrate already supports this use case" — IT DOES. r1 wanted
a new `originTurnSeq`; verification showed `work_items` already carries
`createdBySession` / `createdByUser` (mutually exclusive, CHECK-enforced, populated at
create, already selected on read) plus `specRefName`/`specRefSha256` and `isBug`.
**This spec therefore adds NO schema and NO writes — it is a QUERY over facts the
substrate already records.**

## The defect

Tightbeam has one level (item + assignments) and no way to ask "how is the thing I
asked for going?" — a board of 26 items has real families (one lane's discovered bugs;
one spec's several items) and only prose represents them. Kanban answers this with
declared epics/labels, which drift the moment plan and reality diverge — a second,
unreconciled source of truth. The ruling is to derive instead.

## The two grouping signals (both already durable)

1. **LANE / DISCOVERY provenance — `createdBySession`.** An item created by session S
   was spawned by whatever S was doing. This is the parent link for discovered work:
   the cold-adapter bug created by the client-e2e lane's session is causally that
   lane's child, recorded as a fact at creation.
2. **INTENT grouping — the spec pin (`specRefName` + `specRefSha256`).** Items pinned
   to the same spec are the same intent by construction. This is usually the "high-level
   thing you asked for."

`createdByUser` vs `createdBySession` records the AUTHENTICATED PRINCIPAL CLASS, NOT
human-vs-agent (gate F1): a human acting through a session token — including `--as-user`
— still writes `createdBySession`. The honest reading is "user-principal-created" vs
"session-principal-created"; do not infer humanity from it. `isBug` is likewise a
CALLER CLASSIFICATION, mutable via work-item-update — useful, not proof of discovery.

**EPISTEMICS, labelled (gate F2 — the two axes are NOT the same kind of fact):**
- `createdBySession`/`createdByUser` is IMMUTABLE — stamped at create, never updated —
  so the creator family is a durable causal fact.
- The spec pin is MUTABLE BY DESIGN (`work-item-update` may repin or clear it; it means
  "the spec currently governing this item"). The spec family is therefore a LIVE
  PROJECTION of current governing metadata, not a historical fact: repinning MOVES an
  item between families, and that is correct semantics, not drift. It is still a single
  source of truth — the item's own pin — which is what the ruling required; it is simply
  not immutable, and the response says which axis produced the answer so no caller
  mistakes one for the other.

## Surface — one read verb, no state

`work-item-family` returns a family with a DERIVED rollup, selected by exactly one of:
- `--spec <name> [--spec-sha <sha256>]` — items sharing that pin. NAME ALONE is
  ambiguous across revisions (gate F3): without `--spec-sha` the family is every item
  pinned to that NAME at any revision, and the response says so
  (`key: %{name: n, sha: nil}`); with it, exactly that revision.
- `--session <key>` — items that session-principal created (the lane family).
- `--item <id>` — the family of that item: its spec family if pinned, else its creator
  family, else ITSELF.

Response: `{basis, key, members: [{workItem, createdBySession|null, createdByUser|null,
isBug}], rollup}` ordered by `createdAt`, where:
- `basis` ∈ `"spec" | "session" | "item"` — `"item"` is the honest singleton basis for
  an unpinned, user-principal-created item (gate F3: calling that "session" would be
  false), with `key: <itemId>`.
- `key` is typed per basis: `%{name, sha|nil}` for spec, the session key string for
  session, the item id for item.
- `workItem` is the FULL item object as `work-item-get` returns it (not an id).

**Rollup is computed on read, never stored:**
`{total, open, iceboxed, closed, failed, with_open_assignment, last_progress_at}` —
counts of the members' own states plus the max trace-visible progress across the family
(turn ends, attests, dispositions — all already durable). NO percentage: state counts
plus recency are groundable; a percentage is an inference the substrate cannot justify.

Authorization: the owner-or-admin rule `work-item-trace` uses, applied PER MEMBER — a
member the caller cannot see is OMITTED and excluded from the rollup (never a stub,
never an existence leak), so a partial view never implies a whole one. A caller who can
see no member gets `not_found`. **SELECTOR-FIRST for `--item` (gate F4):** the selector
item must ITSELF pass that rule BEFORE any basis derivation — otherwise reading an
invisible item's pin/creator to return its visible siblings would prove the item exists
and disclose its family basis. Unknown id and invisible id both return `not_found`,
identically, even when visible siblings exist.

`last_progress_at` = the max over VISIBLE members of their turn ends (`turns.endedAt`),
attests (`attests.ts`), and disposition transitions (`causal_events.at`) — all durable
today; `null` when the family has none.

## Known limits, named rather than engineered away

- A session that worked several jobs creates items attributed to the SESSION, not to
  the specific job. That is the honest resolution of what the substrate recorded; if
  job-level parentage is ever genuinely needed, THAT is when a `originTurnSeq` column
  earns its place — not before (r1 proposed it prematurely).
- Items with neither a spec pin nor a shared creator are singletons. Correct: they have
  no causal family, and inventing one would be the declared-grouping failure the ruling
  rejects.
- Retro-grouping ("these four are one push, I now realize") is NOT supported and NOT
  worked around. The honest expression is to create the parent intent and route the
  work through it — then causality records it truthfully.

## Non-goals (the ruling, explicit)

NO declared parent, NO re-parenting, NO tags/labels/epics. NO new columns, NO new
tables, NO emission, NO agent-writable state. NO stored rollup or status field. NO
percentage.

## Required proofs

1. Spec family: three items pinned to one spec return together under `--spec`; an item
   pinned elsewhere is excluded.
2. Lane family: items created by session S return under `--session S`; a user-created
   item is excluded (and returns as its own root under `--item`).
3. `--item` basis selection: a pinned item resolves by spec and says `basis: "spec"`;
   an unpinned one resolves by creator and says `basis: "session"`; an unpinned,
   user-created item is a singleton.
4. Rollup counts match members' real states; `last_progress_at` advances when any
   member gets a turn end / attest / disposition; nothing is written (a second call
   after mutating a member reflects it with no rollup row anywhere).
5. Authorization: an invisible member is omitted AND excluded from the rollup; a caller
   who can see none gets `not_found`.
6. Read-only in its OWN effects (gate F5 — strict zero-write is impossible: Dispatch
   INSERTs an audit row for every successful verb, and denials too): the verb performs
   NO domain or rollup writes — no work_items/assignments/causal_events/turns mutation
   and no stored rollup anywhere — while the ordinary Dispatch audit event is EXPECTED
   and allowed. Result elision (as the transcript verb requires) is deliberately NOT
   applied: a family payload is bounded work metadata, materially less sensitive than
   transcript content, and `work-item-trace` already records a richer result.

## Component touches

A family/rollup read module, `work-item-family` verb (gateway + router + CLI +
cli-surface row), tests. NO schema, NO migration, NO emission. Depends only on columns
already shipped.
