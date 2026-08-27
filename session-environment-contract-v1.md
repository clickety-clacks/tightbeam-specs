# Session environment contract v1

Work item: `wi_d9cf7b4b-6683-4e77-a88b-5c07340d2abc`

Status: proposed. This specification does not authorize implementation until an
independent reviewer records `reviewed-clean` for this exact revision.

This revision changes only the provisioning prerequisite in reviewed commit
`54c2515d0878782c0f9ea918574b29267d196e65`. Mike's direct assignment
`asg_89c1292b-4c2b-403f-852e-f1c76c1304fb` selects `provisioning_facts` and
resolves the branch posed by decision
`dr_b3875e5e-c02a-4338-897c-c66560e10b07`. The source contract for those facts
is `deterministic-acp-toolchain-launch.md` at commit
`09d4118dc6b651f0d1468a723a4d7a7afa8ca045`, file SHA-256
`ff7bbfc3ff4757fe00eb5ffff0870c42e7a7a4dec3d78d756de95c38b7a7ad26`.

## Goal

Give an agent one truthful, inspectable account of the environment that its
Tightbeam session actually receives. The account reports evidence. It never
infers a host capability and never decides whether the agent should proceed.

## Non-goals

- Do not install tools, alter a login profile, or repair a host.
- Do not create substrate defaults from prose or repository files.
- Do not pack harness, model, effort, or context into one model string.
- Do not expose credentials, environment values, probe arguments, or raw probe
  output.
- Do not add a readiness verdict or a substrate policy gate.
- Do not create an admin-authored toolchain registry, a toolchain setter, or a
  second provisioning-fact mutation seam.
- Do not change the provisioning manifest, launch-plan, or lifecycle contract
  owned by `deterministic-acp-toolchain-launch.md`.
- Do not teach an operating pattern before the projection ships.

## Terms

- **Authorized environment row**: an existing host-and-harness environment
  overlay admitted through Tightbeam's current configuration seam. Its public
  projection contains the variable name and row revision, not its value.
- **Provisioning facts**: the assimilation-produced host manifest and fact
  digest defined by `deterministic-acp-toolchain-launch.md` A-1. Assimilation's
  existing `register-host` dispatch is their sole mutation seam.
- **Provisioning revision**: the exact tuple of `provisioningFactDigest`,
  registered `cliBin`, and registered `adapterBinDir` read from one database
  snapshot. This tuple is evidence-key material, not a new stored row or digest.
- **Session incarnation**: one session row identified by its full, unique
  `sessionKey`. The full key is the incarnation identifier. This contract does
  not add a separate session-generation column.
- **Effective session environment**: the environment for one active session
  incarnation after applying its authorized environment rows and the
  provisioning-facts PATH rule below.
- **Declared requirement**: a tool name already declared by the selected
  harness registry entry. The session-only doctor form has no repository
  selector, so a repository, checkout, verification gate, working directory,
  or prose cannot declare a requirement.
- **Projection**: the fact-only `environment` object attached to an existing
  session row in the authenticated list/read and wire projections.
- **Probe**: the bounded `resolve_executable` check added to the existing
  `doctor` command for one declared requirement in one named session's
  effective environment. Listing a session never runs a probe.
- **Evidence key**: the tuple of full session key, exact session state,
  registered host, harness, sorted authorized environment-row name/revision
  pairs, and provisioning revision used for one observation.

## Assumptions

These assumptions are falsifiable implementation preconditions:

1. Current main can read separate harness, model, effort, and context values.
2. The implementation base can read each authorized environment row's public
   name and revision without exposing its value.
3. The implementation base can read and validate one host's provisioning facts
   and digest, plus `cliBin` and `adapterBinDir`, through the existing host and
   placement seams.
4. The full session key uniquely identifies one session incarnation. Current
   main can re-read that row's active state, registered host, and harness after
   a probe.
5. Current main's `doctor` command and authenticated session read can be
   extended with one bounded session-requirement probe without creating a
   second configuration or authorization mechanism.
6. Existing authenticated session list/read and wire projections already decide
   which principals may see a session.

If an assumption is false, the implementer stops and records the missing seam.
The implementer does not invent a second configuration, authorization, session
generation, or provisioning mechanism. Ruling
`dr_ed5dab0a-2fcf-41db-9032-a57aadfe6e05` authorizes only the narrow doctor
extension specified below.

## Invariants

1. A capability is present only when a bounded doctor probe observes it for the
   current evidence key. Environment rows and provisioning facts define the
   effective environment and evidence key; they do not prove a tool capability.
2. Guidance, repository text, login-shell state, installation elsewhere, and a
   prior session's observation are not capability evidence.
3. The substrate reports facts only. It emits no aggregate `ready` boolean and
   makes no proceed/refuse judgment from environment evidence.
4. Harness, model, effort, and context remain separate typed fields.
5. Secret values and raw probe material are neither persisted nor projected.
6. A changed evidence key makes earlier probe evidence inapplicable. The row
   remains historical evidence, but the current projection reports `unknown`
   until a new bounded probe runs.
7. No observation widens session visibility or authorization.
8. Assimilation remains the sole writer of provisioning facts. Session reads
   and doctor do not write or repair them.
9. The effective ACP child PATH contains no gateway-inherited PATH bytes and no
   remote-shell `$PATH` token.

## Provisioning-facts PATH ruling

The `provisioning_facts` decision replaces only the prior `inherited` and
`toolchain_rows` modes and their admin-authored configuration seam. It applies
the deterministic launch plan from `deterministic-acp-toolchain-launch.md` A-3:

- With a valid manifest for the selected harness, `path.mode` is
  `provisioning_facts`. `path.entries` is the ordered, de-duplicated list of the
  runtime executable directory, registered `cliBin`, selected harness CLI
  directory, `/usr/local/bin`, `/usr/bin`, and `/bin`.
- Local and remote effective environments use the same entries. Local launch
  does not append the gateway PATH. Remote launch does not append `$PATH`.
- With absent, invalid, unsupported, or selected-harness-missing facts,
  `path.mode` is `none`, `path.entries` is empty, and `path.failure` contains
  the matching closed provisioning-fact code.
- `tightbeam assimilate --dry-run` is the configuration preview. For each
  selected harness it displays the observed inputs and derived ordered PATH,
  labels the digest and authenticated principal as pending registration, and
  writes no row. A successful assimilation returns the registered digest and
  the same derived PATH. No other command previews or writes this PATH source.

This rule does not prove that an optional tool exists. The `engram` incident is
the acceptance example: prose naming `engram` cannot make it resolvable.

ADD wins only for this mapping and read seam: deleting the projection defeats
the stated goal, while accepting permanent `unknown` cannot provide the bounded
observation the goal requires.

## Architecture

### Projection actor and timing

The gateway reads the session row, authorized environment-row projections, and
the selected host's provisioning facts from one database snapshot. It validates
the provisioning digest and derives PATH by the exact rule above. It assembles
requirement status only from bounded doctor evidence for the current evidence
key. It attaches the `environment` object to the existing authenticated session
list/read response and corresponding wire row.

Session reads are non-mutating. They do not execute a command, refresh a probe,
inspect a login shell, or replace provisioning facts. The extended `doctor`
path is the sole active probe actor. A doctor run records only the closed result
described below.

### Narrow doctor probe

Extend the existing command with this one form:

```text
tightbeam doctor --session <session-key> --requirement <declared-tool> [--json]
```

`--session` and `--requirement` are required together. This form is mutually
exclusive with `--base-dir`. With neither option, existing doctor behavior is
unchanged. Any partial or conflicting form refuses before a probe.

The authenticated caller must already be allowed to read the named session.
The gateway requires that exact session row to be active. It resolves the row's
registered host and harness, the sorted authorized environment-row
name/revision pairs, and the provisioning revision through existing session,
placement, and host seams. It accepts the requirement only when the exact tool
name is declared by that harness registry entry. The command has no repository
input and must not derive one from the caller's checkout, working directory,
active assignment, work item, or prose. A tool name is one basename with no
slash, whitespace, shell operator, or control byte. Unknown or malformed names
refuse and create no evidence row.

If the path mode is `none`, the command refuses before host work and creates no
evidence row. It returns the exact `path.failure` code. The session projection
keeps each declared requirement at `status=unknown` and `source=none`.

For `path.mode=provisioning_facts`, the registered host runs one closed
`resolve_executable` operation with the exact effective PATH entries for that
evidence key. The operation locates a regular, executable file; it never
invokes the declared executable and never evaluates a shell command. The
resolved path and all host output are discarded. A completed match records
`available`; a completed miss or non-executable match records `unavailable`;
timeout, transport failure, or host refusal records `probe_failed` with the
corresponding closed failure value.

The gateway re-reads the complete evidence key, compares it with the probed key,
and conditionally persists the result in one database transaction. A session
retirement, registered-host change, harness change, environment-row revision
change, or provisioning-revision change during the probe discards the result
and returns `unknown`. Stale evidence is not attached to the new key. The
command returns the same closed requirement record that list/read may later
project. It emits no readiness verdict, wake direction, or action gate.

### Projection schema

The additive `environment` object has this closed shape:

```text
environment:
  observedAt: epoch milliseconds
  sessionKey: full enclosing session key
  host: registered host name
  harness: registered harness name
  model: model identifier
  effort: typed effort value or null
  context: typed context value or null
  path:
    mode: provisioning_facts | none
    entries: ordered path entries
    factDigest: lowercase SHA-256 or null
    failure: host_toolchain_facts_missing | host_toolchain_facts_invalid | host_toolchain_facts_unsupported | host_toolchain_harness_missing | null
  overlayNames: sorted environment variable names
  requirements:
    - name: declared tool name
      declaredBy: harness_registry
      status: available | unavailable | probe_failed | unknown
      observedAt: epoch milliseconds or null
      source: doctor_probe | none
      failure: not_found | not_executable | timed_out | refused | transport_failed | null
```

No other path mode, provisioning failure, requirement status, requirement
source, or probe failure value is valid. `path.mode=provisioning_facts` has a
non-null `factDigest`, a null `path.failure`, and the exact derived entries.
`path.mode=none` has a null `factDigest`, empty entries, and one provisioning
failure code.

`requirements` contains only declared requirements. `available`, `unavailable`,
and `probe_failed` have `source=doctor_probe`. `unknown` has `source=none` and
means there is no applicable doctor observation for the current evidence key.
Environment rows and provisioning facts alone leave the status `unknown`.
`unavailable` means the bounded check completed and proved absence or
non-executability. `probe_failed` means the check could not make that
observation; it does not mean unavailable.

`observedAt` is evidence time, not a freshness judgment. The substrate applies
no age threshold. Agents may weigh age. An evidence-key mismatch mechanically
changes the current status to `unknown`.

### Provisioning migration and compatibility

This contract adds no host-fact schema or migration. The schema, exact
predecessor migration, manifest validation, and reassimilation semantics remain
owned by `deterministic-acp-toolchain-launch.md` A-1, A-2, and A-5.

A legacy host row with no manifest remains readable. Its session projection
uses `path.mode=none` and `host_toolchain_facts_missing`. Invalid and unsupported
rows use their matching closed codes. No backfill reads a process environment,
login shell, filesystem, prior launch error, or prose. Reassimilation is the
only repair. Existing doctor behavior stays byte-for-byte compatible when the
session form is absent.

### Secret and visibility boundary

The projection may contain environment names, the fact digest, and the PATH
entries required by the ruling. It must not contain:

- any environment value;
- a credential, token, cookie, authorization header, or credential path;
- probe arguments, stdin, stdout, or stderr;
- provider response bodies or exception text;
- a resolved executable path from doctor; or
- an unbounded or raw provenance value.

Probe persistence is limited to the closed requirement record above plus the
evidence key. Failure classification happens at the probe boundary. Unknown
errors become `refused`; raw text is discarded before persistence and wire
projection.

The `environment` object inherits the exact authorization and row filtering of
the session row that contains it. It is not emitted on a broader org stream,
and adding it does not make an otherwise hidden session visible.

### Test environment boundary

Repository verification continues through the canonical gate. A scrub claim is
limited to the variable classes that the gate actually removes:
`TIGHTBEAM_*`, `RELEASE_*`, `ROOTDIR`, and `BINDIR`. Direct runtime reads and
fixture precedence remain explicit. No broader environment-isolation claim is
permitted.

## Guidance landing boundary

Before this capability ships, there is no operating pattern to teach. Guidance
must describe environment capability as conditional and must not name a command
or projection that users cannot run.

The implementation candidate that first ships the projection must amend the
single canonical operating home, `docs/ONBOARDING.md`, in the same reviewed
candidate. That amendment tells agents to inspect the existing session list/read
projection and to use `tightbeam doctor --session <session-key> --requirement
<declared-tool>` for a bounded refresh. It tells operators to re-run assimilation
when `path.mode=none`. It must use shipped field and command names only. No other
guidance home is amended.

## Acceptance

1. Given valid Gibson provisioning facts, when local and remote Codex sessions
   project their environment, then each reports `path.mode=provisioning_facts`,
   the registered fact digest, and the exact A-3 ordered PATH entries.
2. Given a missing, invalid, unsupported, or selected-harness-missing manifest,
   when a session is read and doctor is requested, then the projection reports
   `path.mode=none` with the matching closed code, doctor refuses before host
   work, no evidence row is created, and each requirement remains `unknown`.
3. Given `assimilate --dry-run` for selected harnesses, when preflight succeeds,
   then output shows each derived PATH, marks digest and principal pending, and
   writes no row. Given a successful registration, then output shows the
   registered digest and the same PATH.
4. Harness, model, effort, and context round-trip as separate fields.
5. Projection exposes overlay names but never their values.
6. A declared executable found by doctor records `available`; a completed miss
   records `unavailable`; timeout/transport/refusal records `probe_failed`; no
   applicable observation records `unknown`.
7. Listing a session performs no probe and causes no environment mutation.
8. Given only environment rows and provisioning facts, when no bounded doctor
   observation matches the evidence key, then the requirement reports
   `status=unknown` and `source=none`.
9. Given prior doctor evidence, when session state, registered host, harness,
   an environment-row revision, or the provisioning revision differs, then the
   current projection reports `status=unknown` and `source=none`.
10. Unknown tool names and tools mentioned only in prose, a repository,
    checkout, working directory, verification gate, assignment, or work item
    never enter `requirements` unless the selected harness registry also
    declares the exact basename.
11. Tests plant secrets in overlay values, probe arguments, stdout, stderr,
    provider bodies, and exceptions; none appear in storage, list/read output,
    wire output, logs, or failure fields.
12. A principal who cannot read a session cannot read its environment object.
13. No aggregate readiness verdict, refusal, wake steering, or action gate is
    derived from the object.
14. Canonical gate tests name only the four scrubbed variable classes above.
15. The shipping candidate amends only `docs/ONBOARDING.md` and uses only the
    actual shipped list/read and doctor field names.
16. Existing doctor behavior is byte-for-byte compatible when neither
    `--session` nor `--requirement` is supplied; partial forms and combinations
    with `--base-dir` refuse before host work.
17. A caller who cannot read the named session cannot probe it. Unknown,
    malformed, path-like, or shell-bearing requirement names refuse without a
    host operation or evidence row. A retired session follows the same refusal.
18. The host probe resolves but never invokes the declared executable. Tests
    prove that stdout, stderr, side effects, and resolved paths cannot enter the
    result, storage, logs, or wire projection.
19. Given five concurrent changes applied separately during five doctor runs —
    active session to retired, registered host, harness, environment-row
    revision, and provisioning revision — when each probe completes, then each
    result is discarded and the new evidence key remains `status=unknown` and
    `source=none`.
20. Given a valid effective PATH, when doctor completes, then it returns only the
    closed requirement record. Given no effective PATH, then it returns only the
    matching provisioning-fact code. Neither form returns a readiness verdict,
    wake instruction, or action decision.
21. Given an exact predecessor host schema and legacy host rows, when the
    provisioning-facts migration runs, then the source contract's migration
    acceptance passes, legacy sessions remain readable with `path.mode=none`,
    and no backfill infers facts.
22. Given two gateway processes with different inherited PATH values and the
    same session, environment rows, and provisioning revision, when they project
    and probe that session, then their PATH entries and evidence keys are
    byte-identical.

## Open questions

No product-policy question blocks this specification. Mike selected
`provisioning_facts`; the full session key supplies incarnation identity; and
the existing session active state supplies the session-lifecycle race boundary.
Any false implementation assumption is a named technical blocker and requires a
new product-owner disposition before scope expands.

## Review and implementation gate

1. Freeze this file in the canonical `tightbeam-specs` repository with an exact
   commit and SHA-256.
2. Obtain one independent `reviewed-clean` or `changes-requested` verdict for
   that exact revision.
3. Dispatch no code before that one review records `reviewed-clean`.
4. Require focused and full gates, a pushed non-main candidate, and an
   independent exact-commit code review.

The work item remains untargeted. This specification authorizes no product
edit, merge, release, deployment, credential change, host configuration change,
or live-state mutation.
