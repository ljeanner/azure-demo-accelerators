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
- ❌ No NDA or unannounced content.
- ✅ Company, competitor, and people names must be **made up**.
- ✅ Fixed seeds so synthetic data is reproducible.

## Review

One PR = one accelerator. A reviewer confirms they could run it from scratch.
