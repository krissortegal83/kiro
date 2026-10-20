"""Unit tests for demonstration integrations and TPM dashboard."""
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "crm-integration-demo"))
sys.path.insert(0, str(ROOT / "tpm-program-dashboard"))

from crm_sync import synchronize  # noqa: E402
from program_dashboard import analyze_program, markdown_report  # noqa: E402


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.original = [
            {"email": "Ana@example.org", "name": "Ana", "updated_at": "2026-10-01T10:00:00Z"}
        ]

    def test_duplicate_event_is_idempotent(self):
        result = synchronize(self.original, [self.original[0]])
        self.assertEqual(len(result["contacts"]), 1)
        self.assertEqual(result["audit"][0]["action"], "unchanged")

    def test_newer_wins_and_stale_does_not(self):
        newer = {"email": "ana@example.org", "name": "Ana Updated", "updated_at": "2026-10-03T10:00:00Z"}
        stale = {"email": "ana@example.org", "name": "Old", "updated_at": "2026-09-01T10:00:00Z"}
        result = synchronize(self.original, [newer, stale])
        self.assertEqual(result["contacts"][0]["name"], "Ana Updated")
        self.assertEqual([x["action"] for x in result["audit"]], ["updated", "stale_ignored"])

    def test_equal_timestamp_conflict_flagged(self):
        change = {"email": "ana@example.org", "name": "Other", "updated_at": "2026-10-01T10:00:00Z"}
        result = synchronize(self.original, [change])
        self.assertEqual(result["audit"][0]["action"], "timestamp_conflict")

    def test_rejects_missing_timezone(self):
        with self.assertRaises(ValueError):
            synchronize([], [{"email":"x@example.org","name":"X","updated_at":"2026-10-01T11:00:00"}])


class ProgramTests(unittest.TestCase):
    def setUp(self):
        self.sample = {"name": "Demo", "tasks": [
            {"id": "a", "title": "Backend API", "team": "Backend", "status": "in_progress", "due_date": "2026-10-01", "depends_on": [], "risk_score": 4},
            {"id": "b", "title": "Frontend", "team": "Frontend", "status": "planned", "due_date": "2026-10-28", "depends_on": ["a"], "risk_score": 2},
        ]}

    def test_detects_overdue_risk_and_blocker(self):
        analysis = analyze_program(self.sample, date(2026, 10, 20))
        self.assertEqual(analysis["health"], "at_risk")
        self.assertIn("overdue", analysis["findings"][0]["flags"])
        self.assertIn("high_risk", analysis["findings"][0]["flags"])
        self.assertIn("blocked_by_dependency", analysis["findings"][1]["flags"])
        self.assertIn("Suggested TPM actions", markdown_report(analysis))

    def test_rejects_cycles(self):
        self.sample["tasks"][0]["depends_on"] = ["b"]
        with self.assertRaises(ValueError):
            analyze_program(self.sample, date(2026, 10, 20))

    def test_successful_program(self):
        self.sample["tasks"][0]["status"] = "completed"
        self.sample["tasks"][1]["status"] = "completed"
        analysis = analyze_program(self.sample, date(2026, 10, 20))
        self.assertEqual(analysis["health"], "on_track")
        self.assertEqual(analysis["completed"], 2)


if __name__ == "__main__":
    unittest.main()
