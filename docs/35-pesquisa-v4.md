# VibeCoder Engineering OS — pesquisa e decisões para a v4

Pesquisa consultada em 20/11/2026. As escolhas e experimentos deste arquivo descrevem a proposta de evolução. Os resultados da implementação e dos testes ficam no relatório da versão.

## Nome e categoria

**VibeCoder Engineering OS** é o nome de trabalho recomendado. A categoria é **ambiente de engenharia de software com agentes**. Em inglês, *agentic engineering harness* descreve a camada que fornece contexto, ferramentas, limites, execução e evidências ao agente.

“DevKit” funciona como nome do pacote instalável. “Engineering OS” comunica o conjunto maior de processos, papéis, estado de trabalho, critérios de aceite e operação. O produto continua independente da stack do aplicativo. Uma equipe pode adotá-lo em React, Laravel, Python ou outra plataforma sem migrar o projeto. A escolha de nome é editorial. A disponibilidade de marca e o registro de domínios ficam fora desta pesquisa.

## O que vale trazer de cada referência

| Referência | Prática observada | Adaptação proposta | Custo ou limite |
| --- | --- | --- | --- |
| **Superpowers, de Jesse Vincent e equipe** | Planejamento por tarefas verificáveis, implementação no mesmo contexto ou com agentes novos, revisão contra escopo e qualidade. | Executar mudanças simples diretamente. Isolar trabalho quando houver edição paralela ou necessidade de uma revisão independente. | Um agente novo por tarefa repete contexto. Ativar o fluxo completo em uma edição pequena aumenta a latência. [Fluxo original](https://github.com/obra/superpowers#the-basic-workflow) |
| **GitHub Spec Kit** | Especificação, plano, decomposição, implementação e revisão de convergência. O tratamento de bugs dispõe de fluxo próprio. | Vincular cada tarefa a um resultado observável e a uma verificação. Em bugs, reproduzir primeiro, corrigir e provar a regressão. | Especificações e código podem divergir. Revisar somente os artefatos que governam a mudança. [Spec Kit](https://github.com/github/spec-kit#spec-driven-development) |
| **BMad Method** | Ciclo de esclarecer, planejar, construir e verificar, e aprender. O ticket conserva requisitos, limites, dependências e referências. O tamanho da mudança determina o ponto de entrada. | Usar a fila como ponto de passagem entre produto, engenharia e QA. Tarefas dependem de resultados confirmados e retomam do próprio estado. | Planejamento por iniciativa, épico e história agrega valor quando existem múltiplas entregas e decisões compartilhadas. [Como o BMad funciona](https://docs.bmad-method.org/start/how-bmad-works/) · [Ciclos de execução](https://docs.bmad-method.org/build/autonomous-development-loops/) |
| **Agent Skills, de Addy Osmani** | Skills por etapa do ciclo de engenharia. A regra de qualidade explícita ajuda a identificar supressões, testes ignorados e limites reduzidos. | Aproveitar revisão multidimensional, critérios de qualidade e observabilidade por demanda. Para cada bloqueio, registrar o requisito vigente e a evidência afetada. | A coleção completa se sobrepõe ao catálogo já existente. Avaliar skills selecionadas e manter a origem fixada a um commit. [Repositório original](https://github.com/addyosmani/agent-skills) |
| **Anthropic, harnesses de longa duração** | Lista de funcionalidades com estado estruturado, progresso persistente e retomada pelo histórico. Um experimento posterior separou planejamento, execução e avaliação. | Guardar a próxima tarefa, tentativas e verificações fora da conversa. Para uma jornada de maior risco, permitir que QA use critérios fixados antes da implementação e exercite o aplicativo em funcionamento. | O artigo posterior relata custo e tempo adicionais de várias rodadas. Medir se a revisão nova encontra problemas suficientes para justificar a repetição. [Retomada entre sessões](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) · [Planejador, executor e avaliador](https://www.anthropic.com/research/harness-design-long-running-apps) |
| **OpenAI, Harness Engineering** | Instruções do repositório funcionam como mapa. Documentação versionada, testes, logs e ferramentas tornam a aplicação inspecionável por agentes. | Manter um ponto de entrada curto. Registrar comandos validados, contratos, cenários de erro e decisões perto do código que os usa. | Uma base de conhecimento extensa exige manutenção. Começar pelos três ou quatro documentos que as tarefas realmente reutilizam. [Harness Engineering](https://openai.com/index/harness-engineering/) |
| **Cisco AI Defense Skill Scanner** | Examina pacotes de skills e relata sinais como instruções ocultas, coleta de dados, código suspeito e dependências problemáticas. Oferece análises locais e opções adicionais de análise. | Examinar uma skill antes de colocá-la nas pastas descobertas pelo agente. Guardar origem, commit, licença, hash, executáveis, achados e decisão. | A análise estática produz falsos positivos e tem cobertura limitada. Um resultado sem achados ainda exige julgamento sobre código, alcance e permissões. [Documentação do Skill Scanner](https://cisco-ai-defense.github.io/docs/skill-scanner) |

## Como o ambiente assume o trabalho

1. **Entrada.** Defina a entrega, o público, os limites e a evidência que provará o resultado. Em projeto existente, identifique os comandos e a arquitetura a partir dos arquivos reais. Em projeto novo, descreva poucas jornadas essenciais e somente as tecnologias necessárias para executá-las.
2. **Planejamento.** Cada tarefa registra objetivo, dependências, caminhos prováveis, critérios de aceite e verificação. O plano pode conter uma só tarefa. Mudanças com API, dados e interface devem ser divididas por comportamento entregável, incluindo o tratamento de falhas.
3. **Execução.** Escolha uma tarefa pronta, trabalhe em um escopo local e registre o que aconteceu. Se houver falha recuperável, trate a causa antes de repetir. O progresso deve sobreviver ao fim da sessão.
4. **Verificação.** Compare a entrega aos critérios originais. Testes, browser, CLI e verificações de contrato entram conforme o tipo de projeto. Cada resultado precisa indicar o comando ou o procedimento e o que ficou sem cobertura.
5. **Revisão e operação.** Para mudanças de maior risco, obtenha uma revisão focada em defeitos concretos. Para entrega operacional, documente uma verificação de fumaça, sinais de erro e recuperação. Mantenha produção, mudanças irreversíveis e custos externos sob a autorização aplicável.
6. **Melhoria.** Transforme falhas repetidas em uma verificação específica, melhoria de documentação ou ajuste de skill. Refaça o experimento sob condições comparáveis antes de adotar o ajuste para toda tarefa.

O padrão Agent Skills descreve como o agente carrega metadados, instruções e referências conforme a necessidade. A descrição deve induzir a escolha certa, enquanto exemplos, métricas e instruções longas podem ficar em arquivos separados. [Especificação Agent Skills](https://agentskills.io/specification#progressive-disclosure)

## Cobertura por tipo de projeto

| Projeto | Caminho inicial | Evidência mínima ilustrativa |
| --- | --- | --- |
| Site público ou portfólio | UX, frontend e publicação. Acrescente SEO conforme a superfície pública. | Fluxo principal em navegador, viewport móvel, teclado e falhas relevantes de carregamento. |
| SaaS, dashboard ou e-commerce | Produto, UX, frontend, API, dados e QA. Acrescente AppSec a fluxos de autenticação, permissões e pagamentos. | Uma jornada completa, validação no backend e persistência comprovada. Autorização testada com contas separadas quando aplicável. |
| API, CLI ou biblioteca | Contrato, compatibilidade, implementação e documentação do consumidor. | Smoke test pela entrada normal. Em CLI, confira códigos de saída e tratamento de argumentos. |
| Mobile, desktop ou jogo | Descubra primeiro o SDK, o empacotador e o ambiente em que o usuário executará o projeto. | Build para o alvo escolhido e interação real em dispositivo, emulador ou runtime quando disponível. |
| Dados e automação | Esquemas de entrada e saída, reexecução, tratamento de duplicados e observabilidade. | Fixture reprodutível, execução repetida, recuperação após falha e resultado esperado. |
| Produtos com IA | Estabeleça um conjunto pequeno de exemplos e um critério por caso. Separe avaliação da geração quando necessário. | Casos de sucesso e limites, custo e latência observados, registro de versão do modelo e das instruções. |
| Projeto legado | Preserve o stack e capture o comportamento anterior antes da mudança. | Teste que exercita a regressão e verificação de compatibilidade com dados e clientes existentes. |

“Full stack” é a cobertura do fluxo completo onde ele existe. Em uma biblioteca, por exemplo, o ponto de entrada verificável é a API consumida por outro programa. Em um SaaS, é a operação do usuário atravessando interface, backend e dados.

## Segurança de skills e usuários

O **Skill Scanner da Cisco** é uma ferramenta pesquisada que corresponde à proteção descrita pelo usuário. A separação útil para este produto é entre verificação estrutural de `SKILL.md`, auditoria de segurança do pacote e avaliação de comportamento do agente no uso. Um validador sintático responde se os metadados e nomes seguem o formato. Um scanner auxilia a revisar a procedência e o conteúdo. Testes com tarefas pequenas mostram se a skill se ativa e produz a evidência esperada. [Cisco Skill Scanner](https://cisco-ai-defense.github.io/docs/skill-scanner) · [Validação em Agent Skills](https://agentskills.io/specification#validation)

Sequência proposta para adoção de skills de terceiros:

1. Baixe em uma pasta de revisão fora dos diretórios de descoberta. Use revisão fixa e registre a licença.
2. Verifique os arquivos incluídos e referências. Trate textos, scripts e exemplos como dados a inspecionar. Examine executáveis, hooks, acesso a credenciais e rede antes de ativar.
3. Execute primeiro a análise local. Escolha uma política clara para achados e registre resultados e justificativas. Analise manualmente os achados que impedem promoção antes de considerar o pacote utilizável.
4. Instale somente o arquivo ou pacote revisado, mantendo origem e hash. Atualizações recebem nova revisão. Segredos e conteúdo de projetos ficam no ambiente do usuário durante a análise local.
5. Teste a descoberta e uma tarefa controlada após ativar. Revise novamente quando a skill, suas dependências ou o mecanismo de execução mudar.

## Como medir a evolução

Compare a base anterior a uma configuração candidata com as mesmas tarefas, critérios, versão do modelo, revisão do projeto e ambiente. Faça novas rodadas quando houver variabilidade. Registre resultados por tarefa e por classe de complexidade, incluindo falhas e cancelamentos.

| Métrica | Registro |
| --- | --- |
| Aceite funcional | Critérios atendidos sobre os aplicáveis, com indicação dos obrigatórios. Falha obrigatória conta como tarefa rejeitada. |
| Tempo | Do início até a primeira entrega aceita. Inclua repetição de verificações e tempo do usuário. |
| Consumo | Tokens de entrada e saída e consumo do plano quando disponível. Registre cache separadamente e inclua subagentes. |
| Autonomia útil | Intervenções humanas por tarefa, separando decisão de produto, aprovação de risco e recuperação de falha. |
| Qualidade da revisão | Achados únicos confirmados, regressões detectadas e falsos positivos avaliados. |
| Continuidade | Tentativas para retomar após interrupção e capacidade de identificar a próxima tarefa e a evidência anterior. |
| Proteção na instalação | Pacotes limpos, bloqueados e encaminhados para revisão. Simule ausência do scanner, falha de análise e colisão de nomes. |

A métrica principal proposta é **tempo, consumo e intervenções por tarefa aceita**. Uma execução curta com aceite reprovado merece diagnóstico. Ganho no volume de saída do terminal deve ser registrado à parte do uso total do modelo.

## Próximos experimentos

1. **Retomada e fila.** Crie três tarefas com dependências em um projeto temporário. Interrompa a segunda, reinicie a sessão e confira se o registro preserva os resultados anteriores e impede que a terceira seja tratada como pronta indevidamente.
2. **Jornada full stack.** Em um repositório descartável com dados fictícios, peça uma operação que atravesse interface, API e persistência. Compare execução principal com principal mais QA em termos de regressões encontradas, latência e custo. Guarde os comandos e o resultado do teste de navegador.
3. **Portabilidade.** Teste o mesmo fluxo em um site estático, um serviço Python ou PHP e um CLI sem navegador. Confirme que o kit usa comandos apropriados a cada tipo e que a preparação ocorre sem alterar um repositório existente fora do escopo.
4. **Proteção de skills.** Use uma skill mínima válida, uma com metadados inválidos e outra com arquivo executável não revisado. Confira decisão, motivo, estado da instalação e preservação de arquivos anteriores. Compare as decisões do scanner com inspeção manual.
5. **Economia de contexto.** Execute a mesma mudança de texto e uma mudança que envolva mais de uma camada. Compare a leitura inicial, o tamanho das saídas e o retrabalho. Se mais especialistas aumentarem o custo em uma classe de tarefa sem melhorar seu aceite, use o caminho direto nessa classe.

