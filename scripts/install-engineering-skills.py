"""Install the VibeCoder 4.0 workflows and reviewed third-party skills additively."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--target", type=Path, help="Instale no projeto indicado. O padrão é o escopo do usuário.")
    args = p.parse_args()
    destination = (args.target.resolve() if args.target else Path.home()) / ".agents/skills"
    candidates = sorted((ROOT / "workflow-skills").iterdir())
    vendor = ROOT / "third-party/skills"
    if vendor.exists():
        records = json.loads((vendor.parent / "skills-lock.json").read_text(encoding="utf-8"))
        for name, files in records["skills"].items():
            if name not in ("code-simplification", "observability-and-instrumentation"):
                raise ValueError("Skill externa fora do lockfile desta edição.")
            folder = vendor / name
            actual = {}
            for path in folder.rglob("*"):
                if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
                    raise ValueError(f"Link inesperado em {name}.")
                if path.is_file():
                    actual[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != files:
                raise ValueError(f"Conteúdo externo divergente em {name}.")
            candidates.append(folder)
    for source in candidates:
        if not (source / "SKILL.md").is_file():
            continue
        target = destination / source.name
        legacy = Path.home() / ".codex/skills" / source.name
        if target.exists() or target.is_symlink() or (not args.target and legacy.exists()):
            print("preservada", source.name)
            continue
        if args.apply:
            shutil.copytree(source, target)
            if source.parent == ROOT / "workflow-skills":
                (target / "KIT-LOCATION.txt").write_text(str(ROOT) + "\n", encoding="utf-8")
        print("instalada" if args.apply else "disponível", source.name, str(target))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        sys.exit(str(exc))
