"""Tests for DCP-MCP tools, parser, and store.

All tests use tmp_path fixtures with synthetic templates. No dependency on
the actual DCP repo templates directory.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from dcp_mcp.parser import (
    extract_checklist,
    extract_dcp_block_text,
    extract_fields,
    extract_standards,
    parse_dcp_blocks,
    validate_dcp_header,
)
from dcp_mcp.store import LocalPolicyStore
from dcp_mcp.tools import (
    check_policy_freshness,
    fetch_policy,
    generate_dcp_block,
    list_available_policies,
    validate_dcp_header_tool,
)

from .conftest import (
    INVALID_BLOCK_MISSING_FIELDS,
    INVALID_BLOCK_NO_HEADER,
    VALID_DPA_TEMPLATE,
    VALID_NDA_TEMPLATE,
    VALID_POLICY_FILE,
)


# ═══════════════════════════════════════════════════════════════════════
# Parser tests
# ═══════════════════════════════════════════════════════════════════════


class TestParser:
    def test_parse_valid_block(self) -> None:
        blocks = parse_dcp_blocks(VALID_NDA_TEMPLATE)
        assert len(blocks) == 1
        block = blocks[0]
        assert block.kind == "document"
        assert block.fields["Document Type"] == "Non-Disclosure Agreement"
        assert block.fields["Audience"] == "External counsel, counterparty legal team"
        assert block.fields["Jurisdiction"] == "Delaware"

    def test_parse_checklist(self) -> None:
        items = extract_checklist(VALID_NDA_TEMPLATE)
        assert len(items) == 4
        assert "Verify mutual confidentiality obligations" in items[0]
        assert "overbreadth" in items[1]

    def test_parse_standards(self) -> None:
        items = extract_standards(VALID_NDA_TEMPLATE)
        assert len(items) == 3
        assert "Formal contractual tone" in items[0]

    def test_parse_fields(self) -> None:
        fields = extract_fields(VALID_NDA_TEMPLATE)
        assert fields["Document Type"] == "Non-Disclosure Agreement"
        assert fields["Policy Version"] == "nda-v2.1"
        assert fields["Policy As-Of"] == "2026-01-15"

    def test_extract_block_text(self) -> None:
        block_text = extract_dcp_block_text(VALID_NDA_TEMPLATE)
        assert block_text is not None
        assert "DCP — DOCUMENT CONTEXT PROTOCOL" in block_text
        assert "Review Checklist:" in block_text
        assert block_text.startswith("═" * 40)

    def test_parse_policy_file(self) -> None:
        blocks = parse_dcp_blocks(VALID_POLICY_FILE)
        assert len(blocks) == 1
        block = blocks[0]
        assert block.kind == "policy"
        assert block.fields["Version"] == "nda-v3.0"
        assert block.fields["Owner"] == "Commercial Transactions"

    def test_parse_no_block(self) -> None:
        blocks = parse_dcp_blocks("Just some text with no DCP block.")
        assert len(blocks) == 0

    def test_extract_from_no_block(self) -> None:
        assert extract_fields("no block here") == {}
        assert extract_checklist("no block here") == []
        assert extract_standards("no block here") == []
        assert extract_dcp_block_text("no block here") is None


# ═══════════════════════════════════════════════════════════════════════
# Validation tests
# ═══════════════════════════════════════════════════════════════════════


class TestValidation:
    def test_valid_block(self) -> None:
        result = validate_dcp_header(VALID_NDA_TEMPLATE)
        assert result.valid is True
        assert len(result.errors) == 0
        assert "Document Type" in result.parsed_fields

    def test_missing_required_fields(self) -> None:
        result = validate_dcp_header(INVALID_BLOCK_MISSING_FIELDS)
        assert result.valid is False
        error_messages = [e["message"] for e in result.errors]
        assert any("Document Type" in m for m in error_messages)
        assert any("Audience" in m for m in error_messages)

    def test_missing_header(self) -> None:
        result = validate_dcp_header(INVALID_BLOCK_NO_HEADER)
        assert result.valid is False
        error_messages = [e["message"] for e in result.errors]
        assert any("Missing DCP header" in m for m in error_messages)

    def test_bare_text_without_delimiters(self) -> None:
        bare_block = (
            "DCP — DOCUMENT CONTEXT PROTOCOL\n\n"
            "Document Type:    Contract Review\n"
            "Audience:         Legal team\n"
        )
        result = validate_dcp_header(bare_block)
        assert result.valid is True
        assert result.parsed_fields["Document Type"] == "Contract Review"

    def test_warnings_for_recommended_fields(self) -> None:
        result = validate_dcp_header(VALID_DPA_TEMPLATE)
        warning_messages = [w["message"] for w in result.warnings]
        assert any("Jurisdiction" in m for m in warning_messages)


# ═══════════════════════════════════════════════════════════════════════
# Store tests
# ═══════════════════════════════════════════════════════════════════════


class TestLocalPolicyStore:
    def test_list_templates(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        templates = store.list_templates()
        assert len(templates) == 3
        types = {t.document_type for t in templates}
        assert "Non-Disclosure Agreement" in types
        assert "Data Processing Agreement" in types
        assert "Vendor Security Assessment" in types

    def test_list_includes_dcp_files(self, templates_dir_with_policy: Path) -> None:
        store = LocalPolicyStore(templates_dir_with_policy)
        templates = store.list_templates()
        assert len(templates) == 4

    def test_get_template_content(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        content = store.get_template_content("nda.md")
        assert "NON-DISCLOSURE AGREEMENT" in content

    def test_get_template_content_not_found(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        with pytest.raises(FileNotFoundError):
            store.get_template_content("nonexistent.md")

    def test_find_template_exact(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("Non-Disclosure Agreement")
        assert meta is not None
        assert meta.document_type == "Non-Disclosure Agreement"
        assert len(meta.review_checklist) == 4
        assert len(meta.drafting_standards) == 3

    def test_find_template_case_insensitive(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("non-disclosure agreement")
        assert meta is not None
        assert meta.document_type == "Non-Disclosure Agreement"

    def test_find_template_abbreviation(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("NDA")
        assert meta is not None
        assert meta.document_type == "Non-Disclosure Agreement"

    def test_find_template_abbreviation_lowercase(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("dpa")
        assert meta is not None
        assert meta.document_type == "Data Processing Agreement"

    def test_find_template_partial(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("vendor")
        assert meta is not None
        assert meta.document_type == "Vendor Security Assessment"

    def test_find_template_fuzzy(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("non-disclosure")
        assert meta is not None
        assert meta.document_type == "Non-Disclosure Agreement"

    def test_find_template_not_found(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("Totally Nonexistent Document")
        assert meta is None

    def test_find_by_filename(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        meta = store.find_template("vendor-assessment")
        assert meta is not None
        assert meta.document_type == "Vendor Security Assessment"

    def test_empty_templates_dir(self, tmp_path: Path) -> None:
        store = LocalPolicyStore(tmp_path)
        assert store.list_templates() == []
        assert store.find_template("NDA") is None

    def test_none_templates_path(self) -> None:
        store = LocalPolicyStore(None)
        assert store.list_templates() == []
        assert store.find_template("NDA") is None

    def test_cache_invalidation(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        assert len(store.list_templates()) == 3

        # Add a new template
        new_template = (
            "═" * 60 + "\n"
            "DCP — DOCUMENT CONTEXT PROTOCOL\n\n"
            "Document Type:    Legal Memo\n"
            "Audience:         Internal team\n"
            + "═" * 60 + "\n"
        )
        (templates_dir / "legal-memo.md").write_text(new_template, encoding="utf-8")
        assert len(store.list_templates()) == 4


# ═══════════════════════════════════════════════════════════════════════
# Tool tests (fetch_policy)
# ═══════════════════════════════════════════════════════════════════════


class TestFetchPolicy:
    def test_valid_document_type(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = fetch_policy(store, "Non-Disclosure Agreement")
        assert result["success"] is True
        assert result["document_type"] == "Non-Disclosure Agreement"
        assert len(result["review_checklist"]) == 4
        assert len(result["drafting_standards"]) == 3
        assert result["policy_version"] == "nda-v2.1"

    def test_unknown_document_type(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = fetch_policy(store, "Invisible Contract")
        assert result["success"] is False
        assert "No template found" in result["error"]
        assert "Available types:" in result["error"]

    def test_fuzzy_match(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = fetch_policy(store, "non-disclosure")
        assert result["success"] is True
        assert result["document_type"] == "Non-Disclosure Agreement"

    def test_abbreviation_match(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = fetch_policy(store, "NDA")
        assert result["success"] is True
        assert result["document_type"] == "Non-Disclosure Agreement"

    def test_empty_input(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = fetch_policy(store, "")
        assert result["success"] is False
        assert "required" in result["error"]


# ═══════════════════════════════════════════════════════════════════════
# Tool tests (validate_dcp_header)
# ═══════════════════════════════════════════════════════════════════════


class TestValidateDcpHeaderTool:
    def test_valid_block(self) -> None:
        result = validate_dcp_header_tool(VALID_NDA_TEMPLATE)
        assert result["success"] is True
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_missing_required_field(self) -> None:
        result = validate_dcp_header_tool(INVALID_BLOCK_MISSING_FIELDS)
        assert result["success"] is True
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_empty_input(self) -> None:
        result = validate_dcp_header_tool("")
        assert result["success"] is False


# ═══════════════════════════════════════════════════════════════════════
# Tool tests (check_policy_freshness)
# ═══════════════════════════════════════════════════════════════════════


class TestCheckPolicyFreshness:
    def test_current_version(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = check_policy_freshness(store, "NDA", "nda-v2.1")
        assert result["success"] is True
        assert result["is_current"] is True
        assert result["current_version"] == "nda-v2.1"
        assert result["embedded_version"] == "nda-v2.1"
        assert "matches" in result["message"]

    def test_stale_version(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = check_policy_freshness(store, "NDA", "nda-v1.0")
        assert result["success"] is True
        assert result["is_current"] is False
        assert result["current_version"] == "nda-v2.1"
        assert result["embedded_version"] == "nda-v1.0"
        assert "does not match" in result["message"]

    def test_unknown_type(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = check_policy_freshness(store, "Nonexistent", "v1")
        assert result["success"] is False
        assert "No template found" in result["error"]

    def test_empty_inputs(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = check_policy_freshness(store, "", "v1")
        assert result["success"] is False
        result = check_policy_freshness(store, "NDA", "")
        assert result["success"] is False


# ═══════════════════════════════════════════════════════════════════════
# Tool tests (list_available_policies)
# ═══════════════════════════════════════════════════════════════════════


class TestListAvailablePolicies:
    def test_lists_all(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = list_available_policies(store)
        assert result["success"] is True
        assert len(result["policies"]) == 3
        types = {p["document_type"] for p in result["policies"]}
        assert "Non-Disclosure Agreement" in types
        assert "Data Processing Agreement" in types
        assert "Vendor Security Assessment" in types

    def test_includes_version_info(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = list_available_policies(store)
        nda = next(p for p in result["policies"] if p["document_type"] == "Non-Disclosure Agreement")
        assert nda["policy_version"] == "nda-v2.1"
        assert nda["last_updated"] is not None

    def test_empty_store(self, tmp_path: Path) -> None:
        store = LocalPolicyStore(tmp_path)
        result = list_available_policies(store)
        assert result["success"] is True
        assert result["policies"] == []


# ═══════════════════════════════════════════════════════════════════════
# Tool tests (generate_dcp_block)
# ═══════════════════════════════════════════════════════════════════════


class TestGenerateDcpBlock:
    def test_generates_block(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = generate_dcp_block(store, "NDA")
        assert result["success"] is True
        assert result["document_type"] == "Non-Disclosure Agreement"
        assert "DCP — DOCUMENT CONTEXT PROTOCOL" in result["dcp_block"]
        assert "Review Checklist:" in result["dcp_block"]

    def test_unknown_type(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = generate_dcp_block(store, "Nonexistent")
        assert result["success"] is False
        assert "No template found" in result["error"]

    def test_empty_input(self, templates_dir: Path) -> None:
        store = LocalPolicyStore(templates_dir)
        result = generate_dcp_block(store, "")
        assert result["success"] is False
