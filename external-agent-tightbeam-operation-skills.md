# External-agent Tightbeam operation skills

## Goal

Ship one targetless Tightbeam repository change that gives an external agent one of two
transport-specific ways to operate an existing Tightbeam organization:

1. `priv/skills/tightbeam-cli/SKILL.md` for the current Tightbeam CLI line.
2. `priv/skills/tightbeam-rest-0-2-0/SKILL.md` for the Tightbeam 0.2.0 authenticated
   HTTP dispatch interface.
3. A repository `README.md` section that links both editions and tells the installer to
   copy exactly one edition into the external agent's project-local skill directory.

The deliverable lets an external agent recover assigned work from durable rows, perform
only that assignment, record its result, and ask the owner's Main session to perform
broader Tightbeam operations.

Mike's required content is a floor, not the document outline. The implementation writer
owns each skill's structure, voice, sequencing, examples, and additional coverage. The
independent review judges whether a fresh external agent can use the document as a
cohesive and complete operating guide, not whether the writer filled a prescribed
template.

Mechanism choice: ADD the two transport-exclusive skill files and one installation
pointer because deleting external operation defeats the ordered capability, while
accepting unaided external operation preserves the exact failure this work must close.

## Non-Goals

- Change a Tightbeam CLI verb, HTTP route, wire shape, authorization rule, identity rule,
  state transition, or response envelope.
- Teach device-token routes under `/api/*` in the REST edition.
- Teach onboarding, administration, identity editing, credential changes, target choice,
  integration, merge, release, or deployment.
- Teach how to install, learn, unlearn, author, or operate a kungfu bundle.
- Copy the served Tightbeam operating manual or CLI flag reference into either skill.
- Add a bundled script, reference file, asset, `agents/openai.yaml`, third skill edition,
  or automatic transport fallback.
- Elect either skill into a Tightbeam archetype or alter the baseline skill inventory.
- Select an integration branch or close
  `wi_f3c76b63-07df-4609-8d88-880a05b05f3c` when the spec completes.

## Terms

- **External agent:** an agent process that can reach a Tightbeam gateway and has a
  Tightbeam session credential for a session that holds exactly one role, but does not
  receive Tightbeam's served identity or operating manual.
- **Work item:** the durable thread for one feature or bug.
- **Assignment:** an obligation on that work held by a session.
- **Card:** a work item that is staffed and moving, in the kanban sense.
- **Session:** one running or retained agent identity with a Tightbeam session key and an
  owner.
- **Main:** the owner's general Tightbeam session. A user-targeted wake routes to that
  owner's Main under the existing Tightbeam target rule.
- **CLI edition:** the skill whose only Tightbeam transport is the `tightbeam` executable
  shipped by the same current-line build as the gateway.
- **REST edition:** the skill whose only Tightbeam transport is HTTPS or loopback HTTP to
  Tightbeam 0.2.0 `POST /agent/dispatch`.
- **Session credential:** the `token`, `url`, and `sessionKey` fields in the nearest
  `.tightbeam-session` found by walking from the assignment working directory toward the
  filesystem root.
- **Kungfu:** a shipped bundle of practiced organizational behavior: guidance, skills,
  rails, rules, and its bundle metadata. This definition does not authorize a kungfu
  operation.
- **Project-local skill directory:** `.codex/skills/<skill-name>/SKILL.md` for Codex or
  `.claude/skills/<skill-name>/SKILL.md` for Claude, relative to the external agent's
  project root.
- **Current line:** the Tightbeam source line that carries the CLI edition and updates the
  edition when its CLI contract changes. This spec verified that line at Tightbeam commit
  `8e269e89c04b6b8569813142a12742f3325b8503`.

## Assumptions

1. Tightbeam `origin/main` at
   `8e269e89c04b6b8569813142a12742f3325b8503` declares CLI version `0.2.0` in
   `cli/Cargo.toml`.
2. At that commit, `lib/tightbeam/wire/router.ex` exposes `POST /agent/dispatch`, accepts
   an org CLI token or session token as a Bearer credential, requires the
   `x-tightbeam-cli-version` compatibility header, and routes mutations through
   `Tightbeam.Dispatch`.
3. At that commit, `cli/src/dispatch.rs` discovers the nearest `.tightbeam-session`
   before environment or provisioned gateway credentials, converts `ws` to `http` and
   `wss` to `https`, sends JSON to `/agent/dispatch`, and adds the Bearer and version
   headers.
4. At that commit, `lib/tightbeam/wire/router.ex` returns one of three dispatch outcomes:
   a 200 `result`, a non-2xx `error`, or a 202 `decisionPending` envelope.
5. At that commit, `priv/skills/` is the repository's existing home for standalone
   shipped Tightbeam skills, and the release build carries application `priv` content.
6. At that commit, `priv/skills/tightbeam-harnesses/SKILL.md` records project-local native
   skill disclosure under `.codex/skills` and `.claude/skills`.
7. The external agent starts in an assignment worktree whose ancestor contains a valid
   `.tightbeam-session` for a session that holds exactly one role, or the CLI edition has
   another CLI-supported endpoint configuration for that same session. The owner or Main
   provisions this identity shape before assigning external operation.
8. The independent spec reviewer will review bytes committed after this draft. The
   builder will receive the reviewed canonical path and SHA-256 before implementation.
9. Mike's clarification in artifact `art_08ffeeef` requires the skill writer to supply
   important operating content that the original floor did not name and requires review
   to judge cohesion and completeness across the whole document.

## Invariants

### I1. One edition, one transport

The CLI skill invokes Tightbeam only through the `tightbeam` executable. The REST skill
invokes Tightbeam only through `POST /agent/dispatch`. Neither skill falls back to the
other transport.

### I2. Existing authority remains in force

The skills explain transport and the operating flow. They do not select work,
expand assignment scope, make an owner decision, or grant a principal more authority
than its session credential already carries. The substrate routes and verifies; the
external agent or Main decides. This preserves wisdom 6.

### I3. Credentials stay private

The skills direct the agent to keep session tokens out of prose, stdout, stderr,
transcripts, committed files, artifact descriptions, process arguments, and request
body JSON. The REST skill sends the token only as the `Authorization: Bearer` header to
the gateway URL read from the session credential. The skills do not direct an agent to
copy, rotate, replace, or onboard credentials.

### I4. Supported session attribution

An external agent operates with a session credential whose session holds exactly one
role. It omits `--as-user`, `asUser`, `asProcess`, and an invented role, so the CLI or
gateway derives the session principal and its one held role. If the gateway returns
`no_role` or `ambiguous_identity`, the agent stops. It uses the assignment's
non-Tightbeam contact channel to ask the owner or Main for a correctly provisioned
single-role session credential. It does not bind a role, change identity, pass
`asUser`, or guess a role.

### I5. Required language is a floor

Each skill contains the three definitions in Terms without changing their meaning. Each
skill contains this sentence byte for byte:

> you should probably get main to do what you need it to instead of trying to do it yourself since main knows how to operate tightbeam.

Each skill explains Tightbeam basics and defines kungfu once. Neither skill includes a
kungfu operation. These items do not limit the writer's responsibility for the rest of
the operating guide.

### I6. Mechanics have one source

The CLI skill points to `tightbeam --help` and does not reproduce the CLI flag reference.
The REST skill names request shapes verified in the source anchors in Architecture. The
writer may add source-verified mechanisms needed to close a scenario in A2. The builder
changes a named mechanism only after amending this spec against current source.

### I7. State changes use one seam

The REST skill sends state-changing operations through `/agent/dispatch`; it does not
write a database, identity tree, credential store, or filesystem projection directly.
The CLI skill relies on the CLI's same dispatch seam. The change introduces no new state.

### I8. Failures stay visible

The skills direct the agent to stop on a CLI nonzero exit, HTTP transport failure,
non-2xx `error` envelope, incompatible version, or malformed response. The REST skill
classifies a 202 `decisionPending` response as a halted operation with an open decision
request, not as success.

### I9. Validation does not touch a live organization

Deterministic checks read repository bytes. Forward tests use a disposable gateway and
disposable database seeded through real Tightbeam verbs. Test prompts and test cleanup do
not mutate a live organization, identity, configuration, credential, release, or target.

### I10. The repository teaches no new operating pattern

Operating-pattern result: **none**. These skills expose existing transport and record
mechanisms to an external agent. They do not amend the served operating manual.

### I11. The work remains targetless

Spec review, implementation, code review, and `DONE-AWAITING-TARGET` do not name an
integration branch. A later owner ruling selects any target.

## Architecture

### A1. Shipped files and frontmatter

The builder adds exactly these skill files:

```text
priv/skills/tightbeam-cli/SKILL.md
priv/skills/tightbeam-rest-0-2-0/SKILL.md
```

The CLI file starts with exactly two YAML frontmatter keys:

```yaml
---
name: tightbeam-cli
description: Operate an existing Tightbeam organization through its current-line CLI. Use when an external agent has the tightbeam executable and must read assigned work, record results, or contact Main without a served Tightbeam identity.
---
```

The REST file starts with exactly two YAML frontmatter keys:

```yaml
---
name: tightbeam-rest-0-2-0
description: Operate an existing Tightbeam 0.2.0 organization through its authenticated HTTP dispatch interface. Use when an external agent must read assigned work, record results, or contact Main without invoking the Tightbeam CLI.
---
```

Each directory contains only `SKILL.md`. Each body stays below the skill-creator ceiling
of 500 lines. Each body uses imperative, role-voice directives. The metadata carries the
trigger; the body does not add a “when to use” section. This is progressive disclosure at
the metadata-to-body boundary.

The structural enforcement rung is a test: separate directories, distinct trigger
descriptions, and transport-exclusion assertions make accidental cross-edition guidance
fail the repository gate. A compile-time type cannot govern Markdown installed into two
external harnesses.

### A2. Writer ownership and whole-document completeness

The implementation assignment carries Mike's clarification verbatim:

> i want to make sure the writer agent has leeway to write a cohesive doc, not just follow your instructions. i wasn't necessarily completionist in my list to you i expect the agent to be completionist.

The writer selects the headings, order, narrative flow, directive voice, amount of
explanation, and source-verified mechanisms needed for a cohesive guide. A list in this
spec is a required coverage floor, not a document outline.

Each skill orients the agent: Tightbeam coordinates agent sessions for a human owner and
keeps work, obligations, communication, and evidence in durable rows. Each skill includes
the I5 terms and sentence. Each skill grounds a returned identifier as a typed record
identifier and directs the agent to use identifiers from the prompt or Tightbeam results.

The writer closes each scenario below either with direct transport-specific instructions
or with an explicit instruction to ask Main. A review finding identifies the scenario and
the missing action; “the original list did not mention it” does not answer the finding.

1. Start in a supported single-role session worktree and establish which Tightbeam
   session, owner, assignment, and work item the agent is acting for. Read
   `workItem.ownerUserId` from the named work item's `work-item-get` result; do not infer
   the owner from a session listing.
2. Recover after context loss from the work item, assignment, attests, and named artifacts
   instead of relying on conversation memory.
3. Distinguish a work item, assignment, card, session, Main, wake, attest, artifact,
   decision request, condition fact, and kungfu at first operational use.
   Explain that one work item can carry several assignments while one assignment names
   one obligation held by one session.
4. Read the relevant durable state before acting and keep the action inside the assigned
   outcome and authority.
5. Record a material intermediate result, exact refusal, completion, surrender, or review
   verdict on the correct assignment.
6. Record evidence stored outside the assignment worktree as an artifact pointer with its
   content digest when custody requires one.
7. Contact another agent, the owner, or the owner's Main with the correct target meaning
   and enough identifiers for the receiver to recover context. Use the work item's
   returned `ownerUserId` for the user target that routes to Main.
8. Ask for a human or owner decision as a durable decision request instead of leaving the
   need in prose.
9. Choose the existing wait instrument for an in-org row, an external system, a human
   answer, or self-continuation; do not poll an in-org row or a human on a timer.
10. Leave a valid completion, surrender, material progress, or bounded continuation
    receipt before a turn ends while an assignment remains open.
11. Create or route newly discovered work only through Main unless the assignment grants
    that coordination authority.
12. Delegate spawning, retirement, identity, configuration, credentials, kungfu operation,
    target choice, merge, release, deployment, and live administration to Main unless the
    assignment grants that exact authority.
13. Interpret success, named refusal, decision-pending, malformed response, version skew,
    authentication failure, and gateway unavailability without claiming an effect that the
    durable rows do not show.
14. Preserve credential privacy, session attribution, external-file custody, unrelated
    repository changes, and the prohibition on direct store mutation.
15. Discover transport mechanics from the authoritative surface instead of guessing a
    command, flag, verb, parameter, route, record shape, model name, role, session, or
    identifier.

The writer may cover more scenarios when source inspection shows that a fresh external
agent needs them. The body does not paste the internal operating manual or CLI flag
catalog. It refracts the existing law into a standalone external-agent guide and points to
the authoritative mechanism surface for depth. Common law carried in both editions uses
the same wording so the transport split does not create two meanings.

### A3. CLI-edition contract

The CLI body states that `tightbeam` is an ordinary executable, JSON arrives on stdout,
and a nonzero exit carries the failure on stderr. It directs the agent to run
`tightbeam --help` before its first Tightbeam operation after installing the skill and
whenever it needs command syntax.

The body includes these source-verified current-line command surfaces as a floor:

- `tightbeam --help`
- `tightbeam list`
- `tightbeam assignments`
- `tightbeam work-item-get`
- `tightbeam work-item-trace`
- `tightbeam attests`
- `tightbeam attest`
- `tightbeam artifacts`
- `tightbeam artifact-record`
- `tightbeam wake`

The skill gives a cohesive operating flow, not a flag catalog. Its floor includes:

1. Use the assignment and work-item identifiers from the wake. If either identifier is
   absent, inspect visible open assignments and stop for Main when the intended card is
   ambiguous.
2. Read the work item and assignment attests.
3. Perform the assigned external work.
4. File the new material result, refusal, completion, or surrender through `attest`.
5. Record a file outside the worktree through `artifact-record` when the assignment needs
   that evidence.
6. Read `workItem.ownerUserId` from the `work-item-get` result, then use that exact value
   in a user-targeted `wake` when Main must act. Do not derive the owner from `list`;
   current-line `list` does not return `ownerUserId`.

The skill directs the agent to run the CLI from the assignment worktree so credential
discovery can use `.tightbeam-session`. It does not tell the agent to print or parse the
token.

Source anchors at Tightbeam commit `8e269e89`:

- CLI command forms and help: `cli/src/args.rs` and the compiled `tightbeam --help`.
- Request construction and endpoint discovery: `cli/src/dispatch.rs`.
- Server verb allowlist and response envelopes: `lib/tightbeam/wire/router.ex`.
- Work-item response, including `workItem.ownerUserId`: `lib/tightbeam/work_items.ex`.

### A4. REST-edition contract

The REST body begins with a compatibility check:

1. Read the nearest `.tightbeam-session` in memory without emitting its contents.
2. Convert a leading `ws://` URL to `http://` or `wss://` to `https://`; preserve an
   existing `http://` or `https://` URL.
3. Send `GET /version` without a credential.
4. Continue only when the response has `protocolVersion: 1` and `version: "0.2.0"`.

For each operation, the agent sends `POST /agent/dispatch` with these headers:

```text
Authorization: Bearer <session token>
Content-Type: application/json
x-tightbeam-cli-version: 0.2.0
```

The agent constructs the secret header in memory and configures its HTTP tool not to emit
request headers. The supported session holds exactly one role. The agent omits `as`,
`asUser`, and `asProcess`, so the gateway attributes the call to that session and its one
held role. A `no_role` or `ambiguous_identity` error is an unsupported credential shape:
the agent stops and asks the owner or Main through the assignment's non-Tightbeam contact
channel to provision a single-role session credential. It does not follow the refusal's
`asUser` suggestion, guess a role, or change identity.

The REST body gives the exact envelope and these minimum-flow request bodies:

```json
{"verb":"inspect","params":{}}
{"verb":"assignments","params":{"state":"open"}}
{"verb":"work-item-get","params":{"workItemId":"wi_example"}}
{"verb":"work-item-trace","params":{"workItemId":"wi_example"}}
{"verb":"attests","params":{"assignmentId":"asg_example"}}
{"verb":"artifacts","params":{"workItemId":"wi_example"}}
{"verb":"attest","params":{"assignmentId":"asg_example","kind":"progress","note":"material result"}}
{"verb":"artifact-record","params":{"kind":"report","title":"result evidence","originPath":"host:/absolute/path","workItemId":"wi_example","contentSha256":"0000000000000000000000000000000000000000000000000000000000000000"}}
{"verb":"wake","userId":"owner-id","params":{"prompt":"Main action requested with the assignment and work-item ids"}}
```

The skill marks `wi_example`, `asg_example`, `owner-id`, the note, path, title, and digest
as placeholders. It directs the agent to substitute values from its wake, source files,
or prior Tightbeam results. It obtains `owner-id` specifically from
`workItem.ownerUserId` in the named work item's `work-item-get` result. It does not invite
the agent to invent record identifiers.

The response contract is explicit:

- A 200 response with `result` is the operation result.
- A 202 response with `decisionPending` means the operation halted and the named decision
  request is open. Record or report that boundary; do not claim the requested effect.
- A non-2xx response with `error.code` is a named refusal or fault. Preserve the code and
  message in the assignment evidence.
- A response outside those shapes is malformed. Stop and report the raw envelope with
  the credential and authorization header removed.

The REST body tells the agent to ask Main when it needs a verb or parameter shape that the
skill does not list. The writer may add a request shape needed to close A2 after verifying
the route, allowlist, handler, identity rule, parameter names, and response in current
source. The skill does not direct the agent to discover or guess a private route.

Source anchors at Tightbeam commit `8e269e89`:

- HTTP routes, auth, allowlist, identity resolution, and three response outcomes:
  `lib/tightbeam/wire/router.ex`.
- Byte-exact bodies, header construction, endpoint discovery, and response parsing:
  `cli/src/dispatch.rs`.
- Handler registration for the named verbs: `lib/tightbeam/gateway.ex`.
- Work-item response, including `workItem.ownerUserId`: `lib/tightbeam/work_items.ex`.

### A5. README installation pointer

The builder adds `## External-agent operation skill` immediately before
`## Two ways to install` in `README.md`. The section:

1. Links `priv/skills/tightbeam-cli/SKILL.md` as the current-line CLI edition.
2. Links `priv/skills/tightbeam-rest-0-2-0/SKILL.md` as the REST 0.2.0 edition.
3. Tells the installer to choose one transport edition and copy that whole directory to
   `.codex/skills/<skill-name>/` or `.claude/skills/<skill-name>/` in the external
   agent's project.
4. Tells the installer to keep the directory name and `SKILL.md` filename unchanged.
5. Tells the installer to start a fresh agent session after the copy so skill metadata is
   rediscovered.
6. Does not imply that installing the skill installs Tightbeam, creates a session,
   supplies a credential, teaches kungfu operation, or changes a Tightbeam identity.

### A6. Deterministic repository validation

The builder adds `test/external_agent_skills_test.exs`. The test reads repository files
through `Application.app_dir/2` where it verifies packaged `priv` content and through the
repository root where it verifies `README.md`.

The test asserts:

1. Both exact `SKILL.md` paths exist in application `priv` content and are nonempty.
2. Each frontmatter block has only `name` and `description`; each name equals its directory
   name; each description includes its transport and triggering context.
3. Each skill contains the I5 sentence byte for byte and the literal term labels for work
   item, assignment, card, Tightbeam, Main, and kungfu. The deterministic test does not
   judge semantic clarity or equivalence; the cold whole-document review in A7 does.
4. The CLI skill contains `tightbeam --help` and the A3 command floor. It contains no
   `/agent/dispatch`, `Authorization: Bearer`, REST request body, or direct store mutation.
   Each additional named command appears in compiled current-line help.
5. The REST skill contains the A4 endpoint, headers, bodies, placeholders, response
   outcomes, and version check. It contains no shell invocation of the `tightbeam`
   executable.
6. Neither skill contains a kungfu operation command.
7. Each JSON body in the REST skill parses. Its `verb` belongs to the router's persisted
   `@agent_verbs` allowlist. A request using a real Router with a disposable database and
   session token reaches the named handler or its expected domain refusal; it does not
   return `invalid_message`, `auth_failed`, or `incompatible_cli`.
8. README contains both relative links, both project-local destination patterns, the
   choose-one instruction, and the fresh-session instruction.

The builder updates no existing baseline-skill list because these external skills are
shipped installation choices, not baseline identity elections.

Repository verification follows `AGENTS.md`: build
`cli/target/release/tightbeam`, run the baseline full gate in the owned worktree, make the
change, run the same full gate again, and record baseline and after counts. Run
`sh packaging/assemble.sh` after the change and inspect the tarball to prove both skill
files ship. A docs-only shortcut does not apply because the new ExUnit validation is part
of the deliverable.

### A7. Forward tests against reality

After deterministic validation passes, the builder starts one disposable Tightbeam 0.2.0
gateway with a disposable database. The builder creates two single-role sessions, one
work item, and two assignments through real product verbs, then captures the real CLI and
REST responses used by the two tests. The test evidence records the gateway build SHA,
request transport, redacted responses, final assignment attests, and exit status.

The owner opens each forward test in a fresh session that has only the named edition
installed:

1. **CLI-only test.** Give the agent the CLI assignment id, work-item id, and a task to
   read the card and file one progress result. Provide the real `tightbeam` executable and
   no direct HTTP tool. Pass when the agent consults `tightbeam --help`, reads the durable
   rows, files the progress attest through the CLI, and invokes no REST mechanism.
2. **REST-only test.** Give the agent the REST assignment id, work-item id, and the same
   task. Provide an HTTP tool configured to redact secret headers and do not put the
   `tightbeam` executable on PATH. Pass when the agent verifies `/version`, reads the
   durable rows, files the progress attest through `/agent/dispatch`, handles each response
   envelope correctly, and invokes no CLI mechanism.

The forward-test prompt does not describe the expected command or request sequence. The
reviewer judges the emitted transport log and final durable rows, not the agent's prose
claim. The reviewer also walks the A2 scenario map against the whole skill and records
each scenario as direct, delegated-to-Main, or missing. A forward-test failure or missing
scenario amends the canonical skill or spec before another run.

### A8. Delivery and custody

The implementation remains targetless. The coder pushes one exact proposal commit and
records its SHA. A different-session independent code reviewer reviews that exact commit.
After a reviewed-clean verdict, the owner reports `DONE-AWAITING-TARGET`; the owner does
not merge, release, deploy, or close the work item without a later target ruling and the
remaining canonical landing gates.

## Acceptance

### AC1 — Two installable editions

**Given** a clean checkout of the implementation proposal, **when** the repository test
loads application `priv`, **then** both A1 paths exist, each directory contains only its
`SKILL.md`, each frontmatter block passes A1, and no third external-operation edition
exists.

### AC2 — Required common content

**Given** either skill file and the A2 scenario map, **when** an independent reviewer reads
the skill cold as an external agent, **then** the file explains Tightbeam, defines work
item, assignment, card, Main, and kungfu, contains the I5 sentence byte for byte, contains
no kungfu operation, and closes each A2 scenario directly or by an explicit delegation to
Main.

### AC3 — CLI transport isolation

**Given** the CLI skill, **when** the content test scans its operation directives, **then**
the file points to `tightbeam --help`, contains the A3 command floor, finds every
additional named command in current compiled help, and contains none of the REST transport
markers forbidden by A6.

### AC4 — REST transport isolation and compatibility

**Given** the REST skill, a supported single-role session credential, and a disposable
0.2.0 gateway, **when** the test executes its A4 request shapes, **then** the agent verifies
protocol version 1 and release 0.2.0, sends the three required headers, receives a handler
result or expected domain refusal for each allowed verb, and does not invoke a Tightbeam
CLI executable.

### AC5 — Identity and credential boundary

**Given** an external agent with a session credential whose session holds exactly one
role, **when** it follows either skill, **then** the gateway attributes the calls to that
session and role, no request body carries a token or explicit principal, and the captured
logs contain no Bearer token or session-file contents. **Given** a zero-role or multi-role
session instead, **when** the gateway refuses identity resolution, **then** the agent stops
without using `asUser`, guessing a role, or changing identity.

### AC6 — Response classification

**Given** disposable Router fixtures for a 200 result, 202 `decisionPending`, non-2xx
`error`, and malformed success body, **when** the REST guidance is forward-tested, **then**
the agent claims success only for the 200 result, reports the other three boundaries with
their non-secret evidence, and does not replay the mutation.

### AC7 — README installation path

**Given** the repository README, **when** an installer follows the section before
`## Two ways to install`, **then** the installer can select one linked edition, copy its
whole directory into the matching Codex or Claude project-local skills root, preserve its
name, and learn that a fresh agent session is required.

### AC8 — Deterministic gate and package custody

**Given** the implementation proposal, **when** the builder runs the A6 baseline and after
gates plus `sh packaging/assemble.sh`, **then** both full gates pass with recorded counts
and the resulting package contains both exact skill paths and bytes.

### AC9 — Transport-exclusive forward use

**Given** the two disposable assignments in A7, **when** fresh agents receive only their
intended edition, **then** the CLI agent files its progress result using only CLI calls and
the REST agent files its progress result using only REST calls; the transport logs and
durable assignment rows prove both results.

### AC10 — Targetless reviewed handoff

**Given** green deterministic and forward evidence, **when** a different-session reviewer
returns a reviewed-clean verdict on the exact proposal commit, **then** the owner can report
`DONE-AWAITING-TARGET` without an integration branch, merge, release, deploy, identity
change, credential change, live-state mutation, or work-item closure.

## Open Questions

None. The product-owner spirit verdict `att_fb57f076-91de-4a23-bb8b-2b339117419c`, Mike
ruling artifact `art_d21fe502`, writer-ownership clarification artifact `art_08ffeeef`,
and source-verified work-item owner carrier and single-role identity precondition settle
the deliverable, nomenclature, transport split, content-floor rule, required sentence,
kungfu boundary, workflow stages, review standard, and targetless state. Deterministic
tests judge bytes and transport mechanics; the independent cold review judges cohesive
meaning.
