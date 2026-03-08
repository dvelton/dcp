════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Privacy Review
Audience:         Product team, engineering lead, privacy legal
Jurisdiction:     [Specify: GDPR, CCPA/CPRA, LGPD, Global, etc.]
Confidentiality:  Internal

Review Checklist:
□ All personal data types collected or processed are identified
□ Each data type has a stated purpose and legal basis
□ Data retention periods are defined and justified
□ Third-party data sharing is identified with recipients and purposes
□ Data subject rights are addressed (access, deletion, portability, opt-out)
□ Data processing agreement (DPA) requirements are identified
□ Cross-border data transfer mechanisms are addressed if applicable
□ Data minimization principle is applied — no collection without justification
□ Security measures are proportionate to data sensitivity
□ Privacy notice / disclosure requirements are identified
□ Consent requirements are identified and mechanism is specified
□ Impact on existing privacy commitments (privacy policy, DPA terms) is assessed

Drafting Standards:
- Clear, structured format — product teams need to act on this, not just read it
- Use tables for data mapping (data type, purpose, legal basis, retention)
- Separate "required actions" from "recommendations"
- Flag blocking issues distinctly from advisory items
- Reference specific regulatory requirements, not general principles
- Include a clear disposition: Approved / Approved with Conditions / Not Approved

Policy Check:     Before reviewing this document, verify that the
                  embedded policy is current if a policy server is available.
════════════════════════════════════════════════════════════


# PRIVACY REVIEW

| | |
|---|---|
| **Product / Feature:** | [Name and brief description] |
| **Review Requested By:** | [Name, Title] |
| **Reviewed By:** | [Name, Title — Privacy Legal] |
| **Date:** | [Date] |
| **Disposition:** | **[Approved / Approved with Conditions / Not Approved]** |

---

## Summary

[2-3 sentences describing what the product or feature does, what data it touches, and the overall privacy assessment. State the disposition upfront.]

## Feature Description

[Brief description of what the product or feature does from a user perspective. Include the user flow relevant to data collection or processing.]

## Data Mapping

| Data Type | Source | Purpose | Legal Basis | Retention | Shared With |
|-----------|--------|---------|-------------|-----------|-------------|
| [e.g., Email address] | [User input / API / Third party] | [Specific purpose] | [Consent / Legitimate interest / Contract] | [Duration] | [Recipients] |
| | | | | | |
| | | | | | |

## Privacy Analysis

### Data Collection and Minimization

[Assess whether the data collected is necessary for the stated purpose. Flag any data that appears excessive.]

### Legal Basis

[Evaluate the stated legal basis for processing. Identify any gaps or areas where the basis is unclear.]

### User Rights

[Assess how data subject rights are supported: access, correction, deletion, portability, opt-out of sale/sharing.]

### Third-Party Sharing

[Evaluate any data sharing with third parties. Identify DPA requirements.]

### Cross-Border Transfers

[If applicable, assess data transfer mechanisms for international transfers.]

### Security

[Assess whether security measures are proportionate to the sensitivity of the data.]

## Required Actions

These items must be completed before launch:

1. **[Action]** — [Description and rationale]
2. **[Action]** — [Description and rationale]

## Recommendations

These items are advisory and should be addressed when feasible:

1. **[Recommendation]** — [Description and rationale]
2. **[Recommendation]** — [Description and rationale]

## Privacy Notice Updates

[Identify any changes needed to the privacy notice or privacy policy to support this feature.]

## Conditions

[If disposition is "Approved with Conditions," list the specific conditions that must be met, with deadlines and owners.]

---

*Next review date: [Date or trigger event]*
