# Operator ruling provenance migration fixture — 2026-08-30

This fixture is a privacy-safe, row-level capture for migration acceptance T1 in
\`operator-ruling-provenance-v1.md\`.

## Source and boundary

- Store: live Gibson Tightbeam \`state.db\`, opened read-only.
- Release: \`0.1.8\`, build \`1337\`, source stamp \`fdb3db5\`.
- Window: 2026-08-20 00:00:00 PT through 2026-08-30 12:08:30 PT, inclusive.
- Selection: operator decision requests ruled by \`user:mike\` in that window.

## Redaction transform

The capture reads only \`id\`, \`ruledAt\`, and \`ruledViaSessionKey\`. It reads no question,
option, context, decision, rationale, message, attachment, raw session key, or raw request id.

1. Sort selected rows by \`ruledAt,id\`.
2. Replace the raw row id and timestamp with one-based \`ordinal\`.
3. Map a null \`ruledViaSessionKey\` to \`sessionState:"legacy-unknown"\` and
   \`sessionSlot:null\`.
4. Sort distinct non-null raw session keys. Replace each with its one-based dense rank as
   \`retained-session-<two digits>\`, and emit \`sessionState:"known"\`.
5. Emit only \`ordinal\`, \`kind\`, \`authority\`, \`sessionState\`, and \`sessionSlot\`.

The transform preserves the legacy shape that migration uses while removing identifiers and
private content. \`rows.jsonl\` contains 294 rows: 291 legacy-unknown rows and 3 known rows
with 3 distinct pseudonymized slots.

## Consumer contract

T1 reads \`rows.jsonl\` as JSON Lines. Each row has exactly this schema:

| Key | Value |
| --- | --- |
| \`ordinal\` | one-based positive integer unique within this file |
| \`kind\` | literal \`operator\` |
| \`authority\` | literal \`user:mike\` |
| \`sessionState\` | \`legacy-unknown\` or \`known\` |
| \`sessionSlot\` | null for \`legacy-unknown\`; otherwise \`retained-session-01\`, \`retained-session-02\`, or \`retained-session-03\` |

The known labels are dense ranks of the three distinct retained raw session keys. They label
session-mediated legacy rows only. A null slot labels a legacy-unknown row; neither label proves
direct-user authorship.

The fixture's SHA-256 is declared by P8 and T1 in the canonical proposal. A replacement capture
uses this same transform and updates both declarations in one amendment.
