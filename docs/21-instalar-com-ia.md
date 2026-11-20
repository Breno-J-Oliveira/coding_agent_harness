# 21 — Instalação do DevKit: humana ou pela própria IA

O DevKit funciona como um repositório-base. Ao abrir no Codex, leia [AGENTS.md](../AGENTS.md), [PROMPT-PARA-IA.md](../PROMPT-PARA-IA.md), [README.md](../README.md). O agente recebe links e um roteiro reproduzível: não é necessário procurar manualmente cada skill.

## Instalar do zero

1. Baixe e extraia este repositório; não é necessário clonar Git.
2. Abra PowerShell (Windows) ou um terminal (macOS/Linux) na pasta extraída.
3. Rode `python scripts/devkit.py doctor` (Windows: `py -3`).
4. Rode `python scripts/devkit.py plan --profile full --with-skills --with-tools --with-design`. **Nenhuma alteração acontece.**
5. Revise fontes em [skills.json](../catalog/skills.json) e [tools.json](../catalog/tools.json).
6. Rode `python scripts/devkit.py install --profile full --apply --with-skills --with-tools --with-design`. Instalação **real** apenas depois da ação explícita.
7. Reinicie o Codex, verifique as skills/agents e execute teste pequeno.
8. Para ativar RTK hook, use a [etapa opcional](23-rtk-e-contexto.md) com prévia e backup.

## Pré-requisitos e soluções

| Dependência | Necessidade | Verificação | Solução |
|---|---|---|---|
| Python 3.11+ | Instalador e validação TOML | `python --version` | [python.org](https://www.python.org/downloads/), no Windows via `winget install -e --id Python.Python.3.13` |
| Codex CLI/Desktop | Executar agentes | `codex --version` (CLI) | [Documentação Codex](https://developers.openai.com/codex) |
| Node.js 22.20+ | `npx skills` (Impeccable usa Node 18.19+) | `node --version` | [nodejs.org](https://nodejs.org/) |
| Git | Busca de skills de repositórios | `git --version` | [git-scm.com](https://git-scm.com/) |
| Internet | Downloads externos | Conexão HTTPS | Proxy, VPN e firewall variam |
| winget ou brew | Instalação opcional de CLI | `winget --version` ou `brew --version` | [winget](https://learn.microsoft.com/windows/package-manager/winget/) / [brew](https://brew.sh/) |

Se uma instalação remota falhar, `doctor` ajuda a localizar binários ausentes. O instalador **não modifica PATH**, não cria contas e não injeta credenciais. Algumas dependências precisam de um novo terminal após instalação. Falhas de um módulo não implicam rollback dos demais: confira o resumo.

## Instalação global ou por projeto

`--scope global`: destino `~/.codex/agents/`, `~/.codex/config.toml`, `~/.codex/AGENTS.md`, `~/.agents/skills/`. Esse modo vale para todos os projetos do mesmo usuário, mas não para outras máquinas automaticamente.

`--scope project --target DIRETORIO`: destino `.codex/agents/`, `.codex/config.toml`, `.agents/skills/` na raiz fornecida. O Codex só carrega configurações locais em **projetos confiáveis**. Mescla um bloco marcado no `AGENTS.md` do projeto com backup, preservando o restante do arquivo.

## Perfis

`core`: requisitos essenciais + skills próprias. `web`: core + frontend/design/SEO. `security`: core + AppSec. `full`: união de todos. O perfil não muda o modelo principal e não significa usar todos os subagentes em toda tarefa.

## Hooks

O instalador usa `--no-hooks` no Impeccable; eventuais hooks podem ser aprovados separadamente depois de revisão. RTK pode instalar um hook de reescrita de comandos. **Ambos devem ser revisados como código executável**, especialmente quando já existem hooks locais. Execute `rtk init -g --codex --dry-run` antes de aplicar. O `--with-rtk-hook` é propositalmente separado da instalação das ferramentas.

## Como verificar sucesso

- `python scripts/validate-package.py`: valida a estrutura do ZIP, **não** a sessão Codex.
- Conte os arquivos `.toml` em `~/.codex/agents/` (ou na pasta do projeto).
- Abra nova sessão Codex, peça lista de roles realmente descobertas e solicite delegação de teste entre `file_scout` e `qa`, sem editar nada.
- Para skills, use `npx skills ls -g` (global) ou `npx skills list` (projeto), e confira comandos da aplicação.
- Para RTK, `rtk --version`, `rtk gain`. Não use a porcentagem de `rtk gain` como economia total da sessão.
- Documente falhas/limitações, especialmente quando o provedor customizado não oferece modelos individuais.

## Voltar atrás

Os backups ficam em `~/.codex/devkit-backups/AAAA...`. Primeiro execute `python scripts/devkit.py uninstall` para prévia e `python scripts/devkit.py uninstall --apply` para remover/restaurar somente arquivos gerenciados sem personalizações. Use `python scripts/devkit.py audit` para verificar modificações antes. Os componentes remotos usam desinstaladores de seus fornecedores (`npx skills remove ...`, `winget uninstall ...`). Veja [Segurança e reversão](24-confianca-e-reversao.md).
