# Disposable ACP compatibility spike

No production changes, no credential reads, no model calls. Packages downloaded from the npm registry into /tmp on Osanwe. Research patch drafts only; not deployment-ready.

Sources:
- https://registry.npmjs.org/@agentclientprotocol/codex-acp/1.10.0
- https://registry.npmjs.org/@agentclientprotocol/claude-agent-acp/0.74.0
- Tightbeam reference: gibson:/home/mike/src/tb018-build/lib/tightbeam/harness/{codex,claude,adapter_patch}.ex. Reference source/live release commit mismatch remains unresolved.

## Actual tests

`python spike.py`: patch current upstream bundles, require exact expected anchor occurrence counts, assert idempotency, node --check both outputs. PASS.
`node carrier-tests.mjs`: eight extracted patched-branch tests, collaborators stubbed. PASS. These prove local carrier assembly and preservation of callbacks; they do NOT prove current vendor event shapes or actual boundary operation.

manifest.json records source/patched SHA256s. codex-patches.json / claude-patches.json contain exact draft replacements.

## Minimal draft adaptation

Codex: keep developer instruction forwarding on new; forward on BOTH resumeSession and loadSession (same anchor occurs twice now); preserve upstream onAccountUpdated callback while adding the old Tightbeam metadata; move legacy child correlation map into CodexSubagentEventRouter and reference it from legacy thread status handling.

Claude: emit old Tightbeam child termination metadata before current upstream finishTask in task_notification and terminal task_updated; preserve upstream asyncTasks and pending task handling. This preserves explicit failed/killed status, whereas the historical notification patch always said completed.

Native subagent negotiation is an additional boundary. When enabled, upstream can intercept notifications before legacy handling. These patches target legacy carrier compatibility, not comprehensive new native-session support. They retain historical map lifetime behavior and need cleanup/race/dedup review before production.

## Untested

No latest-package initialize, paid turn, isolation, live instruction injection, hooks, resume, native subagent lifecycle, background termination, or fresh-org Tightbeam smoke. Root separately tested the old installed patched adapter with a newer Codex runtime. These are different combinations.

## Packaging conclusion

Newest packages require changes to compiled Tightbeam harness pins and patch code, or a newly implemented external compatibility bundle mechanism. Stock 0.1.8 config cannot replace those. A separately versioned maintenance artifact must declare exact base-release identity, compiled modules, locked complete adapter/runtime dependency tuple, platform hashes and rollback tuple. Do not impersonate pinned versions. Rollback restores original complete tuple and runtime overrides; active process lifecycle must be deliberately managed.
