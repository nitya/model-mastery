# Lab 2 · Module 01 — Change and deploy a new version

**Time:** 10 minutes

## Goal

Make one small, measurable change to the Campaign Copywriter, test it locally,
deploy it to Microsoft Foundry as a fixed agent version, and invoke that version
in the cloud.

## Learning objectives

By the end of this module you can:

- Make a scoped instruction change and verify it before deploying.
- Deploy a hosted agent version with `azd deploy`.
- Read the active agent version with `azd ai agent show`.
- Explain why hosted agent versions are immutable.

## Prerequisites

- [Lab 2, module 00](./00-run-agent-locally.md) complete: a successful local
  invocation.
- The local agent from [module 00](./00-run-agent-locally.md) is **stopped**.

## Instructions

### Step 1 — Record your baseline version (1 minute)

1. [] Enter the `src` azd project root and read the currently deployed version:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent show --output json
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** JSON for `product-launch-studio` including a version value and a running
    state.

1. [] Write the version down. Call it **v-baseline**.

>[!Knowledge] A hosted **agent version** is immutable. `azd deploy` never edits the running version;
it packages your source, registers a new version, and switches traffic to it. That is what makes
before-and-after comparison honest — the old version still exists exactly as it was measured.

### Step 2 — Make one scoped change (3 minutes)

1. [] Open
   `agents\product-launch-studio\.agent_configs\baseline\instructions.md`.

1. [] Find the channel rules in the copywriter instructions and add exactly one rule. Use this
   wording so the whole class measures the same change:

    ```text
    Every channel variant must end with a single, explicit call to action that names
    the action the reader should take. Never end with a generic sign-off.
    ```

1. [] Save the file.

	>[!Alert] Change **only** this. Do not adjust the model, the temperature, or another role. The
    entire point of [module 06](./06-compare-and-wrap-up.md) is being able to
    attribute a score change to a specific edit.

<!-- SCREENSHOT: ../images/lab2-copywriter-edit.png -->

### Step 3 — Test locally before deploying (3 minutes)

1. [] Start the agent locally in one terminal:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent run --no-client
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

1. [] In a second terminal, send a copy-only request:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent invoke --local "Write the social caption and email copy for the TrailLite Daypack. Use only E1-E5 in data/campaign-brief.md and preserve every qualifier."
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** each channel variant now ends with a specific, named call to action rather
    than a generic sign-off.

1. [] Stop the local agent with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

>[!tip] Always confirm a change locally before you deploy it. A local round trip costs seconds; a
deployment costs minutes, and in a 90-minute workshop minutes are the scarce resource.

### Step 4 — Deploy a new version (2 minutes)

1. [] Deploy just the agent service:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd deploy product-launch-studio
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** azd packages the source, registers a new agent version, and reports success.
    Expect one to three minutes.

<!-- SCREENSHOT: ../images/lab2-azd-deploy-success.png -->

	>[!Alert] `azd deploy product-launch-studio` deploys the **agent service only**. Never run bare
    `azd provision` in this workshop — infrastructure is pre-provisioned and your lab account cannot
    create resources.

	>[!note] Only the files the agent needs are uploaded. `.agentignore` in the
    agent folder excludes tooling, secrets, and local results from the
    deployment package.

### Step 5 — Confirm and invoke the new version (1 minute)

1. [] Read the active version again:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent show --output json
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** the version has incremented from **v-baseline**. Write the new one down as
    **v-cta**.

1. [] Invoke the deployed version — note there is no `--local` this time:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent invoke "Write the social caption and the LinkedIn post for the TrailLite Daypack using only E1-E5."
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** the cloud response shows the same explicit call-to-action behaviour you saw
    locally.

<!-- SCREENSHOT: ../images/lab2-cloud-invoke-response.png -->

## Expected result

Two versions now exist. **v-baseline** has the original instructions; **v-cta** adds the
call-to-action rule and is live, answering cloud invocations with the new behaviour.

## Quick win

You changed one line, deployed it, and saw the behaviour change in the cloud — the shortest possible
demonstration of the deploy-and-version part of our AgentOps workflow.

## Checkpoint and recovery

```powershell
$env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
azd ai agent invoke "Reply with OK if the deployed version is live."
Remove-Item Env:\AZURE_DEV_USER_AGENT
```

**Expected result:** a short acknowledgement from the deployed agent.

>[!Hint] **Recovery.** If the deployment fails, keep the saved file open, run the agent doctor, and
redeploy from `src`. The baseline checkpoint is a review reference, not a source snapshot:
```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
Get-Content .\checkpoints\00-baseline\instructions.md
$env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
azd ai agent doctor
azd deploy product-launch-studio
Remove-Item Env:\AZURE_DEV_USER_AGENT
```
If the source itself is corrupt, restart the disposable Skillable lab rather than copying a partial
checkpoint into the agent package.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `invalid_agent_manifest` | Run `azd ai agent doctor` and fix the field it names. Usually a YAML edit in `azure.yaml`. |
| Deployment succeeds but the version does not change | The source was unchanged. Confirm `.agent_configs\baseline\instructions.md` was saved, then redeploy. |
| Version poll times out | The remote build is still running. Wait a minute and re-run `azd ai agent show --output json`. |
| `no azure.ai.agent service named ... found` | You are in the wrong folder. `cd C:\LabFiles\model-mastery\foundry\agent-optimization\src`. |
| `invalid value "json" for --output` on invoke | `azd ai agent invoke` supports only `default` and `raw`. Drop the flag. |
| Cloud invoke returns `session_not_ready` or `424` | The new version is still warming up. Wait 20 seconds and invoke again. |
| The cloud response ignores the new rule | You are hitting the old version. Re-check `azd ai agent show` and confirm the version incremented. |

## Transition

Your change is live, but "it looks right to me" is not evidence. Next you will open the trace for
the invocation you just made and see exactly which model and tool calls produced that answer.
