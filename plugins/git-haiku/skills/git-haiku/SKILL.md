---
name: git-haiku
description: Inspect the working tree with git status/diff, write a concise Conventional Commits message, commit, and push to the current remote branch. Use when the user asks to commit, commit and push, or "ship" the current changes and wants it done quickly without a review pass. Do not use it when the user wants the changes reviewed, explained, or split into multiple logical commits, or when history needs rewriting (amend, rebase, force-push).
---

# git-haiku

Fast, low-ceremony commit-and-push. Inspect, write the message, commit, push, report. No narration between steps.

## Procedure

1. **Inspect.** `git status` for the branch and the staged/unstaged split, `git diff` for unstaged changes, `git diff --staged` when something is already staged. Read the diff — the message describes what changed, not what you were asked to do.
2. **Branch check.** If the current branch is `main` or `master`, create a topic branch first (`git switch -c <type>/<short-slug>`) and commit there.
3. **Stage.** Stage the files that belong to the message. If the diff contains unrelated changes, stage only the related ones and say what was left behind.
4. **Message.** Conventional Commits: `type(scope): summary`.
   - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`.
   - Imperative mood, no trailing period, summary under 72 characters.
   - Body only when the *why* is not obvious from the summary — wrapped at 72 columns.
5. **Commit.** `git commit -m "<message>"` (repeat `-m` for the body).
6. **Push.** `git push`, or `git push -u origin <branch>` when the branch has no upstream.
7. **Report.** Commit hash, message, branch. Nothing else.

## Message examples

```
feat(auth): add refresh-token rotation
fix(parser): handle empty input without panicking
docs(readme): document the plugin install path
chore(deps): bump serde to 1.0.219
```

## Rules

- Nothing to commit → say so and stop.
- Never amend, rebase, reset, or force-push. A rejected push is reported, not worked around.
- Never commit secrets, `.env` files, or large build artifacts — if the diff contains them, stop and flag it.
- One coherent change per commit. If the working tree holds two unrelated changes, commit the one the user asked about and name the other.
