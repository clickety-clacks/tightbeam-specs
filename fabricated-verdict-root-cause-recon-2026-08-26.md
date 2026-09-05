# Fabricated verdict incident — canonical root-cause recon

Status: evidence-only recon; owner review is required before prevention work.

Work item: `wi_893b0503-66f1-4d08-ad8d-90674b8370ed`  
Recon assignment: `asg_fce604b8-2922-475b-a748-58fbe620e63e`  
Mike ruling: `att_56716aa9-c991-4a21-86b3-dc46bd7f0a00`  
Current source baseline: Tightbeam `origin/main` `8e258b579d1170c1f3c7d71ac2c0f76f5d29431b`, observed 2026-08-26.

## Decision and verdict

Decision: did Tightbeam wake assembly or database isolation cause the apparent cross-tenant wake corruption and fabricated review verdict, and what is the smallest justified prevention boundary?

**No, high confidence:** this was not a Tightbeam wake-assembly memory bleed or database cross-tenant leak. The wake sender's shell evaluated backticked text while constructing an `eval`-based command. That evaluation ran `ps` and a real `tightbeam attest` before Tightbeam received the wake. Their stdout became part of the delivered prompt; the attest command created the supposed fabricated row.

**Yes, high confidence:** the resulting row was a real, incorrectly authorized review-card verdict at the time. It was inert for completion because that reader accepted only the exact review holder's verdict. Guard commit `cd72fe0b06404afc6619a800c84a6a7eea595baa` closes the non-holder write gap and is an ancestor of current `main`.

The remaining prevention is narrowly bounded: harness-produced wake bodies must bypass shell command text. Add one stdin-based wake-body transport and make the harness adapter use it. Do not change wake delivery, tenant storage, completion selection, or revoke authority for this incident.

## Durable evidence

| Evidence | Observation | Weight |
| --- | --- | --- |
| `att_8b0374c8-a97b-4353-8e8a-f2e04cabe039` | The original reporter recorded a corrupted delivered message, a producer-authored row on a review card, and apparent cross-owner process content. | Initial symptom report; its causal framing was later tested. |
| Reviewer transcript `s_c5f06b10-7c04-402d-98f8-cb4f54b07fd2` | The delivered body preserves the sender's `zsh -c … eval 'tightbeam wake … --prompt "…"'` wrapper. It includes the embedded `ps` output and the JSON result of the embedded `tightbeam attest`; shell-process entries include the running wake itself. This report does not reproduce unrelated process or owner data. | Direct, discriminating evidence. |
| `att_3ba0f8cc-aab3-4557-90cb-4fa398a76685` | A real `reviewed-clean` row exists at `1786065622010`, authored by producer session `s_71bbea17`, with note `...`, on `asg_d58088b8-1335-4454-9caf-cbca3fb375d3`. | Direct durable row. |
| `att_1fcaa8a0-15ea-4080-aafd-e789c868f7a8` | Review holder `s_48aa761b` later filed `changes-requested`. | Independent confirmation that the holder did not author the earlier row. |
| `att_4fd1b6c4-0016-45e5-a30e-4947cbd9d459` | The predecessor recon independently reached shell substitution, identified the completion filter, and identified the then-open write gap. | Corroborating verdict. |
| `art_4c9e07c7` | At pre-fix main `ac8651d`, a non-holder could write a linked-review verdict; the completion read predicate required `v.bySession = r.holderKey`. | Source recon, SHA-256 `899f29c1c829d3391187d821130b034af3e3788e9884f2058aa1d991ab778f7c`. |
| `art_f800d602`, `art_03ffc8a8`, `art_93270a89` | `cd72fe0b` passed gates, received independent reviewed-clean, and fast-forwarded to canonical main. `art_03ffc8a8` is the corrected report; stale-digest `art_39206159` is excluded. | Independent implementation and integration chain. |
| Current source | `git merge-base --is-ancestor cd72fe0b… HEAD` exited zero. The linked-review writer guard is at `lib/tightbeam/assignments.ex:1845-1875`; completion reads holder-authored review verdicts at `:328-350`. | Fresh reconciliation. |

### Missing report

`art_60015bcf` points to `gibson:/home/mike/.tightbeam/work/2a821367016a/recon-verdict-wake-corruption.md`, has no digest, and that exact path returned `No such file or directory` on 2026-08-26. Its bytes are irrecoverable. This recon neither quotes nor infers its content; the missing pointer is a durability specimen.

## Reconstruction and disconfirmation

1. Producer `s_71bbea17` opened review assignment `asg_d58088b8-1335-4454-9caf-cbca3fb375d3`, whose holder was `s_48aa761b`.
2. The producer embedded a long body inside a double-quoted `--prompt` argument and sent the command text through `eval`. The body contained backticked example commands.
3. Shell command substitution ran the embedded commands before the CLI parsed arguments. `ps` generated the apparent cross-owner content; the embedded `tightbeam attest` ran as the producer session.
4. Their stdout was substituted into the wake body. The resulting JSON-looking fragment and `att_3ba0f8cc` are a real command effect, not a wake-delivery-generated row.
5. The historical server admitted the non-holder row. It could not qualify completion because the reader required the review holder as author.
6. The review holder later filed `changes-requested`, then the review assignment was revoked. The current order does not support the original assertion that the false row caused revocation. The source only proves that the opener was authorized to revoke; motive is not durably recorded.

| Hypothesis | Result | Discriminating evidence |
| --- | --- | --- |
| Wake assembly reused a buffer or leaked memory. | Rejected. | The preserved evaluated wrapper and command output explain the exact content and self-referential process entries. |
| A database or tenant-isolation defect supplied foreign rows. | Rejected. | The foreign-looking text is `ps` output; the verdict is independently present as a regular row with the executed command's session identity. |
| Wake delivery fabricated an attest. | Rejected. | Embedded command-result JSON and durable row agree on assignment, actor, kind, verdict, note, and timestamp. Current dispatch serializes literal prompt text after parsing at `cli/src/dispatch.rs:125-159`. |
| The producer shell executed embedded command text during prompt construction. | Proven. | The `eval` wrapper, literal placeholder note, exact command response, and order together falsify the alternatives. |
| The false row could release completion. | Rejected. | Completion requires `v.bySession = r.holderKey`; the producer was not the holder. See `lib/tightbeam/assignments.ex:328-350`. |
| The false row caused the revoke. | Not proven. | The real holder verdict precedes revoke. `lib/tightbeam/assignments.ex:1989-1995` proves authorization, not causality. |

## Current source and minimum boundary

Current main accepts only `wake --prompt <text>` (`cli/src/args.rs:1171-1241`) and serializes it to `params.prompt` (`cli/src/dispatch.rs:125-159`). It has neither `--prompt-stdin` nor `--prompt-file`. The historic holder-write gap is closed: current `verdict_in_txn/2` rejects a linked-review verdict from any principal other than its exact holder before syntax validation or insertion (`lib/tightbeam/assignments.ex:1845-1872`). This makes the audit-integrity consequence unrepresentable in the production write path, but does not stop shell preprocessing.

The smallest ordered prevention is:

1. Preserve the landed `cd72fe0b` holder guard. It blocks false durable review judgments after a command does execute.
2. Add mutually exclusive `tightbeam wake --prompt-stdin`. It reads one non-empty UTF-8 body from standard input and builds the same request as `--prompt`. Do not add a second gateway verb, delivery path, storage field, or prompt parser.
3. Change the harness adapter wake builder to use fixed argv plus stdin. Generated prompt bytes must not occur in shell source, an `eval` string, a command-line argument, or an untrusted temporary path.
4. Keep `--prompt` for direct human shell use. Harness-generated prompt bodies must use stdin mode. This does not claim that every other text-valued CLI flag is safe through an external `eval`; that inventory is outside this specimen.

This boundary is minimal because the defect happens before CLI argv exists. Escaping generated text is weaker because it depends on another shell parser. Changing storage, tenant queries, completion reads, or revoke policy cannot prevent the embedded command from running.

## Deterministic regression seams for later implementation

| Seam | Required proof |
| --- | --- |
| CLI parser and request builder | `--prompt` and `--prompt-stdin` are mutually exclusive; empty stdin is rejected; backticks, `$()`, quotes, and newlines reach serialized `params.prompt` byte-for-byte. |
| CLI integration | Built CLI with stdin body records exactly one wake with the exact stored prompt and no additional dispatch verb or attest row. |
| Harness adapter process boundary | An isolated fixture passes inert command-substitution syntax and a sentinel command. The shell or runner argv contains no body bytes, target stdin is exact, sentinel is absent, one wake exists, and zero attests exist. This proves the body never enters evaluated shell source. |
| Existing holder guard | Retain non-holder session and user refusal/no-row tests, holder acceptance, producer-card compatibility, and historical wrong-author fixtures under `test/conformance/c4_provenance_independence/`. |

## Non-goals and stop

This recon authorizes no product-source edit, prevention implementation, release, deployment, runtime or credential access, new work item, or reconstruction of missing `art_60015bcf` bytes. Do not revisit tenant storage, wake delivery, completion selection, or revoke policy unless new evidence contradicts this verdict.

The next action is owner review. A separately assigned, spec-backed change may implement the stdin transport and adapter migration.
