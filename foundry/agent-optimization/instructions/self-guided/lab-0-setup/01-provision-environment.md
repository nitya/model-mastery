# 01 · Provision the workshop environment

⏱️ **Time:** 10 minutes (Azure provisioning runs in the background while you read Module 02)

## 🎯 Goal

Stand up a Microsoft Foundry project with the five model deployments Product Launch Studio needs, using the workshop's own scripts — no manual portal clicking.

## Objectives

- Anchor your shell with the `WORKSHOP_ROOT` convention.
- Validate models, versions, quota, and local assets **before** spending anything.
- Provision a Foundry project, Application Insights, and five model deployments with `azd`.
- Confirm the environment is real by reading it back.

## ✅ Prerequisites

- An Azure subscription where you can create a Foundry account, project, and model deployments.
- The **model versions and region** your instructor verified (see [instructor preparation](../../../README.md#6-instructor-preparation)). Model identifiers, versions, and regional availability change independently of this repository — the instructor confirms them before delivery.
- A GitHub Codespace or Linux Dev Container opened on this repository (Bash).

<br/>

## 🔢 Steps

### Step 1 — Anchor your shell

```bash
export WORKSHOP_ROOT=/workspaces/model-mastery/foundry/agent-optimization
export WORKSHOP_SRC="$WORKSHOP_ROOT/src"
echo "export WORKSHOP_ROOT=$WORKSHOP_ROOT" >> ~/.bashrc
echo 'export WORKSHOP_SRC="$WORKSHOP_ROOT/src"' >> ~/.bashrc
cd "$WORKSHOP_ROOT"
ls
```

> 💻 **Working locally instead?** From the root of your clone run `export WORKSHOP_ROOT="$PWD/foundry/agent-optimization"; export WORKSHOP_SRC="$WORKSHOP_ROOT/src"`, and make sure Bash, Python 3.11+, the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), and [`azd` ≥ 1.20.0](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) are installed. Everything after this step is identical.

### Step 2 — Sign in

```bash
cd "$WORKSHOP_SRC"
az login
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd auth login
```

In a Codespace, use the device-code flow if the browser handoff does not complete: `az login --use-device-code`.

### Step 3 — Create your private `.env`

`sample.env` is the canonical list of every variable the workshop reads. Copy it, then fill in the four values only you know.

```bash
cd "$WORKSHOP_ROOT"
cp sample.env .env
```

Edit `.env` and set:

| Variable | Value |
|---|---|
| `AZURE_SUBSCRIPTION_ID` | Your subscription GUID (`az account show --query id -o tsv`) |
| `AZURE_LOCATION` | The region your instructor named |
| `AZURE_AI_DEPLOYMENTS_LOCATION` | The region where the five models are available (often the same) |
| `*_MODEL_VERSION` (five of them) | The exact versions your instructor verified |

`.env` is untracked. Never commit it.

### Step 4 — Preflight before you spend

```bash
cd "$WORKSHOP_SRC"
./scripts/preflight.sh --env-file ../.env --online
```

This checks tools, every required variable, the workshop data files, your Azure sign-in, the model catalog in your region, and prints current quota. It **changes nothing**.

> Blank `*_MODEL_VERSION` values fail preflight on purpose. Pinning versions is what makes your results reproducible tomorrow.

### Step 5 — Configure the azd environment

Preview the changes first, then apply them. This writes **local** azd state only.

```bash
cd "$WORKSHOP_SRC"
./scripts/configure-environment.sh --env-file ../.env
AZURE_DEV_USER_AGENT=microsoft_foundry_skill ./scripts/configure-environment.sh --env-file ../.env --apply
```

Type `CONFIGURE` when prompted.

### Step 6 — Preview the Azure resources

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill ./scripts/provision.sh --env-file ../.env --preview
```

Read the what-if output. You should see one resource group, a Foundry account and project, Log Analytics + Application Insights, and five model deployments.

### Step 7 — Provision

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill ./scripts/provision.sh --env-file ../.env --apply
```

Type `PROVISION` when prompted. This creates **billable** resources and typically takes 5–8 minutes.

> ⏳ While it runs, read [Module 02](./02-orientation.md). Come back and finish Step 8 when the command returns.

### Step 8 — Verify

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-values
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai project show --output json
```

<br/>

## 📤 Expected result

- `azd env get-values` prints a populated `AZURE_AI_PROJECT_ENDPOINT` that looks like
  `https://<account>.services.ai.azure.com/api/projects/<project>`, plus `APPLICATIONINSIGHTS_CONNECTION_STRING`.
- `azd ai project show` returns your project endpoint without an error code.
- Five deployments exist: `campaign-coordinator`, `visual-understanding`, `campaign-reasoning`, `adaptive-copy`, `creative-image`.

## 🏆 Quick win

```bash
cd "$WORKSHOP_SRC"
az cognitiveservices account deployment list \
  --name "$(AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_AI_ACCOUNT_NAME)" \
  --resource-group "$(AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_RESOURCE_GROUP)" \
  --query "[].{deployment:name, model:properties.model.name, version:properties.model.version}" \
  --output table
```

One table, five rows: your entire model layer, with pinned versions, in under a minute. Screenshot-worthy — and it is the exact table you will compare against in Module 08 after `adaptive-copy` changes.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** `azd env get-values` shows a non-empty `AZURE_AI_PROJECT_ENDPOINT`.

| If… | Do this |
|---|---|
| Provisioning failed partway | Re-run Step 7. `azd provision` is idempotent; it retries only what is missing. |
| A single model deployment failed on quota | Fix the region or capacity in `.env`, re-run Steps 5 and 7. Everything already created is preserved. |
| You are more than 5 minutes over budget | Continue to Module 02 while provisioning finishes in another terminal. Modules 02 and 03 only need the project endpoint and one working deployment. |
| Nothing works and you must reset | `./scripts/cleanup.sh --preview` to see what exists, then `--apply` to delete, and start again from Step 3. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `[ACTION] Set CAMPAIGN_COORDINATOR_MODEL_VERSION.` | A version is still blank in `.env` | Paste the instructor-verified version string. |
| Preflight reports the model is not in the catalog | Wrong region, or the identifier changed | Re-check with `az cognitiveservices model list --location <region> --output table`. |
| `InsufficientQuota` during provision | No capacity for that model/SKU in the region | Lower `capacity` in `$WORKSHOP_SRC/azure.yaml`, or pick a region with quota. See [quotas and limits](https://learn.microsoft.com/azure/ai-foundry/openai/quotas-limits). |
| Partner model (Claude-Sonnet-6) fails to deploy | Marketplace terms not accepted, or not available in region | Use the `VISUAL_UNDERSTANDING_FALLBACK_*` values in `.env` (GPT-5.4) and re-run Steps 5 and 7. |
| `not_logged_in` / `login_expired` from `azd` | Session expired | `azd auth login` again. |
| `project_not_found` | You ran `azd` outside the project | `cd "$WORKSHOP_SRC"` — `azure.yaml` lives there. |

## ➡️ Next

Your base camp exists. Now learn what you are climbing.

**[Module 02 — Orientation: the studio and the hill](./02-orientation.md)** · ⬆️ [Lab 0](./README.md)
