# 31 — Catálogo de especialidades: skills escolhidas por tarefa

> **Versão 3.0 · 21 packs, 49 skills próprias e 55 skills externas catalogadas.** Não significa instalar tudo por padrão.

Esta curadoria diferencia **skill própria**, **skill de terceiros**, **plugin**, **CLI** e **documentação**. Fonte confiável não é garantia de segurança; revise scripts e permissões.

## Matriz de packs

| Pack | Objetivo | Skills locais | Externas | Comando de prévia |
|---|---|---:|---:|---|
| `engineering` | Engenharia, arquitetura, code review, diagnóstico e fluxos de trabalho | 5 | 8 | `python scripts/skillpacks.py plan --packs engineering` |
| `frontend` | React, TypeScript, design responsivo e estrutura de componentes | 3 | 4 | `python scripts/skillpacks.py plan --packs frontend` |
| `nextjs` | Next.js moderno, Server Components, cache e migrações | 2 | 2 | `python scripts/skillpacks.py plan --packs nextjs` |
| `design` | UI premium, design systems, antisslop visual, espaçamento e motion | 3 | 2 | `python scripts/skillpacks.py plan --packs design` |
| `accessibility` | WCAG 2.2, teclado, screen readers e formulários | 2 | 2 | `python scripts/skillpacks.py plan --packs accessibility` |
| `seo` | SEO técnico, indexação, schemas e conteúdo escalável | 3 | 6 | `python scripts/skillpacks.py plan --packs seo` |
| `performance` | Core Web Vitals, profiling, bundle e carregamento | 3 | 3 | `python scripts/skillpacks.py plan --packs performance` |
| `backend-node` | Node/NestJS, APIs, filas e regras de negócio | 4 | 1 | `python scripts/skillpacks.py plan --packs backend-node` |
| `backend-python` | Python, FastAPI, typing, migrações e testes | 3 | 2 | `python scripts/skillpacks.py plan --packs backend-python` |
| `backend-php` | PHP, Laravel, sessão, autenticação e SQL | 3 | 0 | `python scripts/skillpacks.py plan --packs backend-php` |
| `database` | Postgres, Prisma, SQL, RLS, migrações e índices | 3 | 2 | `python scripts/skillpacks.py plan --packs database` |
| `security` | AppSec autorizado, supply chain, threat modeling e segredos | 4 | 7 | `python scripts/skillpacks.py plan --packs security` |
| `qa-testing` | E2E, contratos, propriedades, flakiness e testes | 4 | 3 | `python scripts/skillpacks.py plan --packs qa-testing` |
| `devops` | Docker, GitHub Actions, deploy e rollback | 3 | 2 | `python scripts/skillpacks.py plan --packs devops` |
| `cloudflare` | Workers, D1/R2, auth edge, Turnstile e CDN | 2 | 6 | `python scripts/skillpacks.py plan --packs cloudflare` |
| `payments` | Stripe, assinaturas, checkout seguro e webhooks | 2 | 0 | `python scripts/skillpacks.py plan --packs payments` |
| `observability` | Sentry, tracing, incidentes, alertas e análise de erros | 2 | 2 | `python scripts/skillpacks.py plan --packs observability` |
| `agent-ops` | Skills confiáveis, isolamento, orquestração e economia de tokens | 4 | 3 | `python scripts/skillpacks.py plan --packs agent-ops` |
| `mobile` | React Native, UX mobile e performance | 2 | 1 | `python scripts/skillpacks.py plan --packs mobile` |
| `ai-apps` | RAG, prompts, evals e funcionalidades LLM | 3 | 1 | `python scripts/skillpacks.py plan --packs ai-apps` |
| `growth` | Analytics, experimentação, UX conversão e onboarding | 2 | 4 | `python scripts/skillpacks.py plan --packs growth` |

## Como decidir o que instalar

1. Primeiro instale o DevKit base (por exemplo `core`) com `python scripts/devkit.py install --profile core --apply`.
2. Depois detecte o stack: `python scripts/skillpacks.py recommend --target CAMINHO_DO_PROJETO`.
3. Faça uma prévia: `python scripts/skillpacks.py plan --target CAMINHO_DO_PROJETO --auto --with-external`.
4. Instale apenas as skills **locais** adequadas: `python scripts/skillpacks.py install --target CAMINHO_DO_PROJETO --auto --apply`.
5. Para instalar skills de terceiros, revise o plano, e só então acrescente `--with-external`.

**Nota sobre atualização:** o gerenciador externo `skills` suporta `npx skills check` e `npx skills update`. Use pin de release/commit em ambientes reproduzíveis, e aprove upgrades conscientemente.

## Catálogo externo por pack (fontes originais)

Uma entrada por skill, deduplicada pelo identificador do mantenedor. O DevKit não redistribui seus conteúdos.

### `engineering`

- **Local**: [`feature-slicing`](../specialties/skills/feature-slicing/SKILL.md)
- **Local**: [`codebase-navigation`](../specialties/skills/codebase-navigation/SKILL.md)
- **Local**: [`root-cause-debugging`](../specialties/skills/root-cause-debugging/SKILL.md)
- **Local**: [`pr-review-evidence`](../specialties/skills/pr-review-evidence/SKILL.md)
- **Local**: [`architecture-decision-records`](../specialties/skills/architecture-decision-records/SKILL.md)
- **Externa**: `diagnosing-bugs` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill diagnosing-bugs -a codex`.
- **Externa**: `tdd` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill tdd -a codex`.
- **Externa**: `code-review` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill code-review -a codex`.
- **Externa**: `domain-modeling` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill domain-modeling -a codex`.
- **Externa**: `improve-codebase-architecture` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill improve-codebase-architecture -a codex`.
- **Externa**: `to-spec` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill to-spec -a codex`.
- **Externa**: `verification-before-completion` — [obra/superpowers](https://github.com/obra/superpowers), instalação sob demanda com `npx skills add obra/superpowers --skill verification-before-completion -a codex`.
- **Externa**: `systematic-debugging` — [obra/superpowers](https://github.com/obra/superpowers), instalação sob demanda com `npx skills add obra/superpowers --skill systematic-debugging -a codex`.

### `frontend`

- **Local**: [`react-component-contracts`](../specialties/skills/react-component-contracts/SKILL.md)
- **Local**: [`frontend-performance`](../specialties/skills/frontend-performance/SKILL.md)
- **Local**: [`forms-validation`](../specialties/skills/forms-validation/SKILL.md)
- **Externa**: `vercel-react-best-practices` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -a codex`.
- **Externa**: `vercel-composition-patterns` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill vercel-composition-patterns -a codex`.
- **Externa**: `vercel-react-view-transitions` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill vercel-react-view-transitions -a codex`.
- **Externa**: `web-design-guidelines` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a codex`.

### `nextjs`

- **Local**: [`nextjs-boundaries`](../specialties/skills/nextjs-boundaries/SKILL.md)
- **Local**: [`nextjs-cache-review`](../specialties/skills/nextjs-cache-review/SKILL.md)
- **Externa**: `next-cache-components-optimizer` — [vercel/next.js](https://github.com/vercel/next.js), instalação sob demanda com `npx skills add vercel/next.js --skill next-cache-components-optimizer -a codex`.
- **Externa**: `next-cache-components-adoption` — [vercel/next.js](https://github.com/vercel/next.js), instalação sob demanda com `npx skills add vercel/next.js --skill next-cache-components-adoption -a codex`.

### `design`

- **Local**: [`design-token-system`](../specialties/skills/design-token-system/SKILL.md)
- **Local**: [`ai-ui-pattern-audit`](../specialties/skills/ai-ui-pattern-audit/SKILL.md)
- **Local**: [`visual-regression`](../specialties/skills/visual-regression/SKILL.md)
- **Externa**: `ui-ux-pro-max` — [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), instalação sob demanda com `npx skills add nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max -a codex`.
- **Externa**: `web-design-guidelines` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a codex`.

### `accessibility`

- **Local**: [`wcag-keyboard-audit`](../specialties/skills/wcag-keyboard-audit/SKILL.md)
- **Local**: [`forms-validation`](../specialties/skills/forms-validation/SKILL.md)
- **Externa**: `accessibility` — [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), instalação sob demanda com `npx skills add addyosmani/web-quality-skills --skill accessibility -a codex`.
- **Externa**: `web-design-guidelines` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a codex`.

### `seo`

- **Local**: [`technical-seo-check`](../specialties/skills/technical-seo-check/SKILL.md)
- **Local**: [`schema-jsonld-qa`](../specialties/skills/schema-jsonld-qa/SKILL.md)
- **Local**: [`search-intent-mapping`](../specialties/skills/search-intent-mapping/SKILL.md)
- **Externa**: `seo-audit` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill seo-audit -a codex`.
- **Externa**: `site-architecture` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill site-architecture -a codex`.
- **Externa**: `schema` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill schema -a codex`.
- **Externa**: `ai-seo` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill ai-seo -a codex`.
- **Externa**: `programmatic-seo` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill programmatic-seo -a codex`.
- **Externa**: `seo` — [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), instalação sob demanda com `npx skills add addyosmani/web-quality-skills --skill seo -a codex`.

### `performance`

- **Local**: [`frontend-performance`](../specialties/skills/frontend-performance/SKILL.md)
- **Local**: [`load-test-planning`](../specialties/skills/load-test-planning/SKILL.md)
- **Local**: [`performance-budget`](../specialties/skills/performance-budget/SKILL.md)
- **Externa**: `performance` — [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), instalação sob demanda com `npx skills add addyosmani/web-quality-skills --skill performance -a codex`.
- **Externa**: `core-web-vitals` — [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), instalação sob demanda com `npx skills add addyosmani/web-quality-skills --skill core-web-vitals -a codex`.
- **Externa**: `web-quality-audit` — [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), instalação sob demanda com `npx skills add addyosmani/web-quality-skills --skill web-quality-audit -a codex`.

### `backend-node`

- **Local**: [`api-pagination-filtering`](../specialties/skills/api-pagination-filtering/SKILL.md)
- **Local**: [`authz-matrix`](../specialties/skills/authz-matrix/SKILL.md)
- **Local**: [`background-jobs`](../specialties/skills/background-jobs/SKILL.md)
- **Local**: [`webhook-idempotency`](../specialties/skills/webhook-idempotency/SKILL.md)
- **Externa**: `domain-modeling` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill domain-modeling -a codex`.

### `backend-python`

- **Local**: [`fastapi-api-hygiene`](../specialties/skills/fastapi-api-hygiene/SKILL.md)
- **Local**: [`python-dependency-safety`](../specialties/skills/python-dependency-safety/SKILL.md)
- **Local**: [`api-pagination-filtering`](../specialties/skills/api-pagination-filtering/SKILL.md)
- **Externa**: `modern-python` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill modern-python -a codex`.
- **Externa**: `python-on-vercel` — [vercel-labs/academy-skills](https://github.com/vercel-labs/academy-skills), instalação sob demanda com `npx skills add vercel-labs/academy-skills --skill python-on-vercel -a codex`.

### `backend-php`

- **Local**: [`php-security-hygiene`](../specialties/skills/php-security-hygiene/SKILL.md)
- **Local**: [`authz-matrix`](../specialties/skills/authz-matrix/SKILL.md)
- **Local**: [`api-pagination-filtering`](../specialties/skills/api-pagination-filtering/SKILL.md)

### `database`

- **Local**: [`sql-index-analysis`](../specialties/skills/sql-index-analysis/SKILL.md)
- **Local**: [`migration-zero-downtime`](../specialties/skills/migration-zero-downtime/SKILL.md)
- **Local**: [`rls-policy-verification`](../specialties/skills/rls-policy-verification/SKILL.md)
- **Externa**: `supabase-postgres-best-practices` — [supabase/agent-skills](https://github.com/supabase/agent-skills), instalação sob demanda com `npx skills add supabase/agent-skills --skill supabase-postgres-best-practices -a codex`.
- **Externa**: `prisma-cli` — [prisma/skills](https://github.com/prisma/skills), instalação sob demanda com `npx skills add prisma/skills --skill prisma-cli -a codex`.

### `security`

- **Local**: [`authz-matrix`](../specialties/skills/authz-matrix/SKILL.md)
- **Local**: [`secrets-exposure-response`](../specialties/skills/secrets-exposure-response/SKILL.md)
- **Local**: [`security-header-audit`](../specialties/skills/security-header-audit/SKILL.md)
- **Local**: [`supply-chain-due-diligence`](../specialties/skills/supply-chain-due-diligence/SKILL.md)
- **Externa**: `code-security` — [semgrep/skills](https://github.com/semgrep/skills), instalação sob demanda com `npx skills add semgrep/skills --skill code-security -a codex`.
- **Externa**: `differential-review` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill differential-review -a codex`.
- **Externa**: `insecure-defaults` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill insecure-defaults -a codex`.
- **Externa**: `supply-chain-risk-auditor` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill supply-chain-risk-auditor -a codex`.
- **Externa**: `variant-analysis` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill variant-analysis -a codex`.
- **Externa**: `sharp-edges` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill sharp-edges -a codex`.
- **Externa**: `semgrep` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill semgrep -a codex`.

### `qa-testing`

- **Local**: [`e2e-critical-flows`](../specialties/skills/e2e-critical-flows/SKILL.md)
- **Local**: [`contract-testing`](../specialties/skills/contract-testing/SKILL.md)
- **Local**: [`flaky-test-triage`](../specialties/skills/flaky-test-triage/SKILL.md)
- **Local**: [`visual-regression`](../specialties/skills/visual-regression/SKILL.md)
- **Externa**: `property-based-testing` — [trailofbits/skills](https://github.com/trailofbits/skills), instalação sob demanda com `npx skills add trailofbits/skills --skill property-based-testing -a codex`.
- **Externa**: `tdd` — [mattpocock/skills](https://github.com/mattpocock/skills), instalação sob demanda com `npx skills add mattpocock/skills --skill tdd -a codex`.
- **Externa**: `verification-before-completion` — [obra/superpowers](https://github.com/obra/superpowers), instalação sob demanda com `npx skills add obra/superpowers --skill verification-before-completion -a codex`.

### `devops`

- **Local**: [`docker-compose-hardening`](../specialties/skills/docker-compose-hardening/SKILL.md)
- **Local**: [`ci-pipeline-gates`](../specialties/skills/ci-pipeline-gates/SKILL.md)
- **Local**: [`release-rollback`](../specialties/skills/release-rollback/SKILL.md)
- **Externa**: `deploy-to-vercel` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill deploy-to-vercel -a codex`.
- **Externa**: `wrangler` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill wrangler -a codex`.

### `cloudflare`

- **Local**: [`edge-deployment-safety`](../specialties/skills/edge-deployment-safety/SKILL.md)
- **Local**: [`security-header-audit`](../specialties/skills/security-header-audit/SKILL.md)
- **Externa**: `cloudflare` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill cloudflare -a codex`.
- **Externa**: `workers-best-practices` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill workers-best-practices -a codex`.
- **Externa**: `turnstile-spin` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill turnstile-spin -a codex`.
- **Externa**: `workers-development` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill workers-development -a codex`.
- **Externa**: `wrangler` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill wrangler -a codex`.
- **Externa**: `web-perf` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill web-perf -a codex`.

### `payments`

- **Local**: [`webhook-idempotency`](../specialties/skills/webhook-idempotency/SKILL.md)
- **Local**: [`payment-flow-acceptance`](../specialties/skills/payment-flow-acceptance/SKILL.md)

### `observability`

- **Local**: [`observability-baseline`](../specialties/skills/observability-baseline/SKILL.md)
- **Local**: [`incident-postmortem`](../specialties/skills/incident-postmortem/SKILL.md)
- **Externa**: `code-simplifier` — [getsentry/skills](https://github.com/getsentry/skills), instalação sob demanda com `npx skills add getsentry/skills --skill code-simplifier -a codex`.
- **Externa**: `secret-serialization` — [getsentry/skills](https://github.com/getsentry/skills), instalação sob demanda com `npx skills add getsentry/skills --skill secret-serialization -a codex`.

### `agent-ops`

- **Local**: [`agent-handoff-contract`](../specialties/skills/agent-handoff-contract/SKILL.md)
- **Local**: [`skill-supply-chain`](../specialties/skills/skill-supply-chain/SKILL.md)
- **Local**: [`context-budget-routing`](../specialties/skills/context-budget-routing/SKILL.md)
- **Local**: [`agent-regression-evals`](../specialties/skills/agent-regression-evals/SKILL.md)
- **Externa**: `dispatching-parallel-agents` — [obra/superpowers](https://github.com/obra/superpowers), instalação sob demanda com `npx skills add obra/superpowers --skill dispatching-parallel-agents -a codex`.
- **Externa**: `skill-scanner` — [getsentry/skills](https://github.com/getsentry/skills), instalação sob demanda com `npx skills add getsentry/skills --skill skill-scanner -a codex`.
- **Externa**: `prompt-optimizer` — [getsentry/skills](https://github.com/getsentry/skills), instalação sob demanda com `npx skills add getsentry/skills --skill prompt-optimizer -a codex`.

### `mobile`

- **Local**: [`mobile-release-check`](../specialties/skills/mobile-release-check/SKILL.md)
- **Local**: [`wcag-keyboard-audit`](../specialties/skills/wcag-keyboard-audit/SKILL.md)
- **Externa**: `vercel-react-native-skills` — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), instalação sob demanda com `npx skills add vercel-labs/agent-skills --skill vercel-react-native-skills -a codex`.

### `ai-apps`

- **Local**: [`rag-evaluation`](../specialties/skills/rag-evaluation/SKILL.md)
- **Local**: [`agent-regression-evals`](../specialties/skills/agent-regression-evals/SKILL.md)
- **Local**: [`context-budget-routing`](../specialties/skills/context-budget-routing/SKILL.md)
- **Externa**: `agents-sdk` — [cloudflare/skills](https://github.com/cloudflare/skills), instalação sob demanda com `npx skills add cloudflare/skills --skill agents-sdk -a codex`.

### `growth`

- **Local**: [`analytics-event-plan`](../specialties/skills/analytics-event-plan/SKILL.md)
- **Local**: [`search-intent-mapping`](../specialties/skills/search-intent-mapping/SKILL.md)
- **Externa**: `analytics` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill analytics -a codex`.
- **Externa**: `ab-testing` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill ab-testing -a codex`.
- **Externa**: `onboarding` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill onboarding -a codex`.
- **Externa**: `conversion-tracking` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), instalação sob demanda com `npx skills add coreyhaines31/marketingskills --skill conversion-tracking -a codex`.

