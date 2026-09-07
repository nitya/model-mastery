# Prepared checkpoints

Run the commands below from the workshop `src` directory, the azd project root.

These reviewable, instructor-authored checkpoints keep the optimization exercise
moving if a live job exceeds the workshop window. They are deliberately marked
`prepared-workshop-checkpoint`; scores and remote operation IDs are null.

Review the two instruction checkpoints side by side; they are not complete agent
source snapshots and should not be copied over the hosted agent. A live Agent
Optimizer candidate always takes precedence:

```powershell
Set-Location 'C:\LabFiles\model-mastery\foundry\agent-optimization\src'
Get-Content .\checkpoints\00-baseline\instructions.md
Get-Content .\checkpoints\01-evidence-optimized\instructions.md
azd ai agent optimize --optimize-model $(azd env get-value OPTIMIZER_MODEL_DEPLOYMENT)
azd ai agent optimize status <operation-id> --watch
azd ai agent optimize apply --candidate <candidate-id>
```

Applying or deploying requires participant review. Never invent a candidate ID.

`evaluation\*.example.*` files are instructor-prepared teaching examples, not
service output or live measurements. Learner-local `azd ai agent eval show -O`
output belongs in `src\.foundry\results\`, created before export.
