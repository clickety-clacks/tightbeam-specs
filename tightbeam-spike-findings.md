# Tightbeam Overnight Spike Findings — 2026-07-16/17

Companion to `tightbeam.md`. Raw empirical results from the overnight spikes
Flynn requested. Sections land as agents report; synthesis + augmented question
list at the end.

## 1. Clawline Wire Inventory (agent: wire-inventory) — COMPLETE

**Headline: v1 wire surface is ~20 WS message types + 11 HTTP routes + ~25 DTOs.
The TypeScript wire types are the shipping contract; the two protocol docs are
STALE (attachment/upload model diverges). Build to the .ts types + tests.**

### WS surface (gateway perspective)
- RECEIVE (5 core): `pair_request`, `auth`, `message`, `stream_read`, `typing`
  (+ `interactive-callback` tolerated/ignored — not load-bearing for core chat).
- SEND (15): `pair_result`, `auth_result`, `message`, `ack`, `error`, `typing`,
  `session_info`, `stream_snapshot`, `stream_created`, `stream_updated`,
  `stream_deleted`, `stream_read_state`, `stream_tail_state`, `event`,
  `sync_complete`.
- Parsers are STRICT: unknown server payload type throws in the client;
  requiredString rejects empty; role must be user|assistant; timestamps must be
  numbers. Outbound JSON must match exactly.

### Key semantics the gateway must reproduce
- Client message ids `c_*`; server event ids `s_*`; duplicate `c_` id from same
  device = idempotent retry (same content) / `invalid_message` (different).
- content max 64KB (`payload_too_large`); protocolVersion literal 1; typing
  rate limit 2/sec/device; ack within 5s or client resends.
- Streaming partials reuse the same `s_` id with `streaming:true`; final
  replaces with `streaming:false`. Partials are NEVER replayed.
- Replay: `replayCursorsBySessionKey` (per-stream cursor → last processed s_ id)
  is authoritative; `lastMessageId` is single-stream legacy fallback only.
  Replay finalized messages per stream → drain queued gap-fill → `sync_complete`.
  `historyReset:true` = client drops local cache (global flag in v1).
- `session_replaced`: new auth for same deviceId terminates the old socket
  immediately (error code + close), no replay of unacked.
- `isAdmin` is computed at runtime per-connection (JWT does not carry it).
- Keepalive: server ping every 30s; client considers dead at 90s.
- Error codes (canonical v1): auth_failed, token_revoked, invalid_message,
  payload_too_large, not_found, rate_limited, session_replaced,
  upload_failed_retryable, server_error.

### Pairing/auth flow
GET /version → pair socket (`pair_request`, rate 5/min/device) → `pair_result`
{token JWT, userId} (first device ever = auto-admin) → close → new socket →
`auth` {token, deviceId, replayCursorsBySessionKey} → `auth_result` {userId,
isAdmin, replayCount, replayTruncated, historyReset, sessionKeys, sessions,
streamReadStates, streamTailStates} → replay → `sync_complete`.

### Session naming (what the chatdb supplied; registry now owns)
- sessionKey formats: personal `agent:main:clawline:{userId}:main`, DM (admin)
  `...:{userId}:dm`, custom `... s_<8hex>` suffix; `agent:main:main` is the
  global openclaw key (adoptable, not a Clawline-owned stream namespace).
- StreamSessionPayload: {sessionKey, displayName, kind, orderIndex, isBuiltIn,
  createdAt, updatedAt, adopted?}.
- Registry must own: per-user stream seeding (main/dm/global-for-admin), labels
  /order/isBuiltIn/adopted, per-stream read+tail state, per-user monotonic s_*
  sequence, replay cursor resolution, access filtering (non-admin sees own main
  only), subscription sync across a user's sockets, create/delete idempotency
  (idempotencyKey), trackable/adoptable external-session catalog.

### HTTP surface (11 routes, Bearer auth except /version)
/version; GET+POST /api/streams; POST /api/streams/adopt; PATCH+DELETE
/api/streams/{key}; GET /api/trackable-sessions; GET /api/session-status;
POST /api/session-control; POST /upload (multipart "file" →
{assetId,mimeType,size}); GET /download/{assetId} (raw bytes).
- SessionStatusPayload display fields: model, fallbackModels, provider,
  harness, authMode, reasoningLevel, thinkingLevel, fastMode, mode, verbosity;
  run {state,runId,messageId,startedAt,queueDepth}; capabilities per-item
  {supported, reason?, options[{title,value,enabled}]} for cancelCurrentRun /
  setModel / setThinking / setReasoning / setFastMode / setMode / setVerbosity
  + legacy boolean flags; modelCatalog {available, models[{ref required,...}]}.
- session-control actions → body keys: cancel_current_run; set_model{model};
  set_thinking{thinkingLevel}; set_reasoning{reasoningLevel};
  set_fast_mode{fastMode}; set_mode{mode}; set_verbosity{verbosity}.
- Attachments: inline base64 image OR assetId → gateway MUST serve
  /download/{assetId}. Upload auth-failure detection: 401 or code
  auth_failed/token_revoked.

### Open questions (drill-down against live provider source in progress)
- Q1 (HIGH): pair-approval/pair_decision types are in docs but NOT in the wire
  union — is multi-admin approval real, event-envelope-borne, or out-of-band?
- Q2 (HIGH): docs show replyToMessageId/clientMessageId on server messages; the
  typed parser drops them — what does the iOS client actually read for echo
  matching and missing-final detection? (Most important field-level unknown.)
- Q3 (HIGH): docs say type:"url"+/media/<id>; code says asset/assetId +
  /download. Confirm live provider emits asset model. (Docs stale.)
- Q4 (MED): session status — HTTP pull only, or any WS push?
- Q5 (MED): sessionKeys[] vs sessions[] — which does the client consume?
- Q6 (LOW): which `event` names are load-bearing? Q7 (LOW): llmVisibleMessageId
  namespace.

### Deferred (confirmed out of v1)
interactive-html attachment codec + interactive-callback handling; the entire
terminal-wire surface (separate /ws/terminal channel, terminal access tokens).

## 2. Research Sweep (agent: research-sweep) — COMPLETE

### 2a. Codex enforcement surface — RAILS COMPILE TARGET VALIDATED ON BOTH HARNESSES
**Codex now has hooks with near-parity to Claude Code.** Events include
PreToolUse / PostToolUse / PermissionRequest / UserPromptSubmit / Stop /
SubagentStop / SessionStart; PreToolUse returns `permissionDecision:"deny"` +
`permissionDecisionReason` (fed back to the model) or exit-2+stderr, and can
even REWRITE tool input (`updatedInput`). Per-tool regex matchers. Config in
`~/.codex/hooks.json` / config.toml / repo `.codex/` — all projectable into
generated homes. stdin JSON contract mirrors Claude's.
- **Managed hooks (requirements.toml) are auto-trusted and UNDISABLEABLE** —
  this is the constitutional tier, natively: ship constitution-tier rails as
  managed hooks, statutes as regular home-projected hooks.
- Bonus layer: execpolicy `.rules` (Starlark `prefix_rule`, allow/prompt/
  forbidden, most-restrictive-wins, static justification strings) — cheap
  first-pass compile target for static command allow/deny rails.
- approval_policy/sandbox_mode remain the global floor.
- Compile story: one rail model → both harnesses with mostly field renaming
  (deny+reason and per-tool matcher exist in both).
Sources: learn.chatgpt.com/docs/hooks, developers.openai.com/codex/exec-policy,
github.com/openai/codex execpolicy README, codex/config-reference.

### 2b. CEL in TypeScript — USE @marcbachmann/cel-js
v8.0.0 (2026-07-07), zero deps, active, Environment API with registerFunction/
registerVariable (exactly the exists()/count() extensibility rails need),
parse-once reusable predicates, static check(). Caveat: claims "most of spec,"
no official conformance-suite assertion. Fallback if strict conformance ever
required: @bufbuild/cel-es (beta, protobuf-heavy). Verdict: no bespoke DSL
needed — ecosystem is good enough.

### 2c. Restate — EVALUATE LATER, START WITH SQLITE
restate-server v1.7.2, single Rust binary, RocksDB embedded, macOS builds.
Virtual objects = per-key serialized execution (per-session FIFO out of the
box); awakeables = external-resolve durable promises (the wake primitive);
durable timers. BUT: separate process, handlers run as an HTTP endpoint the
server calls back into (service registration), multiple ports, and minor
upgrades have carried breaking config renames. Verdict: SQLite outbox + timer
loop first; keep the wake/queue API shaped like keyed-serialized-execution +
external-resolve-promise so Restate can slot in later unchanged.

### 2d. Happy relay architecture — STEAL 4, AVOID 3
Steal: (1) zero-knowledge dumb relay (server stores/forwards encrypted blobs,
never understands payloads); (2) challenge-response pubkey auth (no server
secrets; keys on device); (3) Expo push (APNs/FCM) as the "agent needs a
decision" wake channel; (4) remote-mode/any-key-reclaim phone↔terminal
handoff UX.
Avoid: (1) dual PTY-vs-SDK control paths (they're deprecating PTY — validates
Tightbeam's ACP-only choice); (2) trusting session ids across resume — Claude
--resume MINTS A NEW SESSION ID and Happy had to special-case history reunification
(EMPIRICAL CONFIRMATION of Tightbeam's pointer-chain registry design);
(3) claiming E2E while credentials leak outside it (their Discussion #680) —
if Tightbeam ever claims E2E, secrets must be in scope from day one.

**Design impacts (2a–2d):** three-plane law fully realized cross-harness;
constitutional tier maps to managed hooks; guard language decided; wake
durability decided (SQLite now, Restate-shaped API); resume-fork hazard
confirmed by independent implementation.

## 3. codex-acp Spike (agent: spike-codex-acp, on eezo) — COMPLETE, VERDICT: VIABLE

**Everything Tightbeam needs works, empirically. Auth-symlink design VALIDATED.**

- **Package:** `@agentclientprotocol/codex-acp@1.1.4` (the old
  @zed-industries/codex-acp is DEPRECATED — pin the new namespace). It's a Node
  wrapper over @openai/codex bindings — no cargo build. codex-cli 0.144.4 has
  no native ACP subcommand (has experimental app-server + mcp-server), so this
  adapter IS the bridge.
- **Capabilities (initialize):** loadSession=TRUE,
  promptCapabilities{embeddedContext,image}, sessionCapabilities{resume, list,
  close, delete, additionalDirectories}, auth methods api-key + chat-gpt.
- **session/new advertises everything the pickers need:**
  models.availableModels (34 = model × effort entries,
  current=gpt-5.6-sol[medium]); modes [read-only, agent, agent-full-access];
  configOptions[]: mode, collaboration_mode, model, reasoning_effort
  (low→ultra), fast-mode.
- **Selection works BOTH ways:** set_config_option{reasoning_effort:"high"} ✓;
  set_config_option{model} ✓; set_model{"gpt-5.6-sol[xhigh]"} ✓ (model+effort
  entangled in modelId suffix — either path usable); set_mode ✓. Adapter also
  exposes cancel/close/delete/fork/list/resume/goal_control.
- **Prompt round-trip:** stopReason=end_turn; update stream:
  available_commands_update, session_info_update, agent_message_chunk,
  usage_update (usage + quota metadata in result). Latency ~6.5s cold / ~3.4s
  warm (model latency, not adapter overhead).
- **session/load in a FRESH process: SUCCESS** — full history replayed as
  update notifications + title restored + options re-advertised.
- **Disk correlation exact:** ACP sessionId === Codex rollout UUID at
  ~/.codex/sessions/YYYY/MM/DD/rollout-...-<sessionId>.jsonl.
- **Auth isolation empirically validated:** fresh empty CODEX_HOME →
  "Authentication required" (-32000). Symlink ONLY auth.json in → session/new +
  prompt succeed. Codex populates the isolated home with its own fresh state
  DBs (goals/logs/memories/skills/state sqlite) — fresh independent state,
  shared credentials: exactly Tightbeam's home-projection model. Real ~/.codex
  untouched.
- **app-server assessment:** richer first-party control plane (typed TS
  bindings, stdio/unix/ws transports) but speaks Codex's own protocol, not ACP
  — would cost protocol uniformity. Stick with codex-acp; app-server is the
  documented fallback if the adapter ever stalls.
- Caveats: community/Zed-maintained wrapper layer (pin versions); model/effort
  entanglement in modelId (cosmetic).

Spike artifacts: ~/src/tightbeam-spike/codex-acp on eezo (probe scripts kept
for reuse in gateway tests).

## 4. claude-code-acp Spike (agent: spike-claude-acp, on eezo) — COMPLETE, VERDICT: VIABLE WITH CAVEATS

- **Package:** @zed-industries/claude-code-acp@0.16.2 is DEPRECATED/renamed →
  **pin @agentclientprotocol/claude-agent-acp** (same namespace migration as
  Codex's adapter). ACP SDK canonical name: @agentclientprotocol/sdk (adapter
  internally pins its own 0.14.x copy — dual-track SDK versioning, watch it).
  Wire framing: ndjson JSON-RPC (no Content-Length headers).
- **Capabilities:** loadSession=true, fork/list/resume, image+embeddedContext
  prompts, mcp http+sse. **NO configOptions surface** — models come inline on
  session/new (`models.availableModels`: default/sonnet/haiku/fable) and are
  set via **session/set_model** (set_config_option = Method not found).
  → ADAPTER DIVERGENCE: Codex speaks configOptions, Claude speaks set_model.
  The gateway needs a small per-adapter selection shim (both advertised, both
  work — just different methods).
- **Modes:** default, acceptEdits, plan, dontAsk, **bypassPermissions** (all
  accepted via set_mode) — YOLO mode confirmed available headlessly.
- **Prompt round-trip:** end_turn, ~1.1–1.6s, agent_message_chunk streaming;
  one ~16KB available_commands_update at session start.
- **⚠️ THE FABLE TRAP:** sessions inherit the HOST default model (Flynn's
  settings.json "model":"fable"), which the eezo account can't access →
  first prompt fails -32603. AND session/load resets currentModelId back to
  that default. **Gateway rule: ALWAYS session/set_model immediately after
  session/new AND after every session/load. Never trust currentModelId.**
- **session/load: WORKS** — fresh process replays full history; continuity
  empirically verified (model recalled a secret planted pre-restart).
- **Disk correlation exact:** ACP sessionId == transcript filename
  ~/.claude/projects/<cwd-slug>/<sessionId>.jsonl.
- **Auth isolation — SPEC ASSUMPTION CORRECTED:** Claude auth on eezo is a
  PLAIN FILE (~/.claude/.credentials.json), NOT macOS Keychain. Empty
  CLAUDE_CONFIG_DIR → adapter runs but prompt fails -32000. Injecting
  .credentials.json into the isolated dir → works. **So BOTH harnesses use
  file-based creds and the auth/<harness> symlink/copy design is uniform.**
- **Isolation gap:** host settings.json leaks the default model into isolated
  homes, and a settings.json INSIDE the isolated dir did NOT override it —
  model pinning must happen via ACP (set_model), not via projected files.
- **Gateway must answer server→client session/request_permission** (probe
  auto-approved; bypassPermissions should suppress these for tools).
- PATH note: claude lives at ~/.local/bin on eezo (login-shell PATH only).

Artifacts: ~/src/tightbeam-spike/claude-acp/ probe scripts (acp.mjs ndjson
client helper is directly reusable in the gateway).

## 5. Wire Drill-Down Q1–Q7 (agent: wire-inventory, round 2) — COMPLETE

**REFRAME (most important finding of the night): `src/protocol/chat-wire.ts`
is NOT the true contract.** The iOS app has its own richer decoders
(ProviderWireModels.swift, Message.swift) and the live provider
(~/src/clawdbot/extensions/clawline/src/runtime/server.ts — NOT ~/src/openclaw,
which doesn't exist) emits strictly more fields. **Build target = the
provider's real emitted shape + the iOS decoders**, with chat-wire.ts as a
lower bound only.

Verdicts (evidence = file:line in the agent's report, preserved in session
transcript):
- **Q2 — extra message fields: ALL REQUIRED.** User echoes MUST carry
  deviceId + clientMessageId (echo replacement keys on clientMessageId).
  Assistant messages MUST carry replyToMessageId (= user's s_* event id),
  replyToClientMessageId (= the c_ id), sender. Missing-final detection keys
  on replyToMessageId. Omitting breaks echo replacement + retry logic.
- **Q1 — NO pair-approval WS protocol exists.** The doc's
  pair_approval_request/pair_decision were never implemented. Reality:
  file-backed allowlist/pending store + operator notify + admin sees a plain
  chat message ("Device approval requested: ..."). pair_result reasons
  actually: success | pair_rejected | pair_denied | **pair_pending** (new).
  auth_result failure reasons: auth_failed, device_not_approved,
  **rate_limited** (new), token_revoked. First-admin = allowlist bootstrap
  (first entry), not a handshake.
- **Q3 — asset model CONFIRMED; docs' url//media model is dead.** Emit
  image (inline b64) / asset (assetId → /download) / document (inline
  mimeType+data). All 11 HTTP routes confirmed live in server.ts.
- **Q4 — session-status is HTTP-pull ONLY, BUT run lifecycle is pushed via
  `event:"prompt_turn_state"`** {messageId(=clientMessageId), sessionKey,
  state ∈ accepted|queued|running|delivered|canceled|failed, terminalState,
  correlationId, error?}. iOS depends on it for accepted/delivered/failed
  tracking — **LOAD-BEARING, required v1 addition** missing from round 1.
- **Q5 — use `sessionKeys: string[]`; `sessions: SessionDescriptor[]` is
  DEAD** (never emitted, never consumed). auth_result/session_info also carry
  features, dmScope, streamReadStates, streamTailStates. Stream labels flow
  via stream_snapshot sent right after auth_result.
- **Q6 — two live event names:** prompt_turn_state (required), activity
  ({isActive, messageId, sessionKey} agent-active signal — expected).
- **Q7 — llmVisibleMessageId = alias, not a namespace:** defaults
  clientMessageId ?? server id; reply references point at it.
- **Micro-check CLOSED:** iOS does NOT decode inline message.promptTurn*
  fields (no CodingKeys in either decoder) — gateway can OMIT them on all
  message/echo/replay payloads. Turn lifecycle reaches the client EXCLUSIVELY
  via event:"prompt_turn_state". Replay-gap implication: a turn that ends
  while the client is disconnected is recovered via the client's own
  missing-final detection (replyToMessageId, post-sync_complete) — reinforcing
  Q2's field requirements rather than adding new ones.

## 6. Synthesis — What the Night Proved

1. **The architecture survived every contact with reality.** Both adapters
   viable; auth-symlink isolation validated on both harnesses; session/load
   replay works; rails have a native compile target on both harnesses
   including an undisableable constitutional tier (Codex managed hooks).
2. **The contract correction is the night's biggest save:** building to
   chat-wire.ts would have shipped a gateway that silently broke echo
   replacement, retry, and turn tracking. The real contract (provider
   emissions + iOS decoders) is now fully enumerated — the v1 wire checklist
   is complete and field-level.
3. **Evidence-forced decisions:** always set_model after new/load (fable
   trap); model pinning via ACP not files; per-adapter model-selection shim;
   answer request_permission; SQLite-first wake store (Restate-shaped API);
   @marcbachmann/cel-js; pin the two renamed adapter packages.
4. **Scope got SMALLER in two places:** no pair-approval protocol to build
   (allowlist file + chat-message approvals), and no inline turn-state fields
   on messages (event-only).
5. **Reusable artifacts already exist:** probe scripts (incl. an ndjson ACP
   client helper) in ~/src/tightbeam-spike/{claude-acp,codex-acp} on eezo —
   directly seedable into the gateway's test suite.

**Net v1 checklist additions:** richer ServerMessage fields (Q2); the
prompt_turn_state + activity events; features/dmScope on auth_result +
session_info; pair_pending + rate_limited reasons; allowlist/pending file
store + approval-as-chat-message flow (no approval protocol).
