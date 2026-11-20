# Roteamento de tarefas e modelos — operação realista

`python scripts/route-task.py "Criar autenticação, API e telas de login" --json` gera **uma sugestão offline**, sem chamada a IA. É uma heurística para ajudar o orquestrador a não delegar tudo. O roteador não intercepta requisições ao Codex e não troca automaticamente o modelo de todo comando executado.

## Políticas sugeridas

| Tipo de tarefa | Decisão | Segurança de custo/qualidade |
|---|---|---|
| Ler função, localizar arquivo, buscar símbolo | Principal + `rg` / `smart-read.py`; se necessário `file_scout` leve | Evite invocar outro modelo para uma leitura de 10 linhas |
| Alteração pontual em componente | Principal ou `frontend` | Não precisa abrir comitê virtual |
| Implementação entre API, interface e banco | Principal + no máximo 2–3 especialistas independentes | Separar arquivos e critérios de aceite |
| Segurança, auth, pagamento, deploy, migração | Especialista + revisão e testes reais | Modelo robusto e confirmação humana para riscos |
| SEO/UI | Skills e auditoria de navegador apenas quando o site existe | Não invente scores ou screenshots |

## Perfil de modelos do Codex

```bash
python scripts/build-model-profile.py --cheap-model ID_CONFIRMANDO_DO_PROVEDOR --strong-model ID_FORTE_DO_PROVEDOR
```

Esse script **gera arquivos em pasta nova**. Não altera `~/.codex`. Depois de testar IDs e limites suportados no provedor atual, copie apenas agentes desejados para a pasta global/projeto e compare respostas com testes. O provedor principal, política de aprovação, sandbox e MCPs não devem ser trocados sem autorização.

### Por que não instalar um proxy de roteamento secreto?

Proxies de modelo podem reduzir custo, mas adicionam acesso a credenciais, dependência de rede, governança de dados e possibilidade de degradação de qualidade. Este Dev Kit prefere roteamento explícito por função via TOML compatível com Codex. A troca automática a cada `cat`/`rg` não existe: **ler arquivo é operação de ferramenta, não uma chamada independente de modelo**. Para reduzir tokens desse passo, minimize a saída com RTK, `rg` e leitura limitada.

Fontes: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex config reference](https://learn.chatgpt.com/docs/config-file/config-reference).
