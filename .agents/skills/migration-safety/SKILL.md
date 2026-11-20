---
name: migration-safety
description: Planejar alterações de banco de dados e migrações com risco de indisponibilidade; não usar em scripts estáticos.
---

# migration-safety

1. Faça inventário de tabelas, migrações e consumidores afetados.
2. Prefira estratégia expand-migrate-contract e backfill em lotes.
3. Planeje índices, locks, constraints, integridade e compatibilidade de versões.
4. Produza testes para dados de exemplo e rollback ou recuperação de backup.
5. Nunca executar DDL destrutivo em produção sem autorização explícita.
