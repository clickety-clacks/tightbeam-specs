# Tightbeam testing proof strategy v1

Status: PROPOSED, 2026-08-28. Target unset.

Product evidence baseline: `tightbeam` main
`de135169a34c134861bfaa59267b2e3e6706faa3`.
Specification baseline: `tightbeam-specs` main
`307210c542701b714df88a4ca778cab434dca35d`.

## Spirit

The test system must answer one question: **which user-visible claim is proven, by
which executable evidence, on which exact bytes?** A green aggregate is useful, but it
is not a product proof. An activity report is not a product proof either.

Tightbeam will make the smallest real journey the normal unit of acceptance. The
default journey uses one external client, one gateway/controller, an isolated database,
an ephemeral port, and the public protocol. It proves one claim and fails near its
cause. Larger suites then prove composition. Live tests remain only for seams that a
local process cannot represent.

The standing detection question is:

> What changed on the deliverable since the last look?

For testing, the deliverable is a named acceptance claim moving from unproven to proven.
Test count, runtime, retries, audit rows, and green unrelated suites are supporting data.
They do not substitute for that movement.

## Decision

Adopt the one-client/one-controller hermetic micro-system test as the center of the
strategy. Do not use it as the only kind of test.

The hypothesis is right because the most costly current gaps cross a public boundary:
HTTP or WebSocket framing, authentication, visibility, commit publication, reconnect,
and rebuild. Pure module tests can make every component green while those seams remain
broken. A full live-org or all-feature journey reaches the seams, but it is slow,
failure-coupled, expensive, and difficult to diagnose. The existing
`test/firehose_smoke_test.exs` already demonstrates the useful shape: a real TCP
WebSocket client, a real in-process Bandit gateway, an isolated database, an ephemeral
port, and no provider credential.

Use three complementary forms:

1. Use table and property tests for closed sets, ordering, serializer identity, cursor
   algebra, and authorization matrices.
2. Use one-client/one-controller micro-system tests for ordinary public journeys.
3. Use a real subprocess only when process death, restart, port handoff, or boot order is
   the claim. Use a live provider or client only when that external boundary is the
   claim.

A micro-system test is not end-to-end if it calls the handler or publisher directly. It
must enter through the public HTTP/WebSocket surface, use the production serializer and
authorization path, commit through the production state seam, and observe the result as
a client would.

## Proof tiers and allowed assumptions

| Tier | Purpose | Allowed assumptions | Forbidden shortcut | CI target |
|---|---|---|---|---|
| T0 runner contract | Prove the test artifact and prerequisites are the intended ones. | Pinned OTP/Elixir and Rust can be installed by the runner. | Pre-existing CLI binary, undisclosed PATH repair, a non-distributed direct `mix test`, or turning a required prerequisite into a skip. | Every job, before tests. |
| T1 contract/property | Prove closed tables, serializers, visibility matrices, filtering, cursors, ordering, and exact bytes. | In-process modules, isolated database, deterministic clock/data. | Claiming a transport or client journey. | Every change; focused inner loop. |
| T2 hermetic micro-system | Prove one ordinary journey through a real public boundary. | One real client, one in-process gateway/controller, temp database and directory, ephemeral port, fixture credential, no external network. | Direct handler calls, mocked wire, shared ports/state, sleeps as synchronization. | Every pull request and push. |
| T3 hermetic process/fault | Prove boot, shutdown, restart, overflow, disconnect, and rebuild. | One real client and one real disposable gateway subprocess; bounded fault injection. | Signaling an unverified process, shared live state, wall-clock starvation as the oracle. | Every affected change; all main builds. |
| T4 full regression | Prove product-wide composition on supported operating systems. | T0 has built the exact release CLI and started the distributed test node. | Treating aggregate green as proof of an unmapped acceptance clause. | Linux and macOS on every pull request. |
| T5 live boundary | Prove a real provider, harness, satellite, ATC, or Clawline boundary. | Fresh disposable state, sanctioned credential, minimal paid turns, explicit cleanup and receipts. | Using a live test for behavior already representable hermetically, or silently omitting an unavailable credential leg. | Scheduled, release, and touched-boundary gates. |

Initial time budgets are guardrails, not coverage reductions: a T2 test should finish in
10 seconds and its lane in 2 minutes; a T3 journey should finish in 90 seconds and its
lane in 5 minutes; T4 should stay below 10 minutes. Crossing a budget opens a performance
or decomposition finding. It does not authorize deleting the assertion.

## Runner honesty

The environment is runnable. On Gibson the known tool paths are
`~/.local/opt/elixir-1.19.5/bin` and `~/.cargo/bin`. The product suite requires the exact
release CLI to be built before Elixir tests:

```text
cargo build --release --manifest-path cli/Cargo.toml
scripts/verify_mix.sh
```

The earlier six-failure result and the canonical runner result describe different
contracts, not an unrunnable host:

- `scripts/verify_mix.sh` already creates a unique distributed node and verifies its
  marker. The five Cursor signing failures occur under direct, non-distributed
  `mix test`.
- The sixth failure is a RailScript backstop timing test. Its 30-second sleeper and
  wall-time assertion are a scheduling oracle, so machine load can decide the result.
- CI builds `cli/target/release/tightbeam` before the Elixir gate. The canonical local
  script does not own that build, while RailScript has compile-time binary-exists
  branches that can turn missing required evidence into skips.

Fresh-clone verification on 2026-08-28 at exact product commit `de135169` first proved
two caller-owned prerequisites: the release CLI build and `mix deps.get`. After those
steps, the authoritative distributed gate completed in 362.5 seconds with **9 doctests,
1,895 tests, 1 failure, and 11 skipped**. The sole failure was RailScript's starvation
case: it expected `script_timeout/timeout` and received `script_error/unreported`. Thus
current main is runnable and not green. The non-distributed path adds the five Cursor
signing failures; it is not the authoritative runner.

Make one command own the complete local and CI contract. It must add the two known tool
directories, print tool versions, build the release CLI from the checked-out source,
verify its source identity, start the unique distributed node, and run the suite. CI and
humans must call that same command. A missing tool, stale binary, wrong node, required
skip, or failed cleanup must exit non-zero with the corrective command in the message.

Replace the RailScript timing oracle with an explicit child-start barrier and a
controllable deadline or process signal. The test should prove that the wrapper kills a
known-running child after the deadline. It should not infer that claim from host elapsed
time.

Required acceptance evidence never skips. A platform-specific or credential-dependent
test belongs in a named lane whose absence makes that lane incomplete. It does not count
as green proof elsewhere.

## Current CI truth

Current `.github/workflows/ci.yml` does the following on Linux and macOS:

- installs pinned OTP 28, Elixir 1.19.5, and Rust;
- builds the release Rust CLI;
- runs formatting and `scripts/verify_mix.sh` on a distributed node;
- runs Rust formatting/tests and package checks.

`test/firehose_smoke_test.exs` is part of ordinary ExUnit and therefore runs in that
lane. `scripts/firehose_restart_smoke.exs` is manual. No current workflow invokes it.
`client_e2e/ws.ex` contains no firehose subscription journey. The conformance manifest
still carries pending P6/P7 coverage, so those entries prove nothing.

The required CI shape is:

1. T0 is one canonical command used locally and by every operating-system job.
2. T1 and T2 run on every pull request. Their names identify the acceptance clauses they
   prove.
3. T3 runs on every main build and on a pull request that changes the gateway, socket,
   lifecycle, queue, or restart seam. The firehose restart journey moves here.
4. T4 remains the Linux/macOS regression matrix.
5. T5 runs on a schedule, before release, and when a touched external seam requires it.
6. CI validates a machine-readable acceptance ledger. A clause cannot say `proven`
   unless the named test exists and its named job ran on the exact commit.

## Firehose acceptance map

The status below is for full `event-firehose-v1` acceptance on product main
`de135169`. `Partial` means useful component evidence exists but the complete acceptance
oracle does not. The independent REST-owner coverage contribution
`art_8daabc76` / `att_79edc555` reaches the same disposition from its exhaustive
item-by-item audit at product `01c52e16`; the later `de135169` restart-smoke repair does
not add a CI invocation or close another acceptance item.

| Item | Status | Existing evidence | Missing proof and required tier |
|---|---|---|---|
| A1 registry both-ways diff | Partial | `test/change_socket_test.exs`; `test/admin_projection_test.exs` | One table must diff every main-tip state mutation and source invalidation both ways against R8/R8b. T1. |
| A2 registration cut | Proven | `test/change_socket_test.exs` | Keep the post-registration commit cut as a named T2 assertion. |
| A3 filtered delivery | Partial | `test/change_socket_test.exs` proves class/ref multiplex filters and visibility ordering. | Complete every R8/R8b filter value and absent-ref case through one real subscriber. T1 table plus T2 journey. |
| A4 M1 convergence | Partial | `test/firehose_smoke_test.exs`, `test/admin_projection_test.exs`, `test/firehose_publisher_test.exs` | Prove the full multi-resource create/update/delete model, duplicate/older notice handling, and restart-safe delete/recreate version ordering. T1 plus T2/T3. |
| A5 kill-gateway rebuild | Partial | `test/change_socket_test.exs` proves 1012 and 4008 units; `scripts/firehose_restart_smoke.exs` proves a manual restart/rebuild journey. | Put real gateway kill/restart and slow-consumer 4008 reconnect/rebuild in automated T3. |
| A6 byte-equivalent payloads | Partial | `test/firehose_publisher_test.exs` and `test/admin_projection_test.exs` compare several projections and notice bytes. | Table every R8 class against its canonical REST detail serializer and reject extra/secret fields. T1. |
| A7 real external consumer smoke | Partial | `scripts/firehose_restart_smoke.exs` has historical manual evidence with a real script client. | Run a real external consumer in CI, including subscribe, notice, disconnect, restart, rebuild, and convergence. T3. A real ATC/Clawline proof remains T5 when that client surface lands. |

No existing automated test proves the whole A1-A7 set. A real client has subscribed,
received notices, survived a restart, and rebuilt in the manual restart smoke. That
script is not currently a CI proof.

## REST acceptance map and coordination boundary

The canonical `rest-state-api-v1` defines A1-A43, plus A8a and A13a. The canonical REST
surface is not implemented on current product main. Current routes are legacy/partial
surfaces such as `/api/work`, `/api/work-items`, `/api/streams`, and
`/api/trackable-sessions`. Therefore **no canonical REST acceptance item is fully proven
end-to-end on current main**. The component evidence is still valuable and must be
reused rather than rewritten.

| Acceptance group | Full status | Reusable component evidence | Owner boundary |
|---|---|---|---|
| A1-A4 registry, REST/notice identity, closed projections, convergence | Unproven | `test/firehose_publisher_test.exs`, `test/admin_projection_test.exs`, `test/firehose_smoke_test.exs` | REST owner supplies canonical routes/serializers; testing card supplies ledger and common test kit. |
| A5-A6 pagination and indistinguishable authorization | Unproven | `test/work_state_test.exs` covers current ordering/filter/recovery; router tests cover current authorization. | REST implementation cards own R5/AU7/AU8 behavior. |
| A7-A8a real clients, CLI parity, and `asUser` | Unproven | Existing client-e2e and CLI tests prove older surfaces only. | REST owner maps migrations and parity cases. T5 owns the final real-client proof. |
| A9-A18 read markers, visibility, nested/download, safe values, aliases, composed views, admin, schema, facts | Unproven | `test/admin_projection_test.exs`, `test/router_test.exs`, and current domain tests cover parts. | Implement by REST slice; use T1 matrices and T2 route journeys. |
| A19-A29 Toplines/ExecutionMap shape, filtering, trees, provenance, markers, errors, and R8b notices | Unproven | `test/execution_map_test.exs`, `test/toplines_test.exs`, and publisher tests cover domain composition. | The REST owner owns route slices; firehose card owns only shared R8b registry/parity assertions. |
| A30-A37 Topline pagination, normalized filters, selectors, route seams, closed errors and precedence | Unproven | Current topline/domain and router tests are partial. | REST owner supplies route/error adapters; the shared kit supplies deterministic cursor/auth matrices. |
| A38-A43 message type, transcript/open-reader/detail routes, principals, auth and errors | Unproven | Existing transcript/message projection and router tests are partial. | REST owner owns R3c delivery; shared tests reuse the canonical serializer. |

Coordination rule: `product-owner:rest-state-api` owns the canonical A1-A43 implementation
map, route slices, and their product cards. This testing strategy owns the proof tiers,
acceptance-ledger schema, runner contract, and reusable harness. A REST implementation
card references the shared harness and updates its own acceptance rows; this card does
not create duplicate REST feature work.

The coordinated evidence is durable as `art_8daabc76`, progress `att_79edc555`, and
completion `att_3b6cc07c`. It confirms that Firehose A2 alone has direct automated proof,
Firehose A7 is manual-only, and no REST A1-A43 item has complete current-main proof.

## Acceptance ledger

Add a machine-readable ledger in the product repository for each canonical acceptance
set. Each row records:

- specification file and SHA-256;
- acceptance id;
- `proven`, `partial`, `unproven`, or `external`;
- exact test file and test name;
- proof tier and CI job;
- the product commit on which the latest proof ran.

CI rejects a missing acceptance id, an unknown extra id, a `proven` row whose test or
job is absent, and a changed canonical spec hash without a ledger review. `Partial` and
`external` remain visible; they do not count as proven. This ledger makes the answer to
“does firehose A5 pass?” a lookup followed by an executable test, not a two-week audit.

## Ordered delivery cards

The order is deliberate. Do not start broad acceptance work on an ambiguous runner.

### 1. Make one runner truthful — first card, sized for this week

Make one supported command own PATH, release CLI build, source identity, distributed
node, exact suite invocation, and cleanup. Use it in CI and local guidance. Delete
RailScript's required-binary skip paths and fail loud on prerequisites. Acceptance: a
clean checkout runs without operator folklore; removing cargo, Elixir, the binary, or
distributed mode causes one actionable non-zero refusal; CI calls the same command.

### 2. Remove the RailScript timing oracle

Replace starvation and wall-time inference with a child-start barrier plus deterministic
deadline/process observation. Prove the wrapper kills the intended child and closes its
resources under load. Acceptance: 100 repeated focused runs on a loaded host have zero
flake, and the test fails when kill/backstop behavior is disabled.

### 3. Install the acceptance ledger rail

Add the machine-readable Firehose A1-A7 and REST A1-A43 inventories with current honest
statuses. Add CI validation for completeness, test existence, job execution, and spec
hash changes. Acceptance: deleting an id, naming a nonexistent test, or claiming proof
from a job that did not run fails CI.

### 4. Extract the hermetic one-client/one-controller kit

Turn the proven setup in `test/firehose_smoke_test.exs` into reusable support for one
real HTTP/WebSocket client, one in-process gateway, temp database/directory, ephemeral
port, deterministic barriers, and strict teardown. Acceptance: a representative REST
journey and firehose journey use it; parallel runs do not share state or ports; leaked
processes fail the test.

### 5. Close Firehose A1-A4 and A6

Add the registry both-ways diff, complete filter/visibility matrix, multi-resource M1
convergence journey, and REST/notice byte-identity table. Reuse the shared kit and
canonical serializers. Acceptance: A1-A4 and A6 ledger rows become proven on named T1/T2
tests; injected missing/extra mappings, stale versions, visibility leaks, or serializer
drift fail.

### 6. Automate Firehose restart and slow-consumer recovery

Port `scripts/firehose_restart_smoke.exs` into the T3 CI lane and add the 4008
slow-consumer reconnect/rebuild journey. Keep one client and one disposable gateway
process. Acceptance: A5 and the script-consumer portion of A7 become automated proof;
PID identity, port closure, 1012/4008, resubscription, rebuild, and final model
convergence are asserted.

### 7. Apply the kit to each REST delivery slice

Coordinate with `product-owner:rest-state-api`. For each product slice, require its T1
closed tables, T2 public-route journeys, acceptance-ledger changes, and exact error-byte
tests in the same review. Start with the smallest rebuildable state slice needed by the
firehose; do not create a second REST roadmap here. Acceptance: no REST clause moves to
proven before its canonical route and public client journey exist.

### 8. Finish P6/P7 and real-client proof

Implement or explicitly block the pending conformance mechanisms; a pending manifest
entry remains unproven. Add the minimal T5 ATC/Clawline and provider/harness journeys
needed for external seams, with sanctioned disposable state and exact receipts.
Acceptance: P6/P7 are green or carry one explicit product dependency; Firehose A7 and
REST A7 name the real client, exact commit, and repeatable lane.

## Exit criteria

This strategy is working when all of the following are true:

- a clean checkout has one truthful command and no required skip;
- every canonical acceptance id has one ledger row;
- every `proven` row names an executable test and CI job on exact bytes;
- ordinary public journeys use hermetic one-client/one-controller tests;
- restart claims use a real disposable subprocess;
- live tests are few, explicit, and limited to genuinely external seams;
- a product owner can answer “what remains unproven?” from the ledger without another
  evidence audit.
