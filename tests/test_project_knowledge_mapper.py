import importlib.util
import pathlib
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
        self.assertIn("must not be represented as the full historical", data["caveat"])
        self.assertEqual(len(data["files"]), 1)

    def test_markdown_contains_controlled_sections(self):
        data = MAPPER.build_corpus([ROOT / "README.md"])
        rendered = MAPPER.render_markdown(data)
        self.assertIn("Lexical frequency", rendered)
        self.assertIn("Structural signals", rendered)
        self.assertIn("Coverage", rendered)


if __name__ == "__main__":
    unittest.main()
