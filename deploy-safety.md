# Tightbeam deploy safety

Status: post-policy canonical amendment; spec-ready for independent policy review; implementation remains unauthorized until review and pin  
Work item: `wi_65477046-0932-4973-b19f-17822625d0f8`  
Historical source baseline: main at `ac8651dcb104f312da1c67e0cb7b1abebc640b2b`  
Current-org integration branch: `origin/0.1.x`; main receives changes only by Mike-authorized cherry-pick, per `att_e41a5daf-0146-439d-b3dd-8b58c0a5061d`  
Consolidates: `art_92b4b35a` (`5f88a9b9301a7fd4b3680905a98fdd9d7c0a98a0a8e4b0acc2d3cb9c77f1d9f8`), `art_297d39a8` (`8773dc9015b8aeee75bbc56101cd48d16da4b52e35747ed8e19a5d67f0a0327b`), and `art_991853fe` (`6e9723023c3ff058a997de5281d9044159cbfd3ee2cce8341b910117acf46623`)  
Baseline reviewed-clean evidence: `att_c60afa8a-27e9-44ba-8385-e4b389c68e9c`, `att_c75924b2-a002-4ea6-aea2-66ab19e7a5af`, `att_985db8e6-86ed-4789-bc2d-97e0af8902c1`, and exact-SHA review `att_d295db05-425b-4a38-a0c4-7e4bbec2f4a3`  
Post-OQ authority: Mike approved `att_03d09931-e62d-4ed9-9d1a-ee8790188498`; Mike closed the residual authorization and machine-service policy holes in `att_6f020416-aa7b-40ea-abcf-ec3eabd68853`; Mike narrowed the approval scope to production installation in `att_de7e1be6-64bb-4c8a-abdd-8e68b9f89a18`

## Goal

Provide a supported Linux/systemd deployment path in which:

1. Only exact release bytes that passed verification and received Mike's one-time production-installation approval become restart-loadable on a production machine.
2. The active pointer changes atomically and remains recoverable after process death or power loss.
3. After managed-unit cutover, a prior observed-known-good release remains available for an explicitly authorized atomic rollback. During first cutover, preserved npm bytes and the old units provide the separately authorized legacy rollback path.
4. Operators can distinguish running bytes, restart-loadable bytes, staged candidates, transaction state, and rollback eligibility.
5. The first migration from the npm-owned service path cannot make newer product bytes loadable while the service-unit seam is changing.

This spec replaces the split reviewed design authority with one canonical document against the historical source baseline. It does not assert that an implementation exists or that a release may proceed.

The closure adds a deployment manager because deleting the supported upgrade surface would strand existing service installations, while accepting the current direct-overwrite path would preserve the reported safety defect.

## Non-Goals

1. This spec does not authorize a release, deployment, activation, restart, rollback, service-unit replacement, database migration, or live-state mutation.
2. This spec does not change Tightbeam product behavior, agent behavior, work-item semantics, or the durable org data model.
3. This spec does not provide a macOS/launchd activation path. Current-main may continue to build Darwin packages, but this deployment contract applies only to Linux/systemd hosts.
4. This spec does not provide zero-downtime deployment. First cutover may use a named maintenance outage.
5. This spec does not make a failed health check authorize rollback.
6. This spec does not copy an old release over a live tree as rollback.
7. This spec does not infer compatibility for an unstamped, differently stamped, or multiply stamped database.
8. This spec does not make the gateway process own deployment mutations. Deployment must remain usable while the gateway is stopped.
9. This spec does not delete the existing npm tree or old units until the first-cutover rollback window has closed under explicit authority.
10. This spec does not replace release-candidate review. It consumes its immutable evidence.

## Terms

- **Deployment root**: `/opt/tightbeam`, the root-owned privileged filesystem namespace that contains the lock, challenges, authorization-use facts, staging area, immutable releases, generations, evidence, authorization copies, intents, audit facts, trash, and `active` pointer.
- **Canonical host identity**: the SHA-256 of the exact 32 random bytes in root-owned mode-`0400` `/etc/tightbeam/deploy-host-id`. Supported setup creates this file once from the operating-system cryptographic random source. The manager reads it but cannot create, replace, or repair it. A missing, malformed, or changed value after deployment history exists puts deployment in `held` state.
- **Deployment-root identity**: the SHA-256 of canonical JSON containing the canonical host identity and canonical absolute deployment-root path. The same host/path tuple produces the same identity across crashes; a different host or path cannot satisfy a virgin authorization.
- **Org base**: the directory selected by `TIGHTBEAM_BASE_DIR`, then `TIGHTBEAM_HOME`, then the product fallback. It contains durable org state and remains outside the deployment root.
- **Release manifest**: canonical immutable JSON that binds tarball digest, source commit, version, target platform, build identity, verification evidence, compatibility decision, and the complete payload manifest. Its identity is the SHA-256 of its canonical bytes, stored outside those bytes; the document does not contain its own digest.
- **Payload manifest**: the sorted finite list of payload entries. Each entry contains path, type, mode, size, and SHA-256. The list includes the CLI and gateway release tree.
- **Release**: an immutable payload tree at `releases/sha256-<release-manifest-digest>/tightbeam` that validates against one release manifest.
- **Generation**: an immutable manifest plus a manager-created relative `root` link to one release. Its manifest names its prior generation and the evidence that justified its creation.
- **Active pointer**: the manager-created relative symlink `/opt/tightbeam/active`. Its durable directory entry is the sole activation commit truth.
- **Running generation**: the generation whose release root the current gateway process resolved at exec time. Before first cutover this value is `legacy-process:<absolute-root-and-digest>`.
- **Restart-loadable release**: the fully validated generation selected by `active`; before U0 commits, the exact verified npm release selected by each still-effective registered legacy unit. Conflicting legacy release digests put first cutover in `held` state.
- **Prior observed-known-good generation**: a retained generation with one machine observation fact that binds the service-set digest and proves that each member of that finite service set restarted into the generation and reached its running, serving checks. Offline verification or one service result alone does not grant this state.
- **Deploy transaction**: one identified attempt that advances through the state machine and owns one immutable intent and audit history.
- **Expected active**: either `generation:<generation-id>:<digest>` or `virgin:<deployment-root-identity>`. `generation` names the exact active generation observed under the deploy lock. `virgin` asserts that `active` is absent, no generation has ever been active in this deployment root, and no other first-cutover intent exists. A different later value makes the authorization stale.
- **Virgin deployment root**: a validated deployment root in which `active` is absent, no immutable activation-history fact exists for its deployment-root identity, no generation has ever been selected, and at most the one unresolved U0 intent being recovered exists. Activation-history facts are permanent and GC-ineligible. An absent pointer outside this state is invalid, not virgin.
- **Production installation**: the activation on a production machine that makes one exact verified update restart-loadable by publishing its immutable release and generation and replacing `active`. Receiving, staging, and verifying a candidate do not install it. Ordinary development and test work are not production installation. Restart, observation, rollback, unit rollback, and GC are separate operations and do not consume Mike's production-installation approval.
- **Production trust policy**: the root-owned mode-`0444` canonical JSON file `/etc/tightbeam/deploy-authority.json`. It names one Ed25519 public verification key and its SHA-256 key identifier. Mike keeps the matching private signing key outside each production host. The deployment manager reads this file but cannot change it. A separate local root-maintenance ceremony authorized by Mike installs, revokes, or rotates the key; removing a key makes each unused production-installation approval from that key invalid.
- **Service registry**: the root-owned mode-`0444` canonical JSON file `/etc/tightbeam/deploy-services.json`. It contains one ordered finite non-empty list. Each entry names one systemd unit, its expected non-root service account, org base, and loopback `/version` endpoint. The service-set digest is the SHA-256 of the canonical file bytes. A production-installation approval binds this digest. Readiness uses the fixed active-release `tightbeam doctor --json` command with that entry's org base; the registry cannot supply an executable or command string.
- **Registered service**: one entry in the service registry. During managed operation, its effective systemd `ExecStart` resolves through this machine's `/opt/tightbeam/active`. During virgin first cutover, it may resolve the exact verified legacy npm path until U2 replaces its unit. The manager refuses a missing or duplicate entry. It also refuses when an installed or loaded Tightbeam unit resolves through the managed active path or the verified legacy path but is absent from the registry.
- **Production-installation challenge**: an immutable manager-created record with a cryptographically random 256-bit nonce. It binds canonical host identity, deployment-root identity, the fixed `production-install` action, exact update digests, verification digest, expected active, and service-set digest. One open challenge exists for one production-installation request. A durable consumed, superseded, or revoked fact closes it.
- **Production-installation approval**: canonical JSON containing a challenge-bound `production-install` payload and an Ed25519 signature over that payload. The immutable record names schema, approval ID, Mike key ID, challenge ID, canonical host identity, deployment-root identity, action, exact update digests, verification digest, expected active, and service-set digest. Mike is the sole signer for production installation. The manager accepts the record once and fsyncs its consumed fact before the first installation mutation. Challenge state and expected-active state provide validity bounds; approval acceptance does not use wall-clock time. An e2e runner may sign the same shape with a separate test key injected into a test-only binary for a temporary fixture outside `/opt/tightbeam`; this fixture validates the mechanism but does not require Mike's approval. A production binary contains no test key. Each Gibson production-installation approval binds Gibson's canonical host identity and therefore supplies Mike's explicit permission for that one installation.
- **Deploy principal**: the root-privileged local process that owns the root-owned deployment root and unit-file mutations. No dedicated deploy user exists. Root privilege does not itself grant authorization.
- **Service account**: the existing non-root `User=` and `Group=` in one registered unit. It may execute releases and write that entry's org base, but it may not mutate deployment, trust, registry, authorization, or unit state.
- **Activation intent**: a fsynced immutable record written before pointer replacement. It binds transaction, target, prior, authorization, verification evidence, compatibility, and expected active.
- **Observation**: post-restart evidence for one registered service. It proves that systemd reports the unit active/running, the main process resolves the exact active release, the registered loopback `/version` endpoint returns the active version and build, and the fixed active-release `tightbeam doctor --json` command succeeds for that service's org base when the manager invokes it as the registered service account. A machine observation binds one update and one service-set digest and contains one successful service observation for each registry entry. Observation never changes `active`, and it adds no numeric threshold or wait.
- **First cutover**: the two-transaction migration that first imports the currently supported npm bytes as a managed legacy generation, then atomically changes each registered systemd unit to resolve that same legacy generation.
- **Held**: a state in which the manager reports the exact contradiction and accepts no deployment mutation, service restart, or GC action until new explicit authority resolves it. Read-only status remains available.

## Assumptions

1. Commit `ac8651dcb104f312da1c67e0cb7b1abebc640b2b` is the historical source baseline for this consolidation. The inspected Git object exists locally and identifies `Seed recovery baseline when recurrence opens false`. Current-org integration targets `origin/0.1.x`; main receives changes only by Mike-authorized cherry-pick.
2. The supported target in this spec is Linux x86_64 with one or more system units under `/etc/systemd/system`. The default unit is `tightbeam.service`; the service registry names the exact supported set on one machine.
3. Current-main documents a non-root service `User=` and `Group=`, `Restart=on-failure`, and an npm-owned `ExecStart` in `README.md:411-454`.
4. Current-main still documents `npm install -g` before restart in `README.md:85-118`, and `docs/UPGRADE.md:1-37` still describes stop, mutable code swap, and start.
5. Current-main `packaging/assemble.sh:26-45` creates one npm tarball; `packaging/finalize-artifact.sh:1-11` publishes it only after version smoke. Neither file produces a complete payload manifest.
6. Current-main `scripts/verify_release_candidate_manifest.py:18-27,107-148,171-225` binds source, workflow, package digests, platforms, and toolchains in `tightbeam-release-candidate-proof/v1`. It does not bind a per-payload path/type/mode/size/digest manifest or an activation authorization.
7. Current-main `packaging/tightbeam-gateway:9-18,70` resolves the installed package directory and execs the release inside that directory.
8. Current-main stamps the database shape as `model-identity-v1` and refuses missing, different, or multiple incompatible stamps in `lib/tightbeam/schema.ex:35-38,902-968`.
9. The org base can remain at its effective pre-cutover path while executable bytes move into the deployment root.
10. Linux supplies atomic same-filesystem rename and directory fsync semantics. The production durability claim supports only ext4 mounted with default options. The manager refuses each other filesystem or mount-option class by name as unproven.
11. The current 5795df1 incident is mitigated by owner evidence `att_62853ad7-468b-4435-ad33-3193f4f465f8`. The general supported-path defect remains.
12. The release-candidate workflow and GitHub artifact store are evidence producers, not activation authorities.
13. Current-main supports multiple gateway instances on one machine through distinct ports, node names, and org bases in `README.md:183-205`. This deployment contract provides one deployment root and one deployment scope per machine, not one per gateway instance. The service registry enumerates those instances as one finite machine service set.

## Invariants

- **I-01 — verified-before-loadable**: A staged or verification-failed release cannot change `active`, a registered unit, the npm tree, or a running process.
- **I-02 — approved-before-production-installation**: The production manager accepts activation of an update only after verification and a valid Mike-signed, unconsumed production-installation approval bound to the exact host, candidate, verification evidence, expected-active value, `production-install` action, and service-set digest.
- **I-03 — one commit truth**: The durable `active` directory entry is the sole truth for release activation. An intent or audit row cannot override it.
- **I-04 — immutable content**: A release, generation, intent, authorization copy, and audit fact cannot be edited after publication. A name collision triggers full verification or refusal; it never merges trees.
- **I-05 — one mutation seam**: One local deployment manager owns deployment-root and unit mutations. Activation, rollback, GC, and first cutover take the same exclusive lock.
- **I-06 — same-filesystem atomicity**: Pointer activation and each unit-file replacement use same-filesystem rename. Device mismatch or `EXDEV` refuses without copy/delete fallback.
- **I-07 — prior-good survival**: A non-bootstrap activation protects the prior observed-known-good generation, both releases, the intent, authorization, and evidence before pointer mutation begins. U0 instead protects the old npm tree, old units, and managed legacy generation until cutover rollback authority expires.
- **I-08 — separate authority**: Activation, restart, rollback, first-cutover unit mutation, unit rollback, and GC are distinct actions. Authority for one action does not grant another.
- **I-09 — service immutability**: A service account cannot write the trust policy, host identity, service registry, a path component from `/opt/tightbeam` through the selected executable, the lock, manifests, generations, releases, challenges, authorization-use facts, intents, audit facts, or a registered unit file.
- **I-10 — confined paths**: Filesystem mutation uses directory descriptors with beneath/no-follow resolution. Only manager-created relative `generation/root` and `active` symlinks are accepted.
- **I-11 — deterministic recovery**: Recovery classifies observed namespace truth as virgin, old, target, unrelated-valid, or invalid. It does not infer a desired result from an absent status row.
- **I-12 — no automatic judgment**: A timeout, health failure, missing audit row, process restart, or orphan object does not authorize activation, rollback, restart, unit change, or GC.
- **I-13 — truthful status**: Status reports running, restart-loadable, transaction, audit, next authority, GC hold, service-set digest, each registered service result, and the machine observation result as separate fields.
- **I-14 — compatibility before mutation**: Unsupported schema or state compatibility refuses before activation or rollback.
- **I-15 — legacy-byte exclusion**: First cutover changes registered units only while `active` selects byte/provenance-equivalent legacy bytes. A newer release cannot activate until machine-wide unit cutover is observed complete.
- **I-16 — durable state separation**: Deployment never relocates or rewrites the org base as part of release activation.
- **I-17 — one-use production-installation approval**: The manager fsyncs one consumed fact before the first installation mutation authorized by that record. A consumed, superseded, revoked, wrongly signed, wrong-host, wrong-action, wrong-update, wrong-state, or wrong-service-set record grants no production installation.
- **I-18 — complete machine observation**: A generation becomes observed-known-good only when one machine observation for the exact service-set digest contains a successful observation for each registry entry. One missing, failed, unknown, or wrong-release service keeps the generation unobserved and keeps the prior observed-known-good generation protected.

The design makes invalid state transitions unrepresentable with action-specific authorization types and typed transaction states. Runtime filesystem truth still requires deterministic validation rails at each mutation boundary.

## Architecture

### Historical source map

| Concern | Current seam at `ac8651d` | Required change owner |
|---|---|---|
| Unsafe install and service guidance | `README.md:85-118,411-454`; `docs/UPGRADE.md:1-37` | Documentation owner replaces direct-overwrite upgrade instructions in the implementation change set before the A-01 release gate runs. |
| Package assembly | `packaging/assemble.sh`; `packaging/finalize-artifact.sh`; `packaging/version-smoke.sh`; `packaging/package.json` | Packaging owner emits the canonical payload manifest beside the tarball from real assembled bytes before final artifact publication. The proof bundle carries both; the payload manifest is not self-listed inside the payload tree. |
| Candidate proof | `scripts/verify_release_candidate_manifest.py`; `.github/workflows/release-candidate.yml`; `docs/RELEASE_TRAIN.md` | Release-evidence owner advances the proof schema and binds payload-manifest and verification-evidence digests without turning CI into deployment authority. |
| Local CLI | `cli/src/main.rs`; `cli/src/args.rs`; `cli/src/dispatch.rs` | CLI owner adds local `tightbeam deploy` commands. They must not traverse the gateway HTTP seam. |
| Deployment mutation | no current seam | Deployment owner adds `cli/src/deploy/` with one `DeployManager` mutation entry point and read-only status queries. |
| Unit template | README inline example only | Packaging owner adds a testable system-unit template that resolves `/opt/tightbeam/active/root/bin/tightbeam-gateway`. |
| Compatibility | `lib/tightbeam/schema.ex` shape stamp and boot refusal | Compatibility owner exports build compatibility metadata without weakening the existing boot refusal. |
| Tests | `test/packaging_test.exs`; `test/release_candidate_workflow_test.exs`; Rust CLI tests | Test owner adds real-package, filesystem-race, crash, VM power-loss, systemd cutover, rollback, and GC suites mapped to Acceptance. |

Recommended file decomposition:

- `cli/src/deploy/mod.rs`: the only public mutation facade and transaction-state transition table.
- `cli/src/deploy/model.rs`: canonical record schemas and action-specific authorization/state types.
- `cli/src/deploy/fs.rs`: dirfd/no-follow path confinement, immutable publication, rename, fsync, and recovery reads.
- `cli/src/deploy/verify.rs`: archive validation, payload verification, provenance, platform, version, smoke, and compatibility gates.
- `cli/src/deploy/authorization.rs`: canonical production-installation challenge creation, Ed25519 approval validation, one-use consumption, Mike-only production-installation authority, the e2e test-fixture exception, key revocation, and explicit Gibson binding.
- `cli/src/deploy/systemd.rs`: service-registry validation, effective-unit readback, atomic unit replacement, ordered drain/restart, per-service observation, and unit recovery.
- `cli/src/deploy/status.rs`: read-only machine and per-service status projection derived from pointer, processes, service registry, intents, and audit facts.
- `cli/tests/deploy_safety.rs`: process-death, race, path, permissions, state-machine, and rollback tests.
- `test/deploy_power_loss_test.exs` or an equivalent isolated integration runner: disposable VM/loop-device and reboot matrices. The test must skip only when its named environment gate is absent; the release gate must supply that environment for Linux deploy support.

No other module may write deployment state. `args.rs` parses, `main.rs` routes local deploy commands, and `dispatch.rs` remains the gateway-request path for substrate verbs.

### Deployment namespace

```text
/opt/tightbeam/
  deploy.lock
  challenges/<challenge-id>.json
  authorization-use/<challenge-id>/<fact-digest>.json
  staging/<deploy-id>.partial/
  releases/sha256-<release-manifest-digest>/
    release-manifest.json
    tightbeam/...
  generations/<generation-id>/
    manifest.json
    root -> ../../releases/sha256-<release-manifest-digest>/tightbeam
  evidence/<evidence-digest>.json
  authorizations/<authorization-digest>.json
  intents/<transaction-id>.json
  audit/<transaction-id>/<fact-digest>.json
  trash/<object-id>/
  active -> generations/<generation-id>
```

Root owns this namespace, `/etc/tightbeam`, and each registered systemd unit. Each ancestor of the trust policy, host identity, and service registry is root-owned and not group/world writable. Incomplete staging is mode `0700`. Final directories are `0755`, ordinary payload files are `0444`, and executable payload files are `0555`. The manager refuses setuid/setgid bits, devices, FIFOs, sockets, unexpected hard links, unexpected owners, and service/group/world write permission.

The release manifest contains these fields; its content-addressed path supplies its own digest identity:

1. schema identifier;
2. tarball SHA-256;
3. source commit and product version;
4. target OS and architecture;
5. build workflow, run, and toolchain identity;
6. sorted complete payload manifest;
7. required verification suite identity and result digest;
8. supported org-state/schema shapes;
9. forward and backward compatibility decisions;
10. migration presence and reversibility.

The candidate proof must bind the payload-manifest digest and package digest. A locally computed digest proves integrity only. Before those bytes become restart-loadable on a production machine, Mike's production-installation approval must name those exact verified bytes. An e2e runner may use the separate test-fixture key to validate this mechanism outside production paths without Mike's approval. Gibson additionally requires Mike's explicit permission for each production installation.

### Production-installation approval trust and one-time use

For production installation, the production manager accepts only an Ed25519 signature whose key identifier and signature validate against the current production trust policy. The signed payload uses canonical JSON. The approval identity is the SHA-256 of the complete canonical envelope containing that payload and signature.

The production manager creates and fsyncs a production-installation challenge only after release verification finishes. It accepts no second open challenge for the same installation request. A root principal may close an open challenge as superseded or revoked, but that principal cannot create Mike's signature. Before the first installation mutation, the manager writes and fsyncs an immutable consumed fact that binds the challenge ID and approval digest. A crash after consumption but before installation leaves the approval spent and requires a new challenge plus a new Mike signature.

The manager does not use UTC time to accept or reject a production-installation approval. UTC fields remain audit metadata only. A challenge expires when the manager durably closes it, when its expected-active value changes, when its service-set digest changes, or when the trust policy no longer names its key. The manager refuses a malformed trust policy, host identity, service registry, challenge, approval envelope, signature, or use-state history before installation.

The production manager cannot load an alternate key from an approval, environment variable, command argument, org base, deployment root, or release payload. The gateway service account cannot write the production trust policy, host identity, service registry, challenge state, approval copies, or use facts. The test-only binary refuses `/opt/tightbeam`, the production trust-policy path, and each production systemd unit path. Ordinary development and test commands that do not target production installation do not request or consume Mike's approval.

### Machine service set and observation

Before challenge creation and again under the deploy lock before mutation, the manager canonicalizes and hashes the service registry. It reads each named unit's effective systemd properties. It refuses an empty registry, a duplicate unit, an unregistered Tightbeam unit, or a service-account mismatch. During managed operation it requires each registry entry's `ExecStart` to resolve through `/opt/tightbeam/active`. During virgin first cutover it instead accepts the exact verified legacy npm path until U2 replaces that entry's unit; another path refuses.

One separate restart authorization covers the complete ordered registry and binds its service-set digest. The manager drains and restarts entries in registry order. After each restart, it records that entry's unit state, main PID, resolved release digest, `/version` result, readiness result, and exact failure if one occurs. A failure stops the planned sequence; later per-service entries remain `pending`, while the aggregate machine result is `failed` under the precedence below. Retrying any entry requires new restart authority. Restart authority does not request or consume Mike's production-installation approval.

The machine observation result uses this exclusive precedence: `held` when the registry, unit inventory, process identity, or evidence is contradictory; otherwise `failed` when one registry entry fails its checks, even if later entries remain `pending`; otherwise `pending` while one registry entry lacks a terminal result; otherwise `observed` when each registry entry succeeds for the same active release and service-set digest. The manager stores per-service results and exactly one aggregate result. It does not promote a canary result or one representative instance to machine-wide observed-known-good.

### State machine

The manager permits this order:

```text
received -> staged -> verified -> authorized -> activated -> restarted -> observed
```

- **received**: input bytes and evidence are named, but no durable deployment object exists.
- **staged**: the manager validates the complete archive header set before it creates payload entries, then extracts through confined dirfd/no-follow operations only under `staging/<deploy-id>.partial`; `active`, registered units, npm tree, and running processes remain unchanged.
- **verified**: provenance, archive shape, full payload, platform, ownership/modes, CLI/gateway agreement, compatibility, and real side-path boot smoke pass. The manager fsyncs verification evidence before it can accept production-installation approval.
- **authorized**: for production installation, the manager validates Mike's signature, current trust key, open challenge, canonical host identity, deployment-root identity, candidate digests, verification digest, expected active, fixed `production-install` action, and service-set digest. It re-reads `active` and the service registry under the lock, then fsyncs the consumed fact before the first installation mutation.
- **activated**: the manager durably publishes release, generation, and intent, then atomically replaces `active` and validates the selected target.
- **restarted**: under separate restart authority, systemd drains and restarts each registry entry in order. Activation alone does not restart a service. The transition completes only after each entry has a terminal restart result.
- **observed**: each registry entry has one successful observation bound to the same active release and service-set digest. The manager does not add a numeric threshold or wait to this decision.

Each transition records actor, applicable authority, applicable approval and challenge digests, UTC audit time, canonical host identity, service-set digest, transaction, prior and target generation, tarball and manifest digests, source commit, verification evidence, lock result, syscall barrier outcomes, pointer readback, each service result, machine observation result, running roots, and rollback eligibility.

### Locking and expected-active comparison

The manager holds one exclusive `flock` on `deploy.lock` from the first active read through mutation and durable result recording. Activation, rollback, first cutover, unit rollback, and GC use the same lock. A competing operation returns a named busy result containing the holder transaction ID or later fails expected-active comparison. It cannot overwrite another transaction.

The supported topology has one `/opt/tightbeam` deployment root, one deployment lock, one service registry, and one deployment scope per machine. Gateway instances do not receive separate deployment roots. Each action revalidates the exact service-set digest named by its authorization.

### Atomic release and pointer activation

The manager performs these barriers in order:

1. It creates candidate files exclusively with no-follow semantics, writes final bytes, sets final owner and mode, and fsyncs each file.
2. It fsyncs candidate directories bottom-up.
3. It renames the complete candidate directory to its content-addressed release name. If the name exists, it validates the complete tree. It does not merge. It fsyncs `releases/`.
4. It writes and fsyncs `manifest.json`, creates the relative `root` link, fsyncs the generation directory, renames it into `generations/`, then fsyncs `generations/`.
5. It writes and fsyncs the immutable activation intent and its directory. It protects target, prior, releases, authorization, verification evidence, and intent from GC.
6. It creates a unique temporary relative link beside `active` and fsyncs the deployment-root directory.
7. It uses `renameat` to replace `active` with the temporary link, then fsyncs the deployment-root directory.
8. It re-opens `active` with no-follow checks, resolves beneath the root, and verifies generation and release digests before recording success.

Staging, releases, generations, pointer temp, intents, audit, and trash must reside on one mounted filesystem. The manager compares device IDs before mutation.

### Activation recovery

Manager startup acquires the lock and reads the namespace before it requires a selected payload. It accepts absent `active` only when the namespace validates as virgin and either no U0 intent exists or exactly one unresolved U0 intent names `expected_active = virgin:<this-root-identity>`. Otherwise it validates `active` and the complete selected payload. It then classifies each unresolved intent:

| Observed namespace | State | Permitted action |
|---|---|---|
| Virgin namespace; no U0 intent | `virgin-ready` | Report each registered service's actual process root as running or report that service stopped. Report the exact legacy npm release selected by each on-disk and systemd-effective unit as restart-loadable outside the managed pointer, with verified/unverified state. Accept only a first-cutover authorization bound to this exact virgin root, service-set digest, and each verified old unit/npm digest. |
| Virgin namespace; U0 intent expects this virgin root; target validates | `activation-not-committed` | Preserve target, intent, authorization, evidence, old units, and old npm tree. Append an idempotent recovery fact keyed with the virgin root identity. A principal may explicitly resume or abandon while authorization remains valid. |
| `active == expected_active`; old and target validate | `activation-not-committed` | Preserve both and append an idempotent recovery fact. A principal may explicitly resume or abandon while authorization remains valid. |
| `active == target`; target validates | `activation-committed-recovered` | Do not rename again. Append an idempotent recovered-commit fact. Only separately authorized restart and observation may continue. |
| `active` names another valid generation | `activation-indeterminate` | Hold each deployment mutation, service restart, and GC action. Preserve involved objects and require adjudication. |
| `active` is absent outside the exact virgin cases, or is dangling, escaping, writable, or digest-invalid | `activation-indeterminate` | Hold each deployment mutation, service restart, and GC action. Report the failed invariant and require recovery authority. |

The audit deduplication key is `(transaction_id, state, observed_namespace_identity)`, where the namespace identity is either the active generation digest or the virgin deployment-root identity. A crash during audit append cannot duplicate authority. For U0, a crash before pointer rename recovers the exact virgin `activation-not-committed` state; a crash after rename recovers either virgin/not-committed or target/committed according to durable namespace truth. For later activations, power loss after pointer rename but before root-directory fsync may recover old or target. A missing success row does not decide any case.

### Prior-good rollback

Each generation manifest names `prior_generation`. Ordinary activation requires that prior generation and release to be durable and retained. Rollback:

1. takes the deploy lock;
2. selects an explicitly named retained observed-known-good generation;
3. validates its full manifest, payload, ownership, permissions, compatibility, and expected current generation;
4. validates separate rollback and restart authorizations bound to the same host, current, target, evidence, service-set digest, and restart intent; neither record grants the other's action;
5. creates a new generation pointing at the retained release and naming the current generation as prior;
6. uses the normal pointer activation protocol;
7. restarts only under restart authority, then observes by the same contract.

The manager retains the failed generation for diagnosis. It refuses code rollback across an incompatible or irreversible durable-state change unless a separately reviewed migration plan includes pre-activation backup evidence, a successful restore drill, a compatibility window, and explicit data-rollback authority.

### GC

GC runs under the deploy lock. Its protected set contains:

- active generation and release;
- active generation's prior observed-known-good generation and release;
- one additional observed-known-good generation;
- objects pinned by an open deploy, rollback, incident, migration, or unresolved intent;
- objects younger than the configured rollback window.

Activation-history facts that prove whether a deployment-root identity has ever selected a generation are permanently protected. They are not retention-window objects.

If an activation, rollback, cutover, or unit-rollback intent is unresolved, GC refuses before deleting any object. If the required prior plus additional known-good protected set does not yet exist, GC also refuses.

If the active generation lacks a complete machine observation for the current service-set digest, GC protects the prior observed-known-good generation and refuses any deletion that would weaken rollback. A partial or canary service result does not release that hold.

GC emits an exact dry-run list, re-reads `active` and the protected set, and validates action-specific GC authority before deletion. The authorization supplies the exact retention cutoff; no default rollback-window duration exists. GC renames eligible objects to same-filesystem trash, fsyncs the parent, and deletes only from trash without following symlinks. A failed delete remains named and recoverable until the trash entry is removed.

### Status

`tightbeam deploy status --json` is read-only and reports:

```text
restart_loadable = <generation + release digest read from active | legacy npm root + digest while virgin>
restart_loadable_verification = verified | unverified + reason
transaction      = virgin-ready | not-committed | committed | committed-recovered | indeterminate
audit            = none | complete | recovered-missing-row | contradictory
running          = <per-service generation/digest or legacy process root>
service_set      = <registry digest + ordered unit names | invalid + reason>
services         = <per-unit running digest + unit state + version + readiness + result>
observation      = held | failed | pending | observed (one value; precedence defined above)
prior_known_good = <generation/digest or unavailable + reason>
staged           = <deploy ids + digests>
lock             = free | <holder transaction id>
unit_disk        = <per-unit old digest | new digest | invalid + reason>
unit_effective   = <per-unit old path | managed path | other + reason>
unit_transaction = <per-unit legacy | pending-reload | rollback-pending-restart | observed | indeterminate>
next_authority   = <machine and per-service none | resume-activation | reload-unit | restart | observe | rollback-unit | adjudicate>
gc_hold          = true|false + protected transaction ids
last_results     = verification + production-installation approval + action authorization + activation + unit-cutover + per-service restart + machine observation
```

When `active` exists, the status writer derives restart-loadable state from a fresh validated pointer read. In a virgin namespace, it derives restart-loadable state for each registered service from that service's on-disk and systemd-effective legacy unit path, reports each path's full release digest, and reports verification state separately; it cannot call unverified legacy bytes verified. It cannot print `activated` from intent or audit alone. It cannot print `observed` unless each current registry entry has a successful observation for the same active release and service-set digest.

### Transactional first cutover

First cutover has two transactions and four phases:

1. **U0 — managed legacy generation**: Validate the virgin deployment-root state. Verify the exact currently supported npm archive and full installed payload against trusted provenance and a complete manifest. Bind `expected_active = virgin:<deployment-root-identity>`, the service-set digest, and each exact old unit/npm digest into first-cutover authorization. Before creating the U0 intent, revalidate the same virgin identity and service set under the deploy lock. Import the bytes as `legacy_release`. Create `legacy_generation` with `prior_generation = null`, original unit/npm metadata, and verified import evidence. It does not become observed-known-good until U3 produces one successful observation for each registry entry. Use the normal intent, temporary-link, pointer-rename, root-fsync, readback, and audit barriers to activate it at `/opt/tightbeam/active` without changing an old unit or process. Smoke-exec the managed path and prove byte/provenance equivalence.
2. **U1 — unit preparation**: For each registry entry in order, preserve the complete old npm tree and exact root-owned old/new unit copies with digest, owner, group, mode, and path. Keep the unit rollback copies in a root-owned transaction directory on each live unit's mounted filesystem; the directory must not be a systemd unit search entry. Write and fsync one unit intent that binds the service-set digest, each old/new unit digest, legacy generation, running release digests, authorizer, and transaction. Revalidate `active == legacy_generation` and the registry digest.
3. **U2 — unit replacement**: For each registry entry in order, open `/etc/systemd/system` by directory descriptor, refuse untrusted ancestors, write a sibling temp exclusively, set root ownership and mode `0644`, fsync file and directory, rename over that exact unit, fsync the directory, then re-open and hash the installed unit. One failure stops later replacements and enters the per-unit recovery matrix.
4. **U3 — reload and observation**: Under cutover authority run daemon-reload once. Verify each registry entry's manager-effective `ExecStart` equals the managed path. Under restart authority drain, restart, and observe each entry in registry order. Record `unit-cutover-observed` only when the machine observation result is `observed`. Only then may a newer release activate.

Cutover recovery applies the table to each registry entry and derives the machine result from each on-disk unit digest, systemd effective `ExecStart`, running process root, the service-set digest, and `active == legacy_generation`. One contradictory entry makes the machine result `held`:

| Boundary | Required recovery |
|---|---|
| Before unit rename | Old disk/effective unit remains authoritative. Remove only a validated temp. New release activation remains refused. |
| Durable rename before daemon-reload | Disk is new; manager may cache old. Record `unit-pending-reload`. Re-run reload only under cutover authority. Cached old resolves preserved npm legacy; rebooted new resolves managed legacy. |
| During/after reload before controlled restart | Effective path must equal exact old or new path. Old resumes authorized reload; new resumes authorized restart. Another value holds as `unit-indeterminate`. |
| Restart completed before observation row | Re-read disk, effective unit, running root, active, and service-set digest for that registry entry. Append an idempotent recovered service observation without another restart only if the entry selects managed legacy and passes its running, serving checks. Record machine observation only after each registry entry has a successful service observation. Otherwise preserve state and do not mark it observed. |
| New unit or managed legacy invalid | Refuse newer activation. Under unit-rollback authority, atomically restore the old unit and run daemon-reload. Re-read the on-disk and effective unit. Do not restart. Record `rollback-pending-restart` when both select the old path; require separate restart authorization bound to the current service-set digest, exact restored unit digest, effective path, preserved npm digest, service, and observed current process state before the service starts against preserved npm bytes. |
| Unit rollback reached old disk/effective path before restart | Preserve both unit copies and byte paths. Report `rollback-pending-restart`; accept only the exact separate restart authority described above or adjudication. A spontaneous restart may load the already-effective old verified npm path, but it does not create or consume planned restart authority. |
| During unit rollback | Reclassify disk and effective path as old, new, or held. If a process is running, report its root independently. Preserve both unit copies and byte paths until separately authorized restart and observed resolution. |

After the cutover rollback window closes under explicit authority, ordinary rollback uses generation activation. Reverting the unit to npm remains a separate unit-rollback action and is available only while the preserved npm tree remains.

### Operating pattern and deletion

This spec establishes one pattern: **immutable release plus atomic active pointer** for Linux/systemd product deployment. It does not apply to org data, identity repositories, harness homes, or macOS launchd.

The implementation change set replaces the supported direct-overwrite upgrade instructions in `README.md` and `docs/UPGRADE.md` and replaces each supported inline unit with the managed template before A-01 runs. Those documentation changes ship only with the accepted mechanism. Retiring an operational copy-based watchdog is a separate migration action after the replacement rollback path is proven; it is not a product-source deletion authorized by this spec. Preserve the live npm tree, old units, and watchdog during the first-cutover rollback window.

## Acceptance

The original twenty obligations remain numbered A-01 through A-20. Amendment tests A3-01 through A3-10 refine A-10 and A-20 where the earlier forms were incomplete and add independent gates. A pass requires all thirty cases. Each fixture uses captured real package or service evidence where the case crosses an external boundary.

1. **A-01 — supported-path source guard.** Given release docs, scripts, and service templates, when the guard scans the supported upgrade path, then no direct `npm install -g` or checkout overwrite is an activation step and systemd resolves only the managed `active` path.
2. **A-02 — artifact completeness.** Given a real release tarball and its manifest, when the deployer extracts it, then each path/type/mode/size/digest matches. Adding, removing, truncating, or changing one member causes refusal before `active` changes.
3. **A-03 — trusted provenance.** Given a candidate, when its tarball digest, manifest digest, commit, platform, version, build identity, or verification-evidence digest differs from trusted evidence, then verification refuses before production-installation approval.
4. **A-04 — archive attacks.** Given archives containing an absolute path, `..`, duplicate path, escaping symlink or hard link, device, FIFO, socket, setuid bit, or unexpected owner/mode, when staged, then each case refuses and leaves `active` unchanged.
5. **A-05 — stage isolation.** Given snapshots of active inode, link target, and full selected-release digest, when receive, extract, or a verification failure occurs, then snapshots remain equal. If the service dies during staging, systemd restarts the old release.
6. **A-06 — real boot smoke.** Given a staged real candidate, scratch org base, and unused port, when verification runs, then `/version`, doctor/readiness, CLI/gateway agreement, and one real turn through each release-required harness gate pass using captured real responses.
7. **A-07 — production-installation approval ordering.** Given production installation before verification, challenge creation before verification, approval before verification, a signature not made by the current Mike key, altered signed payload bytes, a production manager offered the test key, an e2e runner targeting `/opt/tightbeam` or a production unit, a Gibson approval bound to another host, digest mismatch, wrong canonical host identity, an action other than `production-install`, wrong expected active, wrong service-set digest, or a consumed, superseded, revoked, or state-expired challenge, when production installation is requested, then the manager refuses before its first installation mutation. Given a valid approval, when the manager begins production installation, then it fsyncs exactly one consumed fact before the first installation mutation and refuses reuse after a crash. Given ordinary development or test work that does not target a production machine's installation paths or units, when that work runs, then it requests and consumes no Mike approval.
8. **A-08 — same-filesystem rule.** Given staging or pointer temp on another mount, when activation starts, then the manager names device mismatch or `EXDEV`, performs no copy/delete fallback, and leaves `active` unchanged.
9. **A-09 — atomic reader race.** Given concurrent readers that resolve and execute/read `active`, when old and new generations alternate repeatedly, then each read is one complete known digest; a missing, mixed, dangling, or partial read fails the test.
10. **A-10 — crash matrix baseline.** Given fault injection after each file write, file fsync, directory fsync, release rename, generation rename, link creation, active rename, root fsync, and status append, including U0 from a virgin namespace, when the manager restarts, then it produces the exact recovery class in this spec. A3-01 through A3-04 control missing-status details.
11. **A-11 — power-loss matrix.** Given the same barriers on ext4 mounted with default options in a disposable VM or loop device, including U0 from a virgin namespace, when power is cut and the filesystem remounts, then the namespace is exact virgin, a fully valid old or target generation, or an explicitly held invalid state. Given another filesystem or mount-option class, the manager refuses it by name as unproven. A kill-only test cannot satisfy this case.
12. **A-12 — concurrent deploys.** Given two deploy IDs racing within the one deployment scope on a machine, when both request mutation, then one holds the lock and the other reports busy or later fails expected-active comparison. The loser cannot overwrite the winner.
13. **A-13 — symlink/path race.** Given concurrent replacement attempts against attacker-writable ancestors, staging children, manifests, and archive links, when the manager operates, then dirfd/no-follow checks refuse and no write escapes the intended root.
14. **A-14 — permissions.** Given each existing non-root service account, when its gateway runs, then it executes active code and writes its registered org base but cannot mutate root-owned deployment objects, trust files, registry, authorization state, or registered units. Given a non-root caller, when deployment mutation is requested, then it refuses. The supported setup creates no dedicated deploy user.
15. **A-15 — restart boundary.** Given a finite registry with two services and old running/active state, when the candidate is only staged, a crash restarts old. After durable activation and before planned restart, status shows each service's running old digest and active new digest; a crash loads new. One separate restart authorization binds the exact ordered service-set digest and does not consume Mike's production-installation approval. The manager restarts in registry order and reaches `observed` only after both services resolve the active digest and pass their running, serving checks, with no added numeric threshold or wait. A contradictory registry, unit inventory, process identity, or evidence leaves the machine `held`. Otherwise, one failed or wrong-release service leaves the machine `failed`, even if a later service remains `pending`. Otherwise, one missing terminal result leaves the machine `pending`. Each negative result leaves the generation unobserved.
16. **A-16 — rollback.** Given observed-known-good A followed by activated B, when rollback to A is authorized while readers race and faults occur at each barrier, then readers see complete A or B and retained A remains byte-identical.
17. **A-17 — rollback authorization.** Given wrong target, stale current generation, unobserved target, incompatible schema, missing evidence, or missing action authority, when rollback is requested, then it refuses before pointer mutation.
18. **A-18 — migration compatibility.** Given the oldest supported org state and an irreversible-schema fixture, when candidate boot and rollback compatibility are checked, then supported directions pass and unsupported byte rollback refuses unless its reviewed restore/forward plan is selected and proven.
19. **A-19 — GC.** Given active, prior, additional known-good, incident-pinned, in-progress, young, orphan, and trash objects plus a two-service machine with one successful and one pending observation, when GC races activation or rollback, then it removes only eligible orphan/trash entries, preserves the protected set, and preserves the prior observed-known-good generation until the complete machine observation succeeds.
20. **A-20 — first-cutover rehearsal baseline.** Given a disposable Linux host with a real npm install, two registered system units, and current guidance, when side-by-side import, ordered unit cutover, reload, ordered drain/restart, per-service observation, machine observation, and authorized legacy rollback run, then no step loads unverified newer bytes. The manager records `unit-cutover-observed` only after both registered services run and serve from managed legacy. A3-05 through A3-10 control the complete pass contract.

Amendment acceptance:

1. **A3-01 — missing activation status.** Given ordinary old-active and virgin-U0 fixtures with injected crashes after target generation fsync, intent fsync, active rename, root fsync, active re-read, and before/during/after success append, when recovery runs, then it emits the exact virgin/old/target/indeterminate class and does not automatically rename, retry, roll back, restart, or GC. In the virgin fixture, pre-rename recovery is `activation-not-committed`; post-rename recovery follows the durable virgin-or-target namespace.
2. **A3-02 — pointer/audit contradiction.** Given intents with `active` equal to virgin-absent, old, target, unrelated valid, dangling, escaping, and corrupt generations plus absent, present, or contradictory success facts, when status and recovery run, then exact virgin is accepted only for a U0 intent bound to that virgin-root identity, pointer truth controls exact old/target, and other states hold with a named conflict.
3. **A3-03 — recovered-commit idempotency.** Given repeated crashes during recovered-commit append, when recovery repeats, then audit deduplicates by transaction/state/digest, protects prior and target, and does not duplicate restart authority.
4. **A3-04 — GC recovery race.** Given an unresolved activation intent, when GC races recovery, then GC refuses before deleting any object, including a release, generation, intent, authorization, or evidence object unrelated to that transaction.
5. **A3-05 — legacy import.** Given altered, truncated, added, or removed npm-tree/archive members, when legacy import runs, then it refuses. Given a real verified legacy archive, then the managed legacy generation is byte/provenance-equivalent to the old path.
6. **A3-06 — unit file crash matrix.** Given a two-service registry plus process-death and VM power-loss injection on ext4 mounted with default options after each service's temp creation, write, owner/mode set, file fsync, pre-rename directory fsync, rename, post-rename directory fsync, re-hash, reload, effective-path query, restart, service-observation append, and machine-observation append, when recovery runs, then it returns the exact per-unit and machine recovery classes.
7. **A3-07 — unit-boundary spontaneous restart.** Given each registered service forced to fail before its unit rename, after its durable rename before reload, and after reload before planned restart, when systemd restarts that service, then it loads verified legacy bytes from preserved npm or managed legacy; a newer candidate is not loadable.
8. **A3-08 — reboot matrix.** Given a two-service registry, ext4 mounted with default options, and reboot after each unit barrier, when the host boots, then each disk-old unit selects old npm legacy and each disk-new unit selects managed legacy. A mixed but valid set reports each unit truth and cannot become machine-observed. A missing, partial, unregistered, or unready unit/active state is held.
9. **A3-09 — unit rollback matrix.** Given one registered service with new-unit validation, reload, or managed-start failure, when explicit unit rollback is authorized with fault injection at each restore barrier, then recovery classifies each unit as old, new, or held and never accepts a partial unit. Reaching old on-disk and effective unit state records `rollback-pending-restart` for that service; no planned restart occurs until a separate restart authorization bound to the current service-set digest is validated. Missing, stale, mismatched, or consumed restart authority leaves the service stopped or leaves an already running process unchanged. The machine cannot become observed while one registry entry remains rollback-pending.
10. **A3-10 — two-phase exclusion.** Given attempts to activate a new release during U0 through U3 and each recovery state, when activation is requested, then it refuses until `unit-cutover-observed` or its recovered equivalent is durable.

Traceability:

| Requirement area | Implementation seams | Acceptance |
|---|---|---|
| Packaging and provenance | packaging scripts, proof verifier, candidate workflow | A-02, A-03, A-06, A3-05 |
| Stage and archive safety | deploy verify/fs modules | A-04, A-05, A-08, A-13, A-14 |
| State, authorization, and pointer activation | deploy model/authorization/fs modules | A-07, A-09, A-10, A-11, A-12, A-15, A3-01, A3-02, A3-03 |
| Rollback and compatibility | deploy manager/verify modules plus schema metadata | A-16, A-17, A-18 |
| GC | deploy manager/fs modules | A-19, A3-04 |
| First cutover and systemd | deploy systemd module and unit template | A-20, A3-05 through A3-10 |
| Documentation/source guard | README, UPGRADE, managed unit template | A-01 |

## Open Questions

No blocking or non-blocking questions remain. Mike closed the former OQ-1 through OQ-5 in `att_03d09931-e62d-4ed9-9d1a-ee8790188498`, closed the residual authorization and machine-service clauses in `att_6f020416-aa7b-40ea-abcf-ec3eabd68853`, and narrowed the approval scope in `att_de7e1be6-64bb-4c8a-abdd-8e68b9f89a18`:

1. **Resolved OQ-1 — production-installation approval.** Mike is the sole signer for installing an update on a production machine. Each production installation requires one Mike-signed, single-use approval bound to the exact canonical host identity, deployment root, fixed `production-install` action, update and evidence digests, expected active state, and service-set digest. The production manager verifies the pinned Mike Ed25519 key and durably consumes the challenge before the first installation mutation. Acceptance uses challenge and deployment state instead of wall-clock time. Receiving, staging, and verifying a candidate do not install it. Restart, observation, rollback, unit rollback, and GC use their separate controls and do not consume Mike's production-installation approval. Ordinary development and test work require no Mike production-installation approval. A test-only binary may accept a separate e2e key only for a temporary fixture outside production paths. Each Gibson production-installation approval binds Gibson's canonical host identity and supplies explicit permission for that one installation.
2. **Resolved OQ-2 — observed-known-good.** A generation becomes observed-known-good when it restarts into a running, serving state. The implementation adds no numeric threshold or wait to this decision.
3. **Resolved OQ-3 — filesystem.** The production durability claim supports ext4 mounted with default options. The manager refuses each other filesystem or mount-option class by name as unproven. The design adds no other filesystem class.
4. **Resolved OQ-4 — principals.** Root owns the registered systemd units, `/etc/tightbeam` deployment policy files, and `/opt/tightbeam`. Each gateway continues to run as its existing non-root account. The design adds no dedicated deploy user.
5. **Resolved OQ-5 — machine scope.** One deployment exists per machine, not per gateway instance. One root-owned ordered service registry enumerates the finite machine service set. One restart authorization binds that exact set. The manager restarts entries in registry order and records each result. A generation becomes observed-known-good only when each registry entry restarts into the exact active release and passes its running, serving checks. Status reports each service and the aggregate pending, failed, held, or observed result. A partial result keeps rollback and GC protection in force. The design adds no per-instance deployment root or parallel per-instance deploy scope.

Implementation must apply these rulings exactly and must not infer additional configurability, thresholds, filesystems, principals, trust roots, authorization formats, service-set sources, or multi-instance deployment scope.
