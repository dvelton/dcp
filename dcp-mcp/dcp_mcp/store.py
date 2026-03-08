"""Policy store abstraction for DCP-MCP.

Defines a ``PolicyStore`` abstract base class and a ``LocalPolicyStore``
implementation that reads templates from the local filesystem.  The
abstraction exists so a future ``HostedPolicyStore`` can swap in without
touching the tool definitions.
"""

from __future__ import annotations

import difflib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from dcp_mcp.parser import ParsedBlock, extract_dcp_block_text, parse_dcp_blocks

logger = logging.getLogger(__name__)

# ── Common abbreviation map ──────────────────────────────────────────────
# Well-known legal/business document abbreviations.  Populated as a
# convenience — users with custom templates don't need to update this.
# The fuzzy matcher is the real fallback.

_ABBREVIATIONS: dict[str, str] = {
    "NDA": "Non-Disclosure Agreement",
    "DPA": "Data Processing Agreement",
    "MSA": "Master Services Agreement",
    "SOW": "Statement of Work",
    "SLA": "Service Level Agreement",
    "RFP": "Request for Proposal",
    "RFI": "Request for Information",
    "MOU": "Memorandum of Understanding",
    "LOI": "Letter of Intent",
    "DPIA": "Data Protection Impact Assessment",
    "TOS": "Terms of Service",
    "EULA": "End User License Agreement",
}


# ── Data classes ─────────────────────────────────────────────────────────

@dataclass
class TemplateInfo:
    """Summary information about a single template."""
    document_type: str
    file_path: Path
    file_name: str
    policy_version: str | None
    policy_source: str | None
    last_updated: datetime
    dcp_block: ParsedBlock | None = None


@dataclass
class TemplateMetadata:
    """Full metadata for a template, including parsed DCP content."""
    document_type: str
    file_path: Path
    review_checklist: list[str] = field(default_factory=list)
    drafting_standards: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    policy_version: str | None = None
    policy_source: str | None = None
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fields: dict[str, str] = field(default_factory=dict)


# ── Abstract base class ─────────────────────────────────────────────────

class PolicyStore(ABC):
    """Abstract interface for accessing DCP policy templates."""

    @abstractmethod
    def list_templates(self) -> list[TemplateInfo]:
        """Return summary info for all available templates."""
        ...

    @abstractmethod
    def get_template_content(self, file_path: str) -> str:
        """Return the full text of a template file."""
        ...

    @abstractmethod
    def get_template_metadata(self, file_path: str) -> TemplateMetadata:
        """Return parsed metadata for a specific template."""
        ...

    @abstractmethod
    def find_template(self, document_type: str) -> TemplateMetadata | None:
        """Find a template by document type string (supports fuzzy matching)."""
        ...


# ── Local filesystem implementation ─────────────────────────────────────

class LocalPolicyStore(PolicyStore):
    """Reads templates from a local directory.

    Scans ``templates_path`` for ``.md`` and ``.dcp`` files containing DCP
    blocks.  Parsed metadata is cached and invalidated when a file's
    modification time changes.
    """

    def __init__(self, templates_path: Path | None, mode: str = "local") -> None:
        self._templates_path = templates_path
        self._mode = mode
        self._cache: dict[Path, tuple[float, TemplateInfo, TemplateMetadata]] = {}

    # ── Public API ───────────────────────────────────────────────────

    def list_templates(self) -> list[TemplateInfo]:
        self._refresh_cache()
        return [info for _, info, _ in self._cache.values()]

    def get_template_content(self, file_path: str) -> str:
        resolved = self._resolve_path(file_path)
        if resolved is None or not resolved.is_file():
            raise FileNotFoundError(f"Template not found: {file_path}")
        return resolved.read_text(encoding="utf-8")

    def get_template_metadata(self, file_path: str) -> TemplateMetadata:
        self._refresh_cache()
        resolved = self._resolve_path(file_path)
        if resolved and resolved in self._cache:
            return self._cache[resolved][2]
        raise FileNotFoundError(f"Template not found: {file_path}")

    def find_template(self, document_type: str) -> TemplateMetadata | None:
        self._refresh_cache()
        if not self._cache:
            return None

        query = document_type.strip()
        query_lower = query.lower()

        # Build lookup structures
        type_to_path: dict[str, Path] = {}
        name_to_path: dict[str, Path] = {}
        for path, (_, info, _) in self._cache.items():
            doc_type = info.document_type
            type_to_path[doc_type] = path
            name_to_path[info.file_name] = path

        all_types = list(type_to_path.keys())
        all_types_lower = {t.lower(): t for t in all_types}
        all_names_lower = {n.lower(): n for n in name_to_path.keys()}

        # 1. Exact match on Document Type (case-insensitive)
        if query_lower in all_types_lower:
            path = type_to_path[all_types_lower[query_lower]]
            return self._cache[path][2]

        # 2. Abbreviation expansion
        expanded = _ABBREVIATIONS.get(query.upper())
        if expanded and expanded.lower() in all_types_lower:
            path = type_to_path[all_types_lower[expanded.lower()]]
            return self._cache[path][2]

        # 3. Exact match on filename stem (case-insensitive)
        if query_lower in all_names_lower:
            path = name_to_path[all_names_lower[query_lower]]
            return self._cache[path][2]

        # 4. Substring match — does the query appear in any document type?
        for doc_type in all_types:
            if query_lower in doc_type.lower():
                path = type_to_path[doc_type]
                return self._cache[path][2]

        # 5. Fuzzy match on document types
        close = difflib.get_close_matches(query_lower, all_types_lower.keys(), n=1, cutoff=0.6)
        if close:
            path = type_to_path[all_types_lower[close[0]]]
            return self._cache[path][2]

        # 6. Fuzzy match on filenames
        close_names = difflib.get_close_matches(query_lower, all_names_lower.keys(), n=1, cutoff=0.6)
        if close_names:
            path = name_to_path[all_names_lower[close_names[0]]]
            return self._cache[path][2]

        return None

    def available_types(self) -> list[str]:
        """Return a list of all available Document Type strings."""
        self._refresh_cache()
        return [info.document_type for _, info, _ in self._cache.values()]

    # ── Internal ─────────────────────────────────────────────────────

    def _resolve_path(self, file_path: str) -> Path | None:
        if self._templates_path is None:
            return None
        p = Path(file_path)
        if p.is_absolute():
            return p if p.exists() else None
        candidate = self._templates_path / p
        return candidate if candidate.exists() else None

    def _refresh_cache(self) -> None:
        if self._templates_path is None or not self._templates_path.is_dir():
            return

        current_files: set[Path] = set()
        for ext in ("*.md", "*.dcp"):
            current_files.update(self._templates_path.glob(ext))

        # Remove cached entries for files that no longer exist
        gone = set(self._cache.keys()) - current_files
        for path in gone:
            del self._cache[path]

        # Update or add entries
        for path in current_files:
            mtime = path.stat().st_mtime
            if path in self._cache and self._cache[path][0] == mtime:
                continue
            try:
                info, meta = self._parse_template(path, mtime)
                self._cache[path] = (mtime, info, meta)
            except Exception:
                logger.warning("Failed to parse template: %s", path, exc_info=True)

    def _parse_template(self, path: Path, mtime: float) -> tuple[TemplateInfo, TemplateMetadata]:
        text = path.read_text(encoding="utf-8")
        blocks = parse_dcp_blocks(text)

        last_updated = datetime.fromtimestamp(mtime, tz=timezone.utc)

        if not blocks:
            # File has no DCP block — still list it with filename as type
            doc_type = path.stem.replace("-", " ").replace("_", " ").title()
            info = TemplateInfo(
                document_type=doc_type,
                file_path=path,
                file_name=path.stem,
                policy_version=None,
                policy_source=None,
                last_updated=last_updated,
            )
            meta = TemplateMetadata(
                document_type=doc_type,
                file_path=path,
                last_updated=last_updated,
            )
            return info, meta

        block = blocks[0]
        doc_type = block.fields.get("Document Type", "")
        if not doc_type:
            doc_type = path.stem.replace("-", " ").replace("_", " ").title()

        policy_version = block.fields.get("Policy Version") or block.fields.get("Version")
        policy_source = block.fields.get("Policy Source")
        policy_as_of = block.fields.get("Policy As-Of")

        # Use Policy As-Of date if available, otherwise file mtime
        if policy_as_of:
            try:
                last_updated = datetime.fromisoformat(policy_as_of).replace(tzinfo=timezone.utc)
            except ValueError:
                pass

        # In local mode, policy source is the file path
        if self._mode == "local" and not policy_source:
            policy_source = str(path)

        # If no explicit version, use file mtime as ISO date
        if not policy_version:
            policy_version = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")

        info = TemplateInfo(
            document_type=doc_type,
            file_path=path,
            file_name=path.stem,
            policy_version=policy_version,
            policy_source=policy_source,
            last_updated=last_updated,
            dcp_block=block,
        )
        meta = TemplateMetadata(
            document_type=doc_type,
            file_path=path,
            review_checklist=list(block.review_checklist),
            drafting_standards=list(block.drafting_standards),
            constraints=list(block.constraints),
            policy_version=policy_version,
            policy_source=policy_source,
            last_updated=last_updated,
            fields=dict(block.fields),
        )
        return info, meta


# TODO: HostedPolicyStore — backed by remote API or database.
# The interface is the same as LocalPolicyStore; swap in via Config.mode.
