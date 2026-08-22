# Lachesis usage cache generation integrity

Status: review-ready

Work item: `wi_ab7e155e-1cf0-447e-99c7-ef36fd30c503`

Source base: `clickety-clacks/lachesis` commit `abc6986ce0b59673116da96310acfa851cfb8366`

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

`live` means that this request's accepted finish published the returned generation. `cache` means
that the request returned an already published fresh generation. `stale` means that the request
returned an older published generation with the teaching error from a later accepted failed read.
`error` means that no published sample exists and the accepted read failed. A losing finish cannot
make its sample `live`. AC-1, AC-3, and AC-5 verify this invariant.

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

The service must not reuse the sample that it read before `Fetch` as fallback after the fetch
returns. It builds the response from the post-finish snapshot. If a `Clear` wins and leaves no
sample, a waiting request starts one replacement fetch within its original five-second wait
context when no fetch is active. If that context expires, the request returns the existing
`UPSTREAM_TIMEOUT` teaching error. It never returns the cleared sample.

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

### AC-2 — Install and clear both supersede an old claim

Given a table test with one blocked fetch claim, when one case calls `Install` and another case
calls `Clear` before releasing the claim, then the losing finish changes neither winner. The
install case returns the installed generation. The clear case returns no sample and keeps the
cleared generation absent after the worker finishes. Each waiter wakes once, and the race detector
reports no close of a closed channel.

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
seconds from that tuple's observation time to the injected cache clock. The response status
matches INV-4. Aggregate `counts` increments that same result status.

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
