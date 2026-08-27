# REST state API v1 — normative wire schema

Status: normative companion to `rest-state-api-v1.md` r3 review draft.

Amendment candidate, 2026-08-25: add the ExecutionMap composed response,
closed error envelope, and dependency-entry schema. The durable Toplines
schema below is unchanged.

G2 session-freshness amendment candidate, 2026-08-27: session item keys and
types remain unchanged. The complete item, including materialized
`mechanicalStatus`, is the versioned value shared by REST and the three
`session.*` firehose classes.

## Encoding rules

JSON is UTF-8. Integers are signed JSON integers and never floating-point
encodings. Timestamps are Unix epoch milliseconds. Fields typed `S` below and
all digests are strings. ExecutionMap's non-resource dependency-vector primary
keys use the exact types defined under “Canonical array and map order.”
`rowVersion` is a positive integer. `dependencyVersion` is a lowercase
64-character SHA-256 hex string.

For a sessions item, `rowVersion` changes if and only if at least one other
serialized R7 field changes. The transaction stores the greater version with
the changed item before its post-commit session notice becomes eligible for
publication. `mechanicalStatus` is exactly `idle` when the committed count of
this session's turns with `status` equal to `queued` or `running` is zero, and
exactly `running` when that count is positive. No other value or mutable input
is valid. A turn transaction that crosses the zero/positive boundary stores
the new `mechanicalStatus` and session `rowVersion` atomically. The serializer
reads that stored value; it does not count turns or compute the field from
another mutable input.

The condition-fact projection `id`, firehose notice `refs.factId`, and natural
version are positive JSON integers with the same numeric value.
`facts.rowVersion` equals `facts.id`. A decimal string is invalid for any of
these three fields. `facts.id` is the sole numeric public field named `id` in
v1.

Every item contains exactly the keys listed by R7/R7a, in that listed order.
Nested objects contain exactly the keys listed here, in their listed order.
The encoder emits no insignificant whitespace. It escapes JSON strings by the
same library path for REST, CLI, and firehose.

Maps whose keys are product data encode keys in ascending Unicode code-point
order. Set-like arrays sort by the tuple named below. Sequence arrays preserve
the named semantic order. Null is allowed only where this file names it.

Notation: `S` string, `I` integer, `B` boolean, `N` JSON number, `O<T>` closed
object shape T, `M<T>` string-keyed map of T, and `A<T>` array of T.
`J` is an opaque user-content JSON value. J objects recursively sort keys;
J arrays preserve author order. J is permitted only for the fields explicitly
typed J below and still passes SR2/SR6 secret exclusion.

## Shared closed shapes

- `Actor`: `{kind:S, ref:S}`; kind is `user|session`.
- `Attachment`: `{assetId:S, mimeType:S, filename:S, size:I}`.
- `CommitRef`: `{repo:S, commit:S}`.
- `Document`: `{path:S, content:S, sha256:S}`.
- `McpServer`: `{name:S, envNames:A<S>}`.
- `Reference`: `{name:S, location:S, access:S|null}`.
- `ModelPreference`: `{model:S, effort:S, context:S|null}`.
- `ReasoningLevel`: `{effort:S, description:S}`.
- `ModelCapabilities`:
  `{supportedReasoningLevels:A<O<ReasoningLevel>>}`.
- `HarnessModel`: `{provider:S, model:S, displayName:S, efforts:A<S>,
  capabilities:O<ModelCapabilities>}`.
- `HarnessCapability`: `{name:S, supported:B}`.
- `ArchetypeDefaults`:
  `{harness:S|null, model:O<ModelPreference>|null}`.
- `Containment`: `{fs:S, network:S}`.
- `SessionOverrides`: `{skillsAdd:A<S>, guidanceExtra:S|null}`.
- `DecisionOption`: `{label:S}`.
- `ToplineMembership`: `{id:S, toplineId:S, workItemId:S,
  ownerUserId:S, linkReason:S, linkedActor:O<Actor>, linkedAt:I,
  unlinkReason:S|null, unlinkedActor:O<Actor>|null, unlinkedAt:I|null,
  workItemTitle:S, workItemState:S}`.
- `Concern`: `{id:S, kind:S, note:S, createdAt:I}`.
- `Attribution`: `{provenanceStatus:S, reasonKind:S|null,
  primaryWorkKind:S|null, primaryWorkId:S|null}`.
- `ExecutionMapOrigin`: `{principal:S, createdBy:S}`.
- `ExecutionMapCreationContext`: `{recorded:B, turnSeq:I|null}`.
- `ExecutionMapParent`: `{status:S, item:S|null}`.
- `ExecutionMapOutcomes`: `{completed:I, surrendered:I, revoked:I}`.
- `ExecutionMapAssignmentCounts`:
  `{open:I, closed:I, byOutcome:O<ExecutionMapOutcomes>}`.
- `ExecutionMapAttestCounts`:
  `{total:I, byKind:M<I>, byVerdictKind:M<I>}`.
- `ExecutionMapClosingAttest`:
  `{assignmentId:S, attestId:S, commitRefs:A<O<CommitRef>>|null}`.
- `ExecutionMapTurns`: `{total:I|null, lastEndedAt:I|null}`.
- `ExecutionMapMind`:
  `{model:S|null, context:S|null, effort:S|null, harness:S|null}`; an object
  with both `model` and `harness` null is absent from the array.
- `ExecutionMapActive`:
  `{runningTurn:B, pendingSessionWake:B, pendingWakeClasses:M<I>}`.
- `ExecutionMapCoverage`:
  `{attributionCutoff:I, basis:S}`; basis is `conservative_shared`.
- `Page`:
  `{oldestCursor:S|null, newestCursor:S|null, hasMoreBefore:B,
  hasMoreAfter:B}`.

ExecutionMap responses are closed top-level objects in this key order:

- flat: `{schemaVersion:I, resource:S, edgeBasis:S,
  coverage:O<ExecutionMapCoverage>, dependencyVersion:S,
  items:A<O<execution map node>>, page:O<Page>}`;
- tree and subtree: `{schemaVersion:I, resource:S, edgeBasis:S,
  coverage:O<ExecutionMapCoverage>, dependencyVersion:S,
  roots:A<O<ExecutionMapTreeNode>>}`;
- assignments: `{schemaVersion:I, resource:S, edgeBasis:S,
  coverage:O<ExecutionMapCoverage>, dependencyVersion:S,
  items:A<O<execution map node>>, noItem:A<S>}`.

`resource` is exactly `execution map`; `edgeBasis` is exactly
`concurrent_turn`. `ExecutionMapTreeNode` contains the execution-map-node keys
in the R7 order followed by `children:A<O<ExecutionMapTreeNode>>`. No unpaged
response contains `page`, and no flat or assignment-selected node contains
`children`.

ExecutionMap error responses are closed top-level objects in this key order:
`{schemaVersion:I, resource:S, error:O<ExecutionMapError>}`.
`schemaVersion` is exactly `1`; `resource` is exactly `execution map`.
`ExecutionMapError` is one of these closed variants:

- `{code:S}`, where `code` is exactly one of `auth_failed`,
  `invalid_as_user`, `invalid_message`, `not_found`, `invalid_filter`,
  `malformed_query`, `invalid_cursor`, or `projection_invalid`;
- `{code:S, message:S}`, where `code` is exactly `identity_not_yours` and
  `message` is exactly `this session belongs to <session.owner_user_id>`, with
  `<session.owner_user_id>` replaced by the target session row's exact stored
  non-null owner user id;
- `{code:S, candidateIds:A<S>}`, where `code` is exactly `ambiguous_id` and
  `candidateIds` contains visible full typed ids in ascending order.

`identity_not_yours` is the sole message-bearing variant. No other error
variant contains `message` or another key. The encoder emits no insignificant
whitespace. Each ExecutionMap response sets exactly the application headers
`Content-Type: application/json; charset=utf-8` and `Cache-Control: no-store`.

## Resource field types and nullability

Fields not listed under “nullable” are required and non-null. Enum fields use
the domains in the next section.

### Catalog and identity

| Resource | Strings | Integers | Booleans | Arrays / objects | Nullable |
|---|---|---|---|---|---|
| org | id, dependencyVersion | — | — | archetypes `A<S>`, hosts `A<S>`, modelCatalog `A<O<HarnessModel>>` | none |
| harness catalog | harness, provider, dependencyVersion | — | — | models `A<O<HarnessModel>>`, capabilities `A<O<HarnessCapability>>` | none |
| hosts | host | rowVersion | — | — | none |
| identity | name, liveRevision, state | rowVersion | — | sessionRevisions `M<S>`, staleness `A<S>`, conflicts `A<S>` | none |
| archetypes | name, compiledGuidance, sourceSha256, dependencyVersion | — | — | skills `A<S>`, where `A<S>`, defaults `O<ArchetypeDefaults>`, references `A<O<Reference>>`, modelPreferences `A<O<ModelPreference>>`, containment `O<Containment>`, mcpServers `A<O<McpServer>>` | none |
| kungfu | name, purpose, rootArchetype, installedRevision, status | rowVersion | — | phrases `A<S>`, documents `A<O<Document>>` | installedRevision |
| guidance | name, content, sha256, dependencyVersion | — | — | — | none |
| rails | name, on, mode, tool, pattern, text, dependencyVersion | — | — | — | none |
| config | key, value | updatedAt, rowVersion | — | — | value |
| host environment | host, harness, name, value | updatedAt, rowVersion | valuePresent | — | value |
| harness processes | id, sessionKey, host, harness, provider, model, state | pid, startedAt, endedAt, rowVersion | — | — | pid, endedAt |

### Core stored resources

| Resource | Strings | Integers | Booleans | Arrays / objects | Nullable |
|---|---|---|---|---|---|
| sessions | sessionKey, displayName, kind, ownerUserId, origin, spawnedBy, handle, archetype, identityName, identityRevision, harness, provider, model, thinkingLevel, modelContext, host, state, mechanicalStatus | orderIndex, clearedThroughSeq, createdAt, updatedAt, rowVersion | isBuiltIn, adopted | overrides `O<SessionOverrides>` | ownerUserId, spawnedBy, handle, identityName, identityRevision, provider, model, thinkingLevel, modelContext, host, clearedThroughSeq, overrides |
| transcript messages | id, sessionKey, role, content, sender, deviceId, clientMessageId, replyToMessageId, replyToClientMessageId, llmVisibleMessageId, assignmentId, jobRef, harness, provider, model, effort | seq, at, attentionTier, turnSeq, rowVersion | — | attachments `A<O<Attachment>>`, context `J` | sender, deviceId, clientMessageId, replyToMessageId, replyToClientMessageId, assignmentId, jobRef, harness, provider, model, effort, turnSeq, context |
| work items | id, title, specRefName, specRefSha256, ownerUserId, state, failReason, routingWakeId, slateWakeId, createdByUser, createdBySession | createdInTurnSeq, createdAt, rowVersion | isBug, createdContextKnown | — | specRefName, specRefSha256, ownerUserId, failReason, routingWakeId, slateWakeId, createdByUser, createdBySession, createdInTurnSeq |
| assignments | id, subject, holderKey, holderRole, openedByUser, openedBySession, state, outcome, closedByUser, closedBySession, closingAttestId, workItemId, reviewsAssignmentId, holderHarness, holderProvider, effectKind, derivedStatus | openedAt, closedAt, rowVersion | holderFallback | files `A<S>` | holderRole, openedByUser, openedBySession, outcome, closedAt, closedByUser, closedBySession, closingAttestId, workItemId, reviewsAssignmentId, holderHarness, holderProvider |
| attests | id, assignmentId, kind, verdictKind, note, bySession, byUser, producer, producerCommand, byHarness, byProvider | ts, rowVersion | — | commitRefs `A<O<CommitRef>>` | verdictKind, note, bySession, byUser, producer, producerCommand, byHarness, byProvider, commitRefs |
| wakes | wakeId, sessionKey, targetRole, origin, prompt, consumer, state, reresolve, reresolveSeed, conditionKind, conditionScope, firedBy, creatorSessionKey, workItemId, assignmentId, class, classElection, deliveryRule | dueAt, createdAt, firedAt, reresolveRung, conditionAfterId, canceledAt, targetGate, rowVersion | rumination, digest, summon | — | targetRole, prompt, firedAt, reresolve, reresolveSeed, reresolveRung, conditionKind, conditionScope, conditionAfterId, firedBy, creatorSessionKey, workItemId, assignmentId, canceledAt, class, classElection, deliveryRule |
| turns | sessionKey, messageId, wakeId, origin, prompt, roleRef, roleFallback, assignmentId, jobRef, model, thinkingLevel, modelContext, harness, owner, requestRef, error, status | seq, replyAttention, adapterGen, createdAt, startedAt, endedAt, publishedAt, rowVersion | — | — | messageId, wakeId, roleRef, roleFallback, assignmentId, jobRef, model, thinkingLevel, modelContext, harness, owner, adapterGen, requestRef, error, startedAt, endedAt, publishedAt |
| artifacts | artifactId, kind, title, description, createdBySession, workItemId, parentSession, originPath, contentSha256, recordedMessageId, recordedTurnEvidence, state, home | createdAt, updatedAt, rowVersion | — | — | description, parentSession, contentSha256, recordedMessageId, home |
| assets | assetId, ownerUserId, mimeType, filename | size, createdAt, rowVersion | — | — | none |
| read markers | userId, scopeKey, marker | updatedAt, rowVersion | — | — | none |
| roles | name, boundSessionKey, ownerUserId | createdAt, updatedAt, rowVersion | — | — | boundSessionKey, ownerUserId |
| users | userId | createdAt, rowVersion | isAdmin | — | none |
| devices | deviceId, userId, claimedName, status, platform, model | createdAt, rowVersion | — | — | claimedName, platform, model |
| facts | kind, scope, origin | id, ts, rowVersion | — | — | scope |
| critical state | sessionKey, reason | startedAt, expiresAt, hardDeadline, updatedAt, rowVersion | — | — | none |

### Decisions and composed resources

| Resource | Strings | Integers / numbers | Booleans | Arrays / objects | Nullable |
|---|---|---|---|---|---|
| decision requests | id, kind, raiserId, raiserSessionKey, ownerUserId, assignmentId, expecterSessionKey, expecterUserId, deadlineWakeId, statuteName, question, status, decision, rationale, ruledBy, withdrawnBy, withdrawnReason, askedOfRole, answer, answeredBy | lineageRung, effortGeneration, raisedAt, deadlineAt, ruledAt, consumedAt, withdrawnAt, answeredAt, rowVersion | — | options `A<O<DecisionOption>>`, context `J` | raiserId, raiserSessionKey, ownerUserId, assignmentId, expecterSessionKey, expecterUserId, deadlineWakeId, statuteName, decision, rationale, ruledBy, ruledAt, consumedAt, withdrawnBy, withdrawnReason, withdrawnAt, askedOfRole, answer, answeredBy, answeredAt, context |
| toplines | id, ownerUserId, title, state, dependencyVersion | createdAt, updatedAt, closedAt, activeWorkCount, openConcernCount | — | createdActor `O<Actor>`, workMemberships `A<O<ToplineMembership>>`, concerns `A<O<Concern>>` | closedAt |
| execution map node | id, title, specRefName, specRefSha256, state, failReason | finishedAt, jobs, startedAt, openDecisionRequests, fanOut, sinceProgressMs | bracket1Armed | origin `O<ExecutionMapOrigin>`, creationContext `O<ExecutionMapCreationContext>`, parent `O<ExecutionMapParent>`, assignments `O<ExecutionMapAssignmentCounts>`, attests `O<ExecutionMapAttestCounts>`, closingAttests `A<O<ExecutionMapClosingAttest>>`, turns `O<ExecutionMapTurns>`, minds `A<O<ExecutionMapMind>>`, active `O<ExecutionMapActive>` | specRefName, specRefSha256, failReason, finishedAt, startedAt, fanOut, minds |
| coordination share | sessionKey, dependencyVersion | from, to, turns, wakeTurns, classedTurns, coordinationTurns, summons, algedonic, share `N` | — | byClass `M<I>` | share |
| digest members | wakeId, prompt, class, classElection, dependencyVersion | createdAt | — | — | class, classElection |
| work-item trace | dependencyVersion | — | — | workItem `O<work items>`, assignments `A<O<assignments>>`, causalChildren `A<S>`, attribution `O<Attribution>` | none |

## Enum domains

- session kind: `main|dm|custom`; session state: `active|retired`.
- message role: `user|assistant`; attentionTier: `-1|0|1`.
- work-item state: `open|iceboxed|closed|failed`.
- assignment state: `open|closed`; outcome:
  `completed|surrendered|revoked|null`.
- attest kind: `progress|completion|surrender|verdict`. `verdictKind` is the
  registered review-verdict string and is null for non-verdict attests.
- wake state: `pending|fired|canceled`; reresolve: `lineage|null`; firedBy:
  `condition|fallback|null`; classElection: `sender|classifier|batcher|null`.
- turn status: `queued|running|delivered|canceled|failed|failed_unknown`.
- artifact kind: `spec|report|doc|data|other`; artifact state:
  `in-workspace|archived|released`; recordedTurnEvidence:
  `tool-call-observed|session-concurrent|none`.
- device status: `allowlisted|pending|denied`.
- decision kind: `statute|effort|agent`; decision status:
  `open|ruled|consumed|withdrawn|superseded|answered`.
- topline state: `open|closed`; actor kind: `user|session`.
- execution-map origin principal: `user|session`; parent status:
  `linked|from_turn|no_turn_observed|unrecorded`. `parent.item` is non-null only
  for `linked`. An execution-map node's `state` uses the work-item state enum.
- harness-process state: `launching|running|park_requested|closed_gracefully|
  killed|kill_failed|exited`.
- identity state: `ready|relearn_conflicted`; kungfu status:
  `available|installed`.
- rail on: `tool-call`; rail mode: `gate`.
- harness, provider, model, effort, and context strings must exist in the
  served harness catalog at serialization time. An absent catalog value is a
  schema error, not a new enum member.

## Canonical array and map order

- `org.archetypes`, `org.hosts`, skills, where, envNames, phrases,
  capabilities, efforts, conflicts, staleness, causalChildren, and all other
  set-like string arrays sort ascending by string.
- harness models and modelCatalog sort by `(provider, model)`.
- references sort by `(name, location, access-or-empty)`; modelPreferences by
  `(model, effort, context-or-empty)`; MCP servers by name; documents by path.
- transcript attachments preserve stored attachment ordinal. Assignment files,
  decision options, and opaque J arrays preserve author order.
- topline memberships sort by `(linkedAt, id)`; concerns by `(createdAt, id)`.
- ExecutionMap flat items, assignment-selected items, forest roots, siblings,
  and children sort by source `(createdAt,id)`. `closingAttests` sorts by
  `assignmentId`. `minds` sorts by `(model-or-empty,context-or-empty,
  effort-or-empty,harness-or-empty)`. `noItem` sorts ascending by assignment id.
- digest members sort by `(createdAt, wakeId)`. Trace assignments use the
  assignments collection order. Work trace causal children sort by id.
- `byClass`, `sessionRevisions`, and every M or J object sort keys ascending.
- The dependency vector sorts by `(resource, canonical primary-key bytes)`.
  Its digest input is canonical JSON of `[resource, primaryKey, rowVersion]`
  entries with no whitespace. ExecutionMap's non-resource entries have these
  exact types and values: `["causal events",I,I]` with both integers equal to
  one positive `causal_events.seq`; `["subagent markers",I,I]` with both
  integers equal to one positive `subagent_markers.id`; and
  `["causal events epoch","causal_events_epoch",I]` with the final integer
  equal to the stored positive epoch-millisecond value.

Any field without a declared type, nullable rule, enum value, nested key, or
order is a schema failure. A reviewed projection-field amendment must change
this file and the main R7/R7a row together. An envelope or dependency-entry
amendment must change this file and the corresponding main R4 or R9 clause
together.
