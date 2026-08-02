# SOLID Principles

Five principles of class and module design. They aim at one thing: making code cheap to change. Apply them where they earn their keep — a growing OO system with real variation. Don't retrofit them onto a two-field data class; that's the over-engineering this whole skill warns against.

## Contents
- [S — Single Responsibility](#s--single-responsibility-principle)
- [O — Open/Closed](#o--openclosed-principle)
- [L — Liskov Substitution](#l--liskov-substitution-principle)
- [I — Interface Segregation](#i--interface-segregation-principle)
- [D — Dependency Inversion](#d--dependency-inversion-principle)

---

## S — Single Responsibility Principle

A class (or module, or function) should have one reason to change. Equivalently: it should answer to one stakeholder or concern. Mixing concerns means a change for one reason risks breaking the others, and the class grows without bound.

The tell: a class whose name is vague (`Manager`, `Processor`, `Helper`) or whose description needs "and."

**Before** — one class formats a report *and* persists it *and* talks to the network. Three reasons to change.
```js
class Report {
  generate() { /* build report text */ }
  saveToDisk(path) { /* file I/O */ }
  emailTo(address) { /* SMTP */ }
}
```
**After** — each concern lives on its own, composed by a caller.
```js
class Report { generate() { /* build report text */ } }
class ReportFileStore { save(report, path) { /* file I/O */ } }
class ReportMailer { send(report, address) { /* SMTP */ } }
```
Now a change to the email mechanism can't break report generation.

## O — Open/Closed Principle

Software entities should be open for extension but closed for modification. You should be able to add new behavior without editing existing, tested code — usually by adding a new type rather than adding another branch to a switch.

**Before** — every new shape forces an edit to `area()`.
```js
function area(shape) {
  switch (shape.type) {
    case "circle": return Math.PI * shape.r ** 2;
    case "square": return shape.side ** 2;
    // add a triangle? edit this function again
  }
}
```
**After** — a new shape is a new class; `area` never changes.
```js
class Circle { area() { return Math.PI * this.r ** 2; } }
class Square { area() { return this.side ** 2; } }
// area(shape) => shape.area()
```
Don't chase this preemptively. Apply it once you've seen the switch grow, which is the signal the axis of change is real.

## L — Liskov Substitution Principle

A subtype must be usable anywhere its base type is expected, without surprising the caller. If a subclass throws on a method the base supports, weakens a guarantee, or demands stricter input, it breaks code written against the base.

The classic trap: `Square extends Rectangle`. Setting width on a rectangle shouldn't change its height — but for a square it must, so code that relied on rectangle behavior breaks when handed a square. The inheritance models "is-a" grammatically but not behaviorally. Prefer composition or a shared abstraction that both honestly satisfy.

Rule of thumb: if you find yourself checking `if (x instanceof SubType)` to special-case a subtype, the substitution has already failed.

## I — Interface Segregation Principle

Don't force a class to depend on methods it doesn't use. Many small, focused interfaces beat one fat one, because a fat interface drags every implementer into changes they don't care about.

**Before** — a read-only client is forced to implement writes it will never use.
```ts
interface Repository {
  find(id): Item;
  save(item): void;
  delete(id): void;
}
```
**After** — split by capability; clients depend only on what they use.
```ts
interface ReadableRepository { find(id): Item; }
interface WritableRepository { save(item): void; delete(id): void; }
```

## D — Dependency Inversion Principle

High-level policy should not depend on low-level detail; both should depend on an abstraction. Concretely: a business-logic class shouldn't `new` up a specific database or HTTP client. Depend on an interface and have the concrete implementation passed in (dependency injection). This makes the policy testable and lets the detail change without touching the policy.

**Before** — the service is welded to a specific implementation.
```js
class OrderService {
  constructor() { this.db = new PostgresClient(); } // hard dependency
  place(order) { this.db.insert(order); }
}
```
**After** — the service depends on an abstraction it's handed.
```js
class OrderService {
  constructor(store) { this.store = store; } // any OrderStore
  place(order) { this.store.insert(order); }
}
// wiring happens at the edge: new OrderService(new PostgresOrderStore())
```
Now tests can pass an in-memory store, and swapping the database never touches `OrderService`.

---

**A closing caution.** SOLID is a toolkit for managing *variation and growth*. Each principle trades some indirection for flexibility. If a piece of code isn't varying and isn't growing, that indirection is pure cost. Reach for these when the pain they prevent is real, not on principle.
