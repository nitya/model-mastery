# Screenshot manifest — Skillable track

This folder holds the screenshots referenced by the Skillable instruction modules. **No binary
screenshots are committed yet.** This file is the capture contract: what to shoot, what to name it,
and what alt text to use.

## How placeholders work

Every module carries an HTML comment at the exact point a screenshot belongs:

```markdown
<!-- SCREENSHOT: ../images/lab0-vscode-explorer.png -->
```

HTML comments render as nothing, so the instructions import and read cleanly with no broken images.
When you capture an image, **replace the comment** with the Markdown reference and the alt text from
the table below:

```markdown
![VS Code Explorer showing the agent-optimization workspace](../images/lab0-vscode-explorer.png)
```

Keep the relative `../images/` prefix — module files live one folder below this one.

## Capture standards

| Setting | Value |
|---|---|
| Source machine | The Skillable Windows 11 lab VM, at the point in the workshop where the screenshot appears |
| Resolution | 1920 × 1080, 100% display scaling |
| Format | PNG |
| Width after crop | 900–1400 px. Crop to the relevant panel; never ship a full desktop for a terminal shot. |
| Theme | VS Code **Dark+**, browser in light theme (matches the Foundry portal default) |
| Redaction | Blur or crop any subscription ID, tenant ID, resource group name, endpoint host, object ID, or learner email. Purpose-based deployment names such as `adaptive-copy` are safe to show. |
| Emphasis | One red 3 px rounded rectangle maximum per image, on the element the step names. No arrows, no numbered call-out bubbles, no text overlays. |
| Freshness | Recapture whenever the Foundry portal navigation or the `azd ai agent` output format changes. |

> Alt text is not decorative. Skillable learners use screen readers and translated instructions.
> Write what the image *shows*, not "screenshot of step 4".

## Lab 0 — Setup

| # | File name | Capture instructions | Alt text |
|--:|---|---|---|
| 1 | `lab0-vm-signin.png` | Windows 11 lock screen with the lab username pre-filled and the password field focused. Do not show a real password. | `Windows 11 sign-in screen with the lab username entered` |
| 2 | `lab0-vscode-explorer.png` | VS Code with the Explorer expanded on the `agent-optimization` workspace and `src` expanded. `agents`, `data`, `scripts`, `checkpoints`, and `azure.yaml` must all be visible under `src`. Crop to the Explorer plus the title bar. | `VS Code Explorer showing the agent-optimization workspace with the expanded src folder` |
| 3 | `lab0-azure-account-picker.png` | The `az login` account picker with **Work or school account** highlighted. Blur any pre-existing account tiles. | `Azure sign-in dialog with Work or school account selected` |
| 4 | `lab0-deployment-list.png` | Terminal output of the `az cognitiveservices account deployment list` table. All five deployment names visible, each showing `Succeeded`. Blur nothing — no identifiers appear in this table. | `Terminal table listing five model deployments, each with provisioning state Succeeded` |
| 5 | `lab0-agent-show.png` | Terminal output of `azd ai agent show --output json`, cropped to the agent name, version, and state fields. Blur the project endpoint host. | `azd ai agent show output with the product-launch-studio agent name, version, and running state` |
| 6 | `lab0-preflight-pass.png` | The full `preflight.ps1 -EnvFile ..\.env -Online` report ending with `[OK] Preflight completed without making changes.` This is the Lab 0 quick win — make it legible end to end. | `Preflight report ending with confirmation that checks completed without making changes` |

## Lab 1 — Model Explore

| # | File name | Capture instructions | Alt text |
|--:|---|---|---|
| 7 | `lab1-playground-deployment-picker.png` | The Foundry playground with the deployment picker open, showing the purpose-based deployment names. Blur the project breadcrumb. | `Foundry playground deployment picker listing the purpose-based model deployments` |
| 8 | `lab1-visual-understanding-response.png` | The playground after the grounding prompt, showing a factual feature inventory that uses `not visible` for unsupported details. Include the attached product image thumbnail. | `Playground response listing only visually verifiable product details, marking unknown attributes as not visible` |
| 9 | `lab1-creative-image-result.png` | The generated hero image beside its prompt. Crop to the image plus the prompt box. | `Generated product hero image beside the prompt used to create it` |

## Lab 2 — Agent Optimize

| # | File name | Capture instructions | Alt text |
|--:|---|---|---|
| 10 | `lab2-copywriter-instructions.png` | `.agent_configs/baseline/instructions.md` open in VS Code, scrolled to the channel and claim-constraint rules. Crop to the editor pane. | `Campaign Copywriter instructions in VS Code showing channel rules and the ban on unsupported claims` |
| 11 | `lab2-agent-run-local.png` | Terminal after `azd ai agent run --no-client`, showing the agent listening on `localhost:8088`. | `Terminal showing the local agent started and listening on localhost port 8088` |
| 12 | `lab2-local-invoke-response.png` | The local invocation response, cropped to show the product evidence section and the start of the channel copy. | `Local invocation response showing grounded product evidence followed by channel copy` |
| 13 | `lab2-copywriter-edit.png` | The VS Code editor with the added call-to-action rule visible and the file saved (no dirty dot). Highlight the added lines. | `Copywriter instructions in VS Code with the new call-to-action rule added` |
| 14 | `lab2-azd-deploy-success.png` | `azd deploy product-launch-studio` output ending in success, with the new version visible. Blur the resource group and endpoint. | `azd deploy output reporting a successfully registered new agent version` |
| 15 | `lab2-cloud-invoke-response.png` | The cloud invocation response, cropped so the explicit call to action at the end of a channel variant is legible. | `Cloud invocation response ending each channel variant with an explicit call to action` |
| 16 | `lab2-trace-list.png` | The Foundry portal tracing list with recent `product-launch-studio` traces. Blur the project name in the breadcrumb. | `Foundry portal tracing list showing recent product-launch-studio traces` |
| 17 | `lab2-trace-span-detail.png` | An expanded trace with the span tree visible and the `adaptive-copy` span selected, showing duration and token usage. **The most important image in the track — make the span names readable.** | `Expanded trace with the adaptive-copy copywriter span selected, showing duration and token usage` |
| 18 | `lab2-eval-yaml.png` | `eval.yaml` open in VS Code showing `agent`, `dataset`, `evaluators`, and `options`. Blur nothing; no secrets appear. | `eval.yaml in VS Code showing the agent, dataset, evaluators, and options sections` |
| 19 | `lab2-eval-run-summary.png` | `azd ai agent eval run` summary with the overall score and per-criterion scores. This is the Lab 2 baseline quick win. | `Evaluation run summary showing an overall score and per-criterion rubric scores` |
| 20 | `lab2-router-three-requests.png` | Terminal showing the three complexity requests and their responses, scrolled so all three prompts are visible. Shrink the font if needed. | `Terminal showing simple, moderate, and complex copy requests answered by the routed agent` |
| 21 | `lab2-router-trace-model.png` | An `adaptive-copy` trace span after its remap to Model Router, where telemetry exposes the underlying model that served the request. If your build does not surface it, capture the span with latency and token usage instead and adjust the alt text. | `Trace span for the adaptive-copy deployment after its Model Router remap, showing which underlying model served the request` |
| 22 | `lab2-optimize-submitted.png` | `azd ai agent optimize` output with the operation ID and portal URL. Blur the URL's project segment. | `azd ai agent optimize output showing the submitted operation ID` |
| 23 | `lab2-optimizer-candidates.png` | The instructor-prepared optimizer review example beside `optimizer-result.sample.json`; keep the not-live warning visible. | `Instructor-prepared optimizer review example clearly labelled as illustrative rather than live output` |
| 24 | `lab2-scorecard-comparison.png` | The three completed evaluation summaries side by side, or a filled-in scorecard. Clearly label any instructor-prepared example row. | `Completed scorecard comparing fixed, routed, and optimized configurations with prepared example rows labelled` |

## Review checklist before committing images

1. [] All 24 files present, named exactly as above, in this folder.
2. [] Every `<!-- SCREENSHOT: ... -->` comment replaced with a Markdown image reference and the alt
   text from this manifest.
3. [] No subscription ID, tenant ID, resource group, endpoint host, object ID, or learner email is
   legible in any image.
4. [] No password, access token, or connection string is visible.
5. [] Each image is under 400 KB; downscale to 1400 px wide if larger.
6. [] Every image renders in the Skillable preview at the correct step.
7. [] Portal screenshots match the current Foundry navigation as of the delivery date.
