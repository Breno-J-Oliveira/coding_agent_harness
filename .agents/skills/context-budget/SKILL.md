---
name: context-budget
description: Reduza contexto em tarefas com leituras repetidas, logs longos, delegação ou necessidade de medir uso de tokens.
---
# Economia de contexto

1. Comece pelo aceite e pelo ponto de entrada afetado. Use `rg`, `git diff --stat` e trechos direcionados. Releia uma fonte já inspecionada quando o conteúdo tiver mudado ou houver dúvida concreta.
2. Use a skill mais específica que resolve a etapa. Leia referências sob demanda. Execute verificações focadas, preserve a saída completa em arquivo local quando útil e traga para o contexto o status e as linhas que explicam a falha.
3. Use o agente principal para mudanças localizadas. Delegue somente verificações independentes cujo ganho justifique o contexto extra. Especifique arquivos, pergunta e formato curto com evidência.
4. Ao retomar, consulte a fila ou um resumo curto com meta, revisão atual, arquivos afetados, próximos passos e comandos já verificados. Em tarefa simples, mantenha o contexto na sessão.
5. Compare tarefas equivalentes com o mesmo critério de aceite. Registre tokens de entrada, em cache e de saída quando disponíveis, tempo, tentativas e intervenções. Meça o consumo por entrega aceita.

Se RTK estiver disponível, use-o para compactar saídas destinadas à leitura humana. Preserve a saída bruta quando o próximo comando consumir JSON ou quando o detalhe for necessário para o diagnóstico.
