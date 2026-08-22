# ATC evidence reconciliation MVP

## Spirit

ATC inventories durable evidence. It does not infer readiness, completeness, or
a verdict. Every visual channel must either state exactly what its durable
source supports or stop carrying that claim.

This is a reconciliation of the current display, not a per-domain ladder
system. Metadata is sufficient for this MVP; evidence contents and composing
multiple Kung Fu do not block it.

## Normative display semantics

These rules are product behavior, not incidental implementation details:

1. **Altitude and item colour show evidence stage.** The generator must emit a
   `stage` for every work item from the durable evidence rows described below.
   Stages 0 through 4 float above the floor, descend as the stage increases,
   and use the corresponding stage colour. Stages 5 and 6 sit on the floor.
   Dropping `stage`, flattening all open items to one altitude or colour, or
   deriving stage from page-local state is a product regression.
2. **Visual landing is not merge status.** `stage >= 5` means the item is
   visually landed on the floor. It does not claim that code reached the
   canonical branch. The merge ring carries that separate claim.
3. **Only visually landed items may show a merge ring.** Stages 0 through 4
   show no merge ring, even if the feed contains merge-related fields. For a
   visually landed item, ring colour has this exact precedence:
   - black when `merged === true`;
   - green when `readyToMerge === true` from an explicit durable
     `ready-to-merge` verdict;
   - light gray when `code === false` is durably known;
   - yellow when `code === true` and `merged` is null or unknown;
   - no ring for every other combination, including `merged === false`
     without an explicit ready verdict.

The evidence-stage mapping is also normative. It inventories rows; it does not
declare readiness, completeness, or merge:

| Stage | Durable evidence represented |
|---|---|
| 0 | No recognized progress, test, completion, or review evidence. |
| 1 | A progress attest exists. |
| 2 | A `tests-passed` verdict exists. |
| 3 | A completion attest exists. |
| 4 | A `reviewed-clean`, `spec-reviewed`, or `verified` verdict exists. |
| 5 | Completion and `reviewed-clean` exist, no assignment is open, and no `tests-passed` row more than five minutes after the last clean review makes that review stale. |
| 6 | The work item is closed and no assignment is open. |

A later recognized row advances the displayed stage without inventing missing
earlier rows. Hover and detail must still list the actual distinct attest and
verdict kinds, so stage never implies that every earlier ladder step exists.

## Channel audit

| Channel | Current claim | Durable backing | Mismatch | MVP reconciliation |
|---|---|---|---|---|
| Work-item altitude and stage colour | Evidence rows have accumulated to the displayed stage | Normative stage mapping above, emitted by the generator from durable rows | The page becomes a flat, same-colour swarm if `stage` disappears; naming stage 5 ready or stage 6 merged would overclaim | Keep altitude and colour as the core evidence metaphor. Require `stage` in the feed. Describe the numbered evidence state, never readiness or merge. |
| Work-item floor placement and size | The item is visually landed because its evidence stage is 5 or 6 | `stage >= 5` from the same durable stage mapping | Visual landing can be mistaken for code landing | Keep floor placement and the landed size change. State explicitly that visual landing is evidence-stage presentation, not canonical branch status. |
| Evidence list in hover/detail | Filled circles say each prior ladder requirement exists | `i < stage`, not the actual row set | It invents absent evidence whenever a later row exists | Feed and render the distinct attest kinds and verdict kinds that actually exist. Do not synthesize missing predecessors. Include open/terminal assignment counts as metadata. |
| Merge-ring presence | Merge status is meaningful for a visually landed item | `stage >= 5` | Drawing rings for floating work makes ordinary unfinished work look exceptional | Render no merge ring below stage 5. Apply the colour rules only after the landed gate passes. |
| Black merged ring | Canonical branch evidence contains the code | Landed gate plus `merged === true` from the canonical resolver | Closure or stage alone must not imply merge | Black only when durable canonical branch evidence proves `merged === true`. |
| Green ready-to-merge ring | An explicit durable ready-to-merge verdict exists | Landed gate plus `readyToMerge === true` | ATC cannot infer readiness from completion, review, or `merged === false` | Green only for the explicit verdict. A false branch result alone does not qualify. |
| Light-gray nothing-to-merge ring | Durable evidence says the item has no code | Landed gate plus `code === false` | Unknown code or merge state must not look like absence | Light gray only for durable non-code state. |
| Yellow unknown ring | Code exists but canonical merge state is unknown | Landed gate plus `code === true` and `merged == null` | Unknown must remain distinct from non-code | Yellow only for code with null or unknown merge state; state “merge state unknown” in detail. |
| Red orphan ring and item-agent tethers | Open item has no live holder; tethered agent holds an open assignment or active/queued turn | Open assignment rows and turn rows | None, if wording stays snapshot-specific | Keep. Say “no open holder” rather than implying the item was abandoned. |
| Working shimmer and waiting flash | A turn is running or queued now | Unended turn rows | None | Keep unchanged. |
| Agent tree position and family arcs | Spawn hierarchy | Durable `spawnedBy` session links | None | Keep. |
| Agent disc size and which names are promoted | Agent role class | Role guessed from display-name keywords | A name is not durable role evidence | Remove role-based size/promotion claims unless backed by explicit durable role data; default to one depth-scaled agent treatment. |
| Agent colour | Recent activity fading to idle | Latest durable turn or attest timestamp | None when labelled activity, not role | Keep. |
| Agent-agent obligation lines | A fired wake produced a queued/running turn between two agents | Wake and turn rows | None | Keep. |
| X/Z proximity | Layout convenience, often centred near current holders | Holder positions and deterministic scatter | Proximity can be mistaken for relationship | Keep explicitly non-semantic. Only tethers, family arcs, and authored arrows assert relationships. |
| Ghosting, focus, selection, and hover | Current viewer scope and interaction state | Page-local view state | Not organization evidence | Keep separate from evidence semantics. Ghosted continues to mean out of scope, not absent. |
| Tags and authored arrows | An identified author made an annotation or relationship claim | Durable annotation rows with author | None; contents are authored claims, not system findings | Keep provenance visible and never promote them into evidence automatically. |
| Viewer selection telemetry | `/api/selection` describes what a viewer selected and sees | Every page posts a `clientId`, but the server keeps one last-writer-wins record | One viewer silently replaces another viewer's reported truth | Retain reports per `clientId` and expose the viewer identity with each report. Compatibility fields may be derived, but must identify which viewer they describe. |
| Legacy author caption | No caption reads as an unowned or system-owned record | Tags, arrows, and saved searches preserve a missing author as `null`; the page currently omits the caption | Unknown provenance is presented as if no provenance question exists | Render `author unknown` for a missing durable author. Do not infer or backfill one, and preserve author-scoped removal rules. |
| Wake/message pulses | A durable wake fired or message was delivered | Wake/message rows | None | Keep. |

## Data and presentation

The generator should emit a compact evidence inventory per work item:

- work-item state;
- evidence `stage`, using the normative mapping above;
- distinct attest kinds and verdict kinds that exist;
- open and terminal assignment counts;
- whether code is evidenced;
- branch state: `true`, `false`, or `unknown`.

Merge resolution must use an explicit canonical remote and branch. A recorded
session workdir is not durable repository identity and must not be required for
resolution. The resolver may use a remote API or a service-owned durable cache,
but it must test the recorded commit against the configured canonical branch.
It must return `unknown` when the remote identity, commit, or lookup is
unavailable. It must never guess a remote from a deleted path or turn lookup
failure into `false`.

The page should show those exact metadata facts in hover/detail. It must not
fill missing evidence, rank an item as ready, or translate closure into merge.
Domain-specific attest/verdict names may be displayed as filed; ATC does not
reinterpret them.

The page must use the emitted `stage` for altitude, stage-graded colour, visual
landing at stage 5 or 6, and the landed eligibility gate for merge rings. A
fallback for an old feed may prevent a crash, but it is not valid canonical
output: a missing stage is a feed defect and must fail acceptance.

The server should retain viewer reports by `clientId`, as settled in
`docs/state-review.md`, instead of flattening them into one shared report. The
page should render a missing annotation/search author as `author unknown` while
leaving the stored value unknown.

## Regression evidence

The 2026-08-22 regressions are acceptance evidence for this contract:

- `add8c3c` restored the landed gate after merge rings appeared around
  floating, unfinished work.
- `a14af4fd85111a04a7d217536a7c1672beaf3855` restored the generator's
  `stage` field and the page's stage altitude, stage colour, floor placement,
  and landed ring gate after the board collapsed into a flat red swarm.

Those commits prove the incident and the repaired behavior. This spec is the
product authority that future implementations and reviews must preserve.

## Proof and scope

Use deterministic fixtures for:

1. every stage from 0 through 6, proving stage-graded colour, descending
   altitude for stages 0 through 4, and floor placement for stages 5 and 6;
2. a later verdict with no earlier software-ladder rows, proving that stage
   advances without inventing missing detail rows;
3. stages 0 through 4 with every merge-field combination, proving that no
   merge ring renders before visual landing;
4. landed controls for black merged, green explicit-ready, light-gray
   durable-non-code, yellow code-and-unknown, and no ring for false/not-ready;
5. an item with an open assignment plus terminal assignments;
6. an agent whose display name suggests a role not present in durable role data;
7. two viewer reports with different selections and focus state;
8. a tag, arrow, and saved search whose durable author is null;
9. a canonical feed with `stage` removed, proving acceptance detects the
   regression instead of accepting a flat fallback display.

Show before/after generated JSON and rendered text/mark counts. Verify the
private browser with real hover/pointer interaction. Scope is
`bin/tb-weather-gen`, `server/tb-atc-api.py`, `web/index.html`, and the smallest fixtures. Do not build
Kung Fu-specific ladders, read evidence contents, redesign the map, deploy, or
write hosted ATC. Require one concise independent exact-commit review under
Mike's MVP threshold.

### Live merged-ring acceptance cases

Before the ring fix, Mike observed these five code-evidenced, stage-5 items
with `merged=null` rendered gray in the live feed. A raw `merged=null` fixture
for each must render yellow rather than gray:

- `wi_27396747-b8b6-4c9b-96c5-be50d549673e`
- `wi_dd815f6e-0300-4b2c-9ac8-0038af8f0e9e`
- `wi_97ba409e-00dc-4449-bd85-82b8de3492dd`
- `wi_fa8adc7a-d1fe-445f-bf1c-c3e7cf4a5c01`
- `wi_8bc90e19-6f7f-46a6-aa85-e903e4fdec7e`

The canonical resolver must then replace `null` when durable branch evidence
answers the question. Commit `dded025cc6e6b900bd9bd24b0c24713793f3298b`
for `wi_27396747-b8b6-4c9b-96c5-be50d549673e` is on canonical
`clickety-clacks/tightbeam-atc` main, so that live item must resolve to
`merged=true` and render black. Resolve the other four from the same explicit
canonical source; render yellow only when the lookup remains genuinely
unknown.

The proof must also include one explicit ready-to-merge green-ring control and
one durably non-code light-gray control. Record any canonical lookup that stays
`null` despite reachable branch evidence as a feed defect. Do not infer a
missing value in the page.
