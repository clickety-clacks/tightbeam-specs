# Kungfu template + author scaffold — v1 (KP2)

Status: READY-TO-HAND-OFF r3 (Fable-authored 2026-07-23; Fable review r2 confirmed all 3
blockers closed; r3 applies the trailing-hyphen nit). Handoff to Sol queued behind the
P4/P5/P6 spine. Roadmap: KP2 — "template bundle exists, loads clean,
seeds via init; author guide written so a new kungfu author needs no other document."
The author-guide half ships as the `tightbeam-kungfu-crafting` skill (the 7-part
contract); this spec covers the missing half — a **scaffold that drops a starter of
each part into its REAL home so the org loads clean** — and its prerequisites.

## The load-bearing correction (r2)

A kungfu bundle's parts do NOT all live under `identity/kungfu/<name>/`. **Nothing
scans that directory.** The loaders read fixed org-level dirs:
- `Archetypes.load!` → `identity/archetypes/*.toml` + `identity/guidance/*.md`
  (flat fragment namespace) + `identity/skills/*/SKILL.md` (archetypes.ex:268,283,301).
- `Rails.load!` → `identity/rails/*.toml` (rails.ex:99).
- `Producers.load!` → `identity/producers.toml` (producers.ex:39) — an ORG file, not a
  bundle part.

So a bundle has **two homes** (confirmed by the live `kungfu/engineering/`, which holds
ONLY the two operator docs):
- **SCANNED parts** (validated at boot): archetype manifest → `identity/archetypes/`,
  guidance kernel(s) → `identity/guidance/`, skill(s) → `identity/skills/`, rail(s) →
  `identity/rails/`.
- **BUNDLE-LOCAL docs** (operator-facing, never scanned): `identity/kungfu/<name>/`
  holds `capabilities.md`, `preferred-models.md`, `intake.md`.

The scaffold therefore writes a starter of each part **into its real home**, name-scoped
to `<name>`. "Loads clean" is then real, because the parts are where the loaders read.

## Manifest: a bundle declares WHAT IT IS FOR (Flynn, 2026-08-01)

Every kungfu manifest declares its PURPOSE — what capability adopting this bundle gives an
org, in plain language a user would recognize from describing their own work. This is not
documentation; it is the field the ONBOARDING AGENT READS to know when to offer a bundle.

Why it must exist: the shipped onboarding skill already names the moment — offer a kungfu
"during onboarding, when the goal they named maps to something in the org's library." That
instruction assumes the agent can tell what a bundle is FOR. With a manifest of
`root_archetype` alone it cannot, and is left to infer purpose from a bundle's name. That
is an invented mechanism of exactly the kind the July audit caught and downgraded; this
field is what makes the instruction real.

The product behavior it enables: a user mentions a capability Tightbeam has — they describe
wanting reviews enforced, or lab notebooks tracked — and the onboarding agent recognizes
the match, educates them that a kungfu provides it, and helps them get it spun up. Without
purpose, that offer can only fire on bundle names the user already knows, which inverts
who is supposed to be teaching whom.

Requirements:
- `purpose` is REQUIRED in every manifest; scaffolding a bundle without one fails loudly.
- It is user-facing prose about the capability, NOT a description of the bundle's internal
  parts. "Enforced review, verification papertrails, and work tracking for software teams"
  is a purpose; "7 archetypes, 13 guidance fragments, 18 skills" is an inventory.
- The `kungfu-list` verb projects it alongside name and root archetype, since that is the
  surface the onboarding agent reads.
- agentic-engineering's own manifest gains one.

## Goal

`tightbeam kungfu-scaffold <name>` drops a minimal, VALID starter of every one of the 7
parts into its correct home, name-scoped so no collision and no unknown-reference boot
failure. The org boots clean immediately with the (unfilled) starter present. The author
then fills the placeholders guided by `tightbeam-kungfu-crafting` alone.

## Non-goals

- Not a marketplace/registry (deferred with rooms/interop).
- Not authoring an opinionated example bundle — starters are empty-but-valid.
- No new *product* validation path: "loads clean" is proven by gateway boot (which
  already composes identity) and by a CI test that calls the existing loaders against a
  temp base_dir. `mix tightbeam.doctor` is NOT extended (it checks dir-populated + .git,
  never composes — doctor.ex:187; do not route validation through it).

## What the scaffold writes (each into its real, scanned home)

For `kungfu-scaffold <name>` (validate `<name>` matches `^[a-z0-9][a-z0-9-]*$`, no `--`,
and NO trailing hyphen — else `<name>` + `-role` composes `foo--role`, rejected at
archetypes.ex:973):

1. `identity/archetypes/<name>-role.toml` — one example role manifest:
   `name = "<name>-role"` (archetype name, no `--`, archetypes.ex:973), `where` OMITTED
   (defaults to gateway hostname, archetypes.ex:977 — the correct starter default),
   `skills = []` (empty is the ONLY safe election until the author adds skills — an
   election of an uninstalled skill fails boot, archetypes.ex:272), `[guidance]` text
   `#include "<name>-role.md"`.
2. `identity/guidance/<name>-role.md` — the kernel fragment the manifest includes
   (placeholder prose). Filename and the `#include` line MUST rename in lockstep
   (fragment namespace is flat basenames, archetypes.ex:301).
3. `identity/skills/<name>-example/SKILL.md` — one example skill, valid frontmatter
   (name/description), placeholder body, NOT a reserved substrate name (SKB refusal,
   archetypes.ex:317). Left UNELECTED (skills=[] in the manifest) so it can exist
   without forcing an election; the author elects it when ready.
4. `identity/rails/<name>-example.toml` — ONE valid no-harm statute. A fully
   commented-out file is REJECTED (rails.ex:105 requires ≥1 [[statute]]); there is no
   no-op tier — every statute compiles to a live PreToolUse grep gate. So the starter
   ships a single statute whose matcher is a **deliberately unmatchable sentinel** (e.g.
   matches the literal string `TIGHTBEAM_KUNGFU_TEMPLATE_PLACEHOLDER_NEVER_MATCHES`),
   statute `name = "<name>-example"` (matches `^[a-z0-9][a-z0-9-]*$`, rails.ex:160), so
   it loads, fires on nothing, and the author replaces it. Document it as replace-me.
5. `identity/kungfu/<name>/capabilities.md` — the §4 capability-matrix template.
6. `identity/kungfu/<name>/preferred-models.md` — the §5 activity-table template.
7. `identity/kungfu/<name>/intake.md` — the §6 operator-questions template, each
   question naming where its answer lands.
Plus `identity/kungfu/<name>/README.md` pointing at `tightbeam-kungfu-crafting` (NOT a
second author guide).

**root_archetype (contract part 7) — resolved:** it is NOT a manifest key (validate!
rejects unknown top-level keys, archetypes.ex:949). The recommended everyday archetype
is NAMED in `capabilities.md`/`intake.md`, and adoption applies it through the EXISTING
`config set default-archetype <name>-role` verb (org-settings, already shipped). No new
manifest field, no loader change.

## The scaffold command — a gateway verb with a thin CLI

`kungfu-scaffold` is a GATEWAY VERB (the server owns `priv/` and the identity repo;
a remote CLI has neither), with a thin CLI parse that dispatches it — exactly the
skill-verb pattern (`skill put` → gateway `put_skill!` → server-side write + attributed
commit, archetypes.ex:765). Admin-tier (matching `skill put`). The verb:
- reads starters from the substrate's `priv/kungfu-template/` (git-tracked with the
  code, like `priv/skills/`; never auto-projected — projection is driven by the
  hardcoded `@baseline_skill_names`, homes.ex:67, nothing wildcards `priv/`),
- substitutes `<name>` into paths/manifest fields/filenames/#include lines per the
  lexical rules above,
- refuses if any target path already exists (no clobber),
- writes all parts into their real homes and makes ONE attributed identity commit
  (`commit_identity!`, archetypes.ex:920).

## Prerequisite (must land with or before this)

`tightbeam-kungfu-crafting` is currently only in Flynn's org identity, NOT in the
substrate (`priv/skills/` ships 8, not this one; not in `@baseline_skill_names`,
homes.ex:67). For "no other document required" to hold in a FRESH org, ship it as a
substrate baseline: add its content to `priv/skills/tightbeam-kungfu-crafting/` and its
name to `@baseline_skill_names`. Small prerequisite lane; without it the scaffold's
README points at a guide a fresh org lacks.

## Acceptance

- `kungfu-scaffold demo` writes: `identity/archetypes/demo-role.toml`,
  `identity/guidance/demo-role.md`, `identity/skills/demo-example/SKILL.md`,
  `identity/rails/demo-example.toml`, and `identity/kungfu/demo/{capabilities,
  preferred-models,intake,README}.md`; one attributed identity commit.
- Re-running refuses (any existing target path → no clobber).
- With the unfilled starter present, **gateway boot composes clean** —
  `Archetypes.load!` + `Rails.load!` succeed (the real test: the scanned parts parse,
  the `#include` resolves, `skills=[]` elects nothing unknown, the sentinel statute
  loads). A CI test scaffolds into a temp base_dir and asserts these loaders succeed.
- `tightbeam-kungfu-crafting` is present as a substrate baseline (prerequisite).
- Audit note: each of the 7 parts has a governing authoring skill (or a filed gap).

## Depends on

- The 7-part contract (`tightbeam-kungfu-crafting`) — shipped in Flynn's org; must
  become a substrate baseline (prerequisite above).
- Existing loaders + the skill-verb server-side commit discipline. No new validation.
- `config set default-archetype` (org-settings, shipped) for the root_archetype apply.
