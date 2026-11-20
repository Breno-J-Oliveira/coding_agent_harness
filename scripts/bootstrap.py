"""Prepare a project for Coding Agent Harness with Codex or Claude Code."""

import argparse
import os
from pathlib import Path
import shutil
import stat
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    ROOT / "workflow-skills" / "idea-to-release",
    ROOT / "workflow-skills" / "engineering-delivery",
    ROOT / "workflow-skills" / "skill-intake-review",
    ROOT / ".agents" / "skills" / "context-budget",
)
ENGINES = {
    "codex": (".agents", "AGENTS.md", "$idea-to-release"),
    "claude": (".claude", "CLAUDE.md", "/idea-to-release"),
}


def entry(invoke):
    return (
        "# Coding Agent Harness\n\n"
        f"Use `{invoke}` para transformar uma ideia em uma entrega verificável. "
        "Para um ajuste pequeno, implemente e valide diretamente.\n\n"
        "Leia somente as instruções, manifests e testes relevantes. "
        "Preserve alterações existentes. Prossiga com decisões reversíveis dentro do escopo. "
        "Use dados fictícios e verificações locais por padrão. "
        "Confirme a autorização antes de publicar, alterar dados reais ou gerar custos.\n"
    )


def inspect(path):
    """Identify existing paths without following symbolic links or junctions."""
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(info.st_mode) or (
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise ValueError(f"Link ou ponto de redirecionamento encontrado: {path}")
    if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
        raise ValueError(f"Tipo de arquivo não suportado: {path}")
    return info


def project_root(target):
    if inspect(target) is None or not target.is_dir():
        raise ValueError("Informe um diretório de projeto existente.")
    root = target.resolve()
    home = Path.home().resolve()
    global_paths = [home / name for name in (".agents", ".claude", ".codex")]
    global_paths.extend(
        Path(os.environ[name]).expanduser()
        for name in ("CODEX_HOME", "CLAUDE_CONFIG_DIR")
        if os.environ.get(name)
    )
    if root in (home, root.parent) or any(
        root.is_relative_to(path.resolve()) for path in global_paths
    ):
        raise ValueError("Use a pasta do projeto e mantenha a configuração pessoal fora da instalação.")
    return root


def plan(root, selected):
    operations = []
    for skill in SKILLS:
        if (inspect(skill) is None or not skill.is_dir()
                or inspect(skill / "SKILL.md") is None or not (skill / "SKILL.md").is_file()):
            raise ValueError(f"Fonte da skill indisponível: {skill}")
        for folder, directories, files in os.walk(skill):
            for name in directories + files:
                inspect(Path(folder) / name)
    for engine in selected:
        config, instructions, invoke = ENGINES[engine]
        instruction_path = root / instructions
        for directory in (root / config, root / config / "skills"):
            if inspect(directory) is not None and not directory.is_dir():
                raise ValueError(f"Esperava uma pasta: {directory}")
        for skill in SKILLS:
            destination = root / config / "skills" / skill.name
            operations.append((destination, skill, inspect(destination) is not None))
        operations.append((instruction_path, entry(invoke), inspect(instruction_path) is not None))
    return operations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True, help="Diretório do projeto")
    parser.add_argument("--engine", choices=(*ENGINES, "both"), default="both")
    parser.add_argument("--apply", action="store_true", help="Gravar a instalação no projeto")
    args = parser.parse_args()
    root = project_root(args.target)
    selected = tuple(ENGINES) if args.engine == "both" else (args.engine,)
    for destination, source, exists in plan(root, selected):
        if exists:
            label = "preservado"
        elif args.apply:
            if isinstance(source, Path):
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, destination)
            else:
                with destination.open("x", encoding="utf-8", newline="\n") as stream:
                    stream.write(source)
            label = "instalado"
        else:
            label = "a instalar"
        print(f"{label} {destination.relative_to(root).as_posix()}")
    if not args.apply:
        print("Prévia concluída. Passe --apply para gravar as mudanças.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        sys.exit(str(exc))
