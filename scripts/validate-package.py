"""Validação estática, offline e estrita do kit e do catálogo."""
from pathlib import Path
import json
import re
import sys
import tomllib

ROOT=Path(__file__).resolve().parents[1]
issues=[]
def issue(message):issues.append(message)
try:
    from devkit import check_catalog
    check_catalog()
except (AssertionError,KeyError,ValueError,FileNotFoundError) as exc:issue('Catálogo inválido: '+str(exc))
files=sorted((ROOT/'agents').glob('*.toml'))
if len(files)!=28:issue('Esperados 28 agentes, encontrados '+str(len(files)))
for src in files:
    try:
        obj=tomllib.loads(src.read_text(encoding='utf-8-sig'))
        for key in ('name','description','developer_instructions'):
            if not isinstance(obj.get(key),str) or not obj[key].strip():issue(f'{src.name}: campo {key} ausente')
        if obj.get('name')!=src.stem:issue(f'{src.name}: name divergente')
    except (ValueError,tomllib.TOMLDecodeError) as exc:issue(f'{src.name}: TOML inválido {exc}')
skills=sorted((ROOT/'.agents/skills').glob('*/SKILL.md'))
if len(skills)!=12:issue(f'Esperadas 12 skills próprias, encontradas {len(skills)}')
for src in skills:
    content=src.read_text(encoding='utf-8')
    front=re.match(r'\A---\n(.*?)\n---\n',content,re.S)
    if not front:issue(f'{src}: frontmatter ausente');continue
    for attr in ('name','description'):
        if not re.search(rf'(?m)^{attr}:\s*\S+',front.group(1)):
            issue(f'{src}: {attr} ausente')
    if not re.search(rf'(?m)^name:\s*{re.escape(src.parent.name)}\s*$',front.group(1)):
        issue(f'{src}: nome não corresponde à pasta')
try:
    tomllib.loads((ROOT/'templates/config-agents.toml').read_text(encoding='utf-8'))
except (ValueError,tomllib.TOMLDecodeError) as exc:issue('Template TOML inválido: '+str(exc))
versions=json.loads((ROOT/'catalog/versions.json').read_text(encoding='utf-8'))
if versions['npm'].get('skills') in ('latest',''):issue('skills CLI sem versão fixa')
for src in (ROOT/'agents').rglob('*'):
    if src.is_symlink():issue('Symlink inesperado em agentes: '+str(src))
for src in (ROOT/'.agents/skills').rglob('*'):
    if src.is_symlink():issue('Symlink inesperado em skills: '+str(src))
# v3: catálogo modular e skills específicas (offline)
try:
    from skillpacks import validate_catalog
    specialty_catalog=validate_catalog()
    if len(specialty_catalog['packs']) < 20:issue('Esperados pelo menos 20 packs')
    if len(specialty_catalog['external_skills']) < 50:issue('Catálogo externo incompleto')
except (AssertionError,KeyError,ValueError,FileNotFoundError) as exc:
    issue('Packs especializados inválidos: '+str(exc))
if issues:
    for line in issues:print('ERRO:',line)
    sys.exit(1)
print(f'OK: {len(files)} agentes, {len(skills)} skills, catálogo/versões/templates verificados offline.')
print('Nota: sem garantia de carregamento no Codex nem verificação de fontes remotas.')
