# Lab 1 · Module 00 — Hill-climbing orientation

**Time:** 5 minutes

## Goal

Build the vocabulary and the mental model you need for the rest of the workshop: what each piece of
Product Launch Studio is, and what makes an improvement believable.

## Learning objectives

By the end of this module you can:

- Distinguish model, model deployment, agent, tool, agent version, trace, evaluation, AgentOps,
  Model Router, and Agent Optimizer.
- Map each capability in the scenario to the component that provides it.
- State the four rules of a controlled improvement loop.

## Prerequisites

- [Lab 0](../lab-0-setup/02-verify-predeployed-environment.md) complete:
  preflight reports `READY`.

## Instructions

### Step 1 — Learn the ten words

1. [] Read the table. Each of these appears in a later module, and mixing two of them up is the most
   common source of confusion in agent work.

    | Term | What it is | Where you meet it |
    |---|---|---|
    | **Model** | The AI itself, for example GPT-5.4 or MAI-Image-2.5 | [Lab 1 playground](./01-model-playground.md) |
    | **Model deployment** | A named, callable instance of a model in your Foundry project, for example `campaign-reasoning` | [Lab 0 verification](../lab-0-setup/02-verify-predeployed-environment.md) |
    | **Agent** | A program that uses a model to decide what to do and which tools to call | [Lab 2, module 00](../lab-2-agent-optimize/00-run-agent-locally.md) |
    | **Tool** | A function the agent can call, for example image generation | [Lab 2, module 00](../lab-2-agent-optimize/00-run-agent-locally.md) |
    | **Agent version** | A fixed snapshot of deployed agent code and configuration; changes create a new version | [Lab 2, module 01](../lab-2-agent-optimize/01-change-and-deploy.md) |
    | **Trace** | The recorded timeline of one request: spans, model calls, tool calls, latency | [Lab 2, module 02](../lab-2-agent-optimize/02-observe-traces.md) |
    | **Evaluation** | Scoring many recorded outputs against a fixed dataset and rubric | [Lab 2, module 03](../lab-2-agent-optimize/03-batch-evaluation.md) |
    | **AgentOps** | The repeatable practice of observing, evaluating, improving, and versioning a working agent | Throughout [Lab 2](../lab-2-agent-optimize/00-run-agent-locally.md) |
    | **Model Router** | A deployment that picks an underlying model per request | [Lab 2, module 04](../lab-2-agent-optimize/04-model-router.md) |
    | **Agent Optimizer** | A service that proposes and scores improved agent instructions | [Lab 2, module 05](../lab-2-agent-optimize/05-agent-optimizer.md) |

>[!Knowledge] Notice the split. **Trace** answers *what happened in this one request?* **Evaluation**
answers *how good are we across many requests?* You need both: a trace tells you where to look, an
evaluation tells you whether your fix actually worked.

### Step 2 — Map capability to component

1. [] Cover the right-hand column and try to fill it in yourself, then check.

    | The capability the scenario needs | The component that provides it | Deployment |
    |---|---|---|
    | Read a product photo and report only what is visible | Product Analyst | `visual-understanding` |
    | Decide the audience, positioning, and constraints | Campaign Strategist | `campaign-reasoning` |
    | Write short, fast, channel-specific copy | Campaign Copywriter | `adaptive-copy` |
    | Draw a promotional visual | Image generation tool | `creative-image` |
    | Run the conversation and assemble the package | Campaign Coordinator | `campaign-coordinator` |

1. [] Answer for yourself: *why is the image generator a **tool** and not a fifth agent?*

	>[!Hint] It does not reason, delegate, or hold a conversation. It takes approved evidence and
    strategy in, and returns an image. That is a function call, so it is modelled as a tool.

### Step 3 — Connect AgentOps to the hill climb

1. [] Keep the two scales clear.

    | Scale | What it means |
    |---|---|
    | **Hill climbing** | The entire journey from the measured baseline toward the target |
    | **AgentOps** | The workflow repeated for each step: run, observe, evaluate, improve, and compare |

### Step 4 — Learn one AgentOps workflow

1. [] Read the AgentOps workflow we’ll use to verify each step in
   [Lab 2](../lab-2-agent-optimize/00-run-agent-locally.md).

    ```mermaid
    flowchart TB
        subgraph TOP[" "]
            direction LR
            A["1 · Run current version"] --> B["2 · Observe<br/>read one trace"]
            B --> C["3 · Evaluate<br/>score the dataset"]
        end
        subgraph BOTTOM[" "]
            direction RL
            D["4 · Change one lever"] --> E["5 · Re-evaluate<br/>same data + rubric"]
            E --> F{"6 · Better?"}
        end
        C --> D
        F -->|yes| G["Keep the change"]
        F -->|no| H["Discard and try<br/>a different lever"]
        style TOP fill:none,stroke:none
        style BOTTOM fill:none,stroke:none
    ```

### Step 5 — Keep the four rules

1. [] Commit the four rules to memory.

    1. **One lever at a time.** Model selection or instructions — never both in one measurement.
    2. **Same dataset, same rubric.** A score is only comparable against an identical yardstick.
    3. **Baseline first.** Without a recorded starting score you cannot claim an improvement.
    4. **Review before you apply.** Nothing generated by an optimizer is deployed unread.

>[!Alert] Rule 4 is enforced in this workshop. In
[Lab 2, module 05](../lab-2-agent-optimize/05-agent-optimizer.md), we inspect
Agent Optimizer candidates and choose one deliberately. We never let the
optimizer apply or deploy a candidate on its own.

### Step 6 — Preview the scorecard

1. [] Look at the three rows you will fill in by the end of the workshop. Right now they are empty
   on purpose.

    | Version | Copywriter lever | Quality | Latency | Module |
    |---|---|---|---|---|
    | Baseline | Fixed `adaptive-copy` | *(you fill in)* | *(you fill in)* | [2 · 03](../lab-2-agent-optimize/03-batch-evaluation.md) |
    | Improvement 1 | Model Router | *(you fill in)* | *(you fill in)* | [2 · 04](../lab-2-agent-optimize/04-model-router.md) |
    | Improvement 2 | Model Router + optimized instructions | *(you fill in)* | *(you fill in)* | [2 · 05](../lab-2-agent-optimize/05-agent-optimizer.md) |

>[!tip] Keep a scratch file open in VS Code and paste your numbers into it as
you go. [Module 06](../lab-2-agent-optimize/06-compare-and-wrap-up.md) compares
all three; saving the numbers now avoids rerunning an evaluation later.

## Expected result

You can state the difference between a trace and an evaluation, name the deployment behind each
role, and explain why you change only one lever at a time.

## Quick win

A completed capability-to-component map. You can now read any later instruction and know exactly
which part of the system it touches.

## Checkpoint and recovery

Self-check — answer these three before continuing:

1. [] Which component is allowed to invent a product claim? *(None. That is the point of the
   grounding constraint.)*
2. [] What is the difference between `adaptive-copy` and GPT-5.4-mini? *(One is a deployment name in
   your project, the other is the model currently behind it.)*
3. [] If quality improves after you change two things, what have you learned? *(Nothing
   attributable.)*

>[!Hint] If any answer was not obvious, re-read Step 1. Five minutes here saves
fifteen in [Lab 2](../lab-2-agent-optimize/00-run-agent-locally.md).

## Troubleshooting

| Symptom | Fix |
|---|---|
| The terms still blur together | Anchor on the question each answers: deployment = *what do I call?*, agent = *who decides?*, trace = *what happened once?*, evaluation = *how good overall?* |
| Mermaid diagrams render as plain text | Your lab client has Mermaid rendering disabled. The numbered rules carry the same content. |

## Transition

You have the vocabulary. Next you will earn the intuition: 18 minutes in the Microsoft Foundry
playground, comparing four models on the exact tasks Product Launch Studio needs.
