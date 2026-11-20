#!/usr/bin/env python3
"""Gera perfis de agentes com modelos por papel, SEM editar ~/.codex.
Exemplo: python scripts/build-model-profile.py --cheap-model modelo-barato --strong-model modelo-forte
"""
import argparse
import json
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIGHT = {"file_scout", "test_triage", "docs_scout", "documentation", "customer", "ux_researcher", "product_owner"}
HEAVY = {"director", "architect", "tech_lead", "security", "backend", "frontend", "fullstack", "database", "qa", "devops", "integration_reviewer"}
VALID_EFFORT = {"low", "medium", "high", "xhigh"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cheap-model', required=True, help='ID EXATO de modelo leve CONFIRMADO no provedor')
    parser.add_argument('--strong-model', required=True, help='ID EXATO de modelo forte CONFIRMADO no provedor')
    parser.add_argument('--cheap-effort', default='low', choices=sorted(VALID_EFFORT))
    parser.add_argument('--strong-effort', default='medium', choices=sorted(VALID_EFFORT))
    parser.add_argument('--output', default='profiles/generated-agents')
    args = parser.parse_args()
    source = ROOT / 'agents'
    out = Path(args.output)
    if not out.is_absolute(): out = ROOT / out
    if out == source or source in out.parents:
        parser.error('Saída não pode substituir a fonte agents/')
    if out.exists() and any(out.iterdir()):
        parser.error(f'Diretório de saída não está vazio: {out}. Use outro caminho.')
    out.mkdir(parents=True, exist_ok=True)
    report=[]
    for src in sorted(source.glob('*.toml')):
        raw=src.read_text(encoding='utf-8')
        obj=tomllib.loads(raw)
        name=obj['name']
        tier='economico' if name in LIGHT else 'profundo' if name in HEAVY else 'equilibrado'
        if tier == 'economico': model,effort=args.cheap_model,args.cheap_effort
        elif tier == 'profundo': model,effort=args.strong_model,args.strong_effort
        else: model,effort=args.cheap_model,'medium'
        if 'model' in obj or 'model_reasoning_effort' in obj:
            parser.error(f'O agente {src.name} já define um modelo. Mescle manualmente.')
        content = raw.rstrip() + f'\n\n# Gerado por build-model-profile.py; validar disponibilidade no provedor.\nmodel = {json.dumps(model, ensure_ascii=False)}\nmodel_reasoning_effort = {json.dumps(effort)}\n'
        tomllib.loads(content)
        (out/src.name).write_text(content,encoding='utf-8')
        report.append({'agent':name,'tier':tier,'model':model,'reasoning_effort':effort})
    (out.parent/'role-routing-manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Gerados {len(report)} agentes em {out}')
    print('ATENÇÃO: IDs foram fornecidos por você, não verificados. Codex não foi alterado.')
    print('Verifique os modelos disponíveis no seu provedor ANTES de instalar. Veja docs/22-roteamento-modelos.md')

if __name__=='__main__': main()
