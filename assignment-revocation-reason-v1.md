# Assignment revocation reason v1

Status: implementation authority — Mike written instruction, 2026-08-30
Work item: `wi_f2ea2015-b535-40c6-9704-77f8a70799df`

## Purpose

An assignment revocation is a consequential terminal act. The record MUST say
why the authorized principal revoked it, or it fails to explain whether prior
work was superseded, discarded, or interrupted.

## Contract

1. `revoke-assignment <assignmentId> --reason "..."` requires exactly one
   text reason. The reason MUST contain 1–2000 Unicode code points and at
   least one non-whitespace code point.
2. The public CLI refuses a missing reason locally. The handler independently
   refuses missing, blank, oversize, or non-text reasons before mutation.
3. The handler preserves its existing authorization and opaque-id behavior.
   It refuses unauthorized, unknown, ambiguous, already-terminal, and
   conflicting calls before mutation.
4. A retry by the same authorized principal with the same reason returns the
   existing revoked assignment and creates no second state notice or record.
   A different reason on an already-revoked assignment is a conflict.
5. A successful revocation writes one immutable provenance record and closes
   the assignment in the same transaction. The record contains assignment id,
   revoker user or session, time, and reason. Database enforcement MUST refuse
   a revoked close without its matching provenance record.
6. Session retirement uses the same provenance mechanism. Its durable reason
   is `holder session retired`.
7. Reopening clears no provenance record. A later revocation writes a new
   record for the new close generation.

## Compatibility and reads

Existing revoked rows remain readable. Migration writes their exact recorded
closer and close time with reason `legacy_unknown`. That sentinel means the
old row never recorded a reason; it MUST NOT be treated as an inferred motive.

The assignment CLI read, assignment detail read, work-state projection, and
`assignment.closed` Firehose payload expose `revocationReason`. It is null for
open, completed, and surrendered assignments. The field follows the existing
assignment visibility boundary; no new broad read or event audience exists.

## Proofs

Tests MUST cover direct and session-mediated callers; authorization; missing,
blank, oversize, and malformed reasons; same-reason retry and conflicting
retry; terminal races; retirement; legacy migration; restart/replay; CLI
usage and exact request body; reads; Firehose; and absence of a reason row on
each refusal.
