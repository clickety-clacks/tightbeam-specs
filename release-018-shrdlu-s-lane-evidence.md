# v0.1.8 replacement plan — SHRDLU S-lane evidence

Executor: `tester:release018-shrdlu-e2e`  
Assignment: `asg_c8e76551-800f-4521-a91d-1aae9c95a3fa`  
Authority: `release-018-test-plan-v2.md` (S1 unchanged through plan v2.2,
commit `5df5826`)  
Release: immutable tag `v0.1.8`, commit
`becb13072624fce1129cfce377882bc2fb647cb8`

## S1 (withdrawn isolated form) — UNPROVEN / NOT CREDITED

Window: 2026-08-15 17:34:11–17:37:39 UTC. Host/account:
`shrdlu` / `clu`.

### Isolation baseline

Before creating the run directory, this read-only probe established the
collision boundary:

```sh
ssh shrdlu 'bash -lc '\''id -un; hostname; ss -ltnp | grep -E ":(11373|12374)[[:space:]]" || true; test -e ~/tb018-s-lane && ls -ld ~/tb018-s-lane || echo ABSENT ~/tb018-s-lane; /home/clu/.local/bin/tightbeam --version'\'''
```

Observed at `2026-08-15T17:34:11Z`:

```text
clu
shrdlu
LISTEN ... 0.0.0.0:11373 ... users:(("beam.smp",pid=886487,fd=23))
ABSENT /home/clu/tb018-s-lane
0.1.7
```

Port 12374 and the run directory were absent. The existing 0.1.7 gateway
was PID 886487 on port 11373. Nothing under `/home/clu/.tightbeam` was
written by S1.

The operator PATH baseline had Rust at `/home/clu/.cargo/bin`, Node/npm at
`/usr/bin`, Claude and Codex at `/home/clu/.local/bin`, and no standalone
Elixir/Mix/Erlang commands. The release package carries its own ERTS, so the
latter is expected for package installation.

### Immutable artifact verification

The package and checksum file were downloaded directly from the immutable
GitHub release:

```sh
curl -fL --retry 3 -o ~/tb018-s-lane/download/tightbeam-0.1.8-linux-x86_64-becb130.tgz \
  https://github.com/clickety-clacks/tightbeam/releases/download/v0.1.8/tightbeam-0.1.8-linux-x86_64-becb130.tgz
curl -fL --retry 3 -o ~/tb018-s-lane/download/SHA256SUMS \
  https://github.com/clickety-clacks/tightbeam/releases/download/v0.1.8/SHA256SUMS
grep 'tightbeam-0.1.8-linux-x86_64-becb130.tgz' SHA256SUMS | sha256sum -c -
```

Result:

```text
tightbeam-0.1.8-linux-x86_64-becb130.tgz: OK
sha256=faf202f5f7057a00f478df54a60998650ddc96d2248813a3e3823775d0737630
```

The first unfiltered `sha256sum -c SHA256SUMS` correctly verified the Linux
asset but exited nonzero because the checksum file also names the undownloaded
Darwin asset. That executor-command issue is preserved in
`evidence/release-018-shrdlu-s1/package-checksum.txt`; the narrowed published
Linux line is the acceptance check.

### Finding 14 prerequisite — completed before driver use

The source was cloned at the immutable tag and the Rust CLI built before any
e2e driver invocation:

```sh
git clone --branch v0.1.8 --depth 1 \
  https://github.com/clickety-clacks/tightbeam.git ~/tb018-s-lane/source
cd ~/tb018-s-lane/source
cargo build --release --manifest-path cli/Cargo.toml
```

Evidence:

```text
SOURCE_HEAD=becb13072624fce1129cfce377882bc2fb647cb8
SOURCE_TAG=v0.1.8
CARGO_BUILD_START_UTC=2026-08-15T17:35:48Z
Finished `release` profile [optimized] target(s) in 57.18s
CARGO_BUILD_EXIT=0
CARGO_BUILD_END_UTC=2026-08-15T17:36:45Z
```

No e2e driver was run before or during this build.

### Isolated package install and gateway boot

The release tarball was installed with a run-owned npm prefix, not the
operator's existing global prefix:

```sh
npm install -g --prefix ~/tb018-s-lane/npm \
  ~/tb018-s-lane/download/tightbeam-0.1.8-linux-x86_64-becb130.tgz
~/tb018-s-lane/npm/bin/tightbeam --version
```

Result: `added 1 package`, exit 0, CLI version `0.1.8`.

The isolated gateway was started in tmux session `tb018-s-lane` with:

```sh
env \
  TIGHTBEAM_LOCAL_HOST_NAME=shrdlu \
  TIGHTBEAM_BASE_DIR=/home/clu/tb018-s-lane/home \
  TIGHTBEAM_PORT=12374 \
  TIGHTBEAM_ADVERTISED_URL=ws://shrdlu:12374 \
  TIGHTBEAM_EFFORT_CHECKIN_HORIZON_MS=2500 \
  CODEX_PATH=/home/clu/.local/bin/codex \
  PATH=/home/clu/tb018-s-lane/npm/bin:/home/clu/.cargo/bin:/home/clu/.local/bin:/usr/local/bin:/usr/bin:/bin \
  /home/clu/tb018-s-lane/npm/bin/tightbeam-gateway
```

At `2026-08-15T17:37:39Z`:

```text
INSTALLED_CLI_VERSION=0.1.8
SOURCE_HEAD=becb13072624fce1129cfce377882bc2fb647cb8
ISOLATED_PID=1378774
LIVE017_PID=886487
tb018-s-lane: 1 windows (created Sat Aug 15 17:37:22 2026)
LISTEN ... 0.0.0.0:11373 ... pid=886487
LISTEN ... 0.0.0.0:12374 ... pid=1378774
```

The gateway created the fresh state at
`/home/clu/tb018-s-lane/home/state.db`, installed ACP adapters under that
same isolated base, and served on 12374. Its only readiness warnings are the
expected missing isolated Claude/Codex credentials; S2 owns onboarding.

The original 0.1.7 CLI still reported `0.1.7`, and its gateway remained the
same PID 886487 on port 11373 after S1. This proves S1 did not replace or stop
the existing install.

### Immutable evidence files

The companion directory `evidence/release-018-shrdlu-s1/` contains the exact
captured build log, package verification, install output, gateway log, doctor
census, port/PID verification, and timestamps. `gateway.json` is deliberately
excluded because it contains the isolated CLI bearer token; no provider
credential file was read or copied.

## S1b (withdrawn isolated base) — UNPROVEN / NOT CREDITED

Authority: plan v2.3 commit `48bef1f` and `docs/TEST-HOSTS.md` section 3a.
Window: 2026-08-15 17:44:12–17:46:06 UTC. This ceremony completed before
S2 onboarding or any e2e evidence; the post-ceremony filesystem census was
`NO_AUTH_FILES` under the isolated base's `auth/` directory.

The tag source was prepared under the host's already-installed pinned
OTP 28 / Elixir 1.19 toolchain. The Rust release build recorded under S1
predates this preparation and no e2e driver ran during it.

The retained driver `evidence/release-018-shrdlu-s1b/s1b_pair_connect.exs`
performed the real wire ceremony:

```elixir
{:ok, %{token: token, user_id: user_id}} =
  Tightbeam.ClientE2E.SimClient.pair("127.0.0.1", 12_374,
    device_id: "release018-s1b",
    claimed_name: "mike"
  )

{:ok, client} =
  Tightbeam.ClientE2E.SimClient.connect(
    "127.0.0.1",
    12_374,
    token,
    device_id: "release018-s1b"
  )
```

The token existed only in process memory and was printed as `[redacted]`.
No token or provider credential is present in the evidence corpus.

Clean terminal output at `2026-08-15T17:45:42Z`:

```text
PAIR_OK user_id=mike token=[redacted]
CONNECT_EVIDENCE: %{
  main: %{
    "displayName" => "Main",
    "kind" => "main",
    "sessionKey" => "agent:main:clawline:mike:main"
  },
  pair_user_id: "mike",
  connected_user_id: "mike",
  connected_is_admin: true,
  auth_success: true,
  auth_user_id: "mike",
  auth_is_admin: true,
  sync_complete: true
}
S1B_PASS
S1B_EXIT=0
```

Read-only SQLite rows after the ceremony, with token columns deliberately
omitted:

```text
users:   mike | isAdmin=1
devices: release018-s1b | mike | allowlisted | sim | client-e2e
sessions: agent:main:clawline:mike:main | Main | kind=main |
          isBuiltIn=1 | ownerUserId=mike | origin=user:mike | active
```

An admin-attributed CLI read independently returned exactly one active Main
session owned by `user:mike`; both model catalogs were empty, as required
before S2 onboarding.

Two executor-only evidence issues are preserved rather than hidden:

1. The first pair/connect succeeded through the full evidence map, then its
   formatter called nonexistent `Tightbeam.JSON.encode!/1`. Process exit
   closed the socket. The same device was paired and connected again after
   changing only the formatter to `IO.inspect`; the second run carries the
   clean terminal receipt above.
2. A read-only display query lost SQL string quotes in the SSH shell and
   failed with `no such column: main`. It was rerun using `isBuiltIn=1`; no
   database mutation occurred.

Companion evidence is in `evidence/release-018-shrdlu-s1b/`, including both
ceremony attempts, sanitized rows, the admin-attributed list result, source
preparation log, and the exact driver.

## S1 v2.7 — in-place replacement on standard port: PASS

Authority: plan v2.7 commit `8579cff`. Window:
2026-08-15 18:05:05–18:09:41 UTC. Host/account/base/port:
`shrdlu` / `clu` / `/home/clu/.tightbeam` / `11373`.

Mike withdrew the isolated/parallel acceptance. The earlier evidence commit
`7281952` remains recorded above but is not credited. The only prior test
installation, `/home/clu/tb018-s-lane`, was resolved before deletion as the
base serving port 12374 in tmux `tb018-s-lane`. That session was stopped and
the directory removed. The standard 0.1.7 gateway on 11373 remained running
until the replacement package was prepared.

The immutable release package was downloaded again and verified against the
published checksum:

```text
package=tightbeam-0.1.8-linux-x86_64-becb130.tgz
sha256=faf202f5f7057a00f478df54a60998650ddc96d2248813a3e3823775d0737630
source=v0.1.8 / becb13072624fce1129cfce377882bc2fb647cb8
```

Finding 14 was re-proven before any v2.7 e2e driver use: `cargo build
--release --manifest-path cli/Cargo.toml` completed successfully under the
pinned tag. The standard 0.1.7 gateway PID 886487 was then terminated
gracefully, and npm replaced the package in `/home/clu/.local`. The CLI
reported `0.1.8`; the installed release tree contained only `0.1.8`.

### Real first-boot stamp refusal (S5 refusal half)

The real 0.1.7 database remained at `/home/clu/.tightbeam/state.db` for the
first 0.1.8 boot. The refusing binary was pinned by the package checksum
above and reported Tightbeam `0.1.8` in its stack. It exited 1 without
opening a listener and emitted:

```text
this Tightbeam database was written by a different build.

  stamped: coordination-fabric-v1-phase1-v3
  this build: operator-decision-requests-v1

operator decision requests changed the decision_requests and wakes shape.

There is no migration. Move the database aside and let it be recreated.
```

This is the v2.7 real-flow S5 refusal half. After the refusal, no process held
the database open. The sanctioned move-aside preserved it at:

```text
/home/clu/.tightbeam/moved-aside-v017-20260815T180853Z/state.db
inode=15468588
sha256=a177ad1c542cda3ac759d9169c4052b2b1b18177cd61abeaa4b65db3c8c59ebb
stamp=coordination-fabric-v1-phase1-v3
```

The move stayed on the same filesystem and preserved inode and checksum.
There were no WAL/SHM companions after the clean 0.1.7 stop. A fresh boot
then created stamp `operator-decision-requests-v1` and served from the
standard package/base on port 11373 as PID 1393618. Verification showed:

```text
CLI_VERSION=0.1.8
RELEASE_DIRS=0.1.8
LISTEN=0.0.0.0:11373 pid=1393618
PORT_12374_ABSENT
WITHDRAWN_BASE_ABSENT
```

No credential file was read, copied, moved, or deleted. Companion evidence
is in `evidence/release-018-shrdlu-s1-v27/`. Sanitized summaries deliberately
exclude the prior Erlang distribution cookie.

### v2.8 retrospective audit — named pristine-proof limit

Plan-under-review commit `2592ed6` made two pre-first-boot artifacts explicit
S1 acceptance requirements. The existing v2.7 capture answers them as follows:

1. **Pre-boot stamp readback: captured and matching.** Before the first 0.1.8
   boot, a read-only connection executed `SELECT shape FROM schema_stamp`
   against the real 0.1.7 DB and returned exactly
   `coordination-fabric-v1-phase1-v3`. The real refusal cited that exact string
   as `stamped:` and cited `operator-decision-requests-v1` as `this build:`.
   The observed database therefore did not carry the plan text's illustrative
   `model-identity-v1` value; the readback-based oracle correctly follows the
   actual DB rather than a hardcoded expected source stamp.
2. **Pre-boot read-only SQLite backup: NOT TAKEN.** No
   `sqlite3 'file:...?mode=ro' ".backup ..."` artifact was created before the
   first 0.1.8 boot. The original DB was moved aside afterward with inode and
   checksum preserved, but that post-refusal preservation is not a substitute
   for a pristine pre-exposure backup while refuse-before-write is itself under
   test.

Accordingly, this run carries a named pristine-proof limitation under the
v2.8 acceptance draft. It must not be silently credited as satisfying the new
mandatory pre-boot backup requirement.

### v2.11b transition backup — COMPLETE WITH READ-ONLY SIDECAR FINDING

Window: 2026-08-15 18:45:50–18:46:28 UTC. Plan HEAD was `03b886e`
(v2.11b). Under the product owner's one-action authorization, SQLite opened
the preserved moved-aside DB through a `mode=ro` URI and wrote a uniquely
named post-exposure online backup beside it:

```sh
sqlite3 'file:/home/clu/.tightbeam/moved-aside-v017-20260815T180853Z/state.db?mode=ro' \
  ".backup '/home/clu/.tightbeam/moved-aside-v017-20260815T180853Z/state.post-exposure-ro-backup-20260815T184550Z.db'"
```

The new backup is 3,182,592 bytes, has SHA-256
`76a581247b42a2c6260278b8de40aa017491e8a15e2a14ac916fa521451af086`,
passes `PRAGMA integrity_check` as `ok`, and reads stamp
`coordination-fabric-v1-phase1-v3`. The source DB remained inode `15468588`,
3,182,592 bytes, mtime `2026-08-15 18:08:28.232649543 +0000`, and SHA-256
`a177ad1c542cda3ac759d9169c4052b2b1b18177cd61abeaa4b65db3c8c59ebb`
before and after.

Important finding: the plan/authorization described the read-only backup as
touching nothing, but SQLite's `mode=ro` open updated the existing preserved
source `state.db-shm` mtime from `1786817718.7575933980` to
`1786819569.3092484900`. The source WAL mtime stayed unchanged. Read-only
verification also created WAL/SHM sidecars beside the NEW backup. All source,
backup, and sidecar artifacts remain preserved; nothing was removed. Exact
names, mtimes, stats, hashes, command, and validation result are in
`evidence/release-018-shrdlu-s1-v211b/post-exposure-backup.txt`. No gateway,
base reset, auth, boot, S1b, OAuth, or S2 mutation accompanied this action.

Plan v2.11d (`5a311f0`) dispositioned the SHM observation as SQLite
connection scratch and bound stability to DB/WAL content, inode, and size.
The supplemental readback records unchanged DB inode `15468588`, size
3,182,592 and SHA-256 `a177ad1c...c59ebb`; WAL inode `15468468`, size zero,
and SHA-256 `e3b0c442...b855`. Thus the new v2.11d binding fields are stable;
the SHM mtime change remains preserved as an explained observation.

## S1b v2.7 — pair then connect on replaced install: PASS

Window: 2026-08-15 18:10:44–18:14:33 UTC. The v0.1.8 tag source was prepared
under OTP 28 / Elixir 1.19. The retained driver used port 11373 and fresh
device id `release018-s1b-v27`; its token existed only in process memory and
was printed as `[redacted]`.

The first executor invocation used `mix run` without `--no-start`; Mix tried
to start a second Tightbeam application and failed `:eaddrinuse` before any
pairing. The exact specimen is preserved and was attested as
`att_1c37a9cb`. The sanctioned correction loaded the driver without starting
a second gateway:

```sh
mix run --no-start /home/clu/tb018-replacement-staging/s1b_pair_connect.exs
```

It completed the real wire ceremony:

```text
PAIR_OK user_id=mike token=[redacted]
connected_user_id=mike
connected_is_admin=true
auth_success=true
sync_complete=true
main.sessionKey=agent:main:clawline:mike:main
S1B_PASS
S1B_EXIT=0
```

Sanitized SQLite rows independently showed user `mike` with `isAdmin=1`,
device `release018-s1b-v27` allowlisted, and one active built-in Main owned by
`mike`. A bare CLI read was correctly refused for missing attribution and
preserved as `att_e61195b6`; the sanctioned admin-attributed read
`tightbeam list --as-user mike` then returned exactly that active Main.
User services `openclaw-gateway` and `subspace-daemon` and system services
`postgresql@16-main` and `docker` were all active after replacement.

Companion evidence is in `evidence/release-018-shrdlu-s1b-v27/`.

## S2 precondition finding — BLOCKED pending plan direction

Without reading any credential file, the fresh 0.1.8 gateway reported an
existing Codex credential from the retained standard auth directory, and the
admin-attributed catalog exposed Codex models before S2a. That makes S2b's
required natural `needs_onboarding` fixture unavailable. No auth file has
been modified. The finding is attested as `att_1c37a9cb`; S2 remains paused
pending an explicit sanctioned auth move-aside/reset path.
