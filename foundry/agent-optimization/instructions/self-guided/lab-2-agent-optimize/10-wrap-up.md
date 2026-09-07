# 10 · Wrap-up and next steps

⏱️ **Time:** 5 minutes

## 🎯 Goal

Turn three experiments into one defensible decision, leave your subscription clean, and know exactly what to do differently at work on Monday.

## Objectives

- Compare baseline, router, and optimizer candidates on one sheet.
- Apply a promote / revert rule you can explain to a stakeholder.
- Revert the router or delete the environment.
- Identify the next hill worth climbing.

## ✅ Prerequisites

- [Module 07](./07-baseline-evaluation.md) baseline recorded.
- [Module 08](./08-model-router-swap.md) and [Module 09](./09-agent-optimizer.md) attempted (results may still be running).

<br/>

## 🔢 Steps

### Step 1 — Collect the numbers (1 min)

```bash
cd "$WORKSHOP_SRC"
ls -1 *results*.json 2>/dev/null
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent eval list
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent optimize list
```

Fill one sheet. Anything still running gets "pending" — that is a legitimate entry, not a gap.

| Arm | What changed | Claim support | Task adherence | Latency | New agent version? |
|---|---|---|---|---|---|
| Baseline | — | | | | n/a |
| Model Router | Model behind `adaptive-copy` | | | | **No** |
| Optimizer candidate | Copywriter instructions | | | | Yes, once deployed |

### Step 2 — Apply the decision rule (1 min)

```text
1. Did the quality constraint hold?      claim support must not regress
2. Did anything else regress?            adherence, latency, cost
3. Is the change small and reviewable?   can you explain the diff in one sentence?
4. Is the delta bigger than the noise?   if not, gather more cases before promoting
```

| Outcome | Decision |
|---|---|
| Quality held **and** efficiency improved | Promote |
| Quality held, efficiency unchanged | Keep the simpler configuration — do not add moving parts for nothing |
| Quality regressed | Revert, whatever else improved |
| Delta inside noise | Not a result. Expand the dataset, then re-measure. |

Two habits are worth more than any single number here: **you measured before you moved**, and **you changed one thing at a time**.

### Step 3 — Revert the router if it lost (1 min)

`switch-router.sh` only moves forward. To go back to fixed GPT-5.4-mini, reset the four values and re-provision:

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env set ADAPTIVE_COPY_MODEL_NAME gpt-5.4-mini
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env set ADAPTIVE_COPY_MODEL_VERSION "<the version from your .env>"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env set ADAPTIVE_COPY_MODEL_FORMAT OpenAI
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env set ADAPTIVE_COPY_MODEL_SKU GlobalStandard
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd provision --preview --no-prompt   # read it first
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd provision --no-prompt
```

Reverting a model choice is a configuration change. No redeploy, no new agent version — the same property you verified in Module 08.

### Step 4 — Clean up (2 min)

The workshop created **billable** resources. Delete them unless you are continuing.

```bash
cd "$WORKSHOP_SRC"
./scripts/cleanup.sh --preview          # lists what exists; deletes nothing
./scripts/cleanup.sh --apply            # type DELETE to confirm
```

Keeping the environment? Then at minimum note the resource group name and set yourself a reminder — idle model deployments still consume quota that your colleagues may need.

<br/>

## 📤 Expected result

- One completed comparison sheet, pending entries included.
- An explicit promote / revert decision with a stated reason.
- Either a reverted `adaptive-copy`, or a deleted resource group, or a deliberate decision to keep the environment.

## 🏆 Quick win

Say this sentence out loud, filling in your own values: *"On a frozen 5–8 case set with a claim-support rubric, moving `adaptive-copy` to Model Router changed claim support from **X** to **Y** and latency from **A** to **B**, so we **kept / reverted** it."* That sentence — specific, bounded, reproducible — is what a model-selection decision should sound like.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** you have made a decision *and* you know the state you left Azure in.

| If… | Do this |
|---|---|
| Runs are still pending | Record the operation IDs, decide later. `azd ai agent eval list` and `optimize list` will still find them. |
| You are unsure whether cleanup worked | `./scripts/cleanup.sh --preview` — an empty resource list means you are done. |
| You want to keep experimenting | Skip cleanup, but expand `data/eval-cases.jsonl` first — 5–8 cases is a smoke test, not a benchmark. |
| You broke something and want a fresh start | `./scripts/cleanup.sh --apply`, then restart at [Module 01](../lab-0-setup/01-provision-environment.md). |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `AZURE_RESOURCE_GROUP is not set` during cleanup | azd environment lost or not selected | `azd env list`, then `azd env select <name>`, and retry. |
| Cleanup leaves a soft-deleted account | Foundry accounts soft-delete by default | `cleanup.sh --apply` uses `azd down --purge`; if you deleted manually, purge the account explicitly. |
| Revert re-provision fails | A blank `ADAPTIVE_COPY_MODEL_VERSION` | Copy the version back from your `.env`. |
| Quota still shows as consumed | Deletion is asynchronous | Wait a few minutes and re-check with `az cognitiveservices usage list`. |

<br/>

## 🎓 What you can now do

| Skill | Where you practised it |
|---|---|
| Provision a Foundry project and a whole model layer from source | Module 01 |
| Choose models per role from evidence you generated yourself | Module 03 |
| Run, deploy, and version a hosted agent without Docker | Modules 04–05 |
| Read traces to attribute behaviour to a specific role and model | Module 06 |
| Baseline an agent on a frozen dataset and rubric | Module 07 |
| Change the model layer without touching the agent | Module 08 |
| Use Agent Optimizer as a reviewed proposal engine, not an autopilot | Module 09 |
| Turn results into a promote / revert decision | Module 10 |

## ➡️ Next · the next hill

1. **Grow the dataset.** 5–8 cases is a smoke test. Harvest real traces into evaluation cases and split them into smoke / regression tiers.
2. **Put the rubric in CI.** An evaluation that only runs when someone remembers is not a guardrail.
3. **Optimize a second role.** The product analyst has its own instructions and its own failure modes — starting with claim rule 7, where images get over-read.
4. **Add continuous evaluation** in production, so quality drift shows up as a signal instead of a customer complaint.
5. **Re-verify models quarterly.** Identifiers, versions, and regional availability move. Pinned versions plus a frozen dataset is how you notice.

## 📚 References

- [Model Router concepts](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/model-router) · [Use Model Router](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/model-router)
- [Evaluation approach for generative AI](https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai) · [Agent evaluators](https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) · [Evaluate agents with the SDK](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/agent-evaluate-sdk)
- [Hosted agents](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents) · [Observability in Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/observability)
- [Azure Developer CLI reference](https://learn.microsoft.com/azure/developer/azure-developer-cli/reference) · [Quotas and limits](https://learn.microsoft.com/azure/ai-foundry/openai/quotas-limits)
- [Preview supplemental terms](https://azure.microsoft.com/support/legal/preview-supplemental-terms/)

<br/>

🏁 **You finished.** ⬆️ [Lab 2](./README.md) · 📚 [Self-guided index](../README.md) · 🏠 [Workshop overview](../../../README.md)
