# Coding Agent Harness

Este repositório mantém um ambiente local de engenharia de software com agentes para Codex e Claude Code.

- Comece pelo trecho do `README.md` que cobre o pedido. Leia só os scripts, skills, manifests e testes afetados. Abra um catálogo apenas para decisões que dependem dele.
- Para instalação por projeto, revise `python scripts/bootstrap.py --target CAMINHO --engine codex|claude|both`. Aplique com `--apply` quando autorizado. Para manutenção da base antiga, o manual em `docs/36-engineering-os.md` cobre `devkit.py plan` e `audit`.
- Preserve arquivos e configurações existentes. Downloads, hooks, produção, mudanças destrutivas, credenciais e custos exigem autorização conforme o escopo da tarefa. Evite expor conteúdo de logs locais ou dados de clientes.
- Preserve os contratos da fila anterior. Execute testes direcionados e `python scripts/check-docs.py` ao mudar documentação. Rode a suíte local antes de publicar um conjunto de mudanças.
- Registre testes e limitações de descoberta ou execução. Para afirmar economia de tokens, compare entregas equivalentes com a mesma qualidade e registre as métricas do executor.
