# Evaluation and optimization notes

## Artifacts

- `data/eval-cases.jsonl`: seven reviewed `{query, expected_behavior}` rows,
  directly usable as `inputData` in current agent-target batch evaluation.
- `data/evaluators/campaign-quality.yaml`: current custom evaluator
  `name`/`promptText` shape. Foundry appends the final result schema.
- `data/eval.yaml`: current Agent Optimizer intent using `dataset.local_uri`,
  evaluator entries, and optimization model search space.
- `checkpoints/`: reviewable offline baseline/candidate with no fabricated
  measurements.

## Live sequence

Copy `data/eval.yaml` to `agents/product-launch-studio/eval.yaml` only for the
exercise; its `../../data/` references resolve from that agent root. Confirm
`agent.version` matches the deployed immutable version. Confirm the evaluator
exists in the target project's evaluator catalog, registering it if needed.

```bash
azd ai agent eval generate --dataset data/eval-cases.jsonl
azd ai agent eval run
azd ai agent optimize --optimize-model campaign-reasoning
azd ai agent optimize status <operation-id> --watch
```

Before applying, compare candidate behavior on all seven cases and inspect
model, temperature, instructions, tools, and skills. Apply locally:

```bash
azd ai agent optimize apply --candidate <candidate-id>
```

Review changes before `azd deploy`; never use optimizer direct-deploy in this
lab. Dataset rows and evaluator thresholds must remain fixed when comparing
runs. Create a new evaluation group if the evaluator bundle changes.

## Offline fallback

If optimization is unavailable or slow, compare
`checkpoints/00-baseline` and `checkpoints/01-evidence-optimized`, then run local
tests manually. These checkpoints teach review mechanics only. Their null
scores must stay null until replaced by real, attributable results.

References:

- [Cloud evaluation](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/cloud-evaluation)
- [Built-in evaluators](https://learn.microsoft.com/azure/foundry/concepts/built-in-evaluators)
- [Observability and evaluation](https://learn.microsoft.com/azure/ai-foundry/concepts/observability)
