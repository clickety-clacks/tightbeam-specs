# v0.1.8 replacement plan — SHRDLU S-lane evidence

Executor: `tester:release018-shrdlu-e2e`  
Assignment: `asg_c8e76551-800f-4521-a91d-1aae9c95a3fa`  
Authority: `release-018-test-plan-v2.md` (S1 unchanged through plan v2.2,
commit `5df5826`)  
Release: immutable tag `v0.1.8`, commit
`becb13072624fce1129cfce377882bc2fb647cb8`

## S1 — fresh isolated Linux install: PASS

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
