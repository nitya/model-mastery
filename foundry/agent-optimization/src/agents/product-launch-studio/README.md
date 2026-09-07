# Product Launch Studio

Product Launch Studio is a beginner-friendly Microsoft Foundry hosted agent.
Four roles collaborate in order:

1. **Campaign Coordinator** turns the request into a launch brief.
2. **Product Analyst** extracts only facts supported by the evidence ledger.
3. **Campaign Strategist** chooses an audience, channel, and message plan.
4. **Campaign Copywriter** writes evidence-cited copy.

MAI image generation is a tool available to the copywriter. It is deliberately
not modeled as a fifth agent. A deterministic claim guard checks every copy
item before release. The orchestration code always supplies the original,
immutable evidence ledger to each handoff instead of trusting an agent to copy
it correctly.

## Local workshop run (no Azure calls)

Python 3.13 is the deployment runtime, but the deterministic core also works
on recent Python 3 versions:

```bash
python main.py --local example-request.json
```

Local mode imports no Microsoft, Azure, OpenAI, or telemetry SDK. The result is
stable and includes a `local://mai-image/...` image reference.

Run the focused tests:

```bash
python -m pytest -q
```

## Hosted Responses entry point

`main.py` uses the current official pattern:
`FoundryChatClient` + Agent Framework `Agent`/`WorkflowBuilder` +
`agent_framework_foundry_hosting.ResponsesHostServer`.

Install runtime packages:

```bash
python -m pip install -r requirements.txt
```

Set `APP_MODE=hosted` and all purpose-specific values. There is intentionally
no generic model fallback:

```text
APP_MODE=hosted
FOUNDRY_PROJECT_ENDPOINT=https://ACCOUNT.services.ai.azure.com/api/projects/PROJECT
COORDINATOR_MODEL_DEPLOYMENT_NAME=coordinator
PRODUCT_ANALYST_MODEL_DEPLOYMENT_NAME=product-analyst
CAMPAIGN_STRATEGIST_MODEL_DEPLOYMENT_NAME=campaign-strategist
COPYWRITER_DEPLOYMENT_MODE=fixed
CAMPAIGN_COPYWRITER_MODEL_DEPLOYMENT_NAME=copywriter-fixed
MAI_IMAGE_MODEL_DEPLOYMENT_NAME=mai-image-1
FOUNDRY_OPENAI_ENDPOINT=https://ACCOUNT.openai.azure.com/
```

For a Foundry model-router deployment, set
`COPYWRITER_DEPLOYMENT_MODE=routed` and
`CAMPAIGN_COPYWRITER_ROUTER_DEPLOYMENT_NAME=copywriter-router` instead. Missing
or invalid settings fail at startup with a `ConfigurationError`; fixed mode
never silently switches to routed mode, or vice versa.

Hosted execution uses `ManagedIdentityCredential`. Set
`AZURE_CLIENT_ID` only for a user-assigned managed identity. Application
Insights export is enabled when `APPLICATIONINSIGHTS_CONNECTION_STRING` is
present; otherwise standard OpenTelemetry spans remain available.

## Agent Optimizer

Only `.agent_configs/baseline/instructions.md` is an optimization target.
Runtime startup imports
`from azure.ai.agentserver.optimization import load_config` and invokes
`load_config()` with no arguments. The model deployment remains controlled by
the explicit fixed/router environment selection, and MAI tool definitions are
not optimizer targets.

`eval.yaml` points at the small local JSONL dataset. Before running an optimizer
job, replace the example deployment names in `eval.yaml` and
`.agent_configs/baseline/metadata.yaml` with deployments that exist in your
Foundry project.

## Request contract

See `example-request.json`. `evidence` is required and each item needs a
statement plus an optional source. Copy output is released only when every
message cites valid evidence IDs and risky superlatives or numeric statements
are present in the cited source text.
