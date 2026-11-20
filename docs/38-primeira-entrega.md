# Da primeira ideia à entrega

## Prepare o projeto

Instale Git e Python 3.11 ou superior. Autentique-se no Codex ou no Claude Code pelo fluxo oficial do seu aplicativo. Este repositório fornece skills e ferramentas locais. O agente e a conta continuam sendo pré-requisitos.

```powershell
git clone https://github.com/Breno-J-Oliveira/coding_agent_harness.git
cd coding_agent_harness
$projeto = Join-Path $PWD '..\meu-produto'
New-Item -ItemType Directory -Path $projeto
git -C $projeto init
python scripts/bootstrap.py --target $projeto --engine both
python scripts/bootstrap.py --target $projeto --engine both --apply
```

Escolha `codex` ou `claude` para instalar em apenas um agente. O bootstrap preserva skills e instruções existentes. Para um projeto já iniciado, use a raiz que você mantém e dispense a criação da pasta e do Git. A sessão interativa pode abrir a pasta diretamente após a instalação.

Em um terminal Bash ou Zsh, use `projeto="$(pwd)/../meu-produto"`, `mkdir -p "$projeto"` e `fila="$HOME/meu-produto-fila.json"` no lugar das atribuições e da criação de pasta do PowerShell. Nos comandos seguintes, mantenha `"$projeto"` e `"$fila"` entre aspas. Em sistemas onde o executável se chama `python3`, use esse nome.

## Entregue a primeira jornada

Abra o projeto e invoque `$idea-to-release` no Codex ou `/idea-to-release` no Claude Code. Passe contexto de produto em linguagem simples.

> Quero um portal para clientes agendarem atendimentos de uma pequena empresa. O cliente vê horários livres e confirma um. A empresa vê a lista do dia. Use dados fictícios, desenvolva a primeira versão local e me mostre como testá-la, publicar e voltar à versão anterior.

O agente começa pelo menor fluxo que prova valor. A entrega ideal inclui a decisão de escopo, os arquivos implementados, a demonstração do fluxo e as verificações executadas. Confirme a pertinência de cada área ao tipo de produto.

| Etapa | Evidência esperada |
| --- | --- |
| Produto e UX | Público, problema, jornada e critérios para o fluxo principal e estados de erro. |
| Arquitetura e dados | Interfaces, regras de domínio, esquema e migração quando aplicáveis. |
| Frontend, API e integração | Jornada responsiva e acessível, validação, permissões e persistência na medida do produto. |
| QA e segurança defensiva | Testes de comportamento, falhas e permissões e verificação de build e lint disponíveis. |
| Release e operação | Instruções de executar, configurar, publicar e reverter. Smoke test e sinais de saúde proporcionais ao produto. |

## Rode a fila no Codex CLI

Use uma pasta de fila privada fora do projeto. O comando `start` define um contrato de MVP a partir da ideia. O Codex refina as decisões reversíveis durante `run`, trabalha no projeto e encerra em revisão ou indica o bloqueio que precisa resolver.

```powershell
$fila = Join-Path $env:USERPROFILE 'Documents/meu-produto-fila.json'
python scripts/engineering.py --board $fila start --project $projeto --idea 'Portal local de agendamentos para uma empresa'
git -C $projeto status --short
python scripts/engineering.py --board $fila run --timeout 1800
python scripts/engineering.py --board $fila status
python scripts/engineering.py --board $fila usage
```

O executor espera um worktree limpo. Para a pasta nova, inclua as configurações revisadas do bootstrap no commit inicial ou use `run --allow-dirty` após conferir todas as mudanças. O executor limita a sessão ao workspace com rede desabilitada. Quando o projeto precisa buscar dependências, prepare-as no ambiente autorizado antes de rodar ou use uma sessão interativa que possa pedir permissão. Em um sandbox indisponível, use `brief` na mesma fila, passe o contrato à sessão no Desktop ou Claude Code e registre as evidências com `record ID --evidence CAMINHO`. Use `retry ID` antes do registro se houve uma tentativa marcada como `failed`.

`accept ID --evidence CAMINHO` registra a revisão e libera dependências. As tarefas de entrega, segurança e operação exigem aceite humano. A entrada `usage` agrega tokens reportados em tentativas com logs e informa quantas ficaram sem medição. Trate esses logs como privados.

## Avance tarefas locais com verificação independente

Use `init` e `add` para montar entregas menores. Passe `--auto-verify` apenas para tarefas cujo critério pode ser conferido por um verificador independente. Em `advance`, forneça um script Python que você escreveu ou inspecionou, guardado fora do projeto. Ele recebe um JSON por stdin com os campos `project` e `task` e retorna zero quando suas verificações passarem. Use critérios concretos e exija falha para qualquer ID que o script não reconheça.

```powershell
python scripts/engineering.py --board $fila advance --verifier 'C:\Verificadores\meu-produto.py' --max-tasks 3 --max-seconds 1800 --max-tokens 80000
```

O verificador roda com as permissões da sua conta. Use código que você controla, valide os caminhos que ele inspeciona e trate a saída do agente como dados. Deixe a execução do código produzido e os testes da aplicação no sandbox da sessão. A fila preserva o hash do verificador e o recibo para cada aceite automático. Um verificador com falha deixa a tarefa em revisão. Sem um verificador ou sem `--auto-verify`, `advance` pausa para aceite após a entrega atual. A tarefa criada pelo `start` é revisada por uma pessoa.

O orçamento de tokens é checado **entre** tarefas. Uma sessão já iniciada pode ultrapassá-lo. Sem métricas, o lote pausa antes da tarefa seguinte. Para reduzir o consumo, comece com as quatro skills essenciais do bootstrap, use um agente principal e deixe catálogos, histórico e referências extensas para quando houver uma decisão que dependa deles. A comparação entre execuções exige mesma tarefa, modelo e critérios aprovados. Use `scripts/token-report.py` para comparar logs Codex de execuções equivalentes.

## Passe de pronto para publicar a publicado

Prepare variáveis pelo nome, ambiente-alvo, verificação de saúde e estratégia de reversão. Use [o roteiro de release](../workflow-skills/idea-to-release/references/release.md) para adaptar a checklist ao projeto. Autorize a ação e o ambiente de deploy na sessão interativa ou em um fluxo de CI próprio. Confirme o resultado no ambiente publicado antes de fechar a entrega.

[Skills no Codex](https://developers.openai.com/codex/skills) · [Skills no Claude Code](https://code.claude.com/docs/en/skills)
