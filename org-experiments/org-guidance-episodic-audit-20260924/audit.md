# Episodic instructions in permanent org guidance

Audited September 24, 2026. This is an audit record, not agent guidance or authorization to change the findings.

The problem recurs beyond the removed no-turn paragraph. Three further passages store a particular job, incident or one-time action in instructions that later agents inherit. That establishes a placement/scope problem. It does not establish that every underlying instruction was unauthorized, that each restriction has expired, or that an agent deliberately circumvented the user.

## The requested rule is published

The user explicitly requested this addition. Published identity **69bdb2090a34abcfdb6679a566123ca7f0bec305** adds it near the start of the shared operating manual. The identical rule is installed in Gibson's `/home/mike/.codex/AGENTS.md` and `/home/mike/.claude/CLAUDE.md`.

> ## Explicit permission to add guidance
> 
> No agent may add persistent guidance anywhere unless the user explicitly asks
> for that guidance addition. If an agent wants to add guidance, it must explicitly
> ask the user for permission and wait for approval. Task instructions, corrections,
> incidents, agent requests and general maintenance authority do not supply that
> permission. This applies to shared and role guidance, skills, repository and
> harness instructions, and durable memory used as instructions. A skill that
> recommends adding guidance does not override this rule.
> 


The supported `tightbeam identity edit` command accepted the org change. Readback hashes match all three candidate files. Identity status reports the live revision with no conflicts. At the check, 74 of 75 listed existing sessions were stale. This publication does not establish that those sessions received the rule. No blanket refresh, model change, wake, service action or behavior eval was performed. External instruction propagation was limited to Gibson.

This is a guidance requirement, not a new mechanical enforcement rail. It explicitly takes precedence over a skill's recommendation to add guidance. The installed legacy authoring skill still describes an operating-manual amendment accompanying each applicable ratified capability spec; that procedure supplies no user permission under the new rule. Installed release files were not edited.

## Confirmed task state in standing instructions

| Passage | Who introduced it | Evidence and effect | Proposed disposition, not applied |
| --- | --- | --- | --- |
| Racter model-access remediation | Publication by `agent:product-owner:tightbeam`, September 22, commit `47fed048` | `guidance/engineering-model-activities.md`, Requested model selections: “The delivery owner still owes a demonstrated runnable GPT-6 Luna max route on Racter through the existing model-access producer.” It also freezes a host-catalog snapshot and an interim Sol fallback. The associated model-selection work and Hosted producer are recorded in messages and assignments. The broader model-guidance change was commissioned; the finding concerns its embedded unfinished job and transient availability. | Keep model-selection principles and any authorized defaults in guidance. Keep the outstanding producer obligation and current access findings on their work item. Do not cancel the obligation or assume access now works. |
| Firehose publication incident | External engineering-kungfu consolidation, September 12, commit `34afb8eb`; CLI attribution `user:mike` | Shared `operating-manual.md` embeds `dr_f62a4790` and commands preservation of existing public refs. The decision is a particular Firehose incident, not a universal operating procedure. The stored rationale explicitly identifies an intermediary's containment ruling, not a direct user decision. No later disposition was found in the targeted decision search. | Preserve the actual hold in its decision/work records. A general instruction to consult applicable current holds belongs in the manual; this incident's live state does not. Removing it from guidance would not release publication. |
| Resume lanes parked on desktop availability | `agent:owner:stall-fix-recovery`, September 15, commit `297e7d25`; retained in the September 24 role split, `1e700352` | `guidance/delivery-coordination.md`: “A lane parked waiting for desktop availability is unparked by this ruling. Resume it against osanwe.” The input relay, message seq 562895, asked for standing Osanwe host guidance and separately said “Apply it to any lane currently parked on desktop availability.” The one-time recovery instruction was included in permanent role guidance too. | Retain the explicitly requested standing desktop host choice. Keep the instruction to resume the then-parked lanes in those lanes' work records. Do not treat old prose as authority to resume unrelated future waits. |

The Osanwe passage was copied into delivery-coordination by this Engram agent during the role split. I preserved it without separating its standing rule from its one-time action. The original addition came from the stall-recovery agent; preserving it was my part in the failure.

## The already-corrected case

Commit `34afb8eb` also turned the September 11 external-agent engineering-kungfu task restriction into a conditional org-wide no-turn paragraph. The original conversation and later authorization were traced in the companion [scope correction](../pdo-role-split-20260924/no-turn-scope-correction/scope-correction.md). The paragraph was removed at **50ca792a** before this broader audit. The user's authority over gateway power remains. No successful post-correction eval is claimed.

Both the Firehose and no-turn additions arrived in the same broad manual rewrite. Git attribution as `user:mike` identifies the CLI principal, not human authorship. The earlier investigation identified the external consolidation agent as `gibson-codex-kungfu-20260911-215913`.

## Other candidates checked, with narrower conclusions

- **Pinned integration targets.** `skills/integration-targets/SKILL.md` embeds the `0.1.8` freeze at commit `2ff4ed2a` / release `v0.1.8+1334`, and routes active maintenance to `0.1.9`. The current pinned paragraph came from `f6e54f51`, August 25 PT, through `user:mike`; earlier edits are attributed to the Tightbeam PO and release-readiness reviewer. This is release-specific policy that can become stale. The original human authorization for this exact wording was not recovered. A newer installed build alone does not prove that a branch freeze was lifted. I have not labeled the freeze unauthorized or removed it.
- **Spec preservation workaround.** `guidance/specs-interim-durability.md`, introduced at `903ed563`, explicitly says it is temporary and gives a removal condition. Message seq 541487 relays a user instruction to copy at-risk specs until durability lands. The referenced work item `wi_609e19b9` is closed, and reviewed implementation evidence targets `0.1.9`. That does not establish deployment of durability on the live `0.1.8` runtime. This is a condition-bound workaround with recorded authority, not proof of another invented pause. Its removal condition still needs checking against the runtime where it applies.
- **Build 1337 runtime advice.** The manual's operator-ruling delivery and review-verdict sections name build 1337 and were introduced in `34afb8eb`. Those facts need version-specific verification before continued use. During this audit the local CLI symlink resolved to a 1343 package; that is not a test of gateway behavior. I did not declare the described limitations fixed merely from the package number.
- **No testing on Gibson.** `guidance/no-testing-on-gibson.md` originated at `97c58032` after the September 1 Tightbeam live-database incident. All 14 current archetypes include it. Its title and rationale refer to Tightbeam, but broad phrases such as “Nothing experimental runs there” lack that scope. Historical manual commit `2f61feb4` explicitly corrected the misuse of Tightbeam holds to block other products. This is a concrete scope-leak risk, particularly for the user-authorized Engram testing in this conversation. A permanent protection for Tightbeam's production state is not inherently episodic. The audit did not recover the raw human wording of the original testing rule, so it does not claim that whole rule was invented.

## Coverage and limits

Inventoried **77 tracked identity files**, including all **34 guidance fragments**, **14 archetype manifests**, **17 skill documents**, **three rule files**, the rail file, and bundle metadata. Read the shared manual, role/shared guidance, compositions and relevant small procedures; searched every skill body for local hosts, work/decision IDs, dated restrictions and policy-writing directives. The large imported Apple reference bodies were screened for org-specific additions, not subjected to a line-by-line technical review. This is an org-guidance scope audit, not a complete product or filesystem audit.

Read identity history and targeted read-only `state.db` records to trace the findings. Relayed messages are labeled as relays; neither an `as-user` principal nor a document heading proves direct human authorship. There may be further temporary instructions without obvious identifiers. All confirmed findings above have exact source passages and introducing commits.

The only new standing instruction added in this audit is the user's explicit-permission rule. Other findings remain unchanged for review. No guidance cleanup, release port, runtime refresh, or eval result is implied by this report. The patches and publication receipt accompany it so the approved rule can be carried into a later authorized source change.
