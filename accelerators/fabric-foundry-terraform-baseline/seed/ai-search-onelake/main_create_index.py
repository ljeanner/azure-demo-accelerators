"""Seed script: build the Azure AI Search index from a Microsoft Fabric lakehouse.

This module owns everything related to building the Azure AI Search index on top
of a OneLake (Microsoft Fabric) lakehouse: data source, index, skillset and
indexer creation, plus running and polling the indexer. Run it once at startup
to seed the index::

    uv run python main_create_index.py

The search service reads the lakehouse files directly through its
system-assigned managed identity (which must hold at least Contributor on the
Fabric workspace), so there is nothing to upload. The ``agents`` project does
not import from this module; it consumes the resulting index through the same
environment variables.
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import aiohttp
from azure.core.exceptions import HttpResponseError
from azure.identity.aio import DefaultAzureCredential
from azure.search.documents.indexes.aio import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    IndexerExecutionResult,
    SearchIndexer,
    SearchIndexerSkillset,
    SearchIndexerStatus,
)
from dotenv import load_dotenv

# Load configuration from a local ``.env`` file (when present) into
# ``os.environ`` so the variables below are read the same way locally and in
# the cloud.
load_dotenv()

logger = logging.getLogger(__name__)


def get_required_env(name: str) -> str:
    """Return the environment variable ``name`` or raise if it is missing."""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable '{name}'.")
    return value


API_VERSION = os.environ.get("API_VERSION", "2025-11-01-preview")
# Microsoft Entra scope used to call the Azure AI Search data/management plane.
SEARCH_TOKEN_SCOPE = "https://search.azure.com/.default"

# --- Azure AI Search ---
SEARCH_ENDPOINT = get_required_env("SEARCH_ENDPOINT")

# --- Microsoft Fabric lakehouse (OneLake data source) ---
# The OneLake indexer reads the lakehouse through the search service's
# system-assigned managed identity, so no connection secret is required. Both
# GUIDs come from the lakehouse URL:
#   https://<host>/groups/<FABRIC_WORKSPACE_ID>/lakehouses/<FABRIC_LAKEHOUSE_ID>
FABRIC_WORKSPACE_ID = get_required_env("FABRIC_WORKSPACE_ID")
FABRIC_LAKEHOUSE_ID = get_required_env("FABRIC_LAKEHOUSE_ID")

# --- Azure OpenAI (embeddings) ---
AOAI_ENDPOINT = get_required_env("AOAI_ENDPOINT")
EMBEDDING_DEPLOYMENT = get_required_env("EMBEDDING_DEPLOYMENT")
EMBEDDING_DIMENSIONS = int(os.environ.get("EMBEDDING_DIMENSIONS", "3072"))

# --- Object names ---
KNOWLEDGE_SOURCE_NAME = get_required_env("AI_SEARCH_KNOWLEDGE_SOURCE_NAME")

DATA_SOURCE_NAME = f"{KNOWLEDGE_SOURCE_NAME}-datasource"
INDEX_NAME = f"{KNOWLEDGE_SOURCE_NAME}-index"
SKILLSET_NAME = f"{KNOWLEDGE_SOURCE_NAME}-skillset"
INDEXER_NAME = f"{KNOWLEDGE_SOURCE_NAME}-indexer"
SEMANTIC_CONFIGURATION_NAME = f"{KNOWLEDGE_SOURCE_NAME}-semantic-configuration"

INDEXER_POLL_INTERVAL_MS = int(os.environ.get("INDEXER_POLL_INTERVAL_MS", "5000"))
# Default budget: 360 * 5s = 30 min. The initial full indexing (embedding every
# lakehouse file) can easily exceed 10 minutes before the run completes.
INDEXER_POLL_ATTEMPTS = int(os.environ.get("INDEXER_POLL_ATTEMPTS", "360"))

# When true, the indexer state is reset before running so every file is
# reprocessed. When false (default), the run is incremental: the OneLake
# indexer's built-in change detection only ingests new or modified files.
RESET_INDEXER = os.environ.get("RESET_INDEXER", "false").lower() in (
    "1",
    "true",
    "yes",
)

# ``reset_indexer`` returns before the reset is fully applied, so an immediate
# ``run_indexer`` can briefly fail with HTTP 409. Retry the start a few times
# instead of pausing for an arbitrary fixed delay.
RESET_RUN_MAX_ATTEMPTS = 5
RESET_RUN_RETRY_INTERVAL_MS = 1000

# Statuses that mean an indexer execution has finished an indexing run.
TERMINAL_EXECUTION_STATUSES = ("success", "transientFailure")
# Tolerance applied when matching an execution to the run we triggered, to
# absorb minor clock skew between this client and the search service.
RUN_MATCH_TOLERANCE = timedelta(seconds=30)

# Directory that holds the AI Search JSON templates (data source, index,
# skillset, indexer). Lives in ``data``.
TEMPLATE_DIR = Path(__file__).resolve().parent / "data"

# Values substituted into the ${VAR} placeholders of the JSON templates.
TEMPLATE_VARIABLES: dict[str, str] = {
    "KS_NAME": KNOWLEDGE_SOURCE_NAME,
    "FABRIC_WORKSPACE_ID": FABRIC_WORKSPACE_ID,
    "FABRIC_LAKEHOUSE_ID": FABRIC_LAKEHOUSE_ID,
    "AOAI_ENDPOINT": AOAI_ENDPOINT,
    "EMBEDDING_DEPLOYMENT": EMBEDDING_DEPLOYMENT,
    "EMBEDDING_DIMENSIONS": str(EMBEDDING_DIMENSIONS),
}

# A single async credential is shared by every client. ``DefaultAzureCredential``
# tries several sources in order (environment, managed identity, Azure CLI, ...).
credential = DefaultAzureCredential()
# ``index_client`` manages indexes/knowledge sources, ``indexer_client`` manages
# data sources, skillsets and indexers. Both are async clients and are closed in
# ``create_search_index`` once the pipeline finishes.
index_client = SearchIndexClient(SEARCH_ENDPOINT, credential, api_version=API_VERSION)
indexer_client = SearchIndexerClient(
    SEARCH_ENDPOINT, credential, api_version=API_VERSION
)


async def create_search_index() -> None:
    """Build the OneLake -> Azure AI Search index pipeline end to end.

    Applies the data source, index, skillset and indexer, then resets and runs
    the indexer against the Microsoft Fabric lakehouse.
    """
    logger.info("🚀 Building Azure AI Search index ...")
    logger.info("Search service   : %s", SEARCH_ENDPOINT)
    logger.info("Index            : %s", INDEX_NAME)
    logger.info("Fabric workspace : %s", FABRIC_WORKSPACE_ID)
    logger.info("Fabric lakehouse : %s", FABRIC_LAKEHOUSE_ID)

    try:
        # 1. Declare the four AI Search objects from the JSON templates:
        #    data source (which lakehouse to read), index (target schema),
        #    skillset (chunking + embeddings) and indexer (the pipeline tying
        #    them together).
        logger.info("Applying data source, index, skillset and indexer...")
        await apply_data_source()
        await apply_index()
        await apply_skillset()
        await apply_indexer()

        # 2. Run the indexer and wait until the run completes. By default this
        #    is incremental (only new/changed files); set RESET_INDEXER=true to
        #    clear the state and reprocess every file.
        logger.info(
            "%s indexer '%s'...",
            "Resetting and running" if RESET_INDEXER else "Running (incremental)",
            INDEXER_NAME,
        )
        run_requested_at = await reset_and_run_indexer()
        logger.info("Waiting for indexer completion...")
        await wait_for_indexer(run_requested_at)

        logger.info("Azure AI Search index '%s' is ready.", INDEX_NAME)
    finally:
        # Async SDK clients hold network sessions that must be closed explicitly.
        await index_client.close()
        await indexer_client.close()
        await credential.close()


# The four ``apply_*`` helpers each load a JSON template from ``data/``, fill in
# its ${VAR} placeholders and create-or-update the matching AI Search object.
# They are idempotent: running them again simply updates the existing object.
#
# The data source and index are sent with a raw REST PUT because the ``onelake``
# data source type and the preview API surface aren't fully modelled by the
# stable SDK.
async def _search_rest_put(resource_path: str, body: dict, *, query: str = "") -> None:
    """PUT a JSON object to the Azure AI Search management plane via REST."""
    token = (await credential.get_token(SEARCH_TOKEN_SCOPE)).token
    url = f"{SEARCH_ENDPOINT}/{resource_path}?api-version={API_VERSION}{query}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, json=body) as response:
            if response.status not in (200, 201, 204):
                detail = await response.text()
                raise RuntimeError(
                    f"PUT {resource_path} failed with HTTP {response.status}: {detail}"
                )


async def _search_rest_delete(resource_path: str) -> None:
    """DELETE an Azure AI Search object via REST (ignores 404)."""
    token = (await credential.get_token(SEARCH_TOKEN_SCOPE)).token
    url = f"{SEARCH_ENDPOINT}/{resource_path}?api-version={API_VERSION}"
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status not in (204, 404):
                detail = await response.text()
                raise RuntimeError(
                    f"DELETE {resource_path} failed with HTTP "
                    f"{response.status}: {detail}"
                )


async def apply_data_source() -> None:
    """Render the data source template and create/update it via REST."""
    # The data source tells the indexer which Fabric workspace/lakehouse to read
    # through the search service's system-assigned managed identity. The data
    # source ``type`` is immutable, so any pre-existing data source of a
    # different type (e.g. ``adlsgen2``) must be deleted before it can be
    # recreated as ``onelake``. The indexer is deleted first because it holds
    # change-tracking state tied to the old data source (it is recreated from
    # its template by ``apply_indexer``).
    await _search_rest_delete(f"indexers/{INDEXER_NAME}")
    await _search_rest_delete(f"datasources/{DATA_SOURCE_NAME}")
    body = render_template("onelake-datasource.json")
    await _search_rest_put(f"datasources/{DATA_SOURCE_NAME}", body)
    logger.info("datasources/%s updated.", DATA_SOURCE_NAME)


async def apply_index() -> None:
    """Render the index template and create/update it via REST."""
    # The index defines the target schema (fields, vector + semantic config).
    # ``allowIndexDowntime`` lets schema settings be updated on an existing
    # index.
    body = render_template("onelake-index.json")
    await _search_rest_put(
        f"indexes/{INDEX_NAME}", body, query="&allowIndexDowntime=true"
    )
    logger.info("indexes/%s updated.", INDEX_NAME)


async def apply_skillset() -> None:
    """Render the skillset template and create/update it via the SDK."""
    # The skillset enriches documents during indexing (e.g. split into chunks
    # and generate embeddings via the Azure OpenAI deployment).
    body = render_template("onelake-skillset.json")
    await indexer_client.create_or_update_skillset(SearchIndexerSkillset(body))
    logger.info("skillsets/%s updated.", SKILLSET_NAME)


async def apply_indexer() -> None:
    """Render the indexer template and create/update it via the SDK."""
    # The indexer ties data source + skillset + index together and performs the
    # actual ingestion when triggered.
    body = render_template("onelake-indexer.json")
    await indexer_client.create_or_update_indexer(SearchIndexer(body))
    logger.info("indexers/%s updated.", INDEXER_NAME)


async def reset_and_run_indexer() -> datetime | None:
    """Reset indexer state and start a fresh execution.

    Returns the UTC time marker used later to identify the completion record
    that belongs to this specific run, or ``None`` when an execution is
    already in progress.
    """
    status = await indexer_client.get_indexer_status(INDEXER_NAME)
    # If a run is already in progress, don't start a competing one; let the
    # caller wait for the existing execution instead.
    if get_active_execution(status) is not None:
        logger.info(
            "Indexer '%s' is already running. Waiting for the active "
            "invocation to finish.",
            INDEXER_NAME,
        )
        return None

    # A full reset clears the change-tracking state so the next run reprocesses
    # everything from scratch. Skipped by default so the run stays incremental
    # (delta) and only new or modified files are ingested.
    if RESET_INDEXER:
        await indexer_client.reset_indexer(INDEXER_NAME)

    if not await start_indexer_after_reset():
        return None

    # Record when we triggered the run so ``wait_for_indexer`` can later match
    # the correct execution record.
    logger.info("Indexer '%s' triggered.", INDEXER_NAME)
    return datetime.now(timezone.utc)


async def start_indexer_after_reset() -> bool:
    """Start the indexer once the reset has been applied.

    ``reset_indexer`` returns as soon as the request is accepted (HTTP 204),
    before the reset is fully propagated, so an immediate ``run_indexer`` can
    briefly fail with HTTP 409. Retry the start while the service still reports
    that transient conflict instead of pausing for a fixed amount of time.
    Returns ``False`` when another run is already in progress.
    """
    for attempt in range(1, RESET_RUN_MAX_ATTEMPTS + 1):
        try:
            await indexer_client.run_indexer(INDEXER_NAME)
            return True
        except HttpResponseError as error:
            if error.status_code != 409:
                raise
            # A 409 means a run is already in progress. The status history can
            # lag behind (eventual consistency), so it may not list the active
            # execution yet. Retry a few times to ride out the reset
            # propagation; if the conflict persists, trust the 409 and let the
            # caller wait for the in-progress run instead of failing.
            status = await indexer_client.get_indexer_status(INDEXER_NAME)
            if get_active_execution(status) is not None:
                logger.info(
                    "Indexer '%s' is already running. Waiting for the active "
                    "invocation to finish.",
                    INDEXER_NAME,
                )
                return False
            if attempt == RESET_RUN_MAX_ATTEMPTS:
                logger.info(
                    "Indexer '%s' still reports an invocation in progress. "
                    "Waiting for it to finish.",
                    INDEXER_NAME,
                )
                return False
            await asyncio.sleep(RESET_RUN_RETRY_INTERVAL_MS / 1000)
    return False


async def wait_for_indexer(run_requested_at: datetime | None) -> None:
    """Poll the indexer status until the triggered run succeeds or fails."""
    for attempt in range(1, INDEXER_POLL_ATTEMPTS + 1):
        status = await indexer_client.get_indexer_status(INDEXER_NAME)

        overall_status = status.status or "unknown"
        active_execution = get_active_execution(status)
        # Pick which execution record represents "our" run:
        #  - if we triggered it, match the one started around that time;
        #  - if another run is active, keep waiting (no completed record yet);
        #  - otherwise fall back to the most recent finished execution.
        if run_requested_at is not None:
            completed_execution = find_completed_execution(status, run_requested_at)
        elif active_execution is not None:
            completed_execution = None
        else:
            completed_execution = find_latest_completed_execution(status)

        if completed_execution is not None:
            execution_status = completed_execution.status or overall_status
            # Treat the run as successful only when it succeeded with zero failed
            # items and no item-level errors.
            if (
                execution_status == "success"
                and (completed_execution.failed_item_count or 0) == 0
                and len(completed_execution.errors or []) == 0
            ):
                logger.info(
                    "Indexer completed with status '%s' (processed %s item(s)).",
                    execution_status,
                    completed_execution.item_count or 0,
                )
                return

            raise RuntimeError(
                format_indexer_failure(
                    INDEXER_NAME, execution_status, completed_execution
                )
            )

        if active_execution is not None:
            processed = active_execution.item_count or 0
            logger.info(
                "Indexer execution status: %s, processed %s item(s) "
                "(%s/%s). Overall indexer status: %s.",
                active_execution.status or "inProgress",
                processed,
                attempt,
                INDEXER_POLL_ATTEMPTS,
                overall_status,
            )
        else:
            logger.info(
                "Indexer overall status: %s, latest execution not available "
                "yet (%s/%s).",
                overall_status,
                attempt,
                INDEXER_POLL_ATTEMPTS,
            )

        await asyncio.sleep(INDEXER_POLL_INTERVAL_MS / 1000)

    raise RuntimeError(f"Indexer '{INDEXER_NAME}' did not finish in time.")


def render_template(template_file: str) -> dict:
    """Load a JSON template from ``TEMPLATE_DIR`` and substitute ${VAR}."""
    template_path = TEMPLATE_DIR / template_file
    template = template_path.read_text(encoding="utf-8")

    # Called for every ${VAR} match; fails fast if a placeholder has no value.
    def replace(match: re.Match[str]) -> str:
        variable_name = match.group(1)
        if variable_name not in TEMPLATE_VARIABLES:
            raise RuntimeError(
                f"Missing template variable '{variable_name}' for {template_file}."
            )
        return TEMPLATE_VARIABLES[variable_name]

    # Replace every ${UPPER_CASE} placeholder, then parse the result as JSON.
    rendered = re.sub(r"\$\{([A-Z0-9_]+)\}", replace, template)
    return json.loads(rendered)


def _executions(status: SearchIndexerStatus) -> list[IndexerExecutionResult]:
    """Return indexer executions, most recent first."""
    # Prefer the full history; fall back to the single last result, or nothing.
    if status.execution_history:
        return list(status.execution_history)
    if status.last_result is not None:
        return [status.last_result]
    return []


def get_active_execution(
    status: SearchIndexerStatus,
) -> IndexerExecutionResult | None:
    """Return the currently in-progress execution, if any."""
    for execution in _executions(status):
        if (execution.status or "") == "inProgress":
            return execution
    return None


def find_completed_execution(
    status: SearchIndexerStatus, run_requested_at: datetime
) -> IndexerExecutionResult | None:
    """Return the finished execution that belongs to the triggered run."""
    for execution in _executions(status):
        # Skip executions that haven't reached a terminal state yet.
        if (execution.status or "") not in TERMINAL_EXECUTION_STATUSES:
            continue
        start_time = execution.start_time
        if start_time is None:
            continue
        # Match by start time (minus a tolerance for clock skew) so we don't
        # accidentally pick up an older run.
        if start_time >= run_requested_at - RUN_MATCH_TOLERANCE:
            return execution
    return None


def find_latest_completed_execution(
    status: SearchIndexerStatus,
) -> IndexerExecutionResult | None:
    """Return the most recent finished execution, if any."""
    for execution in _executions(status):
        if (execution.status or "") in TERMINAL_EXECUTION_STATUSES:
            return execution
    return None


def format_indexer_failure(
    indexer_name: str,
    execution_status: str,
    execution: IndexerExecutionResult,
) -> str:
    """Build a detailed error message for a failed indexer execution."""
    lines = [
        f"Indexer '{indexer_name}' did not complete successfully "
        f"(status '{execution_status}')."
    ]
    if execution.error_message:
        lines.append(f"Error message: {execution.error_message}")
    if execution.failed_item_count:
        lines.append(f"Failed items: {execution.failed_item_count}.")
    for error in (execution.errors or [])[:5]:
        key = error.key or "<no key>"
        lines.append(f"  - [{key}] {error.error_message}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Script entry point: configure logging and drive the async pipeline from a
    # fresh event loop.
    logging.basicConfig(level=logging.INFO)
    asyncio.run(create_search_index())
