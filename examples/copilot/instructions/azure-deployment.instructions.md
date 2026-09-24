---
applyTo: "**/*.bicep,**/*.bicepparam,**/*.tf,**/*.tfvars,**/azure.yaml,**/infra/**,**/deploy/**"
---

# Our Azure environment

Adapt `applyTo` to the project's deployment files.

- Team environment: << subscription and resource group, no secrets >>
- Region: << region >>
- Budget and lifetime: << indicative amount and cleanup date >>
- Deployment tool: << existing tool or manual steps >>

Reuse the prepared environment. Check the target, access, and prerequisites;
Azure access does not guarantee Fabric or M365 access.
Do not store secrets, sensitive plans, or Terraform state in the repository.
Present the changes and estimated costs before asking for deployment confirmation.
Also obtain confirmation for permission changes, public exposure, and deletions.
Do not delete shared resources. Verify functionality after deployment.
