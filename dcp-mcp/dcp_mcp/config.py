"""Configuration loading for DCP-MCP server.

Reads settings from environment variables (with .env file support via
python-dotenv). All paths are resolved through pathlib for cross-platform
compatibility.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

_DEFAULT_TEMPLATES_REL = Path("../templates")
_DEFAULT_SERVER_NAME = "DCP Policy Server"


@dataclass(frozen=True)
class Config:
    """Server configuration resolved from environment variables."""

    templates_path: Path | None
    mode: str  # "local" or "hosted"
    server_name: str
    server_url: str | None  # hosted mode only
    api_key: str | None  # hosted mode only

    @property
    def is_local(self) -> bool:
        return self.mode == "local"


def load_config(env_file: Path | None = None) -> Config:
    """Load configuration from environment, optionally reading a .env file.

    If TEMPLATES_PATH is not set, defaults to ``../templates/`` relative to
    the ``dcp-mcp/`` directory (i.e. the DCP repo's templates folder).  When
    that default path doesn't exist either, ``templates_path`` is set to
    ``None`` and a log message explains how to configure it.
    """
    if env_file:
        load_dotenv(env_file)
    else:
        # Look for .env in the dcp-mcp directory
        default_env = Path(__file__).resolve().parent.parent / ".env"
        if default_env.exists():
            load_dotenv(default_env)

    raw_path = os.getenv("TEMPLATES_PATH")
    if raw_path:
        templates_path = Path(raw_path)
        if not templates_path.is_absolute():
            templates_path = (Path(__file__).resolve().parent.parent / templates_path).resolve()
    else:
        candidate = (Path(__file__).resolve().parent.parent / _DEFAULT_TEMPLATES_REL).resolve()
        if candidate.is_dir():
            templates_path = candidate
        else:
            templates_path = None
            logger.warning(
                "No TEMPLATES_PATH configured and the default path (%s) does not exist. "
                "Set the TEMPLATES_PATH environment variable to your templates directory. "
                "The server will start with an empty template list.",
                candidate,
            )

    if templates_path and not templates_path.is_dir():
        logger.warning(
            "TEMPLATES_PATH '%s' is not a directory. "
            "The server will start with an empty template list.",
            templates_path,
        )
        templates_path = None

    mode = os.getenv("DCP_MODE", "local").lower()
    if mode not in ("local", "hosted"):
        logger.warning("DCP_MODE '%s' is not recognized; defaulting to 'local'.", mode)
        mode = "local"

    return Config(
        templates_path=templates_path,
        mode=mode,
        server_name=os.getenv("DCP_SERVER_NAME", _DEFAULT_SERVER_NAME),
        server_url=os.getenv("DCP_SERVER_URL"),
        api_key=os.getenv("DCP_API_KEY"),
    )
