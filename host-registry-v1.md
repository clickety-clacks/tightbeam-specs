# Host registry — one writer, one truth

Decided 2026-07-28 (Flynn): host facts move INTO THE DB, behind `Tightbeam.DB`
— the serialization seam that already exists. Placement's "hosts are INSTANCE
CONFIG, never DB rows" doctrine is AMENDED; it predates `assimilate` being a
verb that writes hosts. Credential metadata stays host-local (see Non-goals).

## Problem

`Placement.register_host/3` is `read_registry` → `Map.put` → `File.write!` with
nothing serializing it. Every assimilate takes that path, and the boot
endpoint-provisioning pass (4dd0d39) is a second writer family.

MEASURED on this tree, 40 concurrent registrations of distinct hosts, 10 trials
(`Placement.register_host/3` through its public API):

- **371 of 400 registrations returned `{:ok, entry}` to their caller and were
  then absent from the registry.** Roughly 3 of 40 survive per trial: each
  writer reads the file, adds its own host, and writes back a map missing every
  host that landed while it was thinking.
- **1 torn read crashed a writer** with `JSON.DecodeError: unexpected end of
  JSON binary at position 0` — `File.write!` truncates before it writes, so a
  concurrent reader can see a zero-length file.

The live sighting behind the ticket (two assimilates interleaving on
`hosts.json`, `{eurisko}` then `{eliza,eurisko}`) is the two-writer corner of
the same window. The failure is silent by construction: the CLI reports
`registered`, exit 0, and the host is gone. It resurfaces later as
`unknown_host`, or — worse — as a placement decision pointed at the wrong
machine.

The torn read is not confined to writers. `Placement.hosts/1` is on the live
path: every model-catalog refresh enumerates hosts (cd4413b), and every spawn
and tune resolves against it. An assimilate running while the gateway reads can
crash a reader that had nothing to do with it.

`Credentials.write_metadata!` shares the read-modify-write shape but NOT the
torn-read defect: it already writes through a temp file and renames (locally
`atomic_write!`, remotely `printf > tmp && mv`). Its exposure is lost updates
between concurrent writers of one provider's metadata, not corruption.

## Design

1. **`hosts` becomes a DB table** — name (primary key), ssh, base_dir, cli_bin,
   adapter_bin_dir. `Tightbeam.DB` is the existing single-writer seam; nothing
   new is invented to get serialization.
2. **`register_host/3` writes in a transaction** — the read-modify-write
   disappears, because a row upsert has nothing to read first.
3. **`Placement.hosts/1` reads the table**, and still adds the gateway's own
   entry (`local_host_name/0`, `ssh: nil`) on top, which nothing may redefine.
4. **Boot migrates once**: an existing `hosts.json` is read into the table and
   the file renamed aside (`hosts.json.migrated`). A registry that is already a
   table is left alone. The rename is what makes the migration idempotent and
   the old file recoverable.
5. **`gateway.json` stays a file.** The CLI reads it before any DB exists —
   bootstrap chicken-and-egg — and it has one writer. Same for the satellite's
   provisioned `gateway.json`, written by the gateway over rsync.
6. **Placement's moduledoc states the amended belief**, not the history: hosts
   are DB rows; `gateway.json` is the bootstrap file.

## Non-goals

- No lock file, no advisory locking, no retry loop. The DB transaction is the
  serialization; a second mechanism beside it is the thing to avoid.
- No change to what a host entry MEANS, or to resolution/placement semantics.
- No migration of `gateway.json` in either direction.
- **Credential metadata stays host-local.** The host registry is unambiguously
  the GATEWAY's own state; credential metadata for a REMOTE host is that host's
  state, which the gateway reads over ssh
  (`cat <base_dir>/auth/<harness>/.tightbeam/credential.json`). A satellite that
  is reimaged, rotated, or onboarded out of band self-describes — moving the
  fact into the gateway's DB makes the gateway the authority on state stored on
  another machine, and the two copies can then disagree with no tiebreak. Its
  exposure also differs in kind: `write_metadata!` is already atomic
  (temp-then-rename), so the risk is a lost update between two concurrent
  onboards of the SAME provider on the SAME host, not the silent, live-path loss
  measured above.

## Acceptance

1. N concurrent `register_host/3` calls for N distinct hosts leave N hosts
   registered — measured before and after against the numbers above, and every
   caller that was told `{:ok, _}` finds its host present.
2. A reader (`Placement.hosts/1`) concurrent with registrations never observes a
   torn or partial registry.
3. An org booting with an existing `hosts.json` comes up with those hosts in the
   table and the file renamed aside; booting again is a no-op.
4. An org with no `hosts.json` boots clean, and the gateway's own entry is
   present with `ssh: nil` in both cases.
5. Resolution, spawn placement, and the per-refresh catalog enumeration are
   unchanged in behavior — proved by the existing suites staying green, not by
   new assertions restating them.
