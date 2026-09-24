# Azure Demo Accelerators

[![CI](https://github.com/ljeanner/azure-demo-accelerators/actions/workflows/ci.yml/badge.svg)](https://github.com/ljeanner/azure-demo-accelerators/actions/workflows/ci.yml)

Reusable recipes for building **credible Azure / Fabric / AI demos, fast**.
Each accelerator is one folder: a `README.md`, a copy-paste prompt, and a setup checklist.

> **No customer data, no PII, no secrets.** Everything here is synthetic and built from public
> Microsoft Learn documentation.

---

## Available accelerators

| Accelerator | What it unlocks | Est. time |
|---|---|---|
| [`fabric-foundry-terraform-baseline`](accelerators/fabric-foundry-terraform-baseline/) | One `terraform apply` for a demo platform: Fabric capacity **+ workspace + lakehouse**, AI Foundry account + project + models, AI Search wired to the project, Cosmos/Storage/App Insights, the ~25 role assignments agents need, and pause/resume scripts to stop the billing | 20 min |
| [`fabric-data-agent-synthetic-data`](accelerators/fabric-data-agent-synthetic-data/) | A copy-paste prompt **and a runnable reference notebook** to generate a coherent synthetic dataset with a planted storyline, write it as Delta tables in a Fabric Lakehouse, and wire it to a **Fabric Data Agent** (natural language → SQL) | 2-3 h |
| [`foundry-agent-over-fabric-data-agent`](accelerators/foundry-agent-over-fabric-data-agent/) | Put a **Foundry agent** in front of your Fabric data agent: project connection script, two working Python clients, demo script and troubleshooting table | 45 min |

---

## Copilot skill

The method above is also packaged as a **GitHub Copilot skill**, so the agent applies it without
being asked:

```bash
# user scope (all your projects)
cp -r skills/fabric-demo-data-agent ~/.copilot/skills/
```

```powershell
# Windows
Copy-Item skills\fabric-demo-data-agent "$env:USERPROFILE\.copilot\skills\" -Recurse
```

Cloning this repo is enough to get it at **project scope** — skills in `skills/` are picked up
automatically. Then just ask: *"build me demo data for a Fabric data agent"*.

---

## Quick start (hackathon)

> **Running a hackathon today?** Go straight to **[HACKATHON.md](HACKATHON.md)** —
> prerequisites checklist, two timeboxed tracks, definition of done, and the common failure modes.

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

## Credits

Some accelerators adapt work shared by colleagues. Credit and a link to the original
are always stated at the top of the accelerator's README.

- `fabric-foundry-terraform-baseline` — adapted from the FabCon 2026 workshop by
  [Damien Aicheh](https://github.com/damienaicheh), shared with permission.

---

## Contributing

Built a demo that landed? Publish it here.

1. Copy [`_template/`](_template/) to `accelerators/<short-kebab-case-name>/`.
2. Fill in the README (context, prompt, checklist, Microsoft Learn sources).
3. Add a row to the table above.
4. Open a PR.

See [CONTRIBUTING.md](CONTRIBUTING.md).
