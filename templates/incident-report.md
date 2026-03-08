════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Incident Report
Audience:         Incident review board, engineering leadership, affected teams
Confidentiality:  [Specify: Internal / Confidential / Restricted]

Review Checklist:
□ Timeline is complete and timestamped — every significant event from
   detection through resolution is accounted for, using a consistent timezone
□ Root cause is identified, not just the proximate cause — the analysis
   explains why the failure was possible, not just what triggered it
□ Impact is quantified: number of users affected, duration, revenue impact,
   data exposure, or SLA violations — not described in vague terms
□ Detection method is documented — how was the incident discovered, and
   what should have caught it earlier
□ Time to detect (TTD) and time to resolve (TTR) are explicitly stated
□ Remediation actions are specific, have assigned owners, and have deadlines —
   not "we should improve monitoring"
□ Contributing factors beyond the technical root cause are addressed:
   process gaps, missing runbooks, unclear ownership, insufficient testing
□ Lessons learned are actionable and tied to specific remediation items —
   not generic observations
□ Severity classification is justified against the team's severity criteria
□ Report is blameless — focuses on systems and processes, not individuals
□ Customer communication is documented: what was communicated, when, and
   to whom

Drafting Standards:
- Write in past tense — this is a record of what happened
- Use UTC timestamps throughout unless local time is specifically relevant
- Be precise with technical details but write the executive summary for
  a non-technical reader
- Separate facts from interpretation — the timeline is facts, the root
  cause analysis is interpretation, label them accordingly
- Include diagrams for complex failure cascades
- Do not editorialize or assign blame — describe what happened and what
  the system allowed to happen

Policy Check:     Before reviewing this document, verify that the
                  embedded policy is current if a policy server is available.
════════════════════════════════════════════════════════════


# INCIDENT REPORT: [SHORT DESCRIPTION]

| | |
|---|---|
| **Incident ID:** | [e.g., INC-2026-0142] |
| **Severity:** | [Sev1 / Sev2 / Sev3 / Sev4] |
| **Status:** | [Active / Resolved / Closed] |
| **Date of Incident:** | [YYYY-MM-DD] |
| **Duration:** | [Total time from detection to resolution] |
| **Report Author:** | [Name] |
| **Incident Commander:** | [Name] |
| **Report Date:** | [Date] |

---

## Executive Summary

[In 3-5 sentences, describe what happened, the impact, how it was resolved, and the most important follow-up action. Write for someone who will not read the rest of the report.]

**Impact:** [X] users affected | [Duration] of degraded service | [Revenue/SLA impact if applicable]

**Time to Detect (TTD):** [Duration from incident start to detection]
**Time to Resolve (TTR):** [Duration from detection to resolution]

## Timeline

All times in UTC.

| Time (UTC) | Event |
|-----------|-------|
| [HH:MM] | [First sign of the issue — what happened in the system] |
| [HH:MM] | [Detection — how the incident was discovered: alert, user report, etc.] |
| [HH:MM] | [Initial response — who was paged, what was the first action] |
| [HH:MM] | [Escalation or additional responders engaged] |
| [HH:MM] | [Key diagnostic step or hypothesis tested] |
| [HH:MM] | [Mitigation applied — what action reduced or stopped the impact] |
| [HH:MM] | [Resolution confirmed — how was recovery verified] |
| [HH:MM] | [All-clear communicated to stakeholders] |

## Impact

### User Impact

[Describe what users experienced. Quantify: number of affected users, failed requests, error rates, degraded functionality.]

### Business Impact

[Revenue impact, SLA violations, contractual obligations affected, regulatory notification requirements.]

### Data Impact

[Was any data lost, corrupted, or exposed? If yes, describe the scope and any notification obligations.]

## Root Cause Analysis

### Proximate Cause

[What directly triggered the incident. Be specific: the deploy, the config change, the query, the traffic spike.]

### Root Cause

[Why was the system vulnerable to this trigger? What underlying condition made this failure possible? Go deeper than the trigger.]

### Contributing Factors

- [Process gap, missing test, unclear ownership, insufficient monitoring, or other systemic factor that allowed this to happen]
- [Another contributing factor]

## Detection

[How was the incident detected? Was it an alert, a customer report, an internal observation? If detection was delayed, explain what monitoring gaps existed.]

**Expected detection method:** [What should have caught this]
**Actual detection method:** [What did catch this]
**Detection gap:** [If different from expected, explain why]

## Response

[Describe the response process. Who was involved, what decisions were made, and how effective was the response. Note any friction in the response process: missing runbooks, unclear escalation paths, tooling gaps.]

## Customer Communication

| Time (UTC) | Channel | Audience | Message Summary |
|-----------|---------|----------|-----------------|
| [HH:MM] | [Status page / Email / Support] | [Affected customers / All customers] | [What was communicated] |

## Remediation

| # | Action Item | Owner | Deadline | Priority | Status |
|---|------------|-------|----------|----------|--------|
| 1 | [Specific action to prevent recurrence] | [Name] | [Date] | [P0 / P1 / P2] | [Open / In Progress / Done] |
| 2 | [Specific action to improve detection] | [Name] | [Date] | [P0 / P1 / P2] | [Open / In Progress / Done] |
| 3 | [Specific action to improve response] | [Name] | [Date] | [P0 / P1 / P2] | [Open / In Progress / Done] |

## Lessons Learned

### What went well

- [Something that worked effectively during detection, response, or communication]

### What could be improved

- [Something that slowed down detection, response, or recovery — tied to a specific remediation item above]

### Where we got lucky

- [Something that reduced impact by chance rather than by design — these are future risks]

---

*Review meeting: [Date, time, attendees]*
*Next review of remediation items: [Date]*
