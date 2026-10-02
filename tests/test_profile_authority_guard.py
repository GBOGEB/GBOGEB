import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
GOV = ROOT / "governance"
ARCHIVE = ROOT / "artifacts" / "governance-snapshots"


class ProfileAuthorityGuard(unittest.TestCase):
    def test_readme_is_non_authoritative(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        normalized = text.replace("**", "")
        self.assertIn(
            "not the engineering, TRIAGE, Mission Control, release, or portfolio-readiness SSOT",
            normalized,
        )
        self.assertIn("TOP14_EXTENSION", text)
        self.assertIn("NOT_YET_MEASURED", text)
        self.assertNotIn("Phase 3: AI Enhancement & Real-time Analytics | 🔄 35%", text)

    def test_authority_map_fails_closed(self):
        text = (GOV / "PORTFOLIO_AUTHORITY_MAP_CURRENT_v1.yaml").read_text(encoding="utf-8")
        for required in [
            "authority_transfer: false",
            "formal_credit_delta: 0",
            "GBOGEB/cryoplant-project",
            "GBOGEB/CODEX",
            "GBOGEB/ABACUS",
            "GBOGEB/pipeline-automation-hub",
            "cohort: TOP14_EXTENSION",
            "telemetry_state: NOT_YET_MEASURED",
            "state: COMPLETE",
            "destructive_rename_or_delete_safe: false",
        ]:
            self.assertIn(required, text)

    def test_bridge_paths_are_pointer_only_and_archives_exist(self):
        expected = {
            "GLOBAL_EXCEL_SCHEDULE_ENGINE_TOPOLOGY_v1.yaml":
                "GLOBAL_EXCEL_SCHEDULE_ENGINE_TOPOLOGY_v1_PRE_POINTER_20261002.yaml",
            "GLOBAL_MATH_PLOTS_SKILL_TOPOLOGY_v1.yaml":
                "GLOBAL_MATH_PLOTS_SKILL_TOPOLOGY_v1_PRE_POINTER_20261002.yaml",
            "GLOBAL_MATH_PLOTS_MIP_HARDENING_v1.yaml":
                "GLOBAL_MATH_PLOTS_MIP_HARDENING_v1_PRE_POINTER_20261002.yaml",
            "GLOBAL_MATH_PLOTS_WAVES_N_PLUS_2_v1.yaml":
                "GLOBAL_MATH_PLOTS_WAVES_N_PLUS_2_v1_PRE_POINTER_20261002.yaml",
        }
        for pointer_name, archive_name in expected.items():
            pointer = (GOV / pointer_name).read_text(encoding="utf-8")
            self.assertIn("state: POINTER_ONLY", pointer)
            self.assertIn("this_file_is_not_status_authority: true", pointer)
            self.assertIn(archive_name, pointer)
            self.assertTrue((ARCHIVE / archive_name).is_file())

    def test_reference_census_closes_pointerization_precondition(self):
        text = (GOV / "BRIDGE_REFERENCE_CENSUS_20261002_v1.yaml").read_text(encoding="utf-8")
        self.assertIn("P0_REFERENCE_CENSUS: COMPLETE", text)
        self.assertIn("P1_POINTERIZATION: COMPLETE", text)
        self.assertIn("P2_ARCHIVE: COMPLETE", text)
        self.assertIn("P3_PROFILE_GUARD: GREEN", text)
        self.assertIn("smoke_run: 36996386515", text)
        self.assertIn("ORIGINAL_PUBLIC_GOVERNANCE_PATHS_REMAIN_PRESENT", text)


if __name__ == "__main__":
    unittest.main()
