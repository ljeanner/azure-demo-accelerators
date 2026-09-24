# Contributing an accelerator

## What makes a good accelerator

- **Reproducible by someone else** without asking you a single question.
- **Parameterized**: the business scenario is a fill-in block, not hardcoded.
- **Grounded**: every product claim links to a Microsoft Learn page.
- **Honest about cost**: prerequisites, required capacity, setup time.

## How to

```bash
cp -r _template accelerators/my-accelerator
```

Then fill in `accelerators/my-accelerator/README.md`:

| Section | Expected content |
|---|---|
| Goal | One sentence: what the accelerator lets you demonstrate |
| Prerequisites | Licenses, capacity (e.g. Fabric F2+), roles, access |
| The prompt | A copy-paste ```` ``` ```` block with `<< ... >>` placeholders |
| Setup | Numbered steps in the portal / CLI |
| Demo script | The questions you ask live and the expected answers |
| Golden rules | The traps that make the demo fail |
| Sources | Microsoft Learn links (title + URL) |

## Non-negotiable rules

- ❌ No customer data, no real customer names, no PII.
- ❌ No secrets, keys, connection strings, or tokens — not even expired ones.
- ❌ No confidential, NDA, or unannounced content — this repo is public.
- ✅ Company, competitor, and people names must be **made up**.
- ✅ Fixed seeds so synthetic data is reproducible.

## Review

One PR = one accelerator. A reviewer confirms they could run it from scratch.

## Contributing Copilot examples

The [RCG Copilot kit](examples/copilot/README.md) is a separate collection of
opt-in examples, not an accelerator or an installed set of agents.
Keep examples in `examples/copilot/`; do not activate them for everyone by moving
them into `.github/` without an explicit decision.

For each example, explain when to use it, its inputs, expected outputs and limits.
Keep agent YAML frontmatter, skill folder names and `SKILL.md` names consistent
with the linked GitHub documentation. Scope instruction templates with `applyTo`
and explain which placeholders participants must replace.
Update the kit index when adding an example. Review formats, relative links and
copy destinations; do not claim runtime validation unless it was actually performed
in a supported Copilot client.
