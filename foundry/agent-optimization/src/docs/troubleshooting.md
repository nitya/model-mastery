# Troubleshooting

| Symptom | Check | Safe response |
| --- | --- | --- |
| Preflight cannot match a model | Exact case-sensitive catalog name, version, format, SKU, region | Update private `.env`; use visual fallback only after its own checks |
| Quota/deployment failure | Model+SKU usage in deployment region | Reduce reviewed capacity, free quota, choose verified region, or request quota |
| Partner offer error | Marketplace terms and purchaser role | Instructor accepts terms through approved process; do not bypass |
| `AI_PROJECT_DEPLOYMENTS` parse error | Whether it was manually set | Remove the manual value; let `azure.ai.project` marshal deployments |
| Agent returns model 404 | Stable deployment names and azd env overrides | Align agent env vars with literal deployment aliases |
| `project_not_found` | Current directory | Run azd commands from the workshop `src` folder |
| Python build fails | Python 3.13 support and service requirements | Run local import/syntax checks; preserve direct code configuration |
| Hosted agent unavailable | Region and account/project support | Use an instructor-verified hosted-agent region |
| No traces | App Insights connection and sampling | Verify project connection; send one test; avoid logging sensitive content |
| Eval config invalid | Agent version, local paths, evaluator registration | Stage `data/eval.yaml` at project root and verify all references |
| Optimizer rejects model | Optimizer allowlist and existing deployment | Use verified `campaign-reasoning` only if its backing model is eligible |
| Router preview proposes replacement | Expected for stable alias remap | Review impact; apply only after typing `SWITCH` |
| `PublicNetworkAccessDisabled`/403 | Account networking and caller location | Use an approved VNet connection method; do not weaken network controls |

Useful non-destructive commands:

```bash
azd ai project show --output json
azd ai agent show --output json
azd ai agent doctor --output json
azd provision --preview --no-prompt
./scripts/switch-router.sh --env-file ../.env --offline
```

Do not rerun `azd ai agent init` against this configured service: collision
handling can create a suffixed duplicate. Edit `azure.yaml` deliberately and
preview provisioning instead.

References:

- [Troubleshoot hosted agents](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/troubleshoot-hosted-agents)
- [Azure deployment what-if](https://learn.microsoft.com/azure/azure-resource-manager/templates/deploy-what-if)
- [Private Link connectivity](https://learn.microsoft.com/azure/foundry/how-to/configure-private-link#choose-a-secure-connection-method-to-foundry)
- [Azure role-based access control](https://learn.microsoft.com/azure/role-based-access-control/overview)
