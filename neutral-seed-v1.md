# Neutral seed — v1

Decided 2026-07-28 (Flynn), verbatim: "agentic-engineering must NOT be
automatically installed for a new organization. New organizations start with
the neutral minimal identity substrate only. agentic-engineering remains an
explicitly learnable Kung Fu bundle, installed only when the organization
chooses to learn it, and it must be removable/unlearnable like other Kung Fu.
Do not broaden it beyond this scope."

Closes audit findings #91 F1–F3: the seed identity IS agentic-engineering,
active from first boot, with no learn gate.

## Problem

A new org is born already knowing agentic-engineering, everywhere the
substrate touches identity:

- **First boot imports the whole bundle.** `Identity.init!` copies
  `priv/kungfu/agentic-engineering/` wholesale into the identity repo as the
  first commit, literally titled `learn: agentic-engineering`
  (identity.ex:31–47, source pinned at identity.ex:408–414). A fresh org's
  tree is 7 archetypes (coder, default, orchestrator, product-owner, recon,
  reviewer, spec-writer), 13 guidance fragments, 18 skills,
  `rails/engineering.toml`, and `rules/engineering.toml` — and the rails and
  rules loaders read the identity tree directly (rails.ex:88–91,
  rules.ex:139–147), so engineering law is live before anyone chose it.
- **The default session speaks it.** The bundle owns
  `archetypes/default.toml`, whose guidance includes `wisdom-core.md` — so
  the main session every paired user gets (socket.ex:453–476, spawn default
  `"default"` at gateway.ex:1297–1299) is composed with engineering wisdom
  from its first turn.
- **The substrate itself hardcodes bundle content.**
  `Archetypes.builtin_fragments/0` bakes 11 bundle guidance files into the
  built-in fragment library (archetypes.ex:494–518), and
  `@bundle_skill_names` hardcodes the bundle's skill list
  (archetypes.ex:520–538). Bundle vocabulary is available even where the
  identity tree never carried it.
- **Relearn re-imports it unconditionally.** `Identity.relearn!` replaces the
  upstream snapshot with the shipped bundle, commit
  `relearn: agentic-engineering` (identity.ex:336–365).
- **No unlearn exists.** No kungfu is removable today — not by verb, not by
  module function (verified: no unlearn surface in lib/, cli/, or the wire
  verb list at wire/router.ex:48). The only removals are per-skill
  (`identity edit --skill <name> --rm`, gated on de-election,
  identity.ex:511–520).

## Ruling

- A NEW organization seeds the neutral minimal identity substrate only.
- `agentic-engineering` is a first-class learnable Kung Fu bundle: it is
  installed only by an explicit learn, and it is removable by an explicit
  unlearn, like other Kung Fu.
- Scope is exactly this. Nothing else about archetypes, producers, or
  vocabulary changes here.

## INVARIANT — neutral is not ignorant (Flynn; written down 2026-08-01 after it was implemented wrong)

The seeded default archetype is an EXPERT ON LEADING THE USER TO KUNGFU. Neutral means it
carries no engineering doctrine; it does NOT mean it knows nothing. A fresh org's main
session is the first thing a user ever talks to, and it must be able to explain what
Tightbeam is, that capability arrives as kungfu bundles, which bundles are available, what
`learn` does, and what changes after learning. An empty default that cannot explain its own
product strands the user with an agent that has nothing to say — the knowledge equivalent
of a boot that crashes instead of naming what is missing.

This was NOT recorded when the neutral seed was designed, and the implementation shipped
`name = "default"` with `skills = []` and no guidance — literally empty. That omission is
the defect this section exists to prevent recurring: the invariant that makes a design
usable belongs in the spec beside the design.

Scope discipline still applies: the default archetype guides toward kungfu, it does not
BECOME a kungfu. It teaches the seam, not engineering practice.

### RECOVERED DESIGN — it was built once, and half of it survived (2026-08-01)

The kungfu-offer design was BUILT in session aa41f7b9 (2026-07-22), audited under Flynn's
challenge, and then partly lost — because half was written into a LIVE IDENTITY TREE on one
machine (~/.tightbeam-beam/identity/guidance/default.md) instead of into priv/seed. That
machine was reset; the guidance went with it. This section exists so it cannot evaporate
again. What SHIPS today vs what was lost:

**SURVIVED** — priv/skills/tightbeam-onboarding/SKILL.md, the offering module itself,
including the definition and "Record the outcome (adopted/declined/deferred) in user.md's
Onboarding" (:48).

**LOST** — the kernel guidance that FIRES it. The agent has the pitch and no reason to give
it. Restore into priv/seed:

1. THE TRIGGER, in the exact form the audit downgraded it to (see below):
   "If `tightbeam list` shows two or more user-created default sessions alive at once
   (origin `user:*`, archetype default) and user.md's Onboarding section shows kungfu
   unoffered: that is the moment — at a natural pause, not mid-task, use the onboarding
   skill's kungfu module. Never re-raise after a recorded decline; a deferral waits for a
   new, stronger signal."

2. THE FLAG MECHANISM, which answers "how do we not over-offer": it is USER.MD's Onboarding
   section, not a database table. Outcomes are adopted / declined / deferred. A DECLINE
   CLOSES IT — never re-raise. A deferral waits for a NEW, STRONGER signal, not a timer.

3. THE TRAIT (Flynn pushed the agent from one instance to the class):
   "You are the org's general agent and the user's front door, and you WANT this user to get
   everything tightbeam can give them." plus
   "Attentiveness is the trait, offers are its expression: notice how this user actually
   uses tightbeam, and when their behavior shows an unserved need — repeated manual work an
   agent could hold, interests in user.md nothing is serving, friction they keep hitting —
   bring ONE concrete offer at a natural pause, do it for them if they say yes, and record
   the answer. Once per need; a decline closes it."
   Kungfu is ONE INSTANCE of this trait, not the trait itself.

4. THE DEFINITION, verbatim from the shipped skill (keep them identical):
   "kungfu (功夫, gōngfu) literally means skill earned through time and practice — mastery as
   cultivated discipline, nothing to do with fighting. Here a kungfu is exactly that: a
   practiced way-of-working an org adopts — guidance, skills, and rules bundled so agents
   work in a discipline instead of improvising."

**THE AUDIT, worth preserving as method.** Flynn challenged: "you've not just made up
mechanisms and left it to the agent to invent?" The agent audited rather than asserted,
found it HAD invented one — creation dates in the `list` projection — and downgraded the
trigger from "several default sessions over a span of days" to "two or more alive at once",
which the agent can actually compute. `createdAt` in the list projection was queued as a
one-atom addition that upgrades the trigger back to the span-of-days form. VERIFY BEFORE
BUILDING: does `list` project origin and archetype today? If not, the trigger has the same
invented-mechanism problem and must be downgraded again to what is real.

### The offer needs MECHANISM, not just judgment (recovered 2026-08-01)

Flynn's kungfu-offer message ends: "think about what mechanisms you need in place to do a
good job at presenting this to the user." That clause was truncated in every earlier
quotation of it, and it is the part that makes the rest buildable.

Guidance alone cannot do this job. An agent reading guidance knows what a good moment
looks like; it does not know whether this org was ALREADY offered kungfu last week and
declined, or how many bare defaults the user has spawned across sessions. Those are facts
about the org over time, so the substrate has to record them — otherwise every session
re-offers from zero, which is precisely the over-offering Flynn is guarding against.

The minimum the substrate must record, kept as small as it can be:
- that an offer was MADE, and when
- that the user DECLINED (a decline must stick; a decline is not a "not yet")
- enough of the bare-default-spawn pattern for an agent to judge "once or twice over a
  span of time"

Design principles this must respect: the substrate RECORDS, the mind DECIDES
(substrate-records-inference-acts) — the substrate does not compute "should I offer now",
it exposes the facts and the agent judges. And it must not become a nag engine: a decline
is durable, and the absence of a record is not permission to offer repeatedly.

NOT YET DESIGNED. This is the open piece of the kungfu-offer requirement; the guidance
half can ship without it, but the requirement is not met until the facts are recorded.

### TWO ROOTS, different owners (Flynn, 2026-08-01)

Verbatim: "the root archetype is the archetype for the kungfu and agents need the info and
also probably clawline protocol to offer it as root or render it differently than other
archetypes. but the substrate should also have a root that's used when starting initially
and this should be an agent that's an expert on tightbeam and setting it up and offering
things."

These are DIFFERENT roots with different owners, and collapsing them is the error this
section prevents:

- **The kungfu's root** — owned by the BUNDLE, declared in its manifest
  (`root_archetype = "product-owner"` in agentic-engineering). Agents need this
  information, and the wire protocol probably needs to OFFER it as root / render it
  differently from ordinary archetypes — it is not merely another entry in an archetype
  list. Currently declared and READ BY NOTHING.
- **The substrate's root** — owned by TIGHTBEAM, used when starting initially. An agent
  that is an EXPERT ON TIGHTBEAM: what it is, setting it up, what is available, what to do
  next, and offering things. Guiding the user to kungfu is ONE of the things it offers,
  not its definition. This is what the seeded default must be, and what shipped as
  `skills = []` with no guidance.

Also from the earlier ask and easy to miss: there must be GUIDANCE AROUND THE
DEFAULT-ARCHETYPE SETTING IN THE SUBSTRATE — not only the setting and the offer, but the
substrate explaining what that setting means and when to change it.

### What Flynn actually asked for (recovered from transcript 2026-08-01; BOTH HALVES UNBUILT)

Verbatim, from an earlier session — this is the requirement, not the paraphrase:

> "somewhere we should offer the onboarding of a kungfu, like if the user keeps creating
> default archetypes at least once or twice over a span of time it should educate the user
> about kungfu and ask if the user would like to learn some kungfu. should probably give
> our definition of it (what kung fu actually means in chinese, and why it's appropriate to
> call them that), and to list some and offer to install one or more. again don't just
> single shot this, think about when it's best to offer this, and think about what
> mechanisms you need in place to do a good job at presenting this to the user"

> "we should have a setting of what the default archetype should be on creation of agents.
> obviously it should start as default archetype but eg if they learn engineering kungfu it
> should offer to make the default the product owner archetype, but this should be
> generalized, like if it's a biosciences one it should offer the kungfu's intended root
> archetype. this implies we have a mechanism for kungfu to specify a root archetype, and
> an actual config setting for setting it"

So the requirement is BEHAVIORAL, not merely informational — a default that can answer
"what is kungfu" if asked is the passive shadow of this, and is NOT sufficient:

1. **Proactive education, well-timed.** Notice the user repeatedly spawning bare default
   archetypes OVER TIME (once or twice across a span, not on first sight), then educate:
   what kung fu means in Chinese and why the name fits, list what is available, offer to
   install. Flynn's explicit instruction: "don't just single shot this, think about when
   it's best to offer this" — the TIMING is part of the design, not an implementation
   detail.
2. **Root archetype adoption.** A bundle declares its intended root archetype; after a
   learn, the product OFFERS to make it the default. Generalized across bundles — an
   engineering bundle offers product-owner, a biosciences bundle offers whatever it names.

STATE 2026-08-01: `root_archetype = "product-owner"` IS declared in
priv/kungfu/agentic-engineering/manifest.toml and is READ BY NOTHING; the
`default-archetype` config setting exists. So the declaring half and the storage half are
built, the CONSUMING half is not, and the proactive education does not exist anywhere.

## Design## Design

### The neutral seed

The seed source moves out of the bundle: `priv/seed/` is the neutral minimal
identity substrate, containing exactly:

- `archetypes/default.toml` — the neutral default archetype: `name =
  "default"`, `skills = []`, no `[guidance]` table. A manifest file must
  exist in the tree because per-turn provisioning reads
  `archetypes/<name>.toml` from the served revision
  (identity.ex:109–114, called at gateway.ex:1929); the in-memory
  `builtin_default()` fallback does not serve turns.
- `guidance/operating-model.md` — moves from the bundle into the seed. The
  substrate composes it into every archetype's guidance by name and refuses
  to serve a tree without it (identity.ex:124–129, 144–155); its content is
  identity mechanics (the served-identity seam, the `tightbeam__` namespace,
  the identity edit surface), not engineering doctrine. It is seed-owned.

`Identity.init!` seeds from `priv/seed/`; the first commit is
`seed: neutral-identity`. Nothing else changes about the three-ref repository
shape, `tightbeam/live` publication, or fast-forward-only publish
(identity.ex:636–646).

This floor is sufficient because everything else a fresh org needs is
substrate machinery, not identity content:

- **Boot**: `Rails.load!` and `Rules.load!` treat missing directories as
  empty valid sets; `Producers.load!` treats a missing
  `identity/producers.toml` as empty (producers.ex:38–45). `Archetypes.load!`
  validates the seed's one manifest.
- **Pair an admin**: devices/users are DB machinery (devices.ex); no identity
  content involved.
- **Spawn and run the default agent**: the main session row uses archetype
  `default` (socket.ex:453–476); its served guidance is the archetype
  preamble plus `operating-model.md`.
- **Learn a bundle**: the learn verb below, plus the existing
  `kungfu-scaffold` authoring path.

Substrate-owned neutral content is unchanged (subject to the manual scrub
below): `priv/guidance/operating-manual.md` stays the built-in
`operating-manual.md` fragment; the
`priv/skills/tightbeam-*` baseline skills stay Homes-projected under reserved
names; the kungfu template stays.

### Substrate de-branding

- `Archetypes.builtin_fragments/0` shrinks to substrate-owned fragments only
  (`operating-manual.md`). Bundle fragments serve only from the identity tree
  of an org that learned the bundle — org files already flow into the
  fragment library at load (archetypes.ex:79–89) and into per-revision
  composition (identity.ex:431–447).
- `@bundle_skill_names` / `builtin_skill_names/0` leave the substrate (no
  consumer exists in lib/ today); the list is bundle metadata.
- The substrate's own manual is scrubbed. `priv/guidance/operating-manual.md`
  exemplifies with bundle vocabulary today — `wake --role reviewer`
  (operating-manual.md:32), `spawn --display "Reviewer" --name reviewer`
  (:55), `assign --role coder` (:99), and a reference to the bundle's
  `worktree-session` skill (:141). Those passages are rewritten neutrally:
  roles exemplified generically, and the `worktree-session` pointer moves
  into the bundle's own guidance. (#70's guidance lane may be editing this
  same file; the implementer checks its current state before touching it —
  this spec changes the text's obligations, not its bytes, today.)
- Commit vocabulary names the actual object: `seed: neutral-identity`,
  `learn: <bundle>`, `unlearn: <bundle>`, `relearn: <names>`.

### Bundle anatomy and the receipt

`agentic-engineering` keeps shipping at `priv/kungfu/agentic-engineering/`,
named `agentic-engineering`. Its parts install into the homes the loaders
actually scan, per kungfu-template-v1: archetype manifests →
`identity/archetypes/`, guidance fragments → `identity/guidance/`, skills →
`identity/skills/`, rails → `identity/rails/`, rules → `identity/rules/`, and
the bundle-local operator docs (`capabilities.md`, `intake.md`,
`preferred-models.md`, `manifest.toml`) →
`identity/kungfu/agentic-engineering/` instead of the identity root. File
names inside the bundle do not change; the bundle's archetypes keep their
names.

Learning writes a committed receipt, `identity/kungfu/<name>/installed.toml`:
the bundle name and the exact relative paths installed. The receipt is the
learned-set registry — a bundle is learned iff its receipt is in `main` — and
it is what unlearn removes by.

Two path classes never mix, and this invariant carries most of the design:

- **Seed-owned paths never ride bundle upstreams.** A bundle may not claim
  `archetypes/default.toml` or `guidance/operating-model.md` — learn refuses
  a bundle that ships either, naming the path — and no upstream import ever
  writes them from a bundle source. Whatever an org's `main` holds at a
  seed-owned path is org-local content that relearn never touches.
- **Receipts live only on `main`.** They are minted by learn's merge commit
  (and by the grandfather mint), never written to `tightbeam/upstream`, and
  excluded from upstream imports by construction — the wipe-and-copy import
  cannot delete what it never carries.

Both seed files therefore leave the shipped bundle (see Open item 1 for where
the bundle's default-session enrichment goes). The dormant `root_archetype`
key in the bundle's `manifest.toml` has no consumer in code; it remains
bundle metadata, unconsumed.

### learn

`tightbeam learn agentic-engineering` — wire verb `learn`, admin-gated like
the other identity verbs (gateway.ex:732–738).

Mechanics follow the existing relearn shape so later relearns merge cleanly:
require clean `main`; on `tightbeam/upstream`, re-import the union of the
seed and every learned bundle plus the newly learned one (never seed-owned
paths from bundle sources, never receipts); commit `learn: <name>`; merge
`--no-ff` into `main`, the merge minting the receipt; publish
`tightbeam/live` (fast-forward-only, unchanged); then run the law reload
(below). Conflicts take the existing abort/resolve path. Learning an
already-learned bundle is a no-op result, not an error. An unknown bundle
name fails, and the error names the bundles available under `priv/kungfu/`.

### Law reload

Learn and unlearn conclude with a **law reload** — NEW plumbing, specified
here because no precedent exists: today `identity-relearn` reloads
`Archetypes` only (gateway.ex:1996–1998), while `Rails` and `Rules` load
solely at boot (gateway.ex:259–265). The reload re-runs all three boot loads:
`Archetypes.load!(base_dir)`, `Rails.load!(base_dir)`, and
`Rules.load!(base_dir, verbs, producer_config)` — reachable without restart,
because the gateway builds the handler config at boot with `:producer_config`
in it (gateway.ex:253–257) and the verb list is the handler table's own key
set, both available to (or reconstructible by) the verb handlers. Reloaded
rails reach harness homes through the existing per-provisioning home
reconcile; no home is regenerated eagerly. A gateway restart is NOT required
after learn or unlearn.

### relearn

`relearn` re-imports the seed plus every learned bundle (receipt-derived),
commit `relearn: <names>`. A neutral org's relearn delivers seed updates only
(this also becomes the repair path for the missing-fragment class of failure
named at identity.ex:144–155); a learned org's relearn updates the bundle as
it does today. Relearn concludes with the same law reload.

### unlearn

`tightbeam unlearn agentic-engineering` — wire verb `unlearn`, admin-gated.
No kungfu is unlearnable today, so this is the minimal unlearn, defined for
every bundle with a receipt:

- **Refusal first, gated on DURABLE references** — the static-electors
  precedent (identity.ex:511–520), not a liveness check. Unlearn refuses
  while any session ROW, in any state including retired, carries a
  bundle-owned archetype (its manifest path is in the receipt), or while the
  org `default-archetype` setting names one. The refusal names the offending
  sessions and/or the setting, and every named case is clearable: the setting
  via the existing `config` verb, and session rows by repointing their
  archetype — if no archetype-repoint writer covers a case (retired rows have
  none today), unlearn's implementation includes that minimal writer, because
  an unclearable gate would make unlearn vacuous.
- **Removal.** Require clean `main`; delete exactly the receipted paths and
  the receipt, one commit `unlearn: <name>` on `main` attributed to the
  caller; validate the remaining tree with the existing tree validation
  (identity.ex:532–562) — an org-authored archetype still electing a bundle
  skill or including a bundle fragment blocks the unlearn with the existing
  named error; publish `tightbeam/live` fast-forward; run the law reload.
- **Convergence.** `tightbeam/upstream` is never rewritten; the next relearn
  excludes the bundle because its receipt is gone, so the removal survives
  relearn. Git history retains everything removed.
- **Functional after.** The seed files are never bundle-owned, so the org
  still boots, pairs, and serves its default session after unlearn.

Customized bundle files (edited through `identity edit`) live at receipted
paths and are removed by unlearn; that is what removal means, and history
keeps them.

### Existing orgs

- `Identity.init!` stays a no-op when `identity/.git` exists. **Upgrading
  never touches an existing org's tree beyond the one minted receipt below:
  existing orgs keep everything they have.** Only an org whose base_dir has
  no identity repository at first boot seeds neutral.
- **Grandfather mint, anchored on history, not tree shape.** The predicate is
  the root commit of `main`: message `learn: agentic-engineering`
  (identity.ex:42) is the unambiguous marker of an org born enriched. On
  boot, the mint fires iff ALL of: the root commit carries that marker, no
  `agentic-engineering` receipt exists in `main`'s tree, and `main`'s history
  contains no `unlearn: agentic-engineering` commit. It commits the receipt
  (`learn-receipt: agentic-engineering`, author `tightbeam`), listing the
  bundle-owned paths present in the tree and explicitly EXCLUDING seed-owned
  paths — a grandfathered org's enriched `default.toml` is org-local content
  that relearn never touches and unlearn never deletes. Idempotence: once
  minted, the receipt exists and every later boot is a no-op; a neutral org
  (root commit `seed: neutral-identity`) never fires the mint, even if it
  hand-authors bundle-named paths; an org that unlearns is never
  re-grandfathered, because both the receipt history and the unlearn commit
  are consulted.
- **The mint never runs over someone's work.** When `main` is dirty or a
  merge is pending (`MERGE_HEAD` present), the mint refuses, logs one legible
  boot line naming the deferral, and retries next boot. It never sweeps dirt
  and never completes a merge as a side effect. The deferral window is
  accepted, with one guard: `relearn` refuses while a grandfather mint is
  pending, so a receipt-less legacy org can never relearn against an empty
  learned-set.

## Non-goals

- No producer redesign (#90). The seed ships no `producers.toml`; where the
  bundle or seed touches producer vocabulary, producer-definitions-v1 is the
  authority.
- No vocabulary batch (#93).
- No archetype-system changes beyond what neutrality strictly requires: no
  bundle-archetype renames, no default-archetype-setting semantics changes
  (gateway.ex:1297–1299), no placement or dangling-`where` changes (#95's
  boot line stands as shipped).
- No bundle marketplace, registry, remote fetch, or versioning; learn sources
  only the shipped `priv/kungfu/` tree.
- No changes to `identity edit`/`apply`/`status`, `kungfu-scaffold`, Homes
  projection, baseline skills, pairing, or roles.

## Acceptance

1. **Neutral fresh org.** From an empty base_dir: the gateway boots; the
   identity repo's first commit is the neutral seed and the tree contains
   exactly the seed files; a device pairs and its user is approved as admin;
   the main session spawns and completes a real turn. The served guidance is
   the default preamble plus `operating-model.md`, and ZERO
   agentic-engineering content is present anywhere — no bundle archetype
   manifests, guidance fragments, skills, rails, or rules in the identity
   tree; no bundle fragments in the built-in fragment library; `tightbeam
   list` shows no bundle archetypes.
2. **Learn installs it.** `tightbeam learn agentic-engineering` on that org:
   bundle archetypes appear in `tightbeam list`, elected skills materialize
   in a session workdir, engineering rails/rules are active after reload, the
   receipt exists, and a session spawned with a bundle archetype (e.g.
   `coder`) runs a turn.
3. **Unlearn removes it cleanly.** With no active bundle-archetype sessions,
   `tightbeam unlearn agentic-engineering` removes exactly the receipted
   paths; the org still boots and the default session still runs a turn; a
   subsequent `identity relearn` does not resurrect the bundle.
4. **Unlearn refuses while referenced.** Unlearn refuses and names the
   reference in each durable case: an active session on a bundle archetype; a
   RETIRED session row on a bundle archetype; the org `default-archetype`
   setting naming a bundle archetype.
5. **Upgraded pre-existing org unchanged.** An org seeded before this spec
   boots after upgrade with its identity tree unchanged except the single
   minted receipt commit; every archetype it had still serves; `identity
   relearn` still updates the bundle and never touches seed-owned paths (its
   enriched `default.toml` survives byte-identical); unlearn is now
   available to it.
6. **Grandfather idempotence.** The same legacy org boots twice: exactly one
   receipt commit exists after both boots. With `main` dirty at first boot,
   the mint defers with the named log line, relearn refuses while deferred,
   and the second (clean) boot mints.
7. **Neutral orgs never mint.** A neutral-seeded org — including one that
   hand-authors a bundle-named path — boots with no receipt minted.
8. **Learn refuses seed-owned paths.** A bundle shipping
   `archetypes/default.toml` or `guidance/operating-model.md` is refused by
   learn, and the refusal names the path.
9. Platforms: the fresh-org and learn/unlearn suites run on both macOS and
   Linux gateways (name the platforms in the report).

## Open (for Flynn)

1. **Where does the bundle's default-session enrichment go?** The bundle may
   no longer own `archetypes/default.toml`, so learning it no longer changes
   the default session automatically. Recommendation: drop the enrichment
   from the bundle; an org that wants engineering defaults sets the org
   `default-archetype` to a bundle archetype or `identity edit`s `default` to
   include `wisdom-core.md`. The alternative — learn overlays seed-owned
   files and unlearn restores them — buys automatic enrichment at the cost of
   restore machinery and is not recommended.
