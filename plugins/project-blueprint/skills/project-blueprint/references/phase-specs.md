# Phase Specs

How to break a build into phases that can actually be finished.

## Why phases beat a task list

A task list says what to do. A phase says what "done" means — and that is the part that prevents a project from being 90% complete forever. Each phase is a checkpoint where the work either satisfies stated criteria or does not.

Phases also localize risk. If the props contract is wrong, you find out at the end of Phase 1 rather than during Phase 4's theming work, when a hundred components already depend on it.

## The shape

One file per phase, five sections, always the same order.

```md
# Phase N — Name

**Status:** specified, not started
**Depends on:** PHASE-(N-1).md

## Scope
In: …
Out: … (with where it lands instead)

## Deliverables
Numbered. Each concrete enough to build from.

## Key design decisions
The choices made here that later phases inherit — and why.

## Exit criteria
Numbered, mechanically checkable.

## Risks
What could go wrong, and the mitigation.
```

## Phase 0 is always foundation

No user-visible output. Repo skeleton, tooling, schema, auth, CI, the typed path from route to client. Its purpose is that later phases never revisit a decision made here.

It is the phase most often skipped and the one whose absence is most expensive. Everything in Phase 0 is something every later phase depends on; getting it wrong means changing code that by then has a hundred call sites.

## Exit criteria are the whole point

**Mechanically checkable.** A person other than the author must be able to run it and get an unambiguous yes or no.

```
❌ "Catalog works"
❌ "Import is reliable"
❌ "Good performance"

✅ "A product with 3 options and 12 variants renders, is selectable,
    and deep-links per variant."
✅ "Re-running the same import produces zero duplicates and correct updates."
✅ "Lighthouse ≥ 90 on PDP and listing."
```

Aim for five to eight per phase. Fewer means the phase is under-specified; many more means it should have been two phases.

**Include the negative cases.** The criteria that catch real bugs are the ones asserting what must *not* happen:

```
✅ "Dry-run writes nothing — verified by a test asserting zero mutations."
✅ "Concurrent checkout of the last unit oversells zero."
✅ "Changing a product's price leaves historical orders untouched."
```

## Scope needs an "out" list

Every phase states what it is *not* doing and where that work lands instead. Without it, "while I'm in here" absorbs the next phase and nothing ever closes.

```md
**Out:** cart, orders, checkout (Phase 3). Migrations are additive, so
deferring costs nothing — and designing checkout tables before a catalog
exists tends to produce fiction.
```

Note the reasoning. An out-of-scope item with a reason stays out; one without gets re-proposed next session.

## Pull decisions forward when deferring is expensive

Most things should be built in the phase that needs them. The exception is anything whose retrofit touches everything already written.

> `external_refs` ships in Phase 0 even though importers arrive in Phase 2 — it is what makes re-imports idempotent, and adding it later leaves every prior import un-reconcilable.

The test: **if adding this later requires a migration across code that will exist by then, add it now.** Schema, ID format, money representation, and translation tables almost always qualify.

## Sequencing

Order by dependency, then by what de-risks the most.

1. **Foundation** — everything inherits it.
2. **The core domain** — the thing the product is about.
3. **The differentiator** — build it early enough that a problem is survivable.
4. **Transactions and money** — needs the domain to exist first.
5. **Product-ization** — docs, polish, packaging.

The last phase is the one most often cut when time runs short, and cutting it is usually the wrong call: it's what turns working software into something someone else can actually use.

## Risks

Name the two or three that would genuinely hurt, with a mitigation:

```md
- **Variant matrix UI** — highest complexity in the phase. Prototype first.
- **Props contract churn.** If it's still moving at phase end, the upgrade
  promise isn't credible. Freeze before Phase 2.
```

Skip generic risks. "Might take longer than expected" is true of everything and helps nobody.

## During implementation

- **Don't build ahead.** Out-of-phase work is raised, not absorbed.
- **Re-read the current spec at session start.** It is short, and drift is gradual.
- **Update `progress-tracker.md` at session end** — status, decisions made, what's next.
- **Decisions made mid-phase that aren't in the spec go in the decision log**, with the reasoning.
- **A phase closes when every exit criterion passes**, not when it feels finished.

## Sizing

If a phase has more than roughly ten deliverables, split it. If it has two, fold it into a neighbour. A phase should be a coherent chunk of work with a name that means something — not a sprint boundary.
