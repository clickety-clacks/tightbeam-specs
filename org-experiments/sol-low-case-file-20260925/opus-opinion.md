# Independent analysis: the Sol-low PDO / Opus-high PO correction-note run (`wi_ce29ea6e`)

## Model and scope

- **Model:** Claude Opus 5.5 (`claude-opus-5-5`), running as a fresh session. This is the same model family as the PO under review, so weigh my view of the PO with that in mind.
- **Tools:** read-only file tools only, all inside the case directory. I ran no commands, did not verify file hashes, and contacted no one.
- **Read in full or in the relevant parts:**
  - `case-file.md`
  - the task (E1) and the delivered note (E2)
  - the work-item result and trace
  - the PDO public trace (lines 1–78)
  - the writer trace (lines 1–13) and the writer and PO call/reply audits
  - selected PO trace lines
  - the PDO's received context (`s_2541a786-developer.txt`)
  - the historical `pdo.md`, `product-owner.md`, `delivery-coordination.md`, parts of `operating-manual.md`, `team-design/SKILL.md`, `default.toml`, `topology.toml`
  - the installed dispatching skill and its match receipt
  - all three new interview prompts and answers, and `verification.json`
  - the original PO interview prompt and both original interview answers (the PDO's from its trace line 78, the PO's from its audit)
  - `eval-report.md`
- **Not read:** `turns-timeline.json`, `delivery-metrics.json`, `evidence-manifest.json`, `pdo-received-guidance.json`, `original-seats-readback.json`, the interview invocation receipts and run logs, and most engineering/model guidance.
- All times below are UTC on 2026-09-24. Paths are relative to the case directory.

## Short answer to your question

**Neither "re-brief each child" nor "just point at the work item" worked here.**
- The PDO's paraphrased brief lost content.
- The pointer led to records that were empty. The work item has only a title, and `specRefName` and `specRefSha256` are null (`evidence/work-item-result.json:117-120`).
- The children filled the gap by reading the PDO's transcript. That found the facts, but it also carried over an instruction addressed to someone else, which the writer then acted on.

**What the evidence supports** is one authoritative, role-neutral, hash-pinned task document, plus a short instruction for each child. That instruction should state the child's part, output location, who to report to, and its effect kind.

**No new feature is needed for that.** In this build, a work item cannot carry a body, but `artifact-record --work-item --sha256` and `--spec-ref` at creation already exist (`evidence/pdo-public-trace.jsonl:45`, the CLI help). Cross-session file reads on the same host worked in this run.

**One product fix does look necessary.** When `--effect-kind` is omitted, assignments silently become `code`. Meanwhile, three guidance pointers send agents to a skill that says nothing about effect kinds.

## What happened (main points)

| Time | Event | Evidence |
|---|---|---|
| 19:23:01.9 | Intake opens for the PDO. The PDO's single turn runs from here to 19:27:55.5 | `work-item-trace.json:92-103, 533-544` |
| 19:23:36 | PO consultation opened without an effect kind, so it became `code` | `pdo-public-trace.jsonl:12-13` |
| 19:23:41 | Wake to the PO: "read the assignment, work item, and supplied fixture constraints." No content | `:14` |
| 19:23:54–57 | PO checks artifacts (none), then reads the PDO transcript for the facts | `s_51682b82-claude-audit.json:43,51` |
| 19:24:36 | PO topology verdict: one Sonnet writer; "Writer brief carries the PDO brief verbatim"; 5 criteria, #2 "no central copy"; the PDO forwards the note | `:91` |
| 19:24:41 | PDO reads that verdict | `pdo-public-trace.jsonl:27-28` |
| 19:24:52.8 | The PO's wake to the PDO ("…Wake me with the note path and sha256…") is stored in the PDO transcript, but the PDO does not receive it until 19:27:55 | `writer-public-trace.jsonl:13`; `pdo-public-trace.jsonl:70` |
| 19:24:52–58 | Writer card opened as `code`. Wake contains no facts, no claims and no report-to role | `pdo-public-trace.jsonl:31-33` |
| 19:25:02–12 | Writer tries: attests; two nonexistent commands; `work-item-get`; its own transcript; a transcript read with a role string (not found); then the PDO transcript by real key, which has the facts and the PO's "Wake me" | `writer-public-trace.jsonl:2-13` |
| 19:25:35 | Writer wakes `product-owner:…` "as instructed" and calls it "the PDO" | writer audit `:96, :139, :143` |
| 19:25:45 | Writer's self-wake: "Check whether the PDO (product-owner:…)" | `:103` |
| 19:25:42–48 | PDO finds the note by polling; checks 159 words and the sha256 | `pdo-public-trace.jsonl:38-41` |
| 19:26:08.7 | PO records spirit-approved on the original consultation card | `work-item-trace.json:236-242` |
| 19:26:13–19.9 | PDO tries `--effect-kind none` (rejected), then opens a second PO judgment card | `pdo-public-trace.jsonl:46-49` |
| 19:26:33–42 | PDO revokes the writer's `code` card and opens an `evidence` card | `:52-57` |
| 19:26:47 | PO records a duplicate verdict, completes the new card, surrenders the old one | PO audit `:195` |
| 19:27:22–32 | Writer retired, intake completed truthfully, work item closed | `pdo-public-trace.jsonl:63-68` |
| 19:27:55–19:28:16 | Queued PO messages finally reach the PDO; it reconciles them correctly | `:70-76` |

## Issue-by-issue analysis

### 1. Missing brief

**Observed**
- Neither handoff carried the facts or claims A–C (`pdo-public-trace.jsonl:14, :33`).
- This happened even though the PDO's own guidance asks for them:
  - "Give it the outcome, constraints, relevant evidence" (`s_2541a786-developer.txt:493-494`)
  - "Give specialists the outcome, authority, inputs" (`:520-521`)
  - "Pass the actual delivery standard" (`:556`)
- The PO's plan, which the PDO read at 19:24:41, required the brief verbatim. PDO guidance says "You cannot amend [the plan]" (`:501`).

**Strongest account.** Several things combined:
- The dispatching skill the PDO loaded prescribes "a brief of AT MOST ONE SENTENCE plus the references… read the assignment, its attests, and the work-item from the substrate" (`installed-tightbeam-dispatching-SKILL.md`, verified against the tool result by `dispatch-skill-match.json`). That example assumes the task content already lives in those records. Nothing tells the dispatcher to make sure it does when the intake arrived only as a message.
- The PDO followed the pointer pattern without checking the pointer.
- The PDO did not act on the explicit PO requirement.

The guidance is not strictly contradictory: a one-sentence wake could have pointed to a brief file. It does have an unstated precondition that this run violated. The agent-level miss is also real, because the PDO had a clear and specific instruction from the PO.

**Alternatives**
- *Inherited context in the child.* The PDO's new interview raises this (`interviews/pdo-answer.md:27`). The record rules it out for this run: the writer said "no facts arrived directly in my dispatch" (writer audit `:143`), and its trace shows it retrieving them.
- *Low effort contributed.* Plausible, but not something one run can show.

**Confidence:** high on the mechanism; the relative weight of each cause cannot be determined.

### 2. Role/address confusion and the bypassed delivery owner

**Observed**
- The writer woke the PO, and three times called `product-owner:engram-sol-low-eval-20260924` "the PDO".
- The only instruction to "wake… with the note path and sha256" that the writer ever saw was the PO's message addressed to the PDO. The writer read it in the PDO's transcript (`writer-public-trace.jsonl:13`).
- The PDO's wake never told the writer where to report (`pdo-public-trace.jsonl:33`).

**Strongest account.** Three things together:
1. There was no role-specific reporting instruction.
2. Reading another session's transcript as the brief brought in an instruction meant for someone else. The transcript showed the PDO's inbox, including a message the PDO itself had not yet received.
3. The writer mixed up the names "PDO" and "product-owner".

The writer's action literally matched "Wake me" from the PO. So "bypass" overstates any intent to go around the PDO.

**Alternatives**
- *The writer was simply "unreachable" from the PDO.* Not supported. The failed call was `transcript --session "agent:pdo:…"` (`:10-11`). It was followed 1.5 seconds later by a successful read using the real key, and the writer never tried `wake --role pdo:…`.
- *The writer absorbed delivery-owner framing from the intake* (the PO's hypothesis, `interviews/po-answer.md:37-38`). The writer did read that framing, but its own words point to the "Wake me" line.
- *The `default` archetype confused the writer's sense of its role.* That archetype tells a session it is "the user's general Tightbeam agent… front door" (`archetypes/default.toml:17-33`). This is a possible contributor but untested.

**Side effect.** The writer's misrouting was hidden by the PDO's polling. Had the PDO yielded, it would have heard about the note only when the PO forwarded it (19:26:16).

**Confidence:** high that the PO's instruction leaked to the writer and that it conflated the names; moderate on how much each contributed.

### 3. Effect kind and its default

**Observed**
- Two of four child cards defaulted to `code`, which triggered `completion-requires-review` and led to three recovery or replacement cards.
- Three guidance pointers say effect classification lives in `tightbeam-dispatching` (`s_2541a786-developer.txt:205, :554`; `product-owner.md:96`), but the installed skill never mentions effect kinds.
- The CLI help shows `[--effect-kind <kind>]` with no default and no allowed values (`pdo-public-trace.jsonl:43`). The values appeared only in an error message (`:47`).
- The manual's `assign` example leaves the flag out (`developer.txt:889`).
- The PDO did have the cue "coordination consultation" (`:493`), and it did not check the help before its first `assign`.

**Strongest account.** The tool design and the guidance pointers are major contributors: a silent, restrictive default plus a pointer to content that does not exist. The PDO's own assumption that the tool would infer an effect kind (`pdo-public-trace.jsonl:78`) is also real.

The evaluator's framing ("no supporting instruction", `eval-report.md:47`) is accurate but leaves out the missing guidance content.

**Confidence:** high.

### 4. Duplicated work, polling and noise

**Observed**
- The PDO slept and polled for about 90 seconds inside one long turn (`:17-26, :36-39, :59-60`). As a result, every PO message queued until 19:27:55. The PO→PDO channel carried nothing during the run.
- The second PO judgment card (19:26:19.9) was opened 11 seconds after the PO had already recorded a verdict on the first card. The PDO's last read of that card was at 19:24:41.
- Opening a new `coordination` card was a defensible workaround for a `code` card that could not complete. The error was not re-reading first. Guidance says "Reuse an open PO judgment assignment" and "Reconcile… before creating a replacement obligation" (`developer.txt:558, :575-576`).
- **Not noted anywhere in the prior reports:** substrate prods caused some of the "noise".
  - A prod reached the PO right after a verdict-only turn (`work-item-trace.json:115-131`).
  - A prod reached the writer right after it filed progress (`:184-201`).
  - Prods fired about 1.6–2.5 seconds after new cards were opened (`asg_647c7a07` at `:265-283`; `asg_5ccaa965` at `:325-343`). The second fired before the PDO's wake reached the writer, with the text "Your turn ended with no filing…" (`writer-public-trace.jsonl:36`).
  - The manual says plain self-wakes "do not cover an assignment" (`operating-manual.md:82-84`), while the skill says "scheduled wakes pause it". Those two statements are inconsistent.

**Strongest account.** The PDO polled instead of yielding, as the manual directs (`:76-80`), and did not re-read before opening a new card. The substrate's prod timing and the effect-kind churn made the traffic worse.

**Confidence:** high on the PDO's part; moderate on the prod mechanism. Whether those prods are designed behavior or a defect is unverified.

### 5. The skipped planning skill

**Observed.** The PO's recorded calls include no team-design invocation, although its guidance says to load it (`product-owner.md:38-39`). The skip happened in the PO's first turn, before any noise arrived, so attention overload is ruled out, as the PO's new interview correctly notes.

**Did it matter?** Probably very little. The skill's content (`team-design/SKILL.md`) matches the plan the PO produced anyway: smallest process, "put each job where the context it needs already is", name each child's outcome, authority and evidence. It says nothing about effect kinds or brief storage.

**Assessment:** a guidance-compliance lapse with no demonstrated effect on the outcome.

### 6. Factual drift accepted by the PO (and other content issues)

**The note.** It corrects A, B and C substantively and stays within the limit. It has four weaknesses:
- **(a) Claim A:** "Nothing is copied to a coordinator in advance" is broader than facts 1–2, which only rule out needing the tape collection copied centrally. Read in context it will probably be understood as referring to the tapes, but a correction note held to the authoritative facts should not overstate.
- **(b) Claim B:** "The same tape ID on two machines is not the same result" implies an ID collision that no fact states.
- **(c) Claim B** drops "not a central filesystem path".
- **(d)** The requirement to "explain each material correction" is only thinly met.

**Where the PO's miss came from.**
- The PO's first verdict restates criterion 2 as "no advance copy" (PO audit `:163`). That echoes the note's sentence in the wording of the PO's own loose paraphrase. The record therefore shows the PO read the sentence and matched it to criterion 2; it was not simply overlooked.
- The PO checked criterion 5 ("no claims beyond the three facts") only against its listed examples.

**Where the writer's wording came from.** The writer never saw the PO's criteria: the PDO's wake had none, and the writer never read the attests on the consultation card. The PO's criterion therefore did not cause the writer's wording. The two agents drifted in parallel, probably by negating claim A and generalizing from the intent line "without collecting all tapes centrally".

**Severity:** a real defect that needed a one-line fix. The evaluator's "Failed" (`eval-report.md:30`) is too binary; "revise before acceptance" fits better.

## What went right

- **PDO:**
  - consulted the PO before staffing, which satisfied `topology.toml`
  - did not write the note itself
  - staffed exactly the planned model, host and count, as a dedicated temporary session
  - independently checked the word count and sha256
  - never fabricated a review
  - revoked and replaced the misclassified card with evidence preserved
  - retired its hire, filed a truthful completion (`:65-66`) and closed the item
  - reconciled stale queued messages correctly (`:71-76`)
- **PO:**
  - recovered the facts on its own
  - recorded a clear plan with criteria in a durable verdict
  - refused to invent a reviewed-clean record (audit `:115`)
  - checked the note's location and hash
  - caught the dropped B clause
  - treated stale reminders as stale
- **Writer:**
  - recovered the facts in about 10 seconds
  - got the core corrections right
  - recorded the artifact with its path
  - filed progress instead of faking completion
- **Boundaries:** I found no credential-file reads in the traces.

## How the evaluator and fixture setup contributed

- **Task content lived only in a role-addressed intake message.** The driver created the work item with no spec reference. That is a fair test of whether a PDO makes content durable, but it mixes that test with how the task was represented.
- **The work-item title** "Eval: Sol-low PDO with Opus-high PO…" was visible to every agent (`writer-public-trace.jsonl:7`). The PO cites "the PDO was the low-effort seat under evaluation" as a reason for requiring the brief verbatim (`interviews/po-answer.md:26`). That is an observer effect.
- **Original interviews were leading.** New interviews mention your hypothesis. Tools were disabled, so the PDO and PO could not check traces. That explains some over-corrections below.
- **Environment:** the silent effect-kind default, the prod timing, and transcripts showing a session's not-yet-delivered messages to third parties.

## Claims that are misleading or too confident

1. **Original PDO interview:** the skill "showed `--effect-kind` as optional". False: the skill never mentions it. The evaluator caught this.
2. **New PDO interview:** calls transcript recovery "too certain" and offers inherited context as the strongest alternative (`pdo-answer.md:11, :27`). The writer trace contradicts this. It over-corrects.
3. **New PO interview:** lists the source of the writer's wording as possibly "my criterion if the PDO forwarded it" (`po-answer.md:51`). The trace rules this out. Its retreat to "unknown" (`:53`) understates the "no advance copy" echo in its own verdict.
4. **New writer interview:**
   - Presents its B wording as including "not a central filesystem path" (`writer-answer.md:5`); the note omits it (note line 7).
   - Presents a considered reading of delegated authority (`:7`), while its run-time text simply calls the PO "the PDO".
5. **Writer's evidence completion attest** (writer audit `:117`) says the old card "remains open" and "PDO notified by wake w_5099b9ae". The card had been revoked, and that wake went to the PO. The PDO then cited this attest as evidence (`pdo-public-trace.jsonl:65`).
6. **Evaluator report:**
   - "approved it twice" describes one judgment recorded on two cards 38 seconds apart, not two independent approvals.
   - It omits the leaked instruction, the prods and the dangling effect-kind pointers.
   - It does not flag the thin explanations in the note.
7. **Case file:** I found it accurate. Its key cautions (the failed transcript lookup was not a failed wake; the PO's acknowledgment was prompted) are borne out.

## The architecture question in detail

**What the recorded tools support**
- Work item: title plus an optional spec reference and hash, set only at creation (no update command in the help).
- Assignment: subject, advisory files, effect kind.
- `artifact-record` with work item and sha256 — the writer used it successfully.
- Workdir files readable across sessions on the same host, as the PO's direct read of the note in the PDO's workdir shows.
- The PO's first retrieval step already included `artifacts --work-item` (audit `:43`). A recorded brief would have been found. The writer's path did not include that step, so the wake must name the brief.

**What failed**
- The content never became a durable record.
- The pointers pointed at nothing.
- The substitute, a live transcript, is unstable: it grew between the PO's read and the writer's read.
- A transcript mixes in instructions addressed to other roles.

**Shared task material (role-neutral, pinned by hash):**
- the intended outcome
- the authoritative facts and the items to correct
- deliverable form and limits (≤180 words; corrected text plus an explanation for each)
- prohibited effects and the credential rule that apply to all workers
- the PO's acceptance criteria, written to cite fact numbers or quote them rather than paraphrase

**Role-specific instruction (per child, short):**
- who you are and which part you own ("claims A–C", "part 6")
- output path
- who to report to and how
- the card's effect kind
- lifecycle (retire after the verdict)
- restrictions the user asked to be repeated

Delivery-owner-only lines such as "You are delivery owner…", "Keep PDO and PO available" and "Carry this restriction into worker briefs" do not belong in a writer's material. Sending the raw intake verbatim would pass them along.

**Is a new feature needed?** Not demonstrated. Two small conveniences — attaching a spec reference after creation, and listing artifacts in `work-item-get` — are worth considering only if a comparison shows children failing to find a named pointer. The effect-kind default is the one fix I would not wait on.

## Ranked changes and comparisons

1. **Tool/guidance fix (low cost, high confidence).** Make `assign` and `dispatch` require `--effect-kind`, or at least report the `code` default and the allowed values. Add a short effect-kind table to `tightbeam-dispatching`, where three guidance pointers already send agents. This repairs a dangling reference; it is not a new mechanism.
2. **Representation convention using existing tools (guidance, low cost, medium-high confidence).** When content arrives only in a message, the first owner writes one role-neutral brief and records it with `artifact-record --work-item --sha256`. Each child's wake stays one sentence: assignment, brief path and hash, scope, report-to role. Update the skill's example to say the pointer must resolve to the content.
3. **Controlled comparison (evaluation design, moderate cost; answers your question).**
   - Same fixture, models and efforts. Neutral work-item title. Effect kinds handled identically in both arms.
   - Vary only the intake: message only, versus message plus a pinned role-neutral brief referenced from the work item.
   - At least three runs per arm.
   - Measure: retrieval hops, reads of other sessions' transcripts, whether constraints survive, misaddressed wakes, unsupported statements, and whether the PO catches them.
   - The PO's proposed comparison (`po-answer.md:77-79`) changes representation and effect kinds together, so it is confounded.
   - Optional third arm: verbatim raw intake, to test the role-framing leak.
4. **Substrate check (cheap, no evaluation).**
   - Confirm the prod rules: whether verdicts, progress rows and plain self-wakes count.
   - Find out why prods fire about 2 seconds after a card opens, before the opener's wake.
   - Decide whether third-party transcript reads should show undelivered inbound messages.
   - Fix whatever is wrong; document whatever is intended.
5. **Offline PO probe (cheap).** Give a PO the same note several times, once with criteria that quote the facts and once with paraphrased criteria. This separates drift in the criteria from misreading.

Only after these would I compare PDO effort levels (Sol low versus medium) with representation held fixed.

## What would falsify these explanations, and what cannot be settled

**Falsifiers**
- In the pinned-brief arm, children still read other transcripts or drop constraints → representation is not the main cause.
- The writer, given an explicit report-to role, still wakes the PO → name conflation or the `default` archetype identity, not the leaked instruction.
- With the default fixed, the PDO still misclassifies effect kinds → attention or capability.
- A PO given fact-quoting criteria still approves the absolute → judgment, not criterion drift.
- The prod rules turn out to be correct by design → the noise is a documentation problem.

**Cannot be settled from this record**
- the agents' internal reasoning
- any contribution from effort level
- whether the result generalizes beyond one tiny task with mixed models
- whether the writer received the operating manual
- whether artifact paths are readable across hosts
- how children would resolve a spec-reference name to its bytes

## Plain-language assessment

This doesn't look like incompetence. The task facts existed in exactly one place, a chat message to the PDO.

The PDO followed a "short pointer" habit and pointed its helpers at records that were empty, even though the PO had explicitly asked it to pass the facts along. Both helpers dug the facts out of the PDO's chat log. The writer also found a note there that the PO had written to the PDO ("wake me with the path"), took it as its own instruction, and called the PO "the PDO" while doing so.

A hidden default that labels every assignment "code" caused most of the extra cards and reminders. The PDO's in-turn polling meant it never received the PO's messages until the end.

The note is mostly right. It has one overstated sentence, which the PO accepted because it matched the PO's own loosely worded checklist.

Your instinct is right in direction: give children one shared source plus a scoped instruction, rather than rewriting the brief each time. But the shared source has to be a real, pinned document with no role-specific instructions in it. The current tools can already hold that as an artifact; the work item itself cannot. Fix the effect-kind default, adopt the brief-document habit, and run one clean comparison before building anything new.
