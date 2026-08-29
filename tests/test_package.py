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
        self.assertEqual(manifest["version"], "0.1.0")
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
            self.assertIn("30-second summary", page)
            self.assertIn("Check answer", page)
            self.assertIn("Enable 3D view", page)
            self.assertIn("prefers-reduced-motion", page)
            self.assertNotIn("\u2014", page)
            self.assertNotIn("linear-gradient", page)

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
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            profile = root / "docs" / "learning" / "profile.md"
            self.assertIn("Understand request validation", profile.read_text(encoding="utf-8"))
            profile.write_text("User-owned profile\n", encoding="utf-8")
            second = self.run_script("init_learning.py", "--root", str(root), "--objective", "Overwrite me")
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(profile.read_text(encoding="utf-8"), "User-owned profile\n")


if __name__ == "__main__":
    unittest.main()
