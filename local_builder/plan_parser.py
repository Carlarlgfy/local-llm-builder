from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED_HEADINGS = {
    "project", "user outcome", "scope", "constraints", "deliverables",
    "build stages", "run instructions", "permissions",
}


@dataclass(frozen=True)
class ParsedPlan:
    path: Path
    text: str
    project_name: str
    headings: tuple[str, ...]


def parse_plan(path: Path) -> ParsedPlan:
    path = path.resolve()
    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("proof of concept accepts Markdown plans only")
    text = path.read_text(encoding="utf-8")
    headings = tuple(match.group(2).strip().lower() for match in re.finditer(r"^(#+)\s+(.+?)\s*$", text, re.M))
    missing = sorted(REQUIRED_HEADINGS - set(headings))
    if missing:
        raise ValueError("missing required sections: " + ", ".join(missing))
    match = re.search(r"^Name:\s*(.+?)\s*$", text, re.M | re.I)
    if not match:
        raise ValueError("Project section requires a Name field")
    if "Acceptance criteria:" not in text:
        raise ValueError("at least one build stage requires Acceptance criteria")
    return ParsedPlan(path, text, match.group(1).strip(), headings)
