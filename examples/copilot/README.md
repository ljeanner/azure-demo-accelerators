# Copilot examples for the RCG hackathon

Choose the files you need for your demo, copy them into your project,
and adapt them. Nothing in this folder is enabled by default.

## Agents: choose a role

- [Architecture reviewer](agents/azure-architecture-reviewer.agent.md): review your HLD.
- [Demo builder](agents/demo-builder.agent.md): implement your scenario.
- [Demo coach](agents/demo-coach.agent.md): prepare your oral presentation.

Copy the selected files into `.github\agents\`, then select the agent in Copilot.

## Skills: complete a task

- [Prerequisites](skills/demo-preflight/SKILL.md): identify blockers before starting.
- [Integration](skills/connect-demo-integration/SKILL.md): connect a service to your application.
- [Rehearsal](skills/rehearse-demo/SKILL.md): check that the demo can be replayed.
- [PowerPoint](skills/demo-ppt/SKILL.md): prepare a five-slide demo recap.

Copy each selected folder into `.github\skills\`, then ask, for example:
"Use demo-ppt to prepare our demo presentation."
Creating a PPTX requires a compatible tool; otherwise, the skill provides the slide content.

For synthetic data in Fabric, see the separate [Fabric demo data agent skill](../../skills/fabric-demo-data-agent/SKILL.md).

## Instructions: provide context

- [Use case](instructions/use-case.instructions.md): your scenario and technology choices.
- [Azure deployment](instructions/azure-deployment.instructions.md): your environment and constraints.

Copy into `.github\instructions\`, fill in the `<< ... >>` placeholders, and adapt
`applyTo` to your project paths (glob patterns use `/`).
The [shared rules](../../.github/copilot-instructions.md) are already active in this repository.

**Getting started:** describe the use case, review the HLD, then build.
If your Copilot client does not recognize a file, attach it directly to the conversation.
