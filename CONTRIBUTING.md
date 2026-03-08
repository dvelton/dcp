# Contributing to DCP

DCP is a community project. Contributions of new templates, improvements to existing templates, and extensions of the specification are welcome.

---

## How to Contribute a Template

### Template Requirements

Every DCP template must include:

1. **A complete DCP block** at the top of the file, following the format defined in [specification.md](specification.md).
2. **Required fields:** Document Type and Audience.
3. **A review checklist** with specific, actionable items (not vague topic areas).
4. **Drafting standards** appropriate to the document type.
5. **A document skeleton** below the DCP block showing the expected structure for the document type.

### Quality Standards

- **Checklists should reflect practitioner expertise.** Items should encode what an experienced professional actually checks for, not generic guidance that could be found in a textbook.
- **Drafting standards should be specific enough to produce consistent output.** "Professional tone" is insufficient. Describe what professional means for this document type.
- **Document skeletons should be immediately usable.** A lawyer (or other professional) should be able to start working in the template without restructuring it.
- **Plain language.** DCP templates are read by AI tools and by humans. Write for both audiences.

### File Naming

- Use lowercase with hyphens: `vendor-assessment.md`, `board-resolution.md`
- Place legal templates in `templates/`
- Place non-legal templates in `templates/` with a clear document type name

### Submission Process

1. Fork this repository.
2. Create your template following the requirements above.
3. Test the template with at least one AI tool (Microsoft 365 Copilot, ChatGPT, Claude, or GitHub Copilot) to verify the DCP block produces the expected behavior.
4. Submit a pull request with:
   - The template file
   - A brief description of the document type and target audience
   - What AI tool(s) you tested with

---

## Improving Existing Templates

If you have domain expertise that would strengthen an existing template's checklist or drafting standards, open a pull request with your proposed changes. Include a brief explanation of why the change improves the template — ideally with an example of the issue it addresses.

---

## Non-Legal Templates

DCP is domain-agnostic. Templates for any profession that produces structured documents are welcome: compliance, finance, HR, procurement, policy, healthcare, engineering. The same quality standards apply — checklists should encode real practitioner judgment, not generic advice.

---

## Specification Changes

Proposed changes to the DCP specification should be submitted as issues for discussion before implementation. The specification is intentionally minimal — changes should demonstrate clear value across multiple document types and domains before being added to the standard.

---

## Code of Conduct

Be professional, be constructive, be respectful. This project exists to make professionals more effective with AI. Contributions should reflect that purpose.

## License

By contributing, you agree that your contributions will be released under the same [MIT](LICENSE) license as the rest of this project.
