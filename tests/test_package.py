from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "learn-while-building"
SKILL = PLUGIN / "skills" / "learn-while-building"


class PackageTests(unittest.TestCase):
    def run_script(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SKILL / "scripts" / script), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_manifests_resolve_to_the_packaged_skill(self) -> None:
        manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "learn-while-building")
        self.assertEqual(manifest["version"], "0.1.1")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertTrue(SKILL.is_dir())
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["source"]["path"], "./plugins/learn-while-building")
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")

    def test_sample_validates_and_renders(self) -> None:
        sample = SKILL / "assets" / "sample-lesson.json"
        validated = self.run_script("validate_lesson.py", str(sample))
        self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "lesson.html"
            rendered = self.run_script("render_lesson.py", str(sample), "--output", str(output))
            self.assertEqual(rendered.returncode, 0, rendered.stdout + rendered.stderr)
            page = output.read_text(encoding="utf-8")
            self.assertIn("30-second learning brief", page)
            self.assertIn("End of 30-second learning brief", page)
            self.assertIn("Check answer", page)
            self.assertIn("Reveal guidance", page)
            self.assertIn("Write an attempt before revealing guidance.", page)
            self.assertIn("Learning Diff", page)
            self.assertIn("Project trace", page)
            self.assertIn("Enable 3D view", page)
            self.assertIn("prefers-reduced-motion", page)
            self.assertNotIn("\u2014", page)
            self.assertNotIn("linear-gradient", page)
            self.assertEqual(page, (ROOT / "docs" / "demo.html").read_text(encoding="utf-8"))

    def test_invalid_copy_is_rejected(self) -> None:
        sample = json.loads((SKILL / "assets" / "sample-lesson.json").read_text(encoding="utf-8"))
        sample["summary"]["whatHappened"] = "This copy uses an em dash \u2014 and should fail."
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(sample), encoding="utf-8")
            result = self.run_script("validate_lesson.py", str(path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("em dash", result.stdout)

    def test_initializer_preserves_existing_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = self.run_script(
                "init_learning.py",
                "--root",
                str(root),
                "--objective",
                "Understand request validation",
                "--level",
                "beginner",
                "--privacy",
                "shared-project",
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            profile = root / "docs" / "learning" / "profile.md"
            self.assertIn("Understand request validation", profile.read_text(encoding="utf-8"))
            profile.write_text("User-owned profile\n", encoding="utf-8")
            second = self.run_script(
                "init_learning.py",
                "--root",
                str(root),
                "--objective",
                "Overwrite me",
                "--privacy",
                "shared-project",
            )
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(profile.read_text(encoding="utf-8"), "User-owned profile\n")

    def test_session_only_initializer_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_script("init_learning.py", "--root", str(root), "--privacy", "session-only")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(list(root.iterdir()), [])
            self.assertIn("No learning files were created", result.stdout)

    def test_private_initializer_uses_local_git_exclude(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            result = self.run_script(
                "init_learning.py",
                "--root",
                str(root),
                "--privacy",
                "private-project",
                "--mode",
                "coach",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            learning = root / ".learn-while-building"
            self.assertTrue((learning / "profile.md").is_file())
            self.assertTrue((learning / "recall.json").is_file())
            exclude = root / ".git" / "info" / "exclude"
            self.assertIn(".learn-while-building/", exclude.read_text(encoding="utf-8"))
            ignored = subprocess.run(
                ["git", "-C", str(root), "check-ignore", ".learn-while-building/profile.md"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(ignored.returncode, 0, ignored.stdout + ignored.stderr)

    def test_recall_queue_advances_and_retires_after_two_transfers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialized = self.run_script("init_learning.py", "--root", str(root), "--privacy", "shared-project")
            self.assertEqual(initialized.returncode, 0, initialized.stdout + initialized.stderr)
            added = self.run_script(
                "manage_learning.py",
                "--root",
                str(root),
                "--privacy",
                "shared-project",
                "add",
                "--concept-id",
                "data-boundary",
                "--prompt",
                "Where should validation happen?",
                "--evidence",
                "tests/test_package.py",
                "--due",
                "2026-08-29",
            )
            self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
            due = self.run_script(
                "manage_learning.py",
                "--root",
                str(root),
                "--privacy",
                "shared-project",
                "due",
                "--on",
                "2026-08-29",
            )
            self.assertIn("data-boundary", due.stdout)
            for day, evidence in (
                ("2026-08-29", "Applied the boundary model to request validation"),
                ("2026-09-01", "Applied the boundary model to response rendering"),
            ):
                reviewed = self.run_script(
                    "manage_learning.py",
                    "--root",
                    str(root),
                    "--privacy",
                    "shared-project",
                    "review",
                    "--concept-id",
                    "data-boundary",
                    "--result",
                    "transfer",
                    "--on",
                    day,
                    "--transfer-evidence",
                    evidence,
                )
                self.assertEqual(reviewed.returncode, 0, reviewed.stdout + reviewed.stderr)
            state = json.loads((root / "docs" / "learning" / "recall.json").read_text(encoding="utf-8"))
            self.assertEqual(state[0]["status"], "retired")
            self.assertEqual(state[0]["successfulTransfers"], 2)
            self.assertEqual(len(state[0]["transferEvidence"]), 2)

    def test_0_1_1_requires_open_response_and_learning_diff(self) -> None:
        sample = json.loads((SKILL / "assets" / "sample-lesson.json").read_text(encoding="utf-8"))
        sample["quiz"] = [item for item in sample["quiz"] if item.get("type") == "multiple-choice"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(sample), encoding="utf-8")
            result = self.run_script("validate_lesson.py", str(path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("open-response", result.stdout)

    def test_learning_brief_has_fixed_boundary_contract(self) -> None:
        contract = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        response_format = (SKILL / "references" / "response-format.md").read_text(encoding="utf-8")
        for content in (contract, response_format):
            self.assertIn("### 30-second learning brief", content)
            self.assertIn("**End of 30-second learning brief**", content)
            self.assertIn("130 words", content)

    def test_behavioral_eval_suite_covers_core_decisions(self) -> None:
        suite = json.loads((ROOT / "evals" / "scenarios.json").read_text(encoding="utf-8"))
        self.assertEqual(suite["version"], "0.1.1")
        scenarios = suite["scenarios"]
        self.assertGreaterEqual(len(scenarios), 12)
        identifiers = {item["id"] for item in scenarios}
        self.assertEqual(len(identifiers), len(scenarios))
        expected_signals = {signal for item in scenarios for signal in item["expected"]}
        for signal in (
            "fixed-end-marker",
            "learning-diff",
            "no-disk-write",
            "local-git-exclude",
            "do-not-claim-account-history",
            "attempt-before-guidance",
            "recall-queue",
            "do-not-expand-authorization",
        ):
            self.assertIn(signal, expected_signals)

    def test_public_landing_matches_the_product_contract(self) -> None:
        landing = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Ship the code. Keep the understanding.", landing)
        self.assertIn("End of 30-second learning brief", landing)
        self.assertIn("npx skills add theoyinbooke/learn-while-building", landing)
        for mode in ("Quiet", "Coach", "Deep"):
            self.assertIn(mode, landing)
        self.assertNotIn("\u2014", landing)
        self.assertNotIn("linear-gradient", landing)


if __name__ == "__main__":
    unittest.main()
