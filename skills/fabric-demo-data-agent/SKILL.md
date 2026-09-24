---
name: fabric-demo-data-agent
description: "Generate a realistic synthetic dataset, load it into a Microsoft Fabric lakehouse as Delta tables, and wire it to a Fabric data agent for a natural-language demo. USE FOR: fake data for a demo, synthetic dataset, demo data generator, fill a lakehouse, Fabric data agent, NL2SQL demo, build me a demo like Zava, prepare a customer demo on Fabric, demo storyline in data, data agent instructions and example queries. DO NOT USE FOR: real customer data, production data pipelines, or anonymising an existing dataset."
---

# Synthetic demo data → Fabric lakehouse → Fabric data agent

Build a credible demo where a **Fabric data agent** answers business questions in natural language
over data you invented. The hard part is not the data volume — it is that the data must **contain a
story worth telling**.

Reference implementation and a runnable notebook:
<https://github.com/ljeanner/azure-demo-accelerators>

---

## The one rule that decides everything

**Write the demo questions first, generate the data second.**

Uniform random data produces flat charts, and a data agent over flat charts looks useless. Decide the
3 to 5 questions you will ask on stage, then deliberately write their answers into the data.

A good question set has three shapes:

1. **Descriptive** — "Total revenue last quarter by region?" → establishes the numbers are real.
2. **Diagnostic** — "Which store is underperforming, and since when?" → this is the moment that lands.
3. **Comparative** — "What changed in category X over the last six months?" → proves it is not canned.

---

## Workflow

### Step 1 — Ask the user for the business context

Do not invent it silently. Ask for whatever is missing:

- fictional company (name, industry, country, scale)
- domains to cover (sales, stock, purchasing, production, margin, forecast, competition, HR…)
- data window (start → end date) and currency/language
- **the demo scenario**: a triggering event, its time window, and its expected effect in the data
- the 3 to 5 questions the agent must answer

If the user has no scenario, propose one. A demo without a scenario is not worth generating.

### Step 2 — Generate the notebook

Produce a **single PySpark notebook**, runnable in Fabric with a lakehouse attached, structured as:

- **Cell 0 — Configuration.** Every constant at the top: `SEED = 42`, date window, volumes
  (`N_SITES`, `N_PRODUCTS`, `N_CUSTOMERS`, `N_TRANSACTIONS`), scenario window. Nothing hardcoded below.
- **Section 1 — Dimensions.** `dim_*` tables: products, sites, customers, suppliers, competitors.
  Small, readable, pronounceable names — you will read them out loud.
- **Section 2 — Prices and promotions.** Price history with a few changes, promo calendar.
- **Sections 3..N — Facts.** `fact_*` tables: sales, stock, orders, production, margin, forecast.
- **Section — Storyline.** The cell that plants the signal. Explicit, commented, isolated.
- **Section — Validation.** Row counts, referential integrity, no nulls, and **3 aggregate queries that
  prove the signal is there**.
- **Section — Write to lakehouse.** A `TABLES = {"dim_x": df, ...}` dict, then per table
  `df.write.format("delta").mode("overwrite").saveAsTable(name)` with a fallback to
  `.save(f"Tables/{name}")`, printing rows written.

Data requirements to enforce:

| Requirement | Why |
|---|---|
| Star schema, valid foreign keys, zero orphan rows | The agent joins; broken joins produce wrong answers |
| Fixed seed (`random` **and** `numpy`) | Colleagues must reproduce your exact figures |
| Monthly seasonality, weekday effect, yearly trend | Makes time-based questions meaningful |
| Prices consistent with costs, plausible margins | The first thing an analyst in the room checks |
| Some noise, a few missing values | But **never** an inconsistency: no negative quantity, no date outside the window, no discount > 100% |
| The scenario visible **in aggregate** | If it does not jump out on a weekly `GROUP BY`, the agent will not see it either |
| Zero real data, zero PII, invented competitor names | Non-negotiable |

> A ready-made, tested, parameterised notebook exists at
> `accelerators/fabric-data-agent-synthetic-data/notebook/synthetic_data_to_lakehouse.ipynb`
> in the accelerators repo. Prefer adapting it over writing one from scratch — it already covers
> seasonality, the planted storyline, validation and a Spark/pandas fallback so it can be tested locally.

### Step 3 — Produce the three companion deliverables

The notebook alone is not enough. Always generate:

- **A data dictionary** (markdown): per table, its grain, its columns, their type and business meaning.
- **Data agent instructions** (< 15 000 characters): role, one description per table, when to use which
  table, business rules (margin thresholds, what "net revenue" means, fiscal vs calendar year),
  response tone, and the obligation to quote figures.
- **10 example queries**: natural-language question → validated SQL, covering the demo questions.

### Step 4 — Set it up in Fabric

1. **Workspace + lakehouse** — F2 capacity minimum (the floor for data agents). Create the lakehouse.
2. **Notebook** — import it, attach the lakehouse, Run all, check the Delta tables under `Tables/`.
3. **Data agent** — *New item → Data agent*, add the lakehouse from the OneLake catalog
   (up to 5 sources: lakehouse, warehouse, Power BI semantic model, KQL database, ontology, Microsoft Graph).
   **Select only the tables the demo needs** — fewer tables, better SQL.
4. **Descriptions** — describe every table and every non-obvious column. Highest-leverage step, by far.
5. **Instructions** — paste deliverable 2.
6. **Example queries** — paste deliverable 3. This is the number-one precision lever for
   lakehouse/warehouse/KQL sources (not supported for Power BI semantic models).
7. **Test, then Publish.** Replay the demo questions, fix the descriptions and examples — not the
   questions. An unpublished data agent cannot be consumed downstream.
8. **Version it** — enable workspace Git integration; `draft/` and `published/` hold the agent config,
   so colleagues can replay it.

### Step 5 — Rehearse

Run every question **twice**, out loud, timed. Every number you will say must be one you have already
seen in the validation cell. Screenshot the answers as a fallback.

---

## Golden rules

- **Scenario before data.** Always.
- **The signal must be macro-visible.** Weekly `GROUP BY`, obvious to the naked eye.
- **Fixed seed.** Everyone gets your numbers.
- **Few tables exposed, explicit names** (`fact_sales`, never `t1`).
- **Example queries beat long instructions** for SQL quality.
- **Zero real data, zero PII.**
- **Pause the capacity when you are done.** An F-SKU bills by the hour, used or not.

## Common failures

| Symptom | Real cause | Fix |
|---|---|---|
| Agent answers vaguely or picks the wrong table | Missing table/column descriptions | Describe everything |
| Correct SQL, boring answer | Uniform random data | Plant the storyline |
| Agent contradicts itself across runs | Ambiguous metric definition | Pin it in the instructions |
| Nothing works downstream | Data agent saved but not published | Publish it |

## Sources

- [Create a Fabric data agent](https://learn.microsoft.com/fabric/data-science/how-to-create-data-agent)
- [Fabric data agent end-to-end tutorial](https://learn.microsoft.com/fabric/data-science/data-agent-end-to-end-tutorial)
- [Fabric data agent source control and ALM](https://learn.microsoft.com/fabric/data-science/data-agent-source-control)
- [Use the Microsoft Fabric data agent in Foundry Agent Service](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric)
