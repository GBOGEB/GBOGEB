#!/usr/bin/env python3
"""Build a controlled keyword/block map from exported project text.

The mapper is intentionally dependency-free. It separates:
- lexical token frequencies;
- structural Python/control-flow signals;
- STEP_in / STEP_out anchors;
- conversation tuple hints;
- exact source-byte coverage metadata;
- physical-file volume from unique-content volume.

It does not infer engineering/compliance truth from frequency.
Raw conversation content is not copied into the emitted result.
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
    "dashboard", "GitHub", "recursive", "conversation", "GLOB", "3P", "MIP",
    "VBA", "Python", "Markdown", "Word", "Excel", "PPT", "PDF", "CSV",
    "JSON", "YAML", "receipt", "runtime", "status", "decision",
]

FLEX_PATTERNS = {
    "BLOCK": re.compile(r"\bBLOCK(?:_\d+)?\b", re.IGNORECASE),
    "STEP_in": re.compile(r"\bSTEP[_ -]?in\b", re.IGNORECASE),
    "STEP_out": re.compile(r"\bSTEP[_ -]?out\b", re.IGNORECASE),
    "digital twin": re.compile(r"\bdigital\s+twin\b", re.IGNORECASE),
    "3P": re.compile(r"\b3P(?:\*|R|C|3)?\b", re.IGNORECASE),
}

CASE_SENSITIVE_TERMS = {"RTM", "MCP", "VBA", "PPT", "PDF", "CSV", "JSON", "YAML"}

STRUCTURAL_PATTERNS = {
    "python_def": re.compile(r"^\s*def\s+[A-Za-z_]\w*\s*\(", re.MULTILINE),
    "python_if": re.compile(r"^\s*if\s+.+:", re.MULTILINE),
    "python_for": re.compile(r"^\s*for\s+.+:", re.MULTILINE),
    "python_while": re.compile(r"^\s*while\s+.+:", re.MULTILINE),
    "step_in_anchor": FLEX_PATTERNS["STEP_in"],
    "step_out_anchor": FLEX_PATTERNS["STEP_out"],
    "keb_marker": re.compile(r"\[?KEB\]?", re.IGNORECASE),
    "block_marker": FLEX_PATTERNS["BLOCK"],
}

CONVERSATION_HINT = re.compile(
    r"^(?:G|User|Assistant|DeepAgent|RouteLLM|CodeLLM|TeamLLM|ChatLLM)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lexical_count(text: str, term: str) -> int:
    if term in FLEX_PATTERNS:
        return len(FLEX_PATTERNS[term].findall(text))
    flags = 0 if term in CASE_SENSITIVE_TERMS else re.IGNORECASE
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
    raw_chunks = []
    unique_text_by_hash: dict[str, str] = {}
    paths_by_hash: dict[str, list[str]] = {}

    for path in paths:
        payload = path.read_bytes()
        text = payload.decode("utf-8", errors="replace")
        digest = sha256_bytes(payload)
        items.append({
            "path": str(path),
            "name": path.name,
            "bytes": len(payload),
            "sha256": digest,
            "metrics": map_text(text),
        })
        raw_chunks.append(text)
        unique_text_by_hash.setdefault(digest, text)
        paths_by_hash.setdefault(digest, []).append(str(path))

    duplicate_groups = [
        {
            "sha256": digest,
            "count": len(group),
            "paths": group,
        }
        for digest, group in paths_by_hash.items()
        if len(group) > 1
    ]

    raw_aggregate = map_text("\n".join(raw_chunks))
    unique_aggregate = map_text("\n".join(unique_text_by_hash.values()))

    return {
        "schema": "gbogeb.project_knowledge_map.runtime.v2",
        "source_class": "EXACT_MATERIALIZED_CORPUS",
        "privacy_contract": "NO_RAW_SOURCE_TEXT_EMITTED",
        "caveat": (
            "Counts are exact only for the files supplied to this run. "
            "They must not be represented as the full historical ChatGPT project corpus "
            "unless that corpus has been materialized and supplied."
        ),
        "physical_file_count": len(items),
        "unique_content_count": len(unique_text_by_hash),
        "duplicate_file_count": len(items) - len(unique_text_by_hash),
        "duplicate_groups": duplicate_groups,
        "files": items,
        "aggregate_raw": raw_aggregate,
        "aggregate_unique": unique_aggregate,
        "aggregate": raw_aggregate,
    }


def render_frequency_table(metrics: dict) -> list[str]:
    rows = ["| Term | Exact count |", "|---|---:|"]
    rows.extend(
        f"| {term} | {count} |"
        for term, count in metrics["lexical_frequency"].items()
    )
    return rows


def render_markdown(data: dict) -> str:
    unique = data["aggregate_unique"]
    raw = data["aggregate_raw"]
    structural = unique["structural_signals"]
    srows = ["| Signal | Unique-content count |", "|---|---:|"]
    srows.extend(f"| {term} | {count} |" for term, count in structural.items())

    return "\n".join([
        "# Project Knowledge Map — Runtime Result",
        "",
        f"**Source class:** {data['source_class']}",
        f"**Privacy contract:** {data['privacy_contract']}",
        "",
        f"> {data['caveat']}",
        "",
        "## Coverage",
        "",
        f"- Physical files: {data['physical_file_count']}",
        f"- Unique content objects: {data['unique_content_count']}",
        f"- Duplicate files: {data['duplicate_file_count']}",
        f"- Raw characters: {raw['characters']}",
        f"- Unique-content characters: {unique['characters']}",
        f"- Raw lines: {raw['lines']}",
        f"- Unique-content lines: {unique['lines']}",
        "",
        "## Lexical frequency — unique content",
        "",
        *render_frequency_table(unique),
        "",
        "## Structural signals — unique content",
        "",
        *srows,
        "",
        "## Duplicate groups",
        "",
        "~~~json",
        json.dumps(data["duplicate_groups"], indent=2, ensure_ascii=False),
        "~~~",
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
