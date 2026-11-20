"""Checa links Markdown relativos e valida exemplos TOML; sem rede nem mutações."""
from pathlib import Path
import re
import subprocess
import sys
root=Path(__file__).resolve().parents[1]
missing=[]
pattern=re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')
for path in [root/'README.md',*(root/'docs').glob('*.md'),*(root/'templates').glob('*.md')]:
    txt=path.read_text(encoding='utf-8')
    for dest in pattern.findall(txt):
        dest=dest.split('#',1)[0].split('?',1)[0]
        if not dest or dest.startswith(('http:','https:','mailto:','#')): continue
        dest=dest.replace('%20',' ')
        candidate=(path.parent/dest)
        if not candidate.exists(): missing.append(f'{path.relative_to(root)} -> {dest}')
if missing:
    print('Links internos ausentes:\n'+'\n'.join(missing))
    sys.exit(1)
run=subprocess.run([sys.executable, str(root/'scripts/validate-sample-config.py')],check=False)
if run.returncode: sys.exit(run.returncode)
print('OK: links internos Markdown existentes.')
