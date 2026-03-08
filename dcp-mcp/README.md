# DCP-MCP

A Model Context Protocol (MCP) server that gives AI clients live access to your DCP policy templates. Connect once, and your AI has authoritative, versioned access to every review checklist, drafting standard, and policy in your library.

## Why run a DCP-MCP server?

DCP blocks embed review criteria and drafting standards directly into documents. That works well for individual documents, but it doesn't help when an AI client needs to know your team's current policies _before_ working on a document — or when it needs to check whether a document's embedded policy is still up to date.

DCP-MCP solves both problems. It reads your templates directory and exposes your policies as structured data over MCP. Any connected AI client can look up a policy by document type, validate a DCP block, check version freshness, or generate a new DCP block from a template.

One place to update a policy; every connected AI client gets it instantly.

## Quickstart (Local Mode)

### Option A: From the DCP repo

```bash
git clone https://github.com/your-org/dcp.git
cd dcp/dcp-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m dcp_mcp.server
```

The server picks up templates from `../templates/` automatically.

### Option B: Standalone with your own templates

```bash
# Copy or clone just the dcp-mcp directory
cd dcp-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Point to your templates
export TEMPLATES_PATH=/path/to/your/templates
python -m dcp_mcp.server
```

Your templates directory should contain `.md` or `.dcp` files with DCP blocks at the top. The server discovers document types dynamically from whatever files it finds.

## Connect your AI client

Register the server in your MCP client configuration:

```json
{
    "mcpServers": {
        "dcp": {
            "command": "python",
            "args": ["-m", "dcp_mcp.server"],
            "cwd": "/path/to/dcp-mcp"
        }
    }
}
```

If you're using `TEMPLATES_PATH`, add it to the environment:

```json
{
    "mcpServers": {
        "dcp": {
            "command": "python",
            "args": ["-m", "dcp_mcp.server"],
            "cwd": "/path/to/dcp-mcp",
            "env": {
                "TEMPLATES_PATH": "/path/to/your/templates"
            }
        }
    }
}
```

## Available tools

### `fetch_policy`

Look up the review checklist, drafting standards, and policy metadata for a document type. Supports fuzzy matching — "NDA", "non-disclosure", and "nda" all resolve to a Non-Disclosure Agreement template.

### `validate_dcp_header`

Validate a DCP block. Pass the text of a document's DCP block (with or without delimiters). Returns errors, warnings, and all parsed fields.

### `check_policy_freshness`

Check whether a document's embedded policy version is still current. Pass the document type and the Policy Version from the document's DCP block. Returns whether the version matches, days since last update, and a human-readable message.

### `list_available_policies`

List all available document types with their current version and last-updated date. Useful for AI clients to orient themselves on first connection.

### `generate_dcp_block`

Generate a pre-populated DCP block for a document type, extracted from the matching template. Use this when helping a user create a new document.

## Use your own templates

Point `TEMPLATES_PATH` at any directory of `.md` or `.dcp` files containing DCP blocks. The server indexes whatever it finds — your document types, your checklists, your standards.

```bash
export TEMPLATES_PATH=/path/to/your/templates
python -m dcp_mcp.server
```

Templates should have a DCP block at the top of the file. The server extracts the `Document Type` field to identify each template and parses the review checklist and drafting standards for structured access.

See the [DCP specification](../specification.md) for block format details and the [customization guide](../customization-guide.md) for help writing effective checklists and standards.

## Configuration

All settings are environment variables. Copy `.env.example` to `.env` to set them:

| Variable | Default | Description |
|----------|---------|-------------|
| `TEMPLATES_PATH` | `../templates` | Path to your templates directory |
| `DCP_MODE` | `local` | `local` or `hosted` |
| `DCP_SERVER_NAME` | `DCP Policy Server` | Name shown in MCP clients |

## A note on `compare_to_local_standard`

You might expect a tool that takes a document and compares it against the team standard. MCP tools return data to the AI client — they can't invoke the AI themselves. The correct workflow is: the AI calls `fetch_policy` to get the standard, then performs the gap analysis itself. The DCP-MCP prompt resource (`dcp_usage_guide`) explains this to connected AI clients.

## Team / Hosted Mode (coming soon)

The server is designed so hosted mode is a configuration change, not a rewrite. The `PolicyStore` abstraction separates template access from the tool definitions. A future `HostedPolicyStore` can back the same tools with a central database or API, so all team members connect to one authoritative policy source.

## Running tests

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
```

Tests use synthetic templates in temporary directories. No dependency on the actual templates or the DCP repo structure.
