# Context Files

The durable memory of a project. Each file, what it is for, and how to write it so it stays true.

## The governing rule

**One fact, one home.** The moment the same fact lives in two files, they start to diverge — and a future agent gets contradictory instructions with no way to tell which is current.

When content belongs elsewhere, **move it and link to it**. Never copy.

Audit before finishing: if two files describe the same thing, one is already wrong.

## Layout

```
AGENTS.md                    entry point — read order, rules, workflow
CLAUDE.md                    thin pointer to AGENTS.md
context/
  project-overview.md
  functionality.md
  user-flow.md
  architecture.md
  tech-stack.md
  code-standards.md
  ui-tokens.md
  ui-rules.md
  ui-registry.md
  progress-tracker.md
  planning/
    PLAN.md
    PHASE-0.md … PHASE-N.md
```

Scale down for small projects — a CLI has no UI files. Never drop `functionality.md` or `progress-tracker.md`.

Keep `AGENTS.md` at the repo root: it must be found before anything else, and multiple tools look for it there. `CLAUDE.md` stays a pointer so there is one source of truth rather than two that drift.

---

## AGENTS.md

The entry point, and the only file guaranteed to be read. Four sections:

1. **Read order** — numbered table: file, and what it gives you.
2. **Rules that never change** — grouped (design / code / process / libraries). Short, absolute, checkable.
3. **Session workflow** — read at start, update at end.
4. **The invariants** — restated here because this is where they'll be seen.

Keep it under ~150 lines. It competes for attention with the actual task; a long entry point gets skimmed.

If the file has managed blocks (`<!-- BEGIN:… -->`), preserve them verbatim — tooling rewrites them.

A full worked example is at the end of this file.

## project-overview.md

What this is, the problem it solves, who it's for, what success means, deliberate non-goals.

Include the alternatives and why they don't fit. That comparison is what lets someone evaluate a proposed change against the actual purpose.

If there are two audiences — a buyer and an end user, an operator and a customer — say so explicitly with what each optimizes for. Conflating them produces software that serves neither.

## functionality.md

**The scope-creep brake, and the highest-value file in the set.**

Two lists: in-scope (by phase) and out-of-scope. Every out-of-scope entry states **why**:

```md
| Not building | Why |
|---|---|
| Multi-tenancy | Sold as a codebase, one store per deploy. Tenant isolation
                  would cost every query for zero buyer value. |
| Page builder  | Buyers are developers; they edit files. |
```

The reason is what stops it being re-proposed every session. A bare "out of scope" invites relitigation; a reason ends it.

Add the rules too: nothing gets built that isn't listed; "while I'm in here" is scope creep; extension points are not features.

## user-flow.md

Every screen and how users move between them. A route table with phase tags, plus ASCII diagrams of the flows that matter.

Include the rules that ride along with each flow — "guest checkout is always available", "invalid options are disabled, never hidden". Those are the details reinvented wrongly when they live only in someone's head.

## architecture.md

Folder structure, layer boundaries, dependency direction, naming conventions, file organization, testing layout.

State the dependency rule as a rule, not a diagram alone: *"`packages/api` never imports from `apps/web`. Enforced by lint. A violation is a build failure, not a review comment."*

Name the one boundary that matters most and say why. Usually it's where the ORM stops.

## tech-stack.md

Every library, **why it was chosen**, and rules for using it.

The "why" is load-bearing: it's what lets a future agent judge whether a proposed alternative is acceptable. "Drizzle" tells you nothing; "Drizzle, because migrations are readable SQL you can hand to a client, and Prisma's binary engine is a support burden on someone else's server" tells you what a replacement must preserve.

Include a **version matrix with the date it was verified**, and rules for adding a dependency.

## code-standards.md

Language rules specific to *this* project — not a general style guide. If a broader skill covers general quality, point at it and only write what is project-specific.

The highest-value entries are the ones with expensive failure modes: money representation, error handling, what is never trusted from a client, where secrets may appear.

## ui-tokens.md

Design primitives — colors, spacing, radii, type, motion. **The only source of visual values.**

Two tiers: primitives (raw values) and semantics (intent). Components use semantics only. `bg-brand` survives a rebrand; `bg-indigo-600` does not.

State the rule absolutely — no hex values, no raw color utilities — and say what it buys. "Rebrand without touching a component" is a promise one hardcoded hex breaks, and nobody notices until a client asks why one button is the wrong blue.

## ui-rules.md

How components behave, so behavior is never invented: buttons, cards, badges, forms, the five states every data view needs (loading, empty, error, partial, success), feedback, accessibility.

Lead with the order of operations: check the registry → use the library's component → only then build something new.

## ui-registry.md

What already exists, so nothing is built twice. Path, surface, origin, props, variants, where it's used, gotchas.

**Worthless unless updated in the same commit as the component.** Put that in `AGENTS.md`'s session-finish checklist. An unregistered component gets rebuilt within a week; a stale registry is worse than none, because it is trusted and wrong.

Start it with the format and a planned-components list even when empty.

## progress-tracker.md

How the next session knows where things stand:

- **Current phase and status**
- **Phase table** with completion state
- **Current phase checklist**
- **Decision log** — decisions made during implementation that aren't in the specs, with reasoning and date
- **Open items** — blocking vs verify-during-implementation
- **Session log** — two lines per session: what happened, what's next, anything surprising

The most-updated file in the set. If it's stale, the whole set is suspect.

---

## Writing style

**Say why, not just what.** A rule without a reason gets broken the first time it's inconvenient.

**Be absolute where it matters.** "Prefer semantic tokens" gets ignored. "Never write a hex value" doesn't.

**Show the failure.** `❌ price: number` next to `✅ price: Money` beats a paragraph.

**Keep files scannable.** Tables and short sections. These are reference documents read under time pressure, not essays.

**Date anything that can go stale.** Version matrices, verified facts, status.

## Retrofitting an existing project

Describe **what is actually there**, not what should be. Aspirations get marked as aspirations, or the files become fiction and stop being trusted.

Start with `functionality.md`, `architecture.md`, and `progress-tracker.md` — the drift brake, the unwritten conventions, and the record. Add the rest as they earn their place.

---

## Worked example — AGENTS.md

A complete entry point for a project with UI. Adapt the rules and invariants to the project; keep the shape.

````md
<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes. Read the relevant guide in
`node_modules/next/dist/docs/` before writing any code.
<!-- END:nextjs-agent-rules -->

## Read before anything else

Read in this exact order before any implementation:

1. `context/project-overview.md` — what this is, who for, non-goals
2. `context/functionality.md` — in-scope vs out-of-scope, with reasons
3. `context/architecture.md` — layers, dependency direction
4. `context/tech-stack.md` — libraries, versions, per-library rules
5. `context/code-standards.md` — project-specific language rules
6. `context/ui-tokens.md` — the only source of visual values
7. `context/ui-rules.md` — component behavior
8. `context/ui-registry.md` — what already exists
9. `context/planning/PHASE-<current>.md` — this phase's scope and exit criteria
10. `context/progress-tracker.md` — where things stand

## Rules that never change

**Design** — never a hex value or raw color utility. Semantic tokens only.
A rebrand must touch zero components.

**Process** — nothing gets built that isn't in the current phase spec.
"While I'm in here" is scope creep. Raise it, don't absorb it.

**Verification** — never state a version or API from memory. Check the
installed package; it outranks the docs site.

**Circuit breaker** — if the same failure survives one corrective attempt,
stop. Report what you tried and what you observed. Do not attempt a third fix.

## Session workflow

**Start:** read the files above in order.
**Finish:** update `progress-tracker.md` (session log, decisions made) and
`ui-registry.md` (any new component) — in the same commit as the code.
An unregistered component gets rebuilt within a week.

## Invariants

Violating these is a bug regardless of what you were working on:

- Money is integer minor units + currency
- The ORM never escapes the service layer
- Totals are always computed server-side
````

Notes on the example:

- The `<!-- BEGIN: -->` block is tool-managed. Preserve it verbatim; never hand-edit inside it.
- The read order names the files this skill produces. If you rename a file, rename it here too — a read order pointing at a file that doesn't exist teaches the agent the list is unreliable.
- Rules are grouped and absolute. "Prefer semantic tokens" gets ignored; "never a hex value" doesn't.
- Do not list slash commands or skills unless they are actually installed. A read order that invokes a command that doesn't exist is a hallucination shipped into the project's most-read file.
