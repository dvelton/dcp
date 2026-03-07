# DCP Specification

Version 1.1

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
| **Policy Source** | Identifier or location of the canonical policy this DCP block was derived from. | contoso/legal-policies/nda-policy, https://sharepoint.contoso.com/legal/policies/nda.dcp |
| **Policy Version** | Version identifier of the canonical policy embedded in this DCP block. | nda-v4.1, 2026-Q1 |
| **Policy As-Of** | Date the canonical policy was last synced into this DCP block. | 2026-02-15 |

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

## Policy Governance

DCP blocks are always fully self-contained. Every DCP block must be complete and functional on its own — an AI tool should never need to fetch an external resource to use the document. The policy governance features described in this section are optional metadata that enable organizations to keep DCP blocks current as team policies evolve. They are never a runtime dependency.

### The Problem

When a team updates its standards — adding a new checklist item, changing a liability threshold, incorporating a new regulatory requirement — that update only reaches documents created after the change. Documents already in circulation retain the policy that was current when they were created. Over time, the gap between the team's current standards and the standards embedded in existing documents grows.

### Policy Source Fields

Three optional fields enable policy tracking:

| Field | Purpose |
|-------|---------|
| **Policy Source** | Identifies where the canonical policy lives — a URL, a file path, or an org-scoped identifier. This tells tooling where to check for updates. |
| **Policy Version** | Records which version of the canonical policy is currently embedded in this DCP block. |
| **Policy As-Of** | Records when the DCP block was last synced with the canonical policy. |

These fields are informational. If an AI tool can access the policy source, it may compare versions and alert the user that the embedded policy is outdated. If it cannot access the source, it uses the embedded DCP block as-is — the document works exactly the same either way.

Example:

```
Policy Source:    contoso/legal-policies/nda-policy
Policy Version:   nda-v4.1
Policy As-Of:     2026-02-15
```

### Policy Files

A policy file is a standalone file containing the canonical review checklist, drafting standards, and constraints for a document type. It uses the same syntax as a DCP block but contains only the fields that represent team-wide standards — not document-specific metadata like Audience or Jurisdiction.

Policy files use the `.dcp` extension by convention.

Example (`nda-policy.dcp`):

```
════════════════════════════════════════════════════════════
DCP POLICY — NDA

Version:          nda-v4.1
Last Updated:     2026-02-15
Owner:            Commercial Transactions

Review Checklist:
□ Verify mutual confidentiality obligations
□ Check definition of "Confidential Information" for overbreadth
□ Confirm standard carve-outs are present
□ Flag non-compete clauses exceeding 12 months
□ Verify data localization requirements
□ Review AI-generated content provisions

Drafting Standards:
- Formal contractual tone
- Define all capitalized terms on first use
- Use "shall" for obligations, "may" for permissions
- Plain English where possible

Constraints:
- Do not modify defined terms without flagging the change
- Do not remove provisions — suggest modifications instead
════════════════════════════════════════════════════════════
```

Policy files are maintained centrally — in a shared repository, a SharePoint library, or any location accessible to the team. They serve as the single source of truth for what the team's current standards are. When the team updates a policy file, that update can be propagated to existing documents through the batch update process described below.

### Layered DCP Blocks

When a DCP block includes policy governance fields, it operates in two layers:

1. **Base policy** — The review checklist, drafting standards, and constraints that come from the canonical policy file. These are the fields that batch propagation may update.
2. **Document-specific additions** — Items unique to this particular document. These are prefixed with "Additional" and are never overwritten by policy updates.

Example of a layered DCP block:

```
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Non-Disclosure Agreement
Audience:         External counsel
Jurisdiction:     Delaware
Confidentiality:  Highly confidential

Policy Source:    contoso/legal-policies/nda-policy
Policy Version:   nda-v4.1
Policy As-Of:     2026-02-15

Review Checklist:
□ Verify mutual confidentiality obligations
□ Check definition of "Confidential Information" for overbreadth
□ [... items from the canonical policy ...]

Drafting Standards:
- Formal contractual tone
- [... standards from the canonical policy ...]

Additional Checklist Items:
□ Verify IP assignment clause reflects joint development scope
□ Confirm residuals clause is acceptable for this engagement

Additional Constraints:
- Do not modify the non-solicitation carve-out — pre-negotiated with counterparty
════════════════════════════════════════════════════════════
```

**Merge rules:**

- The base `Review Checklist`, `Drafting Standards`, and `Constraints` fields contain the content from the canonical policy. Batch propagation may replace these fields with the current policy version.
- `Additional Checklist Items`, `Additional Drafting Standards`, and `Additional Constraints` are document-specific. They are appended to the base policy and are never modified by propagation tooling.
- Document-specific fields (`Document Type`, `Audience`, `Jurisdiction`, `Confidentiality`, etc.) are never modified by propagation tooling.

### Batch Propagation

Batch propagation is the process of updating DCP blocks in existing documents to reflect the current canonical policy. This is the primary mechanism for keeping policies current across a document library at scale.

**How it works:**

1. Tooling scans a document library (SharePoint, shared drive, repository) for documents containing DCP blocks.
2. For each document, it reads the `Policy Source` and `Policy Version` fields.
3. It compares the embedded version against the current canonical policy.
4. If the versions differ, it flags the document for update — or, with appropriate approval, replaces the base policy fields with the current canonical policy.

**Scoping rules:**

Not every document should be updated. The `Status` field (Draft, Under Review, Final, Executed) provides a natural scoping mechanism. Recommended defaults:

| Status | Propagation Behavior |
|--------|---------------------|
| **Draft** | Update automatically or with minimal approval |
| **Under Review** | Flag for review — update may affect an active negotiation |
| **Final** | Flag only — do not update without explicit approval |
| **Executed** | Do not update — the document is a historical record |

**What gets updated vs. preserved:**

| Field Type | Updated by Propagation? |
|------------|------------------------|
| Base policy fields (Review Checklist, Drafting Standards, Constraints) | Yes |
| Additional fields (Additional Checklist Items, etc.) | No — document-specific, never touched |
| Document metadata (Document Type, Audience, Jurisdiction, etc.) | No |
| Policy governance fields (Policy Source, Policy Version, Policy As-Of) | Yes — updated to reflect the new policy version |

**Approval and reporting:**

Batch propagation should produce a report showing which documents were updated, what changed, and which documents were skipped (and why). In a legal context, silent overwrites are not appropriate — the team should be able to review what changed before or after the update.

### Self-Contained Principle

The policy governance features are designed around one absolute rule: **a DCP block must always work on its own.** The `Policy Source` field is an update channel, not a runtime dependency. If an AI tool encounters a DCP block with policy governance fields but cannot access the policy source, it uses the embedded block exactly as it would any other DCP block. No functionality is lost. The document is fully self-contained.

This means:
- A document emailed to outside counsel works without access to the internal policy repo.
- A document opened in an AI tool with no network access works.
- A document created from a template five years ago still works — it just reflects the policy that was current at that time.

The policy governance layer adds the ability to *keep documents current*. It does not add a requirement to *be connected*.

## Versioning

This specification may be updated over time. The version number appears at the top of this document. DCP blocks do not require a version field — the format is designed to be forward-compatible, and AI tools should interpret any recognized fields regardless of specification version.
