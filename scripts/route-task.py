#!/usr/bin/env python3
"""Sugeridor local de tarefas e delegação. NÃO troca modelos nem inicia bots sozinho."""
import argparse
import json
import re

RULES={
 'security':('segurança','vulnerab','pentest','autorização','auth','owasp','cve','threat','ameaça','privacy','privacidade'),
 'frontend':('interface','componente','react','next.js','css','frontend','front-end','tela','responsivo'),
 'backend':('api','backend','back-end','endpoint','nest','fastapi','rotas','servidor','graphql'),
 'qa':('test','teste','bug','regressão','e2e','playwright','falha'),
 'ui_designer':('design','layout','figma','tipografia','espaçamento','visual','cores'),
 'seo':('seo','schema.org','indexação','sitemap','canonical','search console'),
 'database':('banco','postgres','mysql','sql','migration','migração','índice'),
 'devops':('deploy','docker','ci/cd','github actions','pipeline','infraestrutura'),
 'architect':('arquitetura','refatoração ampla','sistema inteiro','escalabilidade','integração'),
 'file_scout':('ler arquivo','localizar','encontrar arquivo','onde fica','buscar função','find file'),
 'docs_scout':('documentação','docs','biblioteca','readme','procurar docs')}
HIGH_RISK={'security','devops','architect'}


def route(task, risk='normal'):
    text=task.casefold()
    found={role:sum(word in text for word in keywords) for role,keywords in RULES.items()}
    matched=sorted((role for role in found if found[role]),key=lambda x:(-found[x],x))
    trivial=(len(text)<110 and len(matched)<=1 and risk=='normal')
    if trivial and not matched: mode='principal';agents=[]
    elif trivial and matched and matched[0] not in HIGH_RISK:mode='principal';agents=[]
    else:
        mode='especialistas'
        agents=matched[:3] or ['tech_lead']
    risk_level='elevado' if risk=='high' or any(r in HIGH_RISK for r in matched) else 'normal'
    return {'mode':mode,'agents':agents,'risk':risk_level,'model_policy':
            'modelo forte/revisão independente' if risk_level=='elevado' else
            'modelo leve para leitura; principal para edição; comparar qualidade',
            'notes':'Sugestão heurística; não existe interceptação automática de tarefas nem garantia de economia.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('task',help='Descrição curta da tarefa')
    p.add_argument('--risk',choices=('normal','high'),default='normal')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    result=route(a.task,a.risk)
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print('Execução:',result['mode'],'\nAgentes:',', '.join(result['agents']) or 'nenhum')
        print('Risco:',result['risk'],'\nModelos:',result['model_policy'])
        print(result['notes'])


if __name__=='__main__':main()
