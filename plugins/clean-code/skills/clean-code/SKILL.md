---
name: clean-code
description: Write and refactor code so it stays readable, understandable, and maintainable — clear naming, small single-purpose functions, guard clauses over deep nesting, minimal comments, DRY, sound class/SOLID design, and readable tests. Use this whenever producing more than a trivial snippet, writing or refactoring tests, reviewing existing code, or when the user mentions clean/readable/maintainable/well-structured code, code smells, tech debt, or refactoring — even if they never say the words "clean code." Do not use it for one-liners, config edits, or throwaway scripts where structure doesn't matter.
---

# Clean Code

Code is read far more often than it is written. The reader is usually someone else — or you, months later, or another agent — with none of the context you have right now. Clean code optimizes for that reader: it can be understood, changed, and trusted without archaeology. Everything below serves that one goal.

These are heuristics, not laws. The point is clarity, not compliance. If a rule here would make a specific piece of code *harder* to understand, break the rule. Judgment is the skill; the rules are just its common shortcuts.

## How to apply this

**Write it clean the first time.** Don't produce a messy draft and plan a cleanup pass — apply these habits as you type. Clean code is a default posture, not a phase.

**Match the codebase you're in.** Consistency with the surrounding code beats importing your preferred style. If the project names things `snake_case`, uses tabs, and returns error codes, follow that. A "cleaner" file that clashes with its neighbors is a net loss in readability.

**Don't over-engineer (KISS / YAGNI).** The most common failure mode for a capable coder is *too much* structure: speculative abstractions, config for options no one asked for, patterns applied for their own sake. Solve the problem in front of you as simply as it can be solved. Add flexibility when a second real use case arrives, not before.

**Stay in scope.** When editing existing code, resist silently rewriting unrelated things. If you spot a real problem outside your task, mention it or fix it in a clearly separate, described change — don't fold a surprise refactor into an unrelated diff.

The sections below are ordered by how often they matter. Naming and functions carry most of the weight; read those closely. `references/` holds the deeper material.

## Naming

Names are the primary documentation. A good name removes the need for a comment.

- **Reveal intent.** The name should answer *why it exists, what it holds, how it's used* — without a comment. `elapsedTimeInDays` beats `d`. `getActiveUsers()` beats `getData()`.
- **Say what you mean; don't disinform.** Don't call something a `List` if it's a map. Don't name a boolean `flag`. Avoid names that differ by a single letter or a noise word (`ProductData` vs `ProductInfo` — pick one meaning).
- **Functions are verbs; variables and classes are nouns.** `calculateTotal()`, `isEligible`, `PaymentProcessor`. Booleans read as yes/no questions: `isActive`, `hasPermission`, `canRetry`.
- **Prefer full words over abbreviations.** `message` not `msg`, `index` not `idx` — unless the abbreviation is a universal convention in the domain (`id`, `url`, `http`).
- **Length scales with scope.** A loop counter living for two lines can be `i`. A module-level constant needs a name that stands on its own.
- **Drop redundant context.** Inside a `User` class, a method named `user.getUserName()` stutters — `user.getName()` is enough.

**Before**
```js
function proc(d, f) {
  const r = d.filter(x => x.a > f);   // what is a? what is f?
  return r;
}
```
**After**
```js
function findExpensiveOrders(orders, minTotal) {
  return orders.filter(order => order.total > minTotal);
}
```

## Functions

A function is the unit readers reason about. Small, honest functions are the biggest single lever on maintainability.

- **Do one thing.** If you can meaningfully describe what a function does using the word "and," it's probably two functions. A function that validates, saves, and emails is three.
- **One level of abstraction per function.** Don't mix high-level policy (`chargeCustomer()`) with low-level detail (byte fiddling, string formatting) in the same body. High-level functions read like a summary that delegates to named steps.
- **Keep the parameter list short.** Zero to two parameters is comfortable; three is a smell; more than that usually means the arguments want to be an object. Fewer parameters = fewer ways to call it wrong.
- **Avoid boolean flag parameters.** `render(true)` tells the reader nothing, and a function that branches on a flag is doing two things. Split it: `renderVisible()` / `renderHidden()`.
- **Command–query separation.** A function should either *do* something (change state) or *answer* something (return a value) — not both. `if (setAndCheck(x))` hides a side effect inside a question.
- **Prefer return values over output arguments.** Mutating a passed-in object as a hidden result is surprising; return the new value instead.

**Before**
```js
function handleUser(user, sendEmail) {
  if (user.age >= 18) {
    user.status = "active";
    db.save(user);
    if (sendEmail) mailer.send(user.email, "Welcome");
    return true;
  }
  return false;
}
```
**After**
```js
function isAdult(user) {
  return user.age >= 18;
}

function activate(user) {
  user.status = "active";
  db.save(user);
}

// caller expresses the policy at one level of abstraction:
if (isAdult(user)) {
  activate(user);
  mailer.send(user.email, "Welcome");
}
```
The flag disappeared, each function does one thing, and the caller reads like the business rule it implements.

## Control flow and error handling

Nesting is where readability goes to die. Every level of indentation is a fact the reader has to hold in their head.

- **Guard clauses / early return.** Handle edge cases and invalid input up front and return, so the main path stays flat and unindented. Prefer this over an `else` that wraps the whole body.
- **Prefer positive conditions.** `if (isValid)` is easier to parse than `if (!isNotValid)`. Avoid double negatives.
- **Don't nest deeper than you must.** Two levels is fine; at three, look for an extract-function or a guard clause. Deep `if/else` pyramids often hide a missing polymorphism or lookup table.
- **Throw errors; don't return error codes.** Error codes force every caller to remember to check them and tangle the happy path with failure handling. Throwing separates the two. Handling an error is "one thing" — a function that does it shouldn't also do other work.
- **Replace sprawling `switch`/`if-else` on a type with polymorphism or a map** when the same switch keeps reappearing across the codebase (see `references/code-smells.md`).

**Before**
```js
function getPayAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = 0;
  } else {
    if (employee.isRetired) {
      result = retiredAmount();
    } else {
      result = normalPayAmount();
    }
  }
  return result;
}
```
**After**
```js
function getPayAmount(employee) {
  if (employee.isSeparated) return 0;
  if (employee.isRetired) return retiredAmount();
  return normalPayAmount();
}
```

## Comments and formatting

Most comments are apologies for code that isn't clear enough. Fix the code first; comment only what the code genuinely can't say.

- **Don't comment *what* — make the code say it.** `i++; // increment i` is noise. A well-named function beats a comment describing what the code does.
- **Do comment *why*** — intent, tradeoffs, non-obvious constraints, a workaround for a specific bug, a warning about consequences. These carry information the code cannot.
- **Delete commented-out code.** Version control remembers it; a dead block in the file just confuses the reader about whether it matters. Never leave it behind.
- **Don't narrate your own process.** Comments like `// now we loop through the results` or `// added this to fix the thing` are for a conversation, not a codebase.
- **Keep public APIs documented** where the ecosystem expects it (docstrings, JSDoc) — that's reference material for callers, not clutter.
- **Formatting:** keep related lines together and put dependent functions near each other; keep lines short enough to read without scrolling; follow the project's formatter/linter rather than hand-aligning. Let the tool win.

## DRY and the right level of abstraction

- **Don't Repeat Yourself** — for *knowledge*, not for text. If the same business rule or calculation lives in two places, changing it means finding both; extract it. But two lines that merely *look* similar and change for different reasons are not duplication — forcing them together couples things that should move independently.
- **Beware premature DRY.** Two copies is often fine; wait for the third and the real pattern before abstracting. A wrong abstraction is more expensive than a little duplication, because everyone downstream has to bend around it.
- **Keep abstraction levels honest.** A module named for a concept should contain only that concept's logic. When a function reaches "down" into unrelated detail, extract that detail behind its own name.

## Objects and classes

- **Objects vs. data structures.** A *data structure* (DTO, record) exposes data and has little behavior — fine for carrying values across a boundary. An *object* hides its data and exposes behavior. Don't build a half-object that exposes everything *and* has methods; pick one.
- **Tell, don't ask.** Instead of pulling data out of an object to make a decision about it, tell the object to do the thing. `account.withdraw(amount)` beats reading `account.balance`, computing, and writing it back from outside.
- **Law of Demeter — don't talk to strangers.** `a.getB().getC().doThing()` reaches through the internals of other objects and welds you to their structure. Ask your immediate collaborators for what you need.
- **Small classes with one responsibility.** Size is measured in responsibilities, not lines. If a class name needs "and" or vague words like `Manager`/`Processor` to describe it, it likely does too much.

The five SOLID principles expand on class design (single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion). When you're designing types, class hierarchies, or module boundaries — or reviewing an OO design — read **`references/solid.md`**.

## Tests

Test code is real code and rots the same way — and messy tests fail quietly, by being ignored rather than by breaking. The essentials:

- **Name tests by behavior**, so a failure explains itself: `expired_token_returns_401`, not `test_auth()`.
- **One concept per test.** Several assertions verifying a single outcome are fine; three unrelated behaviors are three tests.
- **Test behavior, not implementation.** Tests coupled to internals break on every refactor, which teaches the team that refactoring is expensive — the opposite of what tests are for.
- **Keep them fast, independent, and deterministic.** A flaky test is worse than no test: it trains everyone to ignore red.
- **Don't over-test.** Don't test the language or the framework, and don't chase a coverage number — coverage shows what ran, not what was verified.

When writing, reviewing, or refactoring tests, read **`references/testing.md`** for the fuller treatment: Arrange–Act–Assert structure, boundary cases, mocking restraint, and how DRY applies differently in test code.

## Self-review before you finish

Reread the code you just wrote as if you'd never seen it, and ask:

- Could a new reader understand each name without a comment or hunting for a definition?
- Does each function do one thing, at one level of abstraction, with a short parameter list?
- Is the happy path flat, with edge cases handled by guard clauses up front?
- Did I delete every commented-out block and every comment that only restates the code?
- Is any comment that remains explaining *why*, not *what*?
- Did I add abstraction the current problem doesn't actually need? If so, remove it.
- If I wrote tests: does each one name the behavior it checks, cover the edges, and survive a refactor of the internals?
- Does the style match the surrounding code?

If something fails a check, fix it now — that is the cleanup pass, and it's cheapest before the code is ever committed.

## Reference files

- **`references/solid.md`** — the five SOLID principles with before/after examples. Read when designing classes, interfaces, hierarchies, or module boundaries.
- **`references/testing.md`** — writing clean, readable, trustworthy tests. Read when writing, reviewing, or refactoring tests.
- **`references/code-smells.md`** — a catalog of common code smells (long function, feature envy, shotgun surgery, primitive obsession, repeated switch, etc.) each paired with the refactoring that resolves it. Read when reviewing or refactoring existing code and you sense something is off but want to name it.
