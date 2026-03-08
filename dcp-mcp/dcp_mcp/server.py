"""DCP-MCP server — FastMCP application wiring.

Run with::

    python -m dcp_mcp.server

Or register in your MCP client config::

    {
        "mcpServers": {
            "dcp": {
                "command": "python",
                "args": ["-m", "dcp_mcp.server"],
                "cwd": "/path/to/dcp-mcp"
            }
        }
    }
"""

from __future__ import annotations

import json
import logging

from fastmcp import FastMCP

from dcp_mcp.config import load_config
from dcp_mcp.resources import DCP_USAGE_PROMPT, list_template_resources, read_template_resource
from dcp_mcp.store import LocalPolicyStore
from dcp_mcp.tools import (
    check_policy_freshness,
    fetch_policy,
    generate_dcp_block,
    list_available_policies,
    validate_dcp_header_tool,
)

logger = logging.getLogger("dcp_mcp")

# ── Bootstrap ────────────────────────────────────────────────────────────

config = load_config()
store = LocalPolicyStore(config.templates_path, mode=config.mode)
mcp = FastMCP(config.server_name)


# ── MCP Tools ────────────────────────────────────────────────────────────

@mcp.tool()
def fetch_policy_tool(document_type: str) -> str:
    """Look up the review checklist, drafting standards, and policy metadata
    for a document type.  Supports fuzzy matching — "NDA", "non-disclosure",
    and "nda" all resolve to a Non-Disclosure Agreement template."""
    result = fetch_policy(store, document_type)
    return json.dumps(result, indent=2)


@mcp.tool()
def validate_dcp_header(header_text: str) -> str:
    """Validate a DCP block.  Pass the text of a document's DCP block
    (with or without the ═ delimiters).  Returns errors, warnings, and
    all successfully parsed fields."""
    result = validate_dcp_header_tool(header_text)
    return json.dumps(result, indent=2)


@mcp.tool()
def check_policy_freshness_tool(document_type: str, policy_version: str) -> str:
    """Check whether a document's embedded policy version is still current.
    Pass the document type and the Policy Version value from the document's
    DCP block.  Returns whether the version matches, how many days since
    the last update, and a human-readable message."""
    result = check_policy_freshness(store, document_type, policy_version)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_available_policies_tool() -> str:
    """List all available document types with their current policy version
    and last-updated date.  Useful for orientation on first connection."""
    result = list_available_policies(store)
    return json.dumps(result, indent=2)


@mcp.tool()
def generate_dcp_block_tool(document_type: str) -> str:
    """Generate a pre-populated DCP block for a document type.  Returns the
    full DCP block text (with delimiters) extracted from the matching
    template.  Use this when helping a user create a new document."""
    result = generate_dcp_block(store, document_type)
    return json.dumps(result, indent=2)


# ── MCP Resources ────────────────────────────────────────────────────────

@mcp.resource("templates://list")
def templates_list() -> str:
    """List all available DCP templates."""
    resources = list_template_resources(store)
    return json.dumps(resources, indent=2)


@mcp.resource("templates://{name}")
def templates_read(name: str) -> str:
    """Read the full text of a DCP template."""
    return read_template_resource(store, f"templates://{name}")


# ── MCP Prompts ──────────────────────────────────────────────────────────

@mcp.prompt()
def dcp_usage_guide() -> str:
    """How to use the DCP policy tools effectively."""
    return DCP_USAGE_PROMPT


# ── Entry point ──────────────────────────────────────────────────────────

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
    template_count = len(store.list_templates())
    if template_count:
        logger.info("Loaded %d template(s) from %s", template_count, config.templates_path)
    else:
        logger.info("No templates loaded. Set TEMPLATES_PATH to your templates directory.")
    mcp.run()


if __name__ == "__main__":
    main()
