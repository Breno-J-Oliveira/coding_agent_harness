# 33 — Instalação por projeto: Windows, macOS e Linux

> Requer **Python 3.11+** para `skillpacks.py`. Instalação de skills remotas requer Git, Node.js 22.20+ e npx. Requer Codex para usar os skills no agente.

## Comandos para usar na pasta extraída do ZIP

```powershell
# 1 — Auditar conteúdo do kit e visualizar catálogo (não altera sistema)
python scripts/skillpacks.py validate
python scripts/skillpacks.py list

# 2 — Detectar stack e preparar a instalação no repositório de trabalho
python scripts/skillpacks.py recommend --target "C:\caminho\projeto"
python scripts/skillpacks.py plan --auto --target "C:\caminho\projeto" --with-external

# 3 — Instalação SOMENTE de skills próprias (sem rede)
python scripts/skillpacks.py install --auto --target "C:\caminho\projeto" --apply

# 4 — Exemplo de instalação remota, sujeita a aprovação explícita
python scripts/skillpacks.py install --packs frontend nextjs design --scope project --target "C:\caminho\projeto" --with-external --apply

# 5 — Auditar e reverter skills próprias sem apagar alterações do usuário
python scripts/skillpacks.py audit --target "C:\caminho\projeto"
python scripts/skillpacks.py uninstall --target "C:\caminho\projeto"   # prévia
python scripts/skillpacks.py uninstall --target "C:\caminho\projeto" --apply
```

Nos sistemas Unix, troque os caminhos Windows por `/caminho/projeto`. Para skills globais, use `--scope global`, sabendo que o Codex pode expor essas skills em qualquer projeto.

**Instalação das externas:** o DevKit chama `npx skills@VERSAO add REPO --skill NOME -a codex --copy` e não faz o download sem `--with-external --apply`. Um limite de 16 skills remotas por execução evita instalação em massa acidental; revise o plano antes de usar `--allow-large`. A seleção é feita por **pack**, não por popularidade de stars. Mesmo fontes reconhecidas podem distribuir scripts com riscos.

**Pré-requisitos:** `node --version`, `npx --version`, `git --version`, `python --version` ou `py -3 --version` (Windows). A ausência de ferramentas bloqueia o download, não a instalação local.

**Externo não é gerenciado pelo nosso manifesto:** para listar e atualizar skills remotas utilize `npx skills list`, `npx skills check`, `npx skills update`; para remover, `npx skills remove <skill>`. As skills locais usam `skillpacks-state.json` com SHA-256 e desinstalação preservadora.

## Plugins opcionais (não instalados automaticamente)

| Caso | Fonte e instalação oficial | Observação |
|---|---|---|
| Pagamentos Stripe | https://github.com/stripe/ai — `codex plugin add stripe@openai-curated` | Exige permissões e ambiente adequado |
| Observabilidade Sentry | https://github.com/getsentry/plugin-codex — `codex plugin marketplace add getsentry/plugin-codex` e `codex plugin add sentry@sentry-plugin-marketplace` | MCP pode exigir conexão/autorização |
| Cloudflare | https://github.com/cloudflare/skills — `codex plugin marketplace add cloudflare/skills` e `codex plugin add cloudflare@cloudflare` | Melhor para projetos Cloudflare |
| Testes Playwright | https://github.com/microsoft/playwright-cli — `playwright-cli install --skills=agents` | CLI precisa estar instalada |
| Design Impeccable | https://github.com/pbakaus/impeccable — consultar comando oficial `npx impeccable install` | Auditoria da versão e hooks antes de executar |
| Unslop | https://github.com/heydamir/unslop | Alternativa, não instalar junto ao Impeccable sem motivo |

## Critérios de segurança

- Não é obrigatório usar integração externa. As 49 skills originais são executáveis como instruções locais mesmo offline.
- Não insira chaves de API em `config.toml`, prompt ou URLs; mantenha secrets em armazenamento seguro.
- Evite executar comandos desconhecidos com privilégios elevados, principalmente instalações via npm.
- Não habilite hooks externos silenciosamente. Quando eles já existirem, faça backup e compare o diff.
- O kit não certifica nem garante a segurança de terceiros; monitore mudanças nos fornecedores.
