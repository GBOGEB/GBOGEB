#!/usr/bin/env python3
"""Build a controlled keyword/block map from exported project text.

The mapper is intentionally dependency-free. It separates:
- lexical token frequencies;
- structural Python/control-flow signals;
- STEP_in / STEP_out anchors;
- conversation tuple hints;
- source coverage metadata.

It does not infer engineering/compliance truth from frequency.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

DEFAULT_TERMS = [
    "BLOCK", "def", "if", "for", "while", "STEP_in", "STEP_out", "KEB",
    "HUMAN", "VISUAL", "quantitative", "manifest", "handover",
    "digital twin", "DMAIC", "RTM", "MCP", "DeepAgent", "baseline",
    "dashboard", "GitHub", "recursive", "conversation",
]

FLEX_PATTERNS = {
    "STEP_in": re.compile(r"\bSTEP[_ -]?in\b", re.IGNORECASE),
    "STEP_out": re.compile(r"\bSTEP[_ -]?out\b", re.IGNORECASE),
    "digital twin": re.compile(r"\bdigital\s+twin\b", re.IGNORECASE),
}

STRUCTURAL_PATTERNS = {
    "python_def": re.compile(r"^\s*def\s+[A-Za-z_]\w*\s*\(", re.MULTILINE),
    "python_if": re.compile(r"^\s*if\s+.+:", re.MULTILINE),
    "python_for": re.compile(r"^\s*for\s+.+:", re.MULTILINE),
    "python_while": re.compile(r"^\s*while\s+.+:", re.MULTILINE),
    "step_in_anchor": FLEX_PATTERNS["STEP_in"],
    "step_out_anchor": FLEX_PATTERNS["STEP_out"],
    "keb_marker": re.compile(r"\[?KEB\]?", re.IGNORECASE),
    "block_marker": re.compile(r"\bBLOCK(?:_\d+)?\b", re.IGNORECASE),
}

CONVERSATION_HINT = re.compile(
    r"^(?:G|User|Assistant|DeepAgent|RouteLLM|CodeLLM|TeamLLM|ChatLLM)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def lexical_count(text: str, term: str) -> int:
    if term in FLEX_PATTERNS:
        return len(FLEX_PATTERNS[term].findall(text))
    flags = 0 if term in {"RTM", "MCP"} else re.IGNORECASE
    return len(re.findall(rf"\b{re.escape(term)}\b", text, flags))


def map_text(text: str, terms: Iterable[str] = DEFAULT_TERMS) -> dict:
    return {
        "characters": len(text),
        "lines": len(text.splitlines()),
        "lexical_frequency": {term: lexical_count(text, term) for term in terms},
        "structural_signals": {
            name: len(pattern.findall(text))
            for name, pattern in STRUCTURAL_PATTERNS.items()
        },
        "conversation_tuple_hints": len(CONVERSATION_HINT.findall(text)),
    }


def build_corpus(paths: Iterable[Path]) -> dict:
    items = []
    aggregate = ""
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        items.append({
            "path": str(path),
            "sha256": sha256_text(text),
            "metrics": map_text(text),
        })
        aggregate += text + "\n"

    return {
        "schema": "gbogeb.project_knowledge_map.runtime.v1",
        "source_class": "EXACT_MATERIALIZED_CORPUS",
        "caveat": (
            "Counts are exact only for the files supplied to this run. "
            "They must not be represented as the full historical ChatGPT project corpus "
            "unless that corpus has been materialized and supplied."
        ),
        "files": items,
        "aggregate": map_text(aggregate),
    }


def render_markdown(data: dict) -> str:
    freq = data["aggregate"]["lexical_frequency"]
    rows = ["| Term | Exact count |", "|---|---:|"]
    rows.extend(f"| {term} | {count} |" for term, count in freq.items())
    structural = data["aggregate"]["structural_signals"]
    srows = ["| Signal | Count |", "|---|---:|"]
    srows.extend(f"| {term} | {count} |" for term, count in structural.items())

    return "\n".join([
        "# Project Knowledge Map — Runtime Result",
        "",
        f"**Source class:** {data['source_class']}",
        "",
        f"> {data['caveat']}",
        "",
        "## Lexical frequency",
        "",
        *rows,
        "",
        "## Structural signals",
        "",
        *srows,
        "",
        "## Coverage",
        "",
        f"- Files: {len(data['files'])}",
        f"- Characters: {data['aggregate']['characters']}",
        f"- Lines: {data['aggregate']['lines']}",
        f"- Conversation tuple hints: {data['aggregate']['conversation_tuple_hints']}",
        "",
    ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    args = parser.parse_args()

    missing = [str(p) for p in args.inputs if not p.is_file()]
    if missing:
        parser.error("missing input file(s): " + ", ".join(missing))

    data = build_corpus(args.inputs)
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(render_markdown(data), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
