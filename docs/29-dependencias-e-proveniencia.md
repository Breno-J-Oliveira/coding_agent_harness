# Supply chain, fontes e atualizações

## O que o instalador garante

- Python 3.11+ é suficiente para a instalação **local/offline** de agentes e skills próprias.
- `catalog/versions.json` registra versões selecionadas do CLI `skills`, do Impeccable e do Playwright CLI em novembro de 2026. As versões podem ficar antigas: atualize só depois de verificar notas oficiais e testes.
- `catalog/skills.json` lista repositórios e nomes das skills externas. A instalação por `npx skills add` usa o estado disponível no repositório de origem **e não fixa seu conteúdo por commit**. Portanto, uma skill pode mudar entre duas instalações.
- Nada executa downloads ou scripts de terceiros sem `--apply` e a respectiva flag.
- Impeccable usa `--no-hooks`; RTK hook necessita opt-in separado.

## Avaliação antes de confiar numa skill externa

1. Consulte repositório original, identidade do mantenedor e licença.
2. Leia `SKILL.md`, scripts auxiliares e dependências **antes** da execução.
3. Confira o histórico de commits, releases, integridade de downloads e código remoto consumido em runtime.
4. Rejeite skills com instruções para ler segredos, desativar proteções, adicionar MCPs desconhecidos ou executar scripts de rede sem motivo.
5. Se precisar de reprodutibilidade estrita, espelhe versões auditadas num repositório interno e fixe commits/SHA-256; use a opção de instalação a partir de fonte local do `skills` CLI.
6. Revise novamente a skill após atualização; a descrição e o corpo podem mudar.

| Componente | Tipo | Origem oficial |
|---|---|---|
| Codex | Agente executor | https://github.com/openai/codex |
| CLI de Agent Skills | Instalador de skills | https://github.com/vercel-labs/skills |
| Impeccable | Design/anti-AI look | https://github.com/pbakaus/impeccable |
| RTK | Compressão de outputs | https://github.com/rtk-ai/rtk |
| Playwright CLI | Testes de navegador | https://github.com/microsoft/playwright-cli |
| Semgrep Skills | Segurança de código | https://github.com/semgrep/skills |
| Trail of Bits Skills | Auditoria avançada | https://github.com/trailofbits/skills |

**Exposição de dados:** não forneça secrets em prompts, prompts de terceiros, logs ou relatórios JSONL; nunca torne pública sua pasta pessoal de backups ou seus arquivos de configuração personalizados.
