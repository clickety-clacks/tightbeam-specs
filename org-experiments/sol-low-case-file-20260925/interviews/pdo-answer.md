1. At the time, I treated the original user assignment, its transcript, and `wi_ce29ea6e` as one durable context bundle. The short-wake skill reinforced that assumption by telling dispatchers to send a one-sentence pointer and have the recipient read “the assignment, its attests, and the work-item.”

That belief was only partly supported. The original assignment transcript contained the complete facts, claims A–C, and constraints. The work item itself appears to have held only its title and linked records. I did not verify that the PO or writer could retrieve the original user text by following the work-item reference. The successful note proves the writer obtained the facts somehow; it does not prove the work item supplied them.

2. The PO’s topology verdict explicitly required the writer brief to carry the fixture facts, claims, word limit, and restrictions verbatim. I read that verdict before dispatching the writer. I nevertheless sent this bounded wake:

> “write the <=180-word note … from supplied facts only … never read .tightbeam-session…”

The assignment subject only named the output file. I let the skill’s “AT MOST ONE SENTENCE plus references” pattern dominate the PO’s concrete content requirement. That was the wrong reconciliation. A short wake could have pointed to a complete brief artifact; it did not justify omitting the brief entirely.

My earlier interview stated that the worker “consequently recovered the actual content from transcript context.” That was too certain. The visible evidence shows a sparse wake followed by a correct note. It does not reveal exactly how the worker obtained the full source text.

3. Pointing only to the actual work item plus “write the correction note” was insufficient in this run. The shared record lacked a retrievable brief containing facts 1–3, claims A–C, and the restrictions.

The minimal missing preparation was one authoritative brief stored somewhere both sessions could read, linked from the work item or named in the assignment. A file in the PDO workdir with the verbatim request, plus a one-sentence wake identifying that path and the scoped task, would have satisfied both needs.

The installed `work-item-create` interface exposed a title and optional specification reference/hash, not an arbitrary body field. Assignments similarly offered subjects and advisory file lists. Therefore, “complete shared work item plus ‘work on part 6’” could work as an organizational pattern only if the item reliably linked to a complete shared artifact. This run did not establish that arrangement.

4. Several causes differed:

- **Effect kinds:** primarily my mistaken tool model. I inferred that omitted `--effect-kind` would be classified appropriately because the option was syntactically optional and examples omitted it. No instruction promised inference, while the PDO core expressly called the PO step a coordination consultation. After the refusals, the records showed the actual default was `code`. The guidance was somewhat easy to misread, but the unsupported assumption was mine.
- **Repeated checking:** I misunderstood execution timing. I polled PO transcripts and attests while notifications were queued behind active turns. The checks were not needed and did not accelerate delivery.
- **Duplicate judgment:** I failed to re-read the original PO card immediately before opening a new judgment card. The original card already received a `spirit-approved` verdict before I opened the second assignment. This was stale-state handling, not missing product context.
- **Messages to the PO:** the initial topology request and final judgment request were required. The second judgment request duplicated work because I had not reconciled the latest record.
- **Recovery cards:** these followed from the incorrect effect classifications. The recovery itself truthfully preserved evidence and avoided fabricating reviewed-clean verdicts.

5. The strongest alternative explanation is that the handoff was effective by design: a spawned child may have received enough inherited session context, or may have had a supported route from the referenced work item to the originating assignment, making repetition unnecessary. The correct note and PO decision are compatible with that explanation.

The present record cannot distinguish that from the worker independently locating my transcript or receiving hidden inherited context. A small comparison run could: create two otherwise identical temporary workers with fresh context. Give one only a work-item reference whose item contains merely a title; give the other the same reference plus a linked verbatim brief artifact. Ask both to extract one exact supplied fact and report which source they read. Inspect only their visible inputs and cited source. That would test record reachability without assuming that repeated prose is always necessary or always wasteful.