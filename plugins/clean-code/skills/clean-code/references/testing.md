# Clean Tests

Test code is real code, and it rots the same way. The difference is that messy tests fail *quietly*: they don't crash, they just stop being trusted. Once a suite is slow, flaky, or unreadable, people skip it, disable it, or stop adding to it — and the safety net that made refactoring possible is gone. Tests are what let you change production code with confidence, so they deserve the same care as the code they protect.

Everything below serves one goal: a test suite that a reader can understand at a glance and a team can keep running.

## A test should read like a specification

The primary audience for a test is someone trying to understand what the code is *supposed* to do. When a test fails at 2am, the name and body should explain the intent without the reader opening the implementation.

**Name tests by behavior, not by method.** `test_calculate()` tells you nothing when it goes red. Describe the scenario and the expected outcome: `withdrawing_more_than_balance_is_rejected`, `expired_token_returns_401`. A good name makes the failure output self-explanatory.

**Use the Arrange–Act–Assert shape.** Set up the world, perform the one action under test, check the result — visually separated, in that order. Consistent structure means a reader recognizes the shape instantly instead of parsing it.

```python
def test_expired_coupon_is_not_applied():
    # Arrange
    cart = Cart(subtotal=100)
    coupon = Coupon(code="SAVE10", expires_on=YESTERDAY)

    # Act
    result = cart.apply(coupon)

    # Assert
    assert result.total == 100
    assert result.error == "coupon expired"
```

**Keep the noise out of the test body.** Only the details relevant to *this* scenario belong in the test; everything else goes behind a well-named helper or factory (`a_user_with_expired_subscription()`). A reader should see the one thing that makes this case different, not twenty lines of unrelated setup.

## One concept per test

**Assert one behavior, not one assertion.** The rule is often stated as "one assert per test," but the real goal is one *concept*. Several assertions that together verify a single outcome (as above — total unchanged *and* the right error) are fine. Assertions that verify three unrelated behaviors are three tests wearing a trenchcoat.

Why it matters: when a multi-concept test fails, you don't know which behavior broke, and the first failing assertion hides the rest.

**Avoid branching in tests.** An `if` or a loop in a test means the test is deciding what to check at runtime — so it can silently check nothing. If you need to cover several inputs, use your framework's parameterized/table-driven support, which keeps each case reported separately.

## Test behavior, not implementation

Tests coupled to *how* code works break every time you refactor, which teaches the team that refactoring is expensive — the exact opposite of what tests are for.

- Assert on observable outcomes (returned values, resulting state, messages actually sent), not on private internals or the exact sequence of internal calls.
- Be sparing with mocks. Mock things you don't control or that are slow (network, clock, filesystem, payment gateway). Mocking your own internals bolts the test to today's structure. Over-mocked tests pass while the real system is broken.
- If a test needs to reach into private state to verify anything, that's usually a design signal: the behavior you want to observe isn't exposed anywhere, which the *production* code's callers may also be suffering from.

## Test the boundaries

Bugs cluster at edges, so that's where tests earn the most:

- Empty and single-element collections; zero, negative, and maximum values.
- Off-by-one boundaries — if a rule says "over 18," test 17, 18, and 19.
- `null`/`None`/missing fields, and malformed input.
- Error paths, not just the happy path. Assert that the *right* failure happens, not merely that something failed.

**When you fix a bug, first write the test that reproduces it.** It proves you understood the cause, and it stops the bug from returning silently.

## Keep them fast and independent

- **Fast.** Slow suites get skipped. Keep unit tests to milliseconds by isolating them from network, database, and real sleeps. If you're testing time-dependent logic, inject the clock rather than sleeping.
- **Independent.** Each test sets up its own state and passes in any order, alone or with others. Tests that depend on a shared mutable fixture, or on running after another test, produce failures that can't be reproduced in isolation.
- **Deterministic.** No dependence on real time, random seeds, timezone, locale, or network. A flaky test is worse than no test: it trains everyone to ignore red.
- **Repeatable.** Running the suite twice in a row gives the same result, with no manual cleanup in between.

## Don't over-test

The same restraint that applies to production code applies here — this is where a capable agent most often overshoots.

- Don't test the language, the framework, or third-party libraries. Testing that a getter returns what a setter set verifies nothing about your logic.
- Don't chase a coverage number for its own sake. Coverage shows what was *executed*, not what was *verified*; 100% coverage with weak assertions is theater. Aim coverage at logic that can plausibly break.
- Don't write tests so tightly specified that any reasonable change breaks them. If a small refactor reliably reddens twenty tests, the tests are over-specified.
- Prefer a few meaningful tests over many trivial ones. Every test is code someone has to maintain.

## Refactor tests too

Duplication, unclear names, and dead code are bugs in a test file exactly as they are elsewhere. Extract shared setup into named builders, delete tests for removed behavior, and rename tests when the behavior they describe changes.

Two cautions specific to tests:

- **DRY applies more loosely here.** A little duplication that keeps a test readable in isolation is usually worth it; over-extracting setup into deep helper hierarchies makes a failing test impossible to understand without spelunking. Readability beats deduplication in test code.
- **Never "fix" a test by weakening it.** Deleting the assertion, loosening the matcher, or adding a retry to quiet a flaky test destroys the signal you built it for. Find the real cause — usually shared state, timing, or a genuine bug.

Finally: a test that's been skipped or commented out for more than a moment is either a question that needs answering or dead code. Fix it or delete it — a permanently disabled test is a lie about your coverage.
