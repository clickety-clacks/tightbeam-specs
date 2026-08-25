# Codex session usage capture

Status: digest-complete amendment after exact-revision F4 report `art_10c8b110`; targetless and unbound; independent review lane closed
Work item: `wi_c6589a66-33e2-43f3-ab84-1b21a5b8c6cf`
Tightbeam source base: `3fe0e941840ed138a6a285261c0e35687d8d27a3`
Codex source base: `ba6cf9c69277caec51a4c12c5b7401a9920930e0`
Clawline source base: `bbb6de019bed4ec511c0bd4b6463073831ea2107`
Integration target: none
Work-item binding: none
Authority: `att_fae41482-848b-40c1-a8da-b1daf68e3c75`, `art_0b820dfb`, `att_08edcb9c-33d9-4039-bd3e-41562c965ec1`, `att_771854c7-8817-4540-8d73-43136199d673`, review `att_f7e808e7-dcf3-4c25-8d2a-ff0ccad16eca`, exact-revision F4 clause table `art_10c8b110`, and closed-lane refusal `art_fd676254`

## Spec Homing

Canonical home: `github:clickety-clacks/tightbeam-specs/codex-session-usage-capture-v1.md`.

Authority set: exactly this Spec Homing declaration plus the Goal, Non-Goals, Terms, Assumptions, Invariants, Architecture, Acceptance, and Open Questions sections in this canonical file. The header's authority records and source-base pins provide provenance and evidence; they are not alternate contracts. A workdir copy, artifact pointer, conversation, producer branch, or review report does not override this file.

Binding authority: none. This candidate remains targetless and unbound. It becomes implementation authority only after an independent `reviewed-clean` verdict and an explicit work-item binding record the canonical path and its SHA-256. A material amendment supersedes the prior candidate bytes at this same canonical home.

## Goal

Tightbeam shall expose the authenticated account mode and a sanitized, normalized projection of real Codex rate-limit responses through its existing session-status response. The projection shall preserve the optional wire shape that OpenClaw and Clawline already consume. Provider capture shall occur at the adapter boundary, and session-status reads shall remain non-blocking.

The pattern established here is **provider-captured usage generation**: capture provider truth once at the adapter boundary, publish only a binding-current sanitized generation, and label loss rather than infer quota. It applies only to Codex account-metadata projection in Tightbeam. It does not establish general provider accounting, budget, readiness, or presentation policy.

## Non-Goals

- This spec does not change Clawline or OpenClaw.
- This spec does not invent, estimate, or expose Claude quota. Claude sessions have no `codexUsage` member.
- This spec does not expose Codex quota for API-key sessions.
- This spec does not add an endpoint, database record, usage history, budget decision, alert, polling timer, or provider-facing HTTP call from the Gateway.
- This spec does not retain or log a raw provider response.
- This spec does not read live credentials, account tokens, or provider cookies outside the existing adapter connection.
- This spec does not normalize provider windows other than the two durations defined below.
- This spec does not target an integration branch, bind a work item to a revision, release, or deploy.
- This spec establishes no operating pattern. It adds one capability at an existing boundary.

## Terms

- **Account mode** is the public `display.authMode` value derived from Tightbeam's resolved credential kind: `apiKey` maps to `"api_key"`, `subscription` maps to `"oauth"`, and `none` maps to `null`.
- **Adapter key** is Tightbeam's existing `{harness, archetype, host}` identity for one adapter lane. The same key remains stable when Tightbeam replaces that lane's running adapter process.
- **Adapter incarnation** is an opaque, process-local identifier for one running adapter process on an adapter key. An adapter restart creates a new incarnation without changing the binding generation when the resolved credential binding is unchanged.
- **Eligible binding** is a Codex adapter/account binding that uses Tightbeam's `subscription` credential kind. A Claude binding and a Codex API-key binding are not eligible. Provider account health and rate-limit failures do not change binding eligibility or account mode; they change only usage freshness or availability under Failure mapping.
- **Terminal account invalidation** is the existing typed `:terminal` output produced only when Tightbeam's Codex auth-event classifier receives `account/updated` parameters, directly or through forwarded `_meta.codex.accountUpdated`, with both `authMode: null` and `planType: null`. The adapter already sends this output to Tightbeam's credential path; the usage cache consumes the same typed output without receiving the raw event. A recognized non-null auth mode, an unknown or malformed account-update shape, and every rate-limit JSON-RPC error are non-terminal for this projection. Provider error codes and message strings are never terminal evidence.
- **Binding generation** is an opaque, process-local identifier for one adapter key and resolved credential binding. It contains no provider account identifier and is unique within one Gateway process. It remains unchanged across adapter restarts while that credential binding remains unchanged. A change in the resolved credential binding, terminal account invalidation, or a Gateway restart creates a new binding generation. The public `metadataContextGeneration` value is this identifier's wire representation.
- **Full snapshot** is a successful Codex app-server `account/rateLimits/read` response for the `codex` limit.
- **Sparse update** is a Codex app-server `account/rateLimits/updated` notification. Missing or null fields mean “no new value”; they do not erase a value from a full snapshot.
- **Recognized window** is a provider window whose `windowDurationMins` is exactly `300` or `10080`. Tightbeam labels those values `"5h"` and `"Week"`, respectively.
- **Valid window** is a recognized window whose `usedPercent` is an integer from 0 through 100 and whose `resetsAt`, when present, is an integer Unix timestamp in seconds. Its projection has `remainingPercent = 100 - usedPercent` and converts `resetsAt` to Unix milliseconds. Tightbeam does not clamp or estimate invalid values.
- **Usage generation** is one immutable, sanitized projection accepted for one binding generation. It contains the capture source (`read` or `update`), a local mutation sequence, `fetchedAt` in Unix milliseconds, and one or two valid projected windows. It contains no raw response or provider identity. Loading and unavailable states contain no usage generation.
- **Capture claim** is the binding generation, adapter incarnation, and refresh identifier recorded when a full read starts. A completion shall publish only while all three values match the current claim.
- **Fresh** means that the latest accepted capture for the current binding has at least one unelapsed valid window and no later refresh is pending or has failed.
- **Stale** means that a prior accepted capture for the current binding is being retained because a later refresh is pending, has failed, cannot run because the adapter is unavailable, or was requested after Tightbeam observed an elapsed reset. Stale labels the retained provider values; it does not assert that their percentages remain current.
- **Unavailable** means that the current binding has no prior accepted capture and no full read in flight. Its reason is one of `account_binding_unavailable`, `provider_unavailable`, `timeout`, or `invalid_usage`.
- **Loading** means that the binding is eligible, has no accepted snapshot, and has one full read in flight.

## Assumptions

- Tightbeam source commit `3fe0e941840ed138a6a285261c0e35687d8d27a3` is the implementation authority reconciled for this draft. Its Gateway returns `display.authMode: null` and no `codexUsage` member. Its only delta from the prior reviewed source pin is supervision-delivery revalidation; that delta does not touch session status, adapter metadata, credentials, or usage.
- Codex source commit `ba6cf9c69277caec51a4c12c5b7401a9920930e0` defines `account/rateLimits/read` and `account/rateLimits/updated`. A read requires ChatGPT authentication. The wire values include `usedPercent`, optional `windowDurationMins`, optional `resetsAt`, and provider account fields that are outside this projection.
- That Codex source uses the same invalid-request class for a missing login and a non-ChatGPT login, and uses internal error for both backend failure and an empty snapshot. Those rate-limit failures do not identify a terminal account state. Its `account/updated` notification carries optional `authMode` and `planType`; its documented logout shape sets both to null.
- The reconciled Tightbeam source already classifies only that exact null/null account-update shape as `:terminal` credential evidence. It classifies recognized non-null modes as `:transient` and every other shape as `:unknown`, then passes non-unknown outputs to the configured auth-event callback. This spec reuses that typed output and does not add a usage-specific auth classifier.
- The installed `@agentclientprotocol/codex-acp` 1.1.4 adapter receives `account/rateLimits/updated` but does not forward that event to Tightbeam. An implementation therefore changes the adapter seam before Tightbeam can capture the event.
- Clawline source commit `bbb6de019bed4ec511c0bd4b6463073831ea2107` accepts optional top-level `metadataContextGeneration`, optional `display.authMode`, and optional `display.codexUsage` in the shape specified below. It renders usage only when `authMode` is `"oauth"` and retains cached usage only for the same metadata generation.
- The existing authorization and visibility rules for `/api/session-status` remain the authority for who may read this projection.
- Reconciliation found no implementation delta on the preserved producer branch. This spec does not adopt or replace unreviewed producer bytes.
- No lawful live provider body was captured during reconciliation. The implementation gate therefore requires a real, sanitized fixture before completion can be claimed.
- Mike's lane ruling authorizes this adapter-capture-cache design without a new operator decision because it changes neither spending nor product scope.

## Invariants

1. **I-01 — Adapter provenance.** Provider truth enters Tightbeam only through the existing Codex adapter connection. The Gateway shall obtain usage without calling a provider endpoint or reading a credential.
2. **I-02 — Raw-response lifetime.** The adapter boundary shall discard the raw provider response after normalization. Durable storage, artifacts, logs, crash reports, and process status shall contain only the sanitized fixture or normalized projection defined here.
3. **I-03 — Cache contents.** The cache shall contain only normalized window values, local provenance, freshness state, and the local binding generation.
4. **I-04 — Unsupported absence.** Tightbeam shall expose `display.codexUsage` only for an eligible Codex binding. Unsupported providers, missing credentials, Claude bindings, and Codex API-key bindings shall omit the member rather than emit `null` or a fabricated value.
5. **I-05 — No inferred windows.** One valid provider window produces one projected window. A provider response with zero valid windows produces `unavailable` with reason `invalid_usage` only when the current binding has no prior accepted capture. With a prior accepted capture, Tightbeam retains that capture as stale and records the invalid outcome.
6. **I-06 — Non-blocking status.** A session-status request shall read or atomically advance local cache state without waiting for provider I/O or adapter lifecycle. A read that observes a missing baseline, stale state, or elapsed reset shall atomically join the current capture claim if one exists. If no claim exists and the current adapter is ready to accept the account operation, the read shall create one claim that starts one provider read before returning. If the adapter is not ready, the read shall return stale or unavailable state without creating a claim; the adapter-readiness trigger in Architecture shall request the refresh after recovery.
7. **I-07 — Prompt isolation.** Usage capture shall allow an unrelated prompt to execute concurrently. Metadata completion shall not be a prerequisite for prompt submission or completion.
8. **I-08 — Single mutation seam.** One private mutation seam shall own the binding generation, current adapter incarnation, capture claim, mutation sequence, immutable usage generation, and current capture state. Other components shall submit events to this seam and read its immutable projection.
9. **I-09 — Coalesced current reads.** At most one capture claim shall be current for a binding generation. Concurrent refresh requests shall join that claim and shall not create another provider request. A retired adapter's unresolved provider operation is not a current claim; its completion remains subject to I-11.
10. **I-10 — Atomic generations.** Each capture mutation shall receive a monotonically increasing local sequence at receipt. Readers shall observe either the complete prior generation or the complete next generation.
11. **I-11 — Current-incarnation publication.** Every adapter-originated usage event shall publish only when its binding generation and adapter incarnation match the current cache state. A full-read completion shall also require its refresh identifier to match the current claim. A late completion or sparse notification from a retired adapter, account, or credential binding shall have no public effect.
12. **I-12 — Idempotency.** A replayed full-read completion shall fail its cleared capture claim. A sparse notification whose normalized merge equals the current snapshot shall not create a new public usage generation.
13. **I-13 — Binding transition.** A change in Tightbeam's resolved credential binding or terminal account invalidation shall atomically retire the current capture claim, create a binding generation, clear the old projection, and establish the new binding state before a new full read starts. The usage cache shall consume the existing typed `:terminal` auth classification and shall not classify raw account events independently.
14. **I-14 — Lifecycle retention.** A transient adapter exit shall retire that adapter incarnation and its capture claim, retain a same-binding accepted projection as stale, and leave the binding generation unchanged. The replacement adapter may create a current claim while a retired operation is unresolved. A terminal account invalidation shall perform the binding transition in I-13. A Gateway restart shall clear the in-memory cache and create new binding generations and adapter incarnations.
15. **I-15 — Sparse baseline.** Tightbeam shall accept a sparse update only from the current adapter incarnation and shall merge it only into a full snapshot from the same binding generation. The baseline may have been captured by an earlier incarnation of that unchanged binding. Without such a baseline, Tightbeam shall request a full read and shall not project the sparse update alone.
16. **I-16 — Sparse field semantics.** A sparse update shall replace only fields that it carries. Missing and null fields shall preserve the baseline value.
17. **I-17 — Codex limit selection.** Tightbeam shall prefer `rateLimitsByLimitId["codex"]` when present. It shall otherwise use the historical `rateLimits` member. It shall ignore each other limit identifier. It shall discard `credits`, `individualLimit`, `spendControlReached`, `planType`, `rateLimitReachedType`, `rateLimitResetCredits`, and unrecognized snapshot fields at the adapter boundary.
18. **I-18 — Window order and duplicates.** Projected windows shall appear in `"5h"`, then `"Week"` order. Provider order is primary window, then secondary window. If both valid windows map to one label, the first one wins and observability records an invalid duplicate.
19. **I-19 — Reset observation.** When a status read observes that any projected window has a non-null `resetAt` less than or equal to the injected current time, Tightbeam shall apply the refresh rule in I-06 and return the complete prior accepted capture as stale without waiting. Reset observation shall not change the binding generation, drop a window, or emit `reset_elapsed`. Only a later accepted provider capture or a binding transition may replace or clear the retained windows.
20. **I-20 — Event-derived freshness.** Freshness shall change because of an observed capture, refresh, adapter, binding, status-read, or observation that a provider-declared `resetAt` has passed. A locally invented age threshold shall not decide freshness. Tightbeam shall not emit `stale_expired` in this MVP.
21. **I-21 — Account mode is not health.** `display.authMode` reports credential kind. A provider refusal, adapter failure, or terminal account invalidation may make `codexUsage` unavailable while an existing subscription credential continues to report `"oauth"`.
22. **I-22 — Additive compatibility.** Existing session-status fields and meanings shall remain unchanged. The only public additions are optional top-level `metadataContextGeneration`, optional `display.authMode`, and optional `display.codexUsage`.
23. **I-23 — Generation coupling.** A session-status response that contains `display.codexUsage` shall contain `metadataContextGeneration` from the same atomic projection. A change in the resolved credential binding or terminal account invalidation shall change the emitted generation before Tightbeam exposes state for the new binding.
24. **I-24 — Cache scope.** Sessions on one adapter key and binding generation shall share one cache entry. Sessions on distinct adapter keys shall use distinct entries.
25. **I-25 — Failure reasons.** Tightbeam shall map an unavailable state to the one observed cause listed under Failure mapping only when the current binding has no prior accepted capture. Only the typed terminal account invalidation may produce `account_binding_unavailable`; it shall first perform the generation transition in I-13, so the new generation has no prior capture. For each non-terminal cause, a same-binding accepted capture shall remain stale and Tightbeam shall record an observability outcome instead of exposing `unavailableReason`.

## Architecture

### Capture and mutation seam

The Codex adapter integration shall expose two usage-data inputs to one Tightbeam-owned cache seam: the result of `account/rateLimits/read` and each `account/rateLimits/updated` notification. The cache seam shall also consume the existing typed `:terminal` auth classification and resolved-binding changes as control inputs; it shall not receive or classify raw `account/updated` messages. Adapter creation, adapter load, adapter readiness after restart, establishment of a new eligible binding, receipt of a sparse update without a baseline, observation of an elapsed reset, and recovery from adapter unavailability shall request one full read when the current adapter is ready to accept the account operation. A session-status read that observes an eligible binding with a missing baseline or a settled failed refresh shall apply I-06. These triggers shall coalesce under the current capture claim. A fresh projection shall not cause a read.

The cache shall be process-local and keyed by adapter key and binding generation. Sessions that use the same adapter key and binding generation shall read the same immutable usage generation. Sessions on different adapter keys shall not share cache state. The cache shall not be a database or a source of account identity.

The cache seam shall linearize these events: binding transition, adapter-incarnation transition, refresh start, full-read completion, sparse update, adapter unavailability, provider error, timeout, and reset observation. A handler for an adapter-originated event first verifies the current binding generation and adapter incarnation; a full-read completion also verifies its refresh identifier. The handler then creates at most one new immutable usage generation. This check and publication are one atomic mutation. The seam shall compare the normalized result of a sparse merge with the current snapshot and shall keep the current sequence when the values are equal.

### Projection state

For an eligible binding with no baseline, a refresh start projects:

```json
{
  "freshness": "loading",
  "windows": []
}
```

A valid accepted response projects fresh usage:

```json
{
  "freshness": "fresh",
  "fetchedAt": 1770000000000,
  "windows": [
    {"label": "5h", "remainingPercent": 72, "resetAt": 1770003600000},
    {"label": "Week", "remainingPercent": 41, "resetAt": null}
  ]
}
```

If a later refresh is pending or fails while a same-binding accepted capture exists, the same windows project with `freshness: "stale"`. The same rule applies after reset observation, even when each retained `resetAt` has elapsed. A failed refresh with no prior accepted capture projects:

```json
{
  "freshness": "unavailable",
  "windows": [],
  "unavailableReason": "provider_unavailable"
}
```

`fetchedAt` records when Tightbeam accepted the provider input. It does not claim that Tightbeam knows when the provider measured usage. Tightbeam shall generate `metadataContextGeneration` from the same atomic projection as `authMode` and `codexUsage`.

The session-status response shall use these exact public names and types:

```text
metadataContextGeneration: string?                       # top-level
display.authMode: "oauth" | "api_key" | null
display.codexUsage?: {
  freshness: "loading" | "fresh" | "stale" | "unavailable",
  fetchedAt?: integer milliseconds,
  windows: [
    {
      label: "5h" | "Week",
      remainingPercent: integer 0..100,
      resetAt: integer milliseconds | null
    }
  ],
  unavailableReason?:
    "account_binding_unavailable" |
    "provider_unavailable" |
    "timeout" |
    "invalid_usage"
}
```

Every emitted `codexUsage` object shall include `windows`. `loading` shall use an empty `windows` array and omit `fetchedAt` and `unavailableReason`. `fresh` and `stale` shall include `fetchedAt` and a non-empty `windows` array, and shall omit `unavailableReason`. `unavailable` shall use an empty `windows` array, shall include `unavailableReason`, and may include `fetchedAt` only when a provider input was accepted and rejected as invalid.

### Failure mapping

- A typed terminal account invalidation maps the new binding generation to `account_binding_unavailable`.
- A rate-limit invalid-request response for missing authentication or non-ChatGPT authentication, an internal-error response for backend failure or an empty snapshot, and any other provider or adapter refusal map to `provider_unavailable`. Tightbeam shall not parse a JSON-RPC error message or use an error code as terminal-account evidence.
- Expiry of the capture operation's existing adapter-request timeout maps to `timeout`. This spec adds no timer.
- A successful provider response with no valid recognized window maps to `invalid_usage`.

These reasons appear only when the current generation has no accepted capture. An observed terminal account invalidation first creates a new generation and clears the old projection under I-13. A non-terminal failed refresh, invalid provider response, or reset observation with a same-generation accepted capture produces `stale` and records the outcome through observability. If a rate-limit failure and a terminal account invalidation race, the cache seam shall linearize both: an earlier failure may affect only the old generation, while the terminal transition clears it; a later failure shall fail the retired claim's generation check. Either order shall end with the new generation unavailable for `account_binding_unavailable`. Tightbeam shall not emit the Clawline compatibility vocabulary `stale_expired` or `reset_elapsed` in this MVP because the pinned consumer replaces either same-generation state with its retained stale windows.

If a full response contains one valid and one invalid window, Tightbeam publishes the valid window and records the invalid-window outcome. It does not make the entire generation unavailable.

### Observability

The cache seam shall emit structured, public-safe events through Tightbeam's existing logger. An emitted event may contain only: event name, harness, public host name, local binding generation, capture source (`read` or `update`), outcome (`accepted`, `coalesced`, `superseded`, `invalid`, `timeout`, `provider_unavailable`, or `account_binding_unavailable`), projected freshness, and recognized window labels. When a capture claim settles, at least one event for that claim shall expose its terminal outcome. The implementation may suppress repeated `coalesced` events for later joiners to the same claim.

Logs and process status shall not contain account identifiers, plan names, credit or balance data, raw provider strings, percentages, reset timestamps, fetched timestamps, credentials, tokens, cookies, or the raw response. Process status shall summarize only the allowed event fields.

### Security and fixture custody

The future implementer shall capture the acceptance fixture through a lawful read-only call over an already authenticated Codex adapter connection. Raw provider bytes shall exist only in process memory. The sanitizer shall transform that in-memory value before any filesystem write. It shall remove account identifiers, plan names, credits, balances, usage values, reset values, timestamps, and unknown provider strings while preserving object keys, value types, optionality, and the relationship between fields needed by the parser tests. The implementer shall replace sensitive scalar values with deterministic test values of the same type.

The capture process shall write only the sanitized fixture into a private directory inside the implementer's owned assignment workdir. A sanitizer failure or process interruption before that write shall leave no fixture and no raw file. Any tool or capture path that writes, spools, or dumps raw provider bytes to durable storage is non-conforming and blocks capture. Only the sanitized fixture, its source operation, its capture time in PT, and its SHA-256 may enter the repository or assignment evidence.

### Deletion assessment

ADD wins because the existing consumer behavior depends on provider-backed Codex usage and Tightbeam currently omits it. DELETE would remove an already supported OpenClaw/Clawline surface. ACCEPT would preserve a demonstrated contract failure. The design therefore adds one adapter capture seam and one in-memory normalized cache. It reuses Tightbeam's existing auth-event classifier because deleting terminal invalidation would permit cross-account stale usage, while accepting ambiguous error strings as terminal would invent identity evidence. It deletes the tempting alternatives: a second auth classifier, error-message parsing, raw-on-disk fixture capture, raw-response caching, a new route, persistent history, polling timers, direct Gateway credential access, inferred windows, special reset generation changes, emitted same-generation reset unavailability, and fabricated Claude data.

## Acceptance

Each check uses an injected clock, deterministic adapter replies, and the sanitized real-response fixture unless the check states otherwise.

1. **A-01 — Fixture provenance (I-01, I-02).** Given a lawful real `account/rateLimits/read` response passed directly from the adapter callback to the in-memory sanitizer, when sanitization succeeds, then the capture path's only filesystem write is a fixture that preserves the observed keys, types, optional fields, and nesting. The receipt records the source operation, SHA-256, and PT capture time. In a separate deterministic test, given a structurally equivalent in-memory response with a unique sentinel in each forbidden raw field and a child process with memory dumps disabled, when the test independently forces sanitizer rejection and hard termination before sanitized output is written, then the write trace, owned workdir, and configured crash-output locations contain no fixture, raw file, spool, dump, or sentinel. Falsification: fail on any capture-path write whose bytes contain a sentinel or whose destination is not the sanitized fixture path.
2. **A-02 — Account-mode mapping (I-21, I-22).** Given resolved credential kinds `subscription`, `apiKey`, and `none`, when session status is encoded, then `display.authMode` is respectively `"oauth"`, `"api_key"`, and `null`. Falsification: change one mapping and require the route contract test to fail.
3. **A-03 — Eligible Codex projection (I-03, I-18).** Given an eligible binding, injected acceptance time `1770000000000`, and a sanitized full response with `{usedPercent: 28, windowDurationMins: 300, resetsAt: 1770003600}` and `{usedPercent: 59, windowDurationMins: 10080, resetsAt: null}`, when Tightbeam accepts the response, then the route returns `freshness: "fresh"`, `fetchedAt: 1770000000000`, and windows `[{label: "5h", remainingPercent: 72, resetAt: 1770003600000}, {label: "Week", remainingPercent: 41, resetAt: null}]`.
4. **A-04 — No invented counterpart (I-05).** Given a valid 300-minute window and no 10080-minute window, when Tightbeam projects the response, then it returns only the `"5h"` window. Falsification: add a synthesized `"Week"` window and require the exact projection test to fail.
5. **A-05 — Unsupported absence (I-04, I-21).** Given a Claude subscription, a Codex API key, a missing credential, and an unsupported harness in separate cases, when session status is encoded, then `display.codexUsage` is absent in each case. The Claude subscription reports `display.authMode: "oauth"`. Falsification: encode `codexUsage: null` in one case and require the exact JSON test to fail.
6. **A-06 — Loading without blocking (I-06, I-07, I-09).** Given an eligible binding with no baseline and one blocked full read, when session status is requested, then the request returns `loading` without waiting for that read and does not start a second read. Given an unrelated prompt on the same adapter, when the read remains blocked, then the prompt completes before its existing test deadline.
7. **A-07 — Event-derived freshness (I-14, I-20, I-21).** Given a fresh accepted snapshot, when a later refresh starts, fails, or the adapter exits transiently, then Tightbeam returns the same windows as stale. Given adapter recovery and a successful full read, when Tightbeam accepts that read, then it returns the new windows as fresh. Given a provider refusal while the subscription credential remains resolved, when session status is encoded, then `authMode` remains `"oauth"` and usage is stale if a same-binding accepted capture exists or unavailable with `provider_unavailable` otherwise. No locally invented age threshold participates in these transitions.
8. **A-08 — Reset handling (I-06, I-19, I-20, I-23).** Given a ready adapter and a same-generation accepted capture with one window whose `resetAt` equals the injected current time and one whose reset is later, when session status observes the elapsed reset, then Tightbeam returns both exact prior windows as stale, preserves `metadataContextGeneration`, requests one coalesced refresh, and returns without waiting. Given both resets have elapsed, when the same read occurs, then the result is the same retained stale capture and not `unavailable/reset_elapsed`. Falsification: remove a retained window, change the generation, emit `reset_elapsed`, or start two reads and require the exact state and request-count tests to fail.
9. **A-09 — Sparse merge (I-15, I-16).** Given a full baseline and a sparse same-binding update that changes only `usedPercent`, when Tightbeam accepts the update, then the baseline duration and reset remain and the projected remaining percentage changes. Missing and null update fields preserve their baseline values.
10. **A-10 — Sparse update without baseline (I-09, I-15).** Given a sparse update and no same-binding full baseline, when Tightbeam receives the update, then it publishes no window and starts one full read. Given another sparse update before that read settles, when Tightbeam receives it, then no second read starts.
11. **A-11 — Limit selection (I-17).** Given a response with distinct values in `rateLimitsByLimitId["codex"]`, `rateLimitsByLimitId["other"]`, and historical `rateLimits`, when Tightbeam projects it, then only the `codex` window values appear. Given no `codex` entry, when Tightbeam projects the historical member, then only the historical window values appear. Given sentinels in credits, spend-control, plan, reached-type, reset-credit, and unknown fields, when the adapter normalizes the response, then neither cache inspection nor the public route contains a sentinel.
12. **A-12 — Parser rejection and duplicate order (I-05, I-18).** Given fixture variants with `windowDurationMins: 301`, `usedPercent: 101`, a non-integer reset, and primary and secondary 300-minute windows, when Tightbeam parses each variant, then it rejects the first three invalid windows and chooses the primary valid duplicate. The structured event exposes an `invalid` outcome without a raw value.
13. **A-13 — Binding race and generation coupling (I-08, I-11, I-13, I-23).** Given a blocked full read for binding A, when Tightbeam's resolved credential binding changes to B and A's read later succeeds, then the response exposes B's new `metadataContextGeneration` before any B usage and omits A's value from B's generation. The deterministic mutation test asserts that the binding check and publication are one mutation.
14. **A-14 — Adapter-restart race (I-09, I-11, I-14, I-15).** Given adapter incarnation A with a blocked full read, when A exits, replacement incarnation B keeps the same binding generation and starts a new full read. When A's read later completes and A emits a sparse notification, each retired-incarnation event fails the current-incarnation check and changes neither the public projection nor B's current claim. The test permits A's unresolved provider operation and B's current claim to overlap while asserting that only B's events may publish.
15. **A-15 — Coalescing and idempotency (I-09, I-12).** Given 20 concurrent session-status requests with no baseline, when each requests refresh, then exactly one provider read starts. Given the accepted completion is replayed, when its cleared claim is checked, then the public generation remains unchanged. Given a sparse notification whose normalized merge equals the current snapshot, when the notification is replayed, then the public generation and sequence remain unchanged.
16. **A-16 — Atomic reads (I-08, I-10).** Given one full-read completion, one sparse update, one binding transition, and one session-status read under a deterministic scheduler, when the scheduler runs the 24 permutations, then each response equals one complete immutable generation and no response combines fields from two generations.
17. **A-17 — Exact route compatibility (I-22, I-23).** Given fresh, stale, loading, unavailable, and ineligible states, when `/api/session-status` encodes each response, then its JSON matches the public names, omission rules, values, window order, and types in this spec; every emitted `codexUsage` contains `windows`, and loading and unavailable contain `windows: []`. When a test recursively removes `metadataContextGeneration`, `display.authMode`, and `display.codexUsage`, then the remaining value is structurally equal to the response from the reconciled Tightbeam base.
18. **A-18 — OpenClaw/Clawline compatibility (I-04, I-21, I-23).** Given the exact JSON cases from A-17, when the pinned Clawline status types decode them and the existing footer renders them, then loading and unavailable decode with empty windows, OAuth Codex fresh and stale usage renders, API-key mode renders `API KEY` without usage, and unsupported providers render no Codex usage. Given a same-generation accepted capture followed by reset observation, when the client resolves the status, then it renders the retained windows as stale. Given a binding-generation change, when the client receives the new status, then it discards prior cached usage before rendering the new binding.
19. **A-19 — Privacy (I-02, I-03).** Given provider inputs with unique string sentinels in account id, plan, credit, balance, provider message, token, and cookie fields plus known numeric usage and reset values, when accepted-full, accepted-update, invalid, timeout, provider-unavailable, superseded, binding-transition, and process-status paths run, then repository scans, structured logs, process status, crash output, and persisted storage contain none of the string sentinels or raw numeric usage and reset values. Cache inspection contains only the expected normalized remaining percentage, reset milliseconds, local provenance, freshness, and binding generation. The public route contains only the normalized fields authorized by this spec.
20. **A-20 — Observability (I-02, I-03).** Given capture scenarios that produce accepted, coalesced, superseded, invalid, timeout, provider-unavailable, and account-binding-unavailable outcomes, when each scenario runs, then every structured event contains only the allowed fields. Each claim that settles has at least one terminal outcome among `accepted`, `superseded`, `invalid`, `timeout`, `provider_unavailable`, and `account_binding_unavailable`; a `coalesced` event alone does not satisfy that condition. Removing a settled claim's terminal outcome or adding a forbidden value fails the event-schema test.
21. **A-21 — Prompt-path isolation (I-07).** Given a metadata operation that does not resolve, when a prompt is submitted, then the prompt completes before the prompt test's existing deadline. Falsification: make prompt completion await metadata completion and require the test to time out.
22. **A-22 — Repository gates.** Given an owned throwaway worktree at the exact implementation revision on Gibson, when the implementer first builds `cli/target/release/tightbeam` with `cargo build --release --manifest-path cli/Cargo.toml`, then runs baseline and after-change `mise exec -- mix format --check-formatted` and `mise exec -- scripts/verify_mix.sh`, the after-change gates pass and the receipt records baseline and after counts.
23. **A-23 — Live adapter smoke (I-01, I-07).** Given the adapter-seam change and lawful test credentials, when `mise exec -- mix run --no-start scripts/feature_smoke.exs` runs from the owned exact-revision worktree without a leg filter, then the Claude and Codex smoke legs pass. The receipt records the revision, sanitized output, and result. It omits credentials and raw provider responses.
24. **A-24 — Cache scope (I-24).** Given two sessions on the same adapter key and binding generation, when one session causes a full read to publish, then the other session reads the same usage generation without another provider read. Given two sessions on different adapter keys, when one publishes, then the other session's projection remains unchanged.
25. **A-25 — Unavailable reason mapping and terminal classification (I-13, I-25).** Given the existing logged-out `account/updated` fixture and the existing forwarded session-update shape, each with `authMode: null` and `planType: null`, when Tightbeam's existing auth-event classifier emits `:terminal`, then the cache consumes that typed output, changes `metadataContextGeneration`, clears old windows, and returns `account_binding_unavailable` with `windows: []`. Given account-update variants with a recognized non-null auth mode, an unknown mode, one null field, a missing field, or a malformed shape, when each is classified, then none produces `:terminal` or `account_binding_unavailable`. Given rate-limit errors for missing authentication, non-ChatGPT authentication, backend failure, and an empty snapshot, when each carries a unique error-message sentinel, then every case maps to `provider_unavailable` without parsing the sentinel. Given a request timeout or a successful response with zero valid windows, when no accepted capture exists, then Tightbeam returns `timeout` or `invalid_usage`, respectively, with `windows: []`. Given a same-generation accepted capture followed by any non-terminal failure, when session status is encoded, then Tightbeam retains stale windows and omits `unavailableReason`. Given both orderings of a blocked old-generation rate-limit failure and terminal account invalidation, with no replacement binding, when the deterministic scheduler settles both events, then the final response is the new generation with `account_binding_unavailable`, and the failed old-generation claim cannot republish. Given reset observation with an accepted capture, when session status is encoded, then neither `stale_expired` nor `reset_elapsed` is emitted.

## Open Questions

None. This targetless, unbound amendment has no blocking or non-blocking question. The sole independent review lane is closed; no work-item binding or implementation handoff may treat its unfiled F4 report as a clean verdict.
