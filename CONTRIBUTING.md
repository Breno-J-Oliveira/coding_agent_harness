# Contribuindo com o VibeCoder DevKit

## Antes de propor uma skill, agente ou CLI

1. Descreva problema real, público, gatilho de uso, custo de contexto, compatibilidade e como medir o ganho.
2. Para fontes externas, inclua repositório oficial, documentação, licença, dependências e risco de scripts executáveis. Evite simplesmente apontar popularidade.
3. Para novos agentes, mantenha as instruções curtas e testáveis, registre o perfil em `catalog/agents.json` e evite duplicar papéis existentes.
4. Para skills locais, crie `.agents/skills/<nome>/SKILL.md` com `name`/`description` no frontmatter e gatilho explícito.
5. Se alterar comandos npm, revise o upstream e ajuste `catalog/versions.json`; atualize exemplos/documentação.
6. Execute validações offline:

```bash
python scripts/validate-package.py
python scripts/check-docs.py
python -m unittest discover -s tests -v
```

7. Toda correção de instalador exige teste em diretório temporário que comprove preservação de arquivos, idempotência e ausência de execução externa no modo plan.

Não inclua API keys, backups, JSONL reais com informações pessoais ou capturas de páginas confidenciais. Veja [SECURITY.md](SECURITY.md).
