---
name: webhook-idempotency
description: "Webhooks com verificação e idempotência. Acione quando: Integrar pagamentos e callbacks."
---

# Webhooks com verificação e idempotência

## Quando ativar
Integrar pagamentos e callbacks. Carregue esta skill apenas quando a tarefa corresponder ao objetivo. Não executá-la automaticamente em tarefas não relacionadas.

## Procedimento
1. **Contexto mínimo.** Determine objetivo, arquivos relevantes, stack e critérios de aceite. Use `rg --files`, `rg -n` e leitura de trechos; não despeje árvores completas ou logs grandes no prompt.
2. **Plano de mudança.** Validar assinatura no corpo bruto, replay window, deduplicação por event-id, transação e fila; separar confirmação de entrega. Relacione riscos e dependências; prefira alterações pequenas, reversíveis e compatíveis com o repositório.
3. **Implementação restrita.** Faça somente as alterações solicitadas e autorizadas. Preserve funcionalidades existentes e não edite configurações sensíveis sem revisão. Consulte a documentação oficial da versão instalada antes de recomendar APIs.
4. **Validação.** Testar duplicata, fora de ordem e falha de persistência; nunca expor segredo. Aplique ferramentas automatizadas se disponíveis, mas diferencie análise estática de evidência de execução.
5. **Handoff.** Entregue um resumo com arquivos modificados, comandos de verificação, resultado e riscos residuais. Não declare uma validação não executada.

## Economia e segurança
- Antes de abrir um agente especializado, compare o custo de um comando local com o custo de uma delegação; evite paralelismo para trabalho trivial.
- Limite saída de comandos, conte linhas em vez de imprimir logs extensos e filtre segredos/PII.
- Não utilizar dados de produção, exploração de terceiros ou operações irreversíveis sem autorização explícita.
- Caso uma ferramenta dependa de credenciais, solicite conexão segura; nunca cole tokens em prompts, código ou documentação.

## Documentação e referências verificáveis
- https://docs.nestjs.com/
- https://nodejs.org/en/learn

> As referências são fontes para consulta conforme a versão instalada. Instalações externas não são distribuídas dentro deste kit; verifique origem e código antes de executá-las.

## Pronto quando
- A implementação ou relatório atende aos critérios de aceite.
- Há evidências verificáveis do que funcionou, e os itens não testados estão claramente assinalados.
- Riscos e próximos passos são proporcionais, sem burocracia desnecessária.
