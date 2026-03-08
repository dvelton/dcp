"""MCP tool implementations for DCP-MCP.

Each tool returns structured JSON.  On success the response includes
``"success": true`` and the requested data.  On failure it includes
``"success": false`` and an ``"error"`` message.  No tool raises unhandled
exceptions — all errors are caught and returned in the response payload.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from dcp_mcp.parser import validate_dcp_header as _validate_header, extract_dcp_block_text
from dcp_mcp.store import LocalPolicyStore


def _error(message: str) -> dict[str, Any]:
    return {"success": False, "error": message}


def _ok(**kwargs: Any) -> dict[str, Any]:
    return {"success": True, **kwargs}


# ── Tools ────────────────────────────────────────────────────────────────

def fetch_policy(store: LocalPolicyStore, document_type: str) -> dict[str, Any]:
    """Look up the policy for a document type and return structured data.

    Supports fuzzy matching — "non-disclosure", "NDA", and "nda" all
    resolve to a Non-Disclosure Agreement template (if one is loaded).
    """
    try:
        if not document_type or not document_type.strip():
            return _error("document_type is required.")

        meta = store.find_template(document_type)
        if meta is None:
            available = store.available_types()
            return _error(
                f"No template found for '{document_type}'. "
                f"Available types: {available}"
            )

        return _ok(
            document_type=meta.document_type,
            review_checklist=meta.review_checklist,
            drafting_standards=meta.drafting_standards,
            constraints=meta.constraints,
            policy_version=meta.policy_version,
            policy_source=meta.policy_source or str(meta.file_path),
        )
    except Exception as exc:
        return _error(f"Unexpected error: {exc}")


def validate_dcp_header_tool(header_text: str) -> dict[str, Any]:
    """Validate a DCP block and return a structured report.

    Input is the text of a document's DCP block (with or without
    delimiters).  Returns errors, warnings, and successfully parsed fields.
    """
    try:
        if not header_text or not header_text.strip():
            return _error("header_text is required.")

        result = _validate_header(header_text)
        return _ok(**result.to_dict())
    except Exception as exc:
        return _error(f"Unexpected error: {exc}")


def check_policy_freshness(
    store: LocalPolicyStore,
    document_type: str,
    policy_version: str,
) -> dict[str, Any]:
    """Compare a document's embedded policy version against the current one.

    Returns whether the version is current, the version details, and a
    human-readable message suitable for relaying to the user.
    """
    try:
        if not document_type or not document_type.strip():
            return _error("document_type is required.")
        if not policy_version or not policy_version.strip():
            return _error("policy_version is required.")

        meta = store.find_template(document_type)
        if meta is None:
            available = store.available_types()
            return _error(
                f"No template found for '{document_type}'. "
                f"Available types: {available}"
            )

        current_version = meta.policy_version or "unknown"
        embedded_version = policy_version.strip()
        is_current = current_version == embedded_version

        # Compute days since last update
        now = datetime.now(timezone.utc)
        delta = now - meta.last_updated
        days_since = delta.days

        if is_current:
            message = (
                f"The embedded policy version ({embedded_version}) matches "
                f"the current version. Last updated {days_since} day(s) ago."
            )
        else:
            message = (
                f"The embedded policy version ({embedded_version}) does not "
                f"match the current version ({current_version}). "
                f"The current policy was last updated {days_since} day(s) ago. "
                f"Consider updating the document's DCP block to the latest policy."
            )

        return _ok(
            is_current=is_current,
            current_version=current_version,
            embedded_version=embedded_version,
            days_since_update=days_since,
            message=message,
        )
    except Exception as exc:
        return _error(f"Unexpected error: {exc}")


def list_available_policies(store: LocalPolicyStore) -> dict[str, Any]:
    """Return all available document types with version and last-updated info."""
    try:
        templates = store.list_templates()
        policies = [
            {
                "document_type": t.document_type,
                "policy_version": t.policy_version,
                "last_updated": t.last_updated.isoformat(),
                "file_name": t.file_name,
            }
            for t in templates
        ]
        return _ok(policies=policies)
    except Exception as exc:
        return _error(f"Unexpected error: {exc}")


def generate_dcp_block(store: LocalPolicyStore, document_type: str) -> dict[str, Any]:
    """Extract and return the DCP block from a matching template.

    Useful when an AI client is helping a user create a new document and
    needs a pre-populated DCP block to embed.
    """
    try:
        if not document_type or not document_type.strip():
            return _error("document_type is required.")

        meta = store.find_template(document_type)
        if meta is None:
            available = store.available_types()
            return _error(
                f"No template found for '{document_type}'. "
                f"Available types: {available}"
            )

        content = store.get_template_content(str(meta.file_path))
        block_text = extract_dcp_block_text(content)
        if not block_text:
            return _error(
                f"Template for '{meta.document_type}' exists but contains "
                f"no DCP block."
            )

        return _ok(
            document_type=meta.document_type,
            dcp_block=block_text,
        )
    except Exception as exc:
        return _error(f"Unexpected error: {exc}")
