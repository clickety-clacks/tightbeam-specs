# Editable Work-Item Body and Supported CLI Read/Update

- Status: SPEC-READY — MAIN-ERA AUTHORITY AMENDED FROM REVIEWED-CLEAN ARTIFACT; EXECUTION-TIME `origin/main` EVIDENCE PIN `8d0baa789c4aea1513a6d77ed53a6d54d76d1fb6`; COLD-DIGESTED; B1/I1 CLOSED
- Work item: `wi_0488b06a-0950-4356-84b7-c56e413a6bbe`
- Authority: owner main-era amendment ruling `att_be83756f-1f59-4d2c-bd6c-cd5da5e311f5`; immutable ruling `art_7d8f7444`, SHA-256 `e967132d3c11b8c3afb84a5d6722a73b3900eace6571587ca68a41839a13ce0d`
- Spec assignment: `asg_137f199a-e1fd-4e89-b8b4-4098badbddcc`
- Historical reviewed artifact: `art_31dd4cfc`, SHA-256 `65831b88b0df41ce216255d4de9ea8d2770aecca96869202b4320e5058b73606`
- Historical reviewed-clean verdict: `att_cd680ee6-aac3-4b94-a3e3-4f584824f7a3`; report `art_3af9d997`, SHA-256 `8d97d81dc9dc19c473f87c3e6915bb478eb6bef7e7f4623724e7b296cad43e83`
- Authoritative source line: execution-time `origin/main`; `8d0baa789c4aea1513a6d77ed53a6d54d76d1fb6` is the amendment evidence pin, not a permanent implementation baseline
- Pattern name: **work-item body detail**

## Goal

G1. A work item has one optional, durable text body for scope, requirements, and acceptance criteria.

- Acceptance: Given an existing work item, when an authenticated caller stores body text, then `work-item-get` returns the same text after a gateway restart.

G2. The existing `work-item-get <workItemId>` command is the supported body read command.

- Acceptance: Given a work item with body text, when a caller runs `tightbeam work-item-get <id>`, then the command returns the text under `workItem.body`.

G3. A new `work-item-update <workItemId>` CLI command replaces or clears the body of an existing work item.

- Acceptance: Given a work item, when a caller runs `tightbeam work-item-update <id> --body "replacement"`, then a later get returns `replacement`.

G4. The product keeps `specRefName` and `specRefSha256` distinct from the editable body.

- Acceptance: Given a work item with a pinned spec reference, when a caller sends a body-only replacement or clear, then both spec-reference values remain byte-identical.

This feature must add a mechanism. Deleting the work-item or spec-reference surfaces loses durable intent. Accepting title-only intent does not satisfy the user's request.

## Non-Goals

- This spec does not remove, rename, migrate, alias, or reinterpret `specRefName` or `specRefSha256`.
- This spec does not expose title, bug classification, or spec-reference edits through the new CLI command.
- This spec does not add body history, versions, diffs, rich-text parsing, search, templates, or section-specific fields.
- This spec does not add compare-and-swap, edit leases, merge logic, or an update idempotency key.
- This spec does not add a second read verb.
- This spec does not add a body flag to `work-item-create`.
- This spec does not add the body to `work-item-list`, job traces, work-state projections, execution maps, toplines, or device work-item endpoints.
- This spec does not change work-item state transitions, routing wakes, slate wakes, assignment behavior, or disposition authorization.
- This spec does not change the existing raw gateway behavior for title, spec-reference, or `isBug` updates.
- This spec does not deploy, restart, migrate, backfill, or mutate a live work-item row.
- This spec does not implement, integrate, release, or deploy the feature. Separate post-review authority is required before work starts from a green `origin/main` and follows the repository's current branch-and-merge law.

Decisions considered and declined:

- A new `work-item-body-get` verb is declined because `work-item-get` already returns the detail projection.
- A column on `work_items` is declined because existing stamped databases cannot gain a column through the fail-closed schema bootstrap.
- A body document split into scope, requirements, and acceptance columns is declined because the user asked for one editable body.
- Markdown validation is declined because the body stores human-authored text, not a product-owned document grammar.
- Owner-only editing is declined because the current `work-item-update` handler permits authenticated user and session principals without an item-owner check.

## Terms

- **Work-item body**: Optional UTF-8 text associated with one work-item id. It lives in the `work_item_bodies` sidecar table. The `work-item-get` detail projection exposes it as `workItem.body`.
- **Spec reference**: The existing paired `specRefName` and `specRefSha256` fields on `work_items`. It identifies immutable external authority. It is not body text.
- **Absent body**: The public value `null`. A legacy item with no sidecar row and an item whose body was cleared both project this value.
- **Empty body**: The present string `""`. It is distinct from an absent body.
- **Body replacement**: One update that sets the complete next body value. It is not a text patch.
- **Body clear**: One update that sets the public body value to `null`.
- **Body attribution**: The principal and timestamp of the most recent body change. The detail projection exposes `bodyUpdatedByUser`, `bodyUpdatedBySession`, and `bodyUpdatedAt`.
- **Legacy work item**: A row that existed before the sidecar activation and has no `work_item_bodies` row.
- **Metadata doorbell**: One `work_item_events` row with kind `metadata`. It says a work-item detail changed without copying the body.
- **Body descriptor**: Non-content metadata about a body. Every descriptor carries state (`present` or `absent`), UTF-8 byte length, and the 64-character lowercase hexadecimal SHA-256 of the exact body bytes; an absent body carries a null SHA-256. An update descriptor also carries attribution and whether the requested update changed the stored value. A descriptor does not carry body text.
- **Supported CLI surface**: Commands parsed by the Rust CLI and documented by `tightbeam help`.
- **Additive activation**: A transaction that creates and validates new schema objects without altering or backfilling an existing table.
- **Org credential**: The operator credential that the wire router classifies as `:org`. An org credential does not itself name a work-item principal.
- **Session credential**: A session token that the wire router classifies as `{:session, session}`. It names the session and restricts which explicit identity selectors the caller may use.
- **Legacy metadata patch field**: One of the pre-existing raw `work-item-update` fields `title`, `isBug`, `specRefName`, or `specRefSha256`. The new CLI does not expose these fields.

## Assumptions

A1. Tightbeam stores durable org state in the SQLite database named by the gateway configuration.

A2. `work-item-get` already exists in the Rust CLI, wire router, gateway handler table, and work-item module.

A3. `work-item-update` already exists in the wire router, gateway handler table, and work-item module. Commit `864c7df` initially exposed a generic Rust CLI update, and CLI-surface cleanup `86fecf2` removed it. The baseline intentionally has no Rust CLI update; this feature exposes only the body forms instead of restoring the prior generic metadata surface.

A4. The wire router resolves the credential and explicit identity before the work-item handler applies its principal rule. The observable refusal therefore depends on both the credential class and the identity selector.

A5. SQLite serializes the update transactions that target one database.

A6. JSON request strings and Rust CLI arguments carry UTF-8 text.

A7. The existing live-content ceiling is 64 KiB. The body uses the same byte ceiling so one body cannot exceed one accepted prompt-sized text unit.

A8. The schema bootstrap may add a validated sidecar object set to the current readable shape. It must not alter an existing production table.

A9. Existing CLI callers consume the JSON result that the gateway returns. They do not deserialize a fixed Rust work-item struct.

A10. At amendment execution time, durable open-assignment records declared no claim on the implementation and smoke paths listed in Architecture section 10. Owner ruling `att_be83756f-1f59-4d2c-bd6c-cd5da5e311f5` withholds implementation authority until this exact amendment is reviewed-clean and the owner grants separate implementation authority.

A11. At execution-time `origin/main` `8d0baa789c4aea1513a6d77ed53a6d54d76d1fb6`, `.github/workflows/ci.yml` has SHA-256 `1ccc8176ca9a8b9c2a677eaf31723e3c9602f6790ed8baccb945a5bc2d000e57`. It runs on pushes to `main`; its test matrix jobs are named `linux` and `macos`; and its release guard uses `refs/heads/main`. This body feature makes no workflow edit.

A12. `Tightbeam.ClientE2E.LegGateway` is the repository's existing executable seam for a run-local file-backed gateway. `provision!/2` creates a fresh org from a provisioned template without copying `state.db`; `boot/3`, `restart/2`, and `teardown/2` own the captured gateway process, same-database restart, descendant cleanup, and run-directory removal.

A13. `main` is the only source and integration line for this work. Current repository law requires a holder to branch from a green `origin/main`, finish and verify the branch, record review evidence in the specs repository, and merge the finished work to `main`. A holder does not develop directly on `main`.

## Invariants

### Identity and separation

R1. The system stores the body outside the `work_items` row.

- Acceptance: Given a database at the baseline shape, when body support activates, then `PRAGMA table_info(work_items)` returns the baseline column list unchanged.

R2. A body-only update changes no `specRefName` value.

- Acceptance: Given `specRefName = "specs/tightbeam/example.md"`, when a caller replaces the body, then a direct row read returns the same spec-reference name.

R3. A body-only update changes no `specRefSha256` value.

- Acceptance: Given a 64-character spec-reference digest, when a caller clears the body, then a direct row read returns the same digest.

R4. The CLI accepts no spec-reference flag on `work-item-update`.

- Acceptance: Given `tightbeam work-item-update wi_1 --spec-ref x`, when the CLI parses the command, then it exits with the exact update usage error and sends no request.

### Body value

R5. The body value is `null` or a valid UTF-8 string whose encoded size is at most 65,536 bytes.

- Acceptance: Given a 65,536-byte UTF-8 string, when a caller stores it, then the update succeeds. Given a 65,537-byte string, the update returns `invalid_body` and preserves the prior value.

R6. The system preserves accepted body bytes without trimming or normalization.

- Acceptance: Given a body containing leading spaces, a newline, composed Unicode, quotes, and a trailing newline, when a caller stores and reads it, then the returned UTF-8 bytes equal the submitted bytes.

R7. The public body value distinguishes absent from empty.

- Acceptance: Given a legacy item and an item updated with `--body ""`, when a caller reads both, then the first body is `null` and the second body is `""`.

R8. `--clear-body` sets the public body value to `null`.

- Acceptance: Given a present body, when a caller clears it, then get returns `body: null` and non-null body attribution for the clear.

R9. One update replaces the complete body.

- Acceptance: Given body `alpha beta`, when a caller stores `gamma`, then get returns `gamma` and no fragment of the prior text. Given a raw metadata-only update that omits `body`, the stored body and its attribution remain unchanged.

### Reads and responses

R10. `work-item-get` returns the body and body attribution in its existing `workItem` object.

- Acceptance: Given a session-principal body update, when a caller gets the item, then `bodyUpdatedBySession` names that session and `bodyUpdatedByUser` is `null`.

R11. A legacy item returns null body fields without a backfill write.

- Acceptance: Given a baseline item with no sidecar row, when a caller gets it, then the four body fields are `null` and the sidecar still has no row for the item.

R12. Work-item create, list, update, trace, work-state, execution-map, topline, and device responses do not copy body text.

- Acceptance: Given a work item whose body contains a unique sentinel, when each named projection runs, then only `work-item-get` output contains the sentinel.

R13. Existing `work-item-get` fields keep their names and meanings.

- Acceptance: Given a baseline fixture, when body support reads it, then the pre-feature work-item and assignment fields match the baseline fixture and the four body fields are additive.

### Mutation, attribution, and concurrency

R14. The body and its attribution change in one SQLite transaction.

- Acceptance: Given an injected failure after the sidecar write and before transaction commit, when the update runs, then neither the body nor attribution changes.

R15. A real body change records the authenticated principal that the transport resolved.

- Acceptance: Given a session token acting through `--as-user mike`, when it replaces the body, then `bodyUpdatedByUser` is `mike` and `bodyUpdatedBySession` is `null`.

R16. A repeated update with the stored value does not change attribution.

- Acceptance: Given body `same` and attribution timestamp `T`, when a caller stores `same`, then the returned descriptor says `changed: false` and get still returns timestamp `T`.

R17. A real body change invokes the existing metadata-doorbell callback exactly once after the body transaction commits. A successful callback emits one metadata doorbell. A callback failure does not roll back the committed body and does not retry inside the command.

- Acceptance: Given one changed update followed by one equal-value update and a functioning callback, when a consumer reads `work_item_events`, then it finds one new `metadata` row. Given an injected callback failure, the changed body remains readable, no doorbell appears, and the callback invocation count is one.

R18. Concurrent successful updates use last-committed-write-wins semantics.

- Acceptance: Given two transactions that replace one body with different values, when transaction B commits after transaction A, then get returns B's value.

R19. Body updates accept no compare-and-swap token or idempotency key.

- Acceptance: Given `--if-body-sha256` or `--key` on the CLI update command, when the CLI parses the command, then it exits with the update usage error and sends no request.

R20. Body mutability does not depend on work-item lifecycle state.

- Acceptance: Given one item in each state `open`, `iceboxed`, `closed`, and `failed`, when an authenticated caller replaces each body, then each update succeeds and each state remains unchanged.

### Authorization and audit

R21. A user principal may read and update a body.

- Acceptance: Given an org credential with `--as-user mike` and a session credential owned by `mike` with `--as-user mike`, when each caller runs get and update, then each call succeeds and a real body change attributes `bodyUpdatedByUser` to `mike`.

R22. A session principal may read and update a body.

- Acceptance: Given an existing work item, when a session token runs get and update under a held role, then both calls succeed.

R23. The feature preserves the baseline credential-and-identity refusal mapping for body reads and updates.

- Acceptance: Given an org credential with `--as-process cron`, when the caller runs get or update, then the router resolves `{:process, "cron"}`, the work-item handler returns `process_denied` with HTTP 403, get exposes no body, and update changes no body value. Given a session credential with `--as-process cron`, the router returns `identity_not_yours` with HTTP 403 before the work-item handler runs. Given an org credential with `--as <bound-role>`, the router resolves an agent origin with a missing principal and the work-item handler returns `principal_required` with HTTP 403. Given an org credential with no identity selector, the router returns `invalid_message` with HTTP 400 before the work-item handler runs.

R24. Every `work-item-update` audit row for a request that contains `body` omits body text. An accepted row carries origin, principal, work-item id, body state, byte length, SHA-256, and the changed flag. A raised row carries a stable crash descriptor without the exception message.

- Acceptance: Given body sentinel `DO_NOT_COPY`, when a caller updates it successfully and when an injected post-validation exception renders the submitted body in its message, then neither event payload contains the sentinel; the accepted event carries the body descriptor and the raised event carries `crash: true`, `code: "server_error"`, and `bodyElided: true`.

R25. Every `work-item-get` audit row omits body text. An accepted row carries a body descriptor. A raised row carries a stable crash descriptor without the exception message.

- Acceptance: Given body sentinel `DO_NOT_COPY`, when a caller gets it successfully and when an injected post-read exception renders the body in its message, then the successful response contains the sentinel but neither event payload does; the raised event carries `crash: true`, `code: "server_error"`, and `bodyElided: true`.

R26. A denied update uses the existing denied-event path.

- Acceptance: Given a 65,537-byte body, when a caller submits it, then one denied `work-item-update` event records `invalid_body` and the stored body remains unchanged.

### Durability and schema compatibility

R27. Body support activates as one exact additive schema object set.

- Acceptance: Given a baseline stamped database with neither body object, when schema boot runs, then both objects and one activation row exist after one commit.

R28. An incomplete or malformed body object set causes a named boot refusal.

- Acceptance: Given only `work_item_bodies` or a table with the wrong SQL, when schema boot runs, then it raises `incompatible_work_item_body_v1` and creates no missing object.

R29. An interrupted first activation leaves no partial body object set.

- Acceptance: Given an injected failure after either activation statement, when the transaction exits, then neither new table exists and the next clean boot activates once.

R30. The activation leaves the baseline schema stamp unchanged.

- Acceptance: Given the exact pre-activation current-main stamp, when body support activates, then the stamp remains byte-identical. The execution-time fixture value is `coordination-fabric-v1-phase1-v3`; that literal documents the amendment evidence pin and is not a permanent future stamp.

R31. A file-backed database retains the body across gateway process restart.

- Acceptance: Given a body committed through the real CLI and gateway, when the gateway stops and starts on the same database, then the real CLI get returns the same bytes and attribution.

### CLI and wire

R32. The CLI grammar is `tightbeam work-item-update <workItemId> (--body <text> | --body=<text> | --clear-body)` with at most one supported identity selector. The one-token `--body=<text>` form is the canonical spelling when body text begins with `--`; it is also valid for other body text, including the empty string.

- Acceptance: Given `--body text`, `--body=text`, `--body=`, or `--clear-body`, with no explicit identity or with one valid identity selector, when the CLI parses the command, then it constructs `Command::WorkItemUpdate` with the exact replacement, empty, or clear value. Given argv `--body --clear-body`, the parser treats the two tokens as conflicting body operations and returns the exact command usage text; it does not store literal body text. Given `--body=--clear-body` or `--body=--body`, the parser stores the exact flag-looking text. Given neither body operation, repeated operations, an unsupported flag, or terminal `--body`, parsing returns the exact command usage text. Given more than one identity selector, parsing returns the existing exact identity-mutual-exclusion error. Given an existing command other than `work-item-update` and argv containing `--name=value` or `--clear-body next`, the parser returns the same command or error as the pre-feature baseline.

R33. `--body ""` sends an empty JSON string.

- Acceptance: Given an explicitly empty body argument, when the CLI builds the request, then the request contains `"body":""`.

R34. `--clear-body` sends JSON null.

- Acceptance: Given the clear flag, when the CLI builds the request, then the request contains `"body":null`.

R35. The CLI sends no title, bug, or spec-reference field for a body update.

- Acceptance: Given either supported update form, when the CLI builds the byte-exact JSON request, then `params` contains only `workItemId` and `body`.

R36. The CLI help lists the update command and states replacement and clear semantics.

- Acceptance: Given `tightbeam help`, `tightbeam help work-item-update`, and the unknown-command roster, when a caller reads each command catalog, then each lists `work-item-update`; both help surfaces show the exact syntax and state that the command replaces or clears the body.

R37. The prior `work-item-create` and `work-item-get` request bytes remain unchanged.

- Acceptance: Given the baseline byte fixtures, when the CLI builds those requests after this feature, then each request equals its baseline fixture.

R38. Each implementation lane records its applicable clean `origin/main` verification baseline before its first source edit and records the same gates again on its exact produced commit.

- Acceptance: Given the amended specification is reviewed-clean, separate implementation authority exists, and the then-current `origin/main` gate is green, when a lane that touches Elixir, Rust, or both starts, then its branch starts from that exact main SHA. When its verification evidence is reviewed, the evidence names the clean baseline SHA, produced commit SHA, exact applicable commands, environment hygiene, and exit result for both runs. For each test command, it also records pass, failure, and skip counts. The produced-commit run is green and no applicable count is omitted. Given main is red or either authority is absent, the opener creates no implementation assignment.

R39. One GitHub Actions test workflow run verifies the exact integrated `main` SHA on Linux and macOS before the feature is accepted as complete.

- Acceptance: Given a candidate branch from green main has passed the full local gate, the real smoke, and one independent whole-change exact-commit review, and its review evidence has landed in the specs repository, when the finished branch merges to `main` under current repository law and the push workflow runs, then `github.ref` is `refs/heads/main`, the workflow `head_sha` equals the resulting remote-main SHA, and its `linux` and `macos` test-matrix jobs both conclude `success`. The feature candidate contains no body-feature-authored `.github/workflows/ci.yml` change. The evidence records the workflow run id or URL, workflow ref, workflow `head_sha`, both job names and conclusions, printed Elixir and Rust versions, the release CLI build result, each Mix and Rust gate result, and each test command's pass, failure, and skip counts. The work item remains incomplete while either job is absent, pending, canceled, stale-SHA, or failed.

R40. A raw update is body-only or legacy-metadata-only.

- Acceptance: Given an existing work item and a raw `work-item-update` request that contains `body` and one or more legacy metadata patch fields, when `Tightbeam.WorkItems` handles it, then the handler returns `invalid_body_patch` before any write. When the same request crosses the wire, the router returns HTTP 400. The body, body attribution, title, `isBug`, `specRefName`, and `specRefSha256` remain unchanged.

R41. The repository provides one executable reality-smoke command for a fresh file-backed gateway and the built Rust CLI.

- Acceptance: Given a clean candidate, a provisioned template org, and an unused port at least 12000, when the verifier builds `cli/target/release/tightbeam` and runs `mix run --no-start scripts/work_item_body_smoke.exs` with the two required smoke environment variables, then the script provisions a state-free run directory, boots a gateway, performs the body scenario through that exact CLI binary, restarts the gateway on the same database, repeats the read checks, tears down the process tree, and exits 0. A missing template, invalid or occupied port, missing binary, failed assertion, restart failure, surviving process, or failed cleanup exits nonzero and names the failed phase.

## Architecture

### 1. Durable representation

Add this validated sidecar table. Do not alter `work_items`.

```sql
CREATE TABLE work_item_bodies (
  workItemId       TEXT PRIMARY KEY REFERENCES work_items(id),
  body             TEXT,
  updatedByUser    TEXT REFERENCES users(userId),
  updatedBySession TEXT REFERENCES sessions(sessionKey),
  updatedAt        INTEGER NOT NULL CHECK(updatedAt >= 0),
  CHECK(body IS NULL OR
        (typeof(body) = 'text' AND length(CAST(body AS BLOB)) <= 65536)),
  CHECK((updatedByUser IS NOT NULL) != (updatedBySession IS NOT NULL))
);
```

Add this activation row table:

```sql
CREATE TABLE work_item_body_activation (
  id          INTEGER PRIMARY KEY CHECK(id = 0),
  activatedAt INTEGER NOT NULL CHECK(activatedAt >= 0),
  cause       TEXT NOT NULL CHECK(cause = 'schema_activation'),
  principal   TEXT NOT NULL CHECK(principal = 'process:tightbeam')
);
```

`Tightbeam.Schema` owns one ordered object list for these tables. At boot it follows this total order:

1. Read the presence of both named objects.
2. Validate the SQL of each present object against the canonical SQL.
3. If neither object exists, create both in one transaction and insert activation row `(0, now, 'schema_activation', 'process:tightbeam')`.
4. If both objects exist, validate the single activation row.
5. If one object is missing, duplicated, malformed, or carries a malformed activation row, raise `Tightbeam.Schema.ShapeError` with prefix `incompatible_work_item_body_v1`.

The activation performs no `ALTER`, backfill, data inference, spec-reference write, or work-item write. A legacy item has no sidecar row until its body changes.

This is a new instance of the existing `supervision_liveness_v1` additive-activation pattern, not a second activation framework. It reuses the same presence check, normalized exact-SQL validation, one-transaction creation, interruption injection, activation-row validation, and `ShapeError` behavior with the body-specific refusal prefix.

### 2. Domain mutation seam

`Tightbeam.WorkItems.__handle__/3` remains the single mutation seam.

For a call that contains `:body`, the handler performs this sequence inside the existing update transaction:

1. Fetch the work item and its optional body row.
2. If the request also contains `:title`, `:is_bug`, `:spec_ref_name`, or `:spec_ref_sha256`, return `invalid_body_patch` before any write.
3. Validate that the requested body is `nil` or a binary for which `String.valid?/1` is true and `byte_size/1` is at most 65,536.
4. Compare the requested public body value with the stored public body value.
5. If the values differ, upsert body, resolved principal, and current millisecond timestamp.
6. Fetch the body-update response inside the transaction; commit the transaction before returning it.

The handler receives `nil` for a clear and a string for a replacement. Omitted `:body` preserves the body. Each CLI update request includes `:body`.

A raw gateway request that omits `body` follows the pre-existing metadata update path without a body read or write. A request that contains `body` is a body-only request. Combining `body` with a legacy metadata patch field makes `Tightbeam.WorkItems` return `invalid_body_patch` with message `body cannot be combined with title, isBug, specRefName, or specRefSha256` before either path writes. `Tightbeam.Wire.Router` applies its existing default error-status mapping and returns HTTP 400; no router or gateway source edit is required. This subtraction preserves the unchanged raw metadata behavior and prevents a normal-return validation error from committing a partial mixed update.

A no-op clear on a legacy item does not create a sidecar row. A clear after present text stores a null body with clear attribution. This keeps the public absent value simple while preserving the last real change.

The body update response is new and safe to audit:

```json
{
  "workItem": {
    "id": "wi_1",
    "title": "Ship",
    "specRefName": "specs/tightbeam/ship.md",
    "specRefSha256": "<64 lowercase hex>",
    "isBug": false,
    "ownerUserId": "mike",
    "state": "open",
    "failReason": null,
    "createdByUser": "mike",
    "createdBySession": null,
    "createdAt": 1
  },
  "bodyUpdate": {
    "state": "present",
    "byteLength": 4,
    "sha256": "<sha256 of body bytes>",
    "changed": true,
    "updatedByUser": "mike",
    "updatedBySession": null,
    "updatedAt": 2
  }
}
```

For an absent body, `state` is `absent`, `byteLength` is `0`, and `sha256` is `null`. For an empty body, `state` is `present`, `byteLength` is `0`, and `sha256` is the SHA-256 of the empty byte string.

Raw `work-item-update` calls that omit `body` keep their existing flat response shape. This spec adds no CLI route to those legacy metadata fields.

### 3. Detail read projection

`work-item-get` is sufficient. It adds four fields to the nested `workItem` map:

```json
{
  "body": "text or null",
  "bodyUpdatedByUser": "user id or null",
  "bodyUpdatedBySession": "session key or null",
  "bodyUpdatedAt": "millisecond integer or null"
}
```

The handler uses a left join from `work_items` to `work_item_bodies`. It does not write during a read.

The create, update, and list handlers keep body text out of their ordinary work-item maps. `JobTrace`, `WorkState`, `ExecutionMap`, `Toplines`, and device HTTP projections keep their current shapes. These surfaces carry summaries or telemetry, not the editable intent body.

### 4. Audit and doorbell behavior

The accepted body-update result already contains a body descriptor and no body text. The standard accepted `work-item-update` event stores that result with existing origin and principal columns. For a raised `work-item-update` whose call contains `body`, `Tightbeam.Dispatch` stores `%{crash: true, code: "server_error", bodyElided: true}` instead of `Exception.message/1`. Metadata-only update crashes keep their existing audit shape.

`Tightbeam.Dispatch` sanitizes every `work-item-get` outcome before `EventLog` stores it. For success, the caller receives the full handler result while the event payload keeps the baseline work-item and assignment data, removes the four body detail fields, and adds a `bodyRead` descriptor with state, byte length, and SHA-256. For a raised outcome, the event payload is `%{crash: true, code: "server_error", bodyElided: true}` and omits `Exception.message/1`. The existing caller-facing raised error remains unchanged.

The work-item module invokes the existing `on_work_item_change` callback once after a changed body transaction commits. It passes kind `metadata`. It does not invoke the callback for an equal-value update.

The callback retains the existing best-effort contract. A callback failure after commit leaves the body durable and can leave no metadata doorbell. The command does not retry the callback. Making the doorbell atomic with the body would require a broader Gateway callback contract and is declined for this bounded feature.

The accepted verb event and the body transaction retain the existing non-atomic ordering: the body commits first, then `Dispatch` appends the verb event. A process death or event-append failure in that interval can leave a committed body without a verb event and can return an error after the body committed. This spec accepts that named failure because it matches the existing work-item update audit seam. Transactional audit would require a broader Dispatch contract change.

### 5. Authorization

The feature preserves the current transport-first authorization sequence. The wire router resolves or refuses the caller before `Tightbeam.WorkItems` applies its principal rule:

| Credential and explicit identity | Router outcome | WorkItems outcome | HTTP |
| --- | --- | --- | --- |
| Org credential plus `--as-user <user>` | User principal | Get or update allowed | 200 |
| Session credential plus its owner's `--as-user <user>` | User principal | Get or update allowed | 200 |
| Session credential plus a held `--as <role>` or its credential-derived session identity | Session principal | Get or update allowed | 200 |
| Org credential plus `--as-process cron` | Process principal | `process_denied` | 403 |
| Session credential plus `--as-process cron` | `identity_not_yours`; handler not invoked | Not reached | 403 |
| Org credential plus `--as <bound-role>` | Agent origin and missing principal | `principal_required` | 403 |
| Org credential with no identity selector | `invalid_message`; handler not invoked | Not reached | 400 |

The process name `cron` is the canonical non-reserved example. Existing reserved-process and invalid-role transport refusals remain unchanged and occur before the body handler.

The feature adds no owner check. The transport remains responsible for resolving the authenticated principal and origin. The sidecar stores the resolved principal. The event log stores the resolved origin and principal.

### 6. Concurrency and retry behavior

The update transaction is the serialization boundary. Two successful writers use commit order. The later commit defines the current body.

The command has no update idempotency key. A retry with the stored value is a successful no-op. It produces a verb event for the call, produces no metadata doorbell, and preserves body attribution.

### 7. CLI grammar and wire request

Add a Rust command variant whose body value preserves three states at parse time: replacement string, explicit empty string, and clear.

Supported syntax:

```text
tightbeam work-item-update <workItemId> --body <text>
tightbeam work-item-update <workItemId> --body=<text>
tightbeam work-item-update <workItemId> --clear-body
```

The command may also accept one existing identity selector: `--as`, `--as-user`, or `--as-process`. With no explicit selector, the existing credential-derived identity behavior applies.

The parser permits only `body`, `clear-body`, and identity flags on this command. It requires exactly one body operation. It treats `clear-body` as a boolean only inside the command-scoped update parser; the shared global boolean-flag set remains unchanged. The parser must read `--body` by presence, not through `nonempty/2`, because the empty string is a valid body.

The parser must preserve the difference between an explicit empty argv value and a missing argv value: `--body ""` and the one-token argv value `--body=` are empty replacements, while a terminal `--body` has no value and returns the exact command usage text. If replacement text begins with `--`, the caller uses one argv token with the literal prefix `--body=`. Thus `--body=--clear-body` stores `--clear-body`, while the two argv tokens `--body --clear-body` select conflicting body operations and return the exact command usage text.

The inline form and `clear-body` boolean classification are scoped to the exact `work-item-update` command. The inline form recognizes only the exact `--body=` prefix. It does not add a general `--name=value` grammar to other commands, and it does not change how another command consumes a `--clear-body` token. Existing commands keep their tokenization and error behavior. The update parser preserves body-operation occurrence evidence before the shared flag map can overwrite duplicate names. It rejects repeated `--body`, repeated `--clear-body`, and any mix of separated, inline, or clear operations instead of accepting the last occurrence silently.

Replacement request:

```json
{"verb":"work-item-update","params":{"workItemId":"wi_1","body":"text"}}
```

Clear request:

```json
{"verb":"work-item-update","params":{"workItemId":"wi_1","body":null}}
```

The existing identity key appears before `verb` under the CLI's current request builder. The exact identity-specific byte fixtures remain authoritative.

### 8. Error contract

| Condition | CLI or gateway result | HTTP status |
| --- | --- | --- |
| Missing item id, extra positional argument, neither body operation, conflicting or repeated body operations, separated `--body` followed by a flag-looking token, or unsupported flag | Exact CLI usage error; no request | Not applicable |
| Unknown work-item id | `unknown_work_item` | 404 |
| Body is not string or null | `invalid_body` | 400 |
| Body exceeds 65,536 UTF-8 bytes | `invalid_body` | 400 |
| Body combined with a legacy metadata patch field | `invalid_body_patch` | 400 |
| Org credential plus non-reserved `--as-process <name>` | `process_denied` | 403 |
| Session credential plus `--as-process <name>` | `identity_not_yours` | 403 |
| Org credential plus `--as <bound-role>` | `principal_required` | 403 |
| Org credential with no identity selector | `invalid_message` | 400 |
| Malformed additive schema | Boot raises `incompatible_work_item_body_v1` | Not applicable |
| Unexpected handler exception | Existing `server_error` envelope | 500 |

The exact command usage text is: `usage: tightbeam work-item-update <workItemId> (--body <text> | --body=<text> | --clear-body)`.

The command preserves the existing multiple-identity error: `identity flags are mutually exclusive: pass exactly one of --as, --as-user, or --as-process`.

The credential-path messages remain exact:

- `process_denied`: `process principals cannot use work-item verbs`
- `identity_not_yours`: `a session token cannot act as a process`
- `principal_required`: `work-item verbs require a user credential or a session token`
- Missing org-credential identity `invalid_message`: `as (role) or asUser required`

The `invalid_body` message is: `body must be null or valid UTF-8 text of at most 65536 bytes`.

The `invalid_body_patch` message is: `body cannot be combined with title, isBug, specRefName, or specRefSha256`.

### 9. Traceability

| Requirement | Implementation | Verification |
| --- | --- | --- |
| R1-R9, R11, R14-R20, R26 | `lib/tightbeam/work_items.ex` | `test/work_items_test.exs` |
| R10, R12-R13 | `lib/tightbeam/work_items.ex` | `test/work_items_test.exs`, `test/router_test.exs` |
| R21-R23 | Existing router identity seam plus `lib/tightbeam/work_items.ex` | `test/work_items_test.exs`, `test/router_test.exs`, `test/cli_integration_test.exs` |
| R24-R25 | `lib/tightbeam/work_items.ex`, `lib/tightbeam/dispatch.ex` | `test/work_items_test.exs`, `test/dispatch_test.exs` |
| R27-R30 | `lib/tightbeam/schema.ex` | `test/schema_shape_test.exs` |
| R32-R37 | `cli/src/args.rs`, `cli/src/dispatch.rs` | Rust unit tests in those files, `test/cli_integration_test.exs` |
| R38 | No product mechanism; repository verification policy | Lane baseline/produced-commit receipts |
| R39 | Current-main repository law and unchanged `.github/workflows/ci.yml`; no body-feature workflow edit | Exact-`main`-SHA GitHub Actions evidence |
| R40 | `lib/tightbeam/work_items.ex` | `test/work_items_test.exs`, `test/router_test.exs`, `test/dispatch_test.exs` |
| R31, R41 | `scripts/work_item_body_smoke.exs`, existing `Tightbeam.ClientE2E.LegGateway` | Executable reality-smoke report |

### 10. Ordered staffing plan and current custody

The execution-time census found no declared open assignment claim on the paths below. The opener must recheck durable custody before each dispatch and assign each mutation lane with its exact file list. `lib/tightbeam/gateway.ex` needs no feature edit. If implementation later proves that it does, the affected lane stops for a new owner ruling before taking custody or changing the file.

1. **Amended-spec review and implementation-authority hold.** This main-era amendment requires one independent exact-revision `reviewed-clean` verdict. The owner must grant separate implementation authority after that verdict. No implementation assignment opens before both durable gates exist.
2. **Elixir vertical lane, internally ordered.** Files: `lib/tightbeam/schema.ex`, `lib/tightbeam/work_items.ex`, `lib/tightbeam/dispatch.ex`, `test/schema_shape_test.exs`, `test/work_items_test.exs`, `test/dispatch_test.exs`, and `test/router_test.exs`. First add and prove activation. Then add domain and detail behavior. Then add audit redaction and the wire-level mixed-patch and status proofs. Do not edit `lib/tightbeam/gateway.ex`, `lib/tightbeam/wire/router.ex`, `lib/tightbeam/db.ex`, `lib/tightbeam/work_state.ex`, or `lib/tightbeam/client_e2e/leg_gateway.ex` without a new owner ruling.
3. **Rust CLI lane.** Files: `cli/src/args.rs`, `cli/src/dispatch.rs`, their in-file unit tests, and `test/cli_integration_test.exs`. Add only the reviewed command-scoped grammar, request builder, help, and regression fixtures. Preserve every other command's tokenization and byte fixtures.
4. **Aggregate and reality lane.** After lanes 2 and 3 produce green exact commits, assemble them on a clean candidate branch from the then-current green `origin/main`. This lane owns only `scripts/work_item_body_smoke.exs` plus the integration branch. Run the full Elixir and Rust gates on the clean baseline and exact candidate, build the release CLI, and run the real fresh file-backed restart smoke through that binary. Record exact counts, environment hygiene, paths, PIDs, inputs, restart identity, and teardown result.
5. **Whole-change review.** One independent reviewer checks the assembled exact commit against this canonical spec and the baseline, candidate, and reality-smoke evidence. Partial lane review does not satisfy this gate.
6. **Main integration.** Land the whole-change review evidence in the specs repository. Re-resolve remote main. If it differs from the candidate base, rebuild the candidate from the new green tip, rerun the full gate and reality smoke, and obtain a new whole-change exact-commit review. Merge the finished branch to `main` under current repository law. Do not develop or push unreviewed working bytes directly on `main`.
7. **Exact-SHA CI acceptance.** Record the push workflow whose ref is `refs/heads/main` and whose `head_sha` equals the resulting remote-main SHA. The feature does not complete and no release or deployment begins until both `linux` and `macos` test jobs conclude `success` for that exact SHA.

Lanes 2 and 3 may run in parallel only after lane 1 releases both gates. Lanes 4-7 are strictly ordered.

Each source-editing lane applies the repository baseline rule before its first edit. It branches from a recorded green `origin/main` SHA, strips inherited `TIGHTBEAM_*` and `RELEASE_*` variables for ad-hoc Mix commands, runs each applicable gate half exactly as CI defines it, and records the branch, base SHA, environment, exact commands, and each command's exit result. It records pass, failure, and skip counts for each test command. On its exact produced commit, it repeats the same commands in the same environment and records the produced SHA, exit results, and test counts. A missing green-baseline receipt or a red produced-commit gate blocks that lane's handoff.

Repository gate:

```text
cargo build --release --manifest-path cli/Cargo.toml
mix format --check-formatted
scripts/verify_mix.sh
(cd cli && cargo fmt --check && cargo test)
```

Executable reality-smoke harness:

```text
(cd cli && cargo build --release)
TIGHTBEAM_WORK_ITEM_BODY_SMOKE_TEMPLATE=/absolute/path/to/provisioned/template \
TIGHTBEAM_WORK_ITEM_BODY_SMOKE_PORT=12188 \
mix run --no-start scripts/work_item_body_smoke.exs
```

`scripts/work_item_body_smoke.exs` requires both named environment variables and refuses a port below 12000. It creates a uniquely named `<system-temp>/tightbeam-client-e2e-work-item-body-<timestamp>-<unique-integer>` directory with `Tightbeam.ClientE2E.LegGateway.provision!/2`; that operation copies the template's adapters, credentials, homes, and identity but no `state.db`, `gateway.json`, log, or work directory. The script creates `<run-dir>/work`, calls `LegGateway.boot/3` with the repository root and selected port, and stores the current gateway handle before the first assertion.

The script invokes only the absolute built binary `<repo>/cli/target/release/tightbeam` for product commands. Each invocation runs with `<run-dir>/work` as its working directory and `TIGHTBEAM_BASE_DIR=<run-dir>` so no repository or operator `.tightbeam-session` can supply identity or endpoint state. The script uses the fresh org credential to run `add-user smoke-admin --admin`, then uses `--as-user smoke-admin` for `work-item-create`, `work-item-update`, and `work-item-get`. It creates one item pinned to `specs/smoke/work-item-body.md` and digest `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`. It submits one unique body containing spaces, Unicode, quotes, and newlines as one argv value and parses each JSON response with `Tightbeam.JSON`.

For restart proof, the script calls `LegGateway.restart/2`, replaces its stored handle with the returned handle, and reads the item again through the same absolute CLI binary. It checks exact body bytes, user attribution, and both spec-reference values before and after restart. It then stores an empty string, proves empty differs from null, clears the body, and rechecks the spec reference.

One `try`/`after` block owns the gateway from boot attempt through completion. The `after` block calls `LegGateway.teardown/2` on the latest handle. A teardown error is a smoke failure and keeps the reported run directory when the existing lifecycle seam says removal is unsafe. The harness does not extend `scripts/feature_smoke.exs`: that script attaches to a configured gateway and uses raw HTTP, so it cannot prove this feature's fresh-gateway built-CLI path. Deleting the reality smoke loses the only real restart and CLI-I/O proof; accepting the gap would make R31 unverified.

Exact-SHA cross-platform acceptance gate:

1. Before implementation staffing, record the exact reviewed amendment and separate owner implementation authority. Verify the current green `origin/main` tip still uses `[main]` for `on.push.branches`, `refs/heads/main` for its release guard, and the jobs named `linux` and `macos`. Make no body-feature edit to the workflow. If either authority is absent, main is red, or the workflow shape differs, create no implementation assignment.
2. After local gates, reality smoke, exact-commit whole-change review, and specs-repository review-evidence landing pass, merge the finished branch to `main` under current repository law.
3. Record the `push` workflow run whose ref is `refs/heads/main` and whose `head_sha` equals the resulting remote-main SHA.
4. Require both test-matrix jobs named `linux` and `macos` to conclude `success` in that run.
5. Record the run id or URL, job names, conclusions, printed Elixir and Rust versions, and the exit result for `cargo build --release`, `mix format --check-formatted`, `scripts/verify_mix.sh`, `cargo fmt --check`, and `cargo test`; record pass, failure, and skip counts for both test commands on both platforms.
6. Keep the feature incomplete and block release and deployment when a job is skipped, canceled, stale-SHA, platform-missing, or failed.

Reality-smoke assertions performed by `scripts/work_item_body_smoke.exs`:

1. Start a fresh file-backed gateway through the repository's supported smoke harness.
2. Create a work item with a pinned spec reference through the built Rust CLI.
3. Store a body with spaces, Unicode, quotes, and newlines through the built Rust CLI.
4. Read the body through the built Rust CLI and compare exact UTF-8 bytes.
5. Stop and restart the gateway on the same database.
6. Read the body again and compare bytes, attribution, and spec-reference values.
7. Store an empty body and prove it differs from null.
8. Clear the body and prove spec-reference values remain unchanged.

### 11. Operating-pattern effect

This feature teaches no new agent operating pattern. Existing work-item guidance can mention the supported update command after the product ships. That guidance change is outside this spec.

## Acceptance

AC1 — Legacy read:

- Given a baseline stamped database with a work item and no body objects,
- When the new build starts and a caller runs `work-item-get`,
- Then schema activation succeeds, the item returns `body: null`, and the `work_items` row is byte-identical.

AC2 — Exact replacement:

- Given a pinned work item,
- When a user stores `"  Scope\n✓ \"ship\"\n"`,
- Then get returns the exact UTF-8 bytes and the pinned name and digest do not change.

AC3 — Empty versus absent:

- Given one legacy item and one item updated with an empty body,
- When a caller gets both,
- Then the legacy body is null and the updated body is an empty string.

AC4 — Clear attribution:

- Given present body text,
- When a session principal clears it,
- Then get returns a null body, the session key as updater, and a non-null update time.

AC5 — Boundary validation:

- Given valid UTF-8 bodies of 65,536 and 65,537 bytes,
- When a caller submits each,
- Then the first succeeds and the second returns `invalid_body` without changing the first.

AC6 — No-op:

- Given stored body `same`,
- When a caller stores `same` again,
- Then the update descriptor reports `changed: false`, attribution stays fixed, and no metadata doorbell appears.

AC7 — Lifecycle independence:

- Given open, iceboxed, closed, and failed work items,
- When an authenticated caller replaces each body,
- Then each state and failure reason remains fixed.

AC8 — Last commit wins:

- Given two concurrent updates with bodies `A` and `B`,
- When B commits after A,
- Then get returns B and both transactions return without a partial row.

AC9 — Audit redaction:

- Given a unique body sentinel,
- When a caller updates and gets the item through successful, denied, and injected raised paths,
- Then responses contain the body only where specified and no event payload contains the sentinel or a body-bearing exception message.

AC10 — CLI closure:

- Given the supported update forms,
- When Rust parser and byte-builder tests run with ordinary, empty, clear, `--body=--clear-body`, and `--body=--body` inputs,
- Then each accepted form produces the exact request bytes and preserves its literal value.
- When the tests run with `--body --clear-body`, repeated separated or inline body operations, terminal `--body`, an unsupported metadata flag, and existing non-update baseline fixtures containing `--name=value` and `--clear-body next`,
- Then each invalid update exits with the exact usage and sends no request, while each existing command's result matches its pre-feature fixture.

AC11 — Restart durability:

- Given the dedicated harness has provisioned a state-free file-backed gateway and stored a body through `<repo>/cli/target/release/tightbeam`,
- When `Tightbeam.ClientE2E.LegGateway.restart/2` stops and boots the gateway on the same run directory and port,
- Then a real CLI get returns the same body bytes, attribution, and spec reference.

AC12 — Whole product:

- Given this exact main-era amendment is reviewed-clean, the owner grants separate implementation authority, each implementation lane records its exact green `origin/main` baseline and produced-commit receipt, and one assembled candidate commit has passed the real smoke and whole-change review,
- When the aggregate verifier runs both local gate halves and the exact `scripts/work_item_body_smoke.exs` command, then the local runs pass and the immutable report names each baseline SHA, produced SHA, exact command, environment, command exit result, each test command's pass, failure, and skip counts, the template path, selected port, built CLI path, run directory, gateway PIDs before and after restart, teardown result, and each smoke input.
- When the whole-change review evidence lands in the specs repository, the finished branch merges to `main` under current repository law, and the existing main-targeted GitHub Actions workflow runs on the push, then its ref is `refs/heads/main`, its `head_sha` equals the resulting remote-main SHA, and both jobs named `linux` and `macos` conclude `success` after printing toolchain versions, building the release CLI, and running the Mix and Rust gates.
- Then the immutable report also names the workflow run id or URL, both job conclusions, each gate result, and each test command's pass, failure, and skip counts before the feature completes.

AC13 — Raw metadata compatibility:

- Given a work item with a present body,
- When a raw caller updates title, `isBug`, or the existing spec-reference pair while omitting `body`,
- Then the pre-existing flat update response shape remains unchanged and the body plus attribution remain byte-identical.

AC14 — Raw update separation:

- Given an existing work item and one raw request containing a valid body plus `title`, `isBug`, `specRefName`, or `specRefSha256`,
- When the handler receives the request,
- Then it returns `invalid_body_patch` before any write, records no submitted body text in the denied event, and preserves the body, attribution, and legacy metadata fields.
- When the same request crosses the wire,
- Then the router returns HTTP 400.

AC15 — Credential-specific authorization:

- Given an org credential and `--as-process cron`, when a caller runs get and update, then each returns `process_denied` with HTTP 403; get exposes no body and update preserves the stored body.
- Given a session credential and `--as-process cron`, when a caller runs get and update, then each returns `identity_not_yours` with HTTP 403 before `Tightbeam.WorkItems` runs.
- Given an org credential and `--as <bound-role>`, when a caller runs get and update, then each reaches `Tightbeam.WorkItems` with an agent origin and missing principal and returns `principal_required` with HTTP 403.
- Given an org credential and no identity selector, when a caller runs get and update, then each returns `invalid_message` with HTTP 400 before `Tightbeam.WorkItems` runs.

## Open Questions

OQ1 — **RESOLVED: current-main authority and evidence contract named.** Owner ruling `att_be83756f-1f59-4d2c-bd6c-cd5da5e311f5` and immutable ruling `art_7d8f7444` authorize this bounded policy amendment and one linked exact-revision review. Execution-time `origin/main` `8d0baa789c4aea1513a6d77ed53a6d54d76d1fb6` is the amendment evidence pin, not a permanent implementation tip. Its complete `.github/workflows/ci.yml` has SHA-256 `1ccc8176ca9a8b9c2a677eaf31723e3c9602f6790ed8baccb945a5bc2d000e57`, triggers on pushes to `main`, uses release guard `refs/heads/main`, and runs test jobs named `linux` and `macos`.

Each later implementation lane must start from the then-current green `origin/main` after this amendment is reviewed-clean and the owner grants separate implementation authority. The body feature makes no `.github/workflows/ci.yml` edit. Current repository law requires work on a branch, a green full gate, review evidence in the specs repository, and merge of the finished work to `main`. This resolution removes the obsolete maintenance-branch prerequisite and cross-line integration topology. It does not authorize implementation, binding, completion, merge, deployment, custody change, or disposition.

Owner-authorized review findings B1 and I1 remain closed: the spec contains no body-feature CI mutation prescription, and the command-scoped `--body=<text>` literal spelling plus parser tests remains unchanged.

Implementation may choose private function names. It may not change field names, storage semantics, response shapes, limits, authorization, audit redaction, dependency order, or acceptance behavior without amending this canonical file first.
