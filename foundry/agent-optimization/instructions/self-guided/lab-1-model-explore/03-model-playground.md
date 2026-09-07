# 03 · Model playground — pick the right tool

⏱️ **Time:** 18 minutes

## 🎯 Goal

Run the same launch work against four different models, see where each one is genuinely better, and justify the role assignments the agent already uses.

## Objectives

- Open your project's playground and select a specific deployment.
- Compare a fast model and a frontier model on planning and on claim review.
- Use a vision-capable model to ground copy in the product sheet, with a documented fallback.
- Generate a hero image with a purpose-built image model.
- Record a comparison you can defend — model choice is optimization lever #1.

## ✅ Prerequisites

- [Module 01](../lab-0-setup/01-provision-environment.md) complete: five deployments exist.
- [Module 02](../lab-0-setup/02-orientation.md) read: you know the four roles.
- A browser signed in to the same Azure account.

<br/>

## 🔢 Steps

### Step 1 — Open the playground for *your* project (2 min)

```bash
cd "$WORKSHOP_SRC"
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_AI_PROJECT_ENDPOINT
AZURE_DEV_USER_AGENT=microsoft_foundry_skill azd env get-value AZURE_AI_PROJECT_NAME
```

Go to **[ai.azure.com](https://ai.azure.com)**, sign in with the same account, and open the project whose name matches the value above. Foundry's navigation changes often, so rather than a click-path: look for the **playground** experience and, inside it, the **deployment selector** — that dropdown lists the five deployment names you created. Selecting a deployment is how you choose which model answers.

> 📚 New to the playground? [Get started in the Foundry playground](https://learn.microsoft.com/azure/ai-foundry/quickstarts/get-started-playground).

Keep the campaign brief open in a second tab or terminal — you will paste from it:

```bash
cd "$WORKSHOP_SRC"
cat data/campaign-brief.md
```

### Step 2 — Round A · Speed and structure (4 min)

**Deployment: `campaign-coordinator` (GPT-5.4-mini)**

Paste the campaign brief, then this prompt:

```text
You are the campaign coordinator for the HikeMate TrailLite Daypack launch.
Using ONLY the brief above, produce a launch plan as a table with columns:
deliverable | channel | evidence IDs it can rely on | qualifier it must preserve.
Include exactly 5 deliverables and respect the channel constraints.
If the brief does not support a deliverable, do not invent one.
End with a list of any facts you would need but do not have.
```

Note two things: how **fast** the first token arrives, and whether the "facts I do not have" list is honest.

### Step 3 — Round B · Grounding with vision (4 min)

**Deployment: `visual-understanding` (Claude-Sonnet-6)**

This is the product analyst's job: extraction, not creativity.

```bash
cd "$WORKSHOP_SRC"
ls assets/
```

Upload `assets/traillite-daypack.png`.

```text
Here is the HikeMate TrailLite Daypack product image and the campaign brief.
Produce two sections:
"Visible in the image" — features you can actually see.
"Supported by product-record/manual evidence E1-E5" — facts from the brief,
with their evidence ID.
Then list attributes a copywriter is likely to WANT but that NEITHER source
supports. The image may show only green color, shoulder straps, buckles,
front/side storage areas, a bottle in a side pocket, and a trail setting.
Do not say the bottle is included. An image cannot establish dimensions,
weight, price, water resistance, hydration compatibility, material, durability,
warranty, or capacity. Do not guess. Do not fill gaps.
```

Claim rule 7 is the whole test here: a model that infers a numeric capacity or
water resistance from the picture has fabricated evidence. Those claims may
come only from the manual-backed ledger.

> 🔁 **Vision fallback.** If `visual-understanding` is unavailable in your region, or the partner-model Marketplace terms are not accepted for your subscription, repeat this round against **`campaign-reasoning` (GPT-5.4)**, which is also vision-capable. Note in your comparison which model you actually used — the fallback is a legitimate result, not a failure.

### Step 4 — Round C · Claim review (4 min)

**Deployment: `campaign-reasoning` (GPT-5.4), then repeat on `campaign-coordinator` (GPT-5.4-mini)**

Paste the brief, then this deliberately contaminated draft:

```text
Review this draft against the brief's claim rules. For each sentence output:
VERDICT (supported / unsupported / partially supported) + the evidence ID that
supports it, or "no supporting evidence". Do not rewrite the copy.

DRAFT:
1. The HikeMate TrailLite Daypack is a hiking backpack with a catalog price of $60.
2. Fully waterproof, so your gear stays dry in any storm.
3. A recycled, carbon-neutral pack for a greener trail.
4. Independently certified as the market's most durable 30 L pack.
5. Water-resistant for light rain and splashes, but not waterproof.
```

Sentences 2, 3, and 4 are traps: an explicitly forbidden weather claim, an
unsupported environmental claim, and invented certification, superiority, and
capacity. Sentences 1 and 5 are supported by E1 and E4 and must be accepted —
over-refusal is also a failure. Run the **same** prompt on both deployments and
compare.

### Step 5 — Round D · Hero image (3 min)

**Deployment: `creative-image` (MAI-Image-2.5)**

```text
A photorealistic product hero shot of a green day-hiking backpack with visible
shoulder straps, buckles, front and side storage areas, on a granite trail at
sunrise, alpine valley behind, soft rim light, shallow depth of field, no text,
no logos, no readable branding, 16:9.
```

Notice what the prompt *forbids*: text, logos, readable branding. Generated text and marks are a common source of unsupported claims sneaking into a launch kit through the back door.

### Step 6 — Record the comparison (1 min)

Fill this in for yourself — it is the evidence behind every role assignment in the agent:

| Round | Deployment used | Fast enough? | Caught the traps? | Would I use it for this role? |
|---|---|---|---|---|
| A · Planning | `campaign-coordinator` | | n/a | |
| B · Grounding | `visual-understanding` *(or fallback)* | | | |
| C · Claim review | `campaign-reasoning` | | | |
| C · Claim review | `campaign-coordinator` | | | |
| D · Hero image | `creative-image` | | n/a | |

<br/>

## 📤 Expected result

- Four deployments exercised, each on the task its role actually performs.
- A concrete difference you observed on Round C between the mini model and the frontier model on unsupported claims.
- One generated hero image.
- A filled-in comparison table.

## 🏆 Quick win

Round C, run twice, side by side. In under four minutes you have a defensible answer to "why does the reviewer role cost more than the coordinator role?" — and you produced the evidence yourself instead of quoting a leaderboard.

## 🧭 Checkpoint and recovery

**The one thing that must be true:** you can name one task where the frontier model was clearly better and one where the fast model was good enough.

| If… | Do this |
|---|---|
| You are short on time | Do Rounds A and C only. They carry the lesson; B and D are enrichment. |
| The playground is unavailable to you | Skip to [Module 04](./04-run-agent-locally.md) and run the same prompts through the local agent, which uses the same deployments. |
| A deployment is missing from the selector | It failed to provision. Re-run `./scripts/provision.sh --env-file ../.env --apply` from `$WORKSHOP_SRC`. |

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Deployment not listed in the playground | Wrong project selected, or provisioning incomplete | Match the project name from `azd env get-value AZURE_AI_PROJECT_NAME`. |
| `visual-understanding` returns an error | Partner model unavailable in region, or Marketplace terms not accepted | Use the GPT-5.4 vision fallback in Step 3 and note it. |
| Image generation is rejected | Content filter, or prompt implies real branding | Remove brand names and any request for readable text. |
| Responses truncate | Output token limit | Ask for fewer deliverables, or raise max tokens in the playground settings. |
| 403 / access denied in the portal | Signed in with a different tenant or account | Sign in with the account from `az account show`. |

## ➡️ Next

You picked models by hand. Now see them working together as one agent.

**[Module 04 — Run the agent locally](./04-run-agent-locally.md)** · ⬆️ [Lab 1](./README.md)
