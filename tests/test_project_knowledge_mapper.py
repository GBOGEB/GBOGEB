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
    def test_lexical_and_structural_counts_are_separate(self):
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
        self.assertEqual(metrics["lexical_frequency"]["STEP_in"], 1)
        self.assertEqual(metrics["lexical_frequency"]["STEP_out"], 1)
        self.assertEqual(metrics["structural_signals"]["python_def"], 1)
        self.assertEqual(metrics["structural_signals"]["python_if"], 1)
        self.assertEqual(metrics["structural_signals"]["python_for"], 1)
        self.assertEqual(metrics["structural_signals"]["python_while"], 1)

    def test_corpus_marks_counts_as_materialized_only(self):
        data = MAPPER.build_corpus([ROOT / "README.md"])
        self.assertEqual(data["source_class"], "EXACT_MATERIALIZED_CORPUS")
        self.assertEqual(data["privacy_contract"], "NO_RAW_SOURCE_TEXT_EMITTED")
        self.assertIn("must not be represented as the full historical", data["caveat"])
        self.assertEqual(data["physical_file_count"], 1)
        self.assertEqual(data["unique_content_count"], 1)

    def test_duplicate_content_is_not_double_counted_in_unique_aggregate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            a = root / "a.txt"
            b = root / "b.txt"
            c = root / "c.txt"
            a.write_text("BLOCK KEB HUMAN\n", encoding="utf-8")
            b.write_text("BLOCK KEB HUMAN\n", encoding="utf-8")
            c.write_text("VISUAL\n", encoding="utf-8")
            data = MAPPER.build_corpus([a, b, c])

        self.assertEqual(data["physical_file_count"], 3)
        self.assertEqual(data["unique_content_count"], 2)
        self.assertEqual(data["duplicate_file_count"], 1)
        self.assertEqual(data["aggregate_raw"]["lexical_frequency"]["BLOCK"], 2)
        self.assertEqual(data["aggregate_unique"]["lexical_frequency"]["BLOCK"], 1)
        self.assertEqual(len(data["duplicate_groups"]), 1)

    def test_markdown_contains_controlled_sections(self):
        data = MAPPER.build_corpus([ROOT / "README.md"])
        rendered = MAPPER.render_markdown(data)
        self.assertIn("Lexical frequency", rendered)
        self.assertIn("Structural signals", rendered)
        self.assertIn("Coverage", rendered)
        self.assertIn("Duplicate groups", rendered)


if __name__ == "__main__":
    unittest.main()
