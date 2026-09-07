# 05 · Deploy and version the agent

⏱️ **Time:** 10 minutes

## 🎯 Goal

Publish Product Launch Studio to your Foundry project as a fixed, numbered
version. Foundry calls this an **immutable version**: we create a new version
instead of editing one that is already deployed.

## Objectives

- Deploy the agent with `azd deploy` using direct code deployment (no Docker, no ACR).
- Read back the deployed agent name and version.
- Smoke-test the deployed endpoint.
- Predict, before [Lab 2](../lab-2-agent-optimize/README.md), which upcoming
  change will create a new version—and which will not.

## ✅ Prerequisites

- [Module 01](../lab-0-setup/01-provision-environment.md) complete.
- [Module 04](./04-run-agent-locally.md) attempted (a local run is helpful but not required).
- Terminal 1 from [Module 04](./04-run-agent-locally.md) stopped (`Ctrl+C`) so
  the local run does not hold the session.

<br/>

## 🔢 Steps

### Step 1 — Confirm the deployment method (1 min)

```bash
cd "$WORKSHOP_SRC"
grep -A 4 "codeConfiguration" azure.yaml
```

Because the service block declares `codeConfiguration`, `azd deploy` zips the source and lets Foundry build it. No Dockerfile, no container registry. Container deployment is only needed when an agent depends on system packages or a prebuilt image.

### Step 2 — Check the current state (1 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent show --output json
```

Expect `not_deployed` on your first run. That is your starting point.

### Step 3 — Deploy (4 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd deploy
```

The first deployment takes a few minutes: azd packages the source, Foundry builds it, and a new agent version is registered and activated.

### Step 4 — Read back name and version (1 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent show --output json
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-values | grep -E '^AGENT_'
```

`azd` writes `AGENT_<SERVICE>_NAME` and `AGENT_<SERVICE>_VERSION` back into your
environment. **Write the version down.** The baseline scores in
[Module 07](../lab-2-agent-optimize/07-baseline-evaluation.md) belong to this
version, and [Module 10](../lab-2-agent-optimize/10-wrap-up.md) compares against
it.

| Record this | Value |
|---|---|
| Agent name | `product-launch-studio` |
| Agent version | *(from `AGENT_..._VERSION`)* |
| `adaptive-copy` backed by | GPT-5.4-mini |

### Step 5 — Smoke-test the deployed agent (2 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent invoke \
  "Draft a one-sentence launch headline for the HikeMate TrailLite Daypack and cite the brief line that supports it."
```

Note there is no `--local` this time — this call goes to the deployed agent in Foundry. `azd ai agent invoke` manages the session for you; add `--new-session` if you want a clean slate.

### Step 6 — Predict the versioning behaviour (1 min)

Answer before you continue. We’ll verify both answers in
[Lab 2](../lab-2-agent-optimize/README.md).

| Change | New agent version? |
|---|---|
| Editing `main.py` or `.agent_configs/baseline/instructions.md`, then `azd deploy` | **Yes** — the agent definition changed |
| Switching the model behind the `adaptive-copy` **deployment** in [Module 08](../lab-2-agent-optimize/08-model-router-swap.md) | **No** — the agent still references the same deployment name |

That asymmetry is the practical reason to name deployments after **jobs** (`adaptive-copy`) rather than after models (`gpt-5-4-mini`): you can change the model layer without touching, redeploying, or re-certifying the agent.

<br/>

## 📤 Expected result

- `azd ai agent show` reports an **active** agent with a version string.
- `AGENT_PRODUCT_LAUNCH_STUDIO_NAME` and `..._VERSION` appear in `azd env get-values`.
- The remote invoke returns a grounded headline with a brief citation.

## 🏆 Quick win

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent show --output json | head -20
```

A fixed agent version we can return to later—created from source, with no
Dockerfile and no registry—in roughly four minutes. This is our safe starting
point for every comparison that follows.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** `azd ai agent show` returns an active version, and you have written that version down.

| If… | Do this |
|---|---|
| Deployment fails repeatedly | Run `azd ai agent doctor` from `$WORKSHOP_SRC` and fix the field it names. |
| You are over budget | Take the version number and move on. [Module 06](./06-observe-the-agent.md) can use the traces you already have. |
| You need to redeploy | Just run `azd deploy` again — it creates a new version; the previous one still exists. |
| The deploy path looks wrong (`Packaging container`) | `codeConfiguration` is missing or malformed in `azure.yaml`. Fix it, then redeploy. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `agent_definition_not_found` | Deployed name does not match `azure.yaml` | Redeploy from `$WORKSHOP_SRC`. |
| `invalid_agent_manifest` | Malformed service block | `azd ai agent doctor`, then fix the named field. |
| Version never becomes active | Build or startup failure | `azd ai agent monitor` for logs; check the entry point is `main.py`. |
| Invoke times out | Container still starting | Wait ~60 s after the deploy completes and retry. |
| `missing_project_endpoint` | Environment lost the endpoint | `azd env set AZURE_AI_PROJECT_ENDPOINT "<endpoint>"`. |

## ➡️ Next

It is deployed. Before you try to improve it, learn to see what it is actually doing.

**[Module 06 — Observe what the agent actually did](./06-observe-the-agent.md)** · ⬆️ [Lab 1](./README.md)
