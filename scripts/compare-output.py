#!/usr/bin/env python3
"""Compara TAMANHO de texto de saídas bruta e RTK; NÃO mede consumo total de tokens."""
import argparse
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('raw_output')
p.add_argument('compressed_output')
a=p.parse_args()
r=Path(a.raw_output).read_bytes(); c=Path(a.compressed_output).read_bytes()
print(f'Bruto: {len(r):,} bytes (estimativa {len(r)/4:,.0f} tokens)')
print(f'RTK:   {len(c):,} bytes (estimativa {len(c)/4:,.0f} tokens)')
print(f'Redução estimada do output: {100*(1-len(c)/max(1,len(r))):.1f}%')
print('Não mede prompts, histórico, raciocínio, API, qualidade ou preço total. Compare sessões reais.')
