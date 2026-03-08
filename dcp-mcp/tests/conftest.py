"""Shared fixtures for DCP-MCP tests."""

from __future__ import annotations

from pathlib import Path

import pytest

# A complete, valid DCP template for testing
VALID_NDA_TEMPLATE = """\
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Non-Disclosure Agreement
Audience:         External counsel, counterparty legal team
Jurisdiction:     Delaware
Confidentiality:  Highly confidential

Policy Source:    acme/legal-policies/nda-policy
Policy Version:   nda-v2.1
Policy As-Of:     2026-01-15

Review Checklist:
□ Verify mutual confidentiality obligations
□ Check definition of "Confidential Information" for overbreadth
□ Confirm standard carve-outs are present
□ Flag non-compete clauses exceeding 12 months

Drafting Standards:
- Formal contractual tone
- Define all capitalized terms on first use
- Use "shall" for obligations, "may" for permissions
════════════════════════════════════════════════════════════

# NON-DISCLOSURE AGREEMENT

This is a placeholder NDA body.
"""

# A minimal valid template (no policy governance fields)
VALID_DPA_TEMPLATE = """\
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Data Processing Agreement
Audience:         Privacy counsel, counterparty DPO

Review Checklist:
□ Verify controller/processor roles
□ Check sub-processor provisions

Drafting Standards:
- Formal regulatory tone
- Reference specific GDPR articles
════════════════════════════════════════════════════════════

# DATA PROCESSING AGREEMENT

Body text here.
"""

# A vendor assessment template
VALID_VENDOR_TEMPLATE = """\
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Vendor Security Assessment
Audience:         Security team, procurement
Confidentiality:  Internal

Review Checklist:
□ Verify vendor provides SOC 2 Type II report
□ Confirm data types the vendor will access

Drafting Standards:
- Use clear risk ratings: Critical / High / Medium / Low
- Structure findings by security domain
════════════════════════════════════════════════════════════

# VENDOR SECURITY ASSESSMENT
"""

# A DCP block with missing required fields
INVALID_BLOCK_MISSING_FIELDS = """\
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Jurisdiction:     California
Confidentiality:  Internal
════════════════════════════════════════════════════════════
"""

# A DCP block with no header
INVALID_BLOCK_NO_HEADER = """\
════════════════════════════════════════════════════════════

Document Type:    Some Document
Audience:         Someone
════════════════════════════════════════════════════════════
"""

# A .dcp policy file
VALID_POLICY_FILE = """\
════════════════════════════════════════════════════════════
DCP POLICY — NDA

Version:          nda-v3.0
Owner:            Commercial Transactions

Review Checklist:
□ Verify mutual confidentiality obligations
□ Check definition scope

Drafting Standards:
- Formal contractual tone
- Plain English
════════════════════════════════════════════════════════════
"""


@pytest.fixture
def templates_dir(tmp_path: Path) -> Path:
    """Create a temporary templates directory with test templates."""
    (tmp_path / "nda.md").write_text(VALID_NDA_TEMPLATE, encoding="utf-8")
    (tmp_path / "dpa.md").write_text(VALID_DPA_TEMPLATE, encoding="utf-8")
    (tmp_path / "vendor-assessment.md").write_text(VALID_VENDOR_TEMPLATE, encoding="utf-8")
    return tmp_path


@pytest.fixture
def templates_dir_with_policy(templates_dir: Path) -> Path:
    """Templates directory that also includes a .dcp policy file."""
    (templates_dir / "nda-policy.dcp").write_text(VALID_POLICY_FILE, encoding="utf-8")
    return templates_dir
