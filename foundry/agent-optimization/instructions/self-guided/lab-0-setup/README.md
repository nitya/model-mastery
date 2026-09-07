# Lab 0 — Setup · 15 minutes

**Base camp.** You cannot climb a hill until you are standing on it. This lab puts a working Foundry project under your feet and gives you the map.

## Modules

| # | Module | Time | Goal |
|---|---|---|---|
| 01 | [Provision the workshop environment](./01-provision-environment.md) | 10 min | A Foundry project, five model deployments, verified locally |
| 02 | [Orientation: the studio and the hill](./02-orientation.md) | 5 min | Understand the scenario, the four roles, and the measurement rules |

## What "done" looks like

- `azd env get-values` prints a real `AZURE_AI_PROJECT_ENDPOINT`.
- Five deployments exist: `campaign-coordinator`, `visual-understanding`, `campaign-reasoning`, `adaptive-copy`, `creative-image`.
- You can explain, in one sentence, why `adaptive-copy` is the only deployment that changes later.

## If you are short on time

[Module 01](./01-provision-environment.md) is the only module in the workshop
you cannot skip—everything after it needs a live project.
[Module 02](./02-orientation.md) is reading, so we can continue while Azure
finishes provisioning.

➡️ Start with [Module 01](./01-provision-environment.md) · ⬆️ [Self-guided index](../README.md) · 🏠 [Workshop overview](../../../README.md)
