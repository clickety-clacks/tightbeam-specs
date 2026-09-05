# Supported ACP paths: patch removal and the smallest refactor

Date: 2026-09-05. Assignment: `asg_a48b66c3-925f-4adf-9a90-1915539f092b`. Work item: `wi_c63c9442-aa6e-4337-86e1-5f881c3fa292`. Requester: Mike. Follow-on owner: PO Tightbeam, session `agent:main:clawline:mike:main s_fde9b2be`.

## Decision and verdict

**Not-proven:** Tightbeam cannot yet claim that it can remove all eight installed ACP replacements without losing required behavior. **Confidence: high** in the byte inventory and identified integration gaps; **moderate** in the proposed replacements, which have source evidence but no new model-backed acceptance run.

**Recommendation:** replace Codex instruction forwarding with supported synchronous instruction hooks, replace its account carrier with upstream `_auth/status_update`, and move child observations to upstream native child-session events **after preserving the existing spawn-handle correlation**. Keep Claude's existing upstream system-prompt injection. Separate executable selection from home/state projection and compiled patch pins. Retain the installed child patches until the correlation and terminal-state conditions below pass. Do not deploy the seed's newest-adapter patch drafts.

The main remaining upstream gap is concrete: native child events carry parent and child session IDs, but omit the originating tool-call ID. Tightbeam's current `wake --when-fact subagent_stop --when-scope <spawn tool-call ID>` contract needs that association. Both adapters already possess it internally. Recommend an additive, upstream-supported correlation field, including replay semantics, rather than a new coordination service or a new child accounting model. Codex also maps some unknown outcomes to `failed`; that must not become proof of child termination. [T3][U3][U4][U5]

**Immediate release finding:** the frozen 0.1.9 and main sources pin Claude ACP `0.73.0` but retain anchors that match neither the original nor patched form in that published bundle. Static comparison on eezo found zero matches for both replacements. The patcher therefore has no accepted branch for those bytes. This is a source/package incompatibility, not a claim that a production 0.1.9 launch was reproduced. PO should attach it to the existing upgrade review before treating that candidate as deployable. [P6][T2]

This is a recon recommendation, not authorization to change the identity or wake contracts. PO owns the follow-on implementation decision and any contract amendment. No product code, install, production runtime, credential, or service changed in this recon.

## Scope and proof method

The decidable question is: **Can the current supported interfaces replace each installed patch while preserving instruction authority, isolation, parent-attributed child observations, credential invalidation, and compatible independent upgrades?** This matches the assignment and [full brief](evidence/acp-supported-paths-2026-09-05/BRIEF.txt).

The native persistent goal was created and read back as `active`, thread `01a07278-cb1c-7fe0-bf7d-0c62723da794`. Its objective is the brief's full patch-removal and refactor objective. Activation receipt: `att_8d793af5-b939-41d2-8989-2547fb2e37ef`.

Competing explanations and results:

| Hypothesis | Discriminating evidence | Result |
|---|---|---|
| Every patch fills a vendor capability gap. | Codex supports developer context hooks; current adapters implement auth and native child extensions. | Rejected as a universal claim. Several gaps were in the old adapter translation. |
| Ordinary ACP tool completion already means child completion. | Legacy Codex spawn activity completes independently of child work; Claude retains background children after the Agent tool returns. | Rejected. Existing spec and current source distinguish these events. [T3][U3][U4] |
| Stop/SubagentStop alone can replace the child carriers. | Hooks can block and continue the child; neither stop schema supplies the spawn tool-call ID or a success verdict. | Rejected as a complete replacement. Useful hooks are not final settlement receipts. [E2][C1] |
| Native child sessions are already a drop-in replacement. | Emitted spawn/terminal payloads omit tool-call IDs; native negotiation suppresses legacy control calls. | Rejected for the existing wake API. [U3][U4] |
| A system executable requires giving up session isolation. | Executable selection is separate from `CODEX_HOME`, `CLAUDE_CONFIG_DIR`, and ACP `cwd`. | Rejected. Keep the existing shared credential/home architecture. [T4][U1][U4] |
| A shared CODEX_CONFIG can carry each archetype. | One adapter/client config is reused to create multiple sessions. | Rejected. It can carry generic hook configuration, not a different identity per concurrent session. [U2] |
| Codex hooks lack parent identity because they use sess.session_id(). | Followed construction through `session/session.rs:774–795`: child session_id is the root thread ID. | Rejected. Root identity exists; child turn and immediate nested-parent identity remain distinct. [E2] |

The last test disconfirmed my preliminary interpretation, recorded in `att_f37152d6`. Correction `att_1217b89d` supersedes it. This avoids anchoring on a misleading accessor name. The report does not infer semantics from names such as “completed,” nor treat matching source snippets as an end-to-end test.

**Observed in this recon:** installed package metadata, exact registry-to-installed diffs, source at frozen commits, and static disassembly of copied release BEAM modules on **eezo**. No Tightbeam application was booted. The initial compiler-info extraction failed because the release strips `CInf`; static disassembly then succeeded. This was an evidence-format limitation, not a failed application gate. [P1]

A second static check on eezo compared the exact Claude replacement string literals with the registry `0.73.0` bundle. Both before/after pairs had zero matches. The captured excerpt shows upstream native settlement calls inside those formerly contiguous anchors. This falsifies the assumption that a version-pin bump alone retains compatibility. [P6]

**Prior evidence, independently checked only where stated:** the [seed gateway report](evidence/acp-supported-paths-2026-09-05/astra-gateway-proof.md) records an Osanwe canary, hook denial, gateway restart/resume, and later authorized Gibson activation. Its gateway/runtime hashes match current installed bytes. I did not rerun its paid turns. The [seed patch report](evidence/acp-supported-paths-2026-09-05/REPORT.md) explicitly says its newest-bundle tests used stubs; they do not prove necessity or vendor behavior.

**Not tested here:** live unmodified-adapter turns, hook-based identity injection, all child outcomes, cold refresh, account-change behavior, or migration/rollback. Acceptance cases below identify the missing proof. No assertion of production readiness rests on the source review.

## Exact release and upstream inventory

The installed package is Tightbeam **0.1.8**, build **1337**, stamped **fdb3db5**, resolving in repository history to `fdb3db53b596d4114d06505b39a4c1836fba7564`. This is not the old `tb018-build` checkout at `becb13072624fce1129cfce377882bc2fb647cb8`. Their harness patch source is identical, but the installed stamp includes substantial later gateway, credential, and health work. A build stamp is provenance evidence, not a reproducible-build attestation for every module; the installed hashes and disassembly remain the byte authority. [P1][T1]

| Component | Observed version / identity | Qualification |
|---|---|---|
| Installed gateway | SHA-256 `57b37ce265ded8a313519f66977ac899245b2e1b50afed0a217e4a83997fe100` | Matches prior exact-release gateway proof. |
| Installed Codex ACP | `1.1.4`; bundle SHA-256 `518542bba96c2e719e10a3e6a440adebf417aeb88d387b2fd08116a8a26f2b30` | Six modifications, only `dist/index.js` differs from its registry package. [P2] |
| Installed Claude ACP | `0.66.0`; bundle SHA-256 `04610496ee0d7ee359e2cd4c3a30b7dffb2132d276585c56eba22c85b7f72036` | Two modifications in `dist/acp-agent.js`; other package files match, excluding installed dependency directory. [P3] |
| Installed adapter-side Codex dependency | `0.144.6` | Not the effective Gibson runtime while CODEX_PATH applies. |
| Effective Gibson Codex selection | External package `0.153.2`; runtime SHA-256 `f8786262ebc0fa1337448a2977332beadec66c8d0cda0ce973c7849766d7943c` | Host-env read confirms override; package metadata/hash read, no engine invocation. [P4] |
| Installed Claude SDK | `0.3.220` | Adapter `0.66.0` declares exact SDK version. No claim that a separately installed `claude` command is this SDK's engine. |
| Current Tightbeam 0.1.9 | `4f2b780df863a7a2966d08531855b9e24ac31a54` | Codex pin `1.1.4`, Claude pin `0.73.0`; same replacement bodies. |
| Current Tightbeam main | `dbe4ea59e9412afb08e213e8d6b850e72766571c` | Same pins/replacements as 0.1.9; harness diff changes identity prefix spelling only. [P5] |
| Current Codex ACP | `1.10.0`, `061f9a4a2e463a220d7a3ab2ae5e9732837085ef` | Declares SDK `^1.4.0`, Codex `^0.153.3`. Auth extension introduced in `1.9.0`; native child sessions in `1.7.0`. [U1] |
| Current Claude ACP | `0.75.1`, `3e23c5b960b66a6d2c892e7524c952e731c076a7` | SDK `0.3.257`, ACP SDK `1.4.0`, Node >=22. Native children in `0.71.0`; auth extension in `0.75.0`. This supersedes the seed's `0.74.0` survey. [U4] |
| Codex engine source inspected | `rust-v0.153.2`, `657a993cbee87acf52d14b758ce49dbd46d1b8eb` | Known source baseline for hooks/configuration; not a claim of the earliest release supporting every feature. |
| ACP reference / Zed | ACP `10983547ff6d26dfb33cb65164f3a4207f96c571`; Zed `5a9b9558db01a6b906cec2fb70a797affdc58cdd` | Read protocol and Zed acp_thread source. Zed also has its own subagent metadata; this is not universal core-ACP support. [A1] |

The old `zed-industries/codex-acp` repository is a separate Rust implementation. The installed npm package identifies `agentclientprotocol/codex-acp` as its repository. The inventory follows that package provenance, not the similar repository name. [U1]

Compiled `@adapter_version` values feed `Spinup.install_command`; readiness calls the patcher even when the executable already exists. Local patching asserts the exact package version; remote patching checks string anchors instead. Both bind launches to mutable bundle internals. Provisioning installs both harness packages into one shared npm directory, with a single-flight guard. These are Tightbeam couplings, not ACP requirements. The historical `priv/patches/codex-acp-1.1.4-served-identity.patch` is not another active runtime patch consumer; the harness modules and `Harness.AdapterPatch` own the active mechanism. [T2]

Static selectable-model guards, generated CLI projections, rails hooks, and `CODEX_CONFIG` are additional integration assumptions, not bundle edits. Upgrades must test them too. In particular, the current model catalog must not claim a model that `session/set_config_option` refuses, or silently replace the requested model. [T1][T2]

## Per-patch disposition

“Replace” below means the recommended implementation after its stated acceptance condition. It does not authorize deleting the installed patch today. Version floors are source-established feature introductions or named validation baselines, not certified compatible ranges.

| Patch | Observable purpose and loss on removal | Supported replacement | Disposition / proof still needed |
|---|---|---|---|
| C1: new-session `_meta.developerInstructions` forwarding | Sends the archetype into `thread/start.developerInstructions`. Removing it silently drops this identity string. | Synchronous Codex `SessionStart` context hook, with a fixed generic handler that reads the session's prepared identity snapshot; emit JSON additionalContext, `additionalContextLimit: 0` with a bounded identity size. `UserPromptSubmit` can deliver later revisions. Engine source baseline `0.153.2`; stock ACP already forwards generic config. [E1][U2] | **Replace**, after full-string precedence, two-session isolation, hook failure, compaction and child inheritance tests. No new instruction patch is justified before testing this supported route. |
| C2: load/resume `_meta.developerInstructions` forwarding | Carries guidance into thread resume. Removing it drops requested guidance; retaining it does not prove resident refresh works. | Same supported context hooks; SessionStart covers startup/resume/compact, UserPromptSubmit covers later turns and revision changes. Keep the existing apply contract until its owner authorizes a delivery change. [E1][E3] | **Replace**, gated on actual cold resume and resident refresh. `thread/resume` on an already loaded thread ignores instruction/config overrides; do not present it as a setter. |
| C3: `account/updated` → `_meta.codex.accountUpdated` | Allows a known logged-out event to park the provider's sessions. Removal loses this immediate invalidation path. | Connection-scoped `_auth/status_update`, advertised as `agentCapabilities._meta.authStatus`; Codex ACP >=`1.9.0`, inspected at `1.10.0`. `kind:none` is known logged out; silence is unknown. [U6] | **Replace**. Route directly to the existing auth observer and classify only recognized provider evidence. Test initial none, logout, nonterminal updates, unknown kinds and transport loss. |
| C4: `subAgentActivityCallIds` map | Retains child-thread → activity-tool-call association used by C5. | Native child-session correlation, plus an upstream supported originating-tool-call association. [U3] | **Keep temporarily; replace with C5/C6 as one unit.** Native events currently omit that association. |
| C5: child `thread/status/changed` → custom termination update | Emits correlated stop for idle/systemError/notLoaded. Without it, natural settlement need not produce the custom marker. | Negotiated `subagent_state_update`, with proof of settlement distinct from disconnected/timeout outcomes. [U3] | **Keep temporarily.** Current native Codex timeout/shutdown/notFound fallbacks can say failed without proving termination. Preserve wake fallback for uncertain outcomes. |
| C6: insert child/activity association at subAgentActivity start | Populates C4 so C5 can name a parent-visible handle. | Upstream native spawn event carrying originating handle plus child session ID. [U3] | **Keep temporarily**, then delete with C4/C5. Do not infer the mapping from title, task text, timestamps or transcript scraping. |
| L1: Claude `task_notification` carrier | Emits stop before deleting background-task bookkeeping. Historical patch labels every notification completed, regardless of actual result. | Native `subagent_state_update`, emitted by upstream `NativeSubagentRuntime.finishTask`; introduced >=`0.71.0`, inspected at `0.75.1`. [U4] | **Keep temporarily; replace with L2** once supported spawn-handle correlation exists and real foreground/background captures pass. Preserve actual completed/failed/cancelled distinctions. |
| L2: Claude terminal `task_updated` carrier | Handles completed/failed/killed settlement when task_notification is absent. | Upstream native finishTask at the same task_updated edge, including deduplication. [U4] | **Keep temporarily; replace with L1.** Test missing notification, terminal-before-correlation, cancel and replay. |

Claude `_meta.systemPrompt` is **already upstream behavior**, not a Tightbeam patch. Keep `{type:"preset", preset:"claude_code", append: guidance}`. It enters SDK query options during session creation. Do not replace it with CLAUDE.md or a user message, which changes the authority and instruction-loading contract. Cold SDK query recreation and changes to an existing query are different operations. [T1][U4]

## Identity, homes, hooks and refresh

The required separation is one shared home per `{harness,machine}` for credentials and generic configuration, plus each session's real working directory and instruction identity. Do not move cwd to an artificial identity directory. Do not write archetype instructions into the shared home config. Do not multiply Codex runtimes merely to obtain different environment variables. System-installed executables remain compatible with this separation. [T4]

For Codex, a **generic synchronous handler** can select a prepared, non-secret per-session snapshot using the hook's session/cwd context. Identity composition remains Tightbeam's existing responsibility. The handler outputs the full rendered identity through `hookSpecificOutput.additionalContext`; tagged source gives that content the `developer` role. Set the documented per-handler output threshold to avoid truncating a long identity; the handler itself enforces a finite size. Preserve other hook entries and trust settings. [E1]

Place the handler outside `Rails`' statute logic: `Rails` explicitly contributes zero guidance bytes. A small `Harness.Codex` instruction-delivery function and the existing identity materialization boundary can prepare the snapshot and merge its hook declaration with the generic rails declaration. The filename is an implementation choice; a reserved Tightbeam-owned file under the session workdir avoids product AGENTS.md/config ownership. Preserve the existing owned-file exclusion mechanism. [T4]

Startup hooks must run before the first model request. A resident refresh can use a later UserPromptSubmit delivery, but that is **new context**, not retroactive erasure of earlier instructions. A successful ACP load response does not attest replacement. Tagged `thread_processor.rs` explicitly ignores overrides on resident resume; cold resume builds new config from requested overrides. That source finding does not reproduce or explain the seed's reported cold-refresh failure conclusively. Its exact request trace and a replacement-sentinel run are missing. **Regression provenance remains unproven.** [E3]

Do not add a strict identity acknowledgement system in this lane. Preserve the current owner-ruled apply semantics; test best-effort reread behavior separately from first-turn authority. The older home-projection document explains the architecture but has draft/stale credential passages. Its old Claude setup-token description is not authority to change today's credential handling. The live source, current directive and applicable owner ruling govern that implementation decision. [T4]

Keep PreToolUse enforcement and the existing wiring-check that makes a real forbidden tool call. Codex's launch config currently supplies `bypass_hook_trust`; upstream hook discovery still respects explicitly disabled handlers. A compiled handler, an advertised feature, or a successful initialize is not proof that denial works. Claude still receives its supported settings/SDK permission configuration. This refactor must not silently turn off either gate. [T1][E1]

## Child lifecycle: what each observation establishes

| Case | Established interface behavior | Tightbeam consequence |
|---|---|---|
| Parent and child identity | Codex `session_id` is the root session; `agent_id` is the child thread; `turn_id` is the active child turn. Claude schema provides session_id and agent_id, with no turn_id or spawn tool-use ID. Native child notifications use immediate parent session envelopes. [E2][C1][U3][U4] | Root attribution is supported. Keep explicit nested-parent and originating-turn associations; do not attach a late background stop to whichever assignment is running now. |
| Normal child return | Codex's SubagentStop runs when its model no longer needs follow-up. Upstream tests cover a hook continuing the same child and invoking it twice. [E2] | Record a stop attempt only if useful. Do not fire final stop/wake merely because this hook ran. |
| Foreground versus background | Claude receives actual task_started/task_updated/task_notification frames. Native runtime finishes children at settlement, independently of initial Agent return. Its async-task runtime explicitly excludes agent tasks. [U4][U5] | Use child lifecycle, not non-agent async-task events, to replace L1/L2. |
| Blocking hooks | Stop/SubagentStop can continue execution. `stop_hook_active` describes continuation history, not proof that all other hooks permit stopping. [E2][C1] | An observer hook cannot know final settlement merely by returning allow itself. No provisional stop may close an assignment or fire a definitive child-stop fact. |
| Cancellation | ACP acknowledges parent prompt cancellation with stopReason cancelled. Native child states can distinguish cancelled. Codex child targeted cancel/close capabilities are not advertised. [A2][U3] | Keep existing parent cancellation handling. Do not claim parent cancel proves every background worker died. |
| Failure | Claude task statuses distinguish failed/killed. Codex's native implementation also uses failed for certain missing/timeout outcomes. [U3][U4] | Child failure is not work success. When failure only means lost observation, retain unknown/disconnected semantics and the existing wake deadline. |
| Process death / missing hook | A killed process cannot reliably send a final hook. Tightbeam already observes ACP exit, closes pending calls and lets its coordinator recover. [T5] | Use that existing failure path. Do not synthesize child completion. The existing condition wake fallback handles a missing carrier. |
| Resume / replay | Both upstream adapters reconstruct child histories. Claude and Codex use disconnected for unproven replay outcomes; Codex reopens continued children with a generation suffix. [U3][U4] | Replay must be idempotent. A new generation cannot be swallowed by the old “one stop per child” key. Preserve legacy waiters until drained. |
| Completed work | None of a hook, ACP end_turn, tool completion, or child completed state establishes the assignment's deliverable. [T3][A2] | Assignment attests and reviews remain authoritative. No child assignments, obligations, prods or success inference. |

The current marker table deduplicates by `{kind,sourceEventRef}` and allows one stop per canonical child. It captures the running assignment when an event arrives, not necessarily the assignment that spawned a long-running child. The existing root mapping, source namespace and wake fallback are useful. A replacement should capture the originating assignment at spawn and carry it to settlement; if unavailable, report it as unknown instead of guessing. This is a scoped change to marker attribution, not a new scheduler. [T3]

## Concrete refactor to commission

1. **Isolate selection from projection.** In `lib/tightbeam/harness/{codex,claude}.ex`, `spinup.ex`, `placement.ex` and `adapter_coordinator.ex`, resolve an explicit per-host/per-harness executable selection before launch. Keep `prepare_launch` responsible for shared home, credential-kind environment and cwd-independent process configuration. Keep session creation responsible for cwd, identity and model options. Add a small typed selection record with adapter path, adapter package/version/hash, engine path/version/hash, required capability profile and prior selection. Use the existing configuration/persistence boundary; no executable patch plugins or replacement BEAM bundles.
2. **Replace C1/C2 and C3.** Prepare the per-session instruction snapshot through `identity.ex` and install the generic supported Codex hook declarations alongside existing hooks through the harness projection code. Remove developerInstructions metadata only after its acceptance run. In `acp/adapter.ex`, handle `_auth/status_update` at connection scope; `acp/conn.ex:219` already forwards arbitrary notifications. Extend `Harness.Codex.classify_auth_event` so both the direct observer and `Credentials.terminal_evidence?` recognize the same verified envelope. Reuse `Placement.auth_event_handler`, `HarnessHealth` and credential parking. Do not add token copying, external token refresh ownership or polling. Claude auth telemetry exists upstream now, but enabling new terminal-parking semantics for Claude is a separate behavior decision, not required to delete a patch. [T1][T5][U6]
3. **Close the child correlation gap upstream, then replace C4–C6/L1–L2.** Ask upstream to expose an originating tool-call association on native spawn, including which generation/control operation it represents and how it replays. Claude already retains `parentToolUseId`; Codex has the control item ID when it processes spawn. Preserve that field rather than deriving it. Also request that unobserved Codex terminal outcomes report disconnected, or expose a reason sufficient to distinguish them. These requests follow verified gaps, not speculative feature wishes. No PR was sent in this recon. [U3][U4]
4. **Consume the supported child events in the existing marker path.** Add native-envelope normalization at `Harness.*.classify_subagent_event` or a small shared classifier behind that callback. In `SubagentMarkers`, retain root principal, actual parent, originating handle, generation and spawn-time assignment association. Keep the existing atomic marker/fact/wake transaction and registration race check in `gateway.ex`. Normalize terminal facts only when they establish cessation; disconnected retains the existing deadline path. Handle unknown/new child payloads explicitly. Do not create resident Tightbeam sessions for these internal children. [T3]
5. **Delete patch machinery only at final cutover.** Delete production `@adapter_replacements`, patch-local/remote wrappers and `Harness.AdapterPatch` once no selected production profile needs them. Remove the obsolete priv patch file. Replace anchor/idempotency tests and fixture-only patch conformance vectors in `Harness.Support`/`Harness.Fixture` with meaningful capability, mapping and installed-byte tests. Remove old custom carrier classification only after legacy processes/waiters finish. Keep unrelated harness tests. [T2]

**Interim:** stock 0.1.8 cannot execute this selection design. It still enforces compiled patches. A first Tightbeam maintenance implementation is necessary; independent upgrades become routine only after that seam ships. Merely setting CODEX_PATH or installing a newer ACP package does not remove the compiled coupling.

**Alternative if upstream declines correlation:** PO can authorize a wake API that accepts a native child handle rather than the existing spawn tool-call handle. That requires reliable delivery of the new handle to the parent and a migration of outstanding waiters. It is a product contract change, not a transparent refactor, so it is not the recommendation by default. A direct Codex App Server/Claude SDK integration is another supported architecture, but replaces far more adapter functionality and is disproportionate to the remaining field gaps.

## Independent compatible upgrades

Use an explicit selected executable, or resolve a named system executable once and record the resolved path. Do not silently chase PATH changes on each launch. An operator may select an unmodified global package; a managed install can stage an immutable, version-specific directory. Preserve the complete npm lock and platform dependency identities, because both adapter and engine packages have transitive/runtime dependencies. Do not assume an npm adapter version uniquely identifies the engine bytes. [U1][U4]

At launch, record actual identities and negotiate ACP protocol version, load/close support, model/effort/fast options, native children and the auth extension. Treat provisional native-child/auth extensions as explicit profile requirements. They are upstream-supported extensions, **not settled universal core ACP**. Semantic compatibility needs a tested tuple in addition to feature flags; a handshake cannot prove hook or terminal behavior.

Compatible upgrades may update the selected tuple without rebuilding Tightbeam once those contracts remain unchanged and the acceptance smoke passes. Stage separately, test on eezo/racter, then change the selection at an authorized adapter lifecycle boundary. Leave existing processes on their recorded tuple until quiescent. Restore the prior selection on failure. Do not promise compatibility with arbitrary future versions, changed provisional fields, engine minimums, state formats or protocol-breaking releases.

No new update daemon, generic migration framework or coordination layer is needed. An explicit configuration selection, immutable package bytes, the existing process lifecycle and one compatibility smoke are sufficient. The strongest affordable enforcement is a typed/validated selection and missing-capability refusal, backed by captured boundary tests; prose alone is insufficient.

## Migration and rollback, including Gibson

1. Record the installed Tightbeam build/hash, both patched adapters, complete dependency locks, home paths, selected engine and non-secret overrides. Preserve existing auth stores and session histories in place. Do not copy credentials between hosts. [P1][P2][P3][P4]
2. Validate the proposed Tightbeam refactor against copied release behavior in a disposable org on eezo/racter. Use independently onboarded test credentials if a model-backed run is authorized; this recon neither reads nor supplies them. Take real protocol captures for the acceptance table below.
3. Drain legacy child waiters/processes before switching marker identities. Preserve their existing deadlines. If a waiter cannot drain, defer that host's cutover; do not backfill guessed native IDs. Keep additive storage changes backward-readable until rollback expires.
4. Install/select the reviewed maintenance refactor only through the owner's existing release procedure. At its authorized lifecycle transition, select the tested upstream tuple and verify actual processes, hook denial, identity and resume. Do not mutate shared npm packages under a resident process.
5. Roll back by selecting the recorded old Tightbeam/adapters/engine tuple and restoring changed Tightbeam-owned hook/snapshot configuration at another authorized boundary. Keep session histories intact. A newer engine may write history an older engine cannot read; prove that rollback case before activation, or limit the candidate to disposable sessions until proven. Restoring a path alone does not restore an already-running process.

Gibson currently has:

```text
host=gibson harness=codex
CODEX_PATH=/home/mike/.local/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex
selected package=0.153.2
runtime sha256=f8786262ebc0fa1337448a2977332beadec66c8d0cda0ce973c7849766d7943c
```

Retain this override during recon and inventory it during the 0.1.9 upgrade review (`wi_d0951fd4-0ea6-4f9f-ab6f-4467e4b222fa`). Codex ACP 1.10.0 declares `^0.153.3`, so **do not carry Gibson's 0.153.2 override into that candidate automatically**. Validate and select the candidate's compatible engine, or explicitly approve another tested engine. Removing the override on today's install returns selection to the installed bundled 0.144.6; that is not equivalent to restoring the verified Astra-capable tuple. A vendor package upgrade can also change the bytes at the override path. This is why rollback must name the engine hash as well as the path. [P4][U1]

## Required acceptance evidence

All model/gateway tests run on **eezo or racter**, using the repository's unmodified canonical gate wrapper and a disposable org. No tests run on Gibson. Build-only work there follows its separate worktree rule. Record the host, exact tuples, real captures and expected negative cases.

| Test | Required observable result |
|---|---|
| Fresh identities A/B in one shared runtime | Each receives its own full sentinel-bearing identity, never the other's; conflicting product guidance does not override archetype instructions; elected skills remain isolated. |
| Instruction hook failure/size/trust | Long middle-of-text sentinel survives; missing snapshot, disabled/untrusted hook, timeout and invalid output cannot silently pass the identity acceptance gate. Real PreToolUse denial still works. |
| Resume/refresh | Fresh, resident attach, cold restart/resume, compaction, fork and explicit apply are separate cases. Record old/new sentinels and exact hook sources. Do not infer replacement from load success. |
| Child correlation | Two concurrent children, nested children, repeated controls and background completion after a new parent turn retain correct root, parent, handle and originating assignment. Same tool IDs in different sessions/hosts never collide. |
| Settlement | Foreground/background return, blocked stop then continuation, failed/killed child, cancelled parent and missing notification do not create premature stop facts. Normal settlement produces exactly one marker/wake. |
| Death and replay | Kill disposable adapter/engine, restart/resume, replay duplicates, stop-before-wake registration and resumed child generations. Unknown outcome uses deadline/disconnected; no fabricated completion. |
| Auth | Initial absent report versus known none; explicit logout; login/token refresh; unknown auth kind; API key, managed account and configured provider. No false provider-wide park on transport/rate limit failure; no secrets in captures. |
| Selection and rollback | System executable with same isolated homes/cwds; candidate tuple switch and reversal; incompatible capability refused; old session replay after a candidate-created turn; no mutations to resident package directory. |
| Full boundary regression | Existing live feature smoke for both harnesses, model/effort/fast readback and hooks, plus canonical repository tests appropriate to the change. Stub fixtures alone do not meet this claim. |

If any essential real experiment lacks a separately authorized credential or a working remote host, name that missing proof and stop that gate. Do not substitute production or synthetic vendor responses. The current recon ends with the supported-path recommendation and identified proof gap; it does not label this matrix passed.

## Evidence index

Local paths below are committed with this report. Public source links freeze the inspected commits. Tightbeam source line citations use the frozen main commit unless another revision is named.

- [P1: installed provenance and hashes](evidence/acp-supported-paths-2026-09-05/installed-beam-sha256.txt), [build stamp disassembly](evidence/acp-supported-paths-2026-09-05/Elixir.Tightbeam.BuildStamp.beam.disasm.txt), [stripped compiler chunks](evidence/acp-supported-paths-2026-09-05/installed-beam-provenance.txt). Harness disassembly files in the same directory carry the actual replacement literals and classifiers.
- [P2: complete Codex package comparison](evidence/acp-supported-paths-2026-09-05/codex-package-diff.txt), [exact Codex edits](evidence/acp-supported-paths-2026-09-05/live-codex-vs-upstream.diff).
- [P3: complete Claude package comparison](evidence/acp-supported-paths-2026-09-05/claude-package-diff.txt), [exact Claude edits](evidence/acp-supported-paths-2026-09-05/live-claude-vs-upstream.diff).
- [P4: live hashes](evidence/acp-supported-paths-2026-09-05/live-sha256.txt); host-env observation and package metadata summarized above. [Prior gateway proof](evidence/acp-supported-paths-2026-09-05/astra-gateway-proof.md).
- [P5: 0.1.9/main harness diff](evidence/acp-supported-paths-2026-09-05/019-vs-main-harness.diff); the empty `old-checkout-vs-installed-stamp-harness.diff` verifies only harness-source equality, not whole-release equality.
- [P6: Claude 0.73.0 anchor counts](evidence/acp-supported-paths-2026-09-05/claude-073-anchor-comparison.json), [bundle excerpt](evidence/acp-supported-paths-2026-09-05/claude-073-settlement-excerpt.txt), [package and bundle hashes](evidence/acp-supported-paths-2026-09-05/claude-073-sha256.txt). Source is the frozen main `harness/claude.ex`; 0.1.9 has the same replacement bodies. `compare_patch_anchors.py` reads string literals as data; it does not execute Tightbeam or adapter code.

[P1]: evidence/acp-supported-paths-2026-09-05/installed-beam-sha256.txt
[P2]: evidence/acp-supported-paths-2026-09-05/live-codex-vs-upstream.diff
[P3]: evidence/acp-supported-paths-2026-09-05/live-claude-vs-upstream.diff
[P4]: evidence/acp-supported-paths-2026-09-05/live-sha256.txt
[P5]: evidence/acp-supported-paths-2026-09-05/019-vs-main-harness.diff
[P6]: evidence/acp-supported-paths-2026-09-05/claude-073-anchor-comparison.json
[T1]: https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/harness/codex.ex#L67-L94
[T2]: https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/spinup.ex#L51-L162
[T3]: https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/subagent_markers.ex#L21-L242
[T4]: https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/homes.ex#L1-L27
[T5]: https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/acp/adapter.ex#L1008-L1079
[U1]: https://github.com/agentclientprotocol/codex-acp/tree/061f9a4a2e463a220d7a3ab2ae5e9732837085ef
[U2]: https://github.com/agentclientprotocol/codex-acp/blob/061f9a4a2e463a220d7a3ab2ae5e9732837085ef/src/CodexAcpClient.ts#L530-L615
[U3]: https://github.com/agentclientprotocol/codex-acp/blob/061f9a4a2e463a220d7a3ab2ae5e9732837085ef/src/subagents/CodexSubagentEventRouter.ts#L110-L420
[U4]: https://github.com/agentclientprotocol/claude-agent-acp/blob/3e23c5b960b66a6d2c892e7524c952e731c076a7/src/acp-agent.ts
[U5]: https://github.com/agentclientprotocol/claude-agent-acp/blob/3e23c5b960b66a6d2c892e7524c952e731c076a7/src/async-tasks.ts#L86-L109
[U6]: https://github.com/agentclientprotocol/codex-acp/blob/061f9a4a2e463a220d7a3ab2ae5e9732837085ef/src/AuthStatusMeta.ts#L4-L93
[E1]: https://github.com/openai/codex/blob/657a993cbee87acf52d14b758ce49dbd46d1b8eb/codex-rs/core/src/context/hook_additional_context.rs#L15-L35
[E2]: https://github.com/openai/codex/blob/657a993cbee87acf52d14b758ce49dbd46d1b8eb/codex-rs/core/src/hook_runtime.rs#L375-L454
[E3]: https://github.com/openai/codex/blob/657a993cbee87acf52d14b758ce49dbd46d1b8eb/codex-rs/app-server/src/request_processors/thread_processor.rs#L196-L211
[C1]: https://code.claude.com/docs/en/hooks#subagentstop
[A1]: https://github.com/zed-industries/zed/blob/5a9b9558db01a6b906cec2fb70a797affdc58cdd/crates/acp_thread/src/acp_thread.rs#L275-L292
[A2]: https://agentclientprotocol.com/protocol/v1/prompt-turn#cancellation

Additional checkable primary references:

- [Codex hook configuration and output limits](https://learn.chatgpt.com/docs/hooks#large-hook-output), [developer_instructions setting](https://learn.chatgpt.com/docs/config-file/config-reference), [App Server account API](https://learn.chatgpt.com/docs/app-server).
- [Tagged output spilling and zero-limit behavior](https://github.com/openai/codex/blob/657a993cbee87acf52d14b758ce49dbd46d1b8eb/codex-rs/hooks/src/output_spill.rs#L11-L105), [root session identity](https://github.com/openai/codex/blob/657a993cbee87acf52d14b758ce49dbd46d1b8eb/codex-rs/core/src/session/session.rs#L774-L795), [stop continuation control](https://github.com/openai/codex/blob/657a993cbee87acf52d14b758ce49dbd46d1b8eb/codex-rs/core/src/session/turn.rs#L511-L560), [upstream child-hook tests, read but not run](https://github.com/openai/codex/blob/657a993cbee87acf52d14b758ce49dbd46d1b8eb/codex-rs/core/tests/suite/subagent_notifications.rs#L733-L881).
- [Native Codex child contract and known deviations](https://github.com/agentclientprotocol/codex-acp/blob/061f9a4a2e463a220d7a3ab2ae5e9732837085ef/docs/subagent-sessions.md), [Claude native emitted shapes](https://github.com/agentclientprotocol/claude-agent-acp/blob/3e23c5b960b66a6d2c892e7524c952e731c076a7/src/native-subagents.ts#L310-L355), [Claude native/async schemas](https://github.com/agentclientprotocol/claude-agent-acp/blob/3e23c5b960b66a6d2c892e7524c952e731c076a7/src/acp-subagents.ts#L25-L93).
- [Claude system prompt injection](https://github.com/agentclientprotocol/claude-agent-acp/blob/3e23c5b960b66a6d2c892e7524c952e731c076a7/src/acp-agent.ts#L7777-L7794), [system engine selection and SDK options](https://github.com/agentclientprotocol/claude-agent-acp/blob/3e23c5b960b66a6d2c892e7524c952e731c076a7/src/acp-agent.ts#L7920-L7970).
- [Tightbeam Claude classifier/injection](https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/harness/claude.ex#L253-L511), [patch implementation](https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/harness/adapter_patch.ex#L5-L78), [credential invalidation consumer](https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/placement.ex#L1449-L1492), [credential evidence classifier](https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/credentials.ex#L133-L146), [wake registration](https://github.com/clickety-clacks/tightbeam/blob/dbe4ea59e9412afb08e213e8d6b850e72766571c/lib/tightbeam/gateway.ex#L5301-L5332).

Read-only local requirement references: `subagent-markers-v1.md` (READY; parent observability and tool-handle contract) and `served-identity-home-projection-v1.md` (draft rationale; do not adopt stale credential claims). The recon recommends the smallest supported replacements; it does not rewrite either requirement.
