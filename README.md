# Document Context Protocol (DCP)

DCP is an open standard for embedding AI operating instructions directly into documents. A DCP block tells any AI tool — Microsoft 365 Copilot, ChatGPT, Claude, GitHub Copilot — exactly how to work with the document: what it is, who it's for, what to check, and what standards to apply.

DCP is to documents what MCP is to models: a shared protocol that makes AI useful without setup. DCP content travels along with the document, so specifications are preserved.

---

## The Problem

When lawyers use AI, they often start interaction from scratch. They explain the document type, specify the audience, list what to check for, describe the tone they want, and then correct the output that doesn't meet professional standards. That context is often lost between sessions. It's never shared with colleagues. And the institutional knowledge that makes a senior lawyer valuable: the checklists, the instincts, the "always check for this", these stay locked in individual heads.

The result: AI output that requires editing, inconsistent quality across a team, and no leverage from the expertise that experienced lawyers have accumulated.

## How DCP Works

A DCP block is a structured section embedded at the top of a document. It's plain text — readable by humans and AI alike. No special software is needed to create, read, or use it.

Here's what a DCP block looks like in a non-disclosure agreement:

```
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Non-Disclosure Agreement
Audience:         External counsel
Jurisdiction:     Delaware
Confidentiality:  Highly confidential

Review Checklist:
□ Verify mutual confidentiality obligations
□ Check definition of "Confidential Information" for overbreadth
□ Flag non-compete clauses exceeding 12 months
□ Confirm carve-outs for independently developed information
□ Ensure termination provisions include survival period
□ Verify governing law matches specified jurisdiction

Drafting Standards:
- Formal contractual tone
- Define all capitalized terms on first use
- Include standard boilerplate (severability, waiver, entire agreement)
- Number all sections and subsections
════════════════════════════════════════════════════════════
```

When a lawyer opens this document and asks AI to "review section 3" or "draft the indemnification clause," the AI reads the DCP block and immediately understands the context. No explanation needed.

## What DCP Unlocks

### 1. Document-Type Awareness

AI knows it's working on an NDA, a data processing agreement, or an executive brief — not just "a legal document." It applies the right review criteria, structural expectations, and drafting conventions for that specific document type automatically.

### 2. Built-In Quality Control

Every DCP block includes a review checklist tailored to the document type. When a lawyer asks AI to review a contract, the AI checks for missing provisions, flags non-standard terms, and applies the team's quality standards without being prompted. The checklist is visible to the lawyer too — it's a shared source of truth.

### 3. Consistent Professional Voice

Drafting standards are encoded in the document itself. Output matches the expected tone and style for the document type: formal and precise for contracts, direct and action-oriented for executive briefs, accessible and clear for customer-facing materials. No more editing AI output from "helpful chatbot" into professional legal writing.

### 4. Institutional Knowledge, Made Portable

The expertise that makes experienced lawyers valuable — "always check for this in a DPA," "flag this pattern in vendor agreements," "structure privacy reviews this way" — is captured in the DCP block. When you share the document, you share the knowledge. The context travels with the document. When a junior lawyer uses the template, they benefit from senior-level review criteria from day one.

### 5. Tool-Agnostic

DCP is plain text. It works with any AI tool that reads document content: Microsoft 365 Copilot, GitHub Copilot, ChatGPT, Claude, or whatever comes next. There is no vendor dependency. If you can read the document, you can read the DCP block.

### 6. Zero Installation

DCP is a convention, not software. It works through document templates — Word templates (.dotx), Google Docs templates, markdown files, or any other format that supports text. Lawyers already know how to use templates. IT doesn't need to approve anything. There is nothing to install, configure, or maintain.

## Adopting DCP

### For Individual Lawyers

1. Pick a DCP template from the `templates/` directory that matches your document type.
2. Customize the review checklist and drafting standards to reflect your own priorities.
3. Start your document below the DCP block.
4. When you use any AI tool with the document, the DCP block automatically informs the AI's behavior.

That's it. No tools, no accounts, no setup.

### For Legal Teams

1. Review the DCP templates and customize them for your team's standards — your house style, your checklists, your risk thresholds.
2. Save the customized templates as Word templates (.dotx) in your team's shared template library (SharePoint, shared drive, or DMS).
3. When team members create new documents from these templates, the DCP blocks are already in place.
4. Iterate: refine checklists based on what AI gets right and wrong. The DCP blocks are living documents.

### For Enterprises

1. Establish organization-wide DCP standards through your existing template governance process.
2. Define required fields and checklists by document type.
3. Distribute DCP-enabled templates through your document management infrastructure.
4. Train teams on the standard: it's a five-minute explanation, not a technology rollout.

## Included Templates

This repository includes ready-to-use DCP templates across legal and business document types. Each template includes a complete DCP block with document-type-specific checklists and drafting standards, followed by a document skeleton showing the expected structure.

### Legal Templates

| Template | Description |
|----------|-------------|
| [Non-Disclosure Agreement](templates/nda.md) | Mutual and unilateral NDA review and drafting |
| [Data Processing Agreement](templates/dpa.md) | GDPR-aligned DPA with Article 28 checklist |
| [Legal Memo](templates/legal-memo.md) | Internal legal analysis and recommendations |
| [Executive Brief](templates/executive-brief.md) | High-level summaries for leadership decision-making |
| [Privacy Review](templates/privacy-review.md) | Product and feature privacy assessments |
| [Contract Review](templates/contract-review.md) | Third-party agreement review and redlining |
| [Vendor Security Assessment](templates/vendor-assessment.md) | Vendor risk evaluation and security review |

### Cross-Domain Templates

| Template | Description |
|----------|-------------|
| [Compliance Audit](templates/compliance-audit.md) | Regulatory and policy compliance audit reporting |
| [RFP Response](templates/rfp-response.md) | Structured response to requests for proposal |

## Examples

See the [before/after comparison](examples/before-after.md) for a side-by-side demonstration of what DCP changes in practice — same document, same prompt, dramatically different AI output.

## Customization

See the [customization guide](customization-guide.md) for detailed guidance on adapting DCP templates for your team: writing effective checklists, calibrating drafting standards, and deploying across a team.

## Frequently Asked Questions

**Does DCP require any special software?**
No. DCP is plain text embedded in a document. Any AI tool that can read the document can read the DCP block. Any text editor can create one.

**Does DCP work with Word documents?**
Yes. Place the DCP block at the top of your document or in a text box. When using Microsoft 365 Copilot or any AI tool that reads the document, the DCP block is part of the content. For team-wide adoption, save DCP-enabled documents as Word templates (.dotx).

**Can I customize the checklists?**
That's the point. The included templates are starting points. Every legal team has its own standards, risk tolerances, and house style. Customize the DCP blocks to encode your team's specific expertise.

**Does the DCP block appear in the final document?**
That's up to you. Some teams keep it visible as a quality reference. Others move it to a text box, a comment, or a collapsible section before finalizing the document. The DCP block is for the drafting and review process — how you handle it in the final version is a team decision.

**How is this different from just writing a prompt?**
A prompt is typed once, used once, and lost. A DCP block is embedded in the document template, used every time that document type is created, shared across the team, and refined over time. It's the difference between telling someone what to do each time and giving them a standing operating procedure.

**Can I use DCP outside of legal work?**
Absolutely. The protocol is document-agnostic. Any profession that produces structured documents — compliance, finance, HR, policy, procurement — can benefit from embedding AI context in their templates. Legal is a natural starting point because the documents are high-stakes and the standards are well-defined.

## Specification

See [specification.md](specification.md) for the full DCP block format, field definitions, and placement guidelines.

## Contributing

DCP is open to contributions — new templates, improvements to existing templates, and extensions to the specification. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This work is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it, adapt it, share it. 
