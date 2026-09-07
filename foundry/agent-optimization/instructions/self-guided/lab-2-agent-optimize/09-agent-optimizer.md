# 09 · Agent Optimizer

⏱️ **Time:** 5 minutes to start and inspect · the job itself runs longer

## 🎯 Goal

Let Agent Optimizer propose better copywriter instructions against the **same** dataset and rubric — and practise the discipline of reviewing candidates instead of applying them.

## Objectives

- Confirm the agent is optimization-ready (baseline config + SDK wiring).
- Start an optimization job scoped to the copywriter's instructions.
- Read candidate results — from your job if it finishes, from the prepared checkpoint results if it does not.
- Understand exactly why nothing is applied automatically.

## ✅ Prerequisites

- [Module 07](./07-baseline-evaluation.md) complete: a recorded baseline.
- [Module 08](./08-model-router-swap.md) done or explicitly skipped — you should know which model is behind `adaptive-copy` right now.
- Terminal at `$WORKSHOP_SRC`.

<br/>

## 🧠 What the optimizer does (30 seconds)

You have been climbing by hand: change one thing, re-measure, keep or revert. Agent Optimizer runs that loop for you — it generates candidate configurations, evaluates each against your dataset and rubric, and ranks them. It is a **guide that scouts several steps**, not an autopilot. You still choose the step. Agent Optimizer is in preview; if a flag differs from these notes, trust `azd ai agent optimize --help`.

<br/>

## 🔢 Steps

### Step 1 — Confirm the agent is optimizable (1 min)

```bash
cd "$WORKSHOP_SRC/agents/product-launch-studio"
ls .agent_configs/baseline/
cat .agent_configs/baseline/metadata.yaml
grep -rn "load_config" product_launch_studio/optimizer.py
grep -rn "agentserver-optimization" requirements.txt
```

Three things make this work:

| Requirement | Why |
|---|---|
| `.agent_configs/baseline/` with `metadata.yaml` + `instructions.md` | The optimizer needs a **file-based** baseline to vary, not a string in code |
| `load_config()` in `product_launch_studio/optimizer.py` | The running copywriter reads its instructions and model from that config instead of a hard-coded prompt |
| `azure-ai-agentserver-optimization` in the dependencies | The SDK that resolves the config at runtime |

**One edit before you run.** The baseline ships with a placeholder model and says so in a comment. Point it at the deployment you have actually been evaluating:

```bash
cd "$WORKSHOP_SRC/agents/product-launch-studio"
sed -i 's/^model: copywriter-fixed$/model: adaptive-copy/' .agent_configs/baseline/metadata.yaml
grep "^model:" .agent_configs/baseline/metadata.yaml
```

If that `grep` already prints `model: adaptive-copy`, you are done — the file was updated earlier.

### Step 2 — Check the optimization inputs (1 min)

```bash
cd "$WORKSHOP_SRC"
cat data/eval.yaml
```

Confirm `dataset` and `evaluators` match
[Module 07](./07-baseline-evaluation.md). Then note
`options.optimization_config.model_search_space`, which limits the optimizer to
`adaptive-copy` and `campaign-reasoning`. If they differ, stop and fix them;
otherwise we are comparing altitudes on different mountains.

The optimizer model is chosen from a small allowlist of reasoning models (GPT-5, GPT-5.1, GPT-5.2, GPT-5.4, GPT-5.5, DeepSeek-V4-Pro, DeepSeek-V-3.2). In this workshop that is your `campaign-reasoning` deployment, backed by GPT-5.4.

### Step 3 — Start the job (1 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent optimize --optimize-model campaign-reasoning
```

If it reports that the evaluation setup is missing, copy it into the agent root
as shown in [Module 07](./07-baseline-evaluation.md):
`cp data/eval.yaml agents/product-launch-studio/eval.yaml`. Then run the command
again—same file, same experiment.

Capture the **operation ID** it prints. Monitor it in a second terminal — do not block this one:

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent optimize status <operation-id> --watch
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent optimize list
```

> ⏳ **This job routinely outruns the workshop clock.** That is expected and fine: it generates candidates and evaluates each one against your full dataset. Leave it running and continue with Step 4. Cancel with `azd ai agent optimize cancel <operation-id>` if you need the quota back.

### Step 4 — Read the prepared checkpoint results (2 min)

So the lesson does not depend on job runtime, here is a completed optimization from a prior instructor run — same scenario, same dataset shape, same rubric. Read it as *how to judge candidates*, not as numbers to expect. Your instructor publishes the refreshed figures for your delivery.

| Candidate | What it changed in the copywriter instructions | Claim support | Task adherence | Verdict |
|---|---|---|---|---|
| **baseline** | — | 0.72 | 0.88 | The altitude to beat |
| **c-1** | Requires an evidence ID (E1–E5) after every measurable claim | 0.86 | 0.87 | 🟢 Strong candidate — big grounding gain, adherence flat |
| **c-2** | Adds a refusal template for claims the brief forbids | 0.81 | 0.90 | 🟡 Good, smaller grounding gain |
| **c-3** | c-1 + c-2, plus a tighter word budget | 0.85 | 0.79 | 🔴 Reject — adherence regressed; deliverables got dropped |

How to read that table — the same way you would read your own:

1. **Look at the constraint first.** Claim support is the hard requirement; adherence and latency are trade-offs.
2. **Reject regressions even when the headline number improves.** `c-3` looks fine if you only read column one.
3. **Prefer the smallest change that wins.** `c-1` is one sentence of instruction. Small diffs are reviewable, explainable, and cheap to revert.
4. **A small delta on a small dataset is not a result.** Anything inside noise needs more cases before you promote it.

### Step 5 — Do not apply anything yet (30 seconds)

When your job completes, the flow is **review, then decide** — never auto-apply:

```bash
# AFTER the workshop, and only after you have read the candidate diff:
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent optimize apply --candidate <candidate-id>
git diff -- agents/product-launch-studio/.agent_configs/    # read every line
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd deploy      # only if you accept it
```

Why applying locally and deploying beats one-shot deployment of a candidate:

- The change lands as a **reviewable diff** in source control.
- Your teammates can see *why* the instructions say what they say.
- Rollback is `git revert` plus `azd deploy`, not archaeology.
- Applying instructions you have not read is how a prompt injection or a subtly loosened claim rule reaches production.

<br/>

## 📤 Expected result

- An optimization job started, with its operation ID captured (it may still be running).
- You can name which prepared candidate you would promote and which you would reject, with a reason.
- Nothing has been applied or deployed.

## 🏆 Quick win

`c-1` in the table is a **one-sentence** instruction change that moves the constraint you care about most. The takeaway to carry back to your team: most agent quality problems are not model problems — they are unstated-requirement problems, and the cheapest fix is to state the requirement.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** you can articulate the promote/reject decision rule — quality constraint first, no regressions, smallest diff.

| If… | Do this |
|---|---|
| The job is still running at the end of the workshop | Expected. Note the operation ID and check later with `optimize status <id>`. |
| The job fails to start | Verify `.agent_configs/baseline/metadata.yaml` names a real deployment (`adaptive-copy`, not `copywriter-fixed`) and that the eval contract validates (`azd ai agent doctor`). |
| `--optimize-model` is rejected | The deployment must be backed by an allowlisted optimizer model. Confirm `campaign-reasoning` is GPT-5.4, and check `azd ai agent optimize --help`. |
| You are tempted to apply a candidate now | Don’t. Finish [Module 10](./10-wrap-up.md), then apply with the diff in front of you. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Optimization requires a baseline config` | `.agent_configs/baseline/` missing or empty | Restore it in the agent source directory beside `main.py`. |
| Candidates all score the same as baseline | The optimizer had nothing to vary | Confirm the copywriter really reads its instructions via `load_config()` in `product_launch_studio/optimizer.py`. |
| `eval_config_invalid` | `eval.yaml` failed validation | `azd ai agent doctor`, fix the named field. |
| Job cancelled or timed out | Quota pressure from concurrent evaluation runs | Re-run when the [Module 08 evaluation](./08-model-router-swap.md) finishes. |
| Applied a candidate by accident | It only changed local files | `git checkout -- agents/product-launch-studio/.agent_configs/` — nothing reaches Foundry until `azd deploy`. |

## ➡️ Next

Three steps taken. Time to decide what you keep — and to shut the meter off.

**[Module 10 — Wrap-up and next steps](./10-wrap-up.md)** · ⬆️ [Lab 2](./README.md)
