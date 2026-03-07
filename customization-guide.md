# Customization Guide

DCP templates are starting points, not finished products. The real value comes when you adapt them to encode your team's specific standards, risk tolerances, and institutional knowledge. This guide explains how.

---

## Customizing the Review Checklist

The review checklist is the highest-impact part of a DCP block. It directly determines what the AI checks for when reviewing or drafting a document.

### Write Specific, Actionable Items

Each checklist item should describe a concrete thing to verify, not a general area to think about.

**Weak:**
```
□ Review indemnification provisions
□ Check data handling
□ Look at termination
```

**Strong:**
```
□ Verify indemnification is mutual — flag one-sided obligations
□ Confirm data breach notification timeline does not exceed 72 hours
□ Check that termination for convenience requires 30+ days written notice
```

The difference: weak items tell the AI to "look at" something. Strong items tell it what to look *for* — the specific condition that triggers a flag.

### Encode Your Team's Red Lines

Every legal team has positions they don't compromise on. Put them in the checklist.

```
□ Reject unlimited liability — our cap is 12 months of fees paid
□ Reject exclusive jurisdiction outside of [home jurisdiction]
□ Flag any clause requiring waiver of jury trial
```

These aren't just review criteria — they're institutional knowledge that would otherwise require a senior lawyer to be in the room.

### Include Thresholds, Not Just Topics

Where possible, specify the threshold that distinguishes acceptable from flagged.

```
□ Flag non-compete clauses exceeding 12 months
□ Confirm liability cap is no less than the greater of $1M or 12 months of fees
□ Verify data retention period does not exceed 36 months
```

Without thresholds, the AI will note that a provision exists. With thresholds, it will tell you whether the provision meets your standards.

### Order by Priority

Put the most critical items first. If the AI's context window is constrained or the review is interrupted, the highest-priority checks should be at the top.

---

## Customizing Drafting Standards

Drafting standards control the tone, structure, and conventions of AI output. They're the difference between output that sounds like your team wrote it and output that sounds like a chatbot.

### Define Your Voice

Be specific about tone. "Professional" is too vague — every legal team thinks their tone is professional.

```
Drafting Standards:
- Direct and authoritative — state conclusions, don't hedge
- Use active voice: "The Supplier shall deliver" not "Delivery shall be made by the Supplier"
- No Latin unless it's a term of art with no adequate English equivalent
- Write for a smart businessperson, not a law review
```

### Specify Structure

If your team has a standard structure for a document type, encode it.

```
Drafting Standards:
- Structure: Issue, Short Answer, Background, Analysis, Recommendation
- Lead with the conclusion — do not bury it after the analysis
- Use headers for each major section
- Keep paragraphs to 3-4 sentences maximum
```

### Set Formatting Rules

Small formatting details add up across a team. Standardize them once.

```
Drafting Standards:
- Number all sections and subsections (1, 1.1, 1.1.1)
- Use "Section" not "Article" for subdivision references
- Bold defined terms on first use
- Use tables for option comparisons — never bulleted prose for side-by-side analysis
```

---

## Adding Constraints

The Constraints field tells AI what *not* to do. This is surprisingly important — AI tools have strong default behaviors that may conflict with your needs.

### Common Constraints for Legal Work

```
Constraints:
- Do not modify defined terms without flagging the change
- Do not suggest removing provisions — suggest modifications instead
- Do not reorganize the agreement structure
- Do not provide legal conclusions — present analysis and options
- Preserve the counterparty's section numbering in redline comments
```

### When to Use Constraints vs. Drafting Standards

**Drafting Standards** say "do it this way." Use them for tone, structure, and formatting.

**Constraints** say "don't do this." Use them to override AI default behaviors that cause problems — like restructuring a document you're reviewing (not drafting), or being too aggressive with deletions in a redline.

---

## Team Deployment Checklist

When rolling out customized DCP templates to your team:

1. **Start with 2-3 document types** your team produces most frequently. Don't try to cover everything at once.

2. **Have a senior lawyer review the checklists.** The value of DCP is encoding expert judgment — the checklists should reflect what your best reviewers actually check for.

3. **Test with real documents.** Before distributing templates, use them on actual (anonymized) work product. Does the AI output match your expectations? Adjust the DCP block based on what works and what doesn't.

4. **Distribute through existing channels.** Save customized templates as Word templates (.dotx) in your shared template library. Don't create a new workflow — embed DCP in the workflow your team already uses.

5. **Iterate quarterly.** Review the checklists and drafting standards every quarter. Add items that reflect lessons learned. Remove items that generate false flags. DCP blocks are living documents.

6. **Collect feedback from the team.** Ask lawyers to note when AI output missed something the checklist should have caught, or when the checklist flagged something that wasn't actually an issue. This is how institutional knowledge grows.

---

## Common Mistakes

**Checklists that are too vague.** "Review the liability section" tells the AI nothing it wouldn't do anyway. Specify what to look for.

**Checklists that are too long.** A 50-item checklist dilutes attention. Focus on the 10-15 items that matter most for each document type. If you need more granularity, create separate DCP templates for sub-types (e.g., separate templates for SaaS agreements vs. professional services agreements).

**Drafting standards that conflict with each other.** "Be concise" and "explain all legal terms in plain language" can pull in opposite directions. Prioritize: "Be concise. When legal terms are necessary, define them parenthetically on first use."

**Forgetting the Constraints field.** Without explicit constraints, AI may restructure documents you're reviewing, modify defined terms without flagging the change, or remove provisions rather than suggesting alternatives. If your workflow has "never do this" rules, put them in Constraints.

**Not testing before distributing.** A checklist that sounds right in theory may generate false positives or miss real issues in practice. Always test with real documents before team-wide rollout.
