# From Model Selection To Agent Optimization with Microsoft Foundry

Self-guided 90-minute Linux Codespaces/Dev Container lab. Azure provisioning and
model inference can incur charges. Nothing in this folder provisions resources
until a participant explicitly runs an `--apply` path.

## Outcomes

You will verify model availability, preview infrastructure, deploy a hosted
Responses agent, compare purpose-fit model choices, switch one stable deployment
name to Model Router, run an evaluation, and review an optimization candidate.

## 0–10 minutes: prepare

1. Set `WORKSHOP_ROOT` to the parent of this `src` directory and
   `WORKSHOP_SRC="$WORKSHOP_ROOT/src"`, then open a terminal at `$WORKSHOP_SRC`.
   Every script resolves its own location.
2. Confirm `az`, `azd`, Python 3, and the `azure.ai.agents` azd extension.
3. Authenticate manually:
   `az login` and `azd auth login`.
4. Copy `sample.env` to an ignored file outside source control, fill the
   subscription, region, and every exact model version:

   ```bash
   cp ../sample.env ../.env
   ./scripts/preflight.sh --env-file ../.env
   ```

Never put API keys, access tokens, connection strings, or passwords in `.env`.
This lab uses `DefaultAzureCredential` and managed identities.

## 10–25 minutes: verify before spending

Run the online, read-only check:

```bash
./scripts/preflight.sh --env-file ../.env --online
```

The instructor must verify:

- each exact name/version/format/SKU exists in the chosen deployment region;
- quota covers all five capacities in `azure.yaml`;
- hosted-agent support is available in the project region;
- the subscription may accept any required partner Marketplace offer;
- Claude Sonnet 6 is available, or the documented GPT-5.4 visual fallback is
  selected in `.env`.

Preview the local azd state, then apply it:

```bash
./scripts/configure-environment.sh --env-file ../.env
./scripts/configure-environment.sh --env-file ../.env --apply
```

## 25–40 minutes: inspect and provision

Read [architecture.md](architecture.md), then inspect `azure.yaml` and
`infra/main.bicep`. Five stable deployment names isolate application code from
catalog model names.

```bash
./scripts/provision.sh --env-file ../.env
./scripts/provision.sh --env-file ../.env --apply
```

The first command is an ARM what-if. The second requires typing `PROVISION`.
Provisioning should create a Foundry account/project, five model deployments,
Log Analytics, workspace-based Application Insights, an App Insights project
connection, and project RBAC.

Verify with:

```bash
azd env get-values
azd ai project show --output json
```

## 40–55 minutes: run the hosted agent

The `product-launch-studio` service uses direct code deployment:
Python 3.13, `main.py`, remote dependency resolution, and Responses protocol.

```bash
azd ai agent run --no-client
```

In a second terminal:

```bash
azd ai agent invoke --local \
  "Write a hero for TrailPack using only claims in the campaign brief."
```

When the local invocation succeeds, review the deployment, then run:

```bash
azd deploy product-launch-studio --no-prompt
azd ai agent show --output json
azd ai agent invoke "Give me one evidence-safe TrailPack slogan."
```

Remote calls incur usage. One smoke test is sufficient.

## 55–67 minutes: model selection and routing

Review `data/router-complexity-cases.jsonl`. First observe the fixed
`adaptive-copy` deployment (GPT-5.4-mini). Then preview a remap to Model Router:

```bash
./scripts/switch-router.sh --env-file ../.env --offline
./scripts/switch-router.sh --env-file ../.env
```

Only after reviewing what-if:

```bash
./scripts/switch-router.sh --env-file ../.env --apply
```

The deployment name remains `adaptive-copy`; application configuration does not
change. The model backing that deployment changes to the instructor-verified
Model Router catalog entry.

## 67–85 minutes: evaluate and optimize

From this folder, stage optimizer inputs where the azd extension expects them:

```bash
cp data/eval.yaml agents/product-launch-studio/eval.yaml
```

Register or verify the `campaign_quality` evaluator before treating it as a
remote evaluator. The YAML at `data/evaluators/campaign-quality.yaml` uses the
current `name`/`promptText` contract and intentionally leaves result-schema
enforcement to Foundry.

Run:

```bash
azd ai agent eval generate --dataset data/eval-cases.jsonl
azd ai agent eval run
azd ai agent optimize --optimize-model campaign-reasoning
```

Record the real operation ID, then:

```bash
azd ai agent optimize status <operation-id> --watch
azd ai agent optimize apply --candidate <candidate-id>
```

Do not invent IDs, apply a candidate without reviewing it, or deploy directly
from the optimizer. If the job is still running, use `checkpoints/` for the
offline comparison exercise; those artifacts are clearly unmeasured.

## 85–90 minutes: reflect and clean up

Compare:

- quality versus latency and cost;
- fixed-model predictability versus router adaptability;
- built-in evaluator breadth versus the campaign-specific rubric;
- baseline and candidate instruction specificity.

Restore or remove the copied agent-root `eval.yaml` if it was only workshop scratch. Preview
cleanup and then explicitly apply it:

```bash
./scripts/cleanup.sh
./scripts/cleanup.sh --apply
```

See [cleanup.md](cleanup.md) before deletion.
