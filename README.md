# ai-skills

[Agent Skills](https://agentskills.io) for AI coding agents — reusable instruction sets that make agents produce work you'd be willing to maintain.

Works with Claude Code, Claude Cowork, Cursor, Codex, Google Antigravity, and any tool that supports the Agent Skills standard.

## Skills

| Skill | What it does |
|---|---|
| **[clean-code](plugins/clean-code/skills/clean-code/SKILL.md)** | Write code that stays readable, understandable, and maintainable — intent-revealing naming, small single-purpose functions, guard clauses over deep nesting, comments that explain *why*, pragmatic DRY, SOLID, a code-smell catalog, and clean tests. Emphasizes **not over-engineering**, the most common failure mode of AI-generated code. |
| **[project-blueprint](plugins/project-blueprint/skills/project-blueprint/SKILL.md)** | Plan a project end to end before writing code, then capture it as durable context files (`AGENTS.md` + `context/`) that keep agents accurate across sessions — a decision log that keeps its reasoning, phased specs with mechanical exit criteria, an explicit scope boundary, and verification rules that stop invented versions and APIs. |

The two are designed to work together: `project-blueprint` decides *what* to build and writes down the rules; `clean-code` governs *how* the code inside it gets written.

---

## Install

### Option 1 — Claude Code plugin marketplace (recommended)

Installs once per machine and auto-updates. Run inside Claude Code:

```
/plugin marketplace add haruhadj/ai-skills
/plugin install clean-code@haruhadj-skills
/plugin install project-blueprint@haruhadj-skills
/reload-plugins
```

Enable auto-update from `/plugin` → **Marketplaces** → select this marketplace → **Enable auto-update**.

To install non-interactively from a shell (useful for scripting a new machine):

```bash
claude plugin marketplace add haruhadj/ai-skills
claude plugin install clean-code@haruhadj-skills
claude plugin install project-blueprint@haruhadj-skills
```

### Option 2 — one-line curl (any agent)

Installs every skill by default.

```bash
# user scope: ~/.claude/skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | bash

# project scope: ./.claude/skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | SCOPE=project bash

# any other tool's skills directory
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | SKILLS_DIR=~/.cursor/skills bash

# only specific skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | bash -s -- clean-code
```

### Option 3 — git clone / copy

```bash
git clone https://github.com/haruhadj/ai-skills.git
cp -r ai-skills/plugins/clean-code/skills/clean-code ~/.claude/skills/
cp -r ai-skills/plugins/project-blueprint/skills/project-blueprint ~/.claude/skills/
```

To track updates instead of copying, symlink instead:

```bash
ln -sfn "$PWD/ai-skills/plugins/clean-code/skills/clean-code" ~/.claude/skills/clean-code
ln -sfn "$PWD/ai-skills/plugins/project-blueprint/skills/project-blueprint" ~/.claude/skills/project-blueprint
```

Then `git pull` refreshes the skills everywhere.

---

## Team-wide install

Commit this to your project's `.claude/settings.json` and collaborators are prompted to install when they trust the repo:

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
  "enabledPlugins": [
    "clean-code@haruhadj-skills",
    "project-blueprint@haruhadj-skills"
  ]
}
```

---

## Verify it loaded

In a session, ask **"What skills are available?"** — you should see them listed. Or invoke one directly:

- Plain skill install: `/clean-code`, `/project-blueprint`
- Plugin install: `/clean-code:clean-code` (plugin skills are namespaced by plugin name)

If a skill doesn't appear, run `claude --debug` to surface frontmatter parse errors. An unrecognized frontmatter key makes the whole skill fail validation and disappear silently.

---

## Make them apply automatically

Skills load when the agent judges them relevant. To make that near-certain, add lines to your project's `CLAUDE.md` (or `AGENTS.md` for other tools):

```
When writing, reviewing, or refactoring code, follow the `clean-code` skill.
When planning a project or setting up its context files, follow the `project-blueprint` skill.
```

---

## Structure

```
plugins/
├── clean-code/skills/clean-code/
│   ├── SKILL.md                  # core principles, loaded when triggered
│   └── references/
│       ├── solid.md              # SOLID, when designing classes/modules
│       ├── code-smells.md        # smell → refactoring catalog, when reviewing
│       └── testing.md            # clean tests
│
└── project-blueprint/skills/project-blueprint/
    ├── SKILL.md                  # the four stages, loaded when triggered
    └── references/
        ├── interview.md          # question sets, and what makes a question worth asking
        ├── phase-specs.md        # phase template and exit-criteria craft
        ├── context-files.md      # every context file, purpose and structure
        └── verification.md       # commands and rules against invented facts
```

Reference files use progressive disclosure: only `SKILL.md` enters context on activation, and the agent reads the others when the task calls for them.

---

## Uninstall

```bash
# plugin
/plugin uninstall clean-code@haruhadj-skills

# manual install
rm -rf ~/.claude/skills/clean-code
```

## Adding another skill

1. Create `plugins/<name>/.claude-plugin/plugin.json` and `plugins/<name>/skills/<name>/SKILL.md`.
2. Append an entry to `plugins[]` in `.claude-plugin/marketplace.json` (same `name` and `version` as the plugin manifest).
3. Add it to the Skills table above.
4. Run `python scripts/validate.py`, then push.

CI runs the same validator on every push and pull request, plus `shellcheck` and a real `install.sh` run against the pushed commit — covering every skill in the repo — so a broken commit can't reach the machines that install from `main`.

## License

MIT
