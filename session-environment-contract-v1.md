# Session environment contract v1

Work item: `wi_d9cf7b4b-6683-4e77-a88b-5c07340d2abc`

Status: proposed. This specification does not authorize implementation until an
independent reviewer records `reviewed-clean` for this exact revision.

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
- Do not change the PATH ruling in `att_6dab429d`.
- Do not teach an operating pattern before the projection ships.

## Terms

- **Authorized row**: an existing host-and-harness environment or toolchain row
  admitted through Tightbeam's current configuration seam.
- **Effective session environment**: the environment supplied to one concrete
  session generation after applying the authorized rows and the PATH rule below.
- **Declared requirement**: a tool name already declared by the selected
  harness registry entry or by the repository's canonical verification gate.
  Prose cannot declare a requirement.
- **Projection**: the fact-only `environment` object attached to an existing
  session row in the authenticated list/read and wire projections.
- **Probe**: the existing bounded doctor check for one declared requirement in
  one effective host-and-harness environment. Listing a session never runs a
  probe.
- **Evidence key**: the tuple of session key, session generation, host, harness,
  and authorized environment/toolchain row revisions used for one observation.

## Assumptions

These assumptions are falsifiable implementation preconditions:

1. Current main can read separate harness, model, effort, and context values.
2. Current main can read authorized host-and-harness environment and toolchain
   rows without exposing their values.
3. Current main has a bounded doctor path that can test whether a declared
   executable resolves in the effective environment.
4. Existing authenticated session list/read and wire projections already decide
   which principals may see a session.

If any assumption is false, the implementer stops and records the missing seam.
The implementer does not invent a second configuration, probe, or authorization
mechanism.

## Invariants

1. A capability is present only when a bounded doctor probe observes it for the
   current evidence key. Authorized rows define the effective environment and
   contribute to the evidence key; they never prove a tool capability.
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

## Existing PATH ruling

Preserve `att_6dab429d` exactly:

- With no toolchain rows, keep the inherited PATH byte-for-byte.
- With toolchain rows, construct PATH from the Tightbeam CLI directory, the
  configured directories, and `/usr/local/bin:/usr/bin:/bin`, in that order.
- Apply the same formula to remote session environments.
- Show the shape switch and PATH preview when configuration changes.
- Do not validate remote directories at write time. Adapter launch reports a
  wrong directory loudly.

This rule does not prove that any optional tool exists. The `engram` incident is
the acceptance example: prose naming `engram` cannot make it resolvable.

## Architecture

### Projection actor and timing

The gateway assembles the `environment` object from existing session placement,
model, and authorized rows, and assembles requirement status only from bounded
doctor evidence for the current evidence key. It attaches the object to the
existing authenticated session list/read response and corresponding wire row.

Session reads are non-mutating. They do not execute a command, refresh a probe,
or inspect a login shell. The existing bounded doctor path is the sole active
probe actor. A doctor run records only the closed result described below.

### Projection schema

The additive `environment` object has this closed shape:

```text
environment:
  observedAt: epoch milliseconds
  sessionGeneration: existing session generation identifier
  host: registered host name
  harness: registered harness name
  model: model identifier
  effort: typed effort value or null
  context: typed context value or null
  path:
    mode: inherited | toolchain_rows
    entries: ordered path entries
  overlayNames: sorted environment variable names
  requirements:
    - name: declared tool name
      declaredBy: harness_registry | repository_gate
      status: available | unavailable | probe_failed | unknown
      observedAt: epoch milliseconds or null
      source: doctor_probe | none
      failure: not_found | not_executable | timed_out | refused | transport_failed | null
```

No other status, source, or failure value is valid. `requirements` contains only
declared requirements. `available`, `unavailable`, and `probe_failed` always
have `source=doctor_probe`. `unknown` always has `source=none` and means there
is no applicable doctor observation for the current evidence key. An authorized
row alone never changes `unknown` to another status. `unavailable` means the
bounded check completed and proved absence or non-executability. `probe_failed`
means the check could not make that observation; it does not mean unavailable.

`observedAt` is evidence time, not a freshness judgment. The substrate applies
no age threshold. Agents may weigh age. A session-generation or authorized-row
revision mismatch is mechanical: the current status becomes `unknown`.

### Secret and visibility boundary

The projection may contain environment names and the PATH entries already
required by the PATH ruling. It must not contain:

- any environment value;
- a credential, token, cookie, authorization header, or credential path;
- probe arguments, stdin, stdout, or stderr;
- provider response bodies or exception text;
- a resolved executable path; or
- an unbounded/raw provenance value.

Probe persistence is limited to the closed requirement record above plus the
evidence key. Failure classification happens at the probe boundary. Unknown
errors become `refused`; raw text is discarded before persistence and wire
projection.

The `environment` object inherits the exact authorization and row filtering of
the session row that contains it. It is never emitted on a broader org stream,
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
projection and to use the existing doctor path for a bounded refresh. It must use
the shipped field and command names only. No other guidance home is amended.

## Acceptance

1. With no toolchain rows, a session projection reports `path.mode=inherited`
   and byte-identical inherited PATH entries.
2. With toolchain rows, local and remote projections report
   `path.mode=toolchain_rows` and the exact ordered PATH formula above.
3. Configuration preview reports the PATH shape switch; configuration does not
   validate a remote directory.
4. Harness, model, effort, and context round-trip as separate fields.
5. Projection exposes overlay names but never their values.
6. A declared executable found by doctor records `available`; a completed miss
   records `unavailable`; timeout/transport/refusal records `probe_failed`; no
   applicable observation records `unknown`.
7. Listing a session performs no probe and causes no environment mutation.
8. An authorized environment or toolchain row alone never proves a declared
   capability: before a bounded doctor observation, the requirement projects
   `status=unknown` and `source=none`.
9. A changed session generation or authorized-row revision prevents reuse of
   earlier probe status and projects `status=unknown` and `source=none` until a
   new bounded doctor observation records evidence for the new evidence key.
10. Unknown tool names and tools mentioned only in prose never enter
   `requirements`.
11. Tests plant secrets in overlay values, probe arguments, stdout, stderr,
    provider bodies, and exceptions; none appear in storage, list/read output,
    wire output, logs, or failure fields.
12. A principal who cannot read a session cannot read its environment object.
13. No aggregate readiness verdict, refusal, wake steering, or action gate is
    derived from the object.
14. Canonical gate tests name only the four scrubbed variable classes above.
15. The shipping candidate amends only `docs/ONBOARDING.md` and uses only the
    actual shipped list/read and doctor field names.

## Open questions

No product-policy question blocks this specification. Implementation may reveal
a missing existing seam from the assumptions section; that is a named technical
blocker and requires a new product-owner disposition before scope expands.

## Review and implementation gate

1. Freeze this file in the canonical `tightbeam-specs` repository with an exact
   commit and SHA-256.
2. Obtain independent reviewed-clean for that exact revision.
3. Dispatch no code before steps 1 and 2 are durable.
4. Require focused and full gates, a pushed non-main candidate, and an
   independent exact-commit code review.

The work item remains untargeted. This specification authorizes no merge,
release, deployment, credential change, host configuration change, or live-state
mutation.
