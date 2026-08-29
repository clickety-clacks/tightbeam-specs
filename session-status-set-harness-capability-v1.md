# Session-status `setHarness` capability amendment v1

Status: candidate for one independent exact-revision review. Mike authorized
the firehose schema amendment through decision
`dr_7f4b03d9-d37f-4889-a118-8be67e9eae45`, option A. This file carries no
implementation, target, specRef binding, merge, release, deployment, or live-state
authority.

This amendment supersedes only these parts of the current contracts:

- the `sessions` R7 row, its wire-schema row, and the session part of R8 in
  `rest-state-api-v1.md`;
- the matching session types and optional-field rule in
  `rest-state-api-v1-wire-schema.md`;
- the session class list and session rows in the R8 registry in
  `event-firehose-v1.md`;
- the `list` session-result row in `cli-surface-v1.md`; and
- the `/api/session-status` compatibility behavior in REST M5.

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
  optional `capabilities` field defined by SH1. Session firehose frames for this
  revision carry `schemaVersion:2`. REST keeps its existing
  `schemaVersion:1` envelope; that number identifies the REST API, not the nested
  session row/event revision.
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
   connection loss or an unsupported firehose schema version, as required by the
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
transaction. After commit, the existing best-effort firehose handoff publishes the
one matching SH6 class from the committed post-mutation item. A `tune set_harness`
commit therefore publishes `session.harness_changed` whose `harness`, model fields,
`capabilities.setHarness`, and `rowVersion` equal the next authorized REST detail
item. The old resident option becomes enabled and the new resident option becomes
disabled in that committed payload. [AC6]

SH8. Session firehose frames emitted by a current producer use
`schemaVersion:2`. Their envelope, resource, operation, refs, visibility, sequence,
and recovery behavior otherwise remain unchanged. REST collection and detail
envelopes keep `schemaVersion:1`. The M5 compatibility route keeps its current
unversioned response shape. The CLI request body for `list` remains unchanged.
[AC3, AC8]

A session-row/event-revision-2 reader accepts an item with absent `capabilities` as a
pre-amendment item, accepts each SH1 capability form, and rejects an object that mixes
`reason` and `options`, omits the selected form's required key, adds a capability key,
or changes an option key or type. A firehose reader that does not support
`schemaVersion:2` applies no part of that notice and follows the existing REST rebuild
path after it gains a compatible decoder.

SH9. Migration order is normative:

1. Ship and verify readers that accept the absent, unsupported, and supported forms.
2. Activate the shared session serializer, canonical REST collection and detail,
   CLI `list` projection, M5 adapter, session-control adapter, SH6 registry, and
   revision-2 session notice encoder in one server boundary.
3. Activate `session.harness_changed` publication at the existing successful
   `tune set_harness` commit seam.

No database migration, backfill, capability cache, or row-schema stamp is introduced.
A server rollback restores each surface's pre-amendment output: canonical session and
CLI/firehose items omit the new field, while an older M5 or session-control adapter may
retain its legacy `setHarness` value. Compatible readers accept either legacy case and
retain their pre-amendment behavior. A restart recomputes byte-identical capabilities
from the same session row and registry.
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
harness cannot remain silent. The publisher receives the committed item and class
after commit; it does not decide whether a harness is desirable or ready.

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
- Given a firehose frame with `schemaVersion:2` and a reader that supports only
  version 1, when the reader receives it, then it applies no partial payload and enters
  the existing compatible-decoder plus REST-rebuild path.

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

- Given one unknown session key and one existing session hidden from the caller, when
  the caller requests each canonical detail and M5 status route, then status, exact
  error body, application headers, statement shape, and timing class match, and the
  capability derivation seam records zero calls.
- Given a subscription whose principal cannot read a changed session, when that
  session commits an SH6 mutation, then the subscriber receives no frame that reveals
  the session key, resident harness, registered options, reason, or existence.

AC6 — Firehose mapping, ordering, idempotency, and restart (SH6, SH7, SH9)

- Given one successful session creation, one rename, one harness switch, and one
  retirement, when the registry and post-commit handoff run, then the observed session
  state-notice sequence is exactly `session.spawned`, `session.harness_changed`, and
  `session.retired` in commit order; the rename emits no session state notice. Each
  emitted frame uses resource `sessions`, operation `upsert`, primary ref
  `sessionKey`, and the matching post-commit R7 item.
- Given a harness switch from `claude` to `codex`, when its transaction commits, then
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
  inspected, then the REST envelope remains `schemaVersion:1` and each session notice
  uses `schemaVersion:2`.
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
- Given step 2 is active, when any SH5 surface is read, then the current producer emits
  one current capability form; no surface emits the absent form.
- Given a rollback to the pre-amendment server after compatible readers ship, when the
  readers rebuild, then they accept the absent canonical form and any legacy M5
  supported form, preserve existing behavior, and require no database rollback or row
  rewrite.

Traceability is two-way: SH1 through SH10 cite their acceptance clauses, and AC1
through AC9 cite the requirements they verify. The optional derived capability pattern
traces only to SH1 through SH5. The session state-class amendment traces only to SH6
through SH9.

## Open Questions

None. This candidate has no blocking or non-blocking holes.
