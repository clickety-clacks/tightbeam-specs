# Tightbeam testing proof strategy v2

Status: PROPOSED, 2026-08-28. Target unset.

Product evidence baseline: corrected authoritative main proof at
`01c52e16` and the current Firehose acceptance audit in `art_8daabc76`.
Specification baseline: `tightbeam-specs` main
`307210c542701b714df88a4ca778cab434dca35d`.

## Spirit

The test system must answer one question: **which user-visible claim is proven, by
which executable evidence, on which exact bytes?** A green aggregate is useful, but it
is not an acceptance map. Activity is not proof.

For Firehose, use the smallest real system that can prove each claim. Reuse the real
WebSocket client and gateway setup that already runs in CI. Add a subprocess only when
process death or restart is the claim. Use tables for closed registries, filter
matrices, and byte identity. Do not make a network journey carry a proof that a table
can express more cheaply and completely.

The standing detection question is:

> What changed on the deliverable since the last look?

For this card, the deliverable is one named gap within A1-A7 moving from partial or
manual-only evidence to automated proof. Test counts, audits, fixture extraction, and
green unrelated suites do not substitute for that movement.

## Corrected facts

This strategy does not plan around the two superseded premises in the original card.

- Authoritative `scripts/verify_mix.sh` was green at product `01c52e16`: 9 doctests,
  1,895 tests, 0 failures, and 11 skipped. The six failures from bare `mix test` used a
  different and unsupported invocation. Runner remediation is not a Firehose
  prerequisite.
- `test/firehose_smoke_test.exs` is real end-to-end CI coverage. It uses the real
  `Tightbeam.ClientE2E.WS` TCP client through authentication, subscribe, notice,
  disconnect, reconnect, rebuild, and convergence against an isolated gateway.
- `scripts/firehose_restart_smoke.exs` uses a real client and gateway subprocess, but
  no CI workflow invokes it. Its restart proof remains manual-only.
- The exhaustive audit in `art_8daabc76` establishes the current acceptance status:
  A2 is proven; A1, A3, A4, A5, and A6 are partial; A7 is manual-only.

A later unrelated suite observation must not displace this Firehose work. The
authoritative suite command remains `scripts/verify_mix.sh`; any new baseline failure
is a separate maintenance finding unless it invalidates a Firehose proof directly.

## Decision: extend the existing harness

Mike's one-client/one-controller hypothesis is right for ordinary public journeys, but
it is not the cheapest oracle for every missing clause.

Use one small shared support module, factored from the existing smoke tests, to provide:

- one real `Tightbeam.ClientE2E.WS` client;
- one in-process Bandit gateway for fast public-boundary cases;
- one disposable gateway subprocess for restart cases;
- an isolated database and temporary state directory;
- an operating-system-assigned port with exact ownership and teardown checks;
- deterministic commit, registration, delivery, and restart barriers;
- a configurable Firehose queue limit whose production default remains 1,000; and
- a test-only delivery barrier whose production behavior remains immediate delivery.

The queue limit and delivery barrier are necessary. Today `ChangeSocket` acknowledges
the first notice to `Hub` before the client has consumed the frame. A client that merely
stops reading cannot deterministically fill the Hub queue. Kernel buffering, sleeps,
or 1,001 timed mutations would produce a slow and flaky test. The barrier holds the
first delivery before acknowledgment, and the small queue limit reaches the same
production overflow branch in a few mutations. The public WebSocket client must still
observe close code 4008 and rebuild normally after reconnect.

Do not build a second client, gateway, database fixture, or general test framework.
The support module exists only to remove duplication between the current CI smoke and
the restart smoke.

## Proof shapes

| Shape | Use it for | Concrete Firehose work | CI |
|---|---|---|---|
| Closed table | Complete inventories, filters, visibility order, version algebra, and exact bytes. | A1, the closed portion of A3, reducer rules for A4, and A6. | Every change. |
| In-process micro-system | Ordinary behavior through a real public WebSocket boundary. | A3 delivery and A4 convergence using the existing smoke shape. | Every pull request and push. |
| Subprocess fault micro-system | Gateway death, 1012, 4008, reconnect, rebuild, and port/process lifecycle. | A5 and A7. | Every affected pull request and every main build. |
| Live external boundary | Only a client or provider that cannot be represented locally. | A later real ATC/Clawline consumer, if its own acceptance requires it. | Scheduled or release lane. |

An in-process micro-system test must enter through the public WebSocket surface. It
must use production authentication, visibility, serializer, commit publication, and
rebuild paths. Direct publisher calls may prepare a mutation but cannot be the only
observable path for a public-journey claim.

## Firehose acceptance closure

| Item | Current status | Existing proof | Cheapest missing proof |
|---|---|---|---|
| A1 registry both-ways diff | Partial | `test/change_socket_test.exs`; `test/admin_projection_test.exs` | One canonical mutation/invalidation inventory that includes the missing R8b Topline, membership, and subagent-marker classes. Diff it both ways against production registry inputs. Fail on any missing or extra row. |
| A2 registration cut | Proven | `test/change_socket_test.exs`, “publication before registration cut is never delivered” | Preserve it. Do not rewrite it. |
| A3 filtered delivery | Partial | `test/change_socket_test.exs` proves selected filters and visibility ordering. | Drive every R8/R8b registry row through a closed filter matrix. Prove hidden rows never enter filter matching. Add one real-client representative journey, not one network test per row. |
| A4 M1 convergence | Partial | `test/firehose_smoke_test.exs`; `test/admin_projection_test.exs`; `test/firehose_publisher_test.exs` | Add a registry-driven client model test for create/update/delete, duplicate and older notices, delete/recreate versions, and R8b refetch notices. Use the existing real-client smoke for representative wire journeys. |
| A5 kill-gateway rebuild | Partial | Unit 1012/4008 coverage in `test/change_socket_test.exs`; manual `scripts/firehose_restart_smoke.exs`. | Port the subprocess journey into ExUnit/CI. In the same fixture, prove real kill/1012/reconnect/rebuild and deterministic slow-consumer 4008/reconnect/rebuild. |
| A6 byte-equivalent payloads | Partial | Selected projection and notice comparisons in `test/firehose_publisher_test.exs` and `test/admin_projection_test.exs`. | One table compares every rebuildable R8 class with the canonical REST detail serializer after envelope removal, including secret exclusion and special comparator rules. Final proof waits for the canonical REST detail route; the REST owner owns that route, while this card owns the shared comparator. |
| A7 real external consumer smoke | Manual-only | `scripts/firehose_restart_smoke.exs` has historical manual proof; `test/firehose_smoke_test.exs` has a real CI client but does not restart the gateway. | Make the real subprocess client journey an ordinary CI test. Assert subscribe, notice, exact gateway death, 1012, reconnect, snapshot/rebuild, and final convergence. |

The five partials do not require five bespoke harnesses. They require one shared fixture,
two test processes, and three test files:

1. Keep closed inventory and filter tables with `test/change_socket_test.exs` or one
   focused registry test file.
2. Extend `test/firehose_smoke_test.exs` for fast public convergence.
3. Replace the manual-only restart proof with
   `test/firehose_restart_smoke_test.exs` using the shared fixture.

## REST coordination boundary

The canonical REST audit is durable as `art_8daabc76`, SHA-256
`bf00acfc4591fb0cbfd5ac00867c77d48748b5a689590487aad333399d97257b`,
with progress `att_79edc555` and completion `att_3b6cc07c`. It maps Firehose A1-A7
and REST A1-A43 to exact complete, partial, and missing evidence.

`product-owner:rest-state-api` owns canonical REST routes, delivery order, and the
REST A1-A43 implementation roadmap. This card must not duplicate those cards. The only
shared acceptance seam is A6:

- this strategy supplies the byte comparator for all rebuildable R8 classes and reusable fixtures;
- the REST slice supplies the canonical detail route and serializer entry point; and
- A6 moves to proven only when the comparison runs through that production REST detail
  seam on the same exact product commit.

R8b stays in the A1 and A3 registry coverage and the A4 observe/refetch coverage. It
stays outside A6 because it has no rebuildable resource.

Until then, a green shared serializer table is useful component evidence, not full A6
acceptance.

## Ordered implementation cards

Each card must update the existing acceptance map in the same change. Do not open a
separate audit or ledger project before the tests. The test is the deliverable.

### 1. Factor the Firehose acceptance fixture and automate A5 slow-consumer recovery

Extract only the reusable client, gateway, isolated-state, port, barrier, and teardown
code from the two existing smoke paths. Add an injectable Hub queue limit with default
1,000 and a test-only pre-ack delivery barrier with production default disabled.
Use that seam in the same card through the real WebSocket client: force the production
overflow branch, observe 4008, reconnect, rebuild, and converge.

Acceptance:

- existing `test/firehose_smoke_test.exs` still passes through the real WebSocket;
- parallel fixture instances share no database, directory, port, process, or queue;
- a held first delivery plus a small queue makes the real client observe 4008,
  reconnect, rebuild, and converge through the production overflow branch;
- the acceptance map records the A5 slow-consumer gap as automated proof, while A5
  remains partial only for the gateway-kill path; and
- teardown proves exact PID exit and port closure without touching another process.

### 2. Close A1 and A3 with closed tables

Create one canonical R8/R8b registry inventory. Include Topline, membership, and
subagent-marker mutations and invalidations. Diff the inventory both ways against the
production registration sources. Drive the same rows through type/ref filters,
present/absent/different refs, principal/origin cases, and visibility-first checks.

Acceptance: deleting or adding one mapping, matching an absent ref, or invoking the
filter matcher for a hidden row fails a named test. A1 and A3 move to proven without a
network test for every table row.

### 3. Close A4 with a model-based client journey

Extend the current CI smoke with one client-side reference reducer. Generate a bounded,
deterministic sequence across every rebuildable class: create, update, delete,
duplicate, older notice, delete/recreate, and R8b observe/refetch. Compare the client
model with an authoritative rebuild after each sequence. Keep a small fixed set of
public WebSocket journeys as wire witnesses.

Acceptance: disabling dedupe, accepting an older version, losing a delete/recreate
ordering edge, or treating an R8b refetch notice as a full projection fails. A4 moves to
proven.

### 4. Close A5 gateway-kill recovery and automate A7 in one subprocess CI test

Convert `scripts/firehose_restart_smoke.exs` into an ExUnit test that uses the shared
fixture. With one real client and one disposable gateway subprocess, subscribe,
receive a notice, kill the exact gateway, observe 1012, restart, reconnect, rebuild,
and converge. Regress the Card 1 slow-consumer journey without reimplementing it.

Acceptance: the test runs in the normal Linux and macOS CI path, uses no shared port or
state, identifies the exact process before signaling it, and fails on leaked PID or
open port. A5 and the script-consumer A7 proof become automated.

### 5. Close A6 with the REST delivery slice

Add the serializer comparator for all rebuildable R8 classes now, but land its final acceptance disposition
with the REST owner's canonical detail route. Compare response bodies after the exact
allowed envelope removal. Include secret exclusion, stable identifiers, null/absent
rules, and every special comparator named by the spec.

Acceptance: one-byte drift, an extra secret field, an omitted rebuild field, or a route
using a second serializer fails. A6 moves to proven only when the canonical REST detail
route and Firehose notice comparison run on the same commit.

## Delivery order and sizing

Cards 1 and 2 are the first weekly slice. Card 1 creates no general framework; it
factors code already used twice, adds two bounded controls, and immediately automates
the A5 4008/reconnect/rebuild gap. Card 2 closes A1/A3. Card 3 follows without a new
process harness. Card 4 promotes the existing manual restart proof into CI, closes the
remaining A5 gateway-kill gap, and automates A7. Card 5 lands with the corresponding
REST slice.

Do not start with another runner audit, broad acceptance ledger, live provider test, or
all-product framework. Those paths cost more and do not close the named Firehose gaps.

## Exit criteria

This strategy is complete when:

- A1-A7 each name an automated test and CI job on exact product bytes;
- A2's existing proof remains unchanged;
- the R8/R8b inventory has no unclassified production mutation or invalidation;
- a real client proves ordinary filtered delivery and model convergence;
- a real client proves both 1012 restart recovery and 4008 slow-consumer recovery in
  CI;
- every Firehose payload matches its canonical REST detail representation where the
  spec requires equivalence; and
- no acceptance claim depends on a manual script, sleep-based timing, shared state, or
  an unverified process signal.
