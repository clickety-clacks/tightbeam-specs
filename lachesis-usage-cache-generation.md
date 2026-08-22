# Lachesis usage cache generation integrity

Status: review-ready

Work item: `wi_ab7e155e-1cf0-447e-99c7-ef36fd30c503`

Source base: `clickety-clacks/lachesis` commit `abc6986ce0b59673116da96310acfa851cfb8366`

## Spec-homing

The canonical set for this repair contains two files:

- `lachesis-usage-cache-generation.md`, identified during review by its immutable spec artifact
  and SHA-256 and after reviewed-clean by the matching `spec-ref` and `spec-sha256` binding on
  work item `wi_ab7e155e-1cf0-447e-99c7-ef36fd30c503`, governs cache claims, immutable
  publication, stale-result construction, and response serialization.
- `lachesis-provider-usage-window-drift.md` at `clickety-clacks/tightbeam-specs` commit
  `6bbc7a36fda581e96dce8e8fa262e430340f9840`, SHA-256
  `8c51ad8675a7143210333b8c01fb65b2818bdc01f2fd8013244aee0608aa6334`, remains
  authoritative for adapter normalization, recognized-window validation, fixed diagnostics,
  raw-payload preservation, and teaching errors.

This file does not supersede the adapter spec. The adapter spec controls provider-response
parsing and adapter output. This file controls cache and service behavior after an adapter
returns that output. If both files mention one behavior, the adapter spec controls work inside an
adapter and this file controls work inside the cache or service.

## Goal

Keep each published usage result within one account and one provider-response generation.
An older read that finishes late must not replace a newer cache write.

The exact source base proves the defect:

1. `Cache.Fetch` reserves an in-flight channel, runs the fetch callback, and then writes its
   result without checking for a superseding write (`internal/core/cache.go:43-76`).
2. `fetchAccount` releases the per-account operation lock when its callback returns
   (`internal/core/service.go:523-543`). Cache publication happens after that release.
3. A waiting `Verify`, `Refresh`, or re-onboarding operation can acquire the released account
   lock and publish or clear a newer sample before the older `Cache.Fetch` resumes
   (`internal/core/service.go:267-284`, `365-380`;
   `internal/core/jobs.go:423-425`, `527-535`).
4. The older fetch then writes unconditionally. A later API read can therefore show an older
   utilization with the same reset time after it already showed the newer utilization.

Claude normalization does not splice these fields. It decodes each window's utilization and
reset from one bucket and copies the accepted raw response into the same sample
(`internal/provider/claude/adapter.go:153-224`). The proven defect is whole-generation replay,
not an adapter-level field merge.

The repair makes one provider response one immutable generation. The cache publishes the
normalized windows, raw payload, diagnostics, observation time, derived age, error state, and
result status from one generation snapshot.

## Non-Goals

- Change Claude or Codex normalization, utilization scaling, window IDs, reset parsing, raw
  safety checks, or provider requests.
- Change the 30-second freshness boundary or the public `live`, `cache`, `stale`, and `error`
  status names in the exact source base.
- Add cache persistence, history, ranking, alerts, generation IDs in the API, or provider
  response deduplication.
- Redesign account locking, credential refresh, onboarding, aggregation, or the registry.
- Call a provider, inspect a credential or account, touch the running service, or capture a new
  fixture for this repair.
- Import the unmerged `fresh` and `pending` API vocabulary from another branch.
- Establish an agent operating-manual pattern. This spec establishes only the code pattern
  named under Architecture.

## Terms

- **Provider read:** one call to a provider adapter's `Usage` method and its returned sample or
  teaching error.
- **Usage generation:** the fields derived from one successful provider read: account ID,
  provider, label, plan, `observed_at`, windows, diagnostics, and raw payload.
- **Observation time:** `UsageSample.observed_at`. It is the current API's fetched-at value.
- **Published snapshot:** one cache-owned immutable usage generation, its current fetch error,
  and the cache state used to derive age and result status.
- **Fetch claim:** an opaque identity that authorizes one in-flight read to publish for one
  account. A claim is not an API field.
- **Superseding write:** an `Install` or `Clear` that occurs after a fetch claim starts and before
  that claim finishes.
- **Accepted finish:** a fetch finish whose claim still owns the account's publication seam.
- **Losing finish:** a fetch finish whose claim a superseding write retired.
- **Age-stale result:** the existing background-mode return of a published generation whose
  derived `age_seconds` is greater than 30. It returns before the background refresh finishes,
  so its error can be absent.
- **Stale fallback:** a published successful generation returned with the teaching error from a
  later accepted failed read.
- **Generation order:** the order in which same-account cache mutations linearize while holding
  `Cache.mu`. Timestamps do not decide this order.

## Assumptions

- Registry account IDs are unique. The cache uses the account ID as its only key
  (`internal/model/model.go:49-59`; `internal/core/cache.go:17-25`).
- Both provider adapters construct normalized fields and raw payload before the cache receives
  a sample. Each adapter copies its accepted raw bytes.
- `UsageSample` contains slices, raw bytes, and pointer fields. A Go struct assignment copies
  their headers or pointers, not their owned values (`internal/model/model.go:108-131`).
- The exact cache base uses shallow struct copies in `Install`, `Fetch`, and `aged`
  (`internal/core/cache.go:27-40`, `60-76`, `88-98`).
- The API encodes one `UsageResult` with Go's JSON encoder (`internal/api/server.go:225-236`,
  `268-270`). Serialization does not repair an incoherent or aliased snapshot.
- Existing stale fallback, account isolation, fail-closed recognized-window behavior, raw
  visibility, and teaching errors remain product authority. The earlier
  `lachesis-provider-usage-window-drift.md` spec remains authoritative for adapter behavior.
- Mike observed utilization decrease between two reports whose reset time stayed equal.
  Utilization cannot decrease within one unchanged provider window.
- The writer's Gibson session could not execute synthetic Go proof because `go` was absent.
  Assignment attest `att_89f575b2-2982-43bb-8de7-5d5b9e075766` records the exact failed command.
  The implementation and review lanes must execute the deterministic tests in Acceptance.

## Invariants

### INV-1 — One response stays one generation

The cache publishes a successful provider read as one indivisible usage generation. A response
contains no window, reset, raw payload, diagnostic, plan, label, account, observation time, or
age from another generation. AC-1 and AC-5 verify this invariant.

### INV-2 — The cache owns immutable values

The cache owns each published generation. It deep-copies every mutable or pointed-to
`UsageSample` value at the publication boundary. It also returns a deep copy to callers. A caller
cannot change a published generation through an input or output alias. AC-4 verifies this
invariant.

### INV-3 — A superseding write wins

`Install` and `Clear` retire the current fetch claim atomically with their cache mutation. A
losing finish cannot publish its sample or error. It returns the current published snapshot, not
its losing result. No timestamp or reset value decides the winner. AC-1 and AC-2 verify this
invariant.

### INV-4 — Status and age describe the returned snapshot

The service derives `age_seconds` once from the returned generation's `observed_at` and one clock
reading. It derives result status from the same cache snapshot and fetch outcome.

`live` means that this request's accepted finish published the returned generation. `cache` has two
existing paths. Background mode returns an already published generation whose derived
`age_seconds` is at most 30. A foreground or coalesced request returns a successful generation
published by another accepted cache mutation. `stale` also has two existing paths. An age-stale
result returns a published generation immediately while its background refresh is unfinished; it
carries the snapshot's prior error, which can be absent. A failed-read stale fallback returns the
last successful generation with the teaching error from a later accepted failed read. `error`
means that no published sample exists and the accepted read failed. A losing finish cannot make
its sample `live` or attach its error. AC-1, AC-3, and AC-5 verify this invariant.

### INV-5 — Stale fallback preserves the last success

An accepted failed read leaves the last successful generation unchanged. The cache attaches the
new teaching error to the stale result without changing the sample's fields or observation time.
A later successful read replaces the full sample and clears that fetch error. AC-3 verifies this
invariant.

### INV-6 — Account isolation is structural

A cache mutation changes only the entry whose key equals the registry account ID passed to that
mutation. A claim for one account cannot publish, clear, wake, or return another account's entry.
AC-6 verifies this invariant.

### INV-7 — Existing safety and teaching behavior stays exact

The repair does not change adapter validation. A provider response with zero valid recognized
windows returns no sample and the existing `UPSTREAM_CONTRACT_CHANGED` teaching detail. A response
with at least one valid recognized window preserves raw bytes and keeps existing fixed diagnostics.
AC-7 verifies this invariant.

### INV-8 — One cache mutation seam owns publication

One private cache operation performs claim validation, deep copying, sample or tombstone
publication, error publication, claim retirement, and waiter notification while holding the cache
lock. `Fetch`, `Install`, and `Clear` reach cache state through this seam. AC-8 verifies this
invariant.

## Architecture

The named pattern is **account-scoped immutable usage generation**. It applies only to the
in-memory usage cache and the service code that converts a cache snapshot into `UsageResult`. It
does not apply to credential state, registry rows, provider parsing, or persistent data.

Each account entry owns one published snapshot and at most one fetch claim. `Fetch` creates the
claim while holding the cache lock. The provider read runs outside that lock. The finish operation
then reacquires the lock and compares the exact claim identity.

An accepted finish publishes a deep-owned sample or records its teaching error. A losing finish
leaves the entry unchanged and reads back the current snapshot. `Install` and `Clear` retire an
existing claim before they publish their replacement or tombstone. They wake claim waiters once.
The retired worker may finish later, but it cannot close the claim twice or alter the entry.

The service must not reuse the sample that it read before a foreground `Fetch` as fallback after
that fetch returns. It builds the foreground response from the post-finish snapshot. If a `Clear`
wins and leaves no sample, a waiting request starts one replacement fetch within its original
five-second wait context when no fetch is active. If that context expires, the request returns the
existing `UPSTREAM_TIMEOUT` teaching error. It never returns the cleared sample.

Background mode preserves its existing non-waiting behavior. It returns an already published
generation with `age_seconds` at most 30 as `cache`. When a published generation has
`age_seconds` greater than 30, background mode invokes `Fetch`, which starts or coalesces with an
account refresh, and immediately returns the detached pre-refresh snapshot as `stale`. That
result carries the snapshot's prior error, which can be absent. The unfinished refresh contributes
no sample or error to that response. Its later accepted finish publishes its complete success or
teaching error through the same cache mutation seam.

The cache stores no `age_seconds`. Snapshot creation deep-copies the published generation and
derives age from its observation time. The response builder selects one status from that same
snapshot and fetch outcome. JSON serialization receives only that detached response value.

The deep copy includes `Plan`, `Windows`, each window's `ResetsAt` and `WindowSeconds`,
`Diagnostics`, and `Raw`. Strings, numbers, booleans, providers, account IDs, and times copy by
value. The repair treats each completed teaching error as read-only and preserves its existing
shape.

The cache key remains the registry account ID. The implementation adds no global generation
counter and exposes no generation metadata. Claim identity and lock order provide the required
ordering.

ADD wins because removing the cache would remove stale fallback and bounded response behavior.
Accepting replay would keep an observably false usage result. A claim check plus owned values is
the smallest mechanism that preserves both behaviors.

## Acceptance

### AC-1 — A late old read cannot replace a newer write

Given one synthetic Claude account, start cache fetch A with normalized `used_percent: 23`, reset
time R, observation time T1, diagnostic A, and raw payload A whose `utilization` is `23`. Hold A
before it returns from the fetch callback. Install generation B for the same account with
normalized `used_percent: 100`, the same reset time R, observation time T2 later than T1,
diagnostic B, and raw payload B whose `utilization` is `100`. Release A.

When the fetch finishes and the test reads the cache, then the fetch result and later snapshot
contain B's utilization, observation time, diagnostic, and raw payload. Both contain reset R. No
A field appears. The fetch result does not report A as `live`.

### AC-2 — Install and clear supersede a claim and wake its waiter once

Given a table test, start owner fetch A and hold its provider callback at a barrier. Start a second
`Fetch` for the same account. Prove that the second call is waiting on A's claim and has not invoked
its callback.

When the install case publishes generation B, then the waiting call wakes once and returns B as an
already published result without invoking its callback. Release A only after that return. A's
losing finish returns B without reporting `live`. The later snapshot remains B.

When the clear case clears the entry, then the waiting call wakes once and starts replacement fetch
C within its original wait context. Let C publish before releasing A. The waiting call returns C
as its accepted `live` finish. A's losing finish and the later snapshot each return C without
returning A or the cleared sample; A's losing finish does not report `live`.

In both cases, the second `Fetch` must return one result before A is released. After A returns, a
non-blocking read of the second `Fetch` result channel finds no second result. The install case
invokes A's callback once and the waiting callback zero times. The clear case invokes A's callback
once and C's callback once. `go test -race` reports no blocked waiter, data race, or close of a
closed channel.

### AC-3 — Failed refresh keeps one stale generation

Given a published generation A and an accepted later read that returns a synthetic
`UPSTREAM_UNAVAILABLE` detail, when the caller requests usage, then the result has status `stale`,
contains A unchanged, derives age from A's observation time, and contains the new teaching error.

Given a later successful generation B, when it publishes, then the next result contains only B
and contains no prior fetch error.

### AC-4 — Input and output aliases cannot mutate the cache

Given a sample with non-empty plan, windows, reset pointers, window duration pointers,
diagnostics, and raw payload, when the test installs it and mutates each original value, then a
cache snapshot still equals the pre-mutation sample.

When the test mutates each mutable value in that returned snapshot and reads again, then the next
snapshot still equals the published sample. `go test -race` reports no data race.

### AC-5 — Concurrent serialization emits complete generations

Given synthetic generations A and B with distinct utilization, reset, observation time,
diagnostic, and raw sentinels, coordinate each publication and snapshot with test barriers. Start
JSON encoding from the detached snapshot, then release the next publication. Repeat this sequence
for both generation orders under `go test -race`.

When the test decodes each response, then each response matches the complete A tuple or the
complete B tuple. No response contains a hybrid tuple. `age_seconds` equals the non-negative whole
seconds from that tuple's observation time to the injected cache clock.

For background mode with an already published tuple whose derived `age_seconds` is at most 30,
the response status is `cache`. For a foreground or coalesced request that returns a successful
tuple published by another accepted cache mutation, the response status is `cache`. For an
accepted finish that publishes the returned tuple, the response status is `live`. For background
mode with a published tuple whose derived `age_seconds` is greater than 30, the response status is
`stale` before the refresh finishes and the error is absent when the snapshot has no prior error.
For an accepted failed read with a published tuple, the response status is `stale` and the result
carries that read's teaching error. For an accepted failed read without a published tuple, the
response status is `error`. Aggregate `counts` increments the exact status on that same result.

### AC-6 — Concurrent accounts stay isolated

Given two account IDs with blocked fetches and distinct generation sentinels, when the test
installs and clears them in the opposite order, then each result and snapshot contains only its
own account ID and sentinel. One account's waiter and claim state do not change when the other
account mutates.

### AC-7 — Adapter safety and errors-teach remain unchanged

Given the synthetic Claude and Codex cases from `lachesis-provider-usage-window-drift.md`, when
the implementation runs adapter, service, and API tests, then valid degraded samples preserve raw
payload and fixed diagnostics. Zero-valid-window samples still fail closed with the exact existing
`UPSTREAM_CONTRACT_CHANGED` detail. Stale fallback retains that exact detail without changing the
cached sample.

### AC-8 — Each cache mutation uses the generation seam

Given the implementation diff, when the reviewer traces writes to a cache entry's sample, error,
claim, and tombstone state, then each write occurs inside the one private mutation operation from
INV-8. No service, job, or API code writes those fields directly.

### AC-9 — Repository verification passes without live access

Given the implementation commit, when the builder runs `go test -race ./...`,
`./scripts/scan-fixtures.sh`, `./scripts/offline-smoke.sh`, and `./scripts/verify.sh` from the
Lachesis repository root, then each command exits zero. These commands make no provider call and
read no live credential or account state. Test output contains only synthetic values.

## Open Questions

None. No blocking or non-blocking question remains for this repair.
