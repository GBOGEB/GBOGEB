#!/usr/bin/env python3
"""Controlled project knowledge mapper.

Separates source classes before aggregation, preserves exact byte identity,
deduplicates semantic frequency by SHA-256, and emits privacy-safe structural
BLOCK graphs whose labels are hashes rather than source text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
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

SOURCE_CLASSES = (
    "CONVERSATION_TRANSCRIPT",
    "HANDOVER_BUNDLE",
    "SOURCE_INDEX",
    "DOCUMENTATION",
    "CODE_PYTHON",
    "CODE_SHELL",
    "WORKFLOW_CONFIG",
    "DEPENDENCY_MANIFEST",
    "MANIFEST_CONFIG",
    "GENERATED_ARTIFACT",
    "UNKNOWN",
)

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

SPEAKER_LINE = re.compile(
    r"^(?:G|User|Assistant|DeepAgent|RouteLLM|CodeLLM|TeamLLM|ChatLLM)\s*$",
    re.IGNORECASE,
)
MARKDOWN_HEADING = re.compile(r"^\s*#{1,6}\s+\S")
WINDOWS_PATH = re.compile(r"^[\"']?[A-Za-z]:\\[^\n]+[\"']?$")
DEPENDENCY_LINE = re.compile(r"^[A-Za-z0-9_.-]+\s*(?:==|>=|<=|~=|>|<)[^\s]+$")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


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
            name: len(pattern.findall(text)) for name, pattern in STRUCTURAL_PATTERNS.items()
        },
        "conversation_tuple_hints": sum(
            1 for line in text.splitlines() if SPEAKER_LINE.match(line.strip())
        ),
    }


def classify_source(path: Path, text: str) -> dict:
    """Classify by explicit structural evidence before aggregation."""
    suffix = path.suffix.lower()
    lines = text.splitlines()
    nonempty = [line.strip() for line in lines if line.strip()]

    speaker_count = sum(1 for line in nonempty if SPEAKER_LINE.match(line))
    relevant_posts = len(
        re.findall(r"^Relevant Posts\s*$", text, re.MULTILINE | re.IGNORECASE)
    )
    file_markers = len(re.findall(r"^----FILE:\s+", text, re.MULTILINE))
    windows_paths = sum(1 for line in nonempty if WINDOWS_PATH.match(line))
    dep_lines = sum(1 for line in nonempty if DEPENDENCY_LINE.match(line))

    if speaker_count >= 1 or relevant_posts >= 1:
        return {
            "class": "CONVERSATION_TRANSCRIPT",
            "evidence": "CONTENT_SPEAKER_OR_CHAT_MARKER",
        }
    if file_markers >= 2 or (
        "handover_manifest" in text and "definition_of_victory" in text
    ):
        return {
            "class": "HANDOVER_BUNDLE",
            "evidence": "CONTENT_EMBEDDED_FILE_OR_HANDOVER_MARKER",
        }
    if windows_paths >= 5 and (
        "master_input" in text.lower() or "main code artefact" in text.lower()
    ):
        return {"class": "SOURCE_INDEX", "evidence": "CONTENT_PATH_INVENTORY"}
    if suffix == ".py" or text.startswith("#!/usr/bin/env python"):
        return {"class": "CODE_PYTHON", "evidence": "EXTENSION_OR_SHEBANG"}
    if suffix == ".sh" or text.startswith("#!/usr/bin/env bash"):
        return {"class": "CODE_SHELL", "evidence": "EXTENSION_OR_SHEBANG"}
    if suffix in {".yml", ".yaml"} and re.search(
        r"^\s*(?:jobs|on):\s*", text, re.MULTILINE
    ):
        return {"class": "WORKFLOW_CONFIG", "evidence": "YAML_WORKFLOW_KEYS"}
    if suffix in {".yml", ".yaml", ".json"}:
        return {"class": "MANIFEST_CONFIG", "evidence": "STRUCTURED_CONFIG_EXTENSION"}
    if dep_lines >= 3 and len(nonempty) <= dep_lines + 12:
        return {"class": "DEPENDENCY_MANIFEST", "evidence": "CONTENT_DEPENDENCY_LINES"}
    if path.name.lower().startswith("readme") or suffix in {".md", ".rst"}:
        return {
            "class": "DOCUMENTATION",
            "evidence": "DOCUMENTATION_NAME_OR_EXTENSION",
        }
    if suffix in {".txt", ".log"}:
        return {"class": "GENERATED_ARTIFACT", "evidence": "TEXT_ARTIFACT_FALLBACK"}
    return {"class": "UNKNOWN", "evidence": "NO_MATCH"}


def graph_node(
    source_sha: str,
    ordinal: int,
    line_no: int,
    node_type: str,
    raw_label: str,
    evidence: str,
) -> dict:
    normalized = " ".join(raw_label.strip().split())
    return {
        "id": f"{source_sha[:12]}:{ordinal:05d}",
        "type": node_type,
        "line": line_no,
        "label_sha256": sha256_text(normalized),
        "evidence": evidence,
    }


def extract_block_graph(text: str, source_sha: str) -> dict:
    """Emit a privacy-safe sequential structural graph.

    Derived blocks come only from explicit headings or speaker markers. No
    topic, intent, owner, requirement or engineering semantics are invented.
    """
    nodes = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        node_type = None
        evidence = None
        if FLEX_PATTERNS["STEP_in"].search(stripped):
            node_type, evidence = "STEP_IN", "EXPLICIT_TOKEN"
        elif FLEX_PATTERNS["STEP_out"].search(stripped):
            node_type, evidence = "STEP_OUT", "EXPLICIT_TOKEN"
        elif FLEX_PATTERNS["BLOCK"].search(stripped):
            node_type, evidence = "BLOCK_EXPLICIT", "EXPLICIT_TOKEN"
        elif re.search(r"\[?KEB\]?", stripped, re.IGNORECASE):
            node_type, evidence = "KEB_MARKER", "EXPLICIT_TOKEN"
        elif SPEAKER_LINE.match(stripped):
            node_type = "BLOCK_CONVERSATION_TURN"
            evidence = "DERIVED_FROM_EXPLICIT_SPEAKER_MARKER"
        elif MARKDOWN_HEADING.match(stripped):
            node_type = "BLOCK_SECTION"
            evidence = "DERIVED_FROM_EXPLICIT_HEADING"
        elif re.match(r"^\s*def\s+[A-Za-z_]\w*\s*\(", line):
            node_type, evidence = "CONTROL_DEF", "EXPLICIT_CODE_STRUCTURE"
        elif re.match(r"^\s*(?:if|for|while)\s+.+:", line):
            node_type, evidence = "CONTROL_FLOW", "EXPLICIT_CODE_STRUCTURE"
        if node_type:
            nodes.append(
                graph_node(
                    source_sha,
                    len(nodes) + 1,
                    line_no,
                    node_type,
                    stripped,
                    evidence,
                )
            )

    edges = [
        {
            "from": nodes[i]["id"],
            "to": nodes[i + 1]["id"],
            "type": "NEXT_OBSERVED_STRUCTURE",
        }
        for i in range(len(nodes) - 1)
    ]
    counts = defaultdict(int)
    for node in nodes:
        counts[node["type"]] += 1
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_type_counts": dict(sorted(counts.items())),
        "nodes": nodes,
        "edges": edges,
    }


def empty_metrics() -> dict:
    return {
        "characters": 0,
        "lines": 0,
        "conversation_tuple_hints": 0,
        "lexical_frequency": defaultdict(int),
        "structural_signals": defaultdict(int),
    }


def add_metrics(acc: dict, metrics: dict) -> None:
    acc["characters"] += metrics["characters"]
    acc["lines"] += metrics["lines"]
    acc["conversation_tuple_hints"] += metrics["conversation_tuple_hints"]
    for term, count in metrics["lexical_frequency"].items():
        acc["lexical_frequency"][term] += count
    for term, count in metrics["structural_signals"].items():
        acc["structural_signals"][term] += count


def freeze_metrics(metrics: dict) -> dict:
    return {
        "characters": metrics["characters"],
        "lines": metrics["lines"],
        "conversation_tuple_hints": metrics["conversation_tuple_hints"],
        "lexical_frequency": dict(metrics["lexical_frequency"]),
        "structural_signals": dict(metrics["structural_signals"]),
    }


def build_corpus(paths: Iterable[Path]) -> dict:
    items = []
    raw_chunks = []
    unique = {}
    paths_by_hash = defaultdict(list)
    classes_by_hash = defaultdict(set)

    for path in paths:
        payload = path.read_bytes()
        text = payload.decode("utf-8", errors="replace")
        digest = sha256_bytes(payload)
        source_class = classify_source(path, text)
        graph = extract_block_graph(text, digest)
        item = {
            "path": str(path),
            "name": path.name,
            "bytes": len(payload),
            "sha256": digest,
            "source_class": source_class,
            "metrics": map_text(text),
            "graph_summary": {
                "node_count": graph["node_count"],
                "edge_count": graph["edge_count"],
                "node_type_counts": graph["node_type_counts"],
            },
        }
        items.append(item)
        raw_chunks.append(text)
        unique.setdefault(
            digest,
            {
                "text": text,
                "source_class": source_class,
                "graph": graph,
                "name": path.name,
            },
        )
        paths_by_hash[digest].append(str(path))
        classes_by_hash[digest].add(source_class["class"])

    duplicate_groups = [
        {"sha256": digest, "count": len(group), "paths": group}
        for digest, group in sorted(paths_by_hash.items())
        if len(group) > 1
    ]
    classification_conflicts = [
        {
            "sha256": digest,
            "classes": sorted(classes),
            "paths": paths_by_hash[digest],
        }
        for digest, classes in sorted(classes_by_hash.items())
        if len(classes) > 1
    ]

    by_class_acc = defaultdict(empty_metrics)
    graph_by_class = defaultdict(
        lambda: {
            "source_objects": 0,
            "node_count": 0,
            "edge_count": 0,
            "node_type_counts": defaultdict(int),
        }
    )
    unique_chunks = []
    for obj in unique.values():
        cls = obj["source_class"]["class"]
        metrics = map_text(obj["text"])
        add_metrics(by_class_acc[cls], metrics)
        unique_chunks.append(obj["text"])
        graph_by_class[cls]["source_objects"] += 1
        graph_by_class[cls]["node_count"] += obj["graph"]["node_count"]
        graph_by_class[cls]["edge_count"] += obj["graph"]["edge_count"]
        for key, value in obj["graph"]["node_type_counts"].items():
            graph_by_class[cls]["node_type_counts"][key] += value

    graph_by_class_out = {}
    for cls, value in sorted(graph_by_class.items()):
        graph_by_class_out[cls] = {
            "source_objects": value["source_objects"],
            "node_count": value["node_count"],
            "edge_count": value["edge_count"],
            "node_type_counts": dict(value["node_type_counts"]),
        }

    return {
        "schema": "gbogeb.project_knowledge_map.runtime.v3",
        "source_class": "EXACT_MATERIALIZED_CORPUS",
        "privacy_contract": "NO_RAW_SOURCE_TEXT_EMITTED",
        "aggregation_contract": "SOURCE_CLASS_FIRST_THEN_SHA256_DEDUPLICATION",
        "caveat": (
            "Counts are exact only for files supplied to this run. Source-class "
            "labels are deterministic descriptive classifications and do not "
            "transfer engineering or document authority."
        ),
        "physical_file_count": len(items),
        "unique_content_count": len(unique),
        "duplicate_file_count": len(items) - len(unique),
        "duplicate_groups": duplicate_groups,
        "classification_conflicts": classification_conflicts,
        "files": items,
        "aggregate_raw": map_text("\n".join(raw_chunks)),
        "aggregate_unique": map_text("\n".join(unique_chunks)),
        "aggregate_unique_by_source_class": {
            cls: freeze_metrics(metrics)
            for cls, metrics in sorted(by_class_acc.items())
        },
        "block_graph_by_source_class": graph_by_class_out,
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
    class_rows = [
        "| Source class | Unique chars | Unique lines | Graph nodes | Graph edges |",
        "|---|---:|---:|---:|---:|",
    ]
    for cls, metrics in data["aggregate_unique_by_source_class"].items():
        graph = data["block_graph_by_source_class"].get(cls, {})
        class_rows.append(
            f"| {cls} | {metrics['characters']} | {metrics['lines']} | "
            f"{graph.get('node_count', 0)} | {graph.get('edge_count', 0)} |"
        )
    return "\n".join(
        [
            "# Project Knowledge Map — Runtime Result",
            "",
            f"**Source class:** {data['source_class']}",
            f"**Privacy contract:** {data['privacy_contract']}",
            f"**Aggregation contract:** {data['aggregation_contract']}",
            "",
            f"> {data['caveat']}",
            "",
            "## Coverage",
            "",
            f"- Physical files: {data['physical_file_count']}",
            f"- Unique content objects: {data['unique_content_count']}",
            f"- Duplicate files: {data['duplicate_file_count']}",
            f"- Classification conflicts: {len(data['classification_conflicts'])}",
            f"- Raw characters: {raw['characters']}",
            f"- Unique-content characters: {unique['characters']}",
            "",
            "## Source-class purity",
            "",
            *class_rows,
            "",
            "## Lexical frequency — all unique content",
            "",
            *render_frequency_table(unique),
            "",
            "## Duplicate groups",
            "",
            "~~~json",
            json.dumps(data["duplicate_groups"], indent=2, ensure_ascii=False),
            "~~~",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    parser.add_argument("--graph-out", type=Path)
    args = parser.parse_args()

    missing = [str(path) for path in args.inputs if not path.is_file()]
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
    if args.graph_out:
        graph_payload = {
            "schema": "gbogeb.project_block_graph_summary.v1",
            "privacy_contract": data["privacy_contract"],
            "by_source_class": data["block_graph_by_source_class"],
            "files": [
                {
                    "name": item["name"],
                    "sha256": item["sha256"],
                    "source_class": item["source_class"],
                    "graph_summary": item["graph_summary"],
                }
                for item in data["files"]
            ],
        }
        args.graph_out.parent.mkdir(parents=True, exist_ok=True)
        args.graph_out.write_text(
            json.dumps(graph_payload, indent=2) + "\n", encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
