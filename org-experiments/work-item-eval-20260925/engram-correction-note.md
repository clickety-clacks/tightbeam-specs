# Engram query correction

**A.** Source machines retain their own SQLite indexes and local transcript tapes. The coordinator does not require every satellite to copy its tape collection before a query; it asks each owning machine to run its local query over SSH and returns bounded results.

**B.** A result reference must identify both the source and its tape. A tape ID by itself does not always identify a result across all sources.

**C.** If a selected source is unavailable, the coordinator must show incomplete coverage. That absence does not establish that no matching conversation exists, so it cannot report a complete empty result.

These corrections replace centralized-copy, tape-ID-only, and complete-empty-result claims with the supplied source ownership, reference, and unavailable-source facts.
