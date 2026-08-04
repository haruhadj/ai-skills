---
name: project-blueprint
description: Plan a software project end to end before writing code, then capture the result as durable context files (AGENTS.md + context/) that keep agents accurate across sessions. Use when starting a new project or app, when asked to plan, architect, scope or blueprint a build, when a repo has no trustworthy AGENTS.md or CLAUDE.md, when work will span multiple sessions, or when an agent keeps drifting, re-deciding settled questions, inventing APIs, or quietly expanding scope. Produces a decision log that keeps the reasoning, phased specs with mechanical exit criteria, an explicit in-scope/out-of-scope boundary with justifications, UI tokens/rules/registry, and session rules. Do not use for one-off scripts, single-file edits, or tasks inside an already well-documented project.
---

# Project Blueprint

Most agent failure on long projects is not a reasoning failure. It is a **context failure**. The agent invents an API that never existed, re-decides a question settled three sessions ago, drifts from the architecture, or quietly widens scope — because the decisions were made in a conversation that no longer exists.

This skill fixes that by moving decisions out of conversation and into files: a plan the work follows, and a context set the agent re-reads every session. Write them once, and every future session starts informed instead of guessing.

The output is two things:

1. **A plan** — decisions with their reasoning, and phases with mechanical exit criteria.
2. **A context set** — `AGENTS.md` plus `context/*.md`, the durable memory of the project.

## The four stages

Work them in order. Each depends on the one before.

```
1. Interview   resolve the forks that change the work
2. Plan        decisions + phases + invariants
3. Context     AGENTS.md + context/ files
4. Discipline  session rules that keep it true
```

Do not skip to stage 3. Context files written before the decisions are settled just record confusion in a more permanent format.

---

## Stage 1 — Interview

Ask before planning. But ask *well*: most questions agents ask are filler that a competent colleague would have answered themselves.

**Only ask when the answer changes the work.** If both answers lead you to write the same thing, decide it yourself and say what you chose. Questions with a conventional default are not questions.

**Always recommend.** Give a default and the reasoning, so the user is reacting to a proposal rather than doing your thinking. A question with four options and no recommendation moves work onto the person who has less context than you.

**Notice questions that are already answered.** Constraints propagate. If the user said "I'll sell the codebase," then "is the buyer technical?" is already settled — a non-technical buyer cannot deploy a monorepo. Say so rather than asking. Finding the forced answer is more valuable than collecting a preference.

**Push back once, then commit.** If a stated constraint conflicts with the stated goal, say so in two sentences, propose the amendment, and record it as an amendment with a `Revisit if:` condition. If the user reaffirms, build what they asked for.

`references/interview.md` has the question sets by project type and the traps that produce useless answers.

---

## Stage 2 — Plan

### Decisions keep their reasoning

A decision log that records only conclusions gets relitigated every time someone disagrees. Record the *why*, and amendments as amendments:

```md
### Payments — amendment to the original call
Original decision was "no payments in v1." Amended because a buyer
evaluating an e-commerce codebase looks for checkout within 90 seconds.
**Revisit if:** the first client has no checkout requirement.
```

Anyone reading later — including you — can now evaluate whether the reasoning still holds instead of re-arguing from scratch.

### Phases, not a task list

Each phase gets its own file with the same five sections: **scope** (including what is explicitly *out*), **deliverables**, **key design decisions**, **exit criteria**, **risks**.

**Exit criteria must be mechanically checkable.** "Catalog works" is not a criterion. "A product with 3 options and 12 variants renders, is selectable, and deep-links per variant" is. If finishing a phase is a judgment call, it will be judged done early.

Phase 0 is always foundation — the decisions everything else inherits. It has no user-visible output, and skipping it properly is what turns month three into a rewrite.

### Invariants

Extract the handful of rules that hold across every phase — the ones where a violation is a bug regardless of what you were working on:

> Money is integer minor units + currency. The ORM never escapes the service layer. Totals are always computed server-side.

These go in `AGENTS.md` where they are read constantly, not buried in a phase spec that is only opened once.

`references/phase-specs.md` has the full template and worked examples of good and bad exit criteria.

---

## Stage 3 — Context files

```
AGENTS.md                    entry point: read order, rules, session workflow
CLAUDE.md                    thin pointer to AGENTS.md
context/
  project-overview.md        what, who for, what success means
  functionality.md           in-scope vs out-of-scope, with reasons
  user-flow.md               every screen and how users move between them
  architecture.md            folders, layers, dependency rules
  tech-stack.md              libraries, versions, rules for each
  code-standards.md          language rules specific to this project
  ui-tokens.md               design primitives — the only source of visual values
  ui-rules.md                how UI behaves, so it is never invented
  ui-registry.md             what is already built, so it is never rebuilt
  progress-tracker.md        live status, decision log, session log
  planning/                  PLAN.md + PHASE-N.md
```

Scale it down for small projects — a CLI needs no `ui-tokens.md`. Never scale down `functionality.md` or `progress-tracker.md`; those two do the most work.

### The rule that makes this survive

**One fact, one home.** The instant the stack appears in both `PLAN.md` and `tech-stack.md`, they begin to diverge, and a future agent gets contradictory instructions with no way to tell which is current. When content belongs somewhere else, **move it and link** — never copy.

Audit for this before finishing. If two files describe the same thing, one of them is wrong already.

### What each file is actually for

- **`functionality.md`** is the scope-creep brake. Every out-of-scope entry states *why*, so it stops being re-proposed each session.
- **`ui-tokens.md`** makes "rebrand without touching a component" true. One hardcoded hex breaks it, and nobody notices until a client asks why one button is the wrong blue.
- **`ui-registry.md`** is worthless unless updated in the same commit as the component. An unregistered component gets rebuilt within a week.
- **`progress-tracker.md`** is how the next session knows where things stand. It carries current phase, decision log, and a short session log.

`references/context-files.md` has the purpose, structure, and a template for each file.

---

## Stage 4 — Session discipline

`AGENTS.md` is the entry point and does the ongoing enforcement. It carries:

- **Read order** — numbered, with what each file gives you.
- **Rules that never change** — design, code, process, libraries.
- **Session workflow** — what to read at the start, what to update at the end.
- **The invariants** — restated where they will actually be seen.

Three habits make the difference between context files that stay true and context files that become archaeology:

**Update the tracker and registry at the end of every session.** Not "when convenient." A registry that is a week stale is worse than none, because it is trusted and wrong.

**Never build ahead of the current phase.** If a task is not in this phase's spec, raise it rather than absorbing it. "While I'm in here" is how scope dies.

**Stop after one failed correction.** If the same failure survives one corrective attempt, the model of the problem is wrong — and a third attempt edits code based on that wrong model, so the codebase gets worse while the symptom stays. Stop, report what was tried and what was actually observed, and re-read the relevant context file before touching anything else. Put this rule in `AGENTS.md`; it is the one that fires when a session is going badly, which is exactly when nobody is reading the rest.

`references/context-files.md` ends with a full worked `AGENTS.md` carrying all of these.

---

## Verification — the anti-hallucination rules

This is the part that most directly prevents wrong output, and it applies during planning *and* forever after.

**Never state a version, API, or package fact from memory.** Check it. `npm view <pkg> version peerDependencies time.modified` costs one command and settles what an hour of confident guessing gets wrong.

**Packages outrank documentation sites.** Docs lag releases, sometimes by major versions. When they disagree, the installed package is the truth.

**Record what you verified and when.** A version matrix with a date tells the next session whether to re-check. Without the date it is a rumour.

**When you find you were wrong, correct it everywhere the claim was written** — plan, context files, and the decision log — and note the correction. A wrong fact left in one file will be found and believed later.

**Prefer reading the installed code** over recalling the library. `node_modules/<pkg>` is unambiguous.

`references/verification.md` has the specific commands and the failure patterns worth knowing.

---

## Applying this to an existing project

Same stages, different starting point. Read the codebase first and write the context files to describe **what is actually there**, not what should be. Mark aspirations explicitly as aspirations.

The highest-value files for a project already underway are `functionality.md` (stop the drift), `architecture.md` (write down the conventions that exist only in someone's head), and `progress-tracker.md` (start the record now).

## What this is not

Not a substitute for thinking, and not a reason to produce twelve files for a weekend project. A small tool might need only `AGENTS.md` and `functionality.md`. The test is whether a competent stranger — or an agent with no memory of the conversation — could pick the work up and be correct. Files past that point are ceremony.
