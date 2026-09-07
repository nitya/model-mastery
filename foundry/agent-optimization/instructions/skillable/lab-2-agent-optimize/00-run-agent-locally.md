# Lab 2 · Module 00 — Run the multi-agent application locally

**Time:** 12 minutes

## Goal

Run the complete Product Launch Studio agent on the lab VM, send it the sample brief and product
image, and read the campaign package it produces.

## Learning objectives

By the end of this module you can:

- Start a hosted agent locally with `azd ai agent run`.
- Invoke a locally running agent and read its response.
- Trace grounded evidence from the Product Analyst through to the final copy.
- Locate the Campaign Copywriter instructions in the source tree.

## Prerequisites

- [Lab 0](../lab-0-setup/02-verify-predeployed-environment.md) complete:
  preflight `READY`, both CLIs signed in.
- VS Code open at `C:\LabFiles\model-mastery\foundry\agent-optimization`, with the terminal at
  `$WorkshopSrc` (`...\agent-optimization\src`).

## Instructions

### Step 1 — Read the shape of the application (2 minutes)

1. [] In the VS Code Explorer, open `agents\product-launch-studio\` and note the layout:

    | Path | What it holds |
    |---|---|
    | `main.py` | Entry point; exposes the hosted-agent protocol |
    | `product_launch_studio\config.py` | Reads deployment names from environment variables |
    | `product_launch_studio\orchestration.py` | Coordination logic and role handoffs |
    | `product_launch_studio\instructions.py` | Instructions for non-optimized roles |
    | `product_launch_studio\image_tool.py` | The image generation tool abstraction |
    | `.agent_configs\baseline\` | The baseline configuration Agent Optimizer compares against |
    | `eval.yaml` | Evaluation and optimization configuration |

1. [] Open
   `agents\product-launch-studio\.agent_configs\baseline\instructions.md` and read the copywriter
   instructions.

    **Expected result:** you can see the channel rules, the tone rules, and the explicit ban on
    claims that the product evidence does not support.

<!-- SCREENSHOT: ../images/lab2-copywriter-instructions.png -->

    >[!note] Remember where this file is. We’ll edit it in
    [module 01](./01-change-and-deploy.md), and Agent Optimizer will rewrite it in
    [module 05](./05-agent-optimizer.md).

1. [] Open `agents\product-launch-studio\product_launch_studio\config.py` and confirm it reads
   deployment names and `COPYWRITER_DEPLOYMENT_MODE` from environment variables.

>[!Knowledge] Every role reads a **purpose-based deployment name**. That is why
[module 04](./04-model-router.md) can move
the copywriter onto Model Router by changing one environment variable, with no code edit at all.

### Step 2 — Start the agent locally (3 minutes)

1. [] In the terminal, at the `src` azd project root, start the agent without opening a client:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent run --no-client
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** the agent starts and listens on `http://localhost:8088`. The terminal keeps
    streaming logs — leave it running.

<!-- SCREENSHOT: ../images/lab2-agent-run-local.png -->

	>[!Alert] Leave this terminal running for the rest of this module. Open a **second** terminal for
    the next steps with **Terminal** > **New Terminal**.

1. [] In the second terminal, return to the azd project root:

    +++cd C:\LabFiles\model-mastery\foundry\agent-optimization\src+++

	>[!Hint] If the port is already in use, an earlier run is still alive. Press <kbd>Ctrl</kbd>+<kbd>C</kbd>
    in the old terminal, wait five seconds, and start again.

### Step 3 — Send the campaign brief (4 minutes)

1. [] In the **second** terminal, at the `src` azd project root, review the brief you are about to send:

    +++Get-Content .\data\campaign-brief.md+++

    **Expected result:** a short brief naming the HikeMate TrailLite Daypack, the
    target channels, the five evidence entries, and the compliance constraints.

1. [] Invoke the locally running agent:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent invoke --local "Run the campaign brief in data/campaign-brief.md against the product image in assets/traillite-daypack.png. Keep image observations separate from product-record/manual evidence and return the full campaign package."
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** after roughly 30–60 seconds you receive a campaign package containing
    grounded product evidence, a positioning strategy, and copy for each requested channel.

<!-- SCREENSHOT: ../images/lab2-local-invoke-response.png -->

	>[!note] Image generation is the slowest step. If the response includes a note that the image was
    produced by the local test stub, that is expected under class load and does not affect anything
    you measure later.

### Step 4 — Follow the evidence (3 minutes)

1. [] In the response, find the **product evidence** section produced by the Product Analyst. Pick
   one concrete manual-backed detail, for example the adjustable shoulder straps in E3.

1. [] Find that same detail reused in the **copy** for at least one channel.

    **Expected result:** the copy references features that appear in the evidence, and nothing else.

1. [] Scan the copy for any claim the photo cannot support — dimensions, weight,
   catalog price, water resistance, hydration compatibility, material,
   durability, warranty, or capacity. Note anything you find.

    **Expected result:** in the baseline you should find few or none, but the copy may still be
    generic or off-brief. That gap is what we’ll measure in
    [module 03](./03-batch-evaluation.md).

>[!Knowledge] This is **evidence propagation**: a fact is established once, by the role that can
verify it, and every downstream role is constrained to it. When an agent hallucinates a marketing
claim, the bug is almost never in the copywriter's vocabulary — it is a broken constraint between
roles.

### Step 5 — Stop the local agent

1. [] Return to the **first** terminal and press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop the local agent.

    **Expected result:** the process exits and the prompt returns.

## Expected result

A local run of Product Launch Studio returned a complete campaign package, you traced one product
fact from evidence into copy, and you know where the copywriter instructions live.

## Quick win

A working multi-agent application answering a real brief on your own machine — with four models and
one tool cooperating behind a single request.

## Checkpoint and recovery

```powershell
$env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
azd ai agent invoke --local "Reply with OK if you are running."
Remove-Item Env:\AZURE_DEV_USER_AGENT
```

**Expected result:** a short acknowledgement while the local agent is running.

>[!Hint] **Recovery.** If the local source was edited before this module, use the real baseline
checkpoint as a review reference, then restart the disposable lab to restore source:
```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
Get-Content .\checkpoints\00-baseline\instructions.md
```
The checkpoint is instructor-authored guidance, not a complete source snapshot.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `azd ai agent run` exits immediately | From `src`, read the last log lines and run `azd env get-values`; confirm the required model settings and `COPYWRITER_DEPLOYMENT_MODE` are set. |
| `ModuleNotFoundError` | The virtual environment is not active. Run `.\.venv\Scripts\Activate.ps1`, then retry. |
| `401` or `403` from a model call | Your `az` token expired. Run `az login` again in a new terminal. |
| `429` from a model call | Shared deployment under class load. Wait 15 seconds and re-invoke. |
| `session_not_ready` or `424` | The local server is still warming up. Wait 10 seconds and re-invoke. |
| The invoke hangs past two minutes | Press <kbd>Ctrl</kbd>+<kbd>C</kbd> in the invoke terminal and retry once. If it hangs again, use the recovery snapshot above. |
| Response has copy but no product evidence | The Product Analyst call failed. Check the first terminal's logs for a `visual-understanding` error and tell your instructor if the deployment is unhealthy. |

## Transition

The agent works locally. Next, we’ll change one line of the copywriter’s
instructions, deploy it to Microsoft Foundry as a new fixed version, and see the
change take effect in the cloud.
