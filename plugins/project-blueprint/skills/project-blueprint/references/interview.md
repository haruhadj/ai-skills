# The Interview

Resolving the decisions that change the work, before any planning happens.

## Why this stage exists

A plan built on unstated assumptions is a plan that gets thrown away. The interview's job is to find the small number of forks where different answers produce genuinely different architectures — and to settle them while settling them is still free.

## What makes a question worth asking

**The answer changes what you build.** If both answers lead to the same code, decide it yourself and mention the choice in a sentence.

```
❌ "Should I use TypeScript?"            — conventional default exists
❌ "What should I name the project?"     — doesn't change the work
❌ "Do you want tests?"                  — the answer is yes
✅ "Multi-tenant SaaS, or sold as a codebase?"  — changes everything downstream
```

**It cannot be answered by reading.** Anything discoverable in the repo, the git history, or the package manifest is your job, not theirs.

**It is not already answered by an earlier constraint.** This is the one most often missed — see below.

## Find the forced answers

Constraints propagate. Before asking, check whether an earlier answer already decided it.

> User says: *"I want to sell the codebase to clients."*
> Question you were about to ask: *"Is the buyer technical or non-technical?"*
> Already answered: a non-technical buyer cannot deploy a monorepo with Postgres and migrations. The buyer is necessarily a developer.

Saying so is worth more than asking, because it also surfaces the *consequences*: no setup wizard, docs are a deliverable, the admin UI matters more than you'd think because it's what the agency demos to their client.

Look for forced answers after every user answer. One constraint often settles three questions.

## Always recommend

Give a default and the reasoning. The user should be reacting to a proposal, not doing your thinking — they have less context about the tradeoff than you do at that moment.

```
❌ "Which database?"
✅ "Postgres — the only sane default for self-hosting, and every host has it.
    Say the word if you need something else."
```

Mark the recommendation explicitly when using a question tool, and put it first.

## Push back once, then commit

If a stated constraint conflicts with the stated goal, say so — briefly — and propose the amendment:

> "No payments in v1" plus "sell the codebase" pull against each other: a buyer evaluating an e-commerce starter looks for checkout within ninety seconds. I'd build the payment *abstraction* plus one reference provider — three extra days, and it makes the product sellable.

Then record it as an amendment with a `Revisit if:` condition. If the user reaffirms the original, build the original. Raising a concern twice is nagging.

## Question sets by project type

Adapt; these are prompts, not a script.

### Any project

1. **Delivery model** — SaaS you host, self-hosted by users, sold as source, internal tool? *Drives auth, tenancy, config, docs.*
2. **Primary user** — and are they the same as the buyer? *Two audiences means two quality bars.*
3. **Scope appetite** — thin vertical slice, or full-featured? *Decides whether to prove the architecture first.*
4. **Hard constraints** — deadline, budget, team size, mandated stack, compliance.

### Web applications

5. **Data source** — user entry, import, external API sync, generated?
6. **Auth model** — none, single-user, accounts, roles, SSO?
7. **Deployment target** — a specific cloud, self-hosted, air-gapped? *Rules out managed-service dependencies.*
8. **Locale and currency reach** — cheap to design in, brutal to retrofit.

### Anything commercial

9. **Payments** — who owns the merchant relationship?
10. **Compliance** — PCI, GDPR, accessibility, industry-specific?
11. **Licensing** — if sold: per-site, unlimited, support term? *Blocks release, not development — ask early, decide before launch.*

### Existing codebases

12. **What hurts today?** — the answer names the real project.
13. **What must not break?** — the invariants nobody wrote down.
14. **Where does the team keep getting it wrong?** — that is the missing context file.

## Traps

**Too many questions at once.** Four is a comfortable maximum. Ask the ones that unblock the next step; the rest will be better questions after those answers.

**Questions whose options are all the same.** If you can't articulate how the options differ in what you'd write, it isn't a real fork.

**Deferring a genuine fork.** "We can decide later" is right for reversible choices and wrong for schema, money representation, and tenancy — where "later" means a migration across every query.

**Asking instead of doing.** If you have enough to act, act. Blocking on a question the user must answer before anything ships should be reserved for cases where a wrong guess makes the work useless.

## Recording the answers

Every answer becomes a row in the decision log, with its reasoning. An unrecorded answer will be asked again in three sessions, and the second answer may differ from the first.
