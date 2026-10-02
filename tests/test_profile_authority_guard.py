import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ProfileAuthorityGuard(unittest.TestCase):
    def test_readme_declares_non_ssot_profile_role(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("not the engineering, TRIAGE, Mission Control, release, or portfolio-readiness SSOT", text)
        self.assertIn("TOP14_EXTENSION", text)
        self.assertIn("NOT_YET_MEASURED", text)
        self.assertNotIn("Phase 3: AI Enhancement & Real-time Analytics | 🔄 35%", text)

    def test_machine_authority_map_fails_closed(self):
        text = (ROOT / "governance" / "PORTFOLIO_AUTHORITY_MAP_CURRENT_v1.yaml").read_text(encoding="utf-8")
        required = [
            "authority_transfer: false",
            "formal_credit_delta: 0",
            "GBOGEB/cryoplant-project",
            "GBOGEB/CODEX",
            "GBOGEB/ABACUS",
            "GBOGEB/pipeline-automation-hub",
            "cohort: TOP14_EXTENSION",
            "telemetry_state: NOT_YET_MEASURED",
            "destructive_move_without_reference_census: false",
        ]
        for item in required:
            self.assertIn(item, text)

    def test_governance_guide_marks_global_files_as_bridges(self):
        text = (ROOT / "governance" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Cross-repository bridge snapshots", text)
        self.assertIn("GLOBAL_EXCEL_SCHEDULE_ENGINE_TOPOLOGY_v1.yaml", text)
        self.assertIn("GLOBAL_MATH_PLOTS_SKILL_TOPOLOGY_v1.yaml", text)
        self.assertIn("Do **not** rename, delete or move", text)


if __name__ == "__main__":
    unittest.main()
