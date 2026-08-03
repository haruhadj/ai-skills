# Verification

Rules and commands for not being confidently wrong.

## The problem

Training data has a cutoff; packages do not. The failure mode is not obvious ignorance — it is **fluent, specific, wrong**: a version number, a config shape, a peer dependency, an API that was accurate once. It reads exactly like knowledge, which is why it survives review and lands in a plan.

Planning is where this does the most damage, because a wrong fact there becomes a wrong decision that everything downstream inherits.

## The rules

### 1. Never state a version or API from memory

One command settles what an hour of confident guessing gets wrong:

```bash
npm view <pkg> version peerDependencies dependencies time.modified
npm view <pkg> versions --json | tail -20
```

`time.modified` also answers "is this maintained?" — which is otherwise pure vibes.

### 2. Packages outrank documentation sites

Docs lag releases, sometimes by a major version. When they disagree, **the package is the truth**.

A real case: a library's docs site documented a Tailwind v3 setup — presets, `autoprefixer`, `init -p`. The published `peerDependencies` said `tailwindcss: ">= 4.0.0"`. Following the docs would have pinned the entire project to the wrong major version of its styling system.

The same check disproved a second claim in the same session: the library was assumed poorly maintained; `time.modified` showed a release ten weeks old.

Both errors came from the same mistake — trusting prose over the manifest.

### 3. Prefer the installed code

Once dependencies exist, `node_modules/<pkg>` is unambiguous. Read the types, the README, the bundled docs. No lag, no ambiguity about version.

Some frameworks ship version-specific docs there deliberately. If a project's `AGENTS.md` says to read them, that instruction exists because someone was already burned.

### 4. Record what you verified, and when

```md
**Verified against npm, 2026-08-03:**

| Package | Version | Notes |
|---|---|---|
| `@storefront-ui/react` | 4.0.1 (pub. 2026-05-18) | peer `react: ^19` |
| `@storefront-ui/tailwind-config` | 3.1.0 | peer `tailwindcss: >= 4.0.0` |
```

The date is what tells a future session whether to re-check. Without it, it's a rumour.

### 5. Correct everywhere, not just where it was noticed

When a stated fact turns out wrong, fix it in **every** place it was written — plan, context files, decision log — and note the correction with its reasoning:

```md
### Tailwind — correction
An earlier draft said pin v3. Wrong: it came from the docs site rather than
the packages. `@storefront-ui/tailwind-config@3.1.0` requires `>= 4.0.0`.
Lesson, now in AGENTS.md: the packages are the source of truth.
```

A wrong fact left in one file will be found later and believed.

### 6. Write the lesson into the context files

If a source misled you once, it will mislead the next session. That belongs in `AGENTS.md` and `tech-stack.md`:

> ⚠️ This library's docs site lags its packages. Trust `npm view` over the docs on anything version-sensitive. This has already caused one wrong decision.

## Commands

```bash
# Version, peers, and maintenance signal
npm view <pkg> version peerDependencies time.modified

# What versions exist (catches pre-releases and major jumps)
npm view <pkg> versions --json | tail -20

# Where the real docs live
npm view <pkg> homepage repository.url

# What is actually installed
cat node_modules/<pkg>/package.json | head -30
ls node_modules/<pkg>/dist/docs/ 2>/dev/null

# Python / Rust / Go equivalents
pip index versions <pkg>
cargo search <pkg>
go list -m -versions <module>
```

For API details, prefer a docs-fetching tool (context7 or equivalent) over recall — but still let the package win on version-sensitive questions.

## When to verify

**Always:**
- Any version number entering a plan or lockfile
- Peer dependency compatibility between two libraries
- Whether a library is maintained
- Config file shape and setup steps for a major version
- Any claim that a feature exists

**Usually fine from memory:**
- Language semantics
- Long-stable API shapes you'd notice being wrong immediately
- General patterns and architecture

The distinction: **things that change on a release schedule get checked.** Things that change on a decade scale usually don't.

## Failure patterns

**Confident specificity.** The more precise a remembered claim, the more worth checking. Vague memory prompts a check; exact memory suppresses one.

**Docs-site anchoring.** A well-written docs site feels authoritative. It is prose written by humans on a slower cycle than releases.

**Version drift in a family.** `@scope/a@4.0.1` and `@scope/tailwind-config@3.1.0` can ship together and require different things. Check each package, not the family.

**Assuming the docs URL matches the version.** A `/v2` docs path can describe packages that have since gone to 4.x.

**Skipping the check because it's "obvious".** The Tailwind case was obvious. It was also wrong.

## In the plan

Add a section for facts to confirm at implementation time rather than assume:

```md
Confirm at implementation time (do not assume):
- the actual v4 wiring for `@storefront-ui/tailwind-config`
- whether `transpilePackages` is still required
- React 19 alignment with the pinned framework version
```

This is honest about what a planning session can and cannot settle, and it stops a guess from hardening into a decision.
