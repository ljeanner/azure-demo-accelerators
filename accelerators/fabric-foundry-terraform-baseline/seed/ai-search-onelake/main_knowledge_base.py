import json
import logging
import os

from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    KnowledgeBase,
    SearchIndexKnowledgeSource,
    WebKnowledgeSource,
    WebKnowledgeSourceDomain,
    WebKnowledgeSourceDomains,
    WebKnowledgeSourceParameters,
)
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_required_env(name: str) -> str:
    """Return the environment variable ``name`` or raise if it is missing."""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable '{name}'.")
    return value


API_VERSION = os.environ.get("API_VERSION", "2025-11-01-preview")

# --- Azure AI Search (index produced by seed_ai_search/create_index.py) ---
SEARCH_ENDPOINT = get_required_env("SEARCH_ENDPOINT")

# --- Foundry IQ (knowledge base chat model) ---
FOUNDRY_ENDPOINT = get_required_env("FOUNDRY_ENDPOINT")
CHAT_MODEL_DEPLOYMENT = get_required_env("CHAT_MODEL_DEPLOYMENT")

# --- Object names (kept in sync with seed_ai_search/create_index.py via the env vars) ---
AI_SEARCH_KNOWLEDGE_SOURCE_NAME = get_required_env("AI_SEARCH_KNOWLEDGE_SOURCE_NAME")
KNOWLEDGE_BASE_NAME = get_required_env("KNOWLEDGE_BASE_NAME")

INDEX_NAME = f"{AI_SEARCH_KNOWLEDGE_SOURCE_NAME}-index"
SEMANTIC_CONFIGURATION_NAME = (
    f"{AI_SEARCH_KNOWLEDGE_SOURCE_NAME}-semantic-configuration"
)


def create_index_knowledge_source(index_client: SearchIndexClient) -> None:
    """Create the searchIndex knowledge source backed by the built index."""
    knowledge_source = SearchIndexKnowledgeSource(
        {
            "name": AI_SEARCH_KNOWLEDGE_SOURCE_NAME,
            "kind": "searchIndex",
            "description": (
                f"Knowledge source backed by the '{INDEX_NAME}' Azure AI Search index."
            ),
            "searchIndexParameters": {
                "searchIndexName": INDEX_NAME,
                "semanticConfigurationName": SEMANTIC_CONFIGURATION_NAME,
                "sourceDataFields": [{"name": "title"}, {"name": "chunk"}],
                "searchFields": [{"name": "chunk"}],
            },
        }
    )

    index_client.create_or_update_knowledge_source(knowledge_source)
    logger.info(f"Knowledge source '{AI_SEARCH_KNOWLEDGE_SOURCE_NAME}' ready.")


def create_knowledge_base(index_client: SearchIndexClient) -> KnowledgeBase:
    """Create the Foundry IQ knowledge base over the search-index source."""
    knowledge_base = KnowledgeBase(
        {
            "name": KNOWLEDGE_BASE_NAME,
            "description": (
                "Foundry IQ knowledge base over the Azure AI Search index."
            ),
            "knowledgeSources": [
                {"name": AI_SEARCH_KNOWLEDGE_SOURCE_NAME},
            ],
            "outputMode": "answerSynthesis",
            "answerInstructions": (
                "Provide a concise, citation-backed answer based on the "
                "retrieved documents."
            ),
            "models": [
                {
                    "kind": "azureOpenAI",
                    "azureOpenAIParameters": {
                        "resourceUri": FOUNDRY_ENDPOINT,
                        "deploymentId": CHAT_MODEL_DEPLOYMENT,
                        "modelName": CHAT_MODEL_DEPLOYMENT,
                    },
                }
            ],
            "retrievalReasoningEffort": {"kind": "low"},
        }
    )

    result = index_client.create_or_update_knowledge_base(knowledge_base)
    logger.info(f"Knowledge base '{KNOWLEDGE_BASE_NAME}' ready.")
    return result


def main() -> None:
    """Build the Foundry IQ knowledge base over the existing AI Search index.

    The Azure AI Search index itself is created by ``seed_ai_search/create_index.py``,
    which is run separately at startup. Here we only wire that index up as a
    knowledge source and knowledge base, reading its configuration from the
    same environment variables.
    """
    logger.info("🚀 Starting ...")
    logger.info(f"Index          : {INDEX_NAME}")
    logger.info(f"Knowledge base : {KNOWLEDGE_BASE_NAME}")

    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(
        SEARCH_ENDPOINT, credential, api_version=API_VERSION
    )

    logger.info(f"\nCreating knowledge source '{AI_SEARCH_KNOWLEDGE_SOURCE_NAME}'...")
    create_index_knowledge_source(index_client)

    logger.info(f"Creating knowledge base '{KNOWLEDGE_BASE_NAME}'...")
    knowledge_base = create_knowledge_base(index_client)

    logger.info("\nBlob → Foundry IQ setup complete.")
    logger.info(json.dumps(knowledge_base.as_dict(), indent=2, default=str))


if __name__ == "__main__":
    main()
