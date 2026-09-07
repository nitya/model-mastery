# Self-guided workshop — 90 minutes

Work through the modules **in order**. Each one is a single sitting: a stated time budget, a goal, numbered steps, copyable commands, and a checkpoint so you always know whether you can move on.

> **Read the [workshop overview](../../README.md) first** if you have not seen the scenario or the hill-climbing frame.

<br/>

## How to use these modules

Every module has the same shape:

| Section | What it gives you |
|---|---|
| ⏱️ **Time** | The budget. If you exceed it by more than 50%, jump to *Checkpoint and recovery*. |
| 🎯 **Goal / Objectives** | One sentence, then the concrete skills. |
| ✅ **Prerequisites** | What must already be true. |
| 🔢 **Steps** | Numbered. Every command block names its working directory. |
| 📤 **Expected result** | What success looks like on your screen. |
| 🏆 **Quick win** | A 60-second payoff you can show someone. |
| 🧭 **Checkpoint and recovery** | The one thing that must be true, and how to get unstuck fast. |
| 🔧 **Troubleshooting** | The failures we actually see. |
| ➡️ **Next** | The link forward. |

### The `WORKSHOP_ROOT` convention

The workshop is nested inside a larger repository, so every command anchors to one variable instead of guessing at relative paths. Set it once per terminal (Module 01 makes it permanent):

```bash
export WORKSHOP_ROOT=/workspaces/model-mastery/foundry/agent-optimization
export WORKSHOP_SRC="$WORKSHOP_ROOT/src"
cd "$WORKSHOP_SRC"
```

Working locally instead of in Codespaces? Run this from the root of your clone:

```bash
export WORKSHOP_ROOT="$PWD/foundry/agent-optimization"
export WORKSHOP_SRC="$WORKSHOP_ROOT/src"
```

Every `azd` command in this workshop runs from `$WORKSHOP_SRC`, because that is where `azure.yaml` lives. Agent source lives in `$WORKSHOP_SRC/agents/product-launch-studio`. The top-level `.env`, `sample.env`, and `requirements.txt` remain under `$WORKSHOP_ROOT`.

### The `AZURE_DEV_USER_AGENT` convention

This project tags its `azd` traffic. Prefix `azd` commands — and workshop scripts that call `azd` — inline:

```bash
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-values
```

Set it **inline only**. Never commit it to `azure.yaml`, `.env`, or `azd env set`.

<br/>

## Module map

### Lab 0 — Setup · 15 min → [lab-0-setup](./lab-0-setup/README.md)

| # | Module | Time | You leave with |
|---|---|---|---|
| 01 | [Provision the workshop environment](./lab-0-setup/01-provision-environment.md) | 10 min | A Foundry project and five model deployments |
| 02 | [Orientation: the studio and the hill](./lab-0-setup/02-orientation.md) | 5 min | The scenario, the roles, and the rules of measurement |

### Lab 1 — Explore models · 48 min → [lab-1-model-explore](./lab-1-model-explore/README.md)

| # | Module | Time | You leave with |
|---|---|---|---|
| 03 | [Model playground: pick the right tool](./lab-1-model-explore/03-model-playground.md) | 18 min | A model-to-role comparison you made yourself |
| 04 | [Run the agent locally](./lab-1-model-explore/04-run-agent-locally.md) | 12 min | The four roles and the image tool running on localhost |
| 05 | [Deploy and version the agent](./lab-1-model-explore/05-deploy-and-version.md) | 10 min | An immutable agent version in Foundry |
| 06 | [Observe what the agent actually did](./lab-1-model-explore/06-observe-the-agent.md) | 8 min | Traces that show which model handled what |

### Lab 2 — Optimize the agent · 27 min → [lab-2-agent-optimize](./lab-2-agent-optimize/README.md)

| # | Module | Time | You leave with |
|---|---|---|---|
| 07 | [Baseline evaluation](./lab-2-agent-optimize/07-baseline-evaluation.md) | 12 min | A recorded altitude: scores on a fixed dataset and rubric |
| 08 | [Swap in Model Router](./lab-2-agent-optimize/08-model-router-swap.md) | 5 min | The same deployment name, a different selection strategy |
| 09 | [Agent Optimizer](./lab-2-agent-optimize/09-agent-optimizer.md) | 5 min | Candidate instructions you reviewed and did not blindly apply |
| 10 | [Wrap-up and next steps](./lab-2-agent-optimize/10-wrap-up.md) | 5 min | A promote/revert decision and a clean subscription |

<br/>

## Implementation files you will touch

| Path | What it is |
|---|---|
| [`../../src/azure.yaml`](../../src/azure.yaml) | Model deployments and the hosted agent service definition |
| [`../../sample.env`](../../sample.env) | Every variable the workshop reads; you copy it to `.env` |
| [`../../src/scripts/`](../../src/scripts/) | `preflight.sh`, `configure-environment.sh`, `provision.sh`, `switch-router.sh`, `cleanup.sh` |
| [`../../src/data/`](../../src/data/) | Campaign brief, `eval-cases.jsonl`, `router-complexity-cases.jsonl`, evaluator rubric, `eval.yaml` |
| [`../../src/assets/`](../../src/assets/) | TrailLite Daypack PNG plus exact upstream provenance and MIT license |
| [`../../src/agents/product-launch-studio/`](../../src/agents/product-launch-studio/) | Agent source, `.agent_configs/baseline/`, tests |
| [`../../src/infra/`](../../src/infra/) | Bicep templates used by `azd provision` |

<br/>

## Before you start

- **Preview features.** Model Router, Agent Optimizer, and the `azd ai agent` command surface are in preview. Command flags and output can change between versions — when something looks different, run `--help` before assuming the workshop is wrong. See the [preview supplemental terms](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
- **Portal drift.** Foundry's portal changes often, so these modules describe *what to look for* at [ai.azure.com](https://ai.azure.com) rather than exact click paths, and contain no screenshots.
- **Cost.** You are creating real, billable Azure resources. Module 10 deletes them.

➡️ Start with **[Module 01 — Provision the workshop environment](./lab-0-setup/01-provision-environment.md)**.
