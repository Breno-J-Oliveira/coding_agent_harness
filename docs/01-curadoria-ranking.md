# 01 — Curadoria e ranking das skills

> **Como ler:** P0 = primeira escolha na categoria; P1 = boa complementar; P2 = opcional/situacional. Isto é **curadoria editorial baseada em documentação** (12/11/2026), não ranking por benchmark próprio. Coluna “verificado” significa que o projeto e a função aparecem na documentação do mantenedor, não que foi executado localmente.

## Critérios de avaliação

| Critério | Peso editorial | Pergunta |
|---|---:|---|
| Especificidade e qualidade do fluxo | 25% | Faz uma tarefa concreta melhor do que um prompt genérico? |
| Segurança e procedência | 20% | Origem verificável, acesso controlável, scripts legíveis? |
| Verificabilidade | 20% | Produz teste, métrica, relatório, diff ou evidência? |
| Adequação ao Codex | 15% | Existe instalação para Codex? |
| Economia operacional | 10% | É contextual e minimiza leituras/output? |
| Manutenção e licenciamento | 10% | Publicação e licença claras? |

**Regra:** evite instalar simultaneamente soluções muito parecidas (ex.: três orquestradores obrigatórios ou quatro revisores de design disparados automaticamente). Prioridades não substituem testes no seu stack.

## Design, UX, estética e conversão

| Prioridade | Ferramenta / skill | Origem | Emprego ideal | Limite / ressalva |
|---|---|---|---|---|
| **P0** | [Impeccable](https://github.com/pbakaus/impeccable) | Paul Bakaus | 24 comandos de crítica, layout, tipografia, polimento e detector de AI slop | Hook precisa de aprovação; revisar scripts |
| **P0** | [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | NextLevelBuilder | Biblioteca local de estilos, paletas e combinações tipográficas | Biblioteca não substitui testes com usuários |
| **P0** | [web-design-guidelines](https://github.com/vercel-labs/agent-skills) | Vercel | Interface, acessibilidade e padrões UX | É orientação; confirme com browser + axe |
| **P1** | [Unslop](https://github.com/heydamir/unslop) | Damir Sokolovsky | Eliminar clichês visuais e melhorar consistência | Sobreposição com Impeccable; requer atribuição CC BY 4.0 |
| **P1** | [Taste Skill](https://github.com/Leonxlnx/taste-skill) | Leonxlnx | Sites de apresentação com composição visual mais forte | Fluxo opinativo; depende de navegador/Node |
| **P1** | [react-view-transitions](https://github.com/vercel-labs/agent-skills) | Vercel | Transições de interface em React | Apenas quando compatível e necessário |
| **P2** | [react-composition-patterns](https://github.com/vercel-labs/agent-skills) | Vercel | Design de APIs de componentes reutilizáveis | Não aplicável em projetos HTML simples |

## Frontend, arquitetura e engenharia

| Prioridade | Ferramenta / skill | Origem | Emprego ideal | Limite / ressalva |
|---|---|---|---|---|
| **P0** | [react-best-practices](https://github.com/vercel-labs/agent-skills) | Vercel | React e Next.js, data fetching, bundles e renderização | Não usar em apps não React |
| **P0** | [code-review-and-quality](https://github.com/addyosmani/agent-skills) | Addy Osmani | Revisão correctness, legibilidade, arquitetura, segurança e perf | Não substitui CI nem revisão humana |
| **P0** | [diagnosing-bugs](https://github.com/mattpocock/skills) | Matt Pocock | Reproduzir, diagnosticar, minimizar e criar regressão | Evitar para bugs triviais |
| **P1** | [tdd](https://github.com/mattpocock/skills) | Matt Pocock | Red → green → refactor para lógica de negócio | Exige testes confiáveis |
| **P1** | [spec-driven-development](https://github.com/addyosmani/agent-skills) | Addy Osmani | Definir comportamento antes de implementar | Não exagerar em projetos pequenos |
| **P1** | [Superpowers](https://github.com/obra/superpowers) | Jesse Vincent / comunidade | Fluxos de brainstorming, planos, testes e revisão | Pode ser redundante com Addy/Matt; escolha um principal |
| **P1** | [Vue Skills](https://github.com/antfu/skills) | Anthony Fu | Vue 3/Composition API | Só se usar Vue |
| **P1** | [prototype](https://github.com/mattpocock/skills) | Matt Pocock | Explorar decisões com protótipos descartáveis | Prototipagem não é código final |
| **P2** | [domain-modeling](https://github.com/mattpocock/skills) | Matt Pocock | Domínios complexos e linguagem ubíqua | Pode ser exagero para site estático |

## Backend, banco, APIs e operações

| Prioridade | Ferramenta / skill | Origem | Emprego ideal | Limite / ressalva |
|---|---|---|---|---|
| **P0** | [supabase-postgres-best-practices](https://github.com/supabase/agent-skills) | Supabase | Postgres, índices, transações, RLS, query plans | Postgres, não MySQL nem SQLite |
| **P1** | [Sentry for AI](https://github.com/getsentry/sentry-for-ai) | Sentry | Instrumentar, depurar e monitorar produção | Depende de conta Sentry e cuidado com PII |
| **P1** | [vercel-optimize](https://github.com/vercel-labs/agent-skills) | Vercel | Custos e gargalos em projetos Vercel | Só quando a implantação é na Vercel |
| **P1** | [gh-cli](https://github.com/trailofbits/skills) | Trail of Bits | Fluxos GitHub autenticados | Ferramenta externa e privilégios mínimos |
| **P1** | [Playwright CLI](https://github.com/microsoft/playwright-cli) | Microsoft | Automação web com contexto reduzido | Ferramenta CLI + skill, não apenas SKILL.md |
| **P2** | [devcontainer-setup](https://github.com/trailofbits/skills) | Trail of Bits | Ambientes reprodutíveis | Docker não é necessário em todo projeto |

## Segurança defensiva e revisão de software

| Prioridade | Ferramenta / skill | Origem | Emprego ideal | Limite / ressalva |
|---|---|---|---|---|
| **P0** | [code-security](https://github.com/semgrep/skills) | Semgrep | Diretrizes de coding seguro | Skill em beta; **execute scanner real** |
| **P0** | [static-analysis](https://github.com/trailofbits/skills) | Trail of Bits | Processos para Semgrep, CodeQL e SARIF | Instalação por marketplace; ferramentas auxiliares |
| **P0** | [differential-review](https://github.com/trailofbits/skills) | Trail of Bits | Revisar diff e mudanças sensíveis | Não avalia todo sistema sozinho |
| **P1** | [insecure-defaults](https://github.com/trailofbits/skills) | Trail of Bits | Configs fail-open e padrões inseguros | Conferir falsos positivos |
| **P1** | [supply-chain-risk-auditor](https://github.com/trailofbits/skills) | Trail of Bits | Dependências, install scripts, fornecedores | Complemente com avisos atualizados |
| **P1** | [sharp-edges](https://github.com/trailofbits/skills) | Trail of Bits | APIs suscetíveis a erro humano | Revisão manual final |
| **P1** | [fp-check](https://github.com/trailofbits/skills) | Trail of Bits | Validar falsos positivos antes do relatório | Exige evidência |
| **P2** | [Cloudflare Security Audit](https://github.com/cloudflare/security-audit-skill) | Cloudflare | Auditoria multiestágio | Confira manutenção, permissões e adequação ao stack |

## SEO, conteúdo, performance e crescimento

| Prioridade | Ferramenta / skill | Origem | Emprego ideal | Limite / ressalva |
|---|---|---|---|---|
| **P0** | [seo-audit](https://github.com/coreyhaines31/marketingskills) | Corey Haines | SEO técnico, on-page e diagnóstico | Não tem acesso automático ao Search Console |
| **P0** | [schema](https://github.com/coreyhaines31/marketingskills) | Corey Haines | Dados estruturados JSON-LD | Validar com Google Rich Results Test |
| **P0** | [site-architecture](https://github.com/coreyhaines31/marketingskills) | Corey Haines | Navegação, páginas e hierarquia de URL | Depende do objetivo de negócio |
| **P1** | [ai-seo](https://github.com/coreyhaines31/marketingskills) | Corey Haines | Visibilidade em buscadores e experiências de IA | Campo em evolução; medir resultados reais |
| **P1** | [programmatic-seo](https://github.com/coreyhaines31/marketingskills) | Corey Haines | Páginas programáticas com valor próprio | Evitar páginas em massa de baixo valor |
| **P1** | [analytics](https://github.com/coreyhaines31/marketingskills) | Corey Haines | Plano de eventos e métricas | Privacidade e consentimento |
| **P1** | [cro](https://github.com/coreyhaines31/marketingskills) | Corey Haines | Conversão e UX comercial | Validação por experimento |
| **P0** | [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) | GoogleChrome | Monitoramento e prevenção de regressão | Ferramenta/CI, não skill |

## Melhores combinações por problema

| Problema | Começar por | Adicionar se necessário | Evitar |
|---|---|---|---|
| Site parece gerado por IA | Impeccable | Unslop **ou** Taste | Todos os três reescrevendo tudo ao mesmo tempo |
| Interface inconsistente | UI/UX Pro Max + design tokens | Vercel Web Guidelines | Adotar estética arbitrária sem briefing |
| React lento | React Best Practices + profiler | Lighthouse CI | Otimizar sem baseline |
| Bug recorrente | diagnosing-bugs + testes | differential-review | `try/catch` genérico sem causa-raiz |
| Falha de permissão | Threat model + Semgrep + E2E de autorização | Trail of Bits | Declarar segurança apenas por lint |
| Site não indexa | seo-audit + Search Console | schema, site-architecture | Produzir 500 páginas sem demanda |
| SQL lento | Supabase Postgres Best Practices + `EXPLAIN` | observabilidade | Criar índices sem medir |
| Alto custo de agentes | AGENTS curto + skills sob demanda | telemetria de tokens | 22 bots por padrão |

## Fontes

Os links em cada linha apontam para os repositórios originais. Consulte também [metodologia e fontes](12-fontes.md). Não interpretamos stars como prova de eficácia nem atribuímos notas numéricas de benchmark que não foram medidas.
