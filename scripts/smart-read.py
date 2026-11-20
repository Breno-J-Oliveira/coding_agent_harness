#!/usr/bin/env python3
"""Leitura local com orçamento de linhas; não chama LLM nem transmite arquivos. Evita dumps de arquivos inteiros."""
from pathlib import Path
import argparse
import sys

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',help='Caminho de arquivo UTF-8')
    p.add_argument('--find',default=None,help='Busca literal sem diferenciar maiúsculas')
    p.add_argument('--before',type=int,default=3)
    p.add_argument('--after',type=int,default=5)
    p.add_argument('--max-lines',type=int,default=60)
    p.add_argument('--start',type=int,default=1)
    a=p.parse_args()
    if a.max_lines<1 or a.max_lines>500: p.error('max-lines deve estar entre 1 e 500')
    if a.before<0 or a.after<0: p.error('Contexto deve ser >= 0')
    path=Path(a.file).resolve()
    if not path.is_file(): p.error('Arquivo não encontrado')
    if path.stat().st_size>20*1024*1024: p.error('Arquivo >20MB: use rg ou ferramenta especializada')
    content=path.read_text(encoding='utf-8',errors='replace').splitlines()
    if a.find is None:
        ix=list(range(max(0,a.start-1),min(len(content),a.start-1+a.max_lines)))
    else:
        found=[i for i,line in enumerate(content) if a.find.casefold() in line.casefold()]
        spans=set()
        for i in found:
            spans.update(range(max(0,i-a.before),min(len(content),i+a.after+1)))
        ix=sorted(spans)[:a.max_lines]
        print(f'# matches={len(found)} visible={len(ix)} total_lines={len(content)} file={path}')
    for i in ix:print(f'{i+1:5} | {content[i][:600]}')
    if len(ix)==a.max_lines:print('# output capped; refine --find or --start')
if __name__=='__main__':main()
