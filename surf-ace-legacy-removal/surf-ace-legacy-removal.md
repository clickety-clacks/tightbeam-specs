# Surf Ace lockless-only legacy removal

Status: review candidate. This text becomes implementation authority only after
one independent exact-revision review returns `reviewed-clean` and the work item
binds this file's reviewed SHA-256.

Source basis:

- Product ruling: Mike, 2026-08-29. Surf Ace has no production deployments.
- Superseding product ruling: Mike's 2026-08-29 standing policy, relayed at
  12:01 PT. The product contains no compatibility shim, migration, conversion,
  or cleanup path. An operator deletes old development-fleet state before
  validation.
- Surf Ace discovery base: `clickety-clacks/surf-ace` main
  `19f90ddf6f848d267889e0a3ea9ff6bb76223f9f`.
- Spec-commons discovery base: `clickety-clacks/tightbeam-specs` main
  `9ddcb07a779ee9f73285f5bfa54898651e781f13`.
- Reviewed pairing-recovery source:
  `3fd6b1ec49aedd4a271cec160a07936e17614d74`, integrated by PR 14 as
  `13974d360eea2c9f99787d439903841b637f6246`. Its independent source review
  passed 489/489 tests and proved bounded admission evidence, refusal, retry,
  restart, rollback, duplicate/concurrent request handling, and three-surface
  push/capture behavior.
- Pending implementation input: Mike's reviewable `rip/legacy-mode` branch. The
  removal implementation consumes the exact remote branch revision that its
  owner files as review-ready. This spec does not authorize a competing source
  branch.
- Prior exact-revision review: commit
  `8c9083be9e8c5f6616cd084bba49b1195b47d412` received `changes-requested` in
  `att_e98cdcff-f9e6-4089-97b9-e929d4471d2d`. This revision absorbs its three
  findings. The prior revision is not implementation authority.

## Goal

### Spirit

Surf Ace has no production deployments. Lockless client-local authority is the
only supported authority model. Provider ownership, mode negotiation, migration,
conversion, and rollback compatibility are dangerous dead code because they
preserve two conflicting models and can block a valid lockless surface.

Deliver one deletion-only, lockless-only Surf Ace product. Delete the legacy
compatibility surface from product code, wire contracts, schemas, commands,
persisted schemas, tests, documentation, integration instructions, and operator
procedures. The product applies only the current strict schema to existing state.
It must neither recognize legacy concepts in nor repair old development state. A
separately authorized operator deletes that state before fleet validation starts.

The subtraction ruling is DELETE. ADD loses because any product cleanup,
adapter, tombstone, receipt, migration, or conversion seam preserves the model
being removed. ACCEPT loses because leaving callable compatibility code would
keep conflicting authority live.

## Non-Goals

1. This work does not support a production migration. No production deployment
   exists.
2. This work does not preserve, rename, emulate, translate, import, export, or
   project provider-owned state.
3. This work does not add a startup cleanup, one-time schema migrator,
   compatibility reader, compatibility flag, conversion command, rollback tool,
   legacy-state receipt, or manual product repair command.
4. This work does not preserve old development state, stable identities from
   that state, content from that state, or a recoverable copy of that state.
5. This work does not redesign the current lockless controller, surface, pane,
   history, content, topology, target, cursor, tombstone, operation-receipt,
   admission-attempt, or capacity models.
6. This work does not rewrite Git history. Git history and immutable evidence
   remain the record of the deleted implementation.
7. This spec does not authorize source edits, source review, integration,
   packaging, installation, operational state deletion, live access, or E2E
   execution by itself. Each later stage requires a separate assignment and
   exact reviewed input.
8. This work does not choose a release tag, product target, or Tightbeam target.
9. This spec producer does not open, amend, or implement a competing Surf Ace
   source branch. Findings against `rip/legacy-mode` return to that branch's
   owner.

### Declined decisions

- **DECLINED — product startup cleanup:** the superseding ruling assigns deletion
  to the operator before validation. Product code neither recognizes legacy
  concepts nor decides their disposition.
- **DECLINED — migration or conversion:** there is no production material to
  preserve and no second supported mode to convert from or to.
- **DECLINED — compatibility refusal keyed to former field names:** current
  schemas reject unknown material generically. They do not carry a registry of
  former keys.
- **DECLINED — parallel source implementation:** Mike's reviewable
  `rip/legacy-mode` branch is the sole source candidate.

## Terms

- **Lockless authority**: the current client-local authority identified by
  `surf-ace.lockless-multi-controller.v1`. It admits controller instances without
  granting ownership, priority, quota, veto, or restore rights.
- **Legacy compatibility surface**: any product behavior or material that
  represents provider ownership, a legacy/lockless mode choice, migration from
  provider-owned state, conversion between authority modes, or rollback from
  lockless state to provider-owned state.
- **Deletion-only product**: a product whose current source and generated
  material contain the lockless model and no compatibility implementation. It
  contains no legacy-specific knowledge that could clean, migrate, or convert
  old state.
- **Old development state**: any Surf Ace state root or application store created
  by a package before the reviewed legacy-removal package. Its contents are
  disposable under Mike's ruling.
- **Operational deletion**: a separately authorized host operation that stops
  each writer, deletes the exact approved old development-state roots, verifies
  absence, and leaves no backup, archive, quarantine, or restore source. It is
  not a Surf Ace command or product behavior.
- **Fresh lockless state**: state created from absence by the reviewed
  deletion-only package. It contains only the current lockless schema.
- **Reviewable rip branch**: Mike's `rip/legacy-mode` source branch after its
  owner records canonical repository, base, exact remote commit, tree, test
  evidence, and review readiness.
- **Current four-surface fleet**: the exact four Eezo surfaces discovered after
  operational deletion and fresh startup, then sealed in the separately
  authorized E2E readiness manifest. Old or remembered IDs do not define this
  set.
- **Supported material**: current product source, generated schema, installed
  CLI and runtime surfaces, active documentation, active integration
  instructions, and active operator procedures. This canonical spec and
  immutable evidence are authority records, not supported product surfaces.

## Assumptions

1. The product owner's ruling that Surf Ace has no production deployments is
   true. If a production deployment is found, packaging and operational deletion
   become BLOCKED pending a new product ruling. The implementation does not
   invent migration policy.
2. Mike's reviewable `rip/legacy-mode` branch will carry the source removal. Its
   exact commit is a stage input, not a value this spec infers.
3. The current source contains the reviewed pairing-recovery behavior and bounded
   admission-attempt ledger. Removal preserves the lockless parts of that
   behavior.
4. Old development state is disposable. No identity, content, history, target,
   receipt, or diagnostic from that state must survive operational deletion.
5. The operational deletion assignment can identify exact state roots from the
   reviewed package/runtime configuration and can stop their writers before it
   deletes bytes.
6. Fresh startup after deletion produces four Eezo surfaces when the E2E
   readiness manifest is issued. A different cardinality blocks that run.
7. Each current lockless state owner already enforces finite capacity and
   privacy bounds for fresh state. Removal does not weaken those bounds.

## Invariants

### I-01 — One authority model

Surf Ace implements lockless authority only. A request either satisfies the
lockless protocol or receives a deterministic refusal before mutation. No code
path falls back to provider ownership or selects an authority mode. Acceptance:
A-01, A-02, A-03, A-10.

### I-02 — No ownership semantics

Supported requests, responses, discovery, diagnostics, CLI input/output, and
persisted schemas carry no provider owner, ownership epoch, owner session,
takeover, relinquish, busy-as-owner, self-reclaim, or owner-only authorization
semantics. Friendly controller product labels remain labels only. Acceptance:
A-01, A-02, A-10.

### I-03 — No migration, conversion, or cleanup

`pair.request` has no migration material. Pair responses have no migration
acceptance or migration receipt. The wire has no surface-mode conversion
operation. The CLI has no conversion or cleanup command. Startup has no reader,
projection, transformer, or receipt that is specific to legacy state. Acceptance:
A-01, A-02, A-03, A-09.

### I-04 — Fresh state only

The reviewed package starts from absent state and writes only the current
lockless schema. When a configured state root contains unknown pre-removal
material, startup refuses generically before external I/O and leaves those bytes
unchanged. Acceptance: A-03, A-04, A-07.

### I-05 — Operational deletion precedes product validation

An operator proves each writer stopped, deletes each exact approved old state
root, and proves absence before installation/startup validation opens product
I/O. The product performs no part of this deletion. Acceptance: A-04, A-05,
A-06.

### I-06 — Deletion has no recovery lane

Operational deletion leaves no backup, archive, quarantine, compatibility
snapshot, or restore command. If operational deletion is interrupted, the
operator uses the sealed pre-delete evidence to finish deletion. If that evidence
is missing or corrupt, the run is Red and product validation remains blocked. A
later fresh-start failure is a product/package Red; it does not reopen old-state
deletion or recovery. The workflow does not reinstall an older package against
the deleted roots. Acceptance: A-05, A-06, A-07.

### I-07 — Concurrency cannot recreate old state

Operational deletion begins only after the executor proves that no process,
service, scheduled launcher, or open file handle can rewrite an approved state
root. A writer or root that reappears stops validation. Acceptance: A-05, A-06.

### I-08 — Evidence is private and bounded

The operational report records root identities, manifest SHA-256 values,
process/listener absence, deletion result, and PT timestamps. It includes no
file content, provider/controller/surface/pane identifier from deleted state, or
copied state artifact. Fresh product state retains its existing finite capacity
and privacy limits. Acceptance: A-08, A-10.

### I-09 — Lockless behavior remains real

The exact reviewed package must admit, mutate, capture, render, restart, and
restore test content on each surface in the fresh four-surface Eezo fleet.
Evidence from one surface does not admit or grade another. Acceptance: A-10.

### I-10 — One source candidate

Implementation and source review consume the exact reviewable
`rip/legacy-mode` revision. A reviewer returns findings to its owner. No agent
opens a parallel removal branch or silently composes competing source bytes.
Acceptance: A-11.

## Architecture

### 1. Removal rule

For the exact reviewable `rip/legacy-mode` revision, source review classifies
each current-main match in the closed inventory below as either **deleted** or
**rewritten without the legacy concept**. It leaves no compatibility stub,
ignored field, deprecated alias, dormant command, rollback helper, test-only
implementation, or product cleanup path.

A match outside the paths listed below is a requirement finding. The reviewer
returns it to the branch owner and asks the spec writer whether the inventory
needs amendment. The reviewer does not implement the finding on a new branch.

### 2. Closed removal inventory

#### 2.1 Product ownership and legacy sessions

Delete or rewrite the provider-ownership model across:

- `packages/electron/src/surface-core.ts`: `PersistentProviderOwnership`,
  `providerOwnership`, `getProviderOwnership`, `setProviderOwnership`,
  `clearProviderOwnership`, `hadLegacyOwnership`, ownership admission gates,
  serialization, and deserialization.
- `packages/electron/src/ws-server.ts`: provider sessions, ownership epochs,
  owner resume, takeover, relinquish, busy-owner projection, legacy pairing,
  legacy send gates, and their handlers.
- `packages/extension/src/**`: provider identity and lineage, local/remote
  ownership observation, self-owned surface recovery, ownership retry/circuit
  behavior, owner-session and owner-epoch target fields, relinquish, takeover,
  legacy runtime composition, and ownership-only diagnostics/errors.
- `packages/ios/SurfAce/**`: ownership locks, provider sessions, takeover,
  relinquish, busy-owner discovery, legacy pairing, provider/owner target fields,
  and mode-gated dispatch.
- `packages/protocol/**` and `packages/controller/**`: provider/owner wire fields,
  legacy session behavior, and each controller branch that selects it.
- Executable implementations under `legacy/electron`, `legacy/ios`, and
  `legacy/provider-extension`. Git history remains the archive.

Tests that exist only to prove those behaviors are deleted. Lockless tests are
rewritten only where a fixture currently carries an obsolete field.

#### 2.2 Migration, conversion, rollback, and cleanup

Delete or rewrite:

- `pair.request.migrationMaterial`, pair-response `migrationAccepted` and
  `migrationReceiptId`, their types, validators, generated JSON schema,
  conformance vectors, client/controller hooks, and error projections.
- Electron `migrationReceipts`, `modeBySurfaceId`, `surfaceMode`, mode setters,
  conversion methods, migration-material import, migration-receipt digest/replay,
  `legacy_migration` transition reasons, and mode/remedy errors.
- Controller `prepareMigration` contracts and extension migration source,
  compatibility-read boundary, continuity transaction, phase, preparation,
  replay, source-clear, receipt, and serialization code.
- iOS `SurfAceLocklessMigration.swift`, legacy UserDefaults import/projection,
  negotiated legacy mode, rollback preview, and related authority transition.
- Electron `legacy-rollback-migration.ts`, `legacy-rollback-cli.ts`, their build
  entry points and package scripts, rollback preflight scripts, generated output,
  README instructions, and tests.
- Wire operation `surface.mode.convert`, CLI command
  `surface-mode-convert`, command parsing/routing, request vectors, response and
  error contracts, docs, and tests.
- Any proposed startup cleaner, legacy-specific old-state reader, compatibility
  schema, deletion receipt, obsolete-key registry, or product-owned state
  deletion.

The ordinary lockless pair path keeps its existing controller identity,
capability, cursor, receipt-resolution, and admission-attempt behavior.

#### 2.3 Persisted schema

Current persisted schemas contain no provider ownership, authority mode,
migration, conversion, rollback, or cleanup field. In particular they contain
none of these former records:

- Electron surface `providerOwnership`;
- Electron authority `modeBySurfaceId` and `migrationReceipts`;
- controller/extension `locklessMigrationContinuity`, provider lineage,
  self-owned-surface recovery, ownership-only tombstones, local/remote ownership
  snapshots, owner session/epoch state, and ownership-only target fields; or
- iOS `negotiatedModes`, legacy UserDefaults import inputs, and provider/owner
  fields in stored surface or target material.

The current schema is strict. Unknown top-level or nested fields fail the
existing schema-validation boundary generically. Product code does not name
former fields to decide their disposition.

#### 2.4 Supported descriptions and procedures

Rewrite active descriptions so they state one lockless contract and no
compatibility path. The inventory includes:

- Surf Ace `DESIGN.md`, root and package READMEs, `docs/design/**`, integration
  skills/instructions, package scripts, generated schemas, and conformance
  vectors.
- `tightbeam-specs` active Surf Ace procedure bundles
  `surf-ace-e2e-procedure-v4/**` and
  `surf-ace-e2e-procedure-v4-1-correction/**`. Their admission contract uses a
  reviewed lockless package and an absent/fresh state root. It does not permit,
  derive, request, or route migration material, conversion, or product cleanup.

Historical Git commits, this canonical spec, and immutable evidence may name the
removed concepts. No installed help, supported README, current design, generated
schema, active integration instruction, or active operator procedure may do so.

### 3. Product startup boundary

The deletion-only package has two accepted startup inputs:

1. no state exists, so the product creates fresh lockless state; or
2. state exists and validates exactly as the current lockless-only schema.

Any other state returns one generic unsupported/corrupt-state refusal through
the existing startup failure seam before endpoint bind, advertisement,
discovery, socket acceptance, window mutation, or state write. The refusal does
not enumerate former fields, suggest conversion, or mutate/delete the root.

### 4. Operational deletion boundary

Operational deletion is outside Surf Ace. Its separately authorized procedure
performs this order:

1. Rehash the exact reviewed package and configuration that identify each state
   root and writer.
2. Resolve each explicit old state root. Reject an empty, home, workspace-root,
   system-root, unresolved-variable, glob, or symlink-escaped target.
3. Stop each exact writer and scheduled launcher through its supported host
   control path.
4. Prove no matching process, listener, scheduled launcher, or open writer handle
   remains.
5. Build one metadata-only manifest row for each exact approved root. A present
   root row records `present`, entry count, aggregate byte count, and tree
   SHA-256. An absent root row records `absent-before-deletion`. Do not copy file
   contents.
6. Before deleting any root, compute the manifest SHA-256, atomically write the
   manifest to a run-owned evidence path outside every approved root,
   synchronize the file and its containing directory through the host's
   durable-write primitives, close and reopen it, and require its readback
   SHA-256 to equal the pre-write SHA-256. Record that exact path and digest as
   an artifact on the operational assignment, query the artifact row, rehash the
   path, and require the row digest, pre-write digest, and new readback digest to
   match. Do not mutate the manifest after that check. The sealed manifest is
   the sole source of pre-delete proof.
7. Delete only approved roots whose sealed row says `present`. Do not archive or
   quarantine them. Do not delete an unlisted root.
8. Prove each approved root is absent and no writer/listener reappeared.
9. Finalize the bounded operational report with the sealed manifest SHA-256 and
   per-root deletion result. Only then release the reviewed package
   installation/startup assignment.

If interruption occurs after step 6, product startup remains blocked. On resume,
the executor reopens and rehashes the exact sealed manifest before any action. A
missing, unreadable, or hash-mismatched manifest produces the named Red result
`operational_proof_lost`; the executor does not reconstruct proof from remaining
roots or release product startup. For a sealed `present` row, an absent root is
already deleted; a present root must still equal its sealed tree SHA-256 before
the executor deletes it. A different tree produces the named Red result
`operational_root_changed`. For a sealed `absent-before-deletion` row, a present
root is a reappearance and stops the run. With intact proof and unchanged
remaining roots, the executor repeats writer checks and steps 7 through 9. This
is retry of host deletion, not product cleanup or migration.

### 5. Static closure

The source-review report runs deterministic scans over supported material. It
must find zero definitions, schema keys, commands, operations, or descriptive
clauses for these exact removed concepts:

`providerOwnership`, `setProviderOwnership`, `clearProviderOwnership`,
`hadLegacyOwnership`, `ownership.relinquish`, `migrationMaterial`,
`migrationAccepted`, `migrationReceiptId`, `modeBySurfaceId`,
`negotiatedModes`, `negotiateLegacySurface`, `surface.mode.convert`,
`surface-mode-convert`, `legacy-rollback`, `prepareLegacyMigration`,
`locklessMigrationContinuity`, and `locklessOnlyCleanupReceipt`.

The report also proves the `legacy/` executable source tree is absent and
performs a semantic schema/CLI/doc review for provider owner, owner session,
takeover, migration, conversion, rollback, and cleanup behavior whose spelling
is not in the token list. Generic strict-schema tests use unknown fixture keys;
they do not preserve a named former key as a supported fixture.

### 6. Delivery order and gates

Stages do not overlap. A later stage consumes exact reviewed outputs from the
prior stage.

1. **Reviewed spec**: freeze this bundle on one non-protected
   `tightbeam-specs` branch. One independent reviewer returns `reviewed-clean` or
   `changes-requested` for that exact commit. After `reviewed-clean`, bind the
   work item to the reviewed canonical path and SHA-256.
2. **Reviewable source receipt**: wait for the `rip/legacy-mode` branch owner to
   file canonical repo, base, exact remote commit/tree, gates, and review
   readiness. Do not poll, open a parallel branch, or compose source locally.
3. **Independent source review**: review that exact revision against this closed
   inventory, pairing-recovery preservation, static closure, and the full
   repository gate. Return `changes-requested` findings to the branch owner.
4. **Procedure reconciliation**: amend the two active Surf Ace procedure bundles
   on one reviewed `tightbeam-specs` revision. Do not combine it with the frozen
   spec commit.
5. **Integration**: integrate the unchanged reviewed Surf Ace revision through
   the protected Surf Ace process. Integrate the unchanged reviewed procedure
   revision through the current approved `tightbeam-specs` process. Verify
   ancestry, tree equality, current-main readback, and full gates. Do not
   direct-push, amend reviewed bytes, or change repository policy.
6. **Exact packages**: build the CLI and each Surf Ace runtime package required
   by the Eezo fixture from the exact integrated Surf Ace commit in a clean owned
   directory. Require a complete manifest, native architecture, source/tree
   provenance, and independent package review. Do not install before review.
7. **Operational state deletion**: under separate destructive/live-state
   authority, execute Architecture section 4 and file its report. Do not run a
   Surf Ace command against the old roots.
8. **Fresh startup and E2E**: install only the reviewed exact packages. Start
   from absent state, issue a fresh readiness manifest, and run A-10 on the four
   discovered surfaces.

Operating pattern taught to Tightbeam agents: none. This spec changes Surf Ace
product and procedure authority only; it does not amend the Tightbeam operating
manual.

## Acceptance

### A-01 — Closed product inventory is absent

**Given** fresh clones at the exact integrated Surf Ace and `tightbeam-specs`
commits, **when** the reviewer runs Architecture section 5 against source,
generated schema, installed CLI help/command enumeration, active docs,
integration instructions, and both active Surf Ace procedure bundles, **then**
each listed token and each semantically equivalent supported behavior has zero
matches, the `legacy/` executable tree is absent, and the report lists no
unclassified match.

### A-02 — Pairing has one contract

**Given** a fresh lockless surface and a controller with the required lockless
capability, **when** it sends the ordinary `pair.request`, **then** admission
succeeds without a mode read/write and without migration or ownership material.

**Given** the same surface, **when** a request omits a required capability or
contains an unknown extra field, **then** the protocol returns its documented
`capability_mismatch` or generic `invalid_payload` before mutation, and no
fallback pair path runs.

### A-03 — Product startup does not clean old state

**Given** a run-owned invalid-state fixture that fails the current strict schema
through an anonymous unknown field and contains no copied old-state content or
former field name, **when** the deletion-only package starts against that fixture
offline, **then** startup returns the generic unsupported/corrupt-state refusal
before external I/O, changes no byte in the root, creates no receipt/backup, and
emits no conversion or cleanup instruction.

### A-04 — Absent state creates fresh lockless state

**Given** an absent run-owned state root, **when** the reviewed package starts,
**then** it creates only the current lockless schema, contains no section 2.3
field, and admits an ordinary lockless controller without a mode record.

### A-05 — Operational deletion is exact and complete

**Given** separate destructive authority naming each explicit old Eezo state
root and writer, **when** the executor performs Architecture section 4, **then**
the report proves writer/listener absence before deletion, durable sealing and
artifact readback of the metadata-manifest hash before the first deletion,
absence of each exact root after deletion, no backup/archive/quarantine, and no
product command execution.

### A-06 — Concurrent writer blocks deletion release

**Given** an approved root whose writer, listener, scheduled launcher, or open
write handle remains or reappears, or a sealed `absent-before-deletion` root that
reappears, **when** the executor reaches the quiescence or absence checks,
**then** it stops before package startup, records the exact writer or root
evidence, and does not broaden or guess the deletion target.

### A-07 — Interrupted deletion retries without product recovery

**Given** an interruption after one approved root is deleted and before each
root passes absence, **when** work resumes with the intact sealed manifest,
**then** product startup remains blocked, the executor accepts a sealed-present
but now-absent root as already deleted, rehashes each remaining present root
against its sealed tree SHA-256, and completes deletion on the same explicit set.
It does not restore old state, install an older package, or invoke a Surf Ace
cleanup/migration path.

**Given** the same interruption with a missing, unreadable, or hash-mismatched
sealed manifest, **when** work resumes, **then** the run records
`operational_proof_lost`, leaves product startup blocked, and does not reconstruct
pre-delete proof from the partial state.

**Given** the same interruption with an intact sealed manifest and a remaining
present root whose current tree SHA-256 differs from its sealed value, **when**
work resumes, **then** the run records `operational_root_changed`, leaves product
startup blocked, and does not delete the changed root.

### A-08 — Deletion evidence is bounded and private

**Given** the largest approved old-state root set for the Eezo run, **when** the
operational report is serialized, **then** it contains one fixed row per approved
root plus one summary, contains no deleted file content or identifier extracted
from that content, and stores no copied state artifact. Each human-readable time
is in PT and says `PT`.

### A-09 — Former conversion and cleanup surfaces do not exist

**Given** the installed reviewed CLI and running reviewed endpoint, **when** an
operator enumerates commands and wire operations, **then** no former conversion,
migration, rollback, or cleanup surface is present. Invoking a former CLI command
fails command parsing before network I/O. Sending a former wire operation as an
untyped external test frame receives the generic unknown-operation or
invalid-payload refusal and changes no state.

### A-10 — Four-surface Eezo regression is Green

**Given** separately authorized Eezo execution, exact independently reviewed
packages from one integrated commit, operational deletion evidence for each old
state root, fresh run-owned state, and a readiness manifest that discovers
exactly four fresh surfaces and their panes, **when** the sole operator runs the
reviewed E2E procedure, **then** each surface independently passes:

1. ordinary lockless admission with no conversion, migration, or cleanup input;
2. push/capture/render stages of 1, 5, 20, and 100 pushes, with a unique marker
   visibly present in a capture after each accepted push;
3. one containing client restart and one controller restart, after which its
   fresh surface/pane identities, topology, last accepted marker, and lockless
   operation capability remain valid;
4. rollback of test content to the recorded fresh pre-test content; and
5. a final state/schema scan with no removed concept.

A result from one surface cannot satisfy another surface. Cardinality or identity
drift stops the run before mutation and requires a fresh readiness manifest. A
Red result routes a finding against the reviewed current source/package/procedure;
it does not restore old state or open a compatibility path.

### A-11 — The implementation consumes Mike's source branch

**Given** the branch owner's review-readiness receipt, **when** source review
starts, **then** the reviewed repository, base, remote commit, and tree equal that
receipt for `rip/legacy-mode`, and the work trace contains no parallel
legacy-removal source assignment or competing source commit.

### A-12 — Delivery evidence is exact

**Given** the eight stages in Architecture section 6, **when** a stage reports
Green, **then** its immutable report names the canonical repo, branch, base,
exact commit/tree, SHA-256 inputs and outputs, commands, test counts, and
forbidden actions that did not occur. The spec, source, procedure, and package
review stages also name their exact review verdict. The integration stage names
ancestry, tree-equality, readback, and gate results. The operational-deletion
stage names its section 4 evidence. The E2E stage names its A-10 result per
surface. The next stage starts only after it rehashes the exact inputs from its
prior stage.

## Open Questions

None. This spec has no BLOCKING or NON-BLOCKING open question. The exact
`rip/legacy-mode` commit is a required future stage input, not a design choice.
