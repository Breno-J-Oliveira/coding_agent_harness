import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import engineering
from skillpacks import scan_target

spec = importlib.util.spec_from_file_location("skill_guard", SCRIPTS / "skill-guard.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class EngineeringFlow(unittest.TestCase):
    def test_monorepo_routes_frontend_backend_and_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for app, dependencies in [
                ("web", {"react": "^19"}),
                ("api", {"@nestjs/core": "^11", "pg": "^8"}),
            ]:
                manifest = root / "apps" / app / "package.json"
                manifest.parent.mkdir(parents=True)
                manifest.write_text(json.dumps({"dependencies": dependencies}))
            packs, evidence = scan_target(root)
            self.assertTrue({"frontend", "backend-node", "database"} <= set(packs))
            self.assertTrue(any(item.startswith("apps/api:") for item in evidence))

    def test_review_failure_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "app"
            project.mkdir()
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            board = root / "queue.json"

            def call(*args):
                with patch("sys.argv", ["engineering.py", "--board", str(board), *map(str, args)]):
                    return engineering.main()

            self.assertEqual(call("init", "--project", project, "--goal", "Entrega"), 0)
            self.assertEqual(call("add", "api", "--phase", "backend", "--title", "API",
                                  "--acceptance", "Teste de contrato passa"), 0)
            self.assertEqual(call("add", "web", "--phase", "frontend", "--title", "Web",
                                  "--acceptance", "Formulário funciona", "--after", "api"), 0)
            real_run = subprocess.run

            def runner(argv, **opts):
                if argv[0] == "fixture-codex":
                    payload = opts["input"].decode()
                    self.assertIn("Teste de contrato passa", payload)
                    self.assertNotIn("Formulário funciona", payload)
                    self.assertIn("workspace-write", argv)
                    if runner.exit_code == 0:
                        events = [
                            {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps({
                                "status": runner.status, "summary": "Resultado do teste de contrato."
                            })}},
                            {"type": "turn.completed"},
                        ]
                        for event in events:
                            opts["stdout"].write((json.dumps(event) + "\n").encode("utf-8"))
                    return subprocess.CompletedProcess(argv, runner.exit_code)
                return real_run(argv, **opts)

            with patch.object(engineering.shutil, "which", return_value="fixture-codex"), patch.object(
                engineering.subprocess, "run", side_effect=runner
            ):
                runner.exit_code = 1
                self.assertEqual(call("run"), 1)
                self.assertIsNone(engineering.ready(engineering.load(board)))
                call("retry", "api")
                runner.exit_code = 0
                runner.status = "blocked"
                self.assertEqual(call("run"), 1)
                self.assertEqual(engineering.load(board)["tasks"][0]["runner_outcome"], "blocked")
                self.assertIsNone(engineering.ready(engineering.load(board)))
                call("retry", "api")
                runner.status = "ready"
                self.assertEqual(call("run"), 0)
                self.assertIsNone(engineering.ready(engineering.load(board)))
                with self.assertRaises(ValueError):
                    call("accept", "api", "--evidence", root / "missing.txt")
                evidence = root / "verification.txt"
                evidence.write_text("Contract test passed in the test fixture.")
                call("accept", "api", "--evidence", evidence)
                state = engineering.load(board)
                self.assertEqual(state["tasks"][0]["status"], "done")
                self.assertEqual(len(state["tasks"][0]["evidence_sha256"]), 64)
                self.assertEqual(engineering.ready(state)["id"], "web")
                call("record", "web", "--evidence", evidence)
                state = engineering.load(board)
                self.assertEqual(state["tasks"][1]["status"], "review")
                self.assertEqual(state["tasks"][1]["recorded_sha256"], state["tasks"][0]["evidence_sha256"])
                call("accept", "web", "--evidence", evidence)
                self.assertEqual(engineering.load(board)["tasks"][1]["status"], "done")

    def test_scanner_error_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "candidate"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: candidate\ndescription: Demo\n---\n")
            for output, code, expected in [
                ('{"findings":[]}', 0, "review"), ("tool error", 0, "hold"),
                ('{"findings":[]}', 1, "hold"),
            ]:
                report = root / f"{len(list(root.glob('*.json')))}.json"
                with patch("sys.argv", ["skill-guard.py", str(skill), "--report", str(report)]), patch.object(
                    guard.shutil, "which", return_value="fixture-scanner"
                ), patch.object(guard.subprocess, "run", return_value=subprocess.CompletedProcess([], code, output)):
                    self.assertEqual(guard.main(), int(expected == "hold"))
                self.assertEqual(json.loads(report.read_text())["status"], expected)
