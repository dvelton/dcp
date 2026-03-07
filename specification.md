# DCP Specification

Version 1.0

## Overview

A DCP block is a structured, human-readable text section embedded in a document that provides AI tools with operational context. It defines what the document is, who it's for, how to work with it, and what standards apply.

## Block Format

A DCP block is delimited by horizontal borders and begins with a header line:

```
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

[fields]
════════════════════════════════════════════════════════════
```

### Delimiter

The top and bottom borders use the double horizontal bar character (═), repeated to form a visible boundary. The minimum length is 40 characters. The delimiter serves two purposes: it signals to AI tools that a DCP block is present, and it visually separates the block from document content for human readers.

### Header

The first line inside the block must read `DCP — DOCUMENT CONTEXT PROTOCOL` (using an em dash). This identifies the block to AI tools and distinguishes it from other document metadata.

## Fields

### Required Fields

Every DCP block must include these fields:

| Field | Description | Example |
|-------|-------------|---------|
| **Document Type** | The category of document. | Non-Disclosure Agreement, Legal Memo, Executive Brief |
| **Audience** | The intended reader(s) of the document. | External counsel, Board of Directors, Internal team |

### Recommended Fields

These fields significantly improve AI behavior and should be included when applicable:

| Field | Description | Example |
|-------|-------------|---------|
| **Jurisdiction** | Applicable law or governing jurisdiction. | Delaware, EU (GDPR), California |
| **Confidentiality** | Classification level. | Public, Internal, Confidential, Highly Confidential |
| **Review Checklist** | Specific items AI should verify or flag. | (See below) |
| **Drafting Standards** | Tone, structure, and formatting rules. | (See below) |

### Optional Fields

Teams may add any fields that support their workflow:

| Field | Description | Example |
|-------|-------------|---------|
| **Purpose** | What this specific document accomplishes. | Governs mutual disclosure of proprietary information between X and Y |
| **Version** | Document version or revision identifier. | 2.1, Draft 3 |
| **Owner** | Responsible team or individual. | Privacy Legal, Commercial Transactions |
| **Status** | Current document lifecycle stage. | Draft, Under Review, Final, Executed |
| **Related Documents** | Cross-references to related agreements. | Master Services Agreement (Ref: MSA-2024-001) |
| **Constraints** | Things AI should not do with this document. | Do not modify defined terms; Do not remove existing indemnification provisions |
| **Definitions** | Key terms and their meanings in context. | "Disclosing Party" refers to the party sharing Confidential Information |

### Structured Fields

**Review Checklist** uses checkbox notation:

```
Review Checklist:
□ Verify mutual confidentiality obligations
□ Check non-compete scope and duration
□ Flag non-standard indemnification terms
```

**Drafting Standards** uses bullet notation:

```
Drafting Standards:
- Formal contractual tone
- Define all capitalized terms on first use
- Plain English where possible; avoid unnecessary Latin
```

**Constraints** uses bullet notation:

```
Constraints:
- Do not alter defined terms without flagging the change
- Preserve existing limitation of liability structure
- Do not remove any representations or warranties
```

## Placement

The DCP block should appear **at the top of the document**, before the substantive content begins. This ensures AI tools encounter the instructions before processing the document body.

### Format-Specific Guidance

| Format | Placement |
|--------|-----------|
| **Markdown** | First element in the file, before any headings. |
| **Word (.docx)** | Top of the document body, or in a text box on the first page. May also be placed in a collapsible section or document header. |
| **Google Docs** | Top of the document, optionally in a bordered text box. |
| **PDF** | First page, if the document is generated from a DCP-enabled source. |
| **Plain text** | First block in the file. |

## Compatibility

DCP blocks are plain text. They require no parser, no schema validator, and no special tooling. Any AI tool that reads document content will encounter the DCP block and can use its contents to inform its behavior.

DCP has been tested and is effective with:

- Microsoft 365 Copilot (Word, Outlook)
- GitHub Copilot
- ChatGPT (via document upload or paste)
- Claude (via document upload or paste)

### Relationship to Other Standards

**MCP (Model Context Protocol)**: MCP provides tools and context to AI models at the infrastructure level. DCP provides context at the document level. They are complementary — MCP defines what an AI can do; DCP defines how it should work with a specific document.

**GitHub Copilot Instructions (.instructions.md, AGENTS.md)**: These files provide repo-level or directory-level AI instructions for software development. DCP applies the same principle to individual documents in any domain. For teams working in git repositories, DCP blocks within documents and Copilot instruction files at the repo level can work together.

## Versioning

This specification may be updated over time. The version number appears at the top of this document. DCP blocks do not require a version field — the format is designed to be forward-compatible, and AI tools should interpret any recognized fields regardless of specification version.
