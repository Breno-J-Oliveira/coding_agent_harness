---
name: idea-to-release
description: Transforme uma ideia de software em MVP implementado, verificado e pronto para entrega. Use para projetos novos ou pedidos que abrangem da ideia até a publicação.
---
# Da ideia à entrega

1. Identifique o usuário, o problema, a jornada que prova valor e como observá-la funcionando. Em um projeto existente, leia as instruções locais, os manifests e as verificações afetadas. Em um projeto novo, escolha a menor stack que atende à jornada e ao ambiente disponível. Registre premissas reversíveis e siga. Peça uma decisão quando respostas diferentes mudarem materialmente o produto ou o risco.
2. Defina a primeira entrega em poucas linhas com o resultado observável, os critérios de aceite, as dependências e o que fica para depois. Prefira uma fatia vertical que funcione do ponto de entrada à persistência, quando ela existir.
3. Implemente e verifique cada fatia antes de avançar. Leia o [roteiro de implementação](references/implementation.md) ao definir ou construir a jornada. Use os comandos do projeto e registre o resultado observado.
4. Prepare a entrega com [critérios de release](references/release.md). Publique em produção apenas com autorização para o ambiente e a ação. Se a publicação depender de acesso, custo ou decisão externa, avance toda a preparação local e indique o bloqueio específico.

Use a fila do harness quando disponível para registrar dependências e evidências. Em sessões interativas, mantenha um registro curto com a meta, a próxima tarefa e as verificações executadas. Ao retomar, leia o estado e o diff relevante. Ative um especialista somente quando a tarefa trouxer uma questão independente que justifique a revisão.

Entregue o que funciona, como executar, quais verificações passaram, onde está a documentação e o que ainda bloqueia a publicação.
