# Code Smells and Their Refactorings

A code smell is a surface symptom that often — not always — points to a deeper problem. A smell is an invitation to look, not a verdict. Confirm the underlying issue before refactoring, and don't refactor code you weren't asked to touch without saying so.

Each entry: what it looks like, why it hurts, and the refactoring that resolves it.

## Contents
- [Bloaters](#bloaters) — things that grew too big
- [Object-orientation abusers](#object-orientation-abusers)
- [Change preventers](#change-preventers) — one change forces many
- [Dispensables](#dispensables) — things adding no value
- [Couplers](#couplers) — excessive entanglement

---

## Bloaters

**Long function.** A function that scrolls off the screen or mixes many steps. Hurts because you can't hold it in your head. → *Extract Function*: pull each cohesive step into a well-named helper until the original reads like a summary.

**Long parameter list.** Four+ parameters, or several that always travel together. Hard to call correctly; order-dependent. → *Introduce Parameter Object* (bundle related params into one type) or *Preserve Whole Object* (pass the object you were pulling fields out of).

**Large class.** A class with too many fields and methods — usually multiple responsibilities. → *Extract Class* along responsibility lines (see SRP in `solid.md`).

**Primitive obsession.** Representing a domain concept with a raw string/number — `"USD"` + a float for money, a bare string for an email, a `{lat, lng}` pair passed everywhere. Validation and behavior get scattered across the codebase. → *Introduce a small value type* (`Money`, `EmailAddress`, `Coordinate`) that owns its rules.

**Data clumps.** The same group of fields appears together in many places (start/end date, x/y/z). → Bundle them into their own type; the clump was a hidden concept.

## Object-orientation abusers

**Repeated switch / type-checking conditional.** The same `switch (type)` or `if (x instanceof …)` appears in several places, and every new case means editing all of them. → *Replace Conditional with Polymorphism*, or a lookup map for simple cases (see OCP in `solid.md`).

**Temporary field.** A field that's only set and meaningful some of the time, empty otherwise — confusing to reason about. → *Extract Class* to hold the field and the logic that uses it, created only when needed.

**Refused bequest.** A subclass inherits methods it doesn't want or overrides them to throw. Inheritance was the wrong tool. → Replace inheritance with *composition/delegation* (see LSP in `solid.md`).

## Change preventers

**Divergent change.** One class changes for many different reasons — you edit it for the tax rules *and* the report format *and* the storage schema. → *Extract Class* so each reason to change lives in its own place (this is SRP restated as a smell).

**Shotgun surgery.** The inverse: one conceptual change forces small edits across many files. The knowledge is smeared out. → *Move* the scattered pieces together — inline the fragments into a single module that owns that concept.

## Dispensables

**Comments (as deodorant).** A comment explaining *what* a confusing block does. → Usually *Extract Function* with a descriptive name; the name replaces the comment. Keep comments that explain *why*.

**Duplicate code.** The same logic in two places. → *Extract Function* and call it from both — but only if they encode the *same* knowledge and will change together (see the DRY caution in the main skill; don't merge coincidental lookalikes).

**Dead code.** Unreachable branches, unused variables/functions, commented-out blocks. → Delete it. Version control is the archive; the file is for what's live.

**Speculative generality.** Abstract base classes, hooks, options, and parameters added "in case we need them," with only one real user. → Collapse the abstraction; inline the single implementation. This is over-engineering, and it's the smell a capable coder produces most often.

## Couplers

**Feature envy.** A method that spends most of its time reaching into *another* object's data — computing from that object's fields rather than its own. The method is in the wrong class. → *Move Function* to the class whose data it envies (this is "Tell, Don't Ask" as a smell).

**Message chains.** `a.getB().getC().getD().doThing()` — the caller is navigating other objects' internals and is now hostage to their structure. → *Hide Delegate*: give the immediate object a method that returns what you actually need (this is the Law of Demeter as a smell).

**Inappropriate intimacy.** Two classes that reach into each other's private parts and can't be understood or changed independently. → Move the shared responsibility to one owner, or extract the tangled concern into a third class both use through a clean interface.

---

**Using this catalog well:** name the smell, confirm the real problem is present (a long function that's genuinely one linear recipe may be fine as-is), pick the matching refactoring, and change behavior-preserving code in small verifiable steps with tests green between them. Refactoring means improving structure *without changing behavior* — if you're also fixing a bug or adding a feature, do that as a separate step so the diff stays honest.
