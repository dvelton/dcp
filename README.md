# Document Context Protocol (DCP)

DCP is an open standard for embedding AI operating instructions directly into documents. A DCP block sits at the top of a document and tells any AI tool (Microsoft 365 Copilot, ChatGPT, Claude, GitHub Copilot) what the document is, who it's for, what to check, and what standards to apply.

The block is plain text. It works in Word, Google Docs, markdown, or anything else that holds text. There's nothing to install.

## The Problem

When lawyers use AI with a document, they spend time explaining context that should already be obvious: what kind of document it is, what checklist to apply, what tone to use, what to watch out for. That context is typed once, used once, and lost. It never gets shared with colleagues. The checklists and instincts that make an experienced lawyer valuable stay locked in individual heads.

## How DCP Works

A DCP block is a structured section at the top of a document. Here's what one looks like in an NDA:

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

When a lawyer opens this document and asks AI to "review section 3" or "draft the indemnification clause," the AI reads the DCP block and applies the right context without being prompted.

## Why This Is Useful

The document carries its own instructions. AI knows it's working on an NDA (not just "a legal document") and applies the appropriate review criteria, structure, and tone. The review checklist acts as built-in quality control: AI checks for missing provisions and flags non-standard terms against the team's actual standards, not generic ones.

When you share the document, you share the expertise. A junior lawyer working from a DCP-enabled template gets the benefit of senior-level review criteria from day one. The institutional knowledge that usually stays in people's heads ("always check for this in a DPA," "flag this pattern in vendor agreements") gets encoded in the document itself.

Because DCP blocks are plain text, they work with any AI tool that reads document content. No vendor dependency, no integration work.

## Keeping Policies Current

DCP blocks are self-contained by design. But policies change, and when a team updates its NDA checklist to add a new regulatory requirement, that update only reaches documents created after the change.

Three optional fields handle this: `Policy Source`, `Policy Version`, and `Policy As-Of`. These record where the embedded policy came from and when it was last synced. They're metadata, not dependencies. If an AI tool can reach the policy source, it can check whether the document's policy is current and alert the user. If it can't, the embedded DCP block works exactly as it always has.

The canonical policies themselves live in standalone `.dcp` files maintained centrally by the team. Batch propagation tooling can scan a document library, identify stale DCP blocks, and update them, with scoping rules that distinguish between drafts (update freely), documents under review (flag first), and executed agreements (leave alone). Document-specific additions (prefixed with "Additional") are never overwritten.

See the [specification](specification.md) for full details on policy governance, layered DCP blocks, and batch propagation.

## Getting Started

Pick a template from the `templates/` directory that matches your document type. Customize the review checklist and drafting standards for your own priorities. Start your document below the DCP block. When you use any AI tool with the document, the DCP block informs the AI's behavior automatically.

For team-wide adoption, save customized templates as Word templates (.dotx) in your shared template library. When team members create new documents from these templates, the DCP blocks are already in place.

## Templates

### Legal

| Template | Description |
|----------|-------------|
| [Non-Disclosure Agreement](templates/nda.md) | Mutual and unilateral NDA review and drafting |
| [Data Processing Agreement](templates/dpa.md) | GDPR-aligned DPA with Article 28 checklist |
| [Legal Memo](templates/legal-memo.md) | Internal legal analysis and recommendations |
| [Executive Brief](templates/executive-brief.md) | High-level summaries for leadership decision-making |
| [Privacy Review](templates/privacy-review.md) | Product and feature privacy assessments |
| [Contract Review](templates/contract-review.md) | Third-party agreement review and redlining |
| [Vendor Security Assessment](templates/vendor-assessment.md) | Vendor risk evaluation and security review |

### Cross-Domain

| Template | Description |
|----------|-------------|
| [Technical Specification](templates/technical-spec.md) | Engineering design documents and architecture proposals |
| [Project Proposal](templates/project-proposal.md) | New project or initiative proposals for leadership approval |
| [Incident Report](templates/incident-report.md) | Post-incident documentation for outages, security events, and safety incidents |
| [Policy Document](templates/policy-document.md) | Organizational policies (IT, HR, security, compliance) |
| [Compliance Audit](templates/compliance-audit.md) | Regulatory and policy compliance audit reporting |
| [RFP Response](templates/rfp-response.md) | Structured response to requests for proposal |

### Word Templates

Pre-formatted Word (.docx) versions are available in [`templates/word/`](templates/word/) for the most commonly used document types. Open them in Word, save as a Word template (.dotx) in your shared template library, and your team can start creating DCP-enabled documents immediately.

## Tools

### DCP Validator

A Python script that checks whether a document's DCP block is well-formed. No dependencies beyond Python 3.

```
python tools/validate-dcp.py document.md

# Validate multiple files
python tools/validate-dcp.py templates/*.md

# Machine-readable output
python tools/validate-dcp.py --json document.md

# Exit code only (for CI pipelines)
python tools/validate-dcp.py --quiet document.md
```

The validator checks for correct delimiters, the required header line, required fields (Document Type and Audience), proper checklist notation, and structural issues like missing closing delimiters.

## Examples

See the [before/after comparison](examples/before-after.md) for a side-by-side look at what DCP changes in practice.

## FAQ

**Does DCP work with Word documents?**
Yes. Place the DCP block at the top of your document. Microsoft 365 Copilot reads it as part of the document content. For team-wide use, save DCP-enabled documents as Word templates (.dotx).

**Does the DCP block appear in the final document?**
Up to you. Some teams keep it visible as a quality reference. Others move it to a text box or collapsible section before finalizing. The block is for drafting and review; how you handle it in the final version is a team decision.

**How is this different from writing a prompt?**
A prompt is typed once and lost. A DCP block lives in the document template, gets used every time that document type is created, and gets shared across the team. It accumulates refinements over time.

## Further Reading

- [Specification](specification.md) for the full block format, field definitions, and placement guidelines
- [Customization guide](customization-guide.md) for adapting templates to your team's standards

## Contributing

DCP is open to contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
