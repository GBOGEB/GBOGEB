import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "project_knowledge_mapper.py"
SPEC = importlib.util.spec_from_file_location("project_knowledge_mapper", MODULE)
MAPPER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MAPPER)


class ProjectKnowledgeMapperTests(unittest.TestCase):
    def test_source_class_purity(self):
        cases = [
            ("chat.txt", "RouteLLM\nhello\nRelevant Posts\n", "CONVERSATION_TRANSCRIPT"),
            (
                "bundle.md",
                "----FILE: a.yaml\n----FILE: b.py\nhandover_manifest\ndefinition_of_victory\n",
                "HANDOVER_BUNDLE",
            ),
            (
                "index.txt",
                'MAIN CODE artefact\n"C:\\x\\Master_Input\\a.docx"\n' * 6,
                "SOURCE_INDEX",
            ),
            ("tool.py", "#!/usr/bin/env python3\nprint('x')\n", "CODE_PYTHON"),
            ("run.sh", "#!/usr/bin/env bash\necho x\n", "CODE_SHELL"),
            (
                "ci.yml",
                "name: CI\non: push\njobs:\n  test: {}\n",
                "WORKFLOW_CONFIG",
            ),
            ("README.md", "# Documentation\n", "DOCUMENTATION"),
        ]
        for name, text, expected in cases:
            got = MAPPER.classify_source(pathlib.Path(name), text)
            self.assertEqual(got["class"], expected)

    def test_graph_is_privacy_safe_and_sequential(self):
        text = """# Section A
RouteLLM
BLOCK_001 [KEB]
STEP_in
def alpha():
    if ready:
        pass
STEP_out
"""
        graph = MAPPER.extract_block_graph(text, "a" * 64)
        self.assertGreaterEqual(graph["node_count"], 6)
        self.assertEqual(graph["edge_count"], graph["node_count"] - 1)
        serialized = str(graph)
        self.assertNotIn("Section A", serialized)
        self.assertNotIn("alpha", serialized)
        self.assertTrue(all("label_sha256" in node for node in graph["nodes"]))

    def test_duplicate_content_not_double_counted_by_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            a = root / "README_a.md"
            b = root / "README_b.md"
            c = root / "chat.txt"
            a.write_text("# A\nBLOCK\n", encoding="utf-8")
            b.write_text("# A\nBLOCK\n", encoding="utf-8")
            c.write_text("RouteLLM\nBLOCK\n", encoding="utf-8")
            data = MAPPER.build_corpus([a, b, c])

        self.assertEqual(data["physical_file_count"], 3)
        self.assertEqual(data["unique_content_count"], 2)
        self.assertEqual(data["duplicate_file_count"], 1)
        self.assertEqual(
            data["aggregate_unique_by_source_class"]["DOCUMENTATION"][
                "lexical_frequency"
            ]["BLOCK"],
            1,
        )
        self.assertEqual(
            data["aggregate_unique_by_source_class"]["CONVERSATION_TRANSCRIPT"][
                "lexical_frequency"
            ]["BLOCK"],
            1,
        )
        self.assertEqual(data["classification_conflicts"], [])

    def test_classification_conflict_is_fail_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            a = root / "README.md"
            b = root / "copy.txt"
            a.write_text("# Same\n", encoding="utf-8")
            b.write_text("# Same\n", encoding="utf-8")
            data = MAPPER.build_corpus([a, b])

        self.assertEqual(data["unique_content_count"], 1)
        self.assertEqual(len(data["classification_conflicts"]), 1)

    def test_existing_block_and_code_counts(self):
        text = """BLOCK BLOCK_001
def alpha():
    if ready:
        for item in items:
            while item:
                break
STEP_in -> [KEB] -> STEP_out
HUMAN VISUAL digital twin DMAIC RTM MCP
"""
        metrics = MAPPER.map_text(text)
        self.assertEqual(metrics["lexical_frequency"]["BLOCK"], 2)
        self.assertEqual(metrics["structural_signals"]["python_def"], 1)
        self.assertEqual(metrics["structural_signals"]["python_if"], 1)
        self.assertEqual(metrics["structural_signals"]["python_for"], 1)
        self.assertEqual(metrics["structural_signals"]["python_while"], 1)


if __name__ == "__main__":
    unittest.main()
