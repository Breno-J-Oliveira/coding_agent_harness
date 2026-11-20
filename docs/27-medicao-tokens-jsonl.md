# Medição real de tokens — evidência, não promessa

O RTK otimiza outputs específicos. Roteamento por agentes muda o modelo **em tarefas delegadas**, quando o provedor oferece IDs compatíveis. A qualidade e a economia só podem ser comparadas usando tarefas equivalentes.

## Experimento controlado

1. Prepare duas cópias idênticas do mesmo repositório, ou use `git worktree` com o mesmo commit.
2. Defina tarefa, prazo, ambiente, critérios de aceite e testes. Em baseline, use apenas a configuração de referência; na segunda execução, ative RTK, roteamento e/ou as skills relevantes.
3. Execute `codex exec --json "<tarefa>" > baseline.jsonl` e a versão otimizada em ambiente equivalente.
4. **Não publique os JSONL**: itens podem conter caminhos, comandos, partes de código ou dados sensíveis. Mantenha-os em pasta ignorada pelo Git.
5. Execute testes de produto em ambos os resultados. Não confunda sucesso do script com sucesso da funcionalidade.
6. Compare:

```bash
python scripts/token-report.py --baseline baseline.jsonl --optimized otimizado.jsonl --baseline-pass yes --optimized-pass yes
```

Exemplo de smoke test interno (dados **fictícios**):

```bash
python scripts/token-report.py --baseline benchmarks/fixtures/baseline.jsonl --optimized benchmarks/fixtures/optimized.jsonl
```

O script lê apenas eventos `turn.completed` e soma `input_tokens` e `output_tokens`. `cached_input_tokens` **já está incluído** em `input_tokens`: não some de novo. A taxa de cache não reflete automaticamente o custo financeiro. `reasoning_output_tokens` também pode ser subconjunto dos tokens de saída, não deve ser somado duas vezes. Se o Codex ou fornecedor não expuser esses eventos, o script acusa ausência em vez de inventar números.

## Critérios de aceitação de uma otimização

- O produto mantém comportamentos, testes e requisitos de segurança.
- O desempenho não piora sistematicamente; compare latência e número de tentativas.
- Tokens totais, saída de comandos, preço efetivo e tempo devem ser medidas **separadas**.
- Compare várias tarefas de tipos diferentes e reporte média/mediana/faixa. Um único benchmark não prova desempenho geral.
- Uma redução extrema em comandos (`rtk gain`) não prova redução igual do orçamento total do modelo.

Fontes: [Codex exec JSON](https://learn.chatgpt.com/docs/non-interactive-mode) e [RTK Quick Start](https://github.com/rtk-ai/rtk/blob/develop/docs/guide/getting-started/quick-start.md).
