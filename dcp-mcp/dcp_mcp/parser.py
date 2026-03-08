"""DCP block parser and validator.

Self-contained implementation of DCP block parsing and validation logic.
Adapted from the DCP project's ``tools/validate-dcp.py`` CLI tool — both
parse the same format defined in the DCP specification.  If you change
parsing behaviour here, consider updating ``tools/validate-dcp.py`` to
match (and vice versa).

Public API
----------
- ``parse_dcp_blocks(text)``    — find and parse all DCP blocks in a string
- ``validate_dcp_header(text)`` — validate a DCP block and return a report
- ``extract_fields(text)``      — pull key/value fields from a DCP block
- ``extract_checklist(text)``   — pull Review Checklist items
- ``extract_standards(text)``   — pull Drafting Standards items
- ``extract_dcp_block_text(text)`` — extract the raw DCP block text (delimiters included)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

# ── Constants (match the DCP specification) ──────────────────────────────

DELIMITER_CHAR = "═"
MIN_DELIMITER_LEN = 40
HEADER_DOCUMENT = "DCP — DOCUMENT CONTEXT PROTOCOL"
HEADER_POLICY_PREFIX = "DCP POLICY —"

REQUIRED_FIELDS: dict[str, list[str]] = {
    "document": ["Document Type", "Audience"],
    "policy": ["Version", "Owner"],
}

RECOMMENDED_FIELDS: list[str] = [
    "Jurisdiction",
    "Confidentiality",
]

# Sections that collect list items rather than single-line values
_LIST_SECTIONS = {
    "Review Checklist": "checklist",
    "Drafting Standards": "drafting",
    "Constraints": "constraints",
    "Additional Checklist Items": "checklist",
    "Additional Drafting Standards": "drafting",
    "Additional Constraints": "constraints",
}


# ── Data classes ─────────────────────────────────────────────────────────

@dataclass
class Issue:
    """A single validation error or warning."""
    line: int
    message: str
    severity: Literal["error", "warning"] = "error"


@dataclass
class ParsedBlock:
    """Result of parsing a single DCP block."""
    start_line: int
    end_line: int | None = None
    kind: Literal["document", "policy"] | None = None
    fields: dict[str, str] = field(default_factory=dict)
    review_checklist: list[str] = field(default_factory=list)
    drafting_standards: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    raw_text: str = ""


@dataclass
class ValidationResult:
    """Result of validating a DCP header/block."""
    valid: bool
    errors: list[dict[str, str | int]] = field(default_factory=list)
    warnings: list[dict[str, str | int]] = field(default_factory=list)
    parsed_fields: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "parsed_fields": self.parsed_fields,
        }


# ── Internal helpers ─────────────────────────────────────────────────────

def _is_delimiter(line: str) -> bool:
    s = line.strip()
    return len(s) >= MIN_DELIMITER_LEN and all(c == DELIMITER_CHAR for c in s)


def _find_raw_blocks(lines: list[str]) -> list[tuple[int, int | None]]:
    """Return (start, end) line-index pairs for every delimiter-bounded region."""
    blocks: list[tuple[int, int | None]] = []
    i = 0
    while i < len(lines):
        if _is_delimiter(lines[i]):
            start = i
            i += 1
            end = None
            while i < len(lines):
                if _is_delimiter(lines[i]):
                    end = i
                    i += 1
                    break
                i += 1
            blocks.append((start, end))
        else:
            i += 1
    return blocks


def _parse_single_block(lines: list[str], start: int, end: int | None) -> ParsedBlock:
    """Parse the content between two delimiters into a ``ParsedBlock``."""
    block = ParsedBlock(start_line=start + 1)

    if end is not None:
        block.end_line = end + 1
        content_end = end
        raw_lines = lines[start : end + 1]
    else:
        block.issues.append(Issue(
            start + 1,
            "DCP block opened but never closed — missing closing delimiter",
        ))
        content_end = len(lines)
        raw_lines = lines[start:]

    block.raw_text = "\n".join(raw_lines)

    # Content lines are between the delimiters (exclusive)
    content_start = start + 1

    # Detect header in the first few non-empty lines
    header_found = False
    for idx in range(content_start, min(content_start + 3, content_end)):
        s = lines[idx].strip()
        if not s:
            continue
        if s == HEADER_DOCUMENT:
            block.kind = "document"
            header_found = True
            break
        if s.startswith(HEADER_POLICY_PREFIX):
            block.kind = "policy"
            header_found = True
            break

    if not header_found:
        block.issues.append(Issue(
            content_start + 1,
            f"Missing DCP header. Expected '{HEADER_DOCUMENT}' or '{HEADER_POLICY_PREFIX} ...'",
        ))
        block.kind = "document"

    # Parse fields and list sections
    current_section: str | None = None
    current_list: list[str] | None = None

    for idx in range(content_start, content_end):
        line = lines[idx]
        s = line.strip()

        if not s:
            continue

        # Check if this line starts a new list section
        section_match = False
        for section_name, section_type in _LIST_SECTIONS.items():
            if s.startswith(f"{section_name}:"):
                current_section = section_type
                if section_type == "checklist":
                    current_list = block.review_checklist
                elif section_type == "drafting":
                    current_list = block.drafting_standards
                elif section_type == "constraints":
                    current_list = block.constraints
                section_match = True
                break

        if section_match:
            continue

        if current_section is None:
            # Try to match a key: value field
            m = re.match(r"^([A-Za-z][A-Za-z /&-]+?):\s*(.*)", s)
            if m:
                block.fields[m.group(1).strip()] = m.group(2).strip()
        else:
            # We're inside a list section — collect items
            if current_section == "checklist":
                if s.startswith("□"):
                    item = s[1:].strip().lstrip(" ")
                    current_list.append(item)
                elif line.startswith("   ") or line.startswith("\t"):
                    # Continuation line — append to last item
                    if current_list:
                        current_list[-1] += " " + s
                else:
                    # Validate notation
                    if s.startswith(("-", "*", "•", "[ ]", "[x]", "[X]")):
                        block.issues.append(Issue(
                            idx + 1,
                            f"Review Checklist should use □ notation, found '{s[:3].strip()}'",
                        ))
                    else:
                        # New non-list-section field resets context
                        m = re.match(r"^([A-Za-z][A-Za-z /&-]+?):\s*(.*)", s)
                        if m:
                            current_section = None
                            current_list = None
                            block.fields[m.group(1).strip()] = m.group(2).strip()

            elif current_section in ("drafting", "constraints"):
                if s.startswith("-"):
                    item = s[1:].strip()
                    current_list.append(item)
                elif line.startswith("  ") or line.startswith("\t"):
                    if current_list:
                        current_list[-1] += " " + s
                else:
                    if s.startswith(("□", "*", "•")):
                        block.issues.append(Issue(
                            idx + 1,
                            f"Drafting Standards/Constraints should use - notation, found '{s[:3].strip()}'",
                            severity="warning",
                        ))
                    else:
                        m = re.match(r"^([A-Za-z][A-Za-z /&-]+?):\s*(.*)", s)
                        if m:
                            current_section = None
                            current_list = None
                            block.fields[m.group(1).strip()] = m.group(2).strip()

    # Validate required fields
    for rf in REQUIRED_FIELDS.get(block.kind or "document", []):
        if rf not in block.fields:
            block.issues.append(Issue(start + 1, f"Missing required field: {rf}"))
        else:
            val = block.fields[rf]
            if not val or val.startswith("["):
                block.issues.append(Issue(
                    start + 1,
                    f"Field '{rf}' appears empty or is still a placeholder",
                    severity="warning",
                ))

    # Warn on missing recommended fields (document blocks only)
    if block.kind == "document":
        for rf in RECOMMENDED_FIELDS:
            if rf not in block.fields:
                block.issues.append(Issue(
                    start + 1,
                    f"Missing recommended field: {rf}",
                    severity="warning",
                ))

    return block


# ── Public API ───────────────────────────────────────────────────────────

def parse_dcp_blocks(text: str) -> list[ParsedBlock]:
    """Parse all DCP blocks found in ``text``.

    Returns a list of ``ParsedBlock`` objects.  Most documents contain a
    single block; policy-governed documents may contain layered blocks.
    """
    lines = text.split("\n")
    raw_blocks = _find_raw_blocks(lines)
    return [_parse_single_block(lines, start, end) for start, end in raw_blocks]


def validate_dcp_header(text: str) -> ValidationResult:
    """Validate DCP block text and return a structured report.

    ``text`` should be the content of a DCP block (with or without
    delimiters).  Returns a ``ValidationResult`` with ``valid``, ``errors``,
    ``warnings``, and ``parsed_fields``.
    """
    # If the text doesn't contain delimiters, wrap it so the parser can find it
    lines = text.strip().split("\n")
    has_delimiters = any(_is_delimiter(line) for line in lines)
    if not has_delimiters:
        delimiter = DELIMITER_CHAR * MIN_DELIMITER_LEN
        text = f"{delimiter}\n{text.strip()}\n{delimiter}"

    blocks = parse_dcp_blocks(text)

    if not blocks:
        return ValidationResult(
            valid=False,
            errors=[{"line": 0, "message": "No DCP block found in the provided text."}],
        )

    block = blocks[0]
    errors = [
        {"line": i.line, "message": i.message}
        for i in block.issues
        if i.severity == "error"
    ]
    warnings = [
        {"line": i.line, "message": i.message}
        for i in block.issues
        if i.severity == "warning"
    ]

    parsed_fields = dict(block.fields)
    if block.review_checklist:
        parsed_fields["Review Checklist"] = block.review_checklist
    if block.drafting_standards:
        parsed_fields["Drafting Standards"] = block.drafting_standards
    if block.constraints:
        parsed_fields["Constraints"] = block.constraints

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        parsed_fields=parsed_fields,
    )


def extract_fields(text: str) -> dict[str, str]:
    """Extract key/value fields from the first DCP block in ``text``.

    Returns a flat dict of field name to value.  List sections (Review
    Checklist, Drafting Standards, Constraints) are excluded — use
    ``extract_checklist`` and ``extract_standards`` for those.
    """
    blocks = parse_dcp_blocks(text)
    if not blocks:
        return {}
    return dict(blocks[0].fields)


def extract_checklist(text: str) -> list[str]:
    """Extract Review Checklist items from the first DCP block in ``text``."""
    blocks = parse_dcp_blocks(text)
    if not blocks:
        return []
    return list(blocks[0].review_checklist)


def extract_standards(text: str) -> list[str]:
    """Extract Drafting Standards items from the first DCP block in ``text``."""
    blocks = parse_dcp_blocks(text)
    if not blocks:
        return []
    return list(blocks[0].drafting_standards)


def extract_dcp_block_text(text: str) -> str | None:
    """Extract the raw text of the first DCP block (delimiters included).

    Returns ``None`` if no block is found.
    """
    blocks = parse_dcp_blocks(text)
    if not blocks:
        return None
    return blocks[0].raw_text
