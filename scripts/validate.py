#!/usr/bin/env python3
"""Validate marketplace, plugin manifests, and skill frontmatter.

Run locally with `python scripts/validate.py` before pushing; CI runs the same
script so a broken commit can't break installs on other machines.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = ROOT / "plugins"

# Claude Code truncates longer descriptions when deciding whether to load a skill.
MAX_DESCRIPTION = 1024
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []


def fail(message):
    errors.append(message)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{path.relative_to(ROOT)}: missing")
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON — {exc}")
    return None


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return None

    _, _, rest = text.partition("---")
    body, sep, _ = rest.partition("\n---")
    if not sep:
        fail(f"{path.relative_to(ROOT)}: unterminated frontmatter")
        return None

    fields = {}
    for line in body.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, colon, value = line.partition(":")
        if colon and not key.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return fields


def check_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(f"{skill_dir.relative_to(ROOT)}: no SKILL.md")
        return

    fields = parse_frontmatter(skill_md)
    if fields is None:
        return

    rel = skill_md.relative_to(ROOT)
    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        fail(f"{rel}: frontmatter missing `name`")
    elif name != skill_dir.name:
        fail(f"{rel}: name `{name}` does not match directory `{skill_dir.name}`")
    elif not NAME_PATTERN.match(name):
        fail(f"{rel}: name `{name}` must be lowercase kebab-case")

    if not description:
        fail(f"{rel}: frontmatter missing `description`")
    elif len(description) > MAX_DESCRIPTION:
        fail(f"{rel}: description is {len(description)} chars (max {MAX_DESCRIPTION})")

    for ref in re.findall(r"references/[\w./-]+\.md", skill_md.read_text(encoding="utf-8")):
        if not (skill_dir / ref).is_file():
            fail(f"{rel}: references missing file `{ref}`")


def check_plugin(entry, marketplace_owner):
    name = entry.get("name")
    source = entry.get("source", "")
    if not name:
        fail("marketplace.json: plugin entry missing `name`")
        return None
    if not source.startswith("./"):
        fail(f"marketplace.json: plugin `{name}` source must be a relative path")
        return None

    plugin_dir = (ROOT / source).resolve()
    if not plugin_dir.is_dir():
        fail(f"marketplace.json: plugin `{name}` source `{source}` does not exist")
        return None

    manifest = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
    if manifest is None:
        return plugin_dir

    rel = (plugin_dir / ".claude-plugin" / "plugin.json").relative_to(ROOT)
    if manifest.get("name") != name:
        fail(f"{rel}: name `{manifest.get('name')}` != marketplace entry `{name}`")
    if manifest.get("version") != entry.get("version"):
        fail(
            f"{rel}: version `{manifest.get('version')}` != marketplace version "
            f"`{entry.get('version')}` — bump both together"
        )
    if not manifest.get("description"):
        fail(f"{rel}: missing `description`")

    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        fail(f"{plugin_dir.relative_to(ROOT)}: no skills/ directory")
    else:
        skills = [d for d in sorted(skills_dir.iterdir()) if d.is_dir()]
        if not skills:
            fail(f"{skills_dir.relative_to(ROOT)}: contains no skills")
        for skill_dir in skills:
            check_skill(skill_dir)

    return plugin_dir


def main():
    marketplace = load_json(MARKETPLACE)
    if marketplace is None:
        print("\n".join(f"error: {e}" for e in errors))
        return 1

    if not marketplace.get("name"):
        fail("marketplace.json: missing `name`")
    owner = marketplace.get("owner", {}).get("name")
    if not owner:
        fail("marketplace.json: missing `owner.name`")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        fail("marketplace.json: `plugins` must be a non-empty array")
        entries = []

    registered = set()
    for entry in entries:
        plugin_dir = check_plugin(entry, owner)
        if plugin_dir:
            registered.add(plugin_dir)

    # Catches the real footgun: adding a plugin folder but forgetting to list it.
    if PLUGINS_DIR.is_dir():
        for candidate in sorted(PLUGINS_DIR.iterdir()):
            if candidate.is_dir() and candidate.resolve() not in registered:
                fail(
                    f"plugins/{candidate.name}: not listed in "
                    ".claude-plugin/marketplace.json"
                )

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix in {".md", ".json", ".sh"} or path.name == "LICENSE":
            if "YOUR_GITHUB_USERNAME" in path.read_text(encoding="utf-8", errors="ignore"):
                fail(f"{path.relative_to(ROOT)}: unreplaced YOUR_GITHUB_USERNAME placeholder")

    if errors:
        for message in errors:
            print(f"error: {message}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s) found.", file=sys.stderr)
        return 1

    plugin_count = len(entries)
    print(f"OK — marketplace `{marketplace['name']}`, {plugin_count} plugin(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
