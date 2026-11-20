# 19 — Implantação sem destruir o ambiente existente

## Perfil A — Site institucional premium

**Instale no projeto:** Impeccable, Web Design Guidelines, UI/UX Pro Max e SEO Audit. Adicione Playwright CLI e Lighthouse CI como ferramentas, não como processos obrigatórios em cada edição.

**Delegação:** frontend + ui_designer só se houver tarefas separáveis; QA revisa depois. **Teste:** responsividade, navegação, acessibilidade, indexação e performance. **Evite:** scanners invasivos em sites públicos de terceiros.

## Perfil B — SaaS autenticado

**Instale:** React Best Practices (se React), `code-security`, skill de debugging/TDD, Supabase Postgres Best Practices (se PostgreSQL), Playwright CLI. Adicione Semgrep CLI, dependency scans, verificação de authz/RLS e observabilidade.

**Delegação:** frontend/backend em caminhos separados; security e QA realizam revisão independente. **Teste:** IDOR, papéis de usuário, pagamentos em sandbox, sessões, upload e fluxos reais.

## Perfil C — API / automação

**Instale:** TDD ou revisão de código, segurança, orientações atuais da linguagem/framework. Desative skills de SEO e design não relevantes. **Teste:** contratos, migrações, integração, desempenho e erros.

## Critério de promoção de uma skill

1. Descrever a dor que a skill resolve.
2. Comparar tarefas reais com e sem skill (mesma branch/brief).
3. Medir tempo, tokens (quando disponíveis), número de correções, regressões e satisfação humana.
4. Verificar código e scripts incluídos; manter versão/revisão documentada.
5. Se falhar, remover do catálogo padrão; manter como experimental.

## Scorecard para teste local (preencher)

| Skill | Caso de teste | Sem skill | Com skill | Evidência | Decisão |
|---|---|---|---|---|---|
| Impeccable | Consistência de layout | Não medido | Não medido | Screenshots + checklist | Pendente |
| code-security | Correção de controle de acesso | Não medido | Não medido | Teste de autorização | Pendente |
| seo-audit | Identificar bloqueios de indexação | Não medido | Não medido | URL inspection | Pendente |

**Não transforme preferências da comunidade em números de performance inventados.**
