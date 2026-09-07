# Infrastructure

`main.bicep` creates one resource group, Foundry account/project, workspace-based
Application Insights, Log Analytics, project RBAC, and the model deployments
marshalled by the `azure.ai.project` service in `azure.yaml`.

Direct code deployment uses Foundry Basic Agent Setup, so
`ENABLE_HOSTED_AGENTS=true`, `ENABLE_CAPABILITY_HOST=false`, and
`AZD_AGENT_SKIP_ACR=true` are intentional. Set capability host to `true` only
for a reviewed Standard Agent Setup design with bring-your-own storage.

Model catalog identifiers, versions, deployment SKU, quota, Marketplace terms,
and region support change independently. From the parent `src` azd project root,
run `scripts/preflight.sh --env-file ../.env --online` and populate the private
environment before any preview or deployment.

Official references:

- [Create a Foundry project](https://learn.microsoft.com/azure/foundry/how-to/create-projects)
- [Hosted agents](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)
- [Bicep deployments](https://learn.microsoft.com/azure/azure-resource-manager/bicep/deploy-cli)
- [Application Insights workspace resources](https://learn.microsoft.com/azure/azure-monitor/app/create-workspace-resource)
