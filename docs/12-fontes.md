# 12 — Fontes, critérios de pesquisa e verificabilidade

**Data da curadoria:** 12 de novembro de 2026. **Alvo:** Codex Desktop/CLI no Windows. **Status:** pesquisa documental dos repositórios e páginas de mantenedores; não foi feita instalação de terceiros no computador do usuário.

## Hierarquia de evidências

1. Documentação oficial e README do projeto (preferência).
2. Código de exemplo / `SKILL.md` do próprio mantenedor.
3. Guias técnicos de organizações reconhecidas (OWASP, Google, OpenAI).
4. Discussões comunitárias (usadas apenas para identificar tendências, não para comprovar desempenho).

### Fontes primárias — plataforma e custos

- [OpenAI — Codex Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) — seções `[agents]`, limites, providers e config.
- [OpenAI — Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) — TOML individual e herança.
- [OpenAI — AGENTS.md / prompting](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) — instruções contextuais.
- [OpenAI — Rethinking skills](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — descrição precisa e disclosure progressivo.
- [OpenAI — Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) — trade-off entre paralelismo e uso de tokens (documentação da API; extrapolação para Codex apenas como princípio).
- [OpenAI — Observability and usage](https://developers.openai.com/api/docs/guides/agents-api/observability) — tokens de input, output, cache e agentes.
- [Vercel Labs — skills CLI](https://github.com/vercel-labs/skills) — `npx skills add`, filtros, listagem e global.

### Fontes primárias — design

- [Paul Bakaus — Impeccable](https://github.com/pbakaus/impeccable) — comandos, detector, hook, instalação.
- [Damir Sokolovsky — Unslop](https://github.com/heydamir/unslop) — revisão em etapas; licença CC BY 4.0.
- [NextLevelBuilder — UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — CLI `uipro` e catálogo de diretrizes.
- [Leonxlnx — Taste Skill](https://github.com/Leonxlnx/taste-skill) — layout/consistency gate, instalação.
- [Vercel — Agent Skills](https://github.com/vercel-labs/agent-skills) — performance React, web design guidelines, view transitions.

### Fontes primárias — engenharia e testes

- [Matt Pocock — Skills for Real Engineers](https://github.com/mattpocock/skills) — TDD, diagnosis, prototyping, domain modeling.
- [Addy Osmani — Agent Skills](https://github.com/addyosmani/agent-skills) — spec, plan, review, build, ship.
- [Jesse Vincent — Superpowers](https://github.com/obra/superpowers) — metodologia e fluxos; plugin do Codex.
- [Microsoft — Playwright CLI](https://github.com/microsoft/playwright-cli) — automação em CLI e skills mais concisas.
- [Supabase — Agent Skills](https://github.com/supabase/agent-skills) — Postgres e RLS.
- [Sentry — Sentry for AI](https://github.com/getsentry/sentry-for-ai) — instrumentação e debug de produção.
- [GoogleChrome — Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) — budget e regressão.

### Fontes primárias — segurança

- [Semgrep — Skills](https://github.com/semgrep/skills) — diretrizes de secure coding; beta.
- [Trail of Bits — Skills](https://github.com/trailofbits/skills) — auditoria differential, static, insecure defaults e supply chain.
- [Cloudflare — Security Audit Skill](https://github.com/cloudflare/security-audit-skill) — auditoria com revisões independentes.
- [OWASP — ASVS](https://owasp.org/www-project-application-security-verification-standard/) — requisitos verificáveis.
- [OWASP — Cheat Sheet Series](https://cheatsheetseries.owasp.org/) — medidas técnicas detalhadas.
- [OWASP — ZAP](https://www.zaproxy.org/) — testes dinâmicos autorizados.
- [GitHub — CodeQL](https://codeql.github.com/) — análise de código.
- [Trivy](https://github.com/aquasecurity/trivy) — scans de dependências, imagem e configuração.

### Fontes primárias — SEO e web

- [Corey Haines — Marketing Skills](https://github.com/coreyhaines31/marketingskills) — SEO Audit, Schema, Site Architecture, Analytics.
- [Google — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=pt) — boas práticas sem mitos de ranking.
- [Google — Search developer guide](https://developers.google.com/search/docs/fundamentals/get-started-developers) — indexação e renderização.
- [web.dev — Web Vitals](https://web.dev/articles/vitals) — LCP, INP, CLS.

### Comunidade — sinal, não prova

- [r/codex — Skills úteis no período Sol/Astra](https://www.reddit.com/r/codex/comments/1wgvaa6/what_agent_skills_do_you_actually_find_useful_in/) — relatos favorecem skills estreitas, testes e fluxos mensuráveis; amostra pequena e não representativa.
- [r/codex — Economia de tokens](https://www.reddit.com/r/codex/comments/1rm5wgq/what_is_your_secret_to_save_tokens/) — relatos de AGENTS enxuto, seleção de esforço e revisão periódica.

## Limitações da pesquisa

- A existência de um repositório foi verificada pelo conteúdo acessível em novembro de 2026; isso não prova que todo comando será aceito pela sua versão e configuração de terceiros.
- A compatibilidade declarada pelo mantenedor não equivale à execução comprovada no seu computador.
- Não instalamos nem executamos pacotes de terceiros aqui. As instruções incluem verificações obrigatórias para sua máquina.
- Não atribuimos notas por estrelas ou seguidores; relevância e manutenção mudam.
- Fontes de comunidade são opiniões, não ensaios controlados.
- As sugestões de “melhores” consideram o conjunto de necessidades descrito (projetos web full stack e qualidade premium), não cada framework existente.

## Atualização sugerida

A cada 30–60 dias, confira release/changelog, licença, comandos de instalação, permissões, conflitos, descontinuações e execução de benchmark curto. Toda nova skill deve justificar: **qual erro repetido evita? qual evidência produz? qual custo adiciona?**

### Fontes adicionais para engenharia de contexto e comunidade

- [OpenAI — Build Skills](https://learn.chatgpt.com/docs/build-skills) — skills sob demanda e limite de contexto inicial.
- [LucianLabs — análise de 12 sessões](https://lucianlabs.dev/en/notes/codex-token-xray-sessions/) — estudo observacional limitado, útil para hipóteses sobre custo de ferramentas.
- [Reddit — discussão sobre skills demais](https://www.reddit.com/r/ClaudeCode/comments/1t4cy2y/what_do_you_do_when_you_have_too_much_skills/) — opiniões individuais, sem validação experimental.
- [Reddit — como gerenciar contexto](https://www.reddit.com/r/ClaudeCode/comments/1w3d8oa/how_to_manage_context_better/) — relatos sobre handoff e simplificação.
