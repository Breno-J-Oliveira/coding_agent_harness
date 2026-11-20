"""Bounded queue metrics and optional checks owned by the operator."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


def measure(events):
    totals = dict.fromkeys(("input_tokens", "cached_input_tokens", "output_tokens"), 0)
    measured = False
    with events.open(encoding="utf-8") as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if not isinstance(event, dict) or event.get("type") != "turn.completed":
                continue
            usage = event.get("usage")
            if not isinstance(usage, dict) or not {"input_tokens", "output_tokens"} <= usage.keys():
                continue
            values = {key: usage.get(key, 0) for key in totals}
            if any(type(value) is not int or value < 0 for value in values.values()):
                continue
            measured = True
            for key, value in values.items():
                totals[key] += value
    return totals if measured else None


def snapshot_check(project, script):
    script = script.resolve()
    if script.is_relative_to(project) or script.suffix.lower() != ".py" or not script.is_file():
        raise ValueError("Informe um verificador Python de sua confiança, fora do projeto.")
    return script, hashlib.sha256(script.read_bytes()).hexdigest()


def verify(task, project, script, digest, timeout):
    if hashlib.sha256(script.read_bytes()).hexdigest() != digest:
        raise ValueError("O verificador mudou durante a execução. A tarefa segue em revisão.")
    log = Path(task["evidence"]) / "verification.log"
    contract = {key: task[key] for key in ("id", "phase", "title", "acceptance")}
    with log.open("xb") as output:
        result = subprocess.run(
            [sys.executable, "-I", str(script)], cwd=script.parent,
            input=json.dumps({"project": str(project), "task": contract}).encode("utf-8"),
            stdout=output, stderr=subprocess.STDOUT, timeout=timeout,
        )
    if result.returncode != 0 or hashlib.sha256(script.read_bytes()).hexdigest() != digest:
        return False
    receipt = log.with_name("verified.json")
    receipt.write_text(json.dumps({"verifier_sha256": digest, "exit_code": 0,
                                   "task": contract, "project": str(project)}, ensure_ascii=False),
                       encoding="utf-8")
    task.update(status="done", accepted_evidence=str(receipt),
                evidence_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest(),
                accepted_by="operator-verifier")
    return True
