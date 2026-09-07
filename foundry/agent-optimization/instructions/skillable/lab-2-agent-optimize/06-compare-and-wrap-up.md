# Lab 2 · Module 06 — Compare results and wrap up

**Time:** 5 minutes

## Goal

Score the optimized version, complete the three-row scorecard, and state what each lever bought you
and why this loop is hill climbing.

## Learning objectives

By the end of this module you can:

- Compare three agent versions on one frozen dataset and rubric.
- Attribute each score change to the single lever that caused it.
- Describe the AgentOps workflow end to end.
- Name the next lever you would pull and how you would prove it worked.

## Prerequisites

- [Lab 2, module 05](./05-agent-optimizer.md) complete: **v-optimized**
  deployed, or the prepared example reviewed and labelled.
- Baseline and router scores recorded.

## Instructions

### Step 1 — Score the optimized version (2 minutes)

1. [] Run the same evaluation one last time — same dataset, same rubric:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    New-Item -ItemType Directory -Force .\.foundry\results | Out-Null
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent eval run
    azd ai agent eval show -O .\.foundry\results\my-optimized-results.json
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** a third scored run written to file.

	>[!Hint] Short on time, no live optimized version, or the run is queued? Use the explicitly
    labelled instructor-prepared example and mark it in your
    scorecard:
    ```powershell
    Get-Content .\checkpoints\evaluation\optimized-results.example.json
    ```
    Its values are illustrative, not live measurements.

1. [] Optionally list all three runs together:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent eval list
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

### Step 2 — Complete the scorecard (2 minutes)

1. [] Fill in every cell from your scratch file.

    | Version | Lever changed | Overall | Evidence fidelity | Task adherence | Copywriter latency |
    |---|---|---|---|---|---|
    | **v-cta** — baseline | Fixed `adaptive-copy` | | | | |
    | **v-cta** — improvement 1 | Same version, routed `adaptive-copy` | | | | |
    | **v-optimized** — improvement 2 | Router + optimized instructions | | | | |

<!-- SCREENSHOT: ../images/lab2-scorecard-comparison.png -->

1. [] Answer the four attribution questions:

    1. [] Which lever produced the larger quality gain?
    2. [] Did either lever cost latency, and was that trade acceptable?
    3. [] Did any criterion get **worse** while the overall score rose?
    4. [] Would you promote **v-optimized** to production, and what evidence supports that?

	>[!Alert] Answer question 3 seriously. An overall score can rise while grounding falls. In this
    scenario that is a regression regardless of the headline number, because unsupported product
    claims are a compliance problem, not a quality preference.

>[!Knowledge] This is why the levers were pulled **one at a time**. If you had switched to the router
and rewritten the instructions in the same step, you would have a better agent and no idea which
change earned it — and no way to undo the half that hurt.

### Step 3 — Name the loop (1 minute)

1. [] Trace what you actually did:

    ```mermaid
    flowchart LR
        R["Run<br/>module 00"] --> D["Deploy and version<br/>module 01"]
        D --> O["Observe traces<br/>module 02"]
        O --> E["Evaluate<br/>module 03"]
        E --> L1["Lever 1: Model Router<br/>module 04"]
        L1 --> L2["Lever 2: Agent Optimizer<br/>module 05"]
        L2 --> C["Compare and decide<br/>module 06"]
        C -.->|next iteration| O
    ```

1. [] Say it out loud in one sentence: *establish a baseline, observe, evaluate, change one lever,
   measure again, keep what wins.*

1. [] Name the next lever you would pull if you had another hour, and how you would prove it worked.

	>[!tip] Good candidates for a second iteration: grow the evaluation dataset from real recorded
    traces, tighten the rubric on the criterion that stayed weakest, or move the router experiment to
    a different role such as the strategist.

## What you learned

- **[Lab 0](../lab-0-setup/00-welcome.md)** — you verified a pre-provisioned Foundry project, its purpose-based deployments, and a
  running hosted agent, and read a green preflight report.
- **[Lab 1](../lab-1-model-explore/00-hill-climbing-orientation.md)** — you compared four models on the tasks they were chosen for and built a
  capability-to-task selection table from your own observations.
- **[Lab 2](./00-run-agent-locally.md)** — you ran a four-role agent locally, deployed a fixed version, read a trace, scored
  a baseline, and improved it twice with one lever at a time.

**Ideas worth keeping:**

| Idea | Why it matters |
|---|---|
| Purpose-based deployment names | Swap models without touching code |
| Fixed agent versions | Before-and-after comparison stays honest |
| Traces tell you where, evaluations tell you whether | Two different questions, two different tools |
| Frozen dataset and rubric | The only way scores stay comparable |
| One lever at a time | The only way a gain is attributable |
| Human review before apply | Optimizers search; people decide |

## Expected result

A completed three-row scorecard, an attribution for each score change, and a stated promotion
decision with evidence.

## Quick win

A finished before-and-after scorecard and your own explanation of the AgentOps
workflow—two results you can take straight back to your team.

## Checkpoint and recovery

```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
Get-ChildItem .\.foundry\results\my-*.json | Select-Object Name, Length
```

**Expected result:** your baseline, router, and optimized result files are listed.

>[!Hint] **Recovery.** Any row you could not measure live can be filled from the explicitly labelled
examples in `checkpoints\evaluation\`. Use them only to practise the comparison and mark those rows
**prepared example**; they are not live measurements.

## Troubleshooting

| Symptom | Fix |
|---|---|
| The optimized run scores below the router run | A legitimate outcome. The right decision is not to promote it. Record why. |
| One of the three runs is missing | Use the matching `*.example.json` file in `checkpoints\evaluation\` and mark the row **prepared example**. |
| Scores differ noticeably between class members | Expected. Judge-model scores can vary, and class load changes over time. Compare the **direction and size** of change, not absolute values. |
| You need the original fixed mapping for a rerun | Restart the disposable Skillable lab or ask the instructor to restore its initial azd environment. The router script intentionally has no fixed-mode switch. |

## Transition

The workshop is complete — 90 minutes from model selection to a measured agent improvement. Nothing
needs cleaning up: the lab environment is disposed of when your Skillable session ends, and you
never created a resource.

To run the same journey in your own Azure subscription, follow the self-guided track in
[`../../self-guided/`](../../self-guided/), which provisions everything from scratch on Linux with
Bash.

**Further reading**

- [Microsoft Foundry hosted agents](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry)
- [Model Router in Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/model-router)
- [Evaluate generative AI applications](https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai)
- [Tracing in Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/trace)

Thank you for attending.
