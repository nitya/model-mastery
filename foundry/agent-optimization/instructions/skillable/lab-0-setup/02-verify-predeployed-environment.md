# Lab 0 · Module 02 — Verify the pre-deployed environment

**Time:** 5 minutes

## Goal

Prove — without creating anything — that your Microsoft Foundry project already has the five model
deployments, the running baseline agent, and the local data this workshop needs.

## Learning objectives

By the end of this module you can:

- Read your workshop configuration out of the azd environment.
- Confirm each purpose-based model deployment exists and is healthy.
- Confirm a hosted agent version is deployed and answering.
- Interpret a preflight report and act on a single failed check.

## Prerequisites

- [Module 01](./01-sign-in-and-open-project.md) complete: VS Code open at the
  workshop root, terminal at
  `C:\LabFiles\model-mastery\foundry\agent-optimization\src`, and `az` and `azd` signed in.

>[!Alert] **You will not provision anything in this workshop.** Every command in this module is
read-only. If a check fails, the fix is a configuration or sign-in fix — never
`azd provision` and never `az ... create`. Ask your instructor if a resource is genuinely missing.

## Instructions

### Step 1 — Read your workshop configuration

1. [] In the VS Code terminal, enter the `src` azd project root and list the environment values:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    azd env get-values
    ```

    **Expected result:** values are printed for `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_RESOURCE_GROUP`,
    `AZURE_AI_ACCOUNT_NAME`, `APPLICATIONINSIGHTS_CONNECTION_STRING`, `OPTIMIZER_MODEL_DEPLOYMENT`,
    `COPYWRITER_DEPLOYMENT_MODE`, and the configured `*_MODEL_NAME` values.

1. [] Note the five purpose-based deployment names. You will use these words, not model names, for
   the rest of the workshop.

    | Deployment | Role it powers |
    |---|---|
    | `campaign-coordinator` | Campaign Coordinator |
    | `visual-understanding` | Product Analyst |
    | `campaign-reasoning` | Campaign Strategist |
    | `adaptive-copy` | Campaign Copywriter |
    | `creative-image` | Image generation tool |

>[!Knowledge] The application code never mentions GPT, Claude, or MAI. It reads these environment
variables and calls a **deployment name**. That indirection is what lets your instructor swap the
model behind `visual-understanding`, and what lets us switch the copywriter to
Model Router in [Lab 2](../lab-2-agent-optimize/04-model-router.md),
with no code change at all.

### Step 2 — Confirm the model deployments exist

1. [] List the deployments in the Foundry account:

    ```powershell
    az cognitiveservices account deployment list `
      --name $(azd env get-value AZURE_AI_ACCOUNT_NAME) `
      --resource-group $(azd env get-value AZURE_RESOURCE_GROUP) `
      --query "[].{name:name, state:properties.provisioningState}" -o table
    ```

    **Expected result:** a table that includes `campaign-coordinator`, `visual-understanding`,
    `campaign-reasoning`, `adaptive-copy`, and `creative-image`, each with state `Succeeded`.

<!-- SCREENSHOT: ../images/lab0-deployment-list.png -->

	>[!note] There is no separate router deployment. In
	[Lab 2](../lab-2-agent-optimize/04-model-router.md), the reviewed script switches
	the model behind `adaptive-copy` from GPT-5.4-mini to Model Router.

### Step 3 — Confirm the baseline agent is deployed

1. [] Ask azd about the deployed agent, setting the Foundry user agent inline and removing it
   immediately afterwards:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent show --output json
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** JSON describing an agent named `product-launch-studio` with a version
    number and a running state.

1. [] Write down the version number. This is your **baseline version**, and you will compare
   against it in [Lab 2](../lab-2-agent-optimize/03-batch-evaluation.md).

<!-- SCREENSHOT: ../images/lab0-agent-show.png -->

>[!Knowledge] `AZURE_DEV_USER_AGENT` tells Azure Developer CLI telemetry that the command came from
the Microsoft Foundry tooling flow. Set it inline right before an `azd` call and remove it right
after. Never persist it with `azd env set`, in `.env`, or in `azure.yaml` — it is a local
development setting, not configuration.

### Step 4 — Run the workshop preflight

1. [] Run the non-destructive preflight script:

    +++.\scripts\preflight.ps1 -EnvFile ..\.env -Online+++

    **Expected result:** tool, configuration, model-catalog, and quota checks complete, ending with
    `[OK] Preflight completed without making changes.`

<!-- SCREENSHOT: ../images/lab0-preflight-pass.png -->

	>[!Alert] The preflight script only reads. It checks tool versions, sign-in state, environment
    variables, deployment health, agent status, and local data files. It never provisions, deploys,
    or deletes.

1. [] If any check reports `FAIL`, read the remediation line it prints and follow it before moving on.

### Step 5 — Confirm the local workshop assets

1. [] Check that the evaluation data and prepared fallbacks are on disk:

    ```powershell
    Get-ChildItem .\assets, .\data, .\checkpoints -Recurse -File |
      Select-Object -ExpandProperty FullName
    ```

    **Expected result:** from `$WorkshopSrc`, the listing includes
    `assets\traillite-daypack.png`, `assets\PROVENANCE.md`,
    `assets\contoso-web-MIT-LICENSE.md`, `data\campaign-brief.md`,
    `data\eval-cases.jsonl`,
    `data\evaluators\campaign-quality.yaml`, and
    `checkpoints\00-baseline`, `checkpoints\01-evidence-optimized`,
    `checkpoints\optimizer-result.sample.json`, and files under `checkpoints\evaluation`.

>[!Knowledge] `checkpoints\` is our safety net. It holds known-good files—agent
instructions and clearly labelled instructor-prepared evaluation examples—so a slow or failed
step never costs you the rest of the workshop. These examples are not live measured data.

## Expected result

Preflight passes, exactly five purpose-based deployments are `Succeeded`, a
baseline `product-launch-studio` version is running, and the local data and checkpoint files exist.

## Quick win

A green preflight report. In one command you confirmed roughly a dozen things that normally take a
half hour of portal clicking to check.

## Checkpoint and recovery

```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
.\scripts\preflight.ps1 -EnvFile ..\.env
```

**Expected result:** the final line says `[OK] Preflight completed without making changes.`

>[!Hint] If preflight fails on **authentication**, re-run `az login` and `azd auth login` from
[Module 01](./01-sign-in-and-open-project.md), then run preflight again.
>
>If it fails on **environment**, run `azd env select workshop` and retry.
>
>If it fails on a **deployment** or on the **agent**, tell your instructor. Do not attempt to create
the missing resource; your lab account intentionally cannot.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `azd env get-values` prints nothing | No environment is selected. Run `azd env select workshop`. |
| `az cognitiveservices ... AuthorizationFailed` | Your `az` session is on the wrong subscription. Run `az account set --subscription "<lab subscription>"`. |
| `azd ai agent show` reports the extension is missing | Run `azd extension list` and confirm `azure.ai.agents` is installed. If it is not, this is an image problem — tell your instructor. |
| `.\scripts\preflight.ps1` is blocked by execution policy | From `src`, run it for this session only: `powershell -ExecutionPolicy Bypass -File .\scripts\preflight.ps1 -EnvFile ..\.env`. |
| Preflight warns that `visual-understanding` is backed by GPT-5.4 rather than Claude-Sonnet-6 | Expected in some regions. The workshop is unaffected — the deployment name is what matters. |
| A deployment shows state `Failed` | Capacity issue in the lab subscription. Tell your instructor; do not redeploy it yourself. |

## Transition

[Lab 0](./00-welcome.md) is complete in 10 minutes. Your environment is verified,
and every model in the catalog is callable. In
[Lab 1](../lab-1-model-explore/00-hill-climbing-orientation.md), we’ll meet those
models one at a time in the Microsoft Foundry playground and
decide, with evidence, which capability belongs to which task.
