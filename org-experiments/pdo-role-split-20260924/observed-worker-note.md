# Engram multi-machine fixture correction

## Corrected text

Each source machine keeps its SQLite index with its local transcript tapes. The query coordinator asks the owning machine to run local queries over SSH and returns bounded results. A returned transcript reference identifies its source and tape, rather than a central filesystem path. If a selected source is unavailable, the result must show incomplete coverage; its absence does not prove that no matching conversation exists.

## Material corrections

- **A:** Sources do not copy their complete tape collections to the coordinator. Queries run locally on the owning machine.
- **B:** A tape ID alone is insufficient across sources. The returned reference identifies both source and tape.
- **C:** An unreachable selected source cannot yield a complete empty result. The coordinator must report incomplete coverage.
