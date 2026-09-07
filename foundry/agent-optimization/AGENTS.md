# Workshop maintenance guide

Use this guide for every change under `foundry/agent-optimization/`. A more
specific `AGENTS.md` deeper in the tree takes precedence for that subtree.

## Start with the learner

Write as a technical trainer guiding a professional audience. Learners
understand basic models and agents but may be new to Microsoft Foundry.

- Be clear, concise, and actionable.
- Use **we**, **we’ll**, and **let’s** to make the workshop a shared journey.
- Use **you** when asking the learner to take an action or check a result.
- Explain a technical term in everyday language the first time it appears.
- Preserve official product names, commands, deployment names, and file names.
- Prefer short paragraphs, tables, diagrams, and whitespace over walls of text.
- Use simple analogies only when they make a concept easier to remember.

Avoid internal implementation language in learner instructions. Prefer:

| Avoid | Say instead |
|---|---|
| evidence ledger | approved evidence, source facts, or evidence list |
| canonical list | complete list |
| orchestration | coordination or how the roles work together |
| deterministic | repeatable, or code-based when describing a check |
| remap | switch the model behind a stable deployment name |
| immutable | fixed snapshot; include **immutable** only when teaching the official versioning term |
| artifact | result, saved file, or example unless **artifact** is the platform term being taught |
| frontier model | larger reasoning model or more capable model |

## Keep the story in this order

The root `README.md` introduces the workshop through six learner questions:

1. **Who are you?** Define the audience.
2. **What is the objective?** Introduce the scenario and optimization target.
3. **What is our approach?** Explain hill climbing and AgentOps before tables.
4. **Prerequisites.** Separate self-guided and Skillable requirements.
5. **Getting started.** Link both delivery tracks.
6. **Lab outline.** Show how the 90-minute journey fits together.

Do not move setup details ahead of the audience, objective, and approach.

## Preserve the two-scale mental model

- **Hill climbing is the entire journey** from the measured baseline toward the
  best measured target.
- **AgentOps is the workflow for each step**: run, observe, evaluate, improve
  one lever, compare, and keep or reverse the change.

Do not use the terms as synonyms. Show the full hill first, then the repeated
AgentOps workflow used to verify each move.

The runtime architecture is a relay:

1. Brief and image
2. Campaign Coordinator
3. Product Analyst
4. Campaign Strategist
5. Campaign Copywriter
6. Claim guard
7. Image tool
8. Launch kit

Keep architecture diagrams readable. Wrap long flows into two rows, number the
steps, state how to read the rows, and avoid crossing arrows. Explain AgentOps
in a separate diagram because it surrounds the runtime; it is not another
runtime component.

## Make every module small and self-contained

Use `foundry/model-router/` as structural inspiration. Each learner page should:

1. State the scenario or goal.
2. List a small set of concrete objectives.
3. Name prerequisites and link earlier modules.
4. Break work into short steps with one clear purpose each.
5. Show the working directory before commands.
6. Put the expected result directly after the action that produces it.
7. Include a checkpoint or recovery path.
8. End with a short transition and linked next step.

Split a step when it asks the learner to understand a concept, change
configuration, run a workload, and interpret results all at once. Keep
commands copyable and keep explanation next to the command it supports.

Link every reference to another lab or module. Do not write plain “Module 07,”
“Lab 2,” or “setup” when a relative Markdown link can take the learner there.

## Maintain both delivery tracks

The concepts, sequence, and learning outcomes must stay aligned:

| Track | Environment | Resource model |
|---|---|---|
| `instructions/self-guided/` | Linux, Bash, Codespaces or Dev Container | Learner provisions Foundry resources |
| `instructions/skillable/` | Pre-provisioned Windows 11, PowerShell, VS Code | Learner does not create Azure resources |

Keep commands native to each environment. Do not copy Bash into Skillable or
PowerShell into the self-guided track. Skillable pages must retain Skillable
checkbox and replacement-token conventions.

Both tracks total 90 minutes, but their per-lab timing differs because
Skillable is pre-provisioned. Update both tracks when a concept, diagram,
terminology choice, or expected result changes.

## Protect the workshop experiment

The scenario uses the HikeMate TrailLite Daypack. Product claims must come from
`src/data/campaign-brief.md`; visual observations must remain separate from
documented product facts. Do not infer price, dimensions, weight, capacity,
water resistance, materials, warranty, or included accessories from the image.

Keep these experiment controls unchanged unless the workshop design itself is
being revised:

- The Campaign Copywriter is the only Agent Optimizer target.
- Change one lever at a time.
- Keep the evaluation dataset and rubric fixed between comparisons.
- Review optimizer candidates before applying or deploying them.
- Present prepared checkpoint results as examples, never as live measurements.

## Preserve the Foundry architecture

- Keep the five purpose-based deployment names:
  `campaign-coordinator`, `visual-understanding`, `campaign-reasoning`,
  `adaptive-copy`, and `creative-image`.
- Model Router replaces the model behind `adaptive-copy`; it does not create a
  sixth deployment.
- Keep hosted-agent code under
  `src/agents/product-launch-studio/` using the Responses protocol and direct
  code deployment.
- Keep the Agent Optimizer baseline under
  `src/agents/product-launch-studio/.agent_configs/baseline/`.
- Run project-scoped `azd` commands from `src/`, where `azure.yaml` lives.
- Prefix Foundry-related `azd` commands inline with
  `AZURE_DEV_USER_AGENT=microsoft_foundry_skill`; never persist that value.
- Never commit `.env`, `.azure/`, credentials, endpoints, operation results, or
  other generated environment state.

For Foundry agent development, deployment, evaluation, or optimization work,
load and follow the `microsoft-foundry` skill before changing commands or
architecture.

## Validate the change

Use the smallest checks that cover the edit:

```bash
python3 src/scripts/validate-assets.py --root src
(cd src/agents/product-launch-studio && python3 -m pytest tests)
```

For instruction changes, also check:

- Local Markdown links and anchors resolve.
- Every referenced module or lab is linked.
- Mermaid diagrams use GitHub-supported syntax and remain readable.
- Bash appears only in self-guided pages and PowerShell only in Skillable pages.
- Timings still total 90 minutes.
- The same concept uses the same learner-friendly term in both tracks.

Read the rendered page, not only the diff. A technically correct page is not
finished if a learner cannot quickly see what to do, why it matters, and what
success looks like.
