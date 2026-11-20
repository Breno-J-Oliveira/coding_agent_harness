# 24 — Segurança, confiança e reversão

## Política de segurança do DevKit

Este projeto instala **configuração**, **instruções** e, opcionalmente, **programas externos**. Skills e plugins de terceiros podem conter scripts e links não confiáveis. Não se deve tratar o conteúdo de uma skill como autorização para abrir credenciais, remover verificações ou alterar produção.

## Mapa de riscos

| Mudança | Risco | Controle |
|---|---|---|
| Adicionar até 28 agentes TOML | Contexto extra e papéis mal escolhidos | Arquivos locais curtos, seleção por tarefa, validação |
| Mesclar `config.toml` | Corrupção de sintaxe ou quebra de runtime | Parser TOML, backup e operação atômica |
| Acrescentar `AGENTS.md` | Instrução conflitante | Bloco identificado, backup, aviso sobre override |
| Instalar skills via `npx` | Supply chain e scripts remotos | Catálogo de fontes, `--apply`, revisão manual, isolamento |
| Instalar CLIs via gerenciador | Executáveis com privilégios | Comandos explícitos e fornecedor documentado |
| Integrar RTK / design hooks | Interceptação de ferramentas | Prévia, backup de hooks, autorização separada |
| Alterar modelo de subagente | Custos/erros de compatibilidade | Gerar sem aplicar; teste individual antes da adoção |

## Checklist antes de usar em produção

- [ ] A origem de cada instalação é a correta; versão e licença aceitáveis.
- [ ] Nenhuma skill pede desativar aprovação, sandbox, firewalls ou scanners sem justificativa.
- [ ] Não há API keys, senhas nem credenciais em logs/prompt/commits.
- [ ] Testes de autenticação e autorização ocorreram em ambiente autorizado.
- [ ] Existe rollback para schema, release e infraestrutura.
- [ ] Nenhum deploy externo aconteceu sem autorização.
- [ ] Logs, relatórios e dashboards não afirmam testes que não foram executados.

## Reversão segura

1. Pare sessões Codex em curso e salve alterações em projeto real.
2. Inspecione os arquivos adicionados no destino global/projeto e compare com o backup em `devkit-backups/`.
3. Restaure **somente** as configurações alteradas pelo DevKit, sem apagar mudanças recentes de outros sistemas.
4. Para hooks RTK, use o desinstalador documentado (`rtk init -g --codex --uninstall`, se suportado na versão) **após confirmar a prévia** e confira se os outros hooks continuam ativos.
5. Para skills, use `npx skills list` e `npx skills remove NOME`; ferramentas externas usam seus respectivos gerenciadores de pacotes.
6. Reinicie o Codex e valide a configuração. Não apague `~/.codex/` inteiro.

## Dependências e versões

O catálogo é um inventário consultado em 12/11/2026, **não um lockfile criptográfico**. Instalação com `npx ...@latest` tem risco de mudanças posteriores. Para adoção em empresas, fixe versões/commits, valide checksums quando publicados, execute scripts em sandbox e audite artefatos de origem antes de permitir instalação global.

Referências: [Codex: configuração](https://learn.chatgpt.com/docs/config-file/config-reference), [Codex: subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Skills CLI](https://github.com/vercel-labs/skills), [RTK](https://github.com/rtk-ai/rtk).
