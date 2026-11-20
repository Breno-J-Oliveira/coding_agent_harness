"""Validação LOCAL de TOML do pacote. Não imprime conteúdo de config pessoal."""
from pathlib import Path
import sys
try:
    import tomllib
except ImportError:
    raise SystemExit("Use Python >= 3.11")
root = Path(__file__).resolve().parents[1]
config = root / "templates/config-agents.toml"
with config.open("rb") as f:
    settings = tomllib.load(f)
assert settings.get("agents", {}).get("enabled") is True
assert settings["agents"].get("max_concurrent_threads_per_session") == 3
count = 0
names = set()
for path in sorted((root / "agents").glob("*.toml")):
    with path.open("rb") as f:
        data = tomllib.load(f)
    for field in ("name", "description", "developer_instructions"):
        assert data.get(field), f"{path.name}: faltando {field}"
    assert data["name"] not in names, f"nome duplicado: {data['name']}"
    names.add(data["name"])
    count += 1
assert count == 28, f"Esperados 28 agentes, encontrados {count}"
print(f"OK: template TOML e {count} agentes válidos (estrutura).")
print("Nota: sintaxe válida não comprova descoberta pelo Codex.")
