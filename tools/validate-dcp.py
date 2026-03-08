#!/usr/bin/env python3
"""Validate DCP (Document Context Protocol) blocks in documents."""

import argparse, json, re, sys
from dataclasses import dataclass, field

DELIMITER_CHAR, MIN_DELIMITER_LEN = "═", 40
HEADER_DOCUMENT = "DCP — DOCUMENT CONTEXT PROTOCOL"
HEADER_POLICY_PREFIX = "DCP POLICY —"
REQUIRED_FIELDS = {
    "document": ["Document Type", "Audience"],
    "policy": ["Version", "Owner"],
}


@dataclass
class Issue:
    line: int
    message: str
    severity: str = "error"


@dataclass
class Block:
    start: int
    end: int = None
    kind: str = None
    fields: dict = field(default_factory=dict)
    issues: list = field(default_factory=list)


@dataclass
class Result:
    path: str
    valid: bool
    blocks: int = 0
    issues: list = field(default_factory=list)


def is_delim(line):
    s = line.strip()
    return len(s) >= MIN_DELIMITER_LEN and all(c == DELIMITER_CHAR for c in s)


def find_blocks(lines):
    blocks, i = [], 0
    while i < len(lines):
        if is_delim(lines[i]):
            b = Block(start=i + 1)
            i += 1
            while i < len(lines):
                if is_delim(lines[i]):
                    b.end = i + 1
                    i += 1
                    break
                i += 1
            blocks.append(b)
        else:
            i += 1
    return blocks


def analyze_block(block, lines):
    if block.end is None:
        block.issues.append(Issue(block.start,
            "DCP block opened but never closed — missing closing delimiter"))
        end = len(lines)
    else:
        end = block.end - 2
    cs = block.start  # content start (0-indexed line after opening delimiter)
    # Detect header
    for idx in range(cs, min(cs + 3, end)):
        s = lines[idx].strip()
        if not s:
            continue
        if s == HEADER_DOCUMENT:
            block.kind = "document"
            break
        elif s.startswith(HEADER_POLICY_PREFIX):
            block.kind = "policy"
            break
    else:
        block.issues.append(Issue(cs + 1,
            f"Missing DCP header. Expected '{HEADER_DOCUMENT}' or '{HEADER_POLICY_PREFIX} ...'"))
        block.kind = "document"
    # Parse fields and validate notation
    section = None  # None, "checklist", "drafting"
    for idx in range(cs, end):
        line, s = lines[idx], lines[idx].strip()
        if not s:
            continue
        if s.startswith("Review Checklist:"):
            section = "checklist"
            continue
        if s.startswith("Drafting Standards:"):
            section = "drafting"
            continue
        if section is None:
            m = re.match(r"^([A-Za-z][A-Za-z /&-]+?):\s*(.*)", s)
            if m:
                block.fields[m.group(1).strip()] = (m.group(2).strip(), idx + 1)
        elif section == "checklist":
            if s.startswith("□") or line.startswith("   ") or line.startswith("\t"):
                continue
            if s.startswith(("-", "*", "•", "[ ]", "[x]", "[X]")):
                block.issues.append(Issue(idx + 1,
                    f"Review Checklist should use □ notation, found '{s[:3].strip()}'"))
        elif section == "drafting":
            if s.startswith("-") or line.startswith("  ") or line.startswith("\t"):
                continue
            if s.startswith(("□", "*", "•")):
                block.issues.append(Issue(idx + 1,
                    f"Drafting Standards should use - notation, found '{s[:3].strip()}'",
                    severity="warning"))
    # Required fields
    for rf in REQUIRED_FIELDS.get(block.kind, []):
        if rf not in block.fields:
            block.issues.append(Issue(block.start, f"Missing required field: {rf}"))
        else:
            val, ln = block.fields[rf]
            if not val or val.startswith("["):
                block.issues.append(Issue(ln,
                    f"Field '{rf}' appears empty or is still a placeholder",
                    severity="warning"))


def validate_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except (OSError, UnicodeDecodeError) as e:
        return Result(path, valid=False, issues=[Issue(0, f"Could not read file: {e}")])
    result = Result(path, valid=True)
    blocks = find_blocks(lines)
    result.blocks = len(blocks)
    if not blocks:
        result.valid = False
        result.issues.append(Issue(1,
            f"No DCP block found. Expected delimiter of {MIN_DELIMITER_LEN}+ '{DELIMITER_CHAR}' chars."))
        return result
    if blocks[0].start > 1 and any(lines[i].strip() for i in range(blocks[0].start - 1)):
        result.issues.append(Issue(blocks[0].start,
            "DCP block does not start at the top of the file", severity="warning"))
    for b in blocks:
        analyze_block(b, lines)
        result.issues.extend(b.issues)
    if any(i.severity == "error" for i in result.issues):
        result.valid = False
    return result


def fmt_issue(issue, path):
    tag = "ERROR" if issue.severity == "error" else "WARNING"
    loc = f"{path}:{issue.line}" if issue.line > 0 else path
    return f"  {loc}: [{tag}] {issue.message}"


def to_json(r):
    return {"path": r.path, "valid": r.valid, "blocks": r.blocks,
            "errors": [{"line": i.line, "message": i.message} for i in r.issues if i.severity == "error"],
            "warnings": [{"line": i.line, "message": i.message} for i in r.issues if i.severity == "warning"]}


def main():
    p = argparse.ArgumentParser(
        description="Validate DCP (Document Context Protocol) blocks in documents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  %(prog)s document.md                  Validate a single file\n"
               "  %(prog)s *.md                         Validate all markdown files\n"
               "  %(prog)s --quiet spec.md              Exit code only (0 = valid, 1 = invalid)\n"
               "  %(prog)s --json doc.md                Machine-readable JSON output\n"
               "  find . -name '*.md' | %(prog)s        Read file paths from stdin\n")
    p.add_argument("files", nargs="*", metavar="FILE",
                   help="Files to validate. If none given, reads file paths from stdin.")
    p.add_argument("--quiet", "-q", action="store_true",
                   help="Suppress output; exit 0 if all valid, 1 otherwise.")
    p.add_argument("--json", "-j", dest="json_output", action="store_true",
                   help="Output results as JSON.")
    args = p.parse_args()
    paths = args.files
    if not paths:
        if sys.stdin.isatty():
            p.print_help()
            sys.exit(2)
        paths = [l.strip() for l in sys.stdin if l.strip()]
    if not paths:
        if not args.quiet:
            print("No files to validate.", file=sys.stderr)
        sys.exit(2)
    results = [validate_file(f) for f in paths]
    ok = all(r.valid for r in results)
    if args.json_output:
        out = [to_json(r) for r in results]
        print(json.dumps(out[0] if len(out) == 1 else out, indent=2))
    elif not args.quiet:
        for r in results:
            if r.valid and not r.issues:
                print(f"✓ {r.path} — valid ({r.blocks} DCP block(s))")
            elif r.valid:
                print(f"✓ {r.path} — valid with warnings ({r.blocks} DCP block(s))")
                for i in r.issues:
                    print(fmt_issue(i, r.path))
            else:
                print(f"✗ {r.path} — invalid")
                for i in r.issues:
                    print(fmt_issue(i, r.path))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
