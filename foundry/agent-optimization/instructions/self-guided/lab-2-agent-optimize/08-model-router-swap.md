# 08 · Swap in Model Router

⏱️ **Time:** 5 minutes

## 🎯 Goal

Change **which model** writes the copy without changing the agent, the deployment name, the dataset, or the rubric — then find out whether it actually helped.

## Objectives

- Switch the model behind the existing `adaptive-copy` deployment from fixed
  GPT-5.4-mini to Model Router.
- Confirm that no new agent version was created.
- Compare router behaviour on deliberately mixed-complexity cases.
- Treat routing as a hypothesis to measure, never as a promised improvement.

## ✅ Prerequisites

- [Module 07](./07-baseline-evaluation.md) complete: a recorded baseline.
- Your instructor confirmed **Model Router is available in your region** and populated `MODEL_ROUTER_MODEL_*` in `.env`.
- Terminal at `$WORKSHOP_SRC`.

<br/>

## 🧠 What Model Router is (30 seconds)

Model Router is a deployment that chooses a model **per request** instead of you choosing once, at design time. In hill-climbing terms it is not a step up the same slope — it is a **different route**, and routes can be worse. It is in preview; see [Model Router concepts](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/model-router).

> ⚠️ **No promises.** Routing may lower cost, raise it, or change nothing for this workload; it may also change quality in either direction. This module exists so you can tell which, not so you can assume.

<br/>

## 🔢 Steps

### Step 1 — See the change before you make it (1 min)

```bash
cd "$WORKSHOP_SRC"
./scripts/switch-router.sh --env-file ../.env --offline
```

This prints the current intent and the new intent for the **same deployment name**, and touches nothing:

```text
Deployment: adaptive-copy
Current intent: OpenAI/gpt-5.4-mini/<version>
New intent:     OpenAI/model-router/<version>
```

Only the model behind `adaptive-copy` changes. The name the agent calls does not.

### Step 2 — Azure what-if (1 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill ./scripts/switch-router.sh --env-file ../.env --preview
```

Read the what-if: exactly one deployment should be modified. Nothing else in the project moves.

### Step 3 — Apply (2 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill ./scripts/switch-router.sh --env-file ../.env --apply
```

Type `SWITCH` when prompted. Then confirm the model layer changed and the agent did not:

```bash
cd "$WORKSHOP_SRC"
az cognitiveservices account deployment list \
  --name "$(AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_AI_ACCOUNT_NAME)" \
  --resource-group "$(AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_RESOURCE_GROUP)" \
  --query "[?name=='adaptive-copy'].{deployment:name, model:properties.model.name, version:properties.model.version}" \
  --output table

AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-values | grep -E '^AGENT_.*VERSION'
```

**The agent version is unchanged.** You changed production behaviour with a configuration change, not a code deployment — no rebuild, no new version, no redeploy.

### Step 4 — Probe with mixed complexity (1 min)

```bash
cd "$WORKSHOP_SRC"
cat data/router-complexity-cases.jsonl

AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent invoke --new-session \
  "Write one social post for the HikeMate TrailLite Daypack. Cite the brief line behind every product-record/manual claim."

AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent invoke \
  "Write a launch narrative that distinguishes the TrailLite Daypack's water resistance from waterproofing, flags unsupported capacity and lifetime-durability claims, and proposes compliant alternatives."
```

One easy request, one hard one. Then look at the traces from [Module 06](../lab-1-model-explore/06-observe-the-agent.md): the model attribute on the `adaptive-copy` spans is where routing becomes visible.

### Step 5 — Re-measure, or use the reference (queue it now)

The honest comparison is the **same** evaluation on the **same** dataset and rubric:

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent eval run
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent eval show -O router-results.json
```

That run takes longer than this module’s budget. **Start it now and continue to
[Module 09](./09-agent-optimizer.md).** We’ll read the numbers in
[Module 10](./10-wrap-up.md).

**Reference comparison** — the shape of a router result, from a prior instructor run. Not a prediction, and not a target:

| Metric | Baseline (GPT-5.4-mini) | Router (reference) | Reading |
|---|---|---|---|
| Claim support | 0.72 | 0.74 | Within noise on a small set — not a win you can bank |
| Task adherence | 0.88 | 0.90 | Slightly better on the harder cases |
| p50 latency | lower | higher | Routing adds a selection step |
| Model mix | one model | several | Visible in the trace attributes |

The decision rule that matters: **an efficiency change only counts if quality holds.** If claim support drops, the router loses, no matter what it does to cost.

<br/>

## 📤 Expected result

- `adaptive-copy` now resolves to the Model Router entry; the other four deployments are untouched.
- `AGENT_..._VERSION` is identical to
  [Module 05](../lab-1-model-explore/05-deploy-and-version.md).
- Two invocations succeeded with no code change whatsoever.
- A re-evaluation is running (or queued) against the frozen dataset and rubric.

## 🏆 Quick win

Put the deployment table from
[Module 01](../lab-0-setup/01-provision-environment.md) next to the one from
Step 3. One row changed. No redeploy, new version, or code diff—and the agent
now uses a different model-selection strategy. That is the value of naming
deployments after jobs.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** `adaptive-copy` points at Model Router **and** the agent version is unchanged.

| If… | Do this |
|---|---|
| Model Router is unavailable in your region | Stop at Step 2 (`--preview`) and use the reference comparison table. The lesson — config-level change, same deployment name — is fully intact. |
| You are over budget | Skip Step 4 and go to [Module 09](./09-agent-optimizer.md); the eval from Step 5 keeps running. |
| Quality drops and you want to revert | Use the [Module 10 revert recipe](./10-wrap-up.md): reset the four `ADAPTIVE_COPY_MODEL_*` values and re-provision. |
| The swap fails midway | Re-run `--apply`; provisioning is idempotent. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `[ACTION] Set MODEL_ROUTER_MODEL_VERSION.` | Router version blank in `.env` | Paste the instructor-verified version. |
| Deployment fails: model not found | Model Router unavailable in that region, or the identifier changed | `az cognitiveservices model list --location <region> --output table`. |
| Insufficient quota | Router SKU quota is separate | Lower capacity, or use a region with quota. |
| Invocations now fail with 404 | Provisioning did not finish | Re-run `--apply`, then confirm with the deployment list query in Step 3. |
| Latency jumped a lot | Expected on some routes | Record it. Latency is part of the decision, not a bug to hide. |

## ➡️ Next

You changed the model. Now change the *instructions* — and let the platform propose the wording.

**[Module 09 — Agent Optimizer](./09-agent-optimizer.md)** · ⬆️ [Lab 2](./README.md)
