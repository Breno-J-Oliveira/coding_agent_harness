# VibeCoder Engineering OS 4.0

Um **ambiente de engenharia de software com agentes** reúne os papéis da equipe, as instruções que cada papel usa e um fluxo verificável para entregar software. *Agentic engineering harness* é a categoria técnica mais específica. VibeCoder Engineering OS é o nome editorial escolhido para esta edição.

## Primeiros passos

Em uma nova máquina, instale a base local com `python scripts/devkit.py install --profile full --apply` após revisar `plan --profile full`. Em uma instalação que já tem a base, use apenas o instalador complementar:

```powershell
python scripts/install-engineering-skills.py
python scripts/install-engineering-skills.py --apply
```

Para limitar a ativação a um projeto, inclua `--target C:\Projetos\meu-app`. O instalador complementar pula nomes já presentes no destino.

Abra a pasta do projeto no Codex e peça `Use $engineering-delivery para transformar este objetivo em uma entrega verificável e execute o que estiver dentro do escopo`. Em um projeto existente, o ponto de partida é o comportamento atual e a stack detectada. Em um projeto novo, defina quem usa, qual fluxo entrega valor e como provar que ele funciona, antes de escolher infraestrutura.

O pacote inclui a base de 28 perfis de agentes, 12 skills essenciais, 49 especialidades por projeto e quatro skills adicionadas nesta edição. `engineering-delivery` coordena as etapas, `skill-intake-review` orienta a triagem de skills, `code-simplification` ajuda a reduzir complexidade e `observability-and-instrumentation` orienta logs, métricas e alertas. Os perfis apoiam produto, design, arquitetura, frontend, backend, dados, QA, segurança, entrega e operação. O orquestrador escala o esforço pela tarefa, com um responsável por área de edição.

## Fila de trabalho

Use Python 3.11+, Git e, para executar, Codex CLI autenticado. Os comandos abaixo são executados na pasta do kit. O projeto de exemplo precisa ser um repositório Git que você controla. Guarde a fila fora dele, em uma pasta privada.

```powershell
$fila = Join-Path $env:USERPROFILE 'Documents/projeto-fila.json'
python scripts/engineering.py --board $fila init --project 'C:\Projetos\meu-app' --goal 'Entregar cadastro com validação'
python scripts/engineering.py --board $fila add cadastro --phase backend --title 'Construir o cadastro' --acceptance 'Cadastro válido persiste e campos inválidos não gravam dados'
python scripts/engineering.py --board $fila add jornada --phase qa --title 'Validar o cadastro pela interface' --acceptance 'Concluir o cadastro pelo navegador e conferir o resultado persistido' --after cadastro
python scripts/engineering.py --board $fila next
python scripts/engineering.py --board $fila run
python scripts/engineering.py --board $fila status
python scripts/engineering.py --board $fila accept cadastro --evidence 'C:\Projetos\evidencias\cadastro.md'
```

`run` inicia uma sessão Codex para a próxima tarefa elegível, usando o sandbox de edição do workspace e um limite de tempo. O prompt recebe objetivo, critérios e pistas de stack. A saída JSONL e os erros ficam em uma pasta irmã da fila. Log de execução pode conter trechos privados do projeto. Trate-o como artefato local.

Saída zero com resultado estruturado `ready` coloca a entrega **em revisão**. O aceite registra a evidência revisada pelo responsável e libera dependências. Um resultado `blocked`, timeout ou falha do executor pede diagnóstico. Use `retry ID` após corrigir a causa. Depois de uma interrupção abrupta, confirme que o processo anterior terminou antes de remover a trava da fila. O progresso pode continuar entre sessões. Publicação, produção e custos dependem da autorização da tarefa.

O executor parte de um worktree limpo por padrão. Use `run --allow-dirty` quando as mudanças pendentes foram revisadas e fazem parte do trabalho que a próxima tarefa deve preservar. O aceite registra o SHA-256 da evidência, e o desenvolvedor continua responsável pela avaliação do conteúdo.

O executor segue o modelo configurado no Codex. Se a conta rejeitar esse modelo, use `run --model MODELO` com um modelo disponível na sua conta.

Em execuções dedicadas, `run --minimal-config --model MODELO` mantém a autenticação e as instruções do projeto, mas deixa de carregar o `config.toml` pessoal. Use somente quando as regras obrigatórias do projeto e da organização estiverem disponíveis para a sessão. A economia depende do ambiente e deve ser medida por entrega aceita.

Também é possível executar a próxima tarefa no Codex Desktop. Consulte `next`, execute a tarefa no projeto, guarde a evidência e use `record ID --evidence CAMINHO` para encaminhá-la à revisão. Se uma tentativa na CLI ficou em falha, use `retry ID` para recolocá-la na fila antes de registrar a entrega do Desktop. O aceite segue o mesmo comando.

## Do produto à operação

| Etapa | Responsável sugerido | Critério de saída |
| --- | --- | --- |
| Produto | Product Owner | Problema, usuário, escopo e aceite definidos |
| Design | UX / UI | Fluxo, estados e comportamento responsivo verificáveis |
| Arquitetura | Arquiteto / Tech Lead | Stack, limites e contratos registrados quando a decisão exigir |
| Implementação | Frontend, backend e dados | Uma jornada completa funciona com persistência e autorização aplicáveis |
| QA e segurança | QA, integração e AppSec | Verificações reais nos caminhos de sucesso e falha |
| Entrega | DevOps / Release Manager | Build, verificação de ambiente e recuperação definidos |
| Operação | Observabilidade | Logs úteis, sinais de falha e rotina de triagem |

| Tipo de projeto | Primeiro recorte | Evidência de maior valor |
| --- | --- | --- |
| Site público | Página, navegação e conversão | Navegador, teclado, estados mobile e indexação |
| SaaS | Jornada com interface, API e dados de teste | Integração, persistência e permissões entre contas |
| API ou integração | Operação com contrato e erros | Integração, timeout e repetição idempotente quando aplicável |
| CLI ou biblioteca | Comando ou API pública mínima | Saída, códigos de retorno e compatibilidade |
| Mobile ou desktop | Fluxo em um dispositivo suportado | Execução no dispositivo, permissões, recuperação |
| Dados ou IA | Entrada, transformação e saída | Fixture, avaliação reproduzível, privacidade e custo |
| Legado | Uma falha ou melhoria delimitada | Reprodução, regressão e compatibilidade |

`python scripts/skillpacks.py recommend --target CAMINHO` sugere packs pela presença de manifests. A decisão final considera o tipo de entrega e o stack real. Perfis, biblioteca e verificações podem ser combinados.

## Proteção de skills

A ferramenta é o **Cisco AI Defense Skill Scanner**. Nesta edição o modo local usa os analisadores padrão, sem habilitar análise LLM ou upload. A skill `skill-intake-review` orienta a revisão humana antes da ativação.

```powershell
uv tool install cisco-ai-skill-scanner==2.3.2
python scripts/skill-guard.py 'C:\Revisao\skill-candidata' --report 'C:\Revisao\relatorio.json'
```

`hold` indica que o pacote deve permanecer em revisão. `review` indica que o relatório está disponível para inspeção. Confira riscos, gatilhos, arquivos auxiliares, licença, proveniência e hashes. Regras estáticas têm cobertura limitada. A opção legada `--with-external` dos instaladores chama a CLI de terceiros diretamente, sem passar por esse fluxo.

Para avaliar ganho, use tarefas equivalentes e compare critérios atendidos, tempo, intervenção humana, retrabalho e uso de tokens observado. Registre falhas e contextos reiniciados além do melhor caso.
