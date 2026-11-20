# 04 — Segurança: proteção em camadas, sem promessas de “blindagem total”

## Distinção fundamental

Uma **skill** ensina um fluxo ao agente; um **scanner** avalia propriedades do código e gera achados; um **teste de segurança** tenta verificar uma hipótese; um **monitor** observa produção. Nenhum deles garante, isoladamente, que o sistema é seguro.

## Stack recomendado

| Controle | Ferramenta / método | O que cobre | O que NÃO cobre |
|---|---|---|---|
| Diretrizes de secure coding | [Semgrep code-security](https://github.com/semgrep/skills) | Padrões seguros em diversas linguagens | Não executa auditoria por si só |
| SAST | [Semgrep CLI](https://semgrep.dev/docs/) | Padrões inseguros e fluxos reconhecíveis | Falhas lógicas específicas do negócio |
| Auditoria especializada | [Trail of Bits](https://github.com/trailofbits/skills) | `static-analysis`, `differential-review`, `insecure-defaults`, `supply-chain-risk-auditor` | Exige analista/validação |
| Contrato de segurança | [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Requisitos verificáveis de segurança | Implementação automática |
| Dependências | `npm audit`, `pip-audit`, `composer audit`, GitHub Dependabot | CVEs e versões afetadas | Não encontra lógica insegura inédita |
| CI / CodeQL | [GitHub CodeQL](https://codeql.github.com/) | Consultas profundas em linguagens suportadas | Não encontra todos os bugs |
| DAST autorizado | [OWASP ZAP](https://www.zaproxy.org/) | Achados HTTP em aplicação executável | Pode criar efeitos colaterais; isolar ambiente |
| Imagens / infraestrutura | [Trivy](https://github.com/aquasecurity/trivy) | CVEs, config, secrets, SBOM | Falsos positivos e cobertura limitada |
| Secrets | GitHub Secret Scanning, `gitleaks` | Segredos inadvertidos | Não substitui rotação de credenciais |

## Fluxo de auditoria de um site

### 0. Escopo e autorização

Somente sistemas e endpoints para os quais existe autorização de teste. Identificar produção, staging, contas de teste, limites, riscos de dados e janelas permitidas. Evitar scans invasivos em produção sem aprovação explícita.

### 1. Modelagem de ameaças

Inventariar: ativos, usuários, fronteiras de confiança, endpoints, áreas administrativas, upload, pagamentos, APIs externas, integrações e segredos. Responder: quem pode fazer o quê, sobre qual recurso e com qual prova?

### 2. Baseline estático

Executar linters, testes, scanner de dependências, SAST e varredura de segredos. Salvar relatório com versão e comando. Revisar achados antes de corrigir.

### 3. Revisão de autenticação e autorização

- Hash de senha adequado e MFA onde necessário.
- Sessão/cookie (`HttpOnly`, `Secure`, `SameSite`) e proteção CSRF quando aplicável.
- Autorização **no servidor e por recurso**, inclusive APIs e arquivos.
- Testes de IDOR/BOLA: usuário A não acessa dados do usuário B.
- Expiração/revogação de sessão e limites de tentativas.
- RLS com testes de positivo/negativo quando usar Supabase/Postgres.

### 4. Entrada e saída

- Validação no servidor e queries parametrizadas.
- Escape/contextual encoding contra XSS.
- Upload limitado por tamanho/tipo, armazenamento apropriado e antivírus quando cabível.
- `CSP`, `HSTS` e demais headers baseados na arquitetura.
- SSRF, deserialização, path traversal e command injection conforme superfícies reais.

### 5. Infra e supply chain

- Imagens Docker atualizadas e usuário não-root.
- Segredos em cofre/variáveis seguras, fora do código e logs.
- Dependências travadas, versões revisadas, SBOM quando exigido.
- Backup com restauração testada; permissões de banco mínimas.
- Revisão de GitHub Actions, PRs externos e scripts `postinstall`.

### 6. Testes dinâmicos e regressão

Verificar manualmente e com testes automatizados cenários de autorização, quotas, erro, sessão, rate limit, uploads e business logic. DAST só com ambiente e escopo seguros. Cada achado real gera teste de regressão.

### 7. Monitoramento e resposta

Instrumentar logs sem PII/segredos, métricas, alertas, revisão de erros e rollback. Definir quem pode revogar credenciais, desligar uma integração ou reverter release.

## Priorização por evidência

| Severidade | Exemplo | Saída mínima |
|---|---|---|
| Crítico | Usuário comum acessa dados de outro tenant | Repro em staging + bloqueio de release |
| Alto | Endpoint aceita operação sensível sem autorização | Teste reproduzível + correção + regressão |
| Médio | Config fraca com exploração dependente de cenário | Cenário, impacto e correção proporcionais |
| Baixo | Cabeçalho recomendável faltante sem impacto demonstrado | Registro e priorização |
| Informação | Melhoria defensiva geral | Backlog, sem alegar vulnerabilidade |

## “Blindar o site” — prompt seguro

> Audite defensivamente este repositório para entrega profissional. Inspecione autenticação, autorização por recurso, exposição de segredos, validação de entrada, dependências, headers, upload, APIs, RLS, configuração Docker e logging. Execute scanners apenas em ambiente autorizado. Para cada achado: arquivo/linha, condição necessária, impacto, evidência reproduzível, falso positivo possível, correção e teste de regressão. Não faça testes ativos em produção e não afirme segurança total.

## Regras de agentes

- O agente `security` é **revisor independente**; não concede aprovação automática ao próprio código que escreveu.
- Alterações em credenciais, políticas de acesso e produção exigem revisão humana.
- Não criar vulnerabilidades de demonstração, payloads perigosos ou provas de conceito fora do escopo autorizado.
- Nunca colar segredos reais em tickets, PRs ou relatórios de subagentes.

**Fontes:** [Trail of Bits](https://github.com/trailofbits/skills), [Semgrep](https://github.com/semgrep/skills), [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/), [ZAP](https://www.zaproxy.org/).
