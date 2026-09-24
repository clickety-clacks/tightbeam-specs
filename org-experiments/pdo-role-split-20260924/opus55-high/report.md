# Opus 5.5 high PO rerun, September 24, 2026

The test reached PO consultation but could not evaluate the PO. Anthropic rejected the managed Claude client before any successful model turn. The PDO used the required consultation order and did not produce the deliverable. No topology, worker, or note was produced.

## Configuration and comparison

The user requested an Opus 5.5 high PO and another run. Fresh PDO `s_6aa74e54` used `gpt-5.6-luna` with max effort on Codex. Fresh PO `s_05ab5eab` requested exact `claude-opus-5-5` with high effort on Claude, on Gibson. Work item `wi_b8193d15` reused the supplied-facts <=180-word correction-note task. The prompt matches the previous Luna-max run after substituting the fresh PO identifiers and handoff marker.

Identity was `69bdb2090a34abcfdb6679a566123ca7f0bec305`. PDO provider context confirms Luna max and contains the PDO role, producer ban, consultation-before-staffing instruction, and explicit permission requirement for adding guidance. The misplaced no-turn paragraph is absent. PO model and effort are confirmed as the requested session settings; successful PO execution and receipt of its complete guidance are **not** claimed.

The PO model and harness changed, and published guidance changed since the previous run, including the no-turn removal. The exact guidance delta is retained. This is not a single-variable model comparison. No org guidance or production model configuration changed for this test.

## Observed behavior

- PDO consulted the named PO before attempting to staff a worker, without an external correction or topology-rail refusal.
- It correctly opened consultation `asg_c2afff9d` as `coordination`. The earlier mistaken code effect did not recur.
- It did not write the deliverable or create a worker.
- Its PO brief named the work item, outcome, constraints and requested topology, but did not reproduce the supplied facts and draft claims. Reading the originating PDO transcript would have been necessary to recover the full task. PO behavior on this handoff remains untested.
- After the actual provider refusal, PDO reported the runtime problem and filed a decision request. It did not invent an active no-turn restriction.
- Its proposed fallback option was poorly specified: it contemplated producer/reviewer staffing while retaining the unavailable PO, without explaining where the required PO decision would come from. No fallback was executed.

The first PDO turn took 191.5 seconds according to Tightbeam's start/end timestamps, including tool work and waiting. Twelve recorded tool-call batches occurred before the interview. Wrong skill-path and role queries, repeated command-help discovery, and an oversized assignment query were avoidable overhead.

## Runtime failure and remedy

The provider returned HTTP 400 with `claude_code_version_too_old`:

> Claude Code 2.1.274 does not support this model; version 2.1.280 or newer is required.

Five PO attempts failed: the PDO's initial wake, three automatic supervision prods, and one Main-authored recovery wake. The final wake used `user:mike` attribution but its creator was the Main session. It was not sent by this external driver or the PDO. All failed before useful PO execution; no harness pointer was created for this PO.

The standalone Gibson Claude executable reports 2.1.281. The managed adapter's installed SDK reports 0.3.274 / Claude Code 2.1.274. The live gateway process executable is from released build1342, while the installed gateway symlink points at build1343.

[Released source commit b2add644](https://github.com/clickety-clacks/tightbeam/commit/b2add64414b41606a713ed284abf01a0b4d125e6) changes the managed Claude ACP pin from 0.79.0 to 0.81.0 for its Opus-capable bundled client. Activating installed build1343 requires the shared gateway restart. That activation was not performed by this test. No adapter patch, runtime override, alias substitution or alternative PO model was used.

A restart handoff session already exists on Osanwe, named `tb018-claude-1343-restart`. Read-only inspection showed a Gibson shell prompt, not a pending sudo password prompt or a visibly staged restart command. Its existence does not prove activation. It was left unchanged.

## PDO interview

The same PDO answered before cleanup. It identified the always-loaded role instructions as the reason for consulting and delegating even this small document. It confirmed the coordination effect and acknowledged that the PO brief was not self-contained. It admitted that its fallback wording was inconsistent without either recovery of the PO or an explicit user override. It distinguished its own unnecessary discovery from the automatic PO retries and denied sending the Main-originated recovery wake. It found no current no-turn ban.

The interview took 103.4 seconds with no new tool calls. It is a different task and cannot be used as a controlled latency comparison. Its account is retrospective; actual tool and record evidence determines the observed scores. The PO could not be interviewed because the requested model could not start. No replacement model was used to manufacture an Opus answer.

## Cleanup and next test

The driver saved the records and interview, canceled pending fixture retries, withdrew the fixture fallback decision, revoked the two open fixture assignments, marked this item failed with an environment-blocked reason, and retired exactly the two temporary owners. Verified zero open fixture assignments, pending fixture wakes, or queued/running fixture turns. No product agent, listener, guidance, service, credential or release was changed.

The requested end-to-end eval remains unfulfilled. After build1343 is activated and the exact Opus route works, repeat the same fixture with fresh owners and score consultation, PO decision, worker staffing, actual delivery and avoidable overhead separately. Preserve this blocked run rather than counting it as a PO behavioral failure or successful delivery.
