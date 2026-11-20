# Critérios objetivos de qualidade e entrega

O agente principal não pode transformar o resultado de uma skill em aprovação automática. Cada tipo de alteração exige evidências relevantes:

| Mudança | Evidência mínima | Bloqueia entrega quando |
|---|---|---|
| Frontend | `build`, typecheck/lint, navegação responsiva, teclado e screenshot quando possível | Erro crítico ou fluxo inacessível |
| API e backend | Testes de contrato, autenticação, autorização por objeto, erros e rollback | Dados de outro usuário acessíveis ou contrato quebrado |
| Banco | Migração em base de teste, integridade, backfill, plano de reversão | Perda potencial de dados sem plano aprovado |
| Autenticação / segurança | Threat model, testes de cenário negativo, scanner local e revisão independente | Problema crítico confirmado |
| SEO público | Status HTTP, canonical, sitemap, metadados e verificação de renderização | Indexação comprometida ou canonical inválido |
| Deploy | Variáveis, migrações, observabilidade, healthcheck, rollback e aprovação | Alteração destrutiva sem autorização |
| Economia de tokens | Comparação JSONL real, testes equivalentes e tempo de execução | Otimização reduz qualidade ou dados não comparáveis |

## Contrato compacto de tarefas delegadas

```text
OBJETIVO: <resultado observável>
ESCOPO: <caminhos exatos, sem arquivos compartilhados com outro agente>
CRITÉRIOS DE ACEITE: <testes, observações e limitações>
AUTORIDADE: não alterar produção, segredo, billing ou deploy
RETORNO: conclusão (<= 8 linhas), arquivos, testes reais, riscos, pendências
```

Subagentes não devem simular reuniões ou entregar aprovação institucional fictícia. Devem ser tratados como especialistas de programação, com evidência verificável e supervisão das decisões de alto impacto. Consulte também `docs/10-quality-gates.md` e `docs/16-governanca-autonomia.md`.
