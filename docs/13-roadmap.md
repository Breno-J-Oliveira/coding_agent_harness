# 13 — Roadmap realista de implantação

## Fase 1 — Base operacional (dia 1)

**Objetivo:** instalar núcleo pequeno e confirmar que funciona.

- [ ] Backup `config.toml` e `AGENTS.md`.
- [ ] Revisar modelo/provedor e chaves de subagentes no TOML.
- [ ] Validar descoberta dos papéis já existentes.
- [ ] Instalar somente Impeccable, Web Design Guidelines, Code Review e Playwright CLI (quando aplicável).
- [ ] Rodar um teste simples de leitura e outro de browser sem alterações no projeto.

**Saída:** lista de capacidades descobertas, comandos com status e nenhum arquivo perdido.

## Fase 2 — Qualidade de desenvolvimento (semana 1)

- [ ] Adotar DoD e PR template.
- [ ] Configurar lint/typecheck/tests/CI do projeto piloto.
- [ ] Criar teste E2E de uma jornada essencial.
- [ ] Adicionar Semgrep e revisão de dependências.
- [ ] Testar uma feature com Codex sozinho e com um especialista.

**Saída:** gates que rejeitam regressões observáveis.

## Fase 3 — Design, SEO e performance (semana 2)

- [ ] Estabelecer DESIGN.md com tokens e referências.
- [ ] Selecionar Unslop ou UI/UX Pro Max conforme necessidade real.
- [ ] Fazer screenshots de 390/768/1440px.
- [ ] Medir Lighthouse e Web Vitals disponíveis.
- [ ] Auditar meta/URLs/schema apenas em páginas públicas.
- [ ] Gerar relatório antes/depois com dados, não adjetivos.

**Saída:** melhora rastreável de UX e desempenho, quando validada.

## Fase 4 — Operação multiagente e produção (semanas 3–4)

- [ ] Validar 2–3 agentes em execução sem conflito.
- [ ] Formalizar tarefas e handoffs.
- [ ] Analisar custo por tarefa aceita.
- [ ] Habilitar observabilidade apropriada (Sentry ou stack existente).
- [ ] Estabelecer deploy de preview, proteção de produção e rollback.
- [ ] Fazer retrospectiva: remover skills pouco usadas, ajustar triggers.

**Saída:** processo reproduzível e custeado, não apenas arquivos de configuração.

## Projeto piloto recomendado

Escolher uma feature pequena, completa e com cenário de segurança (por exemplo, cadastro/editabilidade de um recurso com autorização por usuário), em projeto local com testes. **Não começar pelo sistema inteiro nem por uma release de produção.**

## Indicadores de maturidade

| Estágio | Sinal de sucesso |
|---|---|
| 0 — Prompting | Agente produz código, mas sem prova |
| 1 — Reprodutível | Scripts e passos documentados |
| 2 — Validado | CI e E2E rodam de verdade |
| 3 — Delegável | Agentes independentes conseguem integrar sem conflito |
| 4 — Observável | Produção tem métricas, alertas e rollback |
| 5 — Otimizado | Medimos custos/qualidade e retiramos excesso |
