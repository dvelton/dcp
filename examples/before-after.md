# Before and After: DCP in Practice

This document shows the difference DCP makes using a real-world scenario. Same document, same AI tool, same prompt — the only variable is whether the document includes a DCP block.

---

## Scenario

A lawyer receives a vendor's draft NDA for review. The agreement contains a non-compete clause in Section 7 and a one-sided indemnification provision in Section 9. The lawyer asks AI: **"Review this NDA and flag any issues."**

---

## Without DCP

> **AI Response:**
>
> This appears to be a standard non-disclosure agreement. Here are some observations:
>
> - The agreement defines "Confidential Information" broadly to include all information disclosed by either party. You may want to consider whether this definition is appropriate for your purposes.
> - Section 7 includes a non-compete provision restricting competing activities for 24 months. Consider whether this aligns with your business needs.
> - Section 9 contains an indemnification clause. You may wish to review the scope of indemnification obligations.
> - The agreement is governed by the laws of New York.
> - Overall, this appears to be a reasonable NDA. I recommend having legal counsel review before signing.
>
> Would you like me to help with anything else?

**What went wrong:**
- No prioritization. The non-compete clause is buried alongside routine observations.
- Passive, hedging tone: "you may want to consider," "you may wish to review." This is not how lawyers communicate.
- Missed that a non-compete clause is unusual in an NDA — it's not just a negotiation point, it's a structural red flag.
- Missed that the indemnification is one-sided, not mutual.
- Recommended "having legal counsel review" — the user is legal counsel.
- No specific recommendations, no proposed redline language, no risk classification.

---

## With DCP

The same NDA, but with this DCP block at the top:

```
════════════════════════════════════════════════════════════
DCP — DOCUMENT CONTEXT PROTOCOL

Document Type:    Non-Disclosure Agreement
Audience:         External counsel, counterparty legal team
Jurisdiction:     Delaware
Confidentiality:  Highly confidential

Review Checklist:
□ Verify mutual confidentiality obligations
□ Check definition of "Confidential Information" for overbreadth
□ Flag non-compete clauses exceeding 12 months
□ Confirm carve-outs for independently developed information
□ Ensure termination provisions include survival period
□ Verify governing law matches specified jurisdiction
□ Flag any indemnification provisions — unusual in standard NDAs

Drafting Standards:
- Formal contractual tone
- Define all capitalized terms on first use
- Use "shall" for obligations, "may" for permissions
════════════════════════════════════════════════════════════
```

> **AI Response:**
>
> **Review Summary:** 2 Critical issues, 1 Important issue identified.
>
> ---
>
> **CRITICAL — Section 7 (Non-Compete)**
>
> This clause restricts the Receiving Party from engaging in competing activities for 24 months with no geographic limitation. Two issues:
>
> 1. **Duration exceeds threshold.** The 24-month restriction exceeds the 12-month checklist threshold. Market-standard non-competes in this context, where they exist at all, are typically 6-12 months with a defined geographic scope.
>
> 2. **Structural concern.** Non-compete clauses are atypical in mutual NDAs and may indicate the counterparty is embedding restrictive covenants outside of a proper services or employment agreement. This should be flagged to the business team.
>
> **Recommendation:** Request removal of Section 7 entirely. If the counterparty insists on a competitive restriction, negotiate to 12 months maximum with geographic limitation to [jurisdiction], and ensure the restriction is mutual.
>
> ---
>
> **CRITICAL — Section 9 (Indemnification)**
>
> The indemnification obligation is one-sided: the Receiving Party indemnifies the Disclosing Party, but not vice versa. Indemnification provisions are unusual in standard NDAs (per review checklist) and should be scrutinized.
>
> **Recommendation:** Request removal. If retained, make the obligation mutual and cap the indemnification at [amount] or limit it to breaches of confidentiality obligations.
>
> **Proposed redline:** "Each Party shall indemnify and hold harmless the other Party from and against any losses arising from the indemnifying Party's breach of its obligations under this Agreement, subject to the limitations set forth in Section [X]."
>
> ---
>
> **IMPORTANT — Section 2 (Definition of Confidential Information)**
>
> The definition captures "all information disclosed by either Party in any form." This is overbroad — it does not exclude publicly available information or information independently developed by the Receiving Party. Standard carve-outs are missing.
>
> **Recommendation:** Add standard exclusions: (i) publicly available information, (ii) information already known to the Receiving Party, (iii) independently developed information, (iv) information received from a third party without restriction.

**What changed:**
- Issues are classified by severity (Critical vs. Important) — the lawyer sees what matters first.
- The non-compete is flagged as structurally unusual, not just a negotiation preference.
- The one-sided indemnification is caught because the checklist specifically flags indemnification in NDAs.
- Each issue includes specific recommendations and proposed redline language.
- The tone is direct and professional — no "you may want to consider."
- The AI applied the review checklist systematically rather than generating surface-level observations.

---

## Why It Works

The DCP block didn't make the AI smarter. It gave the AI the same context that a senior lawyer would have walking into the review: what to look for, what's normal, what's a red flag, and how to communicate findings. The difference is that this context is encoded once and applied every time — across every NDA, by every lawyer on the team.
