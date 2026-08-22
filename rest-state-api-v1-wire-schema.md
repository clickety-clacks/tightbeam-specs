# REST state API v1 — normative wire schema

Status: normative companion to `rest-state-api-v1.md` r3 review draft.

## Encoding rules

JSON is UTF-8. Integers are signed JSON integers and never floating-point
encodings. Timestamps are Unix epoch milliseconds. Identifiers and digests are
strings. `rowVersion` is a positive integer. `dependencyVersion` is a
lowercase 64-character SHA-256 hex string.

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
- digest members sort by `(createdAt, wakeId)`. Trace assignments use the
  assignments collection order. Work trace causal children sort by id.
- `byClass`, `sessionRevisions`, and every M or J object sort keys ascending.
- The dependency vector sorts by `(resource, canonical primary-key bytes)`.
  Its digest input is canonical JSON of `[resource, primaryKey, rowVersion]`
  entries with no whitespace.

Any field without a declared type, nullable rule, enum value, nested key, or
order is a schema failure. A reviewed amendment must change this file and the
main R7/R7a row together.
