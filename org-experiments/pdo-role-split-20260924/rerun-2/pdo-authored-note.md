# Engram fixture correction note

The three draft claims are incorrect. Corrected text:

“Each source machine keeps its SQLite index with its local transcript tapes. The query coordinator asks the owning machine to run a local query over SSH and returns bounded results. Each transcript reference identifies both the source machine and its tape; it is not a central filesystem path. If a selected source is unavailable, the result must show incomplete coverage. That absence does not establish that no matching conversation exists.”

Corrections:

- A changes “copies its entire tape collection” to local ownership and SSH execution: tapes remain with each source, and queries run there.
- B changes “a tape ID alone” to a source-and-tape reference, because a tape ID without its source is not sufficient across machines.
- C changes “complete empty result” to visible incomplete coverage, because an unreachable source may contain matching conversations.
