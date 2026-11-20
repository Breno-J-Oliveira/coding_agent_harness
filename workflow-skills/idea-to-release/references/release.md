# Da validação ao release

1. Execute o build, os testes e as verificações pertinentes no candidato que será entregue. Anote a revisão testada e os requisitos de execução. Revise documentação, configuração obrigatória e nomes de variáveis sem copiar valores secretos.
2. Prepare os passos para instalar ou atualizar, com migrações, verificação de saúde e caminho de recuperação. Para mudanças em dados, confira backup e restauração em ambiente descartável quando puder. Se a mudança for incompatível com rollback, defina como corrigir adiante e quem decide a ação.
3. Confira o escopo da autorização antes de publicar. Se houver um destino autorizado, use o fluxo existente, confirme a versão e execute uma verificação representativa no ambiente. Relate o endereço, o resultado e qualquer alerta real. Quando faltar autorização ou acesso, deixe as instruções e evidências prontas para quem fará a publicação.
4. Entregue os comandos para rodar e validar, resultados observados, dependências externas e pendências. Em serviços operados continuamente, indique onde ver logs sem dados sensíveis, como detectar falhas na jornada e como recuperar o serviço.
