# Engram in our Tightbeam installation

Updated September 21, 2026. The operating guide is site/docs/engram-integration.html. The original September 19 research is preserved as site/docs/engram-integration-research-20260919.html and engram-integration-recon-2026-09-19.md.

Gibson has released Engram v0.2.5 and the existing engram-tightbeam launcher. The user service engram-gibson-coverage.service collects staged complete-record prefixes from Tightbeam Codex and Claude transcript roots. The user authorized expanding collection to external Codex/Claude sessions and installing local collectors on eezo, racter and osanwe.

The host rollout belongs to wi_9fa5482b-e2e5-4735-ac5c-bec75d1b4f85, held by the Engram PO. The org-local marker guidance belongs to wi_4f67a911-284d-40c0-8a0a-dc3baa8842ec, held by the Tightbeam PO. Host completion, historical backfill and cross-host availability must be recorded separately. No old-policy comparison restart is authorized.

## External agent guidance applied

All four hosts have an appended local Engram block in ~/.codex/AGENTS.md and ~/.claude/CLAUDE.md. Existing unrelated instructions are preserved. Backups are under ~/.local/state/engram-rollout-2026-09-21/backups on each host. The external-session edit does not automatically update Tightbeam's separately generated per-harness homes.

Generate a UUIDv4 per distinct dispatch; send the exact tag in tool-call arguments and recipient brief. Reuse only on a retry of the same handoff. A subsequent child delegation needs a fresh marker. Do not introduce a new outgoing marker as plain assistant text first, because Engram classifies the first surface occurrence as received. Keep the literal marker in the sending tool call even when using a brief file. Markers are provenance, not authority or additional notifications.

## Local and distributed coverage

Each host indexes actual transcript roots rather than archetype names. External roots are ~/.codex/sessions and ~/.claude/projects. Tightbeam roots are ~/.tightbeam/homes/<host>/codex/sessions and ~/.tightbeam/homes/<host>/claude/projects when present. Never scan authentication or configuration credential directories as transcripts.

Cross-host lineage requires both endpoints available to the query. Engram additional_stores supports read-only query fanout, but does not copy evidence between hosts. Prefer consistent local SQLite snapshots with associated immutable tapes and explicit freshness; do not query a changing database through rclone. Rollout results will record the actual boundary.

## Verification baseline

The prior Gibson full normalized-tape audit passed for 7586 tapes and 37288 code windows. Original-source queries covered 100 specimens across Codex/Claude reads/edits. All 102 discovered literal-query parser failures passed after v0.2.5 on snapshot and live installation. This is not whole-source adapter completeness and does not substitute for tests of the new hosts or actual nested handoffs.

Detailed external-guidance receipts are on Gibson in ~/.local/state/engram-rollout-2026-09-21/external-guidance-receipts.json. Host and identity rollout results will update this document and the HTML before the final report.

## Newly verified delegation defects

The real outgoing Codex custom_tool_call marker was not indexed as sent by v0.2.5 although its recipient marker was indexed. A separate controlled append test found correct parent lineage for full ingest and missing lineage for the identical bytes ingested in marker-then-code batches. Both have reproducible evidence under Gibson ~/.local/state/engram-rollout-2026-09-21, marker-repro/result.json and append-repro/result-v3.json. The append v1/v2 fixture attempts had an invalid tool-result envelope and are not product findings. Repair work wi_d1b74590-b41e-40e0-90b4-06e4dd3102ea is assigned to the Engram PO. Do not claim marker guidance alone delivers end-to-end lineage.

## Deployment checkpoint

Gibson external expansion, Racter and Osanwe collectors are active on v0.2.5, with per-root source-backed query samples and restart reconciliation receipts. Eezo staged 20063 files and its historical backfill is running. Racter/Osanwe service: engram-approved-transcripts.service; Eezo LaunchAgent: ai.engram.approved-transcripts-v025. Their installation root is ~/.local/share/engram/coverage-v0.2.5, with query launcher ~/.local/bin/engram-tightbeam. Gibson keeps its original engram-gibson-coverage.service and store. The org-local operating manual was published through served identity with only a 24-line marker section added; session refresh is in progress. Detailed receipts are under /home/mike/.tightbeam/work/239781a2ccce/deployment-2026-09-21 on Gibson.

## Cross-host query checkpoint

Gibson additional_stores now includes consistent native-disk snapshots from Racter and Osanwe captured September 21 at 9:32 AM PT. Remote-only explain and exact peek checks passed; snapshot hashes stayed unchanged and no SQLite sidecars appeared. Referenced tapes were copied and verified. Refresh is manual, not continuous synchronization. Eezo awaits backfill. Receipt: deployment-2026-09-21/cross-host-query-validation.json in the Engram PO workspace.

A third isolated defect is confirmed for native Claude assistant/user message envelopes: neither endpoint was extracted. The repair covers this alongside native Codex sender extraction and append continuity, including existing-store recovery. Evidence: ~/.local/state/engram-rollout-2026-09-21/claude-marker-repro/result.json.
