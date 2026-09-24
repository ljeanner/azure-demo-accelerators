"""Same thing, as an ephemeral in-process agent built with the Microsoft Agent Framework.

Nothing is persisted in the project, so you can rerun this as often as you like
without cleaning anything up. Ideal for rehearsing.

    pip install -r requirements.txt
    az login                      # user identity - service principals are not supported
    python hosted_agent.py "What changed in the Garden category over the last six months?"
"""

import asyncio
import os
import sys

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
CONNECTION_NAME = os.environ["FABRIC_CONNECTION_NAME"]

INSTRUCTIONS = os.environ.get(
    "AGENT_INSTRUCTIONS",
    "You are a retail analytics assistant. "
    "For any question about sales, revenue, margin, stores, products or customers, "
    "you MUST use the Fabric data agent tool - never answer from memory. "
    "Answer in at most five sentences and always quote the figures you used.",
)

QUESTIONS = [
    "What was total revenue last quarter, by region?",
    "Which store is underperforming, and since when?",
    "What changed in the Garden category over the last six months?",
]


async def main() -> None:
    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else QUESTIONS

    credential = AzureCliCredential()
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    connection_id = project.connections.get(CONNECTION_NAME).id
    print(f"Fabric connection: {connection_id}\n")

    agent = Agent(
        client=FoundryChatClient(credential=credential),
        instructions=INSTRUCTIONS,
        tools=[FoundryChatClient.get_fabric_tool(connection_id=connection_id)],
    )

    for question in questions:
        print(f"Q: {question}")
        result = await agent.run(question)
        print(f"A: {result.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
