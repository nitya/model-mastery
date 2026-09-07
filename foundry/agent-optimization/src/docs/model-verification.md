# Model and region verification

Model names in this workshop express intent, not a guarantee that those exact
catalog identifiers exist in every cloud, subscription, date, or region.
Versions are intentionally blank in the top-level `../sample.env`.

## Required evidence

For every model record:

1. Exact catalog `name`, `version`, and `format`.
2. Supported deployment SKU.
3. Available regional quota after existing allocations.
4. API/protocol support needed by the agent.
5. Offer terms and subscription permission for partner/community models.
6. Hosted-agent availability in the project region.

Run:

```bash
./scripts/preflight.sh --env-file ../.env --online
```

The script uses read-only catalog and usage queries. It rejects approximate
name/version matches. Capacity shown in `azure.yaml` is merely a workshop
starting point; change it only after quota review.

## Visual choice

Prefer the instructor-verified Claude Sonnet 6 entry. If it is absent,
unsupported, or blocked by offer terms, replace all four
`VISUAL_UNDERSTANDING_MODEL_*` values with the verified GPT-5.4 fallback
values. Do not mix one model's format or SKU with the other's version.

## Router choice

Verify the catalog entry configured by `MODEL_ROUTER_MODEL_*` before running
the switch helper. Model Router availability, eligible underlying models,
pricing, and region coverage can differ from fixed deployments. The three
examples in `data/router-complexity-cases.jsonl` test intended complexity
classes; they do not promise a specific internal model.

References:

- [Deploy Foundry models](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/deploy-foundry-models)
- [Model Router](https://learn.microsoft.com/azure/foundry/openai/concepts/model-router)
- [Deployment types](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/deployment-types)
- [Quotas and limits](https://learn.microsoft.com/azure/ai-foundry/openai/quotas-limits)
- [Partner model permissions](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-from-partners#permissions-required-to-subscribe-to-models-from-partners-and-community)
