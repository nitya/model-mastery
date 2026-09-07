# Lab 2 · Module 03 — Run a batch evaluation

**Time:** 12 minutes

## Goal

Score the deployed agent against a fixed dataset and rubric to produce the **baseline number** that
every later improvement is measured against.

## Learning objectives

By the end of this module you can:

- Read an evaluation dataset and a scoring rubric.
- Run a batch evaluation against a deployed agent version.
- Read per-criterion scores and identify a failure pattern.
- Explain why the dataset and rubric must stay frozen across runs.

## Prerequisites

- Lab 2 module 01 complete: version **v-cta** deployed.
- Lab 2 module 02 complete: you have a hypothesis in your scratch file.

## Instructions

### Step 1 — Read the dataset (2 minutes)

1. [] Enter the `src` azd project root and look at the evaluation cases:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    Get-Content .\data\eval-cases.jsonl | Select-Object -First 3
    ```

    **Expected result:** JSON lines, each with a `query` (a copywriting request) and an
    `expected_behavior` (a plain-language description of what a good answer does).

1. [] Count the cases:

    +++(Get-Content .\data\eval-cases.jsonl).Count+++

    **Expected result:** a small suite of roughly five to eight representative copywriting cases.

>[!Knowledge] Small and representative beats large and vague in a workshop. Five to eight cases run
in minutes and still expose real failure patterns. In production you would grow this dataset from
recorded traces so it reflects what users actually ask.

### Step 2 — Read the rubric (2 minutes)

1. [] Open the rubric:

    +++Get-Content .\data\evaluators\campaign-quality.yaml+++

    **Expected result:** the `campaign_quality` evaluator with four scored criteria.

    | Criterion | Question it asks |
    |---|---|
    | Evidence fidelity | Is every measurable claim supported, mapped to E1–E5, and qualified? |
    | Claim safety | Are unsupported claims declined or safely rewritten? |
    | Task adherence | Are requested channels, limits, evidence table, and risk review present? |
    | Usefulness | Is the copy clear, audience-appropriate, and actionable? |

	>[!note] Image quality is deliberately **not** scored. Generated imagery is slow and subjective;
    including it would make every comparison in this workshop noisier and longer.

>[!Alert] From this point on the dataset and rubric are **frozen**. Do not edit either file. If they
change between runs, your baseline and your improvements are no longer comparable and the whole
hill-climbing exercise collapses.

### Step 3 — Confirm the evaluation configuration (2 minutes)

1. [] Open `data\eval.yaml` in VS Code and confirm it points at the frozen assets:

    | Field | Expected value |
    |---|---|
    | `agent.name` | `product-launch-studio` |
    | `agent.kind` | `hosted` |
    | `agent.config` | `.agent_configs/baseline/metadata.yaml` |
    | `dataset.local_uri` | `../../data/eval-cases.jsonl` |
    | `evaluators` | four standard evaluators plus local `campaign_quality` |
    | `options.eval_model` | an existing chat deployment used as the judge |

1. [] Copy that frozen contract to the agent root where azd discovers it:

    ```powershell
    Copy-Item .\data\eval.yaml .\agents\product-launch-studio\eval.yaml -Force
    ```

    **Expected result:** the agent-root copy is identical to `data\eval.yaml`.

<!-- SCREENSHOT: ../images/lab2-eval-yaml.png -->

>[!Knowledge] `eval.yaml` is the shared contract between **evaluation** and **optimization**. Module
05's Agent Optimizer reads this same file, so the candidates it generates are scored on exactly the
rubric you are about to run. One contract, two consumers.

### Step 4 — Run the baseline evaluation (4 minutes)

1. [] Run the evaluation against the deployed agent:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent eval run
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** azd submits the run, streams progress, and prints a summary with an overall
    score and per-criterion scores. Expect three to six minutes.

<!-- SCREENSHOT: ../images/lab2-eval-run-summary.png -->

	>[!tip] While it runs, re-read your hypothesis from module 02 and predict which criterion will
    score lowest. Predicting before you look is the fastest way to build calibration.

1. [] Create a learner-local results directory and save the run details there:

    ```powershell
    New-Item -ItemType Directory -Force .\.foundry\results | Out-Null
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent eval show -O .\.foundry\results\my-baseline-results.json
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** the file is written and contains per-case scores.

### Step 5 — Find the failure pattern (2 minutes)

1. [] Record the overall score and the lowest-scoring criterion in your scratch file. This is
   **Baseline** in your scorecard.

1. [] Open two or three of the lowest-scoring cases and look for what they share:

    - Were they the **complex**, heavily constrained requests?
    - Did failures cluster on **constraint adherence** — length or disclaimer?
    - Did failures cluster on **task adherence**, where a requested channel or limit was missed?

1. [] Write one sentence naming the pattern, for example: *"The fixed copywriter model handles simple
   captions well but drops explicit constraints on the multi-constraint cases."*

>[!Knowledge] That sentence is the bridge to the rest of the workshop. If quality drops as request
complexity rises, one fixed model is being asked to be both fast and deep. **Module 04 attacks that
with Model Router.** If instead failures are about ignored rules regardless of complexity, the
instructions are the problem — **module 05 attacks that with Agent Optimizer.**

## Expected result

You have a recorded baseline overall score, per-criterion scores saved to
`.foundry\results\my-baseline-results.json`, and a named failure pattern.

## Quick win

A hard baseline number for the fixed-model version. Every claim you make for the rest of the
workshop can now be checked against it.

## Checkpoint and recovery

```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
Test-Path .\.foundry\results\my-baseline-results.json
```

**Expected result:** `True`.

>[!Hint] **Recovery.** If the evaluation fails or runs past your time budget, stop it and use the
explicitly labelled instructor-prepared example so you keep pace:
```powershell
Get-Content .\checkpoints\evaluation\baseline-results.example.json
```
Use its illustrative scores only for the workshop comparison and mark the row **prepared example**.
It is not service output and must not be presented as a live measurement.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `unknown command "init" for "azd ai agent eval"` | The command is `azd ai agent eval generate`. The suite here already exists, so you do not need it. |
| The run never starts | From `src`, copy `data\eval.yaml` to `agents\product-launch-studio\eval.yaml`, then confirm `azd ai agent show` reports a running version. |
| `429` mid-run | Shared judge deployment under class load. Re-run once; if it fails again, use and label the prepared example. |
| Scores are all zero | The agent returned errors rather than copy. Invoke it once manually to confirm health, then re-run. |
| Run exceeds six minutes | Let it finish in the background if the class is ahead of schedule; otherwise switch to the labelled prepared example and move on. |
| `eval show` writes an empty file | The run has not finalized. Run `azd ai agent eval list`, confirm the latest run completed, then retry. |

## Transition

You know where the baseline loses points. Now you pull the first lever: change **which model** writes
the copy, without touching a single instruction.
