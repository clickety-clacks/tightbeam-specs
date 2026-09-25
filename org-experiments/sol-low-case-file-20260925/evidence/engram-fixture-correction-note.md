# Engram fixture correction note

**Claim A:** "Every satellite copies its entire tape collection to the coordinator before queries work."
Corrected: Each source machine keeps its SQLite index together with its local transcript tapes. Nothing is copied to a coordinator in advance. The query coordinator asks the owning machine to run local queries over SSH and returns bounded results.

**Claim B:** "A tape ID alone always identifies a result across all sources."
Corrected: A returned transcript reference identifies both its source and its tape, not a tape ID alone. The same tape ID on two machines is not the same result; source and tape together are the identifier.

**Claim C:** "If one selected source cannot be reached, the coordinator can report a complete empty result."
Corrected: An unavailable selected source must be visible as incomplete coverage, not folded into a plain empty result. Absence of a match from that source is not evidence that no matching conversation exists there.
