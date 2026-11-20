# Changelog

## 4.1.0

- Bootstrap por projeto para Codex e Claude Code, com quatro skills e prévia por padrão.
- Fluxo `idea-to-release` com referências de implementação e release carregadas por fase.
- Fila com `start` para preparar o MVP, `brief` para execução interativa e `usage` para acompanhar consumo.
- Lotes limitados com `advance`, aceite automático opcional via verificador independente e revisão humana nas fases críticas.

## 4.0.0 — 2026-11-20

- Nome de produto VibeCoder Engineering OS e guia do fluxo de produto à operação.
- Fila persistente de entregas com dependências, retomada, registro do Desktop, evidência e aceite.
- Detecção de stack em monorepos e mais linguagens no roteador de packs.
- Triagem de skills com Cisco AI Defense Skill Scanner, revisão humana, hashes e fontes fixadas.
- Dois workflows próprios e duas skills de terceiros revistas e empacotadas.

## 3.0.0 — 2026-11-12

- **21 packs**, **49 skills locais especializadas**, **55 skills externas catalogadas**, sob demanda.
- `skillpacks.py`: `list`, `recommend`, `plan`, `install`, `audit`, `uninstall`, `validate`; instalação sem sobrescrita e reversão conservadora.
- Módulos de design, SEO, frontend, Next.js, segurança, QA, SQL, pagamentos, cloud, mobile e agentes.
- Integração com documentação de fornecedores, exemplos e testes offline; veja `docs/34-evolucao-v3.md`.

## 2.0.0 — 2026-11-12

- Auditoria e implementação de **35 melhorias** detalhadas em `docs/25-auditoria-v2-35-melhorias.md`.
- Instalador com preflight, manifesto de propriedade SHA-256, gravação atômica, backups, atualização não destrutiva, auditoria e desinstalação seletiva.
- Perfis reduzidos por especialidade (14/23/21/28 agentes) e **6 agentes novos**: contratos, release, threat model, observabilidade, privacidade e dependências.
- **8 skills próprias novas**, totalizando 12, todas em `.agents/skills`.
- Roteador de tarefas local sem LLM e comparador de tokens reais `codex exec --json`.
- Fixação inicial de versões npm verificadas em `catalog/versions.json`; ferramentas remotas ainda não fixadas por commit.
- Impeccable como módulo separado e sem hooks por padrão; integração do RTK continua opt-in.
- Documentação de governança, adoção, experimentos, reversão e segurança; CI de validação offline em múltiplos sistemas.

## 1.0.0 — 2026-11-12

- Primeiro kit portátil: 22 agentes, 4 skills próprias, catálogo de ferramentas, plan/install e documentação para Codex.
- Integração opcional com RTK e gerador de modelos por papel.
