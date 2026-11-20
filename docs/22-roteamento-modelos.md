# 22 — Roteamento inteligente de modelos por complexidade

## O problema real

Rodar um modelo muito caro para localizar um arquivo ou examinar uma falha simples desperdiça orçamento. Por outro lado, usar um modelo fraco para arquitetura, autorização ou migrações aumenta retrabalho e risco.

**O Codex aceita modelos por subagente**, não garante um *middleware universal de interceptação* que troca modelo a cada comando shell. O ganho vem de delegar corretamente tarefas para os papéis com configurações independentes e reduzir o que chega ao contexto.

## Estrutura de decisão

| Tipo | Agentes | Modelo sugerido | Raciocínio | Resultado |
|---|---|---|---|---|
| Leitura, localização, documentação | `file_scout`, `docs_scout`, `documentation` | Modelo leve realmente disponível | low | Arquivos/linhas, fatos curtos |
| Triagem de testes e avaliação de usuário | `test_triage`, `customer`, `ux_researcher` | Modelo leve/intermediário | low/medium | Reprodução, critérios |
| Desenvolvimento não crítico | `frontend`, `backend`, `fullstack`, `database` | Modelo forte | medium | Código + testes |
| Arquitetura, segurança, revisão crítica | `architect`, `security`, `tech_lead`, `integration_reviewer` | Modelo forte | medium/high conforme necessidade | Decisão e riscos |
| Testes determinísticos | Python, `rg`, `git`, `rtk`, Playwright, Semgrep | **Nenhum modelo** | — | Evidência local sem chamadas LLM |

Os IDs são específicos do provedor, da região e do contrato. **Não configure uma string hipotética e espere que funcione.** Use a tela de seleção do Codex, documentação do provedor ou `models` da API do provedor para verificar os nomes e suas capacidades.

## Gerar TOMLs com modelos verificados

```bash
python scripts/build-model-profile.py \
  --cheap-model ID_MODELO_ECONOMICO_CONFIRMADO \
  --strong-model ID_MODELO_FORTE_CONFIRMADO \
  --cheap-effort low --strong-effort medium
```

Gera `profiles/generated-agents/*.toml`, além de um manifesto (`profiles/role-routing-manifest.json`). **Não aplica automaticamente ao Codex.** Antes da cópia, verifique no documento de cada agente se `model` e `model_reasoning_effort` são aceitos pelo seu runtime. Faça backup de roles existentes.

Exemplo de um agente gerado:

```toml
name = "file_scout"
description = "Leitor de repositórios com saídas pequenas"
developer_instructions = "Use rg e leia intervalos mínimos; sem modificações."
model = "ID_REAL_E_VALIDADO"
model_reasoning_effort = "low"
```

Para reduzir custo sem fixar o modelo de todos os filhos, **não** configure um `default_subagent_model` indiscriminadamente em `[agents]`. Deixe papéis específicos sobreporem o modelo principal. A configuração base preserva o `model` atual do usuário.

## Orquestrador não é empresa de teatro

1. Quando a pergunta é curta ou execução determinística, o agente principal resolve.
2. Quando há busca extensa, envie `file_scout` com escopo exato e teto de 10 linhas de resultado.
3. Em uma feature independente, delegue `frontend` e `backend` com arquivos separados; QA após integração.
4. Em correção crítica, mantenha o mesmo especialista para não repetir leitura e use revisor independente só no fim.
5. Não envie histórico de dezenas de mensagens aos filhos quando basta uma especificação curta.

## Como medir

Compare para as **mesmas tarefas e condições**: input tokens, output tokens, cached input tokens, número de chamadas e agentes, custo faturado, duração, bugs introduzidos, testes aprovados e critérios de aceite. Custo/token e qualidade são métricas distintas. Se não há telemetria disponível no runtime, mantenha um benchmark manual e relate a limitação.

> **Não existe economia garantida de 90% no total.** Saídas comprimidas 90% e sessões 90% mais baratas são afirmações muito diferentes. Considere sucesso quando a qualidade se mantém e o custo total medido cai.

Fontes: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex config](https://learn.chatgpt.com/docs/config-file/config-reference), [RTK](https://github.com/rtk-ai/rtk).
