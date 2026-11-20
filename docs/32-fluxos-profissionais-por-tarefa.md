# 32 — Fluxos profissionais com skills específicas

## 1. Design premium e remoção de aparência genérica de IA

Packs: `design frontend accessibility performance`. Skill própria `ai-ui-pattern-audit` define critérios; `design-token-system` cria escalas e tokens; `visual-regression` exige evidência de antes/depois. A Vercel oferece `web-design-guidelines`; UI/UX Pro Max ajuda na direção visual; **Impeccable** ou **Unslop** são alternativas opcionais. Não instale ambos automaticamente. Verifique uso legítimo de imagens, fontes e licenças.

**Aceite:** hierarquia clara, espaçamento consistente, estados loading/error/empty, contraste adequado, teclado funcional, responsividade e testes visuais em 360px/768px/1440px.

## 2. SaaS com autenticação, banco e pagamentos

Packs: `frontend backend-node database payments security qa-testing`. Defina recursos, papéis e tenants; use `authz-matrix` para testes de acesso; `webhook-idempotency` para callbacks; `rls-policy-verification` para banco; `payment-flow-acceptance` para ciclo de assinatura. Se usar Stripe, o plugin oficial Codex é preferível à cópia desatualizada de skills: https://github.com/stripe/ai.

**Aceite:** testes de autenticação negativa, isolamento por tenant, falhas e duplicatas de webhook, controle de assinatura após cancelamento; API não retorna segredos.

## 3. SEO profissional e Core Web Vitals

Packs: `seo performance accessibility`. `technical-seo-check` checa indexação e canonicals; `schema-jsonld-qa` verifica dados reais; `search-intent-mapping` previne conteúdo duplicado. Use `core-web-vitals` da Addy Osmani para medir LCP/INP/CLS, com dados de campo quando disponíveis. Nenhuma nota Lighthouse garante posicionamento no Google.

**Aceite:** sitemap acessível, robots/noindex intencional, canonical correto, dados estruturados válidos, páginas importantes renderizadas e baseline medido.

## 4. Incidente ou vulnerabilidade

Packs: `security observability qa-testing`. Primeiro identifique impacto e escopo autorizado; evite testes invasivos fora de ambientes próprios. Combine secret scanning, SAST, revisão de autorização, patch com regressão e monitoramento. Nunca diga que o site está 100% blindado.

**Aceite:** cada achado tem prova (ou incerteza), severidade, correção, teste e risco residual. Logs não contêm credenciais.

## 5. Código legado PHP ou Python

Packs: `backend-php backend-python database qa-testing engineering` conforme stack real. Para PHP, mantenha PDO parametrizado, sessões seguras e CSRF; para Python, tipo estático, deps travadas, teste e lint. Não adicione frameworks somente para usar uma skill.

## 6. Deploy Cloudflare ou Vercel

Packs: `devops cloudflare observability security`. Ative a integração do provedor somente se o projeto realmente usar a plataforma. Confirme limites de Workers, bindings e ambiente. Plano de rollback não restaura automaticamente dados de banco.

## 7. Multiagentes e economia de tokens

Packs: `agent-ops engineering`. Use uma ferramenta local para arquivo ou busca; `file_scout` de modelo mais leve quando delegação compensar; modelo forte para alterações críticas. Defina limites de consumo por tarefa e compare `scripts/token-report.py` em benchmarks equivalentes. RTK comprime a saída de comandos e não os tokens de raciocínio ou de histórico da sessão.

## 8. RAG e sistemas com modelos

Packs: `ai-apps backend-node database agent-ops security`. Separe respostas sem fonte de respostas com evidência, teste prompt injection, documento fora de domínio, isolamento de usuários e atualização do índice. Use evals e métricas, não somente feedback subjetivo.

## Indicadores mínimos de qualidade

| Tipo | Indicador | Condição de conclusão |
|---|---|---|
| Código | Testes/lint/build | Comandos executados e resultados documentados |
| Web | Lighthouse/CWV | Baseline e comparação nas mesmas condições |
| Segurança | SAST/secret scan/IDOR | Não há críticas conhecidas sem tratamento |
| UX | Teclado/responsividade/erros | Jornadas testadas, inclusive estados extremos |
| Agentes | Custo, latência, acerto | A/B com prompt e tarefa equivalentes |
| Instalação | Hash, autoria, compatibilidade | Logs e inventário sem segredos |
