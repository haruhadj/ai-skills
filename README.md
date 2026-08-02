# clean-code skill

An [Agent Skill](https://agentskills.io) that teaches AI coding agents to write code that stays readable, understandable, and therefore maintainable.

Covers intent-revealing naming, small single-purpose functions, guard clauses over deep nesting, comments that explain *why* rather than *what*, pragmatic DRY, SOLID design, a code-smell catalog, and clean tests — with a deliberate emphasis on **not over-engineering**, which is the most common failure mode of AI-generated code.

Works with Claude Code, Claude Cowork, Cursor, Codex, Google Antigravity, and any tool that supports the Agent Skills standard.

---

## Install

### Option 1 — Claude Code plugin marketplace (recommended)

Installs once per machine and auto-updates. Run inside Claude Code:

```
/plugin marketplace add haruhadj/ai-skills
/plugin install clean-code@haruhadj-skills
/reload-plugins
```

Enable auto-update from `/plugin` → **Marketplaces** → select this marketplace → **Enable auto-update**.

To install non-interactively from a shell (useful for scripting a new machine):

```bash
claude plugin marketplace add haruhadj/ai-skills
claude plugin install clean-code@haruhadj-skills
```

### Option 2 — one-line curl (any agent)

```bash
# user scope: ~/.claude/skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | bash

# project scope: ./.claude/skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | SCOPE=project bash

# any other tool's skills directory
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | SKILLS_DIR=~/.cursor/skills bash
```

### Option 3 — git clone / copy

```bash
git clone https://github.com/haruhadj/ai-skills.git
cp -r ai-skills/plugins/clean-code/skills/clean-code ~/.claude/skills/
```

To track updates instead of copying, symlink it:

```bash
ln -sfn "$PWD/ai-skills/plugins/clean-code/skills/clean-code" ~/.claude/skills/clean-code
```

Then `git pull` refreshes the skill everywhere.

---

## Team-wide install

Commit this to your project's `.claude/settings.json` and collaborators are prompted to install it when they trust the repo:

```json
{
  "extraKnownMarketplaces": {
    "haruhadj-skills": {
      "source": {
        "source": "github",
        "repo": "haruhadj/ai-skills"
      }
    }
  },
  "enabledPlugins": ["clean-code@haruhadj-skills"]
}
```

---

## Verify it loaded

In a session, ask **"What skills are available?"** — you should see `clean-code`. Or invoke it directly:

- Plain skill install: `/clean-code`
- Plugin install: `/clean-code:clean-code` (plugin skills are namespaced by plugin name)

If it doesn't appear, run `claude --debug` to surface frontmatter parse errors. Note that an unrecognized frontmatter key makes the whole skill fail validation and disappear silently.

---

## Make it apply automatically

Skills load when the agent judges them relevant. To make that near-certain for all code work, add a line to your project's `CLAUDE.md` (or `AGENTS.md` for other tools):

```
When writing, reviewing, or refactoring code, follow the `clean-code` skill.
```

---

## Structure

```
plugins/clean-code/skills/clean-code/
├── SKILL.md                    # core principles, always loaded when triggered
└── references/
    ├── solid.md                # SOLID, loaded when designing classes/modules
    ├── code-smells.md          # smell → refactoring catalog, loaded when reviewing
    └── testing.md              # clean tests, loaded when writing/refactoring tests
```

The reference files use progressive disclosure: only `SKILL.md` enters context on activation, and the agent reads the others when the task calls for them.

---

## Uninstall

```bash
# plugin
/plugin uninstall clean-code@haruhadj-skills

# manual install
rm -rf ~/.claude/skills/clean-code
```

## License

MIT
