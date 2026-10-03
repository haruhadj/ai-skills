# ai-skills

[Agent Skills](https://agentskills.io) for AI coding agents — reusable instruction sets that make agents produce work you'd be willing to maintain.

These skills use the open [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md` file and optional supporting files. They work in any agent that implements this standard. Host support, discovery paths, and invocation controls vary; see the install options below.

## Skills

| Skill | What it does |
|---|---|
| **[clean-code](plugins/clean-code/skills/clean-code/SKILL.md)** | Write code that stays readable, understandable, and maintainable — intent-revealing naming, small single-purpose functions, guard clauses over deep nesting, comments that explain *why*, pragmatic DRY, SOLID, a code-smell catalog, and clean tests. Emphasizes **not over-engineering**, the most common failure mode of AI-generated code. |
| **[git-haiku](plugins/git-haiku/skills/git-haiku/SKILL.md)** | Commit and push without ceremony — read `git status`/`git diff`, write a concise Conventional Commits message, commit on a topic branch, and push. Ships with a Haiku-pinned subagent so routine commits don't burn a larger model. |
| **[project-blueprint](plugins/project-blueprint/skills/project-blueprint/SKILL.md)** | Plan a project end to end before writing code, then capture it as durable context files (`AGENTS.md` + `context/`) that keep agents accurate across sessions — a decision log that keeps its reasoning, phased specs with mechanical exit criteria, an explicit scope boundary, and verification rules that stop invented versions and APIs. |

`project-blueprint` and `clean-code` are designed to work together: `project-blueprint` decides *what* to build and writes down the rules; `clean-code` governs *how* the code inside it gets written. `git-haiku` is independent — it takes the finished change and gets it committed.

---

## Install

### Option 1 — install for your agent (recommended)

The [`skills` CLI](https://github.com/vercel-labs/skills) installs skills for many agent clients, including Claude Code, Codex, Cursor, and GitHub Copilot. Run this from your project and choose the agents when prompted:

```bash
npx skills add https://github.com/haruhadj/ai-skills --full-depth
```

To install all three skills for all detected agents without prompts:

```bash
npx skills add https://github.com/haruhadj/ai-skills --full-depth --skill '*' --agent '*' --yes
```

Use `-g` for user-wide installation across projects. Check `npx skills add --help` for the current supported agent list and options.

### Option 2 — Claude Code plugin marketplace

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

### Option 3 — portable shell installer

The installer puts skills in the shared `~/.agents/skills` directory by default. This is discovered by Codex and several other Agent Skills-compatible hosts. Use `SKILLS_DIR` when your host uses another location. Requires Bash, `curl`, and `tar` (macOS, Linux, or WSL).

```bash
# user scope: ~/.agents/skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | bash

# project scope: ./.agents/skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | SCOPE=project bash

# install into a host-specific directory (example: Claude Code)
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | SKILLS_DIR="$HOME/.claude/skills" bash

# only specific skills
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | bash -s -- clean-code git-haiku

# install from a branch other than main
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | REF=develop bash
```

Set `REF` to a commit SHA to install an immutable revision.

`SKILLS_DIR` can point at any directory your agent scans. For example:

```bash
curl -fsSL https://raw.githubusercontent.com/haruhadj/ai-skills/main/install.sh | SKILLS_DIR=~/.cursor/skills bash
```

### Option 4 — clone and copy manually

```bash
git clone https://github.com/haruhadj/ai-skills.git
mkdir -p ~/.agents/skills
cp -R ai-skills/plugins/clean-code/skills/clean-code ~/.agents/skills/
cp -R ai-skills/plugins/project-blueprint/skills/project-blueprint ~/.agents/skills/
cp -R ai-skills/plugins/git-haiku/skills/git-haiku ~/.agents/skills/
```

Replace `~/.agents/skills` with the skill directory used by your host. To track updates from the clone instead of copying, symlink:

```bash
mkdir -p ~/.agents/skills
ln -sfn "$PWD/ai-skills/plugins/clean-code/skills/clean-code" ~/.agents/skills/clean-code
ln -sfn "$PWD/ai-skills/plugins/project-blueprint/skills/project-blueprint" ~/.agents/skills/project-blueprint
ln -sfn "$PWD/ai-skills/plugins/git-haiku/skills/git-haiku" ~/.agents/skills/git-haiku
```

Then `git pull` refreshes the linked skills.

### Hosts without automatic skill discovery

If a host does not implement Agent Skills or scan a skill directory, provide the complete skill folder through that host's upload, attachment, or API mechanism. Keep the folder structure intact so `SKILL.md` can resolve its `references/` files. For example, OpenAI's Responses API accepts uploaded skill bundles or skill references; its Agents API can discover skills from registered capability directories. A model alone cannot install or automatically load files without support from its host application.

---

## Team-wide install

For Claude Code teams using the plugin marketplace, commit this to `.claude/settings.json`; collaborators are prompted to install when they trust the repo:

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

Restart or reload the agent if it was already running. Ask **"What skills are available?"** — a compatible host should list installed skills. Some hosts also expose installed skills as slash commands:

- Direct install: commonly `/clean-code`, `/project-blueprint`
- Claude Code plugin install: `/clean-code:clean-code` (plugin skills are namespaced by plugin name)

If a skill doesn't appear, check that it is under a directory your host scans and restart the host. For Claude Code, run `claude --debug` to inspect skill loading errors.

---

## Make them apply automatically

Skills load when the agent judges them relevant. For consistent use, add a short instruction to the persistent context file your host reads, such as `AGENTS.md` or `CLAUDE.md`:

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
├── git-haiku/
│   ├── skills/git-haiku/SKILL.md # inspect, message, commit, push
│   └── agents/git-haiku.md       # same job as a Haiku-pinned subagent
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
# Claude Code plugin
/plugin uninstall clean-code@haruhadj-skills

# installed skill directory (adjust for your host)
rm -rf ~/.agents/skills/clean-code ~/.agents/skills/project-blueprint ~/.agents/skills/git-haiku
```

## Adding another skill

1. Create `plugins/<name>/.claude-plugin/plugin.json` and `plugins/<name>/skills/<name>/SKILL.md`.
2. Append an entry to `plugins[]` in `.claude-plugin/marketplace.json` (same `name` and `version` as the plugin manifest).
3. Add it to the Skills table above.
4. Run `python scripts/validate.py`, then push.

CI runs the same validator on every push and pull request, plus `shellcheck` and a real `install.sh` run against the pushed commit — covering every skill in the repo — so a broken commit can't reach the machines that install from `main`.

## License

MIT
