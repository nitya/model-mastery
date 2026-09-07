# Instructor guide

## Before the session

Run checks in the same subscription and region students will use. Catalog
availability is not proof of quota, protocol support, or Marketplace acceptance.

1. Create the top-level private `../.env` from `../sample.env`.
2. Use the live catalog to record exact model names, versions, formats, and SKUs.
3. From the `src` azd project root, run `scripts/preflight.sh --env-file ../.env --online`.
4. Confirm quota for each deployment and expected workshop concurrency.
5. Confirm direct code hosted agents and Python 3.13 are enabled in the region.
6. Confirm the `agents/product-launch-studio` service starts locally.
7. Run Bicep build and an ARM what-if, but do not provision on students' behalf.
8. Decide the visual path:
   - primary: verified Claude Sonnet 6 offering and terms;
   - fallback: verified GPT-5.4 mapping.
9. Decide whether the live Agent Optimizer can finish within the allotted time.
   Keep `checkpoints/` ready as the transparent offline fallback.

## Timing and decision gates

| Minute | Gate |
| --- | --- |
| 10 | Tools and authentication available |
| 25 | Exact catalog entries, quota, terms, and region verified |
| 40 | What-if reviewed before provisioning |
| 55 | One local and one remote smoke test maximum |
| 67 | Router what-if reviewed before remap |
| 78 | Eval run started; operation IDs recorded |
| 85 | Live candidate or prepared checkpoint selected for review |
| 90 | Cleanup ownership confirmed |

## Cost controls

- Use the smallest instructor-verified capacity that supports the cohort.
- Five deployments can reserve quota even while idle; image generation and
  optimizer/evaluator calls consume additional usage.
- Keep remote smoke tests to one request.
- Stop duplicate optimizer jobs.
- Delete student environments at the end unless retention is explicitly needed.

## Evidence and safety debrief

Ask learners to locate:

- a valid numerical claim, such as dimensions or weight;
- an unsupported claim that the agent corrected;
- a visual inference the agent refused to make;
- the $60 catalog price kept separate from visual observations;
- a router choice whose cost/latency trade-off they can explain.

The product record, manual, and image come from the MIT-licensed
`Azure-Samples/contoso-web` sample at the commit recorded in
`assets/PROVENANCE.md`; the campaign output remains a workshop exercise. Do not
introduce real customer data.

## Prepared checkpoint policy

`checkpoints/optimizer-result.sample.json` is a simulation, not a service
result. Never fill its null scores with invented values. If using it, compare
files locally and label the exercise “offline candidate review.” Live results
must retain their actual operation ID, candidate ID, and evaluator output.

Official links:

- [Model deployment availability](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/deploy-foundry-models)
- [Quota management](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/quota)
- [Evaluate agents](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/cloud-evaluation)
- [Agent Optimizer](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/agent-optimizer)
