---
name: api-contract-review
description: Revisar criação ou alteração de API pública e seus consumidores; não usar em ajustes só de interface.
---

# api-contract-review

1. Compare contrato OpenAPI/rotas reais, verbos, formatos, autenticação, paginação, erros e códigos HTTP.
2. Identifique breaking changes e casos de compatibilidade retroativa.
3. Proponha testes de contrato e idempotência, incluindo limites de taxa e casos negativos.
4. Entregue lista priorizada `endpoint: risco: evidência: teste`, sem fingir execução.
5. Nunca consultar endpoints de terceiros sem autorização explícita.
