# Build and Optimize AI Agents on Microsoft Foundry


In this workshop you'll learn to build _TrailMate_ an AI agent for an enterprise retail company that can help answer customer questions in a fast, cost-effective and reliable manner - grounded in the product catalog.

You'll work through three **Core Labs**:

1. **Lab 0: Setup** - Validate your Foundry project is provisioned and setup the dev environment.
2. **Lab 1: Model Selection** - Learn about different model types and build intuition for selection based on cost, latency or balance.
3. **Lab 2: Agent Optimization** - Build TrailMate starting with a frontier model and generic instructions. Then hill climb to optimize it.

In the next 90 minutes, you will work through these labs using the Microsoft Foundry portal (low-code) and the GitHub Codespaces environment (code-first) - and build your intuition for the agentops loop and observability features in the platform.

> Let's get started by validating credentials.

## 1. Check Azure Credentials

The workshop will use Skillable-provided Azure credentials. Verify that you have non-empty values for the following. 

- **Username:** ++@lab.CloudPortalCredential(User1).Username++
- **Password (TAP):** ++@lab.CloudPortalCredential(User1).AccessToken++


>[!tip] Clicking on the values will copy them to your clipboard to paste elsewhere.

---

## 2. Skillable VM Use

You will see a Windows VM with login to the right. In this workshop, we are _not_ using the VM - instead we will use a GitHub Codespaces environment in your browser to connect to the Skillable-provisioned infra.

>[!tip] You can extend the instructions pane out to occupy more space since we are not using the VM.

---

## 3. Log into Azure Portal

In this workshop, we will work completely within the browser. Make sure you have a modern browser on your laptop - we recommend Microsoft Edge.

1. Launch the browser and open a new tab.
1. Navigate to ++https://portal.azure.com++
1. Login using the Azure credentials above
1. You should see a single resource group provisioned. **Note the resource group name** You will need this later.

>[!tip] The resource group name will look something like `rg-model-mondaysXXX`.

---

## 4. Log into Microsoft Foundry


Click on the resource group to see details. You should 4 resources listed.

1. Click on the Foundry resource to view details. You should see a `Go To Foundry` button.
1. Click on the button. You should see a new tab open in Microsoft Foundry.
1. Verify that you are logged into Foundry with the same Azure credential. You may need to sign in once and select the Skillable Azure account from the dialog.

>[!tip] The landing page should have the Foundry endpoint and API key information. We will get this using a script later.

---

## 5. Verify Model Deployments

Click on the `Build` tab in the navbar, then select the `Models` option in the sidebar.

- You should see a list of deployed models in the project.
- This should include two Claude models, two GPT models, `model-router` and `MAI-Image-2.5-Pro`.

---

## 6. Launch GitHub Codespaces

Now we need to setup our development environment. We will use GitHub Codespaces for this - you must have a personal GitHub account for this.

1. Visit ++https://aka.ms/model-mastery++
1. Log into GitHub with your personal account
1. Fork the repo to your personal profile
1. Select the blue **Code** button in your fork, then pick the **Codespaces** tab.
1. Click to create a new Codespace.

>[!tip] The GitHub Codespaces will take a while to load. Wait till you see the Visual Studio Code terminal get an active prompt.

---

✅ **Congratulations:** Your Codespaces environment is ready to use. 

➡️ **What's Next**: Open the `foundry/agent-builder/README.md` in the editor and setup your local environment by starting from **Step 5**.