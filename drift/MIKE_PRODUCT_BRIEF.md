# Drift — Mike's product brief

## Instruction to Main

Mike authorizes establishing a new product, Drift, and wants a usable MVP as quickly as possible. Create/staff a dedicated Drift product owner, give that PO this complete brief, and have the PO own durable work, implementation, review, and delivery. Main should create the assignments so completion has a real parent. The PO should file operator decision requests (DRs) for questions not covered here, particularly unresolved product choices, while progressing independent authorized work. Do not stop at a strategy document. Confirm the PO and a held implementation successor, and report progress in product terms.

## Product intent and name

Drift is named for drifting in Pacific Rim: human and agent sharing a writing surface and understanding. Mike wants to word-process while his own general-purpose agent helps, using its existing context, files, tools, and harness. This must be an editable writing tool, not merely an annotated document viewer. He compared the desired interaction to Lavish, but with word processing. He rejected dependence on a proprietary hosted editor after investigating Lex and Revise. Build an independently runnable product without a required vendor cloud or bundled paid AI service. Exact license has not been decided.

## User requirements

- Lightweight writing application. A Quickshell/Qt Quick frontend was proposed by Mike as a possible MVP implementation, not an irrevocable toolkit choice.
- Actual document editing and saving, plus notes/comments anchored to specific passages.
- Human can select text and ask the agent about that selection and its context.
- Agent can point out/highlight passages to discuss them; human can do the same.
- Persistent annotation threads support asynchronous questions, answers, and follow-up discussion attached to text.
- Actions should be mostly symmetric: select, point out, comment, reply, edit, suggest, resolve. Do not arbitrarily make humans read-only reviewers or agents the sole editors. Each participant has its own selection/highlights and an author identity.
- Agent remains in a normal external harness (e.g. Codex) in a side window. User tells it where to connect; Drift does not need its own model runtime or chat harness.
- Event-driven participation is desirable, including notification of new questions. Be truthful about active waiting versus waking an idle harness.
- Fast MVP delivery, but treat Drift as a product, not a one-machine script.

## Topology — latest instruction supersedes earlier local-only example

Mike now prefers the server on Gibson for his deployment. ALL topology must be configurable: service address, bind address/port, storage paths, connection/auth configuration, deployment locations. No hard-coded Gibson, machine names, user names, home paths, or assumption that GUI, service, and agent share a machine. Support a same-machine deployment and a split GUI/server/agent topology through configuration. “Serverless” in the discussion meant no mandatory hosted SaaS dependency; Mike explicitly proposed a lightweight service and now wants Gibson as its initial host. Respect applicable Gibson release/install policy; do not silently turn a development build into an installed service. Resolve any necessary delivery choice through a DR.

## Architecture discussed — proposed starting point

Editor <-> authoritative document service <-> external agent adapter/CLI.

After Mike emphasized symmetric two-way actions, WebSockets were recommended for editor/adapter actions and events. Earlier SSE-plus-POST suggestion was superseded by that recommendation. A small HTTP/CLI surface remains useful so existing agents can use the product without managing a socket. MCP is an optional adapter, not a mandatory foundation or the agent runtime.

Separate transient presence (caret, current selection, temporary point-outs; replaceable updates) from durable state (document revisions, comments/replies, suggested edits; acknowledged, persisted, replayable). Server validates actions and broadcasts resulting events, including to sender. Preserve sequence/revision information for reconnection and stale-write detection.

Potential capabilities: read current/open document; read participant selection plus context; create/list/reply to threads; point out anchored passage; propose or apply revision-aware changes; wait for events since a cursor. Endpoint names mentioned were sketches, not contracts.

An external adapter may own the WebSocket and expose a blocking `drift wait`-style command: return a new question as tool output, let the active agent respond, then wait again. A transport connection alone does NOT wake an idle model/harness. Automatic idle-harness wake/injection needs verified harness support and should not be falsely promised or simulated by blind terminal keystrokes. Durable questions must survive agent disconnects.

## MVP proposals and correctness concerns

The assistant proposed starting with plain text or limited Markdown, local files plus annotation metadata, and proposed replacements with accept/reject. Mike has not selected a format or rich-text fidelity requirement: if that affects the intended word-processing experience, ask through a DR. Avoid assuming DOCX compatibility, pagination, cloud collaboration, or full office-suite features are required now.

Qt Quick TextEdit offers selection positions, programmatic selection, and position geometry. Multiple independent highlights, anchored notes, and rich editing behavior need a short feasibility spike. Do not let an agent point-out steal the human typing cursor. A standalone native Qt application could be evaluated if Quickshell is unsuitable; product experience matters more than forcing a toolkit.

Anchors must survive edits: raw character offsets alone are insufficient. Use revision-aware anchors/transforms and enough text context to detect ambiguity/deletion; don't silently attach a comment to unrelated text. Stale agent edits must not overwrite new human work. Undo, autosave/crash recovery, reconnect/replay, and clear authorship are material daily-use concerns. Remote access must have appropriate authentication/access controls; local-only trust assumptions cannot be baked in.

## Suggested acceptance demonstration

Human writes in Drift; selects a sentence; leaves an anchored asynchronous question. The external agent reads that exact passage plus context, replies in its thread, points out another passage, and suggests an edit. Human can perform the same pointing/comment actions and accept or decline the suggestion. Typing does not lose focus, anchors remain meaningful after nearby edits, and saved text/questions survive restarting. Demonstrate configured separate service/client locations as well as same-machine capability. No vendor account is necessary for Drift itself.

## Delivery guidance

The conversation's estimate (few days for prototype, weeks for reliable daily use) was a rough assistant estimate, NOT a deadline or commitment by Mike. Priority is the quickest useful end-to-end slice. PO should create bounded delivery work, gather concrete evidence, and raise DRs for uncovered questions instead of inventing product commitments. Routine engineering and staffing mechanics remain agent-owned. Report what Mike can actually do, limitations, and the next product choice; don't lead with coordination IDs.

Reference only: Revise's selection/anchored-comment MCP workflow helped establish the desired interaction (https://revise.io/help/mcp-server and https://revise.io/help/ai-reviewing-changes). This is not authorization to copy proprietary code or depend on its service.
