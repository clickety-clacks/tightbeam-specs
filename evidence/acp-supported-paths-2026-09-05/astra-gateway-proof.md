# Gibson Astra activation: verified test and pending activation

2026-09-05. Disposable gateway on Osanwe, separate home/base/port12383, separately onboarded Codex account.

Exact installed Gibson Tightbeam0.1.8 package copied for the test. Gateway BEAM SHA256: 57b37ce265ded8a313519f66977ac899245b2e1b50afed0a217e4a83997fe100.

Installed patched Codex ACP1.1.4 + Gibson's installed Codex0.153.2. Runtime SHA256: f8786262ebc0fa1337448a2977332beadec66c8d0cda0ce973c7849766d7943c.

Tests passed through Tightbeam CLI and released gateway:
- Astra high canary agent s_4068123c delivered turn1: GATEWAY_ASTRA_OK.
- Tightbeam startup gate wiring-check PASS (hook rejected tightbeam-gate-probe).
- Stop and restart disposable gateway; same session delivered turn2: BLUE_CEDAR_738 GATEWAY_ASTRA_OK, preserving remembered context and injected identity.
- Gate wiring check passed again after restart.

Production change now saved:
Host gibson, harness codex, CODEX_PATH=/home/mike/.local/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex
Previously no Codex overlays. CLI reports effective at next adapter start. No production process restarted yet. Installed runtime path is managed by its vendor package; future vendor updates must recheck its version/hash.

Rollback: tightbeam host-env-unset --host gibson --harness codex CODEX_PATH --as-user mike; activate at an approved adapter/gateway lifecycle transition. It restores default bundled-runtime selection, not the already-running process.

0.1.9 upgrade: inventory persisted override; retain only if intentionally compatible, otherwise unset before lifecycle restart; verify effective runtime, Astra turn, hooks, resume. This requirement is routed in work item wi_d0951fd4-0ea6-4f9f-ab6f-4467e4b222fa.

Activation obstacle: no supported adapter-only drain/restart CLI in installed0.1.8; whole-org service restart affects active turns. Production is not idle. Need whole-org maintenance transition rather than unplanned ACP kill/private RPC.

## Production activated

Mike explicitly authorized restart. sudo systemctl restart tightbeam.service completed exit0; service active/running with new MainPID2053998. The selected system Codex runtime is0.153.2. Tightbeam hook wiring-check PASS after restart.

Production canary s_ca4c9875 delivered Astra high turn114382 with exact response ASTRA_PRODUCTION_OK (assistant message s_215bd40b-9669-4bf0-8137-2aa96900f728). Temporary canary retired after verification. No bulk retunes performed as part of activation.
