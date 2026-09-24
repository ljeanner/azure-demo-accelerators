# Azure Demo Accelerators

Reusable recipes for building **credible Azure / Fabric / AI demos, fast**.
Each accelerator is one folder: a `README.md`, a copy-paste prompt, and a setup checklist.

> Internal Microsoft repo. **No customer data, no PII, no secrets.** Everything is synthetic.

---

## Available accelerators

| Accelerator | What it unlocks | Est. time |
|---|---|---|
| [`fabric-data-agent-synthetic-data`](accelerators/fabric-data-agent-synthetic-data/) | Generate a coherent synthetic dataset, write it as Delta tables in a Fabric Lakehouse, and wire it to a **Fabric Data Agent** (natural language → SQL) | 2-3 h |

---

## Quick start (hackathon)

1. Pick the accelerator that matches your demo.
2. Open its `README.md` and paste the prompt into your assistant (Copilot, Claude, ChatGPT…).
3. Fill in the `<< ... >>` placeholders with **your** customer scenario.
4. Follow the setup checklist at the end of the README.
5. Rehearse the demo twice before showing it. An unrehearsed demo is a failed demo.

### The 3 rules that make the difference

1. **Scenario before data.** Write the 5 questions you will ask live first, then generate the data.
2. **The signal must be visible in aggregate.** If the gap doesn't jump out on a weekly chart, the agent won't "see" it either.
3. **Reproducibility.** Fixed seed, parameters at the top of the notebook: your colleagues must get exactly your numbers.

---

## Contributing

Built a demo that landed? Publish it here.

1. Copy [`_template/`](_template/) to `accelerators/<short-kebab-case-name>/`.
2. Fill in the README (context, prompt, checklist, Microsoft Learn sources).
3. Add a row to the table above.
4. Open a PR.

See [CONTRIBUTING.md](CONTRIBUTING.md).
