# Roteiro de implementação

Selecione as verificações que correspondem ao produto. Uma fatia de site estático pode terminar no navegador. Uma fatia de SaaS costuma atravessar interface, API e persistência. Em CLI, API ou integração, defina a entrada pública e o resultado verificável.

| Área | Decisão ou entrega | Evidência esperada |
| --- | --- | --- |
| Produto | Escolher uma jornada, um usuário e o comportamento que prova valor. | Critérios de aceite observáveis para sucesso e falha. |
| UX e design | Mapear navegação, hierarquia e estados de carregamento, vazio, erro e sucesso. | Jornada conferida em telas relevantes, com teclado e foco para interfaces web. |
| Arquitetura | Reaproveitar a stack existente. Em projeto novo, justificar a escolha em função da jornada e da operação. | Contrato entre componentes e instrução de execução local. |
| Frontend | Conectar a interface à operação real e sinalizar o resultado ao usuário. | Fluxo executado no navegador ou dispositivo suportado. |
| Backend | Validar entradas, autorização e limites do domínio. Definir comportamento para repetição quando houver efeitos colaterais. | Verificação de contrato e teste de integração com entradas válidas, inválidas e sem permissão conforme o risco. |
| Dados | Definir invariantes, migrações, transações e dados de teste quando houver persistência. | Instalação limpa ou atualização de fixture representativa, conforme o caso. |
| Segurança e privacidade | Identificar dados sensíveis e fronteiras de confiança. Atribuir acesso mínimo e usar dados fictícios na verificação. | Testes defensivos de autorização, isolamento e configuração proporcionalmente à mudança. |
| QA | Cobrir a jornada e as regressões mais prováveis. | Comando, status e critérios verificados, com indicação de dependências de ambiente. |

Exemplo de fatia para um sistema de agendamento: criar um horário pela interface, confirmar a gravação e verificar que outra conta recebe uma recusa ao tentar acessá-lo. Um relatório avançado pode ficar para uma etapa seguinte.
