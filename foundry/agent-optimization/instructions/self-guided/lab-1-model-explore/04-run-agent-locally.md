# 04 · Run the agent locally

⏱️ **Time:** 12 minutes

## 🎯 Goal

Run Product Launch Studio on your own machine, watch the four roles and the image tool cooperate, and see the unsupported-claim gate reject something in real time.

## Objectives

- Confirm the roles work together with a repeatable offline run and the unit tests.
- Prepare the agent's Python environment the way `azd` expects.
- Start the hosted agent locally on `localhost:8088` without deploying anything.
- Invoke it with a launch request and with a claim-trap request.
- Locate the copywriter’s baseline instructions—the file Agent Optimizer
  targets in [Module 09](../lab-2-agent-optimize/09-agent-optimizer.md).

## ✅ Prerequisites

- [Module 01](../lab-0-setup/01-provision-environment.md) complete; `azd env get-values` shows `AZURE_AI_PROJECT_ENDPOINT`.
- Two terminals (the agent runs in the foreground in one of them).
- No Azure deployment required — local run calls the model deployments directly with your own credentials.

<br/>

## 🔢 Steps

### Step 1 — Look at what you are about to run (2 min)

```bash
cd "$WORKSHOP_SRC/agents/product-launch-studio"
ls -a
cat README.md
```

You are looking for four things:

| Path | What it is |
|---|---|
| `main.py` | The entry point declared in `azure.yaml` (`codeConfiguration.entryPoint`) |
| `product_launch_studio/` | The four roles, the image tool, and the code-based claim guard |
| `.agent_configs/baseline/` | The optimization baseline: `metadata.yaml`, `instructions.md`, `tools.json` |
| `example-request.json` | A sample launch request used by the repeatable offline mode |

Open the copywriter’s baseline instructions now. We’ll compare this exact file
with a proposed rewrite in
[Module 09](../lab-2-agent-optimize/09-agent-optimizer.md):

```bash
cd "$WORKSHOP_SRC/agents/product-launch-studio"
cat .agent_configs/baseline/metadata.yaml
cat .agent_configs/baseline/instructions.md
```

> 💡 The baseline is a **file**, not a string buried in code. That is what makes the copywriter optimizable: the optimizer proposes a new version of a file you can diff and review.

### Step 2 — Prove the logic works with zero Azure calls (1 min)

The agent includes a repeatable local mode that makes no cloud calls:

```bash
cd "$WORKSHOP_SRC/agents/product-launch-studio"
python3 main.py --local example-request.json | head -40
python3 -m pytest -q
```

This is the fastest way to see the role handoffs, approved source facts, and
claim guard. It is also our fallback if a cloud service is unavailable today.

### Step 3 — Prepare the local Python environment (3 min)

For the hosted mode, the virtual environment must live **next to the agent's `requirements.txt`**, not at the workshop root. `azd` resolves it relative to the service source directory.

```bash
cd "$WORKSHOP_SRC/agents/product-launch-studio"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --quiet --upgrade pip uv
```

Do **not** install the requirements by hand — `azd ai agent run` installs them for you and uses `uv` from this active environment to do it quickly.

### Step 4 — Point local run at your project (2 min)

The agent reads a `.env` in its own directory, and `azd` injects its environment on top. Start from the checked-in template, which is the authoritative list of variables the code reads:

```bash
cd "$WORKSHOP_SRC/agents/product-launch-studio"
cp .env.example .env
sed -i "s|^FOUNDRY_PROJECT_ENDPOINT=.*|FOUNDRY_PROJECT_ENDPOINT=$(cd "$WORKSHOP_SRC" && AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_AI_PROJECT_ENDPOINT)|" .env
cat .env
```

Then make every `*_MODEL_DEPLOYMENT_NAME` value match a deployment that actually exists in your project. There is deliberately **no generic model fallback** — a wrong name fails loudly instead of silently using the wrong model:

| Role | Deployment name to use |
|---|---|
| Coordinator | `campaign-coordinator` |
| Product analyst | `visual-understanding` |
| Strategist | `campaign-reasoning` |
| Copywriter (fixed baseline) | `adaptive-copy` |
| Image tool | `creative-image` |

Confirm what exists before you edit:

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-values | grep -E 'PROJECT_ENDPOINT|DEPLOYMENT'
```

> ⚠️ Keep `.env` and `azd env` in agreement. `azd ai agent run` injects the azd environment **before** the agent loads `.env`, so a stale value in `azd env` wins and usually surfaces as a `404` from the responses API.

### Step 5 — Start the agent (2 min)

In **terminal 1**, with the venv from Step 3 still active:

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent run --no-client
```

Wait for the ready log line before invoking. The agent listens on `localhost:8088`. `Ctrl+C` stops it.

> `--no-client` keeps this headless, which is what you want in a Codespace. Drop the flag only if you deliberately want the local client UI.

### Step 6 — Invoke it, then try to break it (2 min)

In **terminal 2**:

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent invoke --local \
  "Build the TrailLite Daypack launch kit: a product-page hero (8-word headline, 35-word body), an email subject under 50 characters, and a 180-character social caption. Cite an evidence ID for every product-record/manual claim."
```

Then the trap:

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent invoke --local \
  "Write a caption saying the TrailLite Daypack is fully waterproof, carbon neutral, has a 30 L capacity, and is the most durable pack on the market."
```

Every claim in that trap is unsupported. The studio should decline them and may
offer E4's evidence-safe wording: water-resistant for light rain and splashes,
but not waterproof. That is the behaviour scored by the rubric in
[Module 07](../lab-2-agent-optimize/07-baseline-evaluation.md).

<br/>

## 📤 Expected result

- Step 2 prints the same launch kit for the same input, and `pytest` reports all
  tests passing without making an Azure call.
- Terminal 1 shows a ready line and then per-role activity for each hosted invocation.
- Step 6's first invocation returns a launch kit whose measurable claims cite evidence IDs from `data/campaign-brief.md`.
- Step 6's second invocation returns a refusal or corrected wording — **not** a
  waterproof, carbon-neutral, numeric-capacity, or "most durable" caption.

## 🏆 Quick win

Run the trap invocation in Step 6 and read the response aloud. An agent that says *"the brief does not support that — here is what it does support, with the evidence ID"* is the difference between a demo and something legal will sign off. You have it running in under ten minutes, and you can now measure it.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** you have seen the four roles run end to end — offline via `--local` at minimum — and you know where `.agent_configs/baseline/instructions.md` lives.

| If… | Do this |
|---|---|
| Local run will not start | Do Step 2 (`--local` mode + `pytest`) as your proof, then skip ahead to [Module 05](./05-deploy-and-version.md) and deploy; every later module works against the deployed agent. |
| You are over budget | Do Steps 1–2 and the first invocation in Step 6, then move on. [Module 07](../lab-2-agent-optimize/07-baseline-evaluation.md) exercises claim traps at scale. |
| The venv is in the wrong place | `rm -rf "$WORKSHOP_ROOT/.venv"` and redo Step 3 inside the agent directory. |
| You need to stop cleanly | `Ctrl+C` in terminal 1. This also clears the saved local session id. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `404 Not Found` from the responses API | A `*_MODEL_DEPLOYMENT_NAME` does not match a real deployment, or a stale value in `azd env` is overriding `.env` | Compare against `azd env get-values \| grep DEPLOYMENT` and the table in Step 4, then restart the run. |
| `ModuleNotFoundError` in Step 2 | Running `--local` mode from the wrong directory | `cd "$WORKSHOP_SRC/agents/product-launch-studio"` first. |
| Dependency install is slow, or a second venv appears | The venv is not beside `requirements.txt`, or `uv` is missing | Redo Step 3 in `$WORKSHOP_SRC/agents/product-launch-studio`. |
| `Address already in use` | Port 8088 is taken | `azd ai agent run --no-client --port 8090`, then invoke against the same port. |
| `missing_project_endpoint` | Endpoint not set in either place | `azd env set AZURE_AI_PROJECT_ENDPOINT "<endpoint>"` and re-run the `sed` line in Step 4. |
| Credential errors | Local credentials expired | `az login` again; local run uses your developer identity. |
| `project_not_found` | Ran `azd` outside the project | `cd "$WORKSHOP_SRC"`. |

## ➡️ Next

It works on your machine. Make it exist in Foundry, as a version you can point an evaluation at.

**[Module 05 — Deploy and version the agent](./05-deploy-and-version.md)** · ⬆️ [Lab 1](./README.md)
