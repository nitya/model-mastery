# 07 · Baseline evaluation

⏱️ **Time:** 12 minutes

## 🎯 Goal

Measure your altitude. Produce scores for the current agent on a fixed dataset with a fixed rubric, so every later change can be judged instead of admired.

## Objectives

- Inspect the evaluation contract: dataset, evaluators, and models.
- Run a batch evaluation against the deployed agent.
- Read the results and identify the weakest dimension.
- Record a baseline you will not change for the rest of the workshop.

## ✅ Prerequisites

- [Module 05](../lab-1-model-explore/05-deploy-and-version.md) complete: an active agent version, and you wrote the version down.
- `adaptive-copy` still backed by **GPT-5.4-mini** — do not run Module 08 first.
- Terminal at `$WORKSHOP_SRC`.

<br/>

## 🔢 Steps

### Step 1 — Look at the mountain before you measure it (2 min)

```bash
cd "$WORKSHOP_SRC"
cat data/eval-cases.jsonl
cat data/evaluators/campaign-quality.yaml
```

Each dataset row has a `query` (the launch task) and an `expected_behavior` (the per-case rubric: what a good answer looks like, including refusing unsupported claims). The evaluator scores responses against that rubric.

> 🧊 **Freeze point.** From here to Module 10, do not edit either file. Changing the dataset or the rubric mid-experiment moves the mountain — every score before and after becomes incomparable.

### Step 2 — Check the evaluation contract (2 min)

```bash
cd "$WORKSHOP_SRC"
cat data/eval.yaml
```

The evaluation contract lives in `data/` alongside the dataset and the rubric, because those three files are one frozen unit. You are checking four things:

| Field | Should point at |
|---|---|
| `agent.name` / `agent.model` | The agent you deployed in Module 05, scored through the `adaptive-copy` deployment |
| `dataset.local_uri` | `../../data/eval-cases.jsonl` (resolved from the agent root) |
| `evaluators` | The `campaign-quality` rubric plus the built-ins (relevance, task adherence, intent resolution, indirect attack) |
| `options.eval_model` | An existing deployment used as the judge — `campaign-reasoning` |

> 📎 **If `azd` reports that it cannot find `eval.yaml`,** it is looking in the agent root. Copy it across and re-run — the contents are identical, so the experiment stays valid:
>
> ```bash
> cd "$WORKSHOP_SRC"
> cp data/eval.yaml agents/product-launch-studio/eval.yaml
> ```
>
> As a last resort you can generate a fresh contract with `azd ai agent eval generate --dataset "$WORKSHOP_SRC/data/eval-cases.jsonl"` — but then you are on a *different* rubric, so record that in your notes.

### Step 3 — Run the baseline evaluation (5 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent eval run
```

This finalizes any pending generation, sends every dataset case to the deployed agent, and scores the responses with the judge model. It usually takes several minutes.

> ⏳ **While it runs**, read Step 6 and pre-fill the parts of the table you already know: agent version, the model behind `adaptive-copy`, and today's date.

### Step 4 — Read the results (2 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent eval show -O baseline-results.json
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent eval list
```

Open `baseline-results.json` and look for three things, in this order:

1. **The score per evaluator** — your altitude.
2. **The lowest-scoring cases** — where the hill is steepest.
3. **The *reason* text on a failure** — the judge explains itself; read at least one.

### Step 5 — Find the weakest dimension (1 min)

Sort your attention by lowest score. In this scenario the usual suspects are:

| Symptom in the results | What it usually means |
|---|---|
| Low grounding / claim-support scores | The copywriter drafts claims the brief does not support and the reviewer only partly catches them |
| Low task-adherence scores | Missing deliverables — e.g. two social posts instead of three |
| High variance across similar cases | Instructions are ambiguous; the model is guessing at intent |

Whatever is weakest is the dimension Module 09's optimizer should attack.

### Step 6 — Record the baseline (write this down)

| Field | Your value |
|---|---|
| Date / time | |
| Agent version | |
| `adaptive-copy` backed by | GPT-5.4-mini |
| Dataset | `data/eval-cases.jsonl` (frozen) |
| Rubric | `data/evaluators/campaign-quality.yaml` (frozen) |
| Judge model | `campaign-reasoning` |
| Score per evaluator | |
| Weakest dimension | |
| Failing case ids | |

<br/>

## 📤 Expected result

- An evaluation run completed against your deployed agent.
- `baseline-results.json` on disk with per-case scores and judge reasoning.
- A filled-in baseline table, and one named weak dimension.

**Reference run** — this is the *shape* of a completed baseline, not a target. Your numbers will differ by model version, region, and date; your instructor publishes numbers from their own verification run.

| Evaluator | Reference score | How to read it |
|---|---|---|
| Claim support (grounding) | 0.72 | The main headroom — unsupported claims still slip through |
| Task adherence | 0.88 | Structure is mostly right |
| Relevance | 0.91 | Rarely the problem in this scenario |

## 🏆 Quick win

Open `baseline-results.json` and read one failing case's `reason` field aloud. You now have a written, per-case explanation of *why* your agent lost points — the thing most teams try to reconstruct from memory in a review meeting three weeks later.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** you have a recorded score for at least one evaluator, tied to a specific agent version.

| If… | Do this |
|---|---|
| The run exceeds ~8 minutes | Let it continue in this terminal and start reading [Module 08](./08-model-router-swap.md). Come back for the numbers. |
| The run fails on config | `azd ai agent doctor` from `$WORKSHOP_SRC` — it validates `eval.yaml` and names the bad field. |
| You cannot complete a run at all | Use the reference table above as the baseline for the *narrative* of Modules 08–10, and label it clearly as a reference, never as your result. |
| Scores look implausibly low across the board | Check that the judge deployment (`options.eval_model`) exists and is not rate-limited. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `eval_config_invalid` | `eval.yaml` failed validation | `azd ai agent doctor`, fix the named field, re-run. |
| Dataset not found | `dataset.local_uri` is resolved relative to `eval.yaml` | Confirm the copied agent-root file still points at `../../data/eval-cases.jsonl`. |
| Every case fails identically | The agent version is not active | `azd ai agent show --output json`, redeploy if needed. |
| Judge complains it cannot verify facts | The rubric asks for real-world verification | The rubric must score against the **brief**, not the judge's own knowledge. Keep grounding scoped to `data/campaign-brief.md`. |
| Throttling / 429s mid-run | Judge and agent share quota | Re-run once; if it persists, raise capacity for `campaign-reasoning`. |

## ➡️ Next

You know your altitude. Take the first step — and change exactly one thing.

**[Module 08 — Swap in Model Router](./08-model-router-swap.md)** · ⬆️ [Lab 2](./README.md)
