════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Vendor Security Assessment
Audience:         Security team, procurement, vendor management, legal
Confidentiality:  Internal

Review Checklist:
□ Verify vendor provides SOC 2 Type II report (or equivalent: ISO 27001,
   SOC 3) — check report date is within the last 12 months
□ Confirm data types the vendor will access or process — flag any PII,
   PHI, financial data, or credentials
□ Check data residency — confirm where data is stored and processed,
   flag any jurisdictions that conflict with company policy
□ Verify encryption standards: at rest (AES-256 or equivalent) and
   in transit (TLS 1.2+)
□ Review access controls — confirm RBAC, MFA for administrative access,
   and least-privilege principles
□ Check incident response — confirm vendor has a documented IR plan
   with defined notification timeline (should not exceed 72 hours)
□ Review sub-processor/sub-contractor practices — confirm vendor
   discloses sub-processors and flows down security obligations
□ Verify business continuity and disaster recovery — confirm RPO and
   RTO commitments are documented
□ Check data retention and deletion — confirm vendor will delete data
   upon termination within a defined timeline with certification
□ Review insurance coverage — confirm cyber liability insurance with
   adequate limits
□ Verify penetration testing — confirm annual third-party pen testing
   with remediation of critical findings
□ Check employee security practices — background checks, security
   training, access deprovisioning on termination

Drafting Standards:
- Use clear risk ratings: Critical / High / Medium / Low / Acceptable
- Structure findings by security domain, not by questionnaire order
- For each finding, state: the gap, the risk it creates, and the
  recommended remediation or contractual mitigation
- Distinguish between "must resolve before engagement" and "accept
  with contractual mitigation"
- Include a clear disposition: Approved / Conditionally Approved / Not Approved
════════════════════════════════════════════════════════════


# VENDOR SECURITY ASSESSMENT

| | |
|---|---|
| **Vendor:** | [Vendor name] |
| **Product/Service:** | [What the vendor provides] |
| **Business Owner:** | [Name, Title] |
| **Assessed By:** | [Name, Title — Security/Legal] |
| **Date:** | [Date] |
| **Disposition:** | **[Approved / Conditionally Approved / Not Approved]** |

---

## Summary

[2-3 sentences describing the vendor, the service, what data is involved, and the overall risk assessment. State the disposition upfront.]

**Risk Overview:** [X] Critical | [Y] High | [Z] Medium | [W] Low

## Vendor Overview

| | |
|---|---|
| **Company** | [Legal name, jurisdiction of incorporation] |
| **Service Description** | [What they do for us] |
| **Data Access** | [What data types the vendor accesses or processes] |
| **Data Residency** | [Where data is stored/processed] |
| **Integration Type** | [API, file transfer, direct access, hosted, etc.] |
| **Contract Value** | [Annual value or total contract value] |

## Certifications and Compliance

| Certification | Status | Report Date | Expiration |
|--------------|--------|-------------|------------|
| SOC 2 Type II | [Yes/No/In Progress] | [Date] | [Date] |
| ISO 27001 | [Yes/No/In Progress] | [Date] | [Date] |
| GDPR Compliance | [Yes/No/Self-Attested] | | |
| HIPAA (if applicable) | [Yes/No/N/A] | | |
| [Other] | | | |

## Security Assessment by Domain

### Data Protection

**Rating: [Critical / High / Medium / Low / Acceptable]**

[Assess encryption, data classification, DLP, backup procedures]

### Access Management

**Rating: [Critical / High / Medium / Low / Acceptable]**

[Assess RBAC, MFA, privileged access management, access reviews]

### Network and Infrastructure

**Rating: [Critical / High / Medium / Low / Acceptable]**

[Assess network segmentation, firewall rules, cloud security posture]

### Incident Response

**Rating: [Critical / High / Medium / Low / Acceptable]**

[Assess IR plan, notification timeline, forensic capability]

### Business Continuity

**Rating: [Critical / High / Medium / Low / Acceptable]**

[Assess BCP/DR, RPO/RTO, testing frequency]

### Personnel Security

**Rating: [Critical / High / Medium / Low / Acceptable]**

[Assess background checks, security training, access deprovisioning]

### Third-Party / Sub-Processor Management

**Rating: [Critical / High / Medium / Low / Acceptable]**

[Assess sub-processor disclosure, security flow-down, monitoring]

## Findings

### Must Resolve Before Engagement

| # | Domain | Finding | Risk | Remediation Required |
|---|--------|---------|------|---------------------|
| 1 | [Domain] | [Specific gap] | [Risk description] | [Required action] |
| 2 | [Domain] | [Specific gap] | [Risk description] | [Required action] |

### Accept with Contractual Mitigation

| # | Domain | Finding | Risk | Contractual Mitigation |
|---|--------|---------|------|----------------------|
| 1 | [Domain] | [Specific gap] | [Risk description] | [Contract provision needed] |
| 2 | [Domain] | [Specific gap] | [Risk description] | [Contract provision needed] |

### Advisory (Low Risk)

- [Finding and recommendation]
- [Finding and recommendation]

## Contractual Requirements

Based on this assessment, the vendor agreement should include:

- [ ] Data Processing Agreement with [specific requirements]
- [ ] Security exhibit specifying [minimum controls]
- [ ] Breach notification obligation within [X] hours
- [ ] Annual SOC 2 Type II report delivery obligation
- [ ] Right to audit [specify scope and frequency]
- [ ] Cyber liability insurance of at least $[X]M
- [ ] Data deletion certification upon termination within [X] days
- [ ] [Other requirements based on findings]

## Conditions for Approval

[If conditionally approved, list specific conditions with deadlines and owners]

1. **[Condition]** — Deadline: [Date] — Owner: [Name]
2. **[Condition]** — Deadline: [Date] — Owner: [Name]

## Next Steps

1. **[Action]** — [Owner] — [Deadline]
2. **[Action]** — [Owner] — [Deadline]

---

*Reassessment due: [Date or trigger — e.g., annually, upon contract renewal, or upon material change in service]*
