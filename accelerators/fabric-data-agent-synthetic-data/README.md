# Synthetic data → Fabric Lakehouse → Fabric Data Agent

**Goal:** in a few hours, produce a credible synthetic dataset and a **Fabric Data Agent** that answers
business questions in natural language, with a scenario that carries the sales narrative.

**Setup time:** 2-3 h · **Prerequisites:** Fabric capacity **F2 or higher**, rights to create items in a Fabric workspace.

> This is the method behind the **Zava Retail** demo (a fictional sporting-goods retailer).
> Paste the prompt below into Copilot / Claude / a Fabric notebook, fill in the `<< ... >>` blocks,
> and let the assistant produce the notebook.

> **In a hurry?** Skip the prompt and start from the working notebook:
> [`notebook/synthetic_data_to_lakehouse.ipynb`](notebook/synthetic_data_to_lakehouse.ipynb).
> Edit the parameters cell, run all, done — see [section 0](#0-shortcut-the-reference-notebook).

---

## 0. Shortcut: the reference notebook

[`notebook/synthetic_data_to_lakehouse.ipynb`](notebook/synthetic_data_to_lakehouse.ipynb) is a
complete, parameterised, **runnable** version of what the prompt is supposed to produce. Use it as
a starting point, or as the reference the assistant should imitate.

1. Attach it to a lakehouse in your Fabric workspace.
2. Edit the **Parameters** cell (volumes, dates, seed, table prefix).
3. Run all — about a minute for 200k transactions.

It produces four tables — `stores`, `products`, `customers`, `transactions` — and ships with:

- **built-in structure**: yearly seasonality, weekday profile, growth trend, per-store multiplier,
  Pareto product popularity. Never a flat line.
- **a planted storyline**: one store collapsing from a given date, one category doubling, a batch of
  negative-margin transactions. Three demo questions with a real answer.
- **validation before writing**: null checks, referential integrity, unique keys, date window.
- **a Spark/pandas switch**: writes Delta in Fabric, CSV on your laptop, so you can test it
  before you touch a capacity.
- **a verification section** printing the exact aggregates you will ask the agent for.

To move to your own domain, replace section 2 (reference data) and section 4 (storyline). The rest
is domain-agnostic.

---

## 1. The prompt (copy-paste)

```
You are a data engineer. Produce a PySpark notebook, runnable in a Microsoft Fabric notebook with an
attached Lakehouse, that generates a SYNTHETIC but REALISTIC and CONSISTENT dataset and writes it as
Delta tables to the Lakehouse. This data will be used to demo a Fabric Data Agent
(natural language questions -> SQL) to decision makers.

### BUSINESS CONTEXT (fill in)
- Fictional company      : << name, industry, country/HQ, founding year >>
- Scale to convey        : << revenue, number of stores/sites, number of customers, number of countries >>
- Brands / product lines : << ... >>
- Domains to cover       : << sales, inventory, procurement, production, margins, forecasting, competition, HR... >>
- Data period            : << start_date >> -> << end_date >>
- Currency / language    : << EUR, labels in EN or FR >>

### DEMO SCENARIO (the most important part)
The data must contain an ACTIONABLE SIGNAL that the agent can detect and explain:
- Trigger event        : << e.g. a competitor launches -30% on one category for 3 weeks >>
- Event window         : << event_start_date >> -> << event_end_date >>
- Expected effect in the data : << volume/average-price drop on category X, stock pressure on SKUs Y,
  margin falling below threshold Z >>
- Questions the demo must be able to answer (5 to 10):
  1. << e.g. How have category X sales evolved over the last 8 weeks? >>
  2. << e.g. Which products are below the 35% margin floor? >>
  3. << ... >>

### DATA REQUIREMENTS
1. Star schema: `dim_*` (reference) and `fact_*` (transactional) tables, valid foreign keys, no orphan rows.
2. `SEED = 42` with seeds fixed (random + numpy) so every colleague gets identical data.
3. Realism is mandatory:
   - monthly seasonality per category, weekend effect, yearly trend;
   - prices consistent with costs (plausible margin, price history with a few changes);
   - calendar promotions, multiple channels (store / e-commerce);
   - some noise and a few missing values, but NEVER an inconsistency (no negative quantities,
     no dates outside the period, no discount > 100%).
4. The demo scenario must be VISIBLE in aggregate: grouping by week/category, the gap must jump out.
5. Volume: aim for a few hundred thousand to a few million fact rows
   (parameters at the top of the notebook: NUM_SITES, NUM_PRODUCTS, NUM_CUSTOMERS, AVG_DAILY_TRANSACTIONS...).
6. NO real data, no real customer/supplier/competitor names, no real PII.

### EXPECTED NOTEBOOK STRUCTURE
- Cell 0: a `# Configuration` block with every constant (seed, dates, volumes, scenario window).
- Section 1: dimensions (products, sites, customers, suppliers, competitors).
- Section 2: pricing & promotions (price history, promo calendar).
- Sections 3..N: facts (sales, inventory, purchase orders, production, margins, forecasts, competitor activity).
- "Write to Lakehouse" section: a `TABLES = {"dim_...": df, "fact_...": df}` dict, then for each table
  `df.write.format("delta").mode("overwrite").saveAsTable(table_name)` with a fallback to
  `.save(f"Tables/{name}")`, printing the row count written per table.
- "Validation" section: row counts, referential integrity checks, and 3 aggregate queries that
  PROVE the scenario signal is present.

### ADDITIONAL DELIVERABLES (beyond the notebook)
A. A **data dictionary** in markdown: for each table, its grain, its columns, their types and business meaning.
B. The **data agent instructions** (< 15,000 characters): role, description of each table, when to use which
   table, business rules (margin thresholds, definition of net revenue, fiscal vs calendar), answer tone,
   and the requirement to cite the numbers.
C. **10 example queries** as "natural language question -> validated SQL query" pairs, covering the demo questions.
D. A **demo script**: 5 questions asked to the agent, in order, with the expected answer.
```

---

## 2. After generation: set it up in Fabric

1. **Workspace + Lakehouse** — F2 capacity minimum; create the Lakehouse (`<Name>LH`).
2. **Notebook** — import the generated notebook, attach it to the Lakehouse, `Run all`.
   Check the Delta tables under `Tables/`.
3. **Data agent** — *New item → Data agent*, name it, then add the Lakehouse from the OneLake catalog
   (up to 5 sources: lakehouse, warehouse, Power BI semantic model, KQL database, ontology, Microsoft Graph).
   Select only the tables the demo needs (fewer tables = more accurate SQL).
4. **Instructions** — paste deliverable **B** into *Data agent instructions*.
5. **Example queries** — paste deliverable **C** into *Example queries* (not supported for Power BI semantic
   models; this is the #1 accuracy lever for lakehouse/warehouse/KQL sources).
6. **Test, then Publish** — replay script **D**, fix instructions/examples, then *Publish*.
   The published data agent can be consumed from Azure AI Foundry / Copilot Studio / M365 Copilot,
   or via the `fabric-data-agent-sdk`.
7. **Version it** — enable workspace Git integration: the `draft/` and `published/` folders hold the data agent
   config (`lakehouse-tables-*` folders), so colleagues can replay your setup.

---

## 3. Golden rules (what makes demos fail)

- **Scenario before data.** Write the 5 demo questions first, generate afterwards.
- **The signal must be macro-visible**, otherwise the agent won't "see" it.
- **Fixed seed**: everyone must get exactly the same numbers.
- **Expose few tables** to the agent, with explicit names (`fact_sales`, not `t1`).
- **Example queries beat long instructions** for SQL quality.
- **Zero real data / zero PII**, made-up competitor names.

## Sources

- [Create a Fabric data agent](https://learn.microsoft.com/fabric/data-science/how-to-create-data-agent)
- [Fabric data agent end-to-end tutorial](https://learn.microsoft.com/fabric/data-science/data-agent-end-to-end-tutorial)
- [Source control, CI/CD, and ALM for Fabric data agent](https://learn.microsoft.com/fabric/data-science/data-agent-source-control)
