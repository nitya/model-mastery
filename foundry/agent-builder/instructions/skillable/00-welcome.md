# From Model Selection to Agent Optimization with Microsoft Foundry

Building your first AI agent feels simple. But keeping that agent running in a reliable and cost-effective manner gets more challenging. Model choices are exploding driving new cost and capability tradeoffs. Real-world usage can reveal edge use cases or new requirements for quality and performance. And, we need constant vigilance to ensure safe and secure operation. This is where end-to-end observability and continuous optimization become necessary. Microsoft Foundry makes it seamless.

In this 90-minute workshop, we'll take you on a journey from plan to production as we build _TrailMate_ an AI agent that helps you find the right gear for your next outdoor adventure. The journey has three stages.

**Stage 1: Setup** / Get familiar with Foundry

- Explore the default Microsoft Foundry project
- Create a test agent and try a sample prompt
- Understand agent lifecycle and observability

**Stage 2: Model Selection** / Meet the Models

- Explore chat completion, reasoning and vision capabilities
- Learn to compare models by cost, quality and latency
- Use model router to auto-select the right model for the task

**Stage 3: Agent Optimization** / Improve the Agent

- Use traces and insights to understand issues
- Build a rubric evaluator to measure outcomes
- Use agent optimizer to start "hill climbing"

By the end of the workshop, you'll have built your intuition for the agentops loop for continuous optimization. And, you will leave with a sandbox you can use to continue exploring more models and optimization levers in Foundry - at your own pace.

---

## Check Azure Credentials

We will use Skillable-provided Azure credentials in this lab. Take a look at the username and password below and make sure they are non-empty values. We will make use of these soon.

**Username:** +++@lab.CloudPortalCredential(User1).Username+++
**Password (TAP):** +++@lab.CloudPortalCredential(User1).AccessToken+++

---

## Login into VM

We will use the Windows VM seen to the left of this screen - specifically, we will be using the built-in browser with GitHub Codespaces as the runtime environment for this lab. Click on the VM screen now and use these credentials to login.

**Username:** +++@lab.VirtualMachine(Windows11).Username+++   
**Password:** +++@lab.VirtualMachine(Windows11).Password+++


---

✅ **In this step:** You learned the objectives and logged into VM.

➡️ **What's Next**: You'll launch a browser & setup the environment