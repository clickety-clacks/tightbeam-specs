# Engram and Tightbeam integration recon

Recorded 2026-09-19 at Mike's request. Research and recommendations, not an
implemented integration or a change to either product's runtime contract.

## Finding

Configuration can collect Tightbeam's native Codex and Claude transcripts.
A small integration is needed for results that name the Tightbeam agent,
preserve its history across harness changes, or explain which delegation and
work item led to a code edit. A new Tightbeam-specific transcript parser is not
the first requirement.

The installed Tightbeam release already shares a harness home across
archetypes. The durable agent identity is the Tightbeam session key. A home
directory, archetype name, worktree path, native harness session ID, and Engram
tape ID are different identifiers.

## Verified topology

The live Gibson gateway reported Tightbeam 0.1.8 at `fdb3db5`. Its
`Homes.home_path/3` resolves:

```text
<host base_dir>/homes/<configured host name>/codex
<host base_dir>/homes/<configured host name>/claude
```

Codex receives that path as `CODEX_HOME`; Claude receives it as
`CLAUDE_CONFIG_DIR`. These are harness homes, not a separate operating-system
HOME for every agent. Archetype guidance is supplied per session, and elected
skills are materialized in that session's working directory. Several
archetypes therefore write native transcripts beneath the same harness home.

The fetched 0.2 main source at
`944feaa11078f02520d66eee10b4d4a5fee3ed20` retains the shared-home functions
and the session/harness pointer model. That source observation is not a claim
that the 0.2 line is deployed.

A read-only September 19 scan of Gibson found:

| Transcript root | JSONL files | Logical file bytes |
| --- | ---: | ---: |
| `~/.tightbeam/homes/gibson/codex/sessions` | 5,628 | 28,315,638,878 |
| `~/.tightbeam/homes/gibson/claude/projects` | 215 | 461,510,485 |

These counts include whatever native transcript files exist under those roots;
they are not counts of unique Tightbeam agents or normalized Engram tapes.
The scan read filesystem metadata. For one recent transcript from each harness,
it read identifying fields and verified a matching Tightbeam pointer. Both
samples mapped to named orchestrator sessions. It did not ingest this corpus.

## What configuration covers

Engram source at `72821518037a9d896f0b4d784fee146800902e78` and the T1772
candidate at `9f8afc65d0b365444446a473c04389adf80bd4b3` already contain native
Codex/Claude adapters, recursive watch sources, and optional relative-path glob
filters. A separate configuration can point them at Tightbeam's transcript
directories and keep output outside the watched roots.

Illustrative Gibson configuration using existing fields:

```yaml
db: ~/.engram/tightbeam/index.sqlite
tapes_dir: ~/.engram/tightbeam/tapes
additional_stores: []
watch:
  debounce_secs: 5
  ingest_timeout_secs: 120
  log: ~/.engram/tightbeam/watch.log
  sources:
    - path: ~/.tightbeam/homes/gibson/codex/sessions
      pattern: "*.jsonl"
    - path: ~/.tightbeam/homes/gibson/claude/projects
      pattern: "*.jsonl"
```

This is a proposed configuration, not an installed one. Generate each host's
paths from its actual base directory and configured name. Do not copy Gibson's
name to every satellite, or assume that `path` expands wildcard directories.
Add native archive roots explicitly if they exist and historical coverage is
wanted. Existing older per-archetype homes, if retained, require an explicit
historical inventory rather than a claim that the two current roots cover them.

The present watcher reacts to file events. It does not scan every existing file
on startup, and it skips missing source directories. Backfill must be explicit;
a source that appears after startup needs reconfiguration or a watcher restart.
Automatic inventory and catch-up could be a later convenience feature.

No Engram executable was found on Gibson's current shell PATH during this recon.
The example establishes source-level configurability, not a working deployment
or compatibility proof for every installed Engram binary. Installing Engram and
making its CLI available to Tightbeam agents are deployment tasks. An MCP server
is not required merely to let an agent run the existing CLI.

## Where a feature or integration is needed

| User-visible capability | Existing support | Missing piece |
| --- | --- | --- |
| Find code reads and edits in native transcripts | Native adapters and configured source roots | Validate real adapter shapes on the selected release and backfill |
| Open surrounding conversation | Engram tapes and peek/grep | Retain the required tapes and their lookup paths |
| Name the Tightbeam agent and archetype in a result | Tightbeam has session metadata and native-session mappings | Join and expose that metadata in Engram results |
| Follow one agent through restarts, fallback, or a harness/host change | Tightbeam's append-only harness pointer chain | Group source tapes under the stable Tightbeam session key while preserving each native segment |
| Explain which assignment or delegation caused an edit | Tightbeam has assignments, work items, turns, wakes, and sender/target records | Import or resolve explicit causal references; distinguish ancestry from the actual dispatch |
| Filter by agent, archetype, or work item | Those fields exist on the Tightbeam side | A supported context/query extension or an external result-enrichment tool |
| Identify historical guidance | Git identity revisions and current session stamps exist | Event-scoped evidence; current stamps alone cannot establish past applied or actually read guidance |
| Query across hosts | Engram can query additional accessible read-only stores | Tape transport, freshness, host identity, and deduplication policy; it is not remote-query federation |

The T1772 candidate's ordinary result `session_id` is the content-addressed
tape ID. It is not Tightbeam's session key or the native harness session ID.
Native IDs can appear in tape `source.session_id` metadata, but there is no
current Tightbeam mapping or archetype projection in that result formatter.

## Smallest useful integration

Start with the current native transcript adapters and a separate context
manifest. A companion tool can initially enrich query results by reading that
manifest and the tape metadata. A reusable product integration should provide
a supported metadata import/read interface instead of requiring every caller
to know Tightbeam's private SQLite schema.

The mapping should retain:

- Export/organization namespace and configured host identity.
- Harness family and native session ID.
- Tightbeam session key, with display name and archetype as attributed metadata.
- Pointer history and its recorded timestamps/reasons.
- Engram tape IDs or immutable tape versions associated with the native source.
- Explicit turn, assignment, work-item, wake, and dispatch references where the
  source records establish the relationship.

Tightbeam already stores `harness_pointers` with `sessionKey`,
`harnessSessionId`, `sourceSessionRef`, `harness`, `machine`, `reason`,
and `createdAt`. Its `sourceSessionRef` encodes the harness, machine, and
native session ID. Reuse this existing identity and keep its export namespace;
do not invent an archetype-derived agent ID.

At the observation point, 18,385 pointer rows represented 3,368 distinct source
sessions and 3,224 Tightbeam session keys. Repeated load rows are history, not
new agents. Joining only the newest pointer would lose older provenance.
The stored current archetype, display name, host, and identity revision must
not be retroactively applied to every historical event.

The inspected `inspect` response exposes agent metadata but not the pointer
chain. A supported export of the selected mapping fields is a small Tightbeam
interface addition. A first local experiment can read those fields read-only,
as this recon did. A production consumer should not depend on arbitrary table
access or `SELECT *`; session records also contain unrelated private fields.

On the Engram side, preserve native source identity, accept the optional
context manifest, and expose the resolved actor and causal references.
Keep this metadata separate from code fingerprints. Basic collection does
not need these features; complete Tightbeam attribution does.

## Dispatch and identity details that configuration cannot infer

Engram's existing dispatch traversal expects a shared
`<engram-src id="UUID"/>` in the sending tool call and receiving message.
Tightbeam's agent keys, wake IDs, assignments, and pointer records do not
automatically satisfy that marker contract. No automatic Engram marker bridge
was found in the inspected live source.

Two implementation options remain:

1. A narrow producer integration emits the existing marker into both real
   transcript sides for new dispatches. Prove sender, recipient, and direction
   for native Tightbeam dispatch, retries, and reused sessions. A recipient-only
   marker is insufficient. This does not recover historical unmarked traffic.
2. A context exporter maps existing durable Tightbeam relationships into
   explicit causal links that an Engram extension can traverse. This can cover
   history where the records actually contain the link.

Prefer the second for durable Tightbeam attribution and historical coverage;
evaluate the first as a smaller optional path for forward-only lineage.
Neither should fingerprint all work-item descriptions or prompts to guess links.
The session that spawned an agent is not necessarily the sender of its latest
assignment, and native harness subagents are not automatically Tightbeam agents.

Identity revisions need similar care. The current session stamp records
bookkeeping, not a per-event proof of what instructions the model read.
The current candidate identity-apply spec explicitly distinguishes file update,
revision stamping, and a best-effort re-read prompt. Return a recorded revision
with its observation scope, or mark history unknown. Do not promise exact
historical loaded identity from today's session row.

A Codex compatibility detail needs fixture coverage: the inspected Engram
extractor handles top-level `session_id`, `payload.session_id`, and
`payload.session.id`, but not a `session_meta.payload.id`-only record.
The sampled current Tightbeam Codex transcript contains both `id` and
`session_id`, so it is covered for that field. That one sample does not prove
older or other harness versions are covered. This is an adapter compatibility
case, not a reason to infer identity from filenames or modify old tape blobs.

## Storage and host layout recommendation

Use one writable local index per collecting host, or one central writer fed
immutable exported tapes. The index's storage location should not multiply
with archetype or session count. Keep native transcripts and Engram output
outside each other's watch roots.

Existing `additional_stores` can combine accessible read-only indexes, provided
the associated tapes are also available. That configuration is not an SSH
transport, a freshness protocol, or cross-machine authorization. Avoid a
network-mounted SQLite file with multiple host writers; see
[SQLite's network-storage guidance](https://sqlite.org/useovernet.html).

Complete and measure T1772 before a broad Tightbeam backfill. Gibson's roughly
28.8 GB of raw transcript files makes the old generic-message indexing policy
especially expensive. Per-agent guidance, skills, and coordination metadata
must not recreate that policy through an integration.

The storage recommendations are recorded separately at
`<shared-workspace>/engram/specs/storage-followups-2026-09-19.md`:
binary fingerprint values, compact repeated metadata, and recurring storage
regression measurements. Context enrichment is another use of compact metadata,
not an exception to the code-window evidence model.

## Bounded proof before implementation is called complete

Use a small retained fixture set and an isolated derived store to prove:

- Two agents with the same archetype in one shared home stay distinguishable.
- One stable Tightbeam agent remains traceable through multiple native session
  IDs and a host/harness change; unrelated agents stay separate.
- Identical native IDs or paths in different host/export namespaces do not
  collide. Resumed or incrementally ingested source tapes do not lose history.
- A real read/edit result opens its exact raw context and identifies the source
  agent. Generic messages remain outside the code evidence index.
- Parent-to-worker-to-edit attribution follows a recorded dispatch or assignment;
  retries and later assignments do not borrow the wrong parent.
- Native subagents, retired agents, archive roots, missing mappings, and
  unavailable satellites have explicit coverage results.
- Unknown historical identity stays unknown. Storage bytes and query behavior
  remain within the accepted baseline for the fixed fixture set.

This recon performed source inspection, filesystem inventory, schema reads,
and two native-ID-to-agent joins. It did not install Engram on Gibson, start a
watcher, rebuild an index, or establish full adapter or end-to-end integration
coverage.

## Evidence and version boundaries

- [Live home implementation](https://github.com/clickety-clacks/tightbeam/blob/fdb3db5/lib/tightbeam/homes.ex),
  especially `home_path/3` and the module's transcript-preservation contract.
- [Live native-session mapping](https://github.com/clickety-clacks/tightbeam/blob/fdb3db5/lib/tightbeam/org.ex),
  `harness_pointers`, `append_pointer_in_txn/4`, `pointer_chain/2`, and
  `source_session_ref/3`.
- [Live query projection](https://github.com/clickety-clacks/tightbeam/blob/fdb3db5/lib/tightbeam/gateway.ex),
  `inspect_session/1`, `inspect_result/3`, and identity revision handling.
- [Fetched main home implementation](https://github.com/clickety-clacks/tightbeam/blob/944feaa11078f02520d66eee10b4d4a5fee3ed20/lib/tightbeam/homes.ex).
- [Engram watch/config source](https://github.com/clickety-clacks/engram/blob/72821518037a9d896f0b4d784fee146800902e78/src/config/mod.rs)
  and `src/main.rs` at the same commit.
- [T1772 query projection](https://github.com/clickety-clacks/engram/blob/9f8afc65d0b365444446a473c04389adf80bd4b3/src/query/format.rs)
  and the native adapters at that commit.
- [Engram dispatch contract](https://github.com/clickety-clacks/engram/blob/72821518037a9d896f0b4d784fee146800902e78/specs/core/dispatch-marker.md).
- Tightbeam specs read at `3ddd4c8de4dbacc33a0e05c2fceaa574d57d2ac7`:
  `served-identity-home-projection-v1.md`, `immediate-identity-apply-v1.md`,
  the hub, and 0.2 program/fabric/build records. The hub marks home projection
  implemented despite the older draft header in its satellite document.
- Live state queries used `file:/home/mike/.tightbeam/state.db?mode=ro`,
  selected metadata only. Credential files and credential values were not read.
