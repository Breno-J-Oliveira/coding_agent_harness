# 17 — Perfis de instalação seletiva

> **Instalação recomendada:** `python scripts/devkit.py plan --profile web --with-skills --with-tools --with-design` e, após revisão, `install --profile web --apply ...`. Os comandos abaixo são **alternativas manuais** para instalar somente ferramentas específicas, não são necessários para quem usa o instalador. Verifique a versão atual do upstream e evite instalar plugins sobrepostos por padrão.

## Perfil A — Site premium / portfolio / institucional

```powershell
npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a codex
npx skills add coreyhaines31/marketingskills --skill seo-audit --skill schema-markup --skill site-architecture -a codex
npx impeccable install --providers=codex --scope=project
npx ui-ux-pro-max-cli init --ai codex
```

Opcionais: **Unslop OU Taste** em um redesign específico. QA: Playwright CLI, auditoria de HTML renderizado e Lighthouse CI.

## Perfil B — SaaS React/Next + API + Postgres

```powershell
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --skill web-design-guidelines -a codex
npx skills add supabase/agent-skills --skill supabase-postgres-best-practices -a codex
npx skills add semgrep/skills --skill code-security -a codex
npx skills add addyosmani/agent-skills --skill code-review-and-quality -a codex
```

Opcionais: Sentry quando houver produção; Trail of Bits para autenticação, autorização, migração ou dependências críticas. QA: testes de API, E2E, security gates e controle de acesso entre usuários.

## Perfil C — Backend Python/PHP/NestJS

```powershell
npx skills add addyosmani/agent-skills --skill code-review-and-quality -a codex
npx skills add semgrep/skills --skill code-security -a codex
```

Use testes específicos do stack (pytest, PHPUnit/Pest, Vitest/Jest), contratos OpenAPI, scanners de dependência e autenticação/autorizações. Não instalar React, design ou SEO quando não se aplicam.

## Perfil D — Auditoria independente e segurança

```powershell
npx skills add semgrep/skills --skill code-security -a codex
codex plugin marketplace add trailofbits/skills
codex plugin list
# Se desejar, após revisar catálogo:
# codex plugin add differential-review@trailofbits
# codex plugin add static-analysis@trailofbits
```

Executar scanners com versão fixada e sem apontar testes ativos a ambientes não autorizados. Segurança não é uma única instalação.

## Perfil E — Equipe mínima com tokens limitados

**Somente:** `AGENTS.md` curto, `diagnosing-bugs` ou review, Playwright CLI quando houver UI e suite de testes do projeto. Zero subagentes por padrão; no máximo um em revisão complexa. Acompanhar custo por aceitação.

## Habilidades que NÃO devem ficar globais por padrão

- UI opinativa de um único projeto; stack Vue se seu projeto é React.
- Migrações Postgres em repositórios PHP/MySQL sem Postgres.
- Auditores altamente especializados que se ativam para qualquer arquivo.
- Orquestradores múltiplos que todos exigem plano, review e aprovação próprios.

## Sequência de instalação

1. Inspecionar origem, licença e scripts.
2. Fazer backup das instruções e da lista de skills.
3. Instalar uma capacidade de cada vez.
4. Reiniciar a sessão e verificar descoberta.
5. Executar uma tarefa curta de prova.
6. Registrar ganho/perda e manter ou remover.
