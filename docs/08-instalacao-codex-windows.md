# 08 — Instalação no Windows + Codex (preservando tudo)

## Etapa 0 — Verificar versões

No PowerShell:

```powershell
node --version
npm --version
python --version
git --version
codex --version
```

O CLI `skills` documenta Node.js **22.20+**. Se o Node for anterior, atualize pelo processo oficial antes de executar `npx skills`. O sistema local pode ter regras corporativas e execução de scripts bloqueada; **não mude ExecutionPolicy permanentemente para contorná-las**. Use o terminal permitido ou converse com o administrador.

## Etapa 1 — Fazer backup

```powershell
$codexDir = Join-Path $env:USERPROFILE '.codex'
$backup = Join-Path $env:USERPROFILE ('codex-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Force -Path $backup | Out-Null
Copy-Item (Join-Path $codexDir 'config.toml') $backup -ErrorAction Stop
if (Test-Path (Join-Path $codexDir 'AGENTS.md')) {
    Copy-Item (Join-Path $codexDir 'AGENTS.md') $backup
}
Write-Host "Backup criado em $backup"
```

Preserve `notify`, `model`, quaisquer providers, plugins, MCPs, memórias, projetos e opções específicas do sistema operacional. **Nunca poste seu config real publicamente** se ele contiver caminhos privados ou segredos.

## Etapa 2 — Mesclar multiagentes

Abra `notepad "$env:USERPROFILE\.codex\config.toml"` e **adicione no final** somente se ainda não existir uma seção `[agents]`; se existir, mescle as chaves nela:

```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 3
# Modelo/effort opcionais: ative somente depois de validar o provider.
# default_subagent_model = "modelo-suportado"
# default_subagent_reasoning_effort = "low"
```

As chaves acima constam na [referência oficial do Codex](https://learn.chatgpt.com/docs/config-file/config-reference). Não coloque duas seções `[agents]` no mesmo arquivo. Use [`config-agents.toml`](../templates/config-agents.toml) apenas como referência.

## Etapa 3 — Agentes personalizados

**Instalação reconhecida:** copie TOMLs de agentes confiáveis para `C:\Users\SEU_USUARIO\.codex\agents\`; o Codex também reconhece `.codex/agents/` no projeto. Um arquivo deve conter `name`, `description`, `developer_instructions`. O arquivo não concede permissões extras ao agente.

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\agents" | Out-Null
(Get-ChildItem "$env:USERPROFILE\.codex\agents" -Filter '*.toml' -ErrorAction SilentlyContinue).Count
```

Este repositório já inclui os **22 TOMLs** na pasta [`agents/`](../agents/). Use o script [`install-agents.ps1`](../scripts/install-agents.ps1) para simular e instalar sem sobrescrever arquivos existentes:

```powershell
powershell -NoProfile -File scripts/install-agents.ps1
powershell -NoProfile -File scripts/install-agents.ps1 -Apply
```

Se você já tem perfis de um pacote anterior, compare os arquivos antes de escolher versões. Perfis com o mesmo nome são preservados; não pressupor que foram substituídos.

## Etapa 4 — AGENTS.md enxuto

Abra [`templates/AGENTS.global.md`](../templates/AGENTS.global.md) e copie apenas as regras ainda não existentes para `~/.codex/AGENTS.md`. Regras de projeto pertencem ao `AGENTS.md` do repositório, não ao global. Não substitua instruções locais relevantes.

## Etapa 5 — Skills CLI

```powershell
# Inspecionar capacidade de instalação:
npx skills --help
npx skills add vercel-labs/agent-skills --list

# Selecione um subconjunto:
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --skill web-design-guidelines -a codex -g
npx skills add semgrep/skills --skill code-security -a codex -g
npx skills add coreyhaines31/marketingskills --skill seo-audit --skill schema-markup -a codex -g
npx skills add supabase/agent-skills --skill supabase-postgres-best-practices -a codex -g

# Verificar:
npx skills list -g
npx skills check
```

A flag `-g` instala para o usuário, `-a codex` seleciona o agente e `--skill` evita baixar um catálogo inteiro. Repositórios podem mudar: use `--list` antes e confirme o nome exato da skill.

## Etapa 6 — Design

```powershell
# Preferencialmente por projeto, com revisão antes de instalação:
npx impeccable install --providers=codex --scope=project
npx ui-ux-pro-max-cli init --ai codex --dry-run
npx ui-ux-pro-max-cli init --ai codex

# Opcional — escolha UMA dessas abordagens para análise anti-slop:
npx skills add heydamir/unslop --skill unslop -a codex
# ou
npx skills add Leonxlnx/taste-skill --skill design-taste-frontend -a codex
```

Impeccable pode instalar hooks. Revise scripts e aprove o hook no aplicativo em `/hooks` se necessário. Execuções `npx` podem instalar pacotes em cache: revise fonte e versão antes.

## Etapa 7 — Navegador econômico e testes

```powershell
npm install -g @playwright/cli@latest
playwright-cli --help
playwright-cli install --skills
```

O CLI é uma **ferramenta** com skills; não é obrigação usar o MCP do navegador em paralelo. Defina uma política clara de qual caminho o agente prefere em cada caso.

## Etapa 8 — Skills avançadas opcionais

```powershell
# Trail of Bits: catálogo de plugins, NÃO instale tudo sem revisar:
codex plugin marketplace add trailofbits/skills
codex plugin list
# Depois de confirmar o nome no catálogo:
# codex plugin add differential-review@trailofbits

# Addy Osmani: escolha apenas se usará o fluxo dele:
codex plugin marketplace add addyosmani/agent-skills
# codex plugin add agent-skills@agent-skills
```

Para **Superpowers**, prefira instalação pelo catálogo de plugins do Codex e evite duplicar orquestrações que já existam. Algumas skills usam licença ou dependências próprias; conferir antes.

## Etapa 9 — Verificações não destrutivas

```powershell
python scripts/validate-sample-config.py
powershell -NoProfile -File scripts/check-environment.ps1
```

Se o PowerShell bloquear `.ps1`, execute os comandos de inspeção individualmente em um terminal autorizado, em vez de alterar a política global. Validar sintaxe não comprova descoberta em runtime.

**Teste no Codex:**

> Liste os subagentes realmente descobertos e as skills carregáveis. Faça uma análise do projeto em modo somente leitura com um especialista de arquitetura e um de segurança, simultaneamente se possível. Relate o nome real de cada agente, as ferramentas usadas, o resultado e o que não pôde validar. Não modifique arquivos.

## Problemas comuns

| Sintoma | Diagnóstico |
|---|---|
| Skill não aparece | Checar `npx skills list`, diretório, reiniciar Codex |
| TOML inválido | Verificar `name`, `description`, `developer_instructions`; `tomllib` |
| Comando `npx` falha | Node/npm, proxy, permissões, fonte e versão |
| Agentes disputam arquivos | Reorganizar tarefas ou worktrees, reduzir concorrência |
| Tokens aumentam | Handoff curto, desativar skills redundantes, medir |
| Hook bloqueado | Inspecionar/aprovar em `/hooks` ou desinstalar |
| Provider não aceita modelo | Reverter modelo do subagente, manter o modelo atual |

**Fontes:** [Codex Config Reference](https://learn.chatgpt.com/docs/config-file/config-reference), [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [skills CLI](https://github.com/vercel-labs/skills), [Impeccable](https://github.com/pbakaus/impeccable).
