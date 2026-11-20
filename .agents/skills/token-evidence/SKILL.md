---
name: token-evidence
description: Medir impacto de RTK, agentes e roteamento com logs JSONL Codex; não alegar economia sem comparação.
---

# token-evidence

1. Execute tarefas equivalentes com mesmo escopo, testes e critérios de aceite.
2. Capture `codex exec --json` localmente; use `scripts/token-report.py` para somar usage sem compartilhar o log bruto.
3. Compare input, cached input, output, falhas, latência e qualidade real.
4. Não some cached_input_tokens novamente ao total; já está em input_tokens.
5. Documente regressões, custos e condições. Rejeite afirmação de 90% sem evidência replicável.
