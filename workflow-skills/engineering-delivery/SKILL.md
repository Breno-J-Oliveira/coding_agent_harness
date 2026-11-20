---
name: engineering-delivery
description: Executar ou retomar uma funcionalidade com fatias verificáveis, fila, dependências e evidências de aceite.
---
# Engineering delivery

Parta do resultado pedido e das instruções do projeto. Para cada entrega, registre o resultado observável, os critérios de aceite verificáveis e apenas as dependências que a bloqueiam. Se o pedido começa com uma ideia de produto sem escopo, use `idea-to-release` quando disponível.

Em tarefa pequena, implemente e verifique diretamente. Em trabalho maior, prefira fatias verticais. Acione especialistas para questões independentes de risco ou qualidade e preserve mudanças existentes.

No Coding Agent Harness, consulte `KIT-LOCATION.txt` se presente. Use `scripts/engineering.py` para persistir tarefas. Para retomar, leia a próxima tarefa, suas dependências e o último resultado relevante. Na CLI, `run` encaminha resultados prontos à revisão. Em sessão interativa, registre com `record` e uma evidência local. Só dê aceite depois de conferir os critérios.

Valide no ponto de entrada real da entrega. Registre comandos, status e bloqueios reais. Para `advance`, use somente a verificação independente e previamente aprovada pelo responsável pelo projeto. Publicação, dados reais e custos seguem a autorização da tarefa.
