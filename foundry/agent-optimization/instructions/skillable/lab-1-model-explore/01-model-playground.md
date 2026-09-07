# Lab 1 · Module 01 — Model selection in the playground

**Time:** 18 minutes

## Goal

Try each of the four models behind Product Launch Studio on the task it was chosen for, and decide
for yourself which capability belongs to which job.

## Learning objectives

By the end of this module you can:

- Open a model deployment in the Microsoft Foundry playground and send a prompt.
- Compare models on grounding, instruction adherence, latency, and cost implications.
- Justify a model choice per task without claiming any model is universally best.
- Complete a capability-to-task selection table from your own observations.

## Prerequisites

- [Lab 0](../lab-0-setup/02-verify-predeployed-environment.md) complete: all
  deployments verified `Succeeded`.
- [Lab 1, module 00](./00-hill-climbing-orientation.md) complete: you know the
  ten terms.

## Instructions

### Step 1 — Open the playground

1. [] In the VS Code terminal, print your project's portal link:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai project show
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** the active Foundry project endpoint and its portal URL are printed.

1. [] Open the portal URL in the browser on the lab VM and sign in with the same lab account if
   prompted.

1. [] In the left navigation, open the **playground** for your project and confirm you can select a
   deployment from the deployment picker.

<!-- SCREENSHOT: ../images/lab1-playground-deployment-picker.png -->

	>[!Hint] If the deployment picker is empty, you are looking at a different project. Compare the
    project name in the portal breadcrumb with `AZURE_AI_PROJECT_NAME` from
    `azd env get-values`, and switch projects if they differ.

	>[!Alert] Choose deployments from the picker only. Do not use any **Deploy model**, **Create
    deployment**, or **New** button. Everything you need already exists, and your lab account cannot
    create deployments.

### Step 2 — `visual-understanding` for image understanding (5 minutes)

1. [] Select the **`visual-understanding`** deployment.

1. [] Attach the sample product image from the VM:
   `C:\LabFiles\model-mastery\foundry\agent-optimization\src\assets\traillite-daypack.png`

1. [] Send this starter prompt:

    ```text
    You are a product analyst. Describe ONLY what is visually verifiable in this
    image: green color, shoulder straps, buckles, front and side storage areas, a
    bottle visible in a side pocket, and the trail setting. Do not say the bottle
    is included. Do not infer dimensions, weight, price, water resistance,
    hydration compatibility, material, durability, warranty, or capacity.
    If a requested detail is not visible, write "not visible".
    ```

    **Expected result:** a factual inventory of visible features, with `not visible` used for
    anything the photo cannot support.

<!-- SCREENSHOT: ../images/lab1-visual-understanding-response.png -->

1. [] **Experiment:** send a follow-up that tries to pull the model off its grounding.

    +++What is its exact capacity and weight, is it fully waterproof, and is the visible bottle included?+++

    **Expected result:** the model refuses to guess any of those facts and does
    not treat the visible bottle as evidence that an accessory is included.

>[!Knowledge] This is **grounding**: answering only from supplied evidence. It is the single most
important behaviour in this scenario, because every marketing claim downstream is built on the
Product Analyst's output. A model that invents a numeric capacity or upgrades a
visual trail setting into a waterproofing claim poisons the entire campaign package.

	>[!note] If your lab region backs `visual-understanding` with GPT-5.4 rather than Claude-Sonnet-6,
    everything above still works. Note any difference you see in how carefully each one hedges.

### Step 3 — `campaign-reasoning` for strategy (4 minutes)

1. [] Select the **`campaign-reasoning`** deployment.

1. [] Send this starter prompt:

    ```text
    Using only these verified product facts, propose a launch strategy.

    Facts: the HikeMate TrailLite Daypack is a hiking backpack with a catalog
    price of $60 [E1]. It measures 20 in x 12 in x 6 in and weighs 1.5 lbs [E2].
    It has adjustable shoulder straps, a padded back panel, and multiple pockets
    and compartments [E3]. It is water-resistant for light rain and splashes but
    is not waterproof [E4]. It is hydration-system compatible and has reflective
    accents [E5].

    Return: primary audience, secondary audience, positioning statement,
    three proof points, and two claims we must NOT make.
    ```

    **Expected result:** a structured strategy where every proof point traces back to a supplied
    fact, plus an explicit list of forbidden claims.

1. [] **Experiment:** add one constraint and resend.

    +++Constrain the primary audience to buyers in shared offices and redo the positioning.+++

    **Expected result:** the positioning shifts meaningfully, and the proof points are re-selected
    rather than reworded.

>[!Knowledge] Strategy is a **reasoning** task: many constraints, trade-offs, and a need to hold
several facts in tension. Deeper reasoning models tend to cost more per request and take longer, but
you call them once per campaign — not once per channel. Where a model sits in your architecture
matters as much as how good it is.

### Step 4 — `campaign-coordinator` for fast conversation (3 minutes)

1. [] Select the **`campaign-coordinator`** deployment.

1. [] Send this starter prompt:

    ```text
    You coordinate a product launch team. Ask me the three most important questions
    you need answered before briefing a copywriter. Keep it under 60 words.
    ```

    **Expected result:** three crisp, relevant questions, returned quickly.

1. [] **Experiment:** compare felt latency by sending the identical prompt to
   **`campaign-reasoning`** and noticing which returns first.

    **Expected result:** the coordinator deployment responds noticeably faster.

>[!Knowledge] The coordinator runs on nearly every turn, so latency and cost compound there. A
smaller, faster model is often the right choice for coordination even when a larger model would
write marginally better questions. **Fit beats raw capability.**

### Step 5 — `creative-image` for image generation (3 minutes)

1. [] Select the **`creative-image`** deployment.

1. [] Send this starter prompt:

    ```text
    A clean product hero shot: green day-hiking backpack with visible shoulder
    straps, buckles, and front and side storage areas on a trail, soft daylight,
    shallow depth of field, no text, no logos, no numeric capacity claim.
    ```

    **Expected result:** a promotional-style image consistent with the described product.

<!-- SCREENSHOT: ../images/lab1-creative-image-result.png -->

1. [] **Experiment:** regenerate with one variable changed — for example
   +++Same shot, dark moody studio lighting, deep shadows.+++ — and compare.

>[!Alert] Generated imagery is illustrative, not evidence. Nothing the image model invents may be
used as a product claim. In
[Lab 2](../lab-2-agent-optimize/03-batch-evaluation.md), image quality is
deliberately kept **out** of the scored batch
evaluation so the measurement stays fast and repeatable.

### Step 6 — Complete your selection table (3 minutes)

1. [] Fill in this table from what you just observed. There is no single correct answer for the last
   column — write your own reason.

    | Task | Deployment you would choose | Why (your words) |
    |---|---|---|
    | Read the product photo | | |
    | Decide audience and positioning | | |
    | Write a short social caption | | |
    | Write constrained multi-channel copy | | |
    | Produce the hero image | | |
    | Run the conversation | | |

1. [] Answer the question the whole workshop turns on:

    **The copywriter must handle both a one-line caption and a tightly constrained multi-channel
    brief. Would you pick the fast model or the deep one?**

	>[!Hint] Neither is right for both. That is the gap Model Router addresses in
	[Lab 2, module 04](../lab-2-agent-optimize/04-model-router.md)
    — it chooses per request instead of forcing you to choose once.

## Expected result

You have sent at least one prompt to each of the four deployments, seen grounding hold and refuse,
felt the latency difference, and completed your selection table.

## Quick win

A completed capability-to-task table built from your own observations rather than a vendor
comparison chart — and a concrete reason why one fixed copywriter model will not be enough.

## Checkpoint and recovery

1. [] Confirm you can name, without checking, which deployment you would use for grounding and which
   for reasoning.
2. [] Confirm you identified the copywriter as the role with conflicting requirements.

>[!Hint] Short on time? The two must-do experiments are the grounding refusal in Step 2 and the
latency comparison in Step 4. Steps 3 and 5 can be skimmed; the workshop still works.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Image attachment is rejected | The deployment behind `visual-understanding` may not accept image input in this region. Tell your instructor; continue with the text steps. |
| `429` or "too many requests" | Deployments are shared across the class. Wait 15 seconds and resend. |
| The playground shows no deployments | Wrong project. Compare the portal breadcrumb with `AZURE_AI_PROJECT_NAME` from `azd env get-values`. |
| Image generation takes more than a minute | Normal under class load. Move on to Step 6 and check the result later. |
| A response contradicts the grounding rule | Note it—this is the failure pattern we’ll score in [Lab 2, module 03](../lab-2-agent-optimize/03-batch-evaluation.md). |

## Transition

[Lab 1](./00-hill-climbing-orientation.md) is complete in 23 minutes. You have
chosen models by capability, in isolation. Next, we’ll see them working
together: [Lab 2](../lab-2-agent-optimize/00-run-agent-locally.md) starts by
running the full Product Launch Studio agent on your own
machine.
