# Session-status `setHarness` capability amendment v1

Status: successor candidate after changes-requested verdict
`att_cd693728-9ab7-47dd-82ee-e2bf6b290f7b`. That review closed F1 through
F3; this successor changes only F4 through F6. Mike authorized
the firehose schema amendment through decision
`dr_7f4b03d9-d37f-4889-a118-8be67e9eae45`, option A. This file carries no
implementation, target, specRef binding, merge, release, deployment, or live-state
authority.

The canonical amendment set is this file plus these four canonical owners in the
same reviewed revision:

- the `sessions` R7 row, session part of R8, and M5
  `/api/session-status` compatibility behavior in `rest-state-api-v1.md`;
- the matching session types and optional-field rule in
  `rest-state-api-v1-wire-schema.md`;
- the session class list and session rows in the R8 registry in
  `event-firehose-v1.md`;
- the `list` session-result contract in `cli-surface-v1.md`.

The unchanged clauses in those specs remain in force. In particular,
`rest-state-api-v1.md` I2, I4, R7, C1, M5, AU4, and SR1, plus firehose V1 through
V5, govern this amendment except where a clause below is more specific.

## Goal

Publish the elected live harness-switch capability as one exact
`setHarness` value on the canonical session item. Make the value semantically
equal in the CLI, canonical REST, compatibility REST, session-control response,
and session firehose representations.

Let an authorized client distinguish these three wire cases:

1. an older producer omitted `setHarness`;
2. the current producer reports that the session cannot select another harness;
3. the current producer reports the registered harness choices and identifies the
   selectable choices.

## Non-Goals

- This amendment does not change the `tune set_harness` command, its parameters,
  authorization, model election, credential validation, readiness validation, turn
  boundary, history barrier, or failure codes.
- This amendment does not promise that a structurally selectable harness will pass a
  later model, credential, readiness, or concurrent-state check.
- This amendment does not add a session-status command. The existing `list` command
  is the CLI read representation.
- This amendment does not add a second session query, a second session serializer, a
  readiness probe, provider I/O, credential access, or a persisted capability cache.
- This amendment does not expose a credential, credential state, provider, model,
  identity, host path, adapter state, or readiness failure through `setHarness`.
- This amendment does not change another session capability or require a generic
  capability registry.
- This amendment does not change client presentation or edit Clawline.
- Operating pattern taught to agents: none.

## Terms

- **Canonical session item**: the closed `sessions` R7 item returned by
  `GET /api/sessions` and `GET /api/sessions/:sessionKey`. The CLI `list`
  session entry and each rebuildable session notice use this item through the shared
  session serializer.
- **Registered harness catalog**: the ordered harness entries exposed by the same
  build-owned registry that validates the `harness` field of `tune set_harness` and
  supplies the harness catalog in `/api/org` and `/api/catalog/harnesses`. Each entry
  has one nonempty public wire name, and no two entries have the same wire name. This
  is the canonical org capability-vocabulary seam, not host or credential readiness.
- **Resident harness**: the exact `harness` value on the authorized session row used
  to build the item.
- **Structurally selectable harness**: a registered harness whose wire name differs
  from the resident harness. The term states that the selection is not the forbidden
  same-harness operation. It makes no model, credential, adapter, readiness, or turn
  availability claim.
- **Harness option**: the closed object
  `{title:S,value:S,enabled:B}`. `title` and `value` contain the same registered
  harness wire name. `enabled` is true exactly for a structurally selectable harness.
- **`setHarness` capability**: one of two closed objects:
  `{supported:false,reason:S}` or
  `{supported:true,options:A<HarnessOption>}`. The unsupported form contains no
  `options` key. The supported form contains no `reason` key.
- **Absent capability**: a session representation from a producer that predates this
  amendment and therefore has no top-level `capabilities` key or has a legacy
  `capabilities` object without `setHarness`. Absence is input compatibility. A
  current producer emits one of the two current capability forms.
- **Current producer**: a server revision that activates SH1 through SH10 as one
  deployment boundary.
- **Session row/event schema revision 2**: the canonical session item with the
  optional `capabilities` field defined by SH1. Every firehose notice from a
  current producer carries `schemaVersion:2`. REST keeps its existing
  `schemaVersion:1` envelope; that number identifies the REST API, not the nested
  session row/event revision.
- **Firehose protocol version 2**: the upgrade protocol that admits notice
  `schemaVersion:2`. It has no resume cursor or replay token. A pre-amendment
  protocol-1 reader cannot establish this connection.
- **Protocol-offer episode**: one reader attempt sequence. It starts at reader
  process start, manual reload, a change to the reader's installed protocol
  decoders, or automatic recovery after an established socket ends through
  transport loss or firehose C4/D3/D4 code `1008`, `4008`, or `1012`. A
  pre-upgrade `426` advances the same episode; a client-initiated `1002` ends it.
- **Semantically equal capability**: two values have the same capability form, the
  same exact reason when unsupported, or the same ordered option objects when
  supported. Envelope fields outside `setHarness` do not affect this comparison.

## Assumptions

1. The existing session visibility function can select one authorized session row
   before any session item is serialized. An authorization test falsifies this if a
   denied caller reaches the capability derivation seam.
2. The resident harness on each served session row names one entry in the registered
   harness catalog. A serializer test falsifies this if a current producer can emit a
   session item whose resident harness is absent from the catalog.
3. A client replaces its session map from a fresh authorized REST snapshot after
   connection loss or a refused firehose protocol version, as required by the
   existing firehose recovery contract.
4. Current JSON clients tolerate an additive optional session-item key after their
   decoder has passed the compatibility gate in SH8. The gate falsifies this
   assumption against captured current-client fixtures before server activation.

Closure choice: ADD wins because deleting the elected `tune set_harness` capability
would remove a core 0.2 feature, while accepting omission would keep clients guessing
from server identity or stale product flags. The amendment adds one derived field and
one missing state class; it adds no readiness mechanism or stored state.

## Invariants

SH1. The canonical session item appends the optional top-level field
`capabilities` after `mechanicalStatus` and before `rowVersion`.
When present, `capabilities` is the closed object
`{setHarness:O<SetHarnessCapability>}`. No other key is admitted in this object by
this amendment. A current producer always includes `capabilities`; a reader accepts
its absence from a pre-amendment item. [AC1, AC3]

The amended R7 session field order is:

`sessionKey`, `displayName`, `kind`, `orderIndex`, `isBuiltIn`, `adopted`,
`ownerUserId`, `origin`, `spawnedBy`, `handle`, `archetype`, `overrides`,
`identityName`, `identityRevision`, `harness`, `provider`, `model`,
`thinkingLevel`, `modelContext`, `host`, `clearedThroughSeq`, `state`,
`createdAt`, `updatedAt`, `mechanicalStatus`, `capabilities`, `rowVersion`.

SH2. One pure derivation receives only the authorized session row and the registered
harness catalog. It emits the unsupported form with reason exactly
`session is not active` when `state` is not `active`. Otherwise, it creates one
harness option for each registered harness in registry order. It emits the supported
form when at least one option has `enabled:true`. It emits the unsupported form with
reason exactly `no alternate harness is registered` when no option is enabled.
The current producer refuses activation when its build-owned catalog has an empty or
duplicate wire name. If an authorized served session names no catalog entry, the
serializer fails the complete session representation before writing response or
notice bytes; it never emits a partial item or invents an option. [AC1, AC2]

SH3. The derivation sets `title` and `value` to the entry's exact wire name. It sets
`enabled:false` only for the resident harness and `enabled:true` for each other
registered harness. It preserves registry order. It does not inspect or infer model
inventory, catalog health, credentials, provider, identity, adapter readiness, turn
state, elapsed time, or a prior capability value. The later mutation keeps its
existing validation and can refuse a selected option by its existing named reason.
[AC1, AC7]

SH4. The visibility-filtered session query supplies one authorized session-row
snapshot to the shared session-item serializer. The serializer captures the
build-owned catalog once for that item and passes those two values to SH2. REST, CLI,
and firehose adapters do not call SH2 before authorization, add a key to its result,
remove a key from its result, reorder its options, or derive the result again. An
unknown and a forbidden session remain indistinguishable under the existing
authorization contract. [AC4, AC5]

SH5. These representations expose the same SH2 result:

| Representation | Exact location |
|---|---|
| CLI | `tightbeam list` result `sessions[*].capabilities.setHarness` |
| Canonical REST collection | `GET /api/sessions` item `capabilities.setHarness` |
| Canonical REST detail | `GET /api/sessions/:sessionKey` item `capabilities.setHarness` |
| M5 compatibility REST | `GET /api/session-status?sessionKey=...` value `capabilities.setHarness` |
| Session-control write response | `POST /api/session-control` value `status.capabilities.setHarness` |
| Firehose | session notice `payload.capabilities.setHarness` |

The M5 adapter and session-control adapter preserve their other existing fields. They
copy the complete `setHarness` object from the canonical session item; they do not
construct it. No new client adopts the M5 route. [AC4]

SH6. The rebuildable session state classes that carry this capability are exactly
`session.spawned`, `session.harness_changed`, and `session.retired`. Each maps to resource
`sessions`, operation `upsert`, primary ref `sessionKey`, and the shared R7 session
serializer. `session.harness_changed` represents one successful `tune set_harness`
commit whose prior and resulting resident harness values differ. A no-change replay,
refusal, or rolled-back transaction emits no session state notice. Retirement emits
`session.retired`, not `session.harness_changed`. This amendment does not assign a
class to another pre-existing session mutation. [AC6]

SH7. A session mutation writes its item change and higher `rowVersion` in one
transaction. After commit, it invokes the existing best-effort firehose publisher
once with the matching SH6 class and committed post-mutation item. If the publisher
and fan-out remain healthy through that handoff, fan-out accepts one matching notice.
A crash after commit can lose the notice as allowed by firehose D1; authorized REST
remains the rebuild source. A healthy `tune set_harness` handoff carries
`session.harness_changed` whose `harness`, model fields,
`capabilities.setHarness`, and `rowVersion` equal the next authorized REST detail
item. The old resident option becomes enabled and the new resident option becomes
disabled in that payload. [AC6, AC9]

SH8. A pre-amendment producer accepts only firehose `protocolVersion=1` and
emits notice `schemaVersion:1`. A current producer accepts only
`protocolVersion=2` and emits only notice `schemaVersion:2`. At the start of
each protocol-offer episode, a reader constructs the ordered plan `[2,1]`,
removes each version for which it has no decoder, and offers each remaining
version at most once. An HTTP `426` before upgrade has an empty body and creates
no WebSocket, subscription, sequence allocation, close frame, cursor, or
applied notice. On `426`, the reader makes one authorized `GET /api/sessions`
rebuild request, removes the rejected version, and immediately offers the next
plan entry. When no entry remains, it makes no further automatic upgrade until
a new protocol-offer episode starts. Tightbeam has no firehose resume cursor or
replay token. [AC3, AC8, AC9]

A successful protocol-1 upgrade fixes the expected notice schema to `1`; a
successful protocol-2 upgrade fixes it to `2`. There is no separate schema
negotiation. After either upgrade, the reader subscribes first, receives
`subscription_ready`, takes a fresh authorized REST snapshot, and then applies
notices with the new connection's per-connection sequence. If a notice carries
a schema other than the schema fixed by the accepted protocol, the reader
applies neither that notice nor a later notice on the connection, closes the
socket with standard code `1002`, makes one authorized `GET /api/sessions`
rebuild request, and ends the episode without an automatic reconnect. REST
collection and detail envelopes keep `schemaVersion:1`. The M5 compatibility
route keeps its current unversioned response shape. The CLI request body for
`list` remains unchanged.

A current reader accepts an item with absent `capabilities` as a pre-amendment
item, accepts each SH1 capability form, and rejects an object that mixes `reason`
and `options`, omits the selected form's required key, adds a capability key, or
changes an option key or type.

SH9. Migration order is normative:

1. Ship and verify dual-capable readers that retain the protocol-1/schema-1
   decoder, add the protocol-2/schema-2 decoder, accept the absent,
   unsupported, and supported forms, and implement SH8's offer plan and
   refusal recovery. This amendment does not authorize removing the
   protocol-1/schema-1 decoder.
2. In one server activation boundary, install the shared session serializer,
   canonical REST collection and detail, CLI `list` projection, M5 adapter,
   session-control adapter, SH6 registry, protocol-2/schema-2 encoder, and
   `session.harness_changed` publisher. The activation closes each established
   protocol-1 socket with D4 code `1012` before the server admits any
   `tune set_harness` request or serves a current session representation. If
   any member is unavailable, no G9 firehose upgrade, `tune set_harness`
   request, or current G9 session representation becomes routable.

No database migration, backfill, capability cache, or row-schema stamp is introduced.
A server rollback restores each surface's pre-amendment output: canonical session and
CLI/firehose items omit the new field, while an older M5 or session-control adapter may
retain its legacy `setHarness` value. Compatible readers accept either legacy case and
retain their pre-amendment behavior. Rollback closes each established protocol-2
socket with D4 code `1012` before the rollback producer accepts protocol 1 and
emits schema 1. A restart recomputes byte-identical capabilities from the same
session row and registry.
[AC3, AC6, AC9]

SH10. This amendment does not select a product release number. The implementation
release records the compatibility decision required by
`cli-gateway-versioning.md`. The `list` request is wire-identical, and the result
change is additive after SH8's reader gate. While the product remains pre-1.0, the
existing exact CLI/gateway version match and client-update rules remain in force.
Changing the build-owned harness registry requires a normal gateway release. That
release causes the existing protocol reconnect and fresh authorized REST rebuild;
the rebuilt snapshot is authoritative even when the session `rowVersion` did not
change. A running producer does not hot-reload this registry.
[AC8]

## Architecture

The named pattern is **optional derived session capability**. It applies only to
`capabilities.setHarness` on the canonical session item and the compatibility
locations in SH5. It does not establish a generic capability system or a readiness
projection.

The session visible-query seam returns the authorized row to the sole session-item
serializer. The serializer captures the registered harness catalog and passes both
values to one pure function that implements SH2 and SH3. The serializer places the
result at SH1's exact key position. The CLI, REST, compatibility adapters, and
firehose call that serializer or copy the complete `setHarness` object from its
output.

The existing session mutation transactions remain the sole mutation seams. This
amendment introduces no state. The firehose registry adds
`session.harness_changed` so the exact commit that changes this capability's resident
harness has one registered post-commit publisher handoff. The publisher receives
the committed item and class after commit; it does not decide whether a harness is
desirable or ready, and D1 still permits a crash to lose the notice.

The strongest affordable enforcement rung is a closed serializer plus registry and
transport contract tests. A second `setHarness` builder, a third capability form, an
unregistered session mutation class, or a secret-bearing option fails the tests before
release.

## Acceptance

AC1 — Supported closed shape (SH1 through SH3)

- Given an authorized active session whose resident harness is `claude` and a
  registered catalog ordered `claude`, `codex`, when each SH5 representation is
  serialized, then `setHarness` is exactly
  `{"supported":true,"options":[{"title":"claude","value":"claude","enabled":false},{"title":"codex","value":"codex","enabled":true}]}`
  after removal of its enclosing representation.
- Given the same entries supplied from maps with randomized insertion order 1,000
  times, when the shared serializer runs, then each encoded `setHarness` byte string
  equals the canonical registry-order bytes above.
- Given a supported capability, when the wire-schema validator inspects it, then it
  rejects `reason`, an extra option key, a non-boolean `enabled`, or a title that
  differs from value.

AC2 — Unsupported closed shape (SH2)

- Given an authorized retired session and two registered harnesses, when the shared
  serializer runs, then `setHarness` is exactly
  `{"supported":false,"reason":"session is not active"}` and contains no
  `options` key.
- Given an authorized active session and a registry that contains only its resident
  harness, when the shared serializer runs, then `setHarness` is exactly
  `{"supported":false,"reason":"no alternate harness is registered"}` and
  contains no `options` key.
- Given a retired session and a registry with no alternate harness, when the shared
  serializer runs, then the first exact reason wins: `session is not active`.
- Given a build-owned registry with an empty or duplicate wire name, when the current
  producer activation gate runs, then activation fails before any current-producer
  session representation is served.
- Given an authorized session whose resident harness is absent from an otherwise
  valid catalog, when any SH5 representation is requested or published, then the
  complete representation fails before response or notice bytes and no partial
  session item is emitted.

AC3 — Absent-form and version compatibility (SH1, SH8, SH9)

- Given captured pre-amendment CLI and session-notice fixtures that omit
  `setHarness`, a normative pre-amendment canonical REST item that omits it, and
  captured M5 and session-control fixtures that carry the legacy supported form, when
  a compatible current reader decodes them, then it records the absent or supported
  form and preserves the client's pre-amendment behavior.
- Given captured current-client decoders, when each decodes an otherwise unchanged
  session item with SH1's optional field, then it either accepts and ignores the field
  or reads the closed capability; no existing display, session selection, or control
  action changes.
- Given a current producer and a reader that supports only protocol 1, when the
  reader requests `protocolVersion=1`, then the server returns HTTP
  `426` before upgrade with no body, socket, subscription, sequence, close frame,
  cursor, or applied notice. The reader makes one authorized `GET /api/sessions`
  rebuild request, exhausts its one-entry plan, and makes no further automatic
  upgrade until a new protocol-offer episode starts.
- Given a dual-capable reader and a pre-amendment producer, when a protocol-offer
  episode starts, then the reader offers `2`, receives the empty `426`, makes the
  one refusal rebuild, offers `1` once, subscribes, receives ready, takes a
  separate fresh post-ready snapshot, and accepts only schema 1 on that connection.
- Given either an accepted protocol-1 connection with a notice whose
  `schemaVersion` is not `1` or an accepted protocol-2 connection with a notice
  whose `schemaVersion` is not `2`, when the reader receives it, then it applies
  no part of that or a later notice, closes with `1002`, makes one authorized
  `GET /api/sessions` rebuild, ends the episode, and makes no automatic reconnect.

AC4 — Representation equality (SH4, SH5)

- Given one authorized active session, when the client reads CLI `list`, canonical
  REST collection and detail, M5 session status, a successful session-control response,
  and a matching session notice, then extracting each SH5 location produces six
  semantically equal values.
- Given a test double that changes the shared SH2 result between calls, when each
  adapter runs once, then each representation proves it consumed the session
  serializer output and no adapter invoked a second derivation.
- Given a catalog test double that returns a different order on a second read, when
  one session item is serialized, then the double records one read and every option
  follows that captured order.

AC5 — Authorization before existence (SH4)

- Given one visible session and one session hidden from the caller, when the caller
  requests the canonical collection and CLI `list`, then each result contains only
  the visible session and an instrumented capability derivation seam records one
  call for the visible key and zero calls for the hidden key on each surface.
- Given one unknown session key and one existing session hidden from the caller, when
  the caller requests each canonical detail and M5 status route, then status, exact
  error body, application headers, statement shape, and timing class match, and the
  instrumented capability derivation seam records zero calls for either key.
- Given the same unknown and hidden keys, when the caller submits the corresponding
  denied session-control requests, then their existing authorization-before-existence
  responses match and the instrumented capability derivation seam records zero calls
  for either key.
- Given a sole subscription whose principal cannot read a changed session and no
  concurrent authorized read or subscription for that session, when the session
  commits an SH6 mutation, then the subscriber receives no frame that reveals the
  session key, resident harness, registered options, reason, or existence, and the
  instrumented capability derivation seam records zero calls for the hidden key.

AC6 — Firehose mapping, ordering, idempotency, and restart (SH6, SH7, SH9)

- Given one successful session creation, one rename, one harness switch, and one
  retirement while the publisher and fan-out remain healthy through each handoff,
  when the registry and post-commit handoff run, then the observed session
  state-notice sequence is exactly `session.spawned`, `session.harness_changed`, and
  `session.retired` in commit order; the rename emits no session state notice. Each
  emitted frame uses resource `sessions`, operation `upsert`, primary ref
  `sessionKey`, and the matching post-commit R7 item.
- Given a harness switch from `claude` to `codex` whose publisher and fan-out remain
  healthy through handoff, when its transaction commits, then
  the one `session.harness_changed` payload has the higher `rowVersion`, resident harness
  `codex`, disabled `codex` option, enabled `claude` option, and a `setHarness` value
  semantically equal to the next authorized REST detail item.
- Given a duplicate no-change mutation, a named refusal, and a rollback, when the
  publisher runs, then none emits a session state notice or changes `rowVersion`.
- Given a committed session item, when the service restarts without a session or
  registry change, then the authorized REST item before and after restart has
  byte-identical `capabilities`, and no restart-only session notice is emitted.

AC7 — Privacy and non-readiness boundary (SH3)

- Given fixtures whose credential values, credential health, provider, model,
  identity, adapter readiness, queued turns, and running-turn state differ while the
  authorized session `state`, resident `harness`, and registered catalog remain equal,
  when the shared serializer runs, then every `setHarness` byte is equal.
- Given secrets placed in each credential and identity source, when each SH5
  representation is encoded, then `setHarness` contains only `supported`, the exact
  generic reason when unsupported, or `title`, `value`, and `enabled`; no secret,
  provider, model, identity, host path, adapter error, or readiness reason appears.
- Given a supported option whose later mutation fails model, credential, readiness,
  or turn-boundary validation, when the failure returns, then the failure keeps its
  existing named code and the capability serializer performs no mutation or probe.

AC8 — Wire and CLI compatibility decision (SH8, SH10)

- Given a pre-amendment and current `tightbeam list` call, when the CLI request bytes
  are compared, then they are equal. The current response differs only by the additive
  session capability required by SH1 and any canonical-session fields already required
  by REST C1.
- Given current session REST and firehose outputs, when their version fields are
  inspected, then the REST envelope remains `schemaVersion:1`, the firehose upgrade
  uses `protocolVersion=2`, and each notice uses `schemaVersion:2`.
- Given the implementation release record, when the release gate checks it, then it
  states the CLI/gateway compatibility decision and retains the existing pre-1.0 exact
  version-match rule.
- Given a release whose registered harness catalog differs from the prior build, when
  a client reconnects, then it performs the existing fresh authorized REST rebuild
  and replaces the prior options even when the session `rowVersion` is unchanged.

AC9 — Migration and rollback (SH9)

- Given compatible readers have not completed SH9 step 1, when the server activation
  gate is evaluated, then SH9 step 2 does not start and server outputs retain their
  pre-amendment shapes.
- Given any SH9 step-2 member is unavailable, when the server activation gate runs,
  then the current producer admits no `tune set_harness` request and serves no
  current session representation.
- Given the step-1 dual-capable reader has an established protocol-1 connection
  to the pre-amendment producer, when step 2 activates, then the server closes
  that socket with `1012`; the new episode offers `2` once, subscribes, receives
  ready, takes a fresh post-ready snapshot, and accepts schema 2.
- Given step 2 is active, when a `tune set_harness` commit changes the resident
  harness while the publisher and fan-out remain healthy through handoff, then the
  current representation is observable and fan-out accepts exactly one
  `session.harness_changed` notice; no activation interval permits the representation
  or commit without the publisher being installed and routable.
- Given the publisher or fan-out crashes after that commit before completing the
  handoff, when the reader performs its next D1b heartbeat/sequence rebuild or
  reconnect rebuild, then zero notice is permitted and the authorized REST snapshot
  exposes the higher `rowVersion` and current capability.
- Given a rollback to the pre-amendment server closes a dual-capable reader's
  protocol-2 socket with D4 code `1012`, when the new protocol-offer episode runs,
  then the reader offers `2`, receives the empty `426`, makes the one refusal
  rebuild, offers `1` once, subscribes, receives ready, takes a separate fresh
  post-ready snapshot, accepts schema 1, accepts the absent canonical form and any
  legacy M5 supported form, preserves existing behavior, and requires no database
  rollback or row rewrite.

Traceability is two-way: SH1 through SH10 cite their acceptance clauses, and AC1
through AC9 cite the requirements they verify. The optional derived capability pattern
traces only to SH1 through SH5. The session state-class amendment traces only to SH6
through SH9.

## Open Questions

None. This candidate has no blocking or non-blocking holes.
