# Cleanup

Run these commands from the workshop `src` directory, the azd project root.

Cleanup is intentionally two-step and destructive only after confirmation.

```bash
./scripts/cleanup.sh
./scripts/cleanup.sh --apply
```

The preview lists the selected resource group and resources. Apply requires
typing `DELETE` and runs `azd down --purge --force`. This removes the Foundry
account/project, all five deployments, hosted-agent versions managed by the
environment, Application Insights data, and Log Analytics workspace.

Before deletion:

- export only evaluation or trace artifacts your organization permits;
- record real optimizer operation/candidate IDs if needed;
- verify the active azd environment and resource group;
- confirm no shared resources were added to the workshop group;
- assign one person responsibility for completing cleanup.

After deletion, verify the resource group is gone in Azure. Remove local
untracked `.env`, copied `eval.yaml`, `.azure/` state, and downloaded result
artifacts as appropriate. Never commit those files if they contain identifiers,
telemetry, or secrets.

PowerShell:

```powershell
./scripts/cleanup.ps1
./scripts/cleanup.ps1 -Apply
```

Reference: [azd down](https://learn.microsoft.com/azure/developer/azure-developer-cli/reference#azd-down)
