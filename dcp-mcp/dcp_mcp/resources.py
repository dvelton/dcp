"""MCP resource definitions for DCP-MCP.

Exposes DCP templates as MCP resources under the ``templates://`` URI
scheme.  AI clients can list available templates and read their full text.
"""

from __future__ import annotations

from dcp_mcp.store import LocalPolicyStore


def list_template_resources(store: LocalPolicyStore) -> list[dict[str, str]]:
    """Return resource descriptors for all templates in the store.

    Each descriptor includes a URI, name, description, and MIME type
    suitable for registration with an MCP server.
    """
    templates = store.list_templates()
    resources = []
    for t in templates:
        resources.append({
            "uri": f"templates://{t.file_name}",
            "name": t.document_type,
            "description": f"DCP template: {t.document_type}",
            "mimeType": "text/markdown",
        })
    return resources


def read_template_resource(store: LocalPolicyStore, uri: str) -> str:
    """Read the full text of a template identified by its URI.

    The URI format is ``templates://<filename>`` where ``<filename>`` is the
    stem of the template file (no extension).
    """
    # Strip the scheme
    name = uri.removeprefix("templates://").strip("/")

    # Try to find the file by stem across supported extensions
    templates = store.list_templates()
    for t in templates:
        if t.file_name == name:
            return store.get_template_content(str(t.file_path))

    raise FileNotFoundError(f"No template found for URI: {uri}")


# ── MCP Prompt ───────────────────────────────────────────────────────────

DCP_USAGE_PROMPT = """You are connected to a DCP (Document Context Protocol) policy server. \
This server gives you access to your organization's document review standards, \
drafting policies, and validation tools.

How to use the DCP tools effectively:

1. When reviewing a document, start by calling `fetch_policy` with the document type \
   (e.g., "NDA", "DPA", "Vendor Assessment"). This returns the review checklist and \
   drafting standards that apply. Use these criteria to guide your analysis.

2. When a document contains a DCP block, call `validate_dcp_header` with the block text \
   to check for structural issues, missing fields, or notation problems.

3. When a document's DCP block includes a Policy Version field, call `check_policy_freshness` \
   to verify whether the embedded policy is still current.

4. Call `list_available_policies` to see all document types the server knows about, \
   along with their current versions and last-updated dates.

5. When helping a user create a new document, call `generate_dcp_block` with the \
   document type to get a pre-populated DCP block they can embed at the top of \
   their document.

Do NOT attempt to compare a document against a policy standard yourself and then \
call a tool to "confirm" your analysis. The correct workflow is: fetch the policy \
first, then apply it to the document. The tools provide the standards; you perform \
the analysis.
"""
