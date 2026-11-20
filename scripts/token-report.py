#!/usr/bin/env python3
"""Compara uso REAL de tokens a partir de `codex exec --json` (JSONL).
Não faz chamadas de API, não salva conteúdo, não inventa preço por token.
"""
import argparse
import json
from pathlib import Path

FIELDS=('input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens')


def summarize(path):
    totals={key:0 for key in FIELDS}
    turns=failed=0
    with Path(path).open(encoding='utf-8') as stream:
        for num,line in enumerate(stream,1):
            if not line.strip():continue
            try: event=json.loads(line)
            except json.JSONDecodeError as exc:raise ValueError(f'{path}: linha {num} inválida') from exc
            if event.get('type')=='turn.failed':failed+=1
            if event.get('type')!='turn.completed':continue
            usage=event.get('usage',{})
            if not isinstance(usage,dict):raise ValueError(f'{path}:{num}: usage não é objeto')
            for name in FIELDS:
                value=usage.get(name,0)
                if not isinstance(value,int) or value<0:
                    raise ValueError(f'{path}:{num}: {name} inválido')
                totals[name]+=value
            turns+=1
    if not turns:raise ValueError(f'{path}: nenhum turn.completed com uso de tokens')
    totals['turns']=turns
    totals['failures']=failed
    totals['total_tokens']=totals['input_tokens']+totals['output_tokens']
    totals['non_cached_input_tokens']=max(0,totals['input_tokens']-totals['cached_input_tokens'])
    return totals


def compare(baseline, optimized):
    original=baseline['total_tokens']
    reduction=100*(original-optimized['total_tokens'])/original if original else 0
    return {'baseline':baseline,'optimized':optimized,'total_reduction_pct':round(reduction,2),
            'input_reduction_pct':round(100*(baseline['input_tokens']-optimized['input_tokens'])/baseline['input_tokens'],2) if baseline['input_tokens'] else None,
            'cached_input_note':'cached_input_tokens está incluído em input_tokens; preços podem ser diferentes.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',required=True,help='JSONL de execução de referência')
    p.add_argument('--optimized',required=True,help='JSONL de execução otimizada')
    p.add_argument('--baseline-pass',choices=('yes','no','unknown'),default='unknown')
    p.add_argument('--optimized-pass',choices=('yes','no','unknown'),default='unknown')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    try:result=compare(summarize(a.baseline),summarize(a.optimized))
    except (ValueError,OSError) as e:p.error(str(e))
    result['quality']={'baseline':a.baseline_pass,'optimized':a.optimized_pass}
    result['valid_savings_claim']=(a.baseline_pass=='yes' and a.optimized_pass=='yes' and
                                   not result['baseline']['failures'] and not result['optimized']['failures'])
    if a.json:print(json.dumps(result,indent=2,ensure_ascii=False))
    else:
        print('Baseline:',result['baseline']['total_tokens'],'tokens; otimizado:',result['optimized']['total_tokens'])
        print('Redução total observada: %.2f%%'%result['total_reduction_pct'])
        print('Qualidade verificada dos dois:','SIM' if result['valid_savings_claim'] else 'NÃO — compare testes e critérios antes de concluir economia')
        print('A métrica não estima valores cobrados, cache, contexto multiagente oculto nem custo de serviços externos.')


if __name__=='__main__':main()
