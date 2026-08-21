# Lachesis provider usage window drift

Status: review-ready  
Work item: `wi_a0a41827-6282-4e9c-8997-354fcb4931ce`  
Authority: `art_95c6a05a` at SHA-256 `3198b102913dfdb95f66cc89cbe4b80b7d990149a73586e6015599144d80c289`; `art_10c08c43` at SHA-256 `c3ec07fe8a724876509935b31c624d026300fd4702c2070d6ba57eb0e50e4c0c`; Spirit rulings `att_3a8a7ecf-226e-4d52-8ad7-17c9879d3659` and `att_c545a057-74b5-4b32-b65c-1849aac4ccb1`; deployed base `8eedd020607995f9df9ab7c937b96917c0470122`.

## Goal

Keep each valid recognized Codex or Claude usage window usable when another candidate window is invalid or unrecognized. Each provider adapter preserves the accepted response unchanged in `raw`, omits the unusable candidate from normalized `windows`, and reports the omission through a fixed public-safe diagnostic.

One unusable candidate does not fail its account or the multi-account aggregate when a valid recognized window remains. A response with no valid recognized window fails closed.

## Non-Goals

- Infer a new normalized mapping for a provider structure that has no existing adapter mapping. Such a structure remains visible in `raw` and produces a diagnostic.
- Change credential parsing, refresh, login, adoption, cancellation, active-job locking, provider-home lifecycle, caching, account aggregation, or provider request behavior.
- Close the Claude paste-code onboarding gap. That separate work is iceboxed as `wi_e0aa150c` with artifact `art_3b06d88d`.
- Add server-side ranking, history, alerts, diagnostic persistence, logs, or inference.
- Put an unsanitized provider response, account or subscription identifier, request metadata, provider-home path, credential, label, plan name, timestamp, balance, reset time, usage value, or unknown free-form provider string in the repository or public history.
- Call a provider, inspect credential or provider state, adopt an account, or touch the running service while producing or reviewing this spec.
- Change the fatal behavior for invalid top-level JSON, a non-object top level, or raw data rejected by the credential-field safety scan.
- Establish an operating-manual pattern. This repair establishes only the adapter pattern named under Architecture.

## Terms

- **Candidate window:** a value in a provider location that the adapter already treats as a possible usage window. Codex candidate locations are `rate_limit.primary_window`, `rate_limit.secondary_window`, and each `additional_rate_limits` entry. Claude candidate locations are `five_hour`, `seven_day`, `seven_day_sonnet`, and each member of `limits` when that container can be enumerated.
- **Recognized window:** a candidate whose shape has an explicit normalized mapping in the deployed adapter. For Codex, this is the existing `used_percent` window mapping. For Claude, this is the existing `utilization` bucket mapping for fixed buckets and map-form `limits` members.
- **Valid recognized window:** a recognized window whose required numeric value is present and in range and whose present optional fields decode to their existing types. Codex `used_percent` is from 0 through 100 inclusive. Claude `utilization` is from 0 through 1 inclusive.
- **Unusable candidate:** an invalid recognized window, an enumerated candidate with no recognized mapping, or a valid candidate whose normalized ID collides with an ID already retained from an earlier candidate.
- **Unrecognized container:** a present candidate-window container whose shape the adapter cannot enumerate using an existing mapping. It counts as one unusable candidate.
- **Raw provider data:** the exact JSON bytes accepted by the existing credential-field safety scan and returned as `UsageSample.raw`.
- **Diagnostic:** a derived item in `UsageSample.diagnostics` with exactly `code` and `message` string fields. It is neither an API error nor persisted state.
- **Fatal contract error:** an `UPSTREAM_CONTRACT_CHANGED` result with no `UsageSample`.
- **Codex window order:** retained primary, retained secondary, then valid additional entries sorted by decoded `name` ascending with source order breaking equal-name ties.
- **Claude window order:** retained `five_hour`, `seven_day`, and `seven_day_sonnet`, in that order, then retained map-form `limits` members sorted by their existing map key.
- **Diagnostic order:** Codex primary, secondary, then additional source order; Claude fixed-bucket order, then sorted map keys or array source order. An unrecognized container occupies its candidate location once.

## Assumptions

- Deployed commit `8eedd020607995f9df9ab7c937b96917c0470122` preserves isolated provider homes across failed verification.
- Production cancellation succeeds and releases the active-job lock.
- Multiple isolated Codex credentials remain preserved after failed verification. Preserved Codex and Claude homes become eligible for authorized API adoption only after this repair is reviewed and redeployed.
- Both adapters already preserve an accepted raw usage response byte-for-byte in `UsageSample.raw`.
- The existing raw-usage safety scan runs before normalization and remains authoritative for credential-bearing fields.
- The current aggregate already isolates account errors and returns successful accounts beside failed accounts.
- A later builder, not this spec lane, may make separately authorized read-only usage calls for fixture capture and deployment verification.
- The separate Claude paste-code onboarding gap does not block explicit-home API adoption or this adapter repair.
- Lachesis tree execution remains Codex-only: each session and descendant session uses harness `codex`, and each spawn explicitly selects `--harness codex --model gpt-5.6-sol` instead of relying on an archetype default.

## Invariants

### INV-1 — Raw truth survives local degradation

Each provider adapter copies accepted provider JSON unchanged to `UsageSample.raw` when it returns a sample. Omitting an unusable candidate from normalized `windows` does not remove or rewrite that candidate in `raw`.

### INV-2 — Window drift degrades locally

Each provider adapter evaluates candidate windows independently. It omits an unusable candidate and continues processing candidates that it can evaluate. When at least one valid recognized window remains, the returned sample carries one provider-fixed diagnostic per omitted candidate. An unusable candidate alone does not produce an account error.

### INV-3 — The safety floor remains closed

After top-level JSON and raw-safety checks pass, each provider adapter returns `UPSTREAM_CONTRACT_CHANGED` and no sample when zero valid recognized windows remain. It does not infer headroom from an unrecognized structure.

### INV-4 — Diagnostics disclose no provider material

In a successful degraded sample, each omitted Codex candidate produces exactly:

```json
{"code":"CODEX_USAGE_WINDOW_OMITTED","message":"Codex omitted an invalid or unrecognized usage window."}
```

In a successful degraded sample, each omitted Claude candidate produces exactly:

```json
{"code":"CLAUDE_USAGE_WINDOW_OMITTED","message":"Claude omitted an invalid or unrecognized usage window."}
```

Each diagnostic has no other field. Its fields do not derive from the response. A diagnostic contains no response fragment, source field or JSON path, candidate name, normalized ID, source position, account or request identifier, provider-home path, plan, timestamp, balance, reset time, or usage value. Diagnostics use diagnostic order.

When zero valid recognized windows remain, the adapter returns no sample and therefore no per-candidate diagnostic array. The fatal teaching error in INV-7 is the public-safe account-level report for that path.

### INV-5 — Retained IDs and order are deterministic

Each adapter preserves its provider order and existing ID and display-name rules for retained candidates.

A retained unnamed Codex additional entry uses its original one-based source position in its ID and display name. Omitted entries do not renumber it. For named Codex entries whose existing slug-derived IDs collide, the adapter retains the first valid entry in Codex window order and omits later colliding entries.

For Claude candidates whose existing IDs collide, the adapter retains the first valid entry in Claude window order and omits later colliding entries. Only retained candidates reserve IDs. Repeated normalization of the same raw JSON produces the same ordered `windows` and the same number and sequence of fixed diagnostics.

### INV-6 — Diagnostics do not change account or aggregate status

A sample with diagnostics and at least one valid recognized window is successful. Direct usage returns the existing successful result shape. Aggregate usage keeps the account in its existing `live`, `cache`, or `stale` status and does not increment `error` because of a diagnostic.

If normalization returns the fatal contract error and no cached sample exists, direct usage returns the existing HTTP 502 error envelope and aggregate usage returns HTTP 200 with that account at `status: "error"`. Other account results remain present. If a cached sample exists, the existing cache policy may return it as `stale` beside the current error.

### INV-7 — Fatal errors remain teachable and public-safe

The zero-valid-window failure has:

- `code`: `UPSTREAM_CONTRACT_CHANGED`
- `prerequisites`: one unmet `VALID_RECOGNIZED_WINDOW` prerequisite whose description is `The provider response contains at least one valid recognized usage window.`
- `state`: only `provider`, set to `codex` or `claude`
- `remedy.summary`: `Retry the exact call. If the error repeats, update Lachesis before trusting provider usage.`
- `remedy.calls`: an empty array
- `remedy.commands`: `["retry the exact call"]`
- `help`: `/api/v1/help/usage`

Its provider-specific message is:

- Codex: `Codex usage contained no valid recognized limit window.`
- Claude: `Claude usage contained no valid recognized limit window.`

The adapter-level error adds no response fragment, source field or JSON path, candidate name, normalized ID, source position, account or request identifier, provider-home path, plan, timestamp, balance, reset time, or usage value. Existing core and API envelopes may add their already-public account and request context.

### INV-8 — One derived mutation seam per provider

Codex normalization is the only producer of Codex window diagnostics. Claude normalization is the only producer of Claude window diagnostics. The model carries diagnostics with the sample; core aggregation, caching, and API encoding pass them through without deriving, editing, logging, or persisting them separately.

## Architecture

The named pattern is **adapter-local window degradation**. It applies to candidate-window extraction and normalization in the Codex and Claude adapters. It does not apply to arbitrary unknown top-level fields, raw-data safety, credential operations, job lifecycle, account aggregation, or onboarding.

Each adapter isolates candidate decoding from top-level decoding. A wrong type in one candidate cannot abort decoding of a sibling candidate. An enumerable unrecognized candidate produces one fixed diagnostic. An unrecognized container that cannot be enumerated produces one fixed diagnostic. Arbitrary fields outside candidate locations stay raw-visible and do not produce diagnostics.

The Codex adapter applies the pattern to primary, secondary, and additional candidates. It preserves the existing deterministic synthetic IDs for unnamed additional entries and the existing order for retained windows.

The Claude adapter applies the pattern to fixed buckets and the `limits` container. It combines valid recognized fixed buckets with valid recognized map-form `limits` members instead of allowing one present container to suppress valid siblings. An enumerable `limits` member without an existing mapping stays raw-visible, is omitted, and produces the fixed Claude diagnostic.

`UsageSample` gains a `diagnostics` array. Successful Codex and Claude samples encode an empty array when no diagnostic exists. This additive field is the only API schema change.

Production evidence already closes adjacent lifecycle questions: cancellation releases the active-job lock, and failed verification preserves isolated provider homes. Therefore this spec changes neither job locking nor provider-home lifecycle. The iceboxed Claude paste-code gap remains outside this work item.

ADD wins because deleting normalized provider windows would hide routing headroom, while accepting account-wide failure for one unusable candidate would violate the binding repair contract. Accepting zero recognized windows as success loses because it can report misleading headroom.

## Acceptance

### AC-1 — Mixed Codex candidates degrade locally

Given a synthetic Codex response with one valid recognized window, one additional candidate with no `used_percent`, one additional candidate with a wrong JSON type, and one valid named additional candidate, when the adapter normalizes the response, then it returns the valid windows in Codex window order, omits the two unusable candidates, preserves raw bytes exactly, emits two exact Codex diagnostics, and returns no error.

### AC-2 — Mixed Claude candidates degrade locally

Given a synthetic Claude response with one valid fixed bucket, one invalid recognized bucket, and one enumerable unrecognized `limits` member, when the adapter normalizes the response, then it returns the valid fixed window, omits the two unusable candidates, preserves raw bytes exactly, emits two exact Claude diagnostics, and returns no error.

### AC-3 — Unrecognized containers cannot erase valid siblings

Given a synthetic response for either provider with one valid recognized window and a present candidate-window container whose shape the adapter cannot enumerate, when the adapter normalizes the response, then it keeps the valid window, preserves the container in raw data, emits one exact provider diagnostic, and returns no error.

### AC-4 — Zero valid recognized windows fails closed

Given a synthetic response for either provider with candidate locations present but no valid recognized window, when the adapter normalizes the response, then it returns no sample, returns no per-candidate diagnostic array, and returns the exact provider-specific `UPSTREAM_CONTRACT_CHANGED` detail from INV-7.

### AC-5 — IDs and order stay deterministic and collision-free

Given valid retained candidates separated by unusable candidates and candidates whose existing normalized IDs collide, when the same raw JSON is normalized twice, then both ordered window lists match, both diagnostic sequences match, omitted candidates do not renumber an unnamed Codex entry, the first valid colliding candidate is retained, and retained IDs contain no duplicate.

### AC-6 — Diagnostic content is fixed and public-safe

Given an unusable synthetic candidate containing sentinel strings, when either adapter returns a degraded sample, then no sentinel appears in diagnostics, errors, logs, or test output, and each diagnostic JSON has only the exact `code` and `message` fields from INV-4.

### AC-7 — Aggregate behavior remains per-account

Given registered synthetic Codex and Claude accounts where one returns a degraded sample with a valid window and one returns the zero-valid-window failure, when a caller reads aggregate usage, then the API returns HTTP 200, keeps the degraded account out of the `error` count, represents the failed account under the existing cache policy, and retains both result slots in registry order.

### AC-8 — Existing safety regressions stay green

Given the implementation commit, when the builder runs adapter and service tests, then existing invalid-top-level-JSON, unsafe-raw, valid-raw preservation, aggregate isolation, cache, credential-preservation, cancellation, and active-job-lock tests pass without weakening their assertions.

### AC-9 — Repository gates pass

Given the implementation commit, when the builder runs `go test -race ./...`, `./scripts/scan-fixtures.sh`, `./scripts/offline-smoke.sh`, and `./scripts/verify.sh` from the repository root, then each command exits zero. Test output, fixtures, and smoke logs contain no unsanitized provider body, identifier, private path, plan name, timestamp, balance, reset time, usage value, or unknown free-form provider string.

### AC-10 — Sanitized-real fixtures prove both observed shapes

Given separate authorization for one read-only Codex usage call and one read-only Claude usage call, when the later builder captures each response in a private temporary workspace, then the builder sanitizes one fixture per provider before it enters the repository. Sanitization replaces account and subscription identifiers, request metadata, operator-linked timestamps, identifying plan names, balances, usage values, reset times, and unknown free-form strings with deterministic synthetic values while preserving the structural keys, value types, nesting, optionality, and window shapes needed by the adapter tests.

When the builder verifies the sanitized fixtures, then `./scripts/scan-fixtures.sh` exits zero, a human-readable diff against the sanitizer rules shows no prohibited value, and an independent reviewer approves the fixture. A hand-written ideal fixture does not satisfy this clause.

The capture procedure owns every unsanitized capture from creation through confirmed removal. On success, capture failure, sanitizer failure, cancellation, or a caught interruption, it attempts removal before completing that exit. At the start of any later capture or fixture-work continuation, it removes any residual unsanitized capture from the designated private capture workspace before any other fixture step. If removal cannot be confirmed, the procedure reports cleanup failure, the builder remains the named owner of the residue, and no repository commit, fixture artifact, fixture or test log, review handoff, or further fixture step may proceed until removal is confirmed. Before ending the turn, the builder records a public-safe blocker receipt with the provider name, pass/fail outcome, owner, and next cleanup deadline or scheduled continuation. The receipt contains no capture path or provider material.

Given each normal and caught abnormal exit above with operable cleanup, when the capture procedure completes that exit, then no unsanitized capture remains. Given forced cleanup failure, when the procedure exits, then it reports cleanup failure, records the bounded owner receipt, and blocks every downstream action named above. Given a simulated uncatchable termination that leaves a residual capture, when fixture work resumes, then the residual capture is removed before any other fixture step. These teardown checks run for both providers, use only synthetic sentinel captures, and make no provider call.

### AC-11 — Reviewed redeploy and authorized API adoption prove reality

Given a reviewed implementation based on deployed commit `8eedd020607995f9df9ab7c937b96917c0470122`, when the orchestrator deploys it on Gibson and receives separate authorization to adopt one preserved isolated Codex home and one preserved isolated Claude home through the API, then both adoptions succeed without moving, copying, deleting, or refreshing a credential. A read-only usage call for each adopted account returns at least one normalized valid recognized window, preserves each unusable candidate in unchanged raw provider data, emits the provider's fixed diagnostic for each omitted candidate, and does not fail the multi-account aggregate.

Deployment evidence records only the reviewed commit, fixed codes, pass/fail outcomes, and commands with sensitive arguments removed. It records no home path, label, account or subscription identifier, request metadata, response body, plan, timestamp, balance, reset time, usage value, or unknown free-form provider string.

## Open Questions

None. No blocking or non-blocking product hole remains for this MVP repair.
