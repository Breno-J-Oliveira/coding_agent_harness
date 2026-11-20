import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bootstrap.py"
EXPECTED_SKILLS = {
    "context-budget", "engineering-delivery", "idea-to-release", "skill-intake-review",
}


class BootstrapTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "meu projeto"
        self.project.mkdir()

    def invoke(self, *args, env=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--target", str(self.project), *args],
            encoding="utf-8", errors="replace", capture_output=True, env=env, timeout=30,
        )

    def test_preview_and_dual_install(self):
        result = self.invoke("--engine", "both")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("a instalar .agents/skills/idea-to-release", result.stdout)
        self.assertFalse(list(self.project.iterdir()))
        result = self.invoke("--engine", "both", "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        for prefix, instruction, invocation in (
            (".agents", "AGENTS.md", "$idea-to-release"),
            (".claude", "CLAUDE.md", "/idea-to-release"),
        ):
            location = self.project / prefix / "skills"
            self.assertEqual({child.name for child in location.iterdir()}, EXPECTED_SKILLS)
            entry = (self.project / instruction).read_text(encoding="utf-8")
            self.assertIn(invocation, entry)
            for name in EXPECTED_SKILLS:
                self.assertTrue((location / name / "SKILL.md").is_file())
                self.assertFalse((location / name / "KIT-LOCATION.txt").exists())

    def test_only_selected_engine_and_local_files_are_preserved(self):
        entry = self.project / "CLAUDE.md"
        entry.write_bytes(b"regras anteriores\r\n")
        existing = self.project / ".claude" / "skills" / "idea-to-release" / "SKILL.md"
        existing.parent.mkdir(parents=True)
        existing.write_bytes(b"skill anterior\n")
        for _ in range(2):
            result = self.invoke("--engine", "claude", "--apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("preservado CLAUDE.md", result.stdout)
            self.assertEqual(entry.read_bytes(), b"regras anteriores\r\n")
            self.assertEqual(existing.read_bytes(), b"skill anterior\n")
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / ".agents").exists())

    def test_rejects_global_location(self):
        result = self.invoke("--apply", env={**os.environ, "CODEX_HOME": str(self.project)})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("configura", result.stderr)
        self.assertFalse(list(self.project.iterdir()))

    def test_refuses_symlink_without_partial_install(self):
        outside = Path(self.temp.name) / "fora"
        outside.mkdir()
        try:
            (self.project / ".claude").symlink_to(outside, target_is_directory=True)
        except (NotImplementedError, OSError):
            self.skipTest("Criação de link indisponível neste ambiente.")
        result = self.invoke("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("redirecionamento", result.stderr)
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse(list(outside.iterdir()))
