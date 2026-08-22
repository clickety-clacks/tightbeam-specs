# Engineering activation consumer on Tightbeam main v2

Status: spec-ready for one independent policy review; implementation, pinning, installation, deployment, restart, release, and live-state mutation remain unauthorized  
Recorded: 2026-08-20 23:23 PT  
Work item: `wi_ddd80184-9cf7-4612-8a0a-ac610b5b7b10`  
Policy assignment: `asg_f511f989-90db-45e8-b1d3-434d3d9b58bc`  
Owner authority: `art_abe67f90`, SHA-256 `3d0d5b6b82f81760e06d31780738bde39d91c7d06a3edeb3d574bac06c838bf4`  
Main reconciliation: `art_044819f6`, SHA-256 `10af361e2addcac2c1fc17a451468a48a6063389f93a74b58064c1193d00ff8a`, verdict `att_d92acfca-ed6b-4883-9f59-208e60f58d34`  
Neutral substrate authority: `art_2bc5475e`, SHA-256 `5eb530a0183d793b35be1363c2a0aaea8b021490f11ef159887377f4f42805fb`  
Deployment-safety authority: `art_c4230451`, SHA-256 `5db00f518feb0c398e0c33a0f9a44d1c89e1af06ee177fd08a9fd6f040fb316e`  
Supersedes the Engineering consumer policy in `art_16df51ca` and `art_44b99337`; preserves their reviewed findings and acceptance except where this complete policy states a replacement.

## Goal

Define the Engineering policy that joins the reviewed neutral `activation-events-v1` primitive to the reviewed Linux deployment manager on Tightbeam main.

The policy must make a production installation mechanically unable to cross either adopted rename entry point until the manager holds an `AcceptedActivationAttempt` derived from the committed or exact-replayed neutral attempt response.

The policy must preserve a durable paper trail that binds Mike's production-installation approval, the exact machine target, the manager attempt, the external mutation, each service result, the machine result, owner notice, and recovery.

The policy must keep each production path that lacks the adopted typed seam labelled **NOT MECHANICALLY GATED**.

This policy adds the Engineering consumer adapter because deleting the supported production-installation surface would strand existing service installations, while accepting the current direct-overwrite path would fail this work item's paper-trail goal.

## Non-Goals

1. This policy does not authorize source changes, implementation cards, a spec pin, package installation, deployment, activation, restart, rollback, service-unit replacement, release action, credential mutation, Git-ref mutation, or work-item disposition.
2. This policy does not change the neutral event table, event kinds, verbs, capability, lifecycle, read relations, replay rules, wake semantics, or acceptance contract in `art_2bc5475e`.
3. This policy does not add a second activation primitive, a deploy-specific substrate fact, a generic policy engine, a generic callback registry, or a generic workflow engine.
4. This policy does not add a deployment root per gateway instance, a second deployment scope on one machine, a configurable service-set source, or a parallel deployment lock.
5. This policy does not add a filesystem class or mount-option class beyond ext4 mounted with default options.
6. This policy does not add a deployment user. Root remains the deployment executor, and each gateway remains under its registered non-root service account.
7. This policy does not add a time threshold, health-duration threshold, or observation wait.
8. This policy does not define a macOS or launchd mutation, restart, recovery, rollback, or observation contract.
9. This policy does not claim that release-candidate evidence, a design row, a CI receipt, a later restart, or prose mechanically gates a production mutation.
10. This policy does not change the separate authority required for restart, rollback, unit rollback, GC, acknowledgement, or compensation.

## Terms

- **Execution-time main authority**: Git commit `644c04064594328b5ec1c1b76301a1ac893bffc2`, which `refs/heads/main` named at 2026-08-20 23:23 PT. Its root tree is `54f9c06efc8bdbb922b0e0ddba812c5e49168724`. The exact relevant object identities appear under Architecture. The frozen `0.1.8` and `0.1.x` history is evidence, not an integration target for this policy.
- **Neutral activation primitive**: the one `activation_events` stream and fixed `activation-*` verb family defined by `art_2bc5475e`. Tightbeam verifies identity, shape, order, replay, access, and durable notice mechanics. It does not decide Engineering readiness, authority sufficiency, result meaning, recovery, or acknowledgement policy.
- **Deployment manager**: the root-privileged local `DeployManager` defined by `art_c4230451`. It is the sole writer of `/opt/tightbeam` deployment state and registered systemd unit files. Root privilege makes it the executor, not the authorizer.
- **Production installation**: the action defined by `art_c4230451` that makes one exact verified update restart-loadable on a production machine by publishing immutable objects and replacing `active`.
- **Mike approval identity**: the Ed25519 public key and SHA-256 key identifier in root-owned mode-`0444` `/etc/tightbeam/deploy-authority.json`. Mike retains the matching private key outside the production host.
- **Production-installation basis**: one canonical, single-use, Ed25519-signed approval envelope. It binds the approval and challenge IDs, Mike key ID, canonical host identity, deployment-root identity, fixed `production-install` action, exact update digests, verification-evidence digest, expected-active value, and ordered service-set digest.
- **Canonical host identity**: the SHA-256 of the exact 32 random bytes in root-owned mode-`0400` `/etc/tightbeam/deploy-host-id`, as defined by `art_c4230451`.
- **Deployment-root identity**: the SHA-256 of canonical JSON containing the canonical host identity and canonical absolute deployment-root path, as defined by `art_c4230451`.
- **Ordered service set**: the finite non-empty ordered entries in root-owned mode-`0444` `/etc/tightbeam/deploy-services.json`. Its identity is the SHA-256 of the canonical file bytes.
- **Engineering deployment target**: a content-bound target snapshot containing the canonical host identity, deployment-root identity, and ordered service-set digest. One target represents one machine deployment, not one gateway instance.
- **Manager intent**: the immutable, fsynced deployment-manager record that binds the transaction ID, operation, exact target, prior state, target state, applicable authority, expected-active value, evidence, and adopted rename seam before the neutral attempt call.
- **Manager acceptance fact**: one immutable audit fact in the existing `/opt/tightbeam/audit/<transaction-id>/` namespace. It binds the manager-intent digest to the committed or exact-replayed attempted-event ID, paired owner-notice wake ID, canonical neutral request digest, target digest, service-set digest, expected-active value, and adopted seam. It is not a second activation primitive or a new deployment namespace.
- **AcceptedActivationAttempt**: an unforgeable in-process value. Only `activation_client.rs` can construct it. Construction requires a committed or exact-replayed `attempted` event response, its transactionally paired owner-notice wake ID, a matching manager intent, and a durably recorded manager acceptance fact. A boolean, optional callback, log entry, caller assertion, deserialized input, or test double cannot construct it in production code.
- **Active-pointer rename entry point**: the one `renameat(temp_active, active)` operation used by managed-legacy U0 activation, later forward activation, and compensation.
- **Unit-file rename entry point**: the one deployment-manager operation that performs `renameat(temp_unit, registered_unit)` during the reviewed systemd cutover or an authorized unit replacement. A single cutover attempt binds the exact ordered unit plan, and each unit rename receives the matching accepted-attempt value.
- **Per-service result**: the durable result for one registered service, including unit state, process identity, resolved release, `/version` evidence, readiness evidence, and exact failure when present.
- **Machine observation result**: exactly one of `held`, `failed`, `pending`, or `observed`, derived from the complete set of per-service results by the precedence in Invariant E-05.
- **Raw callback failure evidence**: the complete response or local failure envelope available to the manager, plus cause, authenticated or requesting principal evidence, transaction ID, seam, target, expected-active value, request digest, and occurrence order.
- **Adopted path**: a production mutation path whose exact mutation entry point requires `AcceptedActivationAttempt` and whose real runtime fixture passes this policy.

## Assumptions

1. Execution-time `origin/main` and the remote `refs/heads/main` both resolve to `644c04064594328b5ec1c1b76301a1ac893bffc2` at 2026-08-20 23:23 PT.
2. That commit contains no `activation_events`, `activation-events-v1`, `activation-attempt`, or `AcceptedActivationAttempt` match.
3. That commit contains no `cli/src/deploy/` tree and no deploy CLI command.
4. `README.md` at that commit still directs an operator to run `npm install -g` before service restart.
5. `docs/UPGRADE.md` at that commit still contains the direct stop, checkout pull, compile, and start cycle.
6. The Linux npm overwrite, direct source-checkout upgrade, and macOS npm/LaunchDaemon paths therefore remain **NOT MECHANICALLY GATED**.
7. `art_2bc5475e` is the reviewed authority for one neutral activation primitive.
8. `art_c4230451` is the reviewed authority for Linux deployment storage, authorization records, filesystem barriers, systemd mechanics, status, recovery, rollback, GC, first cutover, and its A-01 through A-20 and A3-01 through A3-10 acceptance cases.
9. Mike's durable ruling `att_03d09931-e62d-4ed9-9d1a-ee8790188498` selects Mike as production-installation authorizer, running and serving as the observation bar, ext4 default options as the supported durability class, root-owned deployment objects and units with existing non-root gateway accounts, and one deployment per machine.
10. The manager can hold its deployment lock across policy evaluation, neutral attempt append or replay, manager acceptance recording, and the rename boundary.
11. The neutral client can preserve exact raw gateway responses or exact local transport failures in manager-owned durable evidence.
12. Marketing A-28 and Biosciences A-29 remain separate neutral-feature runtime release gates. The Engineering fixture cannot satisfy either gate.

## Invariants

**E-01 — one neutral primitive.** Engineering records declaration, authority, attempt, observation, compensation, notice, and acknowledgement through `art_2bc5475e`. The substrate contains no Engineering-specific event kind, verb, state, policy decision, or sibling fact.

**E-02 — pinned main source.** An implementation card derived from this artifact targets commit `644c04064594328b5ec1c1b76301a1ac893bffc2`. A later main commit requires a new read-only reconciliation before implementation authority can bind it.

**E-03 — authorizer and executor stay distinct.** The neutral `authorizer` and `basis` identify Mike's Ed25519 approval and exact signed envelope for production installation. The neutral `executor` identifies the root deployment manager. Root privilege alone grants no production-installation authority.

**E-04 — one exact machine target.** The target binds the canonical host identity, deployment-root identity, and ordered service-set digest. A changed member, order, unit, account, org base, endpoint, host identity, or deployment-root identity changes the target and invalidates a stale basis.

**E-05 — exclusive observation precedence.** The manager stores each per-service result. It derives exactly one machine result: `held` when registry, unit inventory, process identity, or evidence is contradictory; otherwise `failed` when at least one registered service has a terminal failure or serves the wrong release; otherwise `pending` when at least one registered service lacks a terminal result; otherwise `observed` when each registered service runs and serves the same active release under the same service-set digest.

**E-06 — fixed production platform and principals.** The production durability claim applies only to ext4 mounted with default options. Root owns deployment objects, trust files, registry files, authorization state, and registered units. Each gateway runs as its existing registered non-root account. The manager refuses an unproved filesystem or mount-option class by name before mutation.

**E-07 — accepted attempt before rename.** The active-pointer rename and unit-file rename entry points each require a matching `AcceptedActivationAttempt`. Production code exposes no alternate rename entry point that omits this type.

**E-08 — durable order.** For each adopted rename, the manager fsyncs its intent before calling the neutral attempt. It receives the committed or exact-replayed attempted event and owner-wake IDs before it records acceptance. It fsyncs the acceptance fact before it constructs `AcceptedActivationAttempt`. It passes that value before the rename. It records external truth after the rename.

**E-09 — callback failure fails closed.** A missing capability, featureless gateway, missing callback, unsupported callback, refusal, transport failure, changed replay, malformed response, mismatched event, mismatched wake, or unrecoverable response prevents `AcceptedActivationAttempt` construction and invokes zero adopted renames. The manager fsyncs raw failure evidence before returning the refusal. If evidence persistence fails, the manager still invokes zero renames and reports the evidence-persistence failure.

**E-10 — recovery does not duplicate mutation.** Before an adopted rename may have run, recovery can replay the exact neutral request and proceed only after target truth still matches the intent. After a rename may have run, recovery invokes zero additional renames, reads namespace and systemd truth, and records observation or reconciliation against the original neutral attempt.

**E-11 — coverage stays exact.** A path becomes mechanically gated only after its owned mutation entry point requires `AcceptedActivationAttempt` and its real runtime fixture passes. A row, CI receipt, source scan, later restart, or design approval does not change coverage.

**E-12 — action authorities stay separate.** Mike's production-installation approval does not authorize restart, observation, rollback, unit rollback, GC, compensation, acknowledgement, or adjudication. Each action uses the separate authority defined by deployment safety or Engineering policy.

**E-13 — notice remains evidence.** The neutral attempted event and owner wake commit together. Wake `fired` proves enqueue. Explicit owner acknowledgement records receipt. Missing acknowledgement remains visible and does not rewrite machine observation or assignment outcome.

**E-14 — source guards follow real proof.** A source guard activates only after the matching adopted path passes its real fixture. Before that pass, the guard reports `NOT ADOPTED` and the path remains **NOT MECHANICALLY GATED**.

**E-15 — cumulative prerequisites.** The Engineering runtime fixture must satisfy neutral R-09c and A-19, A-20, A-26, A-27, and A-34; deployment-safety A-01 through A-20 and A3-01 through A3-10; and this artifact's Acceptance section.

**E-16 — policy is not implementation authority.** This artifact and a later reviewed-clean verdict authorize no source, installation, deployment, restart, release, credential, live-state, or work-item mutation without a separate owner ruling.

## Architecture

### Authority and precedence

1. `art_2bc5475e` remains the sole authority for neutral substrate storage, fields, event shapes, verbs, capability, replay, lifecycle, reads, notices, and neutral acceptance.
2. `art_c4230451` remains the authority for Linux deployment mechanics and its acceptance suite, except that this artifact replaces its obsolete `origin/0.1.x` integration direction with E-02 and inserts the accepted-attempt seam defined here before both rename entry points.
3. This artifact is the complete Engineering consumer policy. It supersedes the consumer portions of `art_16df51ca` and `art_44b99337`. A builder does not layer either prior consumer artifact onto this one.
4. `0.1.8`, `0.1.x`, `ac8651dcb104f312da1c67e0cb7b1abebc640b2b`, and `378807eabb39cecc25ea801494053f8aa20feafa` remain historical evidence only.

### Exact main source map

| Object at execution-time main | Git object ID | Policy use |
|---|---|---|
| root tree | `54f9c06efc8bdbb922b0e0ddba812c5e49168724` | complete source identity |
| `README.md` | `992136f271b72000888cefe6f0a90f8596b91f9b` | unsafe npm/Linux/macOS path census |
| `docs/UPGRADE.md` | `cb9ab47cf8fbd88bff926bfdb686449b684632c5` | unsafe source-checkout path census |
| `cli/src/args.rs` | `6e422e1c728607bd992638aff0ff22e42b64b63d` | future local command parse seam |
| `cli/src/main.rs` | `eebb7aa4207bba1c325e8ece13bc9aadb98a1ef6` | future local command route seam |
| `cli/src/dispatch.rs` | `6faac17045b5037077cf1dd6298b21bf8fdfe822` | neutral gateway-client seam only |
| `lib/tightbeam/wire/router.ex` | `7bebec5c5317f77bd78ff19c41d07c4df8a7d4e5` | future neutral wire verbs and capability |
| `lib/tightbeam/schema.ex` | `dd6415406ab273861366b6f05c0e22820e587780` | future additive neutral table |
| `packaging/assemble.sh` | `0c900431ea7e9352158386a0b3899c450fa56e20` | prepared-input evidence producer |
| `packaging/finalize-artifact.sh` | `2b18ce9cce73af7139d8859c48023e7eb368ec43` | prepared-input evidence producer |
| `.github/workflows/release-candidate.yml` | `c033c35223734871a26b591985af4e5230932a36` | verification evidence producer, not authority |

### Engineering operation classification

The adapter accepts four Engineering activation classes:

1. `managed-legacy-u0-activation`: import the exact verified supported npm bytes as a managed legacy generation and perform the first `active` rename with `expected_active = virgin:<deployment-root-identity>`.
2. `release-generation-activation`: replace `active` with one exact verified generation.
3. `release-generation-compensation`: declare a new neutral activation linked with `compensates`, select an exact retained observed-known-good generation, and use a fresh action basis.
4. `service-manager-cutover`: replace the registered systemd units with the reviewed managed unit plan that selects the already active managed legacy generation.

Package receipt, extraction, verification, inactive release publication, inactive generation construction, release-candidate proof, tag creation, and GitHub Release creation are preparation or evidence production. They are not activation attempts because they do not change restart-loadable or systemd-effective bytes.

U0 is an Engineering production activation, but it is not a production installation of an update: it selects byte- and provenance-equivalent legacy bytes already selected by the registered units. U0 uses the separate first-cutover authority from `art_c4230451` and does not consume Mike's production-installation approval. A U0 candidate whose managed bytes differ from the verified legacy bytes refuses under deployment-safety legacy-byte exclusion; the adapter does not widen U0 into an update installation.

### Neutral field mapping

| Neutral field | Engineering value |
|---|---|
| `rootAssignmentId` | the open Engineering implementation or fixture assignment on this work item |
| `ownerUserId` | the current work-item owner captured at declaration |
| `domain` | `engineering` |
| `correlationKey` | the stable manager transaction ID |
| `preparedInput` | a content-bound release manifest, managed-legacy manifest, retained-generation manifest, or complete ordered unit-plan manifest for the exact operation |
| `target` | a `ResourceRef` to the Engineering deployment-target snapshot defined below |
| `authorizer` | `{namespace: engineering.production-install-authorizer, id: <Mike-key-id>}` for production installation; an action-specific Engineering identity for a separate non-installation action |
| `basis` | the content-bound production-installation approval envelope or separate action-specific basis |
| `decision` | `{namespace: engineering.production-install, code: approved}` for an accepted production-installation basis; Tightbeam does not interpret it |
| `executor` | `{namespace: engineering.deploy-manager, id: root@<canonical-host-identity>}` |
| `externalAttempt` | `{namespace: engineering.deploy-attempt, id: <manager-transaction-id>, sha256: <manager-intent-digest>}` |
| `targetStateBefore` | the content-bound virgin or active machine snapshot, including service-set digest and per-service state |
| `result` | one Engineering aggregate code: `machine-held`, `machine-failed`, `machine-pending`, or `machine-observed` |
| `targetStateAfter` | the content-bound post-attempt machine snapshot |
| `outputs` | manager receipt, active-generation manifest, per-service result bundle, restart receipt, recovery evidence, and retained prior-known-good reference when present |
| `evidence` | one content-bound observation bundle containing each per-service result and the exclusive aggregate derivation |
| compensation | a new declaration with `prior.relation=compensates`, an exact retained target, and fresh action authority |

For U0, `targetStateBefore` binds the deployment-root identity, absent `active`, permanent activation-history result, exact unresolved-U0-intent count, service-set digest, and verified old unit and npm digests. The adapter does not substitute `null`, an absent-generation guess, or a synthetic generation ID for `virgin:<deployment-root-identity>`.

The canonical Engineering deployment-target snapshot is RFC 8785 canonical JSON with exactly these keys:

```text
schema: engineering-deployment-target/v1
canonicalHostIdentity: <64 lowercase hex>
deploymentRootIdentity: <64 lowercase hex>
serviceSetDigest: <64 lowercase hex>
```

The neutral target uses namespace `engineering.deployment-target`, ID `machine:<canonical-host-identity>:root:<deployment-root-identity>`, and the SHA-256 of those canonical bytes. A target mismatch refuses before a neutral attempt is selected.

### Production-installation authority mapping

The Engineering policy accepts one production-installation authority event only when its `authorizer` equals `{namespace: engineering.production-install-authorizer, id: <Mike-key-id>}`, its `basis` equals `{namespace: engineering.production-install-approval, id: <approval-id>, sha256: <canonical-envelope-digest>}`, and its `decision` equals `{namespace: engineering.production-install, code: approved}`. The Mike key ID comes from the current production trust policy. The basis digest is the SHA-256 of the exact canonical signed approval envelope.

Before selecting that authority event for `activation-attempt`, the adapter verifies:

1. the release, payload, provenance, compatibility, and side-path boot evidence required by deployment safety;
2. the current canonical host identity, deployment-root identity, service-set digest, and expected-active value;
3. the fixed `production-install` action;
4. the challenge is open and its state matches the signed envelope;
5. the signature validates under the current Mike Ed25519 key;
6. the update and verification-evidence digests match the prepared input;
7. the approval remains unconsumed, unsuperseded, and unrevoked; and
8. the manager has fsynced the one-use consumed fact before the first production-installation mutation.

The production binary accepts no test key. A test-only binary can accept one separate e2e key only for a temporary fixture outside `/opt/tightbeam`, `/etc/tightbeam`, and production systemd unit paths. The test-only binary refuses a production path by name.

### Accepted-attempt construction and rename APIs

`cli/src/deploy/activation_client.rs` owns `AcceptedActivationAttempt`, its private fields, and its only production constructor. The type is not deserializable, cloneable across transactions, constructible from a boolean, or exposed through CLI or wire input.

The value binds:

- manager transaction ID;
- operation class;
- manager-intent digest;
- neutral activation ID;
- committed attempted-event ID;
- paired owner-notice wake ID;
- canonical neutral request digest;
- Engineering target digest;
- expected-active value;
- service-set digest;
- adopted seam: `active-pointer` or `unit-file-set`; and
- manager acceptance-fact digest.

`cli/src/deploy/fs.rs` accepts this value at the active-pointer rename function and verifies that its transaction, target, expected-active value, and seam match the held manager state.

`cli/src/deploy/systemd.rs` accepts this value at the unit-file rename function and verifies that its transaction, target, ordered unit-plan digest, service-set digest, and seam match the held cutover state. Each unit rename in that cutover receives the same value and the exact unit-plan member index.

`cli/src/deploy/mod.rs` remains the only public deployment mutation facade. `engineering_policy.rs` owns Engineering readiness, authority, target, result, recovery, notice, and acknowledgement rules. `activation_client.rs` calls the neutral verbs and owns the accepted-attempt type and constructor. `model.rs` owns the manager records. No module outside `cli/src/deploy/` writes deployment state.

### Exact durable order

For active-pointer activation, while holding the deployment lock, the manager executes this order:

1. read and validate current target truth;
2. validate the action-specific Engineering policy and Mike approval when the action is production installation;
3. fsync the one-use approval-consumption fact when applicable;
4. publish and validate inactive immutable release and generation objects;
5. write and fsync the immutable manager intent;
6. append or exact-replay neutral `activation-attempt` with the manager transaction as `externalAttempt`;
7. receive the committed attempted-event ID and transactionally paired owner-wake ID;
8. write, fsync, and re-read the immutable manager acceptance fact;
9. construct `AcceptedActivationAttempt` from the verified response and acceptance fact;
10. create and fsync the temporary `active` link;
11. call the typed active-pointer rename entry point with the accepted-attempt value;
12. fsync the deployment-root directory and validate `active` by re-read;
13. record the manager result and each later per-service result;
14. append neutral `activation-observe`, or append an indeterminate observation followed by later reconciliation; and
15. expose the attempt and observation notices for explicit owner acknowledgement.

For systemd unit cutover, steps 1 through 9 use the complete ordered unit-plan manifest as prepared input and bind `unit-file-set` as the seam. The manager then writes each sibling temp unit, fsyncs it and its directory, and passes the same accepted-attempt value plus the member index to each unit rename. It records each on-disk result before it advances to the next unit. Daemon reload, separate restart authority, ordered restart, per-service observation, and aggregate observation follow the reviewed deployment-safety order.

The check and action at each rename entry point form one typed function call. The entry point revalidates the accepted value against the held transaction immediately before it invokes `renameat`.

### Refusal and recovery

Before returning a callback refusal, the manager writes raw callback failure evidence into the root-owned deployment journal, fsyncs the file and parent directory, and records the evidence digest in the transaction result. A raw gateway envelope remains byte-preserved. A local error record preserves the exact operation, error class, cause chain, principal evidence, request digest, and transport state. Neither record is parsed to infer a successful attempt.

| Recovery boundary | Required behavior |
|---|---|
| intent durable; neutral attempt absent | replay or append the exact neutral request; invoke zero renames until a committed response returns |
| neutral attempt committed; response lost | exact replay returns the original event and wake IDs; changed replay refuses; invoke zero renames before the replayed response |
| acceptance fact durable; active-pointer rename proven absent | revalidate target truth and reconstruct the accepted-attempt value from the exact replay plus acceptance fact; invoke exactly one active-pointer rename |
| acceptance fact durable; all planned unit-file-set member renames proven absent | revalidate target truth and the complete ordered unit plan; reconstruct the accepted-attempt value from the exact replay plus acceptance fact; invoke the complete ordered per-member rename sequence and record each on-disk result durably before the next rename |
| rename may have run | invoke zero additional renames; read active-pointer or unit truth; record observation or indeterminate evidence against the original attempt |
| pointer, unit, registry, process, or evidence truth contradicts intent | derive `held`; preserve involved objects; require explicit human adjudication through a separate authority path |
| raw-failure evidence cannot become durable | invoke zero renames; return the evidence-persistence failure and preserve the unresolved intent |

Recovery does not create a second neutral attempt, synthesize success from an intent, infer failure from elapsed time, or use a later restart as proof of pre-rename gating.

### Observation projection

The observation bundle stores the ordered service-set digest, active release digest, one result object for each registry entry, and the machine result. It retains a `pending` result for a service whose planned restart did not run after an earlier failure. The aggregate calculation applies E-05 to the set as a whole; it does not discard per-service results.

The neutral `result` carries the aggregate Engineering code. The neutral `outputs` includes the content-bound per-service result bundle. Tightbeam records both without interpreting them. `observed-known-good` is an Engineering and deployment-manager state, not a neutral derived state.

### Source guards and coverage

At execution-time main:

| Path | Policy state |
|---|---|
| Linux npm package overwrite | **NOT MECHANICALLY GATED** |
| Linux managed-generation activation | reviewed design; no implementation |
| Linux first systemd cutover | reviewed design; no implementation |
| direct source-checkout upgrade | **NOT MECHANICALLY GATED** |
| macOS npm/LaunchDaemon | **NOT MECHANICALLY GATED**; no reviewed launchd contract |
| release-candidate and GitHub Release proof | evidence producer; not an activation gate |

After the Linux real runtime fixture passes, a separately authorized migration can replace the supported Linux npm-overwrite and production source-checkout instructions, install the managed unit template, and activate exact source guards. The guards match owned production entry points and remedies. They do not match ordinary development, package creation, inactive staging, simulators, historical fixtures, or non-production roots.

### Ordered implementation cards after separate owner authorization

1. Implement the reviewed neutral activation primitive on main without Engineering vocabulary.
2. Implement the reviewed Linux deployment-safety manager on main, including the sealed accepted-attempt requirements at both rename entry points.
3. After Cards 1 and 2 expose their reviewed seams, implement `engineering_policy.rs` and `activation_client.rs`.
4. Run the Linux real-runtime proof on a disposable ext4-default systemd host with a real package, gateway, wake pipeline, manager, crash/replay matrix, callback mutants, U0, forward activation, service observation, aggregate observation, and compensation.
5. After Card 4 passes, migrate the supported Linux paths and activate exact guards.
6. If the product later claims production launchd coverage, first produce and independently review a macOS cutover, restart, recovery, rollback, and observation contract; then implement and prove that separate lane.

Cards 1 and 2 can run independently after separate owner authorization. Card 3 depends on both. Card 4 depends on Card 3. Card 5 depends on Card 4. Card 6 remains outside Linux MVP scope.

## Acceptance

**C-01 — source authority.** Given this artifact and a repository object database, when the reviewer resolves the pinned main commit and each object in the source map, then the commit equals `644c04064594328b5ec1c1b76301a1ac893bffc2` and each object ID matches. A moved `refs/heads/main` does not silently change this artifact's source authority.

**C-02 — neutral boundary.** Given the implementation's substrate vocabulary, when the neutral self-gate runs, then it contains the one `activation_events` table and fixed neutral verb family from `art_2bc5475e`, with no Engineering or deploy-specific sibling fact, verb, event kind, derived state, or policy evaluator.

**C-03a — production authority mapping.** Given a valid Mike-signed production-installation envelope, when the adapter maps the authority event, then `authorizer`, `basis`, `decision`, `executor`, and `externalAttempt` equal the closed values in the Neutral field mapping table.

**C-03b — privilege is not authority.** Given a root manager without that authority event and basis, when it requests production installation, then the manager invokes zero installation mutations.

**C-04 — test-key confinement.** Given the production binary, when a test key is offered through a file, environment value, command argument, org base, deployment root, release payload, or approval envelope, then verification refuses it. Given the test-only binary and a target under `/opt/tightbeam`, `/etc/tightbeam`, or a production unit path, then it refuses before mutation.

**C-05 — exact target.** Given one target snapshot, when host identity, deployment-root identity, service member, service order, unit, account, org base, endpoint, or service-set bytes change, then the target digest changes and a basis bound to the prior target refuses before the neutral attempt.

**C-06 — aggregate precedence.** Given four ordered service-result fixtures, when the projector runs, then: a contradiction plus any other results yields `held`; absent contradiction, a failure plus pending results yields `failed`; absent contradiction or failure, a missing terminal result yields `pending`; and only successful results for each registered service on one active release and service-set digest yield `observed`.

**C-07 — per-service preservation.** Given a three-service run where service one succeeds, service two fails, and service three remains pending, when status and the observation bundle are read, then all three results remain present and the aggregate is `failed`.

**C-08 — platform refusal.** Given ext4 mounted with default options, when the durability preflight runs, then the supported filesystem check passes. Given another filesystem or a non-default ext4 mount-option class, then the manager names the unproved class and invokes zero deployment mutations.

**C-09 — principal permissions.** Given a registered non-root gateway account, when it runs the selected release, then it can write its org base and cannot write deployment objects, trust files, registry files, authorization state, or registered units. Given manager-created deployment objects and units, then their recorded owner is root. No dedicated deploy user exists.

**C-10a — active-pointer compile gate.** Given a compile-fail API fixture, when code calls the active-pointer rename without `AcceptedActivationAttempt` or tries to construct that value through deserialization, a boolean, public fields, or a caller assertion, then the fixture fails to compile.

**C-10b — active-pointer runtime gate.** Given a valid accepted value from another transaction, target, expected-active value, service set, or `unit-file-set` seam, when code calls the active-pointer entry point, then it refuses before `renameat`. Given a matching value, the entry point revalidates it immediately before one rename.

**C-11a — unit-file compile gate.** Given a compile-fail API fixture, when code calls the unit-file rename without `AcceptedActivationAttempt` or tries to construct that value outside `activation_client.rs`, then the fixture fails to compile.

**C-11b — unit-file runtime gate.** Given a valid accepted value with another transaction, target, ordered unit-plan digest, service-set digest, member index, or `active-pointer` seam, when code calls the unit-file entry point, then it refuses before `renameat`.

**C-12 — successful durable order.** Given an instrumented active-pointer activation, when it succeeds, then the trace orders manager-intent fsync before neutral attempt commit or replay, response receipt before acceptance-fact fsync, acceptance-fact fsync before accepted-value construction, accepted-value validation before `renameat`, and observation after rename. The mutation spy records zero rename calls before accepted-value validation and exactly one first call after it.

**C-13 — unit-set durable order.** Given a two-service cutover, when it succeeds, then one accepted value binds the complete ordered plan, each unit rename receives its correct member index, each on-disk result becomes durable before the next rename, and the manager preserves both per-unit results before reload or restart.

**C-14 — callback refusal.** Given missing capability, a featureless gateway, missing callback, unsupported callback, refusal, transport failure, changed replay, malformed response, event mismatch, or wake mismatch, when the manager reaches either adopted seam, then it records raw failure evidence and the mutation spy records zero renames.

**C-15 — evidence-persistence failure.** Given a callback failure and injected failure at raw-evidence file write, file fsync, or directory fsync, when the manager refuses, then the mutation spy records zero renames and the returned result names the evidence-persistence boundary.

**C-16 — lost response replay.** Given a committed attempted event whose response is lost, when recovery uses the same principal, idempotency key, and canonical request, then the neutral service returns the original event and wake IDs. For the active-pointer seam, the mutation spy records zero calls before that replay response and exactly one active-pointer rename after target revalidation. For the unit-file-set seam with all planned member renames proven absent, the mutation spy records zero calls before that replay response and then records the complete ordered per-member rename sequence after target and unit-plan revalidation, with each correct member index and each on-disk result durable before the next rename.

**C-17 — post-rename recovery.** Given a crash after either rename may have run and before observation, when recovery runs, then it invokes zero additional renames, reports namespace and systemd truth, and appends one observation or indeterminate record against the original attempt.

**C-18 — U0 mapping.** Given a validated virgin root, when the adapter declares managed-legacy U0, then `expected_active` equals `virgin:<deployment-root-identity>`, `targetStateBefore` binds the required virgin and legacy evidence, and the active-pointer entry point requires a matching accepted attempt before the first `active` rename.

**C-19 — action separation.** Given a valid Mike production-installation approval, when restart, rollback, unit rollback, GC, compensation, acknowledgement, or adjudication is requested without its separate authority, then the requested action refuses without consuming or widening the installation approval.

**C-20 — coverage census.** Given execution-time main before implementation, when the coverage report runs, then Linux npm overwrite, direct source-checkout upgrade, and macOS npm/LaunchDaemon report **NOT MECHANICALLY GATED**. A design row, CI receipt, source scan, later restart, or successful unrelated fixture leaves those labels unchanged.

**C-21 — guard activation.** Given a Linux path whose real fixture has not passed, when its source guard runs, then it reports `NOT ADOPTED` and does not deny ordinary development or staging. Given a passed real fixture and separate migration authority, then the exact retired production entry point refuses with the managed-path remedy.

**C-22 — real Linux proof.** Given a real package, real gateway, real wake pipeline, real deploy manager, and disposable ext4-default systemd host with at least two registered services, when the fixture runs U0, forward activation, lost-response replay, callback mutants, crash boundaries, per-service failure and pending cases, observation, and compensation, then it records raw real responses, ordered mutation traces, target truth, systemd results, owner notices, acknowledgements, artifact ID, and SHA-256. A hand-written response, mock-only transcript, or static design fixture does not pass.

**C-23 — cumulative suites.** Given an implementation candidate, when release acceptance runs, then neutral R-09c and A-19, A-20, A-26, A-27, A-34; deployment-safety A-01 through A-20 and A3-01 through A3-10; and this artifact's C-01 through C-09, C-10a, C-10b, C-11a, C-11b, and C-12 through C-22 pass. Marketing A-28 and Biosciences A-29 cite their own immutable runtime artifacts before the neutral feature can receive a release pass.

**C-24 — no implementation authority.** Given this artifact or its reviewed-clean verdict without a later owner ruling, when a session requests a source edit, implementation card, pin, install, deploy, restart, release, credential mutation, live-state mutation, or work-item disposition, then the request remains unauthorized.

## Open Questions

None. Mike's rulings and the six owner-authorized replacements close the load-bearing policy choices. A later main commit, a macOS production-coverage claim, or a request to vary filesystem, principal, target, threshold, or service-set policy requires a new owner ruling and a new spec amendment; it is not an implementation detail.
