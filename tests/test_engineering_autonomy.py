import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import engineering


class AutonomyTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.project = self.root / "app"
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        self.board = self.root / "queue.json"

    def call(self, *args):
        output = io.StringIO()
        with patch("sys.argv", ["engineering.py", "--board", str(self.board), *map(str, args)]):
            with contextlib.redirect_stdout(output):
                code = engineering.main()
        return code, output.getvalue()

    def test_start_creates_full_stack_contract_and_brief(self):
        self.call("start", "--project", self.project, "--idea", "Customer portal")
        _, brief = self.call("brief")
        self.assertIn("Customer portal", brief)
        self.assertIn("persistência", brief)
        self.assertIn("passos de deploy", brief)
        self.assertNotIn("No JSON final", brief)
        with self.assertRaisesRegex(ValueError, "Já existe"):
            self.call("start", "--project", self.project, "--idea", "Other idea")

    def test_advance_verifies_and_respects_budget_and_manual_gate(self):
        self.call("init", "--project", self.project, "--goal", "Local delivery")
        for task, after in (("storage", []), ("api", ["--after", "storage"])):
            self.call("add", task, "--phase", "backend", "--title", task,
                      "--acceptance", "Marker contains verified", "--auto-verify", *after)
        with self.assertRaisesRegex(ValueError, "aceite humano"):
            self.call("add", "release", "--phase", "entrega", "--title", "Release",
                      "--acceptance", "Checklist", "--auto-verify")
        self.call("add", "release", "--phase", "entrega", "--title", "Release",
                  "--acceptance", "Checklist", "--after", "api")
        verifier = self.root / "verify.py"
        verifier.write_text(
            'import json, sys\nfrom pathlib import Path\nrequest = json.load(sys.stdin)\n'
            'actual = Path(request["project"]) / request["task"]["id"]\n'
            'sys.exit(0 if actual.read_text() == "verified" else 1)\n', encoding="utf-8",
        )
        actual_run = subprocess.run

        def stub(argv, **options):
            if argv[0] != "fixture-codex":
                return actual_run(argv, **options)
            request = json.loads(options["input"].decode().split("\n\n", 1)[1])
            task = request["task"]
            self.assertNotIn("evidence", task)
            (options["cwd"] / task["id"]).write_text(stub.content)
            events = [
                {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps({
                    "status": "ready", "summary": "Done"})}},
                {"type": "turn.completed", "usage": {"input_tokens": 500, "output_tokens": 30}},
            ]
            for event in events:
                options["stdout"].write((json.dumps(event) + "\n").encode())
            return subprocess.CompletedProcess(argv, 0)

        def statuses():
            return [task["status"] for task in engineering.load(self.board)["tasks"]]

        with patch.object(engineering.shutil, "which", return_value="fixture-codex"), patch.object(
            engineering.subprocess, "run", side_effect=stub
        ):
            stub.content = "wrong"
            self.assertEqual(self.call("advance", "--verifier", verifier)[0], 1)
            self.assertEqual(statuses(), ["review", "pending", "pending"])
            self.call("retry", "storage")
            stub.content = "verified"
            self.assertEqual(self.call("advance", "--verifier", verifier, "--max-tokens", 520, "--allow-dirty")[0], 0)
            self.assertEqual(statuses(), ["done", "pending", "pending"])
            self.assertEqual(self.call("advance", "--verifier", verifier, "--allow-dirty")[0], 0)
        self.assertEqual(statuses(), ["done", "done", "review"])
        _, usage = self.call("usage")
        self.assertEqual(json.loads(usage)["total_tokens"], 2120)
        self.assertEqual(json.loads(usage)["attempts_measured"], 4)
