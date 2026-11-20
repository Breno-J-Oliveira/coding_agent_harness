# Instalar, atualizar, auditar e reverter com segurança

## Fluxo recomendado

1. Execute `python scripts/devkit.py doctor` e confira Python, Node, Git e Codex.
2. Execute `python scripts/devkit.py plan --profile core` ou `--profile full --with-skills --with-tools --with-design` para ver mudanças **sem escrita nem rede**.
3. Para aplicar arquivos locais: `python scripts/devkit.py install --profile core --apply`.
4. Para incluir código remoto de terceiros, inclua explicitamente `--with-skills`, `--with-design` e/ou `--with-tools`; revise cada fornecedor e versão antes.
5. Reinicie Codex e teste descoberta de agentes e skills dentro de um repositório confiável.

## Escopos

- Global: `$CODEX_HOME/agents`, `$CODEX_HOME/config.toml`, `$CODEX_HOME/AGENTS.md`, e `~/.agents/skills`.
- Projeto: `<repo>/.codex/agents`, `<repo>/.codex/config.toml`, `<repo>/AGENTS.md` e `<repo>/.agents/skills`.
- Nunca altere confiança de um repositório automaticamente. Arquivos `.codex/config.toml` específicos de projetos podem exigir que Codex confie no projeto.

## Atualizar o kit (sem apagar preferências)

```bash
python scripts/devkit.py audit
python scripts/devkit.py plan --profile full
python scripts/devkit.py install --profile full --apply
python scripts/devkit.py audit --json
```

O manifesto `devkit-state.json` registra o SHA-256 dos arquivos gerenciados. Um arquivo do usuário que existe antes do primeiro install **não é sobrescrito**; `config.toml` e `AGENTS.md` são exceções controladas: recebem adições mescladas após backup. Se um arquivo gerenciado foi modificado pelo usuário, o instalador o preserva e sinaliza conflito. Essa proteção pode impedir uma atualização até haver reconciliação manual.

## Desinstalação seletiva

```bash
python scripts/devkit.py uninstall
python scripts/devkit.py uninstall --apply
```

O primeiro comando somente mostra o que seria removido/restaurado. O segundo remove os arquivos cujo hash ainda confere com o Dev Kit, e restaura o conteúdo original de configurações/regras quando houver backup verificado. Personalizações do usuário permanecem. O script **não** desinstala Node, Git, CLIs externas, skills externas instaladas pelo `npx skills`, nem desfaz hooks de terceiros: esses componentes possuem seus próprios ciclos de vida.

**RTK hook:** prévia com `rtk init -g --codex --dry-run -v`; para remover o hook, confira `rtk init -g --codex --uninstall` na versão instalada. Fazer cópia do `hooks.json` antes de alterar.

## Segurança e limites

- O `devkit-state.json` é um arquivo local de gestão, **não** fonte de credenciais. Não compartilhe backups nem arquivos `config.toml` com segredos ou hosts privados.
- Locks são exclusivos durante `--apply`. Se houver travamento, verifique se não há outra instalação antes de remover `.devkit-install.lock` manualmente.
- Falhas na instalação remota podem deixar as **etapas locais concluídas**: o resultado informa pendências. Repetir `install` é idempotente para arquivos locais não modificados.
- O instalador valida sintaxe e caminhos locais, mas não executa uma auditoria de segurança das dependências baixadas.
