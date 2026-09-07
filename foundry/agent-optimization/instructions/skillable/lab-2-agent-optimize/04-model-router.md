# Lab 2 · Module 04 — Improve selection with Model Router

**Time:** 5 minutes

## Goal

Remap the existing Campaign Copywriter deployment to Model Router, run three requests of increasing
complexity, and compare the result with your fixed-model baseline.

## Learning objectives

By the end of this module you can:

- Preview and apply a model remap without adding a deployment.
- Describe what Model Router decides and what it does not.
- Compare a routed version with a fixed-model baseline on the same rubric.

## Prerequisites

- Lab 2 module 03 complete: you have a baseline score recorded.
- The parent workshop root contains the instructor-completed `.env`.

>[!Alert] The workshop always has exactly five purpose-based deployments. There is no separate
router deployment. This module remaps the same `adaptive-copy` deployment from GPT-5.4-mini to
Model Router.

## Instructions

### Step 1 — Preview and apply the remap (1 minute)

1. [] From the `src` azd project root, run the default what-if preview:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    .\scripts\switch-router.ps1 -EnvFile ..\.env
    ```

    **Expected result:** Azure shows the proposed in-place model change for `adaptive-copy`, then the
    script reports `[OK] What-if complete; no deployment changed.`

	>[!tip] For a local-only preview that makes no Azure call, use
    `.\scripts\switch-router.ps1 -EnvFile ..\.env -Offline`.

1. [] Apply the reviewed remap:

    ```powershell
    .\scripts\switch-router.ps1 -EnvFile ..\.env -Apply
    ```

    Type `SWITCH` when prompted.

    **Expected result:** the script provisions the reviewed in-place change and reports
    `[OK] adaptive-copy now maps to Model Router.`

	>[!Alert] Do not run bare `azd provision`. The script sets the four adaptive-copy model values
    and `COPYWRITER_DEPLOYMENT_MODE`, then provisions only the reviewed configuration.

1. [] Verify the remap while leaving the hosted-agent version unchanged:

    ```powershell
    azd env get-value COPYWRITER_DEPLOYMENT_MODE
    azd env get-value ADAPTIVE_COPY_MODEL_NAME
    ```

    **Expected result:** `routed` and the configured Model Router model name.

>[!Knowledge] No Python changed and the deployment name did not change. The agent still calls
`adaptive-copy`; the model behind that purpose-based name is now Model Router.

### Step 2 — Run three complexity levels (2 minutes)

1. [] **Simple** — a short caption:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent invoke "Write one social caption for the TrailLite Daypack. Maximum 20 words."
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

1. [] **Moderate** — coordinated multi-channel copy:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent invoke "Write coordinated copy for social, email, and LinkedIn for the TrailLite Daypack. Each channel needs a different call to action and evidence citations."
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

1. [] **Complex** — tightly constrained copy:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent invoke "Audit TrailLite Daypack copy that claims full waterproofing, 30 L capacity, recycled construction, independent certification, market superiority, and lifetime durability. Correct every unsupported claim, preserve E4's light-rain limitation, and end with compliant LinkedIn copy for weekend hikers."
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** all three succeed. Record what happens; do not assume the complex case must
    improve before you measure it.

<!-- SCREENSHOT: ../images/lab2-router-three-requests.png -->

1. [] Open **Tracing** in the Microsoft Foundry portal and inspect the `adaptive-copy` span for each
   request. Where telemetry exposes it, note which underlying model served each request.

<!-- SCREENSHOT: ../images/lab2-router-trace-model.png -->

>[!Alert] Routing is a **per-request decision**, and it is not a promise. Judge the router on
aggregate quality, latency, and cost across your dataset — never on one routing outcome.

>[!Knowledge] Model Router chooses **which model answers each request**. It does not change your
instructions, tools, rubric, dataset, or purpose-based deployment name.

### Step 3 — Re-evaluate and compare (2 minutes)

1. [] Re-run the same evaluation and save the result in a learner-local directory:

    ```powershell
    New-Item -ItemType Directory -Force .\.foundry\results | Out-Null
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent eval run
    azd ai agent eval show -O .\.foundry\results\my-router-results.json
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** a second scored run is written under `.foundry\results`.

1. [] Fill in the second row of your scorecard:

    | Version | Copywriter lever | Overall | Weakest criterion | Copywriter span latency |
    |---|---|---|---|---|
    | Baseline | Fixed `adaptive-copy` | | | |
    | **Improvement 1** | **Routed `adaptive-copy`** | | | |

1. [] Answer honestly: did quality improve, stay flat, or trade off against latency?

	>[!note] A flat or mixed result is legitimate. Routing helps most when request complexity varies.

## Expected result

The existing `adaptive-copy` deployment is remapped to Model Router without an agent redeploy, three
complexity levels ran, and you have a second scored row on the identical dataset and rubric.

## Quick win

A measured fixed-model versus routed-model comparison while retaining exactly five deployments.

## Checkpoint and recovery

```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
azd env get-value COPYWRITER_DEPLOYMENT_MODE
azd env get-value ADAPTIVE_COPY_MODEL_NAME
Test-Path .\.foundry\results\my-router-results.json
```

**Expected result:** `routed`, the configured Model Router model name, and `True`.

>[!Hint] **Recovery.** If the router evaluation fails or runs long, inspect the explicitly labelled
instructor-prepared teaching example:
```powershell
Get-Content .\checkpoints\evaluation\router-results.example.json
```
Its values are illustrative, not live measurements. Mark the scorecard row **prepared example**.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Preview says `.env` is missing | Confirm `C:\LabFiles\model-mastery\foundry\agent-optimization\.env` exists. It belongs at the parent workshop root, not under `src`. |
| Preview fails preflight | From `src`, run `.\scripts\preflight.ps1 -EnvFile ..\.env -Online` and follow its remediation. |
| Apply waits for input | Type `SWITCH`, or rerun the reviewed command with `-Yes`. |
| Provisioning fails during the remap | Re-run the same `-Apply` command; it is idempotent. If it fails again, continue with the prepared example and tell your instructor. |
| Every request appears to route to the same model | Normal. Your three prompts may not be far enough apart in complexity. Report what you observed. |
| The trace does not show an underlying model name | Not all telemetry surfaces it. Compare latency and token usage instead. |
| `429` during the three requests | Shared deployment under class load. Wait 15 seconds and resend that request only. |

## Transition

You changed **which model** answers while retaining the `adaptive-copy` name. Now change **what the
copywriter is told** by using Agent Optimizer to propose and score candidate instructions.
