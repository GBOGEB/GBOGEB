#!/usr/bin/env python3
"""Compare two exact project source sets without publishing raw source text.

RUN-DELTA v0.3 separates five views:
CHAT_ONLY | ARTEFACT_ONLY | CODE_ONLY | ALL_UNIQUE | PHYSICAL_RAW.

Text sources reuse project_knowledge_mapper classification/graph semantics.
Known binary formats are hash-tracked only and never decoded into lexical data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import project_knowledge_mapper as mapper

BINARY_SUFFIXES = {
    ".pdf", ".docx", ".xlsx", ".pptx", ".zip",
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
}
VIEW_CLASSES = {
    "CHAT_ONLY": {"CONVERSATION_TRANSCRIPT"},
    "CODE_ONLY": {
        "CODE_PYTHON", "CODE_SHELL", "WORKFLOW_CONFIG",
        "DEPENDENCY_MANIFEST", "MANIFEST_CONFIG",
    },
    "ARTEFACT_ONLY": {
        "HANDOVER_BUNDLE", "SOURCE_INDEX", "DOCUMENTATION",
        "GENERATED_ARTIFACT", "UNKNOWN",
    },
}
ANCHOR_KEYS = ("block_marker", "keb_marker", "step_in_anchor", "step_out_anchor")
DRIFT_TERMS = ("HUMAN", "VISUAL", "quantitative")
VIEW_ORDER = ("CHAT_ONLY", "ARTEFACT_ONLY", "CODE_ONLY", "ALL_UNIQUE", "PHYSICAL_RAW")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def zero_graph() -> dict:
    return {"node_count": 0, "edge_count": 0, "node_type_counts": {}}


def is_text_payload(path: Path, payload: bytes) -> bool:
    if path.suffix.lower() in BINARY_SUFFIXES or b"\x00" in payload:
        return False
    try:
        payload.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def record_for_path(path: Path) -> dict:
    payload = path.read_bytes()
    digest = sha256_bytes(payload)
    text_ok = is_text_payload(path, payload)

    if text_ok:
        text = payload.decode("utf-8")
        source_class = mapper.classify_source(path, text)
        metrics = mapper.map_text(text)
        graph = mapper.extract_block_graph(text, digest)
        parser_mode = "TEXT_PARSED"
    else:
        source_class = {
            "class": "GENERATED_ARTIFACT",
            "evidence": "BINARY_HASH_ONLY",
        }
        metrics = mapper.map_text("")
        graph = zero_graph()
        parser_mode = "BINARY_HASH_ONLY"

    return {
        "name": path.name,
        "bytes": len(payload),
        "sha256": digest,
        "parser_mode": parser_mode,
        "source_class": source_class,
        "metrics": metrics,
        "graph_summary": {
            "node_count": graph["node_count"],
            "edge_count": graph["edge_count"],
            "node_type_counts": graph["node_type_counts"],
        },
    }


def source_set_hash(records: list[dict], *, physical: bool) -> str:
    if physical:
        rows = sorted(
            f"{r['name']}|{r['sha256']}|{r['source_class']['class']}|{r['parser_mode']}"
            for r in records
        )
    else:
        by_sha = {r["sha256"]: r for r in records}
        rows = sorted(
            f"{sha}|{r['source_class']['class']}|{r['parser_mode']}"
            for sha, r in by_sha.items()
        )
    return hashlib.sha256(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()


def build_snapshot(paths: list[Path], run_id: str) -> dict:
    physical = [record_for_path(path) for path in paths]
    unique: dict[str, dict] = {}
    names_by_hash = defaultdict(list)
    classes_by_hash = defaultdict(set)

    for record in physical:
        unique.setdefault(record["sha256"], record)
        names_by_hash[record["sha256"]].append(record["name"])
        classes_by_hash[record["sha256"]].add(record["source_class"]["class"])

    duplicate_groups = [
        {"sha256": digest, "count": len(names), "names": sorted(names)}
        for digest, names in sorted(names_by_hash.items())
        if len(names) > 1
    ]
    classification_conflicts = [
        {
            "sha256": digest,
            "classes": sorted(classes),
            "names": sorted(names_by_hash[digest]),
        }
        for digest, classes in sorted(classes_by_hash.items())
        if len(classes) > 1
    ]

    unique_records = list(unique.values())
    return {
        "schema": "gbogeb.project_run_snapshot.v0.3",
        "run_id": run_id,
        "privacy_contract": "NO_RAW_SOURCE_TEXT_EMITTED",
        "physical_files": physical,
        "unique_objects": unique_records,
        "physical_count": len(physical),
        "unique_count": len(unique_records),
        "duplicate_count": len(physical) - len(unique_records),
        "duplicate_groups": duplicate_groups,
        "classification_conflicts": classification_conflicts,
        "physical_set_sha256": source_set_hash(physical, physical=True),
        "semantic_set_sha256": source_set_hash(unique_records, physical=False),
    }


def aggregate(records: list[dict]) -> dict:
    out = {
        "member_count": len(records),
        "bytes": 0,
        "graph_nodes": 0,
        "graph_edges": 0,
        "source_class_counts": defaultdict(int),
        "anchors": defaultdict(int),
        "drift_terms": defaultdict(int),
    }
    for record in records:
        out["bytes"] += record["bytes"]
        out["graph_nodes"] += record["graph_summary"]["node_count"]
        out["graph_edges"] += record["graph_summary"]["edge_count"]
        out["source_class_counts"][record["source_class"]["class"]] += 1
        structural = record["metrics"]["structural_signals"]
        lexical = record["metrics"]["lexical_frequency"]
        for key in ANCHOR_KEYS:
            out["anchors"][key] += structural.get(key, 0)
        for key in DRIFT_TERMS:
            out["drift_terms"][key] += lexical.get(key, 0)

    out["source_class_counts"] = dict(sorted(out["source_class_counts"].items()))
    out["anchors"] = dict(out["anchors"])
    out["drift_terms"] = dict(out["drift_terms"])
    return out


def view_records(snapshot: dict, view: str) -> list[dict]:
    if view == "PHYSICAL_RAW":
        return snapshot["physical_files"]
    records = snapshot["unique_objects"]
    if view == "ALL_UNIQUE":
        return records
    return [
        record for record in records
        if record["source_class"]["class"] in VIEW_CLASSES[view]
    ]


def subtract_dict(current: dict, baseline: dict) -> dict:
    return {
        key: current.get(key, 0) - baseline.get(key, 0)
        for key in sorted(set(baseline) | set(current))
    }


def delta_aggregate(baseline: dict, current: dict) -> dict:
    return {
        "member_count": current["member_count"] - baseline["member_count"],
        "bytes": current["bytes"] - baseline["bytes"],
        "graph_nodes": current["graph_nodes"] - baseline["graph_nodes"],
        "graph_edges": current["graph_edges"] - baseline["graph_edges"],
        "source_class_counts": subtract_dict(
            current["source_class_counts"], baseline["source_class_counts"]
        ),
        "anchors": subtract_dict(current["anchors"], baseline["anchors"]),
        "drift_terms": subtract_dict(
            current["drift_terms"], baseline["drift_terms"]
        ),
    }


def compare_snapshots(baseline: dict, current: dict) -> dict:
    baseline_sha = {r["sha256"] for r in baseline["unique_objects"]}
    current_sha = {r["sha256"] for r in current["unique_objects"]}

    views = {}
    for view in VIEW_ORDER:
        baseline_view = aggregate(view_records(baseline, view))
        current_view = aggregate(view_records(current, view))
        views[view] = {
            "baseline": baseline_view,
            "current": current_view,
            "delta": delta_aggregate(baseline_view, current_view),
        }

    return {
        "schema": "gbogeb.project_run_delta.v0.3",
        "privacy_contract": "NO_RAW_SOURCE_TEXT_EMITTED",
        "baseline_run": baseline["run_id"],
        "current_run": current["run_id"],
        "baseline_physical_set_sha256": baseline["physical_set_sha256"],
        "current_physical_set_sha256": current["physical_set_sha256"],
        "baseline_semantic_set_sha256": baseline["semantic_set_sha256"],
        "current_semantic_set_sha256": current["semantic_set_sha256"],
        "added_sha256": sorted(current_sha - baseline_sha),
        "removed_sha256": sorted(baseline_sha - current_sha),
        "retained_sha256_count": len(baseline_sha & current_sha),
        "baseline_counts": {
            "physical": baseline["physical_count"],
            "unique": baseline["unique_count"],
            "duplicates": baseline["duplicate_count"],
        },
        "current_counts": {
            "physical": current["physical_count"],
            "unique": current["unique_count"],
            "duplicates": current["duplicate_count"],
        },
        "classification_conflicts": {
            "baseline": baseline["classification_conflicts"],
            "current": current["classification_conflicts"],
        },
        "views": views,
    }


def load_list(path: Path) -> list[Path]:
    base = path.parent
    paths = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        candidate = Path(line)
        paths.append(candidate if candidate.is_absolute() else base / candidate)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-list", type=Path, required=True)
    parser.add_argument("--current-list", type=Path, required=True)
    parser.add_argument("--baseline-id", default="RUN_A")
    parser.add_argument("--current-id", default="RUN_B")
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    baseline = build_snapshot(load_list(args.baseline_list), args.baseline_id)
    current = build_snapshot(load_list(args.current_list), args.current_id)
    result = compare_snapshots(baseline, current)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
