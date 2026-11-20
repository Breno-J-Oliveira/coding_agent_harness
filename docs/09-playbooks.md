# 09 — Playbooks reutilizáveis para o Codex

## 1. Nova feature SaaS

```text
Objetivo: implementar [feature] em [módulo], mantendo interfaces e contratos existentes.
Primeiro: confirme requisitos, 3 a 7 critérios de aceite e teste negativo crítico.
Localize os arquivos relevantes (não leia o monorepo inteiro).
Crie plano enxuto e só delegue fluxos independentes de frontend/backend.
Implemente a menor fatia vertical funcional. Teste lint, tipos, unidade, integração e E2E apropriados.
Valide autorização e dados de outro usuário quando houver multi-tenant.
Entregue: diff, comandos/testes + resultados, riscos e pendências reais. Não faça deploy.
```

## 2. Bug difícil com regressão

```text
Reproduza [sintoma] antes de editar código. Registre cenário, entrada e resultado real.
Use diagnosing-bugs: hipóteses plausíveis, instrumentação mínima, isolamento da causa.
Escreva teste que falha antes do fix e passa após o fix. Não encubra erro com fallback falso.
Verifique efeitos colaterais. Entregue evidências e causa-raiz.
```

## 3. Redesign com identidade forte

```text
Audite somente [rota/componente] usando Impeccable. Preserve marca, comportamento e tokens válidos.
Critique genericidade visual, espaçamento, copy, fluxo e acessibilidade.
Tire screenshots 390 e 1440px, liste até 5 problemas ordenados por impacto.
Corrija de forma incremental, rode detector e verifique teclado/formulários/estados.
Compare screenshots antes/depois. Não redesenhe o sistema inteiro.
```

## 4. Auditoria de segurança autorizada

```text
Analise o repositório em modo defensivo e somente leitura primeiro.
Escopo: autenticação, autorização por recurso, validação, dependências, CI, segredos e configurações.
Use skills Semgrep/Trail of Bits onde aplicável; diferencie achados de hipóteses.
Não faça testes invasivos em produção. Não copie credenciais.
Priorize por risco, cite arquivo/linha, evidência, cenário, fix e teste de regressão.
```

## 5. SEO de site público

```text
Audite [URL] e repositório usando seo-audit, schema e site-architecture.
Verifique HTML renderizado, canonical, robots, sitemap, indexabilidade, meta, JSON-LD e UX.
Se não houver acesso ao Search Console, diga isso; não invente dados de ranking.
Tire baseline Lighthouse e proponha correções priorizadas com evidências.
```

## 6. Pré-release

```text
Revise diff vs escopo, execute quality gates do projeto e apresente evidências.
Inclua testes de jornada crítica, permissões, responsividade e rollback.
Não declare produção pronta se houver falha bloqueante ou testes não executados.
Peça aprovação para deploy/migração destrutiva, qualquer custo externo ou uso de credenciais.
```

## 7. Revisão de custo de agentes

```text
Avaliando as últimas 5 tarefas: compare gasto de tokens, duração, qualidade, retrabalho e quantidade de spawns.
Identifique skills redundantes, leituras amplas e handoffs prolixos.
Proponha mudanças pequenas em AGENTS.md, papéis e ativação de skills.
Não edite configurações sem mostrar diff e riscos.
```

## 8. Simulação de cliente

```text
Atue como uma PERSONA HIPOTÉTICA de [perfil] tentando executar [tarefa].
Explique dificuldades prováveis e perguntas de validação, sem inventar entrevistas nem dados reais.
Depois execute uma jornada E2E com Playwright se o projeto estiver rodando.
Separe: hipótese simulada, problema observado, recomendação e teste real.
```
