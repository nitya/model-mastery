# Lab 2 · Module 02 — Inspect traces and metrics

**Time:** 8 minutes

## Goal

Open the trace for the invocation you just made, walk the timeline of model and tool calls, and
identify one concrete optimization opportunity from the evidence.

## Learning objectives

By the end of this module you can:

- Locate a specific agent invocation's trace in the Microsoft Foundry portal.
- Read spans for role handoffs, model calls, and tool calls.
- Read latency and token usage per span.
- Turn a trace observation into a testable hypothesis.

## Prerequisites

- [Lab 2, module 01](./01-change-and-deploy.md) complete: version **v-cta**
  deployed and invoked in the cloud.

## Instructions

### Step 1 — Stream the live log first (2 minutes)

1. [] Enter the `src` azd project root and send one invocation you can then go and find:

    ```powershell
    Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent invoke "Write LinkedIn copy for the TrailLite Daypack. Audience: weekend hikers. Tone: plain and factual. Maximum 90 words. Cite every product-record/manual claim, keep water-resistant distinct from waterproof, and make no unsupported claim."
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** a constrained LinkedIn post is returned. Note roughly how long it took.

1. [] Stream the session log for the same run:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai agent monitor
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

    **Expected result:** log lines showing the coordinator delegating and each role returning. Press
    <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop streaming.

>[!Knowledge] `azd ai agent monitor` is the fast, terminal-side view of a single session. The portal
trace is the durable, structured view: it survives the session, breaks the request into spans, and
attaches latency and token usage to each one. Use the log to notice, the trace to diagnose.

### Step 2 — Open the trace in the portal (2 minutes)

1. [] Print the project link if the browser is no longer on it:

    ```powershell
    $env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
    azd ai project show
    Remove-Item Env:\AZURE_DEV_USER_AGENT
    ```

1. [] In the Microsoft Foundry portal, open your project and go to the observability area, then
   open **Tracing**.

1. [] Find the most recent trace for `product-launch-studio` and open it.

<!-- SCREENSHOT: ../images/lab2-trace-list.png -->

	>[!Hint] If no traces appear, wait 30 to 60 seconds and refresh — telemetry export is not
    instant. If they still do not appear, confirm `APPLICATIONINSIGHTS_CONNECTION_STRING` is present
    in `azd env get-values`.

	>[!note] Portal navigation labels change between releases. If a label differs from this text, look
    for the observability or tracing entry for your project. See
    [Tracing in Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/trace).

### Step 3 — Walk the timeline (2 minutes)

1. [] Expand the trace and identify these spans:

    | Look for | What it tells you |
    |---|---|
    | The root span | Total wall-clock time for the whole request |
    | A coordinator span | Where delegation decisions were made |
    | A `visual-understanding` model call | Whether product evidence was fetched or reused |
    | A `campaign-reasoning` model call | The strategy step |
    | An `adaptive-copy` model call | **The copywriter — this is your target** |
    | A tool span | The image tool, if it ran for this request |

<!-- SCREENSHOT: ../images/lab2-trace-span-detail.png -->

1. [] Select the **`adaptive-copy`** span and record three numbers:

    - Span duration
    - Input tokens
    - Output tokens

	>[!tip] Paste these into your scratch file next to your baseline notes.
	[Module 04](./04-model-router.md) compares the
    same span after you switch the copywriter to Model Router.

### Step 4 — Find one optimization opportunity (2 minutes)

1. [] Using only what the trace shows, answer these three questions:

    1. [] Which single span consumed the largest share of total latency?
    2. [] Did any role get called more than once for this request? If so, why might that be?
    3. [] Does the copywriter span's token count look proportionate to a 90-word LinkedIn post?

1. [] Write one sentence in your scratch file in this form:

    ```text
    Hypothesis: <span> is <slow / expensive / repeated> because <reason from the trace>,
    so <lever> should improve it.
    ```

    **Expected result:** a specific, testable statement — for example, *"the copywriter span uses far
    more output tokens than a 90-word post needs, because the instructions do not enforce length, so
    tightening instructions should improve it."*

>[!Knowledge] A trace tells you **where** to look, not **whether** a fix worked. That is why the next
module builds a scored baseline: a hypothesis from one trace becomes a measured claim only when it
is tested against a fixed dataset and rubric.

>[!Alert] One trace is one sample. Do not conclude that a model is slow or a role is broken from a
single request — especially in a shared class environment where load varies minute to minute.

## Expected result

You located the trace for your own invocation, recorded latency and token usage for the
`adaptive-copy` span, and wrote one testable hypothesis.

## Quick win

You found the copywriter span and turned a vague feeling that "the copy is a bit long" into a
specific, measurable hypothesis with numbers attached.

## Checkpoint and recovery

1. [] Confirm your scratch file contains: copywriter span duration, input tokens, output tokens, and
   one hypothesis sentence.

>[!Hint] **Recovery.** If traces are not exporting in your lab instance, use the illustrative example
instead so you keep pace:
```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
Get-Content .\checkpoints\evaluation\baseline-trace-summary.example.md
```
It contains an instructor-prepared illustrative span breakdown you can reason about. It is not a
recorded trace or your own run.

## Troubleshooting

| Symptom | Fix |
|---|---|
| No traces at all | Wait 60 seconds and refresh. Then confirm `APPLICATIONINSIGHTS_CONNECTION_STRING` exists in `azd env get-values`. |
| Traces exist but spans are unnamed | You may be viewing a partially exported trace. Open a newer one. |
| Token usage is blank | Not every model surfaces usage on every span. Use span duration for your comparison instead. |
| `azd ai agent monitor` shows nothing | The session ended. Re-invoke, then start `monitor` immediately. |
| The portal navigation does not match this text | Labels shift between releases. Look for the observability or tracing entry for your project. |
| The copywriter span is missing | The request may have been answered without delegating. Re-invoke with an explicit copy request naming a channel. |

## Transition

You have a hypothesis about one span. Next you will turn opinion into a number: a batch evaluation
across a fixed dataset and rubric that gives you the baseline score for the rest of the workshop.
