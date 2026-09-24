# Hackathon day

A one-page plan for running (or surviving) a one-day demo hackathon with these accelerators.

---

## Before you arrive

| # | Check | Why |
|---|---|---|
| 1 | An Azure subscription where you are **Owner + User Access Administrator** | The Terraform baseline creates role assignments. `Owner` alone fails. |
| 2 | `az login` works and the right subscription is selected | `az account show` |
| 3 | Fabric is enabled on the tenant, and you can create workspaces | Ask your tenant admin the day *before*, not the day of |
| 4 | Terraform ≥ 1.9 and Python ≥ 3.10 installed | `terraform version`, `python --version` |
| 5 | Quota for your chat + embedding models in your region | Model capacity is regional and is the #1 cause of a failed `apply` |
| 6 | A **one-sentence scenario** written down | "A retailer wants to know why one store is underperforming." If you can't say it in one sentence, you don't have a demo yet. |

> If item 3 or 5 is uncertain, pick Track A below — it needs the least tenant cooperation.

---

## Tracks

Pick one. Do not try to do two.

### Track A — Data agent in a day (most reliable)

**Outcome:** a Fabric data agent answering business questions on a synthetic dataset you invented.

| Time | Step |
|---|---|
| 0:00 – 0:30 | Write the **5 questions** you will ask on stage. Nothing else. |
| 0:30 – 1:15 | Run [`fabric-data-agent-synthetic-data`](accelerators/fabric-data-agent-synthetic-data/) → the reference notebook, adapted to your domain |
| 1:15 – 1:45 | Verify the aggregates. Your 5 questions must have visible answers. |
| 1:45 – 2:30 | Create the data agent, add descriptions on every table and column |
| 2:30 – 3:15 | Add agent instructions + example queries, test all 5 questions twice |
| 3:15 – 4:00 | Rehearse out loud, timed |

### Track B — Full platform (if you need Foundry too)

**Outcome:** Track A, plus an AI Foundry project with models and search on top.

| Time | Step |
|---|---|
| 0:00 – 0:20 | `terraform apply` on [`fabric-foundry-terraform-baseline`](accelerators/fabric-foundry-terraform-baseline/) — start it early, it is the long pole |
| 0:20 – 2:00 | Track A steps, in the workspace Terraform just created |
| 2:00 – 3:00 | Index the lakehouse into AI Search (`seed/ai-search-onelake/`) |
| 3:00 – 4:00 | Put a Foundry agent in front with [`foundry-agent-over-fabric-data-agent`](accelerators/foundry-agent-over-fabric-data-agent/), rehearse |

---

## Timeboxing rules

- **Freeze the data at T+2h.** Past that point, no new tables, no new columns. Spend the rest on
  the narrative.
- **One blocker = 20 minutes.** If you are still stuck after 20 minutes, ask, or cut the feature.
  A smaller demo that runs beats a big one that doesn't.
- **Rehearse before you polish.** The last hour is for speaking, not for building.

---

## What "done" looks like

A demo is ready when all of these are true:

- [ ] You can state the scenario in **one sentence**, without notes.
- [ ] Your 5 questions run **twice in a row** with the same, correct answers.
- [ ] Every number you will say out loud, you have **already seen** in the verification cell.
- [ ] Someone else ran your notebook end to end and got **your numbers** (fixed seed).
- [ ] You know what to say when it fails live. It will fail once.
- [ ] Total runtime is **under 8 minutes**.

---

## Common failure modes

| Symptom | Real cause | Fix |
|---|---|---|
| Agent answers vaguely or picks the wrong table | No table/column descriptions | Describe every table and non-obvious column. This is the highest-leverage fix, by far. |
| Agent does the right SQL but the answer is boring | Uniform random data | Plant the storyline in the data (section 4 of the notebook) |
| `terraform apply` fails on a model deployment | Regional TPM quota | Lower `capacity` in `var.chat_model`, or change region |
| `terraform apply` fails on a role assignment | Missing User Access Administrator | Ask for the role, or deploy into a resource group you own |
| Agent contradicts itself between two runs | Ambiguous metric definition | Define it in the agent instructions: "revenue means `net_amount`" |
| Foundry agent never calls the Fabric tool | No tool routing in the instructions | Say it explicitly, or force it with `tool_choice="required"` |
| Foundry agent works for you, fails for a colleague | Fabric tool uses identity passthrough | Grant them `READ` on the data agent **and** on the lakehouse |
| Everything worked yesterday, nothing works today | Capacity paused, or session expired | `scripts/capacity.sh resume`, `az login` |

---

## After the hackathon

- **Pause the capacity** (`scripts/capacity.sh pause`) or `terraform destroy`. An F-SKU bills by
  the hour whether or not you use it.
- If your demo worked, **turn it into an accelerator**: copy [`_template/`](_template/) and open a
  PR. The next person should not start from zero.
