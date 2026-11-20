# 34 — Evolução v3: especialização real sem inundar o Codex

## Entregas desta versão

1. Adição de **21 packs específicos**, de engenharia a pagamentos e observabilidade.
2. Adição de **49 skills originais** com escopo, procedimento e critérios de aceite próprios.
3. Curadoria de **55 skills externas distintas**, agrupadas por pack e fornecedor.
4. Instalador `scripts/skillpacks.py` que não altera nada em `plan`.
5. Instalação offline de skills próprias usando diretório compatível com Agent Skills.
6. Instalação remota opt-in via CLI oficial `skills`, com versão controlada no catálogo.
7. Recomendações heurísticas de stack lendo apenas manifests locais.
8. Detecção de React, Next.js, Expo/RN, Nest, Prisma/SQL, Stripe, Sentry e AI SDK.
9. Detecção de PHP Composer, Python, Cloudflare, Docker e CI.
10. Controle de colisões: nunca sobrescrever uma skill de usuário sem permissão.
11. Auditoria SHA-256 e manifesto de propriedade separado do instalador base.
12. Reversão seletiva de skills criadas pelo instalador, preservando as editadas.
13. Filtro/limite de downloads para evitar instalar dezenas de skills sem intenção.
14. Documentação de fontes oficiais e diferenças de instalação de plugins.
15. Atualização de skills Next.js para a fonte oficial atual `vercel/next.js`.
16. Separação de design visual, acessibilidade, SEO, performance e frontend.
17. Skills específicas de autenticação, RLS, webhooks e pagamentos.
18. Skills para teste E2E, contratos, flakiness, regressão visual e WCAG.
19. Skills para Docker, CI/CD, rollback e ambientes Cloudflare.
20. Skills para incidentes, Sentry, trace e postmortem.
21. Skills para supply chain de skills e MCPs, evals e roteamento de modelos.
22. Manual de adoção por projeto com planos, verificação e reversão.
23. Fluxos reais de SaaS, site estático, SEO, backend e operação multiagente.
24. Testes de integração offline para instalador, conflitos e detecção da stack.
25. Política de instalação sob demanda em vez de 49 skills presentes sempre no contexto.

## Limitações declaradas

O script não comprova que cada repositório remoto conserva nomes de skills no futuro; isso depende dos mantenedores. Testes locais **não validam downloads externos, compatibilidade com todas as versões de Codex nem economia de 90% de tokens**. Plugins como Stripe e Sentry requerem instalação e permissões externas específicas, deliberadamente não automatizadas pelo DevKit.
