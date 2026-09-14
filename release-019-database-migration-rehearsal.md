# 0.1.9 database migration rehearsal

Status: runbook

This rehearsal proves that 0.1.9 can migrate a real 0.1.8 database without
changing the live Gibson database.

## Preserve the source snapshot

Before any live database maintenance, create a consistent snapshot with
SQLite `VACUUM INTO`. The snapshot must pass `PRAGMA quick_check` before use.
Keep the original snapshot read-only and give it a stable name such as:

`state-0.1.8-pre-0.1.9-migration-YYYYMMDDTHHMMSSZ.db`

Record these facts beside it in a manifest:

- SHA-256 hash and byte size
- snapshot time in UTC
- source Tightbeam version, build, and commit
- source schema version
- `PRAGMA quick_check` result
- storage location and retention date

The manifest and preserved bytes identify the migration source. Do not write a
marker into the database itself.

## Rehearse on a disposable copy

1. Copy the preserved snapshot into a new isolated test base directory.
2. Confirm the copy's SHA-256 matches the manifest before starting 0.1.9.
3. Point only the isolated 0.1.9 test instance at that directory. Use a test
   port and test work directory. Do not point a candidate at Gibson's live
   `~/.tightbeam` base.
4. Run the supported 0.1.9 startup and migration path once.
5. Save the exact candidate commit, commands, timestamps, logs, and exit codes.

Never test by editing the preserved snapshot in place. Begin every retry from a
fresh copy of the same verified bytes.

## Acceptance checks

The rehearsal passes only when all of these checks pass:

- startup and migration finish without manual SQL
- `PRAGMA quick_check` passes after migration
- the schema version is the expected 0.1.9 version
- required 0.1.9 indexes exist, including indexes added for database timeout
  corrections
- durable sessions, work items, assignments, decisions, messages, and turns
  remain readable with their pre-migration counts reconciled
- representative transcript, pending-work, wake, and startup queries complete
  within their stated limits
- normal gateway startup and bounded Linux and macOS acceptance checks pass
- a second startup performs no additional migration and preserves the result

Record failures against the candidate. Do not repair the test database by hand
and then call the rehearsal successful.

## Retention and cleanup

Keep the immutable source snapshot and its manifest through the 0.1.9 release
and rollback window. Disposable migrated copies may be deleted after their logs
and results are preserved. Deleting a test copy must never delete or replace the
source snapshot.

The existing Gibson backup job creates an hourly verified SQLite snapshot and
copies it to Tars. It also retains one daily copy for 14 days. Before a live
change, preserve a named snapshot separately so the hourly mirror cannot replace
the migration source.
