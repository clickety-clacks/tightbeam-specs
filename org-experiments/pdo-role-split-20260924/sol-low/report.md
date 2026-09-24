# Sol low PDO configuration, September 24, 2026

The user requested Sol low PDOs, then clarified that this must affect all new work items. This is a configuration rollout, not an eval pass.

Published PDO archetype defaults and model preference changed from GPT-5.6 Luna medium to GPT-5.6 Sol low through the supported identity CLI. Identity revision ea24101a18ad3dbf2ce76589f16f1904a1a7acfd changes only four configuration fields in archetypes/pdo.toml. No prose guidance changed.

Both active product delivery owners now use gpt-5.6-sol with low effort: Engram s_417a6fb8 and Tightbeam s_777369c7. Their current archetype remains orchestrator; this operation did not migrate their roles. The CLI preserved both engine conversations. Tightbeam's in-flight turn finished before tuning. The settings apply to subsequent turns, including new work items and follow-ups on existing work.

Verified committed session settings and the CLI's live PDO default and model-preference projection. No new model turn or completed eval is claimed.

The shared model-selection prose still contains the prior Luna-medium PDO choice in one capsule and two activity-table rows. Explicit permission to update those three references was requested under the user's guidance-authoring rule. Until updated, a future explicit model selection can conflict with the new default.

The prepared fresh eval uses a Sol-low PDO and Opus-5.5-high PO. It has not been dispatched. Running gateway build1342 still uses managed Claude2.1.274, which Opus rejected. Installed build1343 contains the client correction. A shared gateway restart was requested under the user's explicit gateway-power rule and has not been authorized in this thread.

For later .9 adoption, retain the configuration delta and rollout evidence separately from behavioral evidence. A model choice and catalog support do not establish successful consultation, staffing or delivery.
