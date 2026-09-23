import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAPPER_PATH = ROOT / "scripts" / "project_knowledge_mapper.py"
DELTA_PATH = ROOT / "scripts" / "project_run_delta.py"

mapper_spec = importlib.util.spec_from_file_location("project_knowledge_mapper", MAPPER_PATH)
mapper = importlib.util.module_from_spec(mapper_spec)
assert mapper_spec and mapper_spec.loader
mapper_spec.loader.exec_module(mapper)

import sys
sys.modules["project_knowledge_mapper"] = mapper

delta_spec = importlib.util.spec_from_file_location("project_run_delta", DELTA_PATH)
delta = importlib.util.module_from_spec(delta_spec)
assert delta_spec and delta_spec.loader
delta_spec.loader.exec_module(delta)


class ProjectRunDeltaTests(unittest.TestCase):
    def test_five_views_separate_duplicate_growth(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            chat = root / "chat.txt"
            chat_copy = root / "chat_copy.txt"
            doc = root / "README.md"
            code = root / "tool.py"
            code2 = root / "tool2.py"
            binary = root / "preview.pdf"

            chat.write_text("RouteLLM\nBLOCK KEB HUMAN VISUAL\n", encoding="utf-8")
            chat_copy.write_bytes(chat.read_bytes())
            doc.write_text("# A\nVISUAL\n", encoding="utf-8")
            code.write_text("#!/usr/bin/env python3\ndef a():\n    pass\n", encoding="utf-8")
            code2.write_text("#!/usr/bin/env python3\ndef b():\n    if True:\n        pass\n", encoding="utf-8")
            binary.write_bytes(b"%PDF-1.7\x00secret-binary-payload")

            baseline = delta.build_snapshot([chat, doc, code], "RUN_A")
            current = delta.build_snapshot(
                [chat, chat_copy, doc, code, code2, binary], "RUN_B"
            )
            result = delta.compare_snapshots(baseline, current)

        self.assertEqual(result["baseline_counts"]["physical"], 3)
        self.assertEqual(result["current_counts"]["physical"], 6)
        self.assertEqual(result["current_counts"]["unique"], 5)
        self.assertEqual(result["views"]["CHAT_ONLY"]["delta"]["member_count"], 0)
        self.assertEqual(result["views"]["PHYSICAL_RAW"]["delta"]["member_count"], 3)
        self.assertEqual(result["views"]["ALL_UNIQUE"]["delta"]["member_count"], 2)
        self.assertEqual(result["views"]["CODE_ONLY"]["delta"]["member_count"], 1)
        self.assertEqual(result["views"]["ARTEFACT_ONLY"]["delta"]["member_count"], 1)

    def test_anchor_and_human_visual_quantitative_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            base = root / "README_base.md"
            extra = root / "README_extra.md"
            base.write_text("# Base\n", encoding="utf-8")
            extra.write_text(
                "# Extra\nBLOCK KEB STEP_in STEP_out HUMAN VISUAL quantitative\n",
                encoding="utf-8",
            )
            baseline = delta.build_snapshot([base], "RUN_A")
            current = delta.build_snapshot([base, extra], "RUN_B")
            result = delta.compare_snapshots(baseline, current)

        drift = result["views"]["ARTEFACT_ONLY"]["delta"]
        self.assertEqual(drift["anchors"]["block_marker"], 1)
        self.assertEqual(drift["anchors"]["keb_marker"], 1)
        self.assertEqual(drift["anchors"]["step_in_anchor"], 1)
        self.assertEqual(drift["anchors"]["step_out_anchor"], 1)
        self.assertEqual(drift["drift_terms"]["HUMAN"], 1)
        self.assertEqual(drift["drift_terms"]["VISUAL"], 1)
        self.assertEqual(drift["drift_terms"]["quantitative"], 1)

    def test_removed_sha_is_fail_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            a = root / "README_a.md"
            b = root / "README_b.md"
            a.write_text("# A\n", encoding="utf-8")
            b.write_text("# B\n", encoding="utf-8")
            baseline = delta.build_snapshot([a, b], "RUN_A")
            current = delta.build_snapshot([a], "RUN_B")
            result = delta.compare_snapshots(baseline, current)

        self.assertEqual(len(result["removed_sha256"]), 1)
        self.assertEqual(result["views"]["ALL_UNIQUE"]["delta"]["member_count"], -1)

    def test_binary_is_hash_only_and_privacy_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            binary = root / "secret-preview.pdf"
            binary.write_bytes(b"%PDF-1.7\x00SUPER_SECRET_SOURCE_TEXT")
            record = delta.record_for_path(binary)

        self.assertEqual(record["parser_mode"], "BINARY_HASH_ONLY")
        self.assertEqual(record["source_class"]["class"], "GENERATED_ARTIFACT")
        self.assertEqual(record["graph_summary"]["node_count"], 0)
        self.assertNotIn("SUPER_SECRET_SOURCE_TEXT", str(record))

    def test_unique_views_partition_all_unique(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            chat = root / "chat.txt"
            doc = root / "README.md"
            code = root / "tool.py"
            chat.write_text("RouteLLM\n", encoding="utf-8")
            doc.write_text("# Doc\n", encoding="utf-8")
            code.write_text("#!/usr/bin/env python3\nprint('x')\n", encoding="utf-8")
            snapshot = delta.build_snapshot([chat, doc, code], "RUN")

        total = sum(
            delta.aggregate(delta.view_records(snapshot, view))["member_count"]
            for view in ("CHAT_ONLY", "ARTEFACT_ONLY", "CODE_ONLY")
        )
        all_unique = delta.aggregate(
            delta.view_records(snapshot, "ALL_UNIQUE")
        )["member_count"]
        self.assertEqual(total, all_unique)


if __name__ == "__main__":
    unittest.main()
