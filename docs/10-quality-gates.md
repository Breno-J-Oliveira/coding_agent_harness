# 10 — Quality gates, Definition of Done e CI/CD

## Gate por momento

| Momento | O que deve passar | Saída |
|---|---|---|
| Commit local | Formatação, lint e verificações rápidas | Sem erro bloqueante |
| PR | Build, tipos, unidade, integração, secrets, dependências | Evidência de CI |
| Preview | E2E de jornada crítica, acessibilidade e review visual | Screenshot/trace |
| Pré-release | Migrações, flags, rollback, privacidade, autorização | Aprovação explícita |
| Produção | Healthcheck, métricas, erro, alerta e rollback pronto | Release ID + acompanhamento |

## Definition of Done (DoD)

- [ ] Requisito e critérios de aceite cumpridos, com evidência.
- [ ] Diff sem mudanças não autorizadas.
- [ ] Código legível, no padrão do repositório.
- [ ] Testes relevantes executados (não apenas escritos).
- [ ] Autenticação/autorização e privacidade revisadas quando necessárias.
- [ ] Nenhum segredo no código, log, issue ou PR.
- [ ] Front: estados de erro/carregamento, responsividade e teclado.
- [ ] Performance e SEO analisados quando afetados.
- [ ] Migrações e rollback documentados quando aplicáveis.
- [ ] Documentação atualizada onde o comportamento mudou.
- [ ] Revisão humana nos pontos de risco (produção, pagamentos, dados, permissões).

## RACI simplificado

| Tarefa | Responsável por executar | Revisor | Quem autoriza |
|---|---|---|---|
| Feature padrão | Front/Back/Fullstack | Tech Lead + QA | Humano para merge relevante |
| Migração | Database | Backend + Security | Humano se destrutiva |
| Auth e autorização | Backend | Security + QA | Humano |
| Redesign | UI + Frontend | UX + QA | Humano para mudança de marca |
| CI / Deploy | DevOps | Tech Lead + Security | Humano para produção |
| SEO | SEO/design + Front | QA | Humano para conteúdo público |

## GitHub Actions: princípios

- Usar permissões mínimas de `GITHUB_TOKEN` (`contents: read` por padrão).
- Fixar versões verificadas de ações e revisar mudanças em workflows.
- Nunca dar segredos a PRs externos não confiáveis.
- Separar build, teste e deploy; exigir aprovação para ambiente protegido.
- Publicar artefatos de teste sem dados sensíveis.
- Cobrar resultados mínimos, não métricas arbitrárias que gerem hacks.

Este repositório contém um workflow **apenas para validação dos links locais e da estrutura documental** em `.github/workflows/docs-check.yml`. Ele não pretende ser pipeline de um projeto web. Para cada app, criar pipeline alinhado ao seu stack e ambiente.

## Gates por criticidade

| Mudança | Gates extras |
|---|---|
| Texto/UI simples | Lint, screenshot, teclado se afetado |
| Form de cadastro | Teste negativo, validação servidor, E2E |
| Pagamento | Idempotência, webhooks, rollback, testes de duplicidade |
| Auth | Sessão, rate limit, acesso cruzado entre usuários |
| Banco | Backup, reversibilidade, concorrência, plano de dados |
| Infra | Varredura de imagem, secrets, healthcheck, deploy controlado |

## Evidência mínima no PR

```markdown
## Mudança
- Objetivo e escopo
## Testes executados
- comando: resultado e ambiente
## Screenshots / traces
- links internos autorizados
## Segurança e dados
- superfícies afetadas e validações
## Riscos / rollback
- plano se aplicável
## Pendências
- testes não executados e motivo
```

Não basta um relatório dizer “PASS”: o gate deve existir na integração contínua ou fornecer evidência reproduzível.
