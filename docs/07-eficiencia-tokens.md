# 07 — Economia de tokens e de custo sem sacrificar qualidade

> **A métrica importante é custo por tarefa aceita**, não apenas tokens por resposta. Um prompt curto que falha três vezes pode sair mais caro do que uma análise mais profunda que resolve na primeira tentativa.

## Fontes de desperdício

| Causa | Consequência | Correção |
|---|---|---|
| AGENTS.md de 800 linhas | Aumenta contexto em toda sessão | Global de ~30–80 linhas e links locais |
| 30 skills se ativando para todo pedido | Regras conflitantes | Descrições específicas + disparo sob demanda |
| 22 subagentes em paralelo | Overhead, mensagens e conflitos | Máximo inicial 3, normalmente 0–2 |
| Arquivos enormes lidos repetidamente | Contexto e custo | `rg`/paths e leitura por intervalo |
| Saídas detalhadas de cada bot | Repetição no orquestrador | Handoff de 6–10 linhas + paths |
| MCPs em excesso | Ferramentas e schemas desnecessários | CLI e skills quando viável |
| Loops de redesign sem captura visual | Reformulações sem evidência | Screenshots comparáveis + critérios |
| Modelo máximo para tarefas triviais | Custo sem benefício | Roteamento por dificuldade, após validar disponibilidade |
| Testes completos após cada caractere | Latência excessiva | Gates locais rápidos; suite completa por marco |
| Contexto acumulado obsoleto | Respostas inconsistentes | Handoff documentado e sessão nova em marcos |

## Política de modelos e raciocínio

- **Leve:** busca pontual, correção de formatação, documentação, triagem.
- **Intermediário:** implementação padrão, testes, revisão delimitada.
- **Alto:** arquitetura crítica, diagnóstico difícil, segurança e bugs complexos.

Não definir um modelo específico que a conta/provedor talvez não tenha. Preserve o modelo e o provedor já configurados por cada usuário até confirmar os IDs e capacidades disponíveis. Um nome não confirmado pode interromper a execução. Quando configurar `default_subagent_model`, medir a qualidade real das tarefas antes de escolher.

## Habilidades com contexto progressivo

Conforme recomendação da OpenAI, o documento raiz de uma skill deve ser **roteador curto**; referências grandes ficam em arquivos carregados só quando úteis. Descrições devem delimitar gatilhos com precisão (ex.: “criar/revisar migration” em vez de “qualquer tarefa de banco”). Fonte: [Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

## CLI vs MCP

[Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli) documenta que CLI + skills costuma ser mais econômico para agentes programadores, pois evita schemas extensos e snapshots gigantes no contexto. Use MCP quando ações estruturadas, estado persistente ou conectores são indispensáveis. Isso é uma **tendência de design**, não uma promessa de redução percentual universal.

## Regra de roteamento mensurável

Para cada tipo de tarefa, compare A/B:

- **A:** Codex sozinho, sem skill.
- **B:** Codex + skill adequada.
- **C:** Codex + skill + 1/2 subagentes, somente onde útil.

Registrar: qualidade dos testes, tarefas concluídas, número de iterações, duração, tokens de entrada/saída, custo estimado, erros de regressão e necessidade de intervenção humana. Se B e C não melhoram, **não manter por hábito**.

## Planilha de acompanhamento (CSV sugerido)

```csv
id,tipo,estrategia,input_tokens,output_tokens,cached_input_tokens,duracao_s,intervencoes,testes_ok,criterios_aceitos,custo_estimado
T-001,bug,A,,,,,,,
T-001,bug,B,,,,,,,
T-001,bug,C,,,,,,,
```

Dados de tokens podem ser incompletos por ferramenta/provedor; não interpretar falta de dados como uso zero. Tokens em cache **não são necessariamente gratuitos**. Veja [Observability and usage](https://developers.openai.com/api/docs/guides/agents-api/observability).

## Budget de subagentes (padrão inicial)

1. **0 subagentes** para tarefas pequenas.
2. **Até 2** para implementação paralelizável.
3. **Até 3** em arquitetura complexa ou auditorias independentes.
4. Reavaliação antes de cada novo spawn; não permitir árvores recursivas por padrão.
5. Um coordenador, responsáveis únicos por arquivo e conclusão centralizada.

## Contexto persistente recomendado

```text
AGENTS.md                 # Regras mínimas, como testar, políticas
README.md                 # Como subir o projeto
ARCHITECTURE.md           # Mapa rápido de componentes
GLOSSARY.md               # Termos do produto (se complexo)
docs/DECISIONS/           # ADRs curtos, versionados
docs/FEATURE_SPEC.md      # Escopo e aceite ativo
```

Não inserir logs de cada agente nesses documentos. Para estado transitório, usar `work/` gitignored ou comentários de PR. Sempre guardar **a decisão**, não transcrições completas do raciocínio do agente.

## Otimização prática de busca

```powershell
# Encontrar símbolos / lugares antes de abrir arquivos inteiros:
rg -n "authenticate|authorize|middleware" apps/api/src
rg --files apps/web/src | Select-Object -First 60
# Revisar somente o que mudou:
git diff --stat
git diff -- apps/api/src/auth
```

**Fontes:** [OpenAI — Rethinking skills](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), [OpenAI multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent), [Playwright CLI](https://github.com/microsoft/playwright-cli).
