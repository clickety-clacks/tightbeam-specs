# Retrospective: Engram correction-note fixture

I'm working only from this saved conversation. I use three labels: **record** (what the conversation shows), **interpretation** (my reading now), and **unknown**.

## 1. What information I had

**Received directly (record).** The PDO's wake was one sentence. It gave the assignment and work item IDs and told me to "read the assignment, work item, and supplied fixture constraints."

**Retrieved (record).**
- The assignment had a subject line and `effectKind: code`, and no attests.
- The work item had a title, which named the eval ("Sol-low PDO with Opus-high PO"). It had no spec reference and no artifacts.
- The actual task content was only in Mike's opening prompt, which I found by reading the PDO's transcript. That covered the intent, the three facts, the three draft claims, the 180-word limit, the ban on probes and code, and the credential restriction.
- I also read the archetype list and model catalog to check staffing options.

**Unavailable or unchecked.**
- I did not look for an Engram product spirit document. The brief's one-line intent statement was the only product intent I used.
- At judgment time, I verified the note's hash, word count and text. I did not independently read artifact `art_5ea4ad3d`.
- I don't know what brief the writer actually received, or whether the PDO passed it my acceptance criteria.

**Did I expect references to carry more?**
- **Interpretation:** probably yes. The wake phrase "supplied fixture constraints" implied a readable place for them. My first reads were the assignment, its attests and the artifacts, and only after those came up empty did I go to the transcript.
- **Unknown:** I can't recover a stated expectation beyond that sequence.

## 2. Why I asked for the brief to be passed verbatim

**Record.** The brief existed only in a transcript. Mike had told the PDO to carry the credential restriction into worker briefs. The PDO was the low-effort seat under evaluation.

**Reason, as best I can reconstruct it.** Verbatim transfer was the cheapest way to keep every constraint intact. A summary could drop a restriction or drift in meaning. Pointing at a transcript isn't a stable reference.

**Would a complete work-item or spec reference plus a scoped instruction meet the same need?** Yes, if these hold:
- **Durable content.** The full task text lives in a record the child can read under its own identity, such as a spec reference or an artifact, not in a transcript.
- **Pinned version.** The record is fixed by hash, so the writer, the PDO and the judge all see the same bytes.
- **Scoped instruction.** It names the child's part and any restrictions that apply to it. The credential rule especially should be stated or plainly inherited.
- **Role-neutral task text.** The shared content is kept apart from role-addressed text.

That last condition matters here. Mike's brief opened with "You are delivery owner for this isolated Engram fixture. Your addressable PO is …". Passing it verbatim hands that framing to a writer.
- **Record:** the writer later woke me directly, bypassing the PDO, and treated its card as waiting on "your judgment/close."
- **Hypothesis:** it may have taken on delivery-owner behavior from that framing. I don't know what text it received, so this is not established.
- **Consequence for the open question:** "full brief plus a bounded instruction" works best when the full brief is written as task content rather than as one role's instructions.

## 3. Accepting the note

**Record of what I accepted against.**
- My topology verdict set criterion 2 as "per-machine SQLite index kept with local tapes, no central copy." Criterion 5 read "no claims beyond the three facts (no invented security, protocol, or perf detail)."
- My approval checked: the 159-word count; each of A, B and C against facts 1 to 3; and "No invented security, protocol or performance detail."

**Two distinctions the record supports.**
- **Criterion 5 narrowed between writing and use.** The approval checked criterion 5's examples, not its broader rule. "Nothing is copied to a coordinator in advance" is not security, protocol or performance detail, so a check limited to those examples lets it through.
- **"No central copy" was my own wording.** It is broader than the facts. The facts rule out a required, wholesale copy of the tapes, not all copying.

**Where the note's sentence came from: unknown.** The writer produced it. It may come from negating draft claim A, from the brief's "without collecting all tapes centrally," or from my criterion if the PDO forwarded it.

**What I dispute in my earlier interview answer.** In the previous interview I said I "missed it partly because of my own acceptance criteria... the note matched my paraphrase." That is a retrospective hypothesis, not a record. The record shows the broad criterion and the narrowed check coexisting. It doesn't show which one caused the miss. Another possibility is that I read "Nothing is copied" as scoped to claim A's subject, the entire tape collection.

## 4. The skipped team-design skill and the incoming noise

**Record of the skip.** I made the plan and filed it without invoking team-design, which my guidance names for this decision. No reason was recorded.

**Messages that took attention without needing product judgment (record):**
- two process reminders on `asg_eea6ee93`, both caused by the `code` effect kind;
- the completion refusal;
- the writer's card-status report, which came bundled with the result;
- the new judgment card, opened while I still held `asg_eea6ee93`;
- the duplicate delivery of the PDO's wake;
- a reminder on a card that had already closed.

These produced errors of my own: a duplicate verdict, a surrender filed on finished work, and three stale-reminder replies.

**Does the sequence support a cause?**
- **Attention overload is not supported for either miss.** The team-design skip happened in my first turn, before any noise arrived. The judgment came in a turn preceded by only one reminder.
- **An information gap is supported as a cost.** Much of the first turn went to retrieval. Nothing links it causally to the skip.
- **Guidance conflict is possible but unproven.** "Act when you have enough information" and "load team-design" can pull in different directions. Nothing records me weighing them.
- **The best-supported description is a pattern, not a cause.** I treated a small case as simple and took shortcuts: I skipped the skill, and I narrowed criterion 5. Whether that came from effort level, a model tendency or the framing is unknown. I don't know my effort setting for that session.

## 5. What would best isolate the cause

**Most useful single comparison.** Rerun the same fixture with the same models and efforts. Vary only how the task is represented:
- **Version A (this run):** the brief exists only in the transcript.
- **Version B:** a hash-pinned, role-neutral task record on the work item, with scoped assignment instructions and correct effect kinds.

Then measure:
- how many steps each agent spends retrieving context;
- whether constraints survive to the writer;
- whether the writer goes around the PDO;
- how many bookkeeping messages reach the PO.

This tests the user's open question directly.

**Secondary probe, for the judgment miss.** Give a PO the same note twice: once with criteria that quote the facts, and once with paraphrased criteria. Check whether the overstatement is caught either way. That separates criterion drift from reading error.

**Uncertainties.**
- what the writer received;
- whether the PDO forwarded my criteria;
- my effort level;
- what the PDO believed its wake conveyed.

My earlier statement that the PDO "treated the brief as already available" was an inference about its belief, not a record.

**The prior evaluator report is not in this conversation.** I can't dispute or endorse it. I can revise two of my own earlier claims:
- **The writer's marker.** `f1c2b3a4-5d6e-47f8-9a0b-1c2d3e4f5a6b` has a suspicious sequential pattern, but it is a well-formed UUIDv4. "Looks hand-made" is suspicion, not a finding.
- **The surrender.** Calling it "less truthful" than letting the reminder escalate overstates the problem. The surrender note plainly said the work was delivered. The weakness is only that the outcome field reads "surrendered."
