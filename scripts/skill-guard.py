"""Run Cisco Skill Scanner locally and keep a review report."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys


def inventory(directory):
    hashes = {}
    for path in sorted(directory.rglob("*")):
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        if path.is_symlink() or attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Link dentro do pacote: {path.relative_to(directory)}")
        if path.is_file():
            if len(hashes) >= 2000 or path.stat().st_size > 20_000_000:
                raise ValueError("Pacote acima do limite desta inspeção local.")
            hashes[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("skill", type=Path, help="Pasta de uma skill extraída em área de revisão.")
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    if a.skill.is_symlink() or (hasattr(a.skill, "is_junction") and a.skill.is_junction()):
        p.error("Inspecione uma cópia regular da skill.")
    skill, report = a.skill.resolve(), a.report.resolve()
    if not (skill / "SKILL.md").is_file() or report.is_relative_to(skill):
        p.error("Informe uma pasta com SKILL.md e um relatório fora do pacote.")
    engine = shutil.which("skill-scanner")
    if not engine:
        p.error("Instale o scanner com uv tool install cisco-ai-skill-scanner==2.3.2.")
    before = inventory(skill)
    env = dict(os.environ, LITELLM_LOCAL_MODEL_COST_MAP="True", HF_HUB_OFFLINE="1")
    with report.open("x", encoding="utf-8") as output:
        try:
            result = subprocess.run([engine, "scan", str(skill), "--format", "json",
                                     "--fail-on-severity", "high"],
                                    capture_output=True, text=True, encoding="utf-8",
                                    errors="replace", timeout=120, env=env)
        except (OSError, subprocess.SubprocessError):
            json.dump({"skill": skill.name, "status": "hold", "files_sha256": before,
                       "error": "O scanner não iniciou ou não terminou no prazo."}, output, indent=2)
            print(f"hold: {report}")
            return 1
        try:
            findings = json.loads(result.stdout)
            if not isinstance(findings, dict) or not isinstance(findings.get("findings"), list):
                raise ValueError("Resposta incompleta.")
        except ValueError:
            findings = None
        unchanged = before == inventory(skill)
        status = "review" if result.returncode == 0 and unchanged and findings is not None else "hold"
        json.dump({"date": datetime.now(timezone.utc).isoformat(), "skill": skill.name, "status": status,
                   "scanner_exit": result.returncode, "files_sha256": before, "cisco_report": findings,
                   "error": None if findings is not None else "Scanner não gerou um relatório válido."},
                  output, ensure_ascii=False, indent=2)
    print(f"{status}: {report}")
    return 0 if status == "review" else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        sys.exit(str(exc))
