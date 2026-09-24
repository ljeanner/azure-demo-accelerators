# Fabric + Foundry Terraform baseline

**Goal:** provision, in one `terraform apply`, everything a Fabric + AI Foundry demo needs —
a Fabric capacity, an AI Foundry account and project with model deployments, Azure AI Search
(wired to the project), Cosmos DB, storage, Application Insights, and the **~25 role assignments**
that make agents actually work.

**Setup time:** ~20 min · **Prerequisites:** Azure CLI (`az login`), Terraform ≥ 1.9, and
**Owner + User Access Administrator** on the target subscription or resource group
(role assignments and Cosmos SQL data-plane roles are created).

> ### Credit
> The Terraform in [`infra/`](infra/) and the OneLake seeding scripts in [`seed/`](seed/) are
> adapted from the **FabCon 2026 workshop by [Damien Aicheh](https://github.com/damienaicheh)**,
> shared here with his permission. Demo-specific pieces (Azure Functions apps, Office 365 connector
> namespace, Communication Services, Document Intelligence) were removed so what remains is a
> reusable Fabric + Foundry baseline.

---

## What gets deployed

| File | Resource | Why it matters |
|---|---|---|
| `fabric.tf` | `azurerm_fabric_capacity` (F2 by default) | The signed-in deployer is set as capacity admin, so you can create a workspace immediately. **F2 is the minimum for Fabric data agents.** |
| `fabric_workspace.tf` | `fabric_workspace` + `fabric_lakehouse` (`microsoft/fabric` provider) | Creates the workspace bound to the capacity and an empty lakehouse, and grants the AI Search identity **Contributor** on the workspace. Toggle with `create_fabric_workspace`. |
| `ms_foundry.tf` | Foundry account (`azapi`, `Microsoft.CognitiveServices/accounts@2025-06-01`) | `allowProjectManagement = true` + `customSubDomainName` + user-assigned identity. The `azurerm` provider does not cover these yet — hence `azapi`. |
| `ms_foundry_project.tf` | Foundry project | Exports `properties.internalId`, recomposed into a GUID in `locals.tf`. That GUID is what scopes the Cosmos and Storage role assignments. |
| `ms_foundry_models.tf` | Model deployments | Chat + embedding, `GlobalStandard` SKU, explicit capacity, `Microsoft.DefaultV2` RAI policy. Parameterized through `var.chat_model` / `var.embedding_model`. |
| `ai_search.tf` | AI Search + project connection | Semantic search enabled, system-assigned identity, and a `CognitiveSearch` connection on the project with `authType = "AAD"`. |
| `cosmos_db.tf`, `sto.tf`, `aai.tf`, `log.tf` | Cosmos DB, Storage, App Insights, Log Analytics | The "bring your own storage" backing stores for Foundry agent threads, plus project connections for each. |
| `roles.tf` | ~25 role assignments | The part everyone gets wrong. See below. |
| `locals.tf`, `randomize.tf`, `rg.tf`, `data.tf` | Naming + RG | Convention `env-region-domain-workload-hash`, and `coalesce` so you can reuse an existing RG or create one. |

### Why `roles.tf` is the real value

- **Cosmos SQL data-plane roles** on `enterprise_memory/<project-guid>-thread-message-store`,
  `-system-thread-message-store` and `-agent-entity-store`. These are created *after* the project
  exists and are chained with `depends_on` because Cosmos rejects parallel role writes.
- **ABAC condition on `Storage Blob Data Owner`**, restricting the identity to containers named
  `<project-guid>*-azureml-agent` instead of granting the whole account.
- Separate grants for the **user-assigned identity**, the **AI Search system identity**, and the
  **Terraform caller** (so `terraform apply` then a local script both work).

---

## Deploy

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # edit it
terraform init
terraform apply
```

Useful outputs:

```bash
terraform output -raw fabric_capacity_name                  # attach your Fabric workspace to it
terraform output -raw fabric_workspace_id                   # FABRIC_WORKSPACE_ID for the seed scripts
terraform output -raw fabric_lakehouse_id                   # FABRIC_LAKEHOUSE_ID for the seed scripts
terraform output -raw project_endpoint                      # Foundry project endpoint
terraform output -raw search_service_endpoint
terraform output -raw search_system_identity_principal_id   # grant it access to the Fabric workspace
```

### About the Fabric workspace

The workspace and lakehouse are created with the [`microsoft/fabric`](https://registry.terraform.io/providers/microsoft/fabric/latest/docs)
provider, which talks to the Fabric REST API and authenticates with your `az login` session.

Two things to know:

- The provider needs the **capacity GUID**, not the ARM resource ID — hence the
  `data "fabric_capacity"` lookup that resolves it from the capacity name.
- If your tenant blocks Fabric API access (the *"Service principals can use Fabric APIs"*
  tenant setting, or a conditional-access policy), set `create_fabric_workspace = false`
  and create the workspace by hand in the Fabric portal. Everything else still applies.

---

## Keep the cost under control

**A running F-SKU capacity bills by the hour, used or not.** F2 is roughly a couple of
euros a day, but an F64 left running over a weekend is a bad surprise. Pause it as soon as
the demo is over:

```bash
./scripts/capacity.sh pause     # or: resume / status
```

```powershell
.\scripts\capacity.ps1 pause    # or: resume / status
```

The scripts read the capacity name and resource group from the Terraform outputs and call
`az fabric capacity suspend|resume`, installing the `microsoft-fabric` CLI extension on first
use. While paused, Fabric content on that capacity is unavailable — resume a few minutes
before you present.

> For a hackathon: pause at the end of each day, resume in the morning.
> Full teardown is `terraform destroy`.

### Teardown

```bash
terraform destroy
```

---

## Optional: index OneLake into AI Search (`seed/ai-search-onelake/`)

Turns a Fabric lakehouse into a vector index and a **Foundry IQ knowledge base**, without copying data.

1. The AI Search managed identity already has **Contributor** on the workspace if you
   deployed with `create_fabric_workspace = true`. Otherwise, add
   `search_system_identity_principal_id` as Contributor on the workspace by hand.
2. `cp .env.template .env` and fill in `FABRIC_WORKSPACE_ID` / `FABRIC_LAKEHOUSE_ID`
   (both GUIDs come straight from the lakehouse URL).
3. Run:

```bash
uv run python main_create_index.py     # data source + skillset + index + indexer
uv run python main_knowledge_base.py   # knowledge source + Foundry IQ knowledge base
```

What the JSON templates do:

- `onelake-datasource.json` — `"type": "onelake"`, `connectionString = ResourceId=<workspace-guid>`,
  container = lakehouse GUID. **No data copy, no key.**
- `onelake-skillset.json` — `SplitSkill` (2000 chars, 500 overlap) then `AzureOpenAIEmbeddingSkill`,
  projected chunk-per-document via `indexProjections`.
- `onelake-index.json` — HNSW / cosine vector field, integrated vectorizer, semantic configuration.
- `onelake-indexer.json` — incremental by default; set `RESET_INDEXER=true` to reprocess everything.

---

## Golden rules

- **Fabric capacity costs money while it runs.** Pause it between demos with
  `scripts/capacity.sh pause`, or `terraform destroy`.
- **`Owner` is not enough**: you also need **User Access Administrator** to create role assignments.
- The **Cosmos SQL role assignments must run after** the project exists — keep the `depends_on` chain.
- Model **capacity (TPM) is regional**; if `apply` fails on a deployment, lower `capacity` or change region.
- `purge_soft_delete_on_destroy` is enabled on Cognitive Services, so a destroyed Foundry account
  frees its name immediately. Do not enable that in production.

## Sources

- [Terraform `azurerm_fabric_capacity`](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/fabric_capacity)
- [Terraform `microsoft/fabric` provider](https://registry.terraform.io/providers/microsoft/fabric/latest/docs)
- [Pause and resume your capacity](https://learn.microsoft.com/fabric/enterprise/pause-resume)
- [What is Microsoft Fabric capacity?](https://learn.microsoft.com/fabric/enterprise/licenses)
- [Azure AI Foundry — role-based access control](https://learn.microsoft.com/azure/ai-foundry/concepts/rbac-azure-ai-foundry)
- [Index data from OneLake files (Azure AI Search)](https://learn.microsoft.com/azure/search/search-how-to-index-onelake-files)
- [Create a Fabric data agent](https://learn.microsoft.com/fabric/data-science/how-to-create-data-agent)
