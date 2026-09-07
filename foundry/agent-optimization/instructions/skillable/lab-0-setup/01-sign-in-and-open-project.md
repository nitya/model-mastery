# Lab 0 · Module 01 — Sign in and open the project

**Time:** 3 minutes

## Goal

Sign in to the lab virtual machine, open the workshop in Visual Studio Code, and sign in to Azure so
the command line can reach your Microsoft Foundry project.

## Learning objectives

By the end of this module you can:

- Open the Product Launch Studio workspace in VS Code.
- Authenticate the Azure CLI and the Azure Developer CLI on the lab VM.
- Locate the workshop root folder from a PowerShell terminal.

## Prerequisites

- The lab virtual machine has finished starting and the Windows desktop is visible.

## Instructions

### Sign in to the virtual machine

1. [] Sign in to the VM with the following credentials:

    **Username**: +++@lab.VirtualMachine(Windows11).Username+++
    **Password**: +++@lab.VirtualMachine(Windows11).Password+++

	>[!tip] Select the keyboard symbol next to the text to type it into the VM for you.

<!-- SCREENSHOT: ../images/lab0-vm-signin.png -->

### Open the workshop in Visual Studio Code

1. [] On the desktop, select the **Visual Studio Code** icon to open it.

1. [] Confirm the Explorer on the left shows the **agent-optimization** workspace containing
   `instructions`, `README.md`, `requirements.txt`, `sample.env`, and `src`. Expand `src` to see
   `agents`, `data`, `scripts`, `checkpoints`, and `azure.yaml`.

<!-- SCREENSHOT: ../images/lab0-vscode-explorer.png -->

	>[!Hint] If VS Code opens without those folders, open the project manually:
    - Select **File**, then **Open Folder**.
    - Go to `C:\LabFiles\model-mastery\foundry\agent-optimization` and select **Select Folder**.
    - If asked whether you trust the authors, choose **Yes, I trust the authors**.

	>[!Alert] Keep VS Code open for the whole workshop. Every later module runs commands from a
    terminal inside this window, at this folder.

### Open a terminal at the azd project root

1. [] Open a terminal with **Terminal** > **New Terminal**. It opens at the bottom of VS Code.

1. [] Set the stable workshop paths and enter the `src` azd project root:

    ```powershell
    $WorkshopRoot = 'C:\LabFiles\model-mastery\foundry\agent-optimization'
    $WorkshopSrc = Join-Path $WorkshopRoot 'src'
    Set-Location $WorkshopSrc
    Get-Location
    ```

    **Expected result:** the path is
    `C:\LabFiles\model-mastery\foundry\agent-optimization\src`.

	>[!Hint] Every later azd, script, agent, data, and checkpoint command runs here. The configuration
    files `sample.env` and `.env` remain one level up at the workshop root.

### Sign in to Azure

1. [] Start Azure CLI sign-in:

    +++az login+++

1. [] If a browser window opens behind VS Code, minimize VS Code from the taskbar to reach it.

1. [] Choose **Work or school account**, then select **Continue**.

<!-- SCREENSHOT: ../images/lab0-azure-account-picker.png -->

1. [] Sign in with the following credentials:

    **Azure Username**: +++@lab.CloudPortalCredential(User1).Username+++
    **TAP**: +++@lab.CloudPortalCredential(User1).AccessToken+++

1. [] Select **Yes** when asked to stay signed in, then return to VS Code.

1. [] In the terminal, accept the default subscription when prompted.

    **Expected result:** the terminal prints your subscription and tenant, and returns to the prompt.

1. [] Sign in to the Azure Developer CLI with the same account:

    +++azd auth login+++

    **Expected result:** the terminal prints `Logged in to Azure.`

>[!Knowledge] Two CLIs, two sign-ins. `az` is the general-purpose Azure CLI and is what the
Microsoft Foundry SDKs pick up through `DefaultAzureCredential`. `azd` is the Azure Developer CLI,
which owns your workshop environment, deploys agent versions, and drives Agent Optimizer. They keep
separate credential caches, so you sign in to both.

## Expected result

VS Code is open at `C:\LabFiles\model-mastery\foundry\agent-optimization`, a PowerShell terminal is
open at `$WorkshopSrc` (`...\agent-optimization\src`), and both `az` and `azd` report a signed-in account.

## Quick win

You have a single window that can read the workshop code, talk to your Foundry project, and deploy
agent versions — no other tool needed for the next 87 minutes.

## Checkpoint and recovery

Run this checkpoint before moving on:

```powershell
az account show --query "{subscription:name, user:user.name}" -o table
azd env list
```

**Expected result:** the first command names your subscription and lab user. The second lists an
environment named `workshop` marked as the default.

>[!Hint] If `azd env list` shows no default environment, select it explicitly:
```powershell
azd env select workshop
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `az` or `azd` is not recognized | Close the terminal, open a new one with **Terminal** > **New Terminal**, then `cd C:\LabFiles\model-mastery\foundry\agent-optimization\src`. |
| The sign-in browser never appears | Minimize VS Code from the taskbar. The window often opens behind it. |
| `AADSTS` error during sign-in | The access token is single-use per attempt. Re-copy the TAP with the keyboard symbol and retry `az login`. |
| Sign-in succeeds but the wrong subscription is selected | Run `az account set --subscription "<name from az account list -o table>"`. |
| VS Code shows "Restricted Mode" | Select **Manage** in the banner and choose **Trust**, otherwise Python tooling stays disabled. |

## Transition

Your tools can now reach Azure. In the next module you will confirm that everything the workshop
depends on — the models, the agent, and the data — is already deployed and healthy.
