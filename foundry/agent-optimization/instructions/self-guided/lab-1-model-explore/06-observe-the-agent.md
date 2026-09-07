# 06 · Observe what the agent actually did

⏱️ **Time:** 8 minutes

## 🎯 Goal

Turn the agent from a black box into something you can inspect: which role ran, which model answered, how long it took, and where the tokens went.

## Objectives

- Stream logs for a live agent session.
- Find your agent's traces in Application Insights.
- Read one conversation end to end and attribute spans to roles.
- Capture the latency and token numbers that make
  [Lab 2](../lab-2-agent-optimize/README.md) meaningful.

## ✅ Prerequisites

- [Module 05](./05-deploy-and-version.md) complete: an active agent version.
- At least one invocation sent in
  [Module 05](./05-deploy-and-version.md), Step 5.
- `ENABLE_MONITORING=true` was set during provisioning, so Application Insights exists.

<br/>

## 🔢 Steps

### Step 1 — Generate something worth looking at (1 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent invoke --new-session \
  "Produce the full TrailLite Daypack launch kit: headline, 60-word paragraph, three social posts, and a hero image prompt. Cite the brief line behind every product-record/manual claim and label visual observations separately."
```

Use `--new-session` so this conversation is easy to find.

### Step 2 — Watch the session logs (2 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd ai agent monitor
```

`monitor` streams logs for the session your last invoke used. This is your first stop for *"it failed and I do not know why."* Stop the stream with `Ctrl+C`.

### Step 3 — Find the telemetry resource (1 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value APPLICATIONINSIGHTS_CONNECTION_STRING
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_RESOURCE_GROUP
```

Agent traces follow the [GenAI OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/): one span per model call and per tool call, with attributes such as `gen_ai.operation.name`, `gen_ai.request.model`, and token counts.

### Step 4 — Read one conversation (3 min)

Open **[ai.azure.com](https://ai.azure.com)**, select your project, and look for the **tracing / observability** experience — Foundry surfaces agent traces alongside the project rather than at a fixed menu path. Open the most recent conversation and expand the span tree.

Answer these four questions from the trace:

| Question | Where to look |
|---|---|
| How many model calls did one launch request take? | Count the model spans |
| Which span used `adaptive-copy`? | The model/deployment attribute on each span |
| Which span was slowest? | Span duration |
| Did the image tool run? | The tool-call span |

> 📚 Reference: [Observability in Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/observability) and [trace agents](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/trace-agents-sdk).

### Step 5 — Record the "before" picture (1 min)

Fill this in. It is qualitative on purpose:
[Module 07](../lab-2-agent-optimize/07-baseline-evaluation.md) supplies the
numbers; this table supplies the shape.

| Observation | Your value |
|---|---|
| Model calls per launch request | |
| Slowest role | |
| Role that consumed the most output tokens | |
| Did the claim guard send any copy item back for a rewrite? | |

<br/>

## 📤 Expected result

- `azd ai agent monitor` streamed logs for your session.
- You opened one trace and can name the span that used `adaptive-copy`.
- You have a rough latency/token profile for a single launch request.

## 🏆 Quick win

Point at the span that used `adaptive-copy` and say: *"that one span is the only thing I am going to change for the rest of the workshop."* Scoping an optimization to a single, observable span is what makes the result attributable instead of anecdotal.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** you have seen at least one trace or log stream from your deployed agent.

| If… | Do this |
|---|---|
| Traces have not appeared yet | Telemetry ingestion lags by a minute or two. Re-run Step 1, wait, refresh. |
| Application Insights is missing | `ENABLE_MONITORING` was false. Set it in `$WORKSHOP_ROOT/.env`, then from `$WORKSHOP_SRC` re-run `./scripts/configure-environment.sh --env-file ../.env --apply` and `./scripts/provision.sh --env-file ../.env --apply`. |
| You are over budget | `azd ai agent monitor` alone satisfies the checkpoint. Move on—[Module 07](../lab-2-agent-optimize/07-baseline-evaluation.md) does not depend on the portal. |
| The portal layout does not match | Expected; Foundry evolves. Search the project for tracing, or query Application Insights directly in the Azure portal. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `monitor` shows nothing | No active session | Run an invoke first, then `monitor`; or pass `--session-id`. |
| No traces at all | Connection string not injected | Confirm `APPLICATIONINSIGHTS_CONNECTION_STRING` in `azd env get-values`, then redeploy. |
| Spans lack model attributes | Older instrumentation | Ensure the agent's requirements include `azure-monitor-opentelemetry` and redeploy. |
| Cannot open the resource | Missing reader role on the resource group | Ask your subscription admin for Reader on `AZURE_RESOURCE_GROUP`. |

## ➡️ Next

You can see what the agent does. Now measure how *well* it does it — and stop trusting your eyes.

**[Module 07 — Baseline evaluation](../lab-2-agent-optimize/07-baseline-evaluation.md)** · ⬆️ [Lab 1](./README.md)
