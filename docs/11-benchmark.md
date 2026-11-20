# 11 — Como testar se as skills realmente melhoram o Codex

## Hipótese e desenho

Comparar três configurações em **tarefas equivalentes**, sem mudar modelo, provedor, contexto, hardware ou dependências entre os testes (ou registrar as diferenças):

- **A — Baseline:** Codex sem skills extras; apenas ferramentas e testes existentes.
- **B — Curado:** Codex com as skills relevantes.
- **C — Multiagente:** B + subagentes em tarefas separáveis.

Rodar casos reais e reproduzíveis, preferencialmente com ordem randomizada e pelo menos três repetições por caso. Análise de amostra pequena dá sinal preliminar, não prova universal.

## Conjunto de tarefas sugerido

| Caso | Objetivo | Critérios de sucesso |
|---|---|---|
| D1 | Redesign de card/dashboard | Marca coerente, screenshot, a11y, aceitação humana |
| D2 | Remover clichês de landing page | Menos problemas validados sem perder identidade |
| F1 | Corrigir bug React | Teste vermelho→verde, nenhuma regressão |
| B1 | Implementar API com RBAC | Contrato, testes negativos, autorização por recurso |
| S1 | Auditar endpoint de upload | Achados verdadeiros e evidências, poucos falsos positivos |
| DB1 | Otimizar consulta Postgres | Plano medido, resultado sem alteração semântica |
| SEO1 | Melhorar indexação de site público | Problema corrigido e teste de URL |
| QA1 | Automatizar jornada de checkout | E2E confiável e trace em falha |

## Métricas

| Métrica | Como medir |
|---|---|
| Conclusão | % critérios aceitos por humano |
| Correção | Testes automatizados e inspeção do diff |
| Regressão | Falhas novas ao executar suite existente |
| Custo | Input/output/cache × tarifação real do provedor |
| Tempo | Início→entrega com gates completos |
| Autonomia | Intervenções humanas necessárias |
| Qualidade de design | Rubrica com avaliador cego, não só score do agente |
| Segurança | TP/FP/FN em vulnerabilidades conhecidas do teste |
| Verificação | % afirmações do relatório acompanhadas de evidência |

## Testes de segurança responsáveis

Criar pequenos projetos **isolados e propositalmente vulneráveis** apenas para avaliação autorizada, ou usar benchmarks públicos projetados para esse fim. Não apontar scans automatizados para sistemas de terceiros sem permissão.

## Controle de viés

- Mesmo briefing e escopo por variante.
- Não mostrar ao avaliador qual skill foi usada na geração.
- Repetir em tarefas distintas (skills podem brilhar apenas em seu nicho).
- Reportar casos em que uma skill piorou o resultado.
- Não medir só tokens: medir **custo por critério aceito**.
- Falsos positivos em segurança contam como custo de revisão.

## Decisão após avaliação

- **Adotar globalmente:** ganho consistente em várias tarefas e pouco contexto extra.
- **Adotar por projeto:** ganho específico de stack.
- **Sob demanda:** revisão pontual com custo alto, mas relevante.
- **Remover:** redundante, insegura, gera muito ruído ou reduz qualidade.

A referência geral de medição de tokens, cache e subagentes está na [documentação de observabilidade da OpenAI](https://developers.openai.com/api/docs/guides/agents-api/observability).
