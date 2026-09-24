"""Create a Foundry agent that queries a Fabric data agent, as a persisted prompt agent.

The agent is created in the project, queried once, and deleted again unless KEEP_AGENT=true.

    pip install -r requirements.txt
    az login                      # user identity - service principals are not supported
    python prompt_agent.py "Which store is underperforming, and since when?"
"""

import os
import sys

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    FabricDataAgentToolParameters,
    MicrosoftFabricPreviewTool,
    PromptAgentDefinition,
    ToolProjectConnection,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
MODEL = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini")
CONNECTION_NAME = os.environ["FABRIC_CONNECTION_NAME"]
AGENT_NAME = os.environ.get("AGENT_NAME", "demo-fabric-agent")
KEEP_AGENT = os.environ.get("KEEP_AGENT", "false").lower() == "true"

# Tool routing lives here. Without it the model happily answers from general
# knowledge and never calls Fabric - the most common demo failure.
INSTRUCTIONS = os.environ.get(
    "AGENT_INSTRUCTIONS",
    "You are a retail analytics assistant. "
    "For any question about sales, revenue, margin, stores, products or customers, "
    "you MUST use the Fabric data agent tool - never answer from memory. "
    "Answer in at most five sentences, always quote the figures you used, "
    "and say so explicitly when the data does not support a conclusion.",
)


def main() -> int:
    question = " ".join(sys.argv[1:]) or input("Question: ")

    credential = DefaultAzureCredential()
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)

    connection = project.connections.get(CONNECTION_NAME)
    print(f"Fabric connection: {connection.id}")

    agent = project.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=INSTRUCTIONS,
            tools=[
                MicrosoftFabricPreviewTool(
                    fabric_dataagent_preview=FabricDataAgentToolParameters(
                        project_connections=[
                            ToolProjectConnection(project_connection_id=connection.id)
                        ]
                    )
                )
            ],
        ),
    )
    print(f"Agent ready (name={agent.name}, version={agent.version})")

    try:
        openai = project.get_openai_client(agent_name=agent.name)
        # tool_choice="required" guarantees the Fabric call for a scripted demo.
        # Drop it if you want to show the model deciding on its own.
        response = openai.responses.create(tool_choice="required", input=question)
        print(f"\nQ: {question}\nA: {response.output_text}")
    finally:
        if KEEP_AGENT:
            print(f"\nAgent kept: {agent.name} (v{agent.version})")
        else:
            project.agents.delete_version(
                agent_name=agent.name, agent_version=agent.version
            )
            print("\nAgent version deleted (set KEEP_AGENT=true to keep it)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
