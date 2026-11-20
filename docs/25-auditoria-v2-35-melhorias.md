# Auditoria V2 — 35 melhorias e adições implementadas

Data de revisão: **12 de novembro de 2026**. Base examinada: `VibeCoder_DevKit_Professional_Codex.zip` (v1). A versão V2 mantém o propósito de um **Dev Kit público**, não um perfil pessoal. Uma melhoria **implementada** significa que seu código/arquivo foi incluído no repositório; não implica que a instalação em cada versão do Codex ou o funcionamento de CLIs remotas tenham sido testados.

## Instalador e preservação de dados

| Nº | Melhoria concreta | Implementação/validação |
|---|---|---|
| 01 | Validar `config.toml` **antes** de copiar arquivos | `scripts/devkit.py:check_requirements`; teste de config inválida |
| 02 | Detectar marcadores incompletos no AGENTS antes da escrita | `rendered_rules`; teste de marcador incompleto |
| 03 | Fazer operações de gravação atômicas com arquivo temporário | `atomic_write()` |
| 04 | Reverter alterações locais da etapa interrompida | `ManagedFiles.undo_on_error`; teste de rollback |
| 05 | Trava exclusiva contra instalações simultâneas | `.devkit-install.lock` gerenciado em `session_lock()` |
| 06 | Manifesto de propriedade por SHA-256 dos arquivos do kit | `devkit-state.json` + `ManagedFiles` |
| 07 | Não sobrescrever arquivo existente que não pertence ao kit | `ManagedFiles.put` e teste de conflito |
| 08 | Recusar atualização quando usuário personalizou arquivo gerenciado | validação do SHA atual antes de atualizar |
| 09 | Permitir upgrade seguro de arquivo gerenciado sem personalização | estado anterior + atualização + teste dedicado |
| 10 | Backups do config e das regras anteriores | `devkit-backups/<timestamp>/` |
| 11 | Comando `audit` detecta alterações e perdas | `devkit.py audit [--json]` |
| 12 | Comando `uninstall` com prévia e `--apply` | `devkit.py uninstall`, testes de restauração |
| 13 | Desinstalação preserva arquivos pessoais e customizações | verificação de hash antes de remover |
| 14 | Bloqueio de destino symlink para evitar gravar fora do escopo | `ensure_safe_target`; teste de symlink |
| 15 | Integração do `AGENTS.md` por projeto, não apenas global | `templates/AGENTS.project.md` + instalador |
| 16 | Limite de subagentes personalizável entre 1 e 8 | flag `--max-agents`, mantendo valores existentes |
| 17 | `doctor --json` para automações e diagnóstico não interativo | `doctor --json` + testes |
| 18 | CLIs de terceiros não têm stdout/stderr privados despejados | `invoke()` mostra apenas status e comando |

## Time virtual e economia de contexto

| Nº | Melhoria concreta | Implementação/validação |
|---|---|---|
| 19 | Perfis realmente selecionam subconjuntos de agentes | `catalog/agents.json`: core 14, web 23, security 21, full 28 |
| 20 | Especialista `api_reviewer` para compatibilidade de contratos | `agents/api_reviewer.toml` |
| 21 | Especialista `release_manager` para releases e rollback | `agents/release_manager.toml` |
| 22 | Especialista `threat_modeler` para modelagem de ameaças | `agents/threat_modeler.toml` |
| 23 | Especialista `observability` para SLI/SLO e tracing | `agents/observability.toml` |
| 24 | Especialista `privacy` para minimização de dados | `agents/privacy.toml` |
| 25 | Especialista `dependency_auditor` para supply chain | `agents/dependency_auditor.toml` |
| 26 | Oito skills novas carregadas somente quando relevantes | `.agents/skills/`: onboarding, API, ameaça, dependências, SEO, migração, tokens, incidentes |
| 27 | Roteador offline de tarefas sem custo de LLM | `scripts/route-task.py` (heurística, não agente automático) |
| 28 | Comparador de **usage real** do `codex exec --json` | `scripts/token-report.py`, sem enviar logs a serviços |
| 29 | Métricas separam input, cached input, output e falhas | comparador reconhece JSONL `turn.completed` |
| 30 | Economia só é validada quando ambos os resultados passaram QA | flags `--baseline-pass`/`--optimized-pass` e guia de benchmark |

## Dependências, governança e documentação

| Nº | Melhoria concreta | Implementação/validação |
|---|---|---|
| 31 | Fixar versões consultadas de CLIs npm, evitando `@latest` como padrão | `catalog/versions.json`, `@playwright/cli@0.1.21`, `skills@1.8.1`, `impeccable@4.8.2` |
| 32 | Impeccable instalado **sem hooks** por padrão | `--with-design` e `--no-hooks`; aprovação separada para hooks |
| 33 | RTK continua módulo explícito com prévia e backup | `--with-rtk-hook`; nenhum hook silencioso |
| 34 | Validar catálogos, papéis, SKILL.md e links Markdown sem rede | `scripts/validate-package.py`, `scripts/check-docs.py` |
| 35 | Ampliar testes de instalação, reversão, roteamento e telemetria | `tests/test_installer.py`, `tests/test_tooling.py`, CI multiplataforma |

## Problemas que **não** podem ser resolvidos só por repositório

- Trocar automaticamente o modelo **a cada leitura de arquivo** exigiria um roteador de execução/proxy integrado e suporte do provedor. Aqui o modelo leve é aplicado por perfil de subagente apenas se configurado e suportado; `route-task.py` fornece sugestão, não interceptação.
- O RTK pode reduzir drasticamente a **saída de comandos**, mas não garante 90% menos tokens totais. Cada contexto, cache, modelo e validação altera o resultado.
- Ferramentas externas podem alterar comportamento ou ser removidas. O kit não verifica sua integridade remotamente em cada instalação. A V2 fixa **alguns comandos npm**, mas as skills GitHub ainda não estão pinadas por commit.
- **Segurança absoluta e conformidade regulatória não podem ser prometidas.** São necessárias revisões humanas, testes no sistema real e procedimentos de produção.
- E2E com Codex Desktop, Windows, macOS e Linux, instalaçāo remota de todas as skills e execução de RTK real precisam ser realizados nos ambientes finais. Os testes offline não substituem esse aceite.

**Fontes:** [Subagentes Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Skills Codex](https://learn.chatgpt.com/docs/build-skills), [Configuração Codex](https://learn.chatgpt.com/docs/config-file/config-reference), [Codex exec JSONL](https://learn.chatgpt.com/docs/non-interactive-mode), [CLI de skills](https://github.com/vercel-labs/skills), [RTK](https://github.com/rtk-ai/rtk).
