# Validação do VibeCoder Engineering OS 4.0

Validação local no Windows em 20 de novembro de 2026, com Python 3.12, Git e Codex CLI 0.162.1.

| Verificação | Resultado |
| --- | --- |
| `python -B -m unittest discover -s tests` | 62 testes encontrados, 60 aprovados e 2 ignorados pela suíte. O teste da fila cobre dependência, falha, resultado `blocked` com saída zero, nova tentativa, evidência e aceite. |
| `python scripts/validate-package.py` | Validou 28 perfis de agentes, 12 skills essenciais, catálogo, versões e modelos da instalação base. |
| `python scripts/skillpacks.py recommend --target <raiz-do-Nexly>` | Detectou frontend, backend Node, banco e CI, incluindo os manifests em `apps/`. A recomendação é uma leitura do repositório. |
| Cisco Skill Scanner 2.3.2 | Analisou `code-simplification` e `observability-and-instrumentation`. Cada relatório apresentou apenas o aviso informativo `MANIFEST_MISSING_LICENSE`. Os arquivos MIT foram conferidos antes da instalação. |
| `python scripts/install-engineering-skills.py --apply` | Quatro skills disponíveis no escopo do usuário. A segunda execução preservou as quatro cópias existentes. |
| `engineering.py run` com Codex real | A conta rejeitou o modelo do perfil padrão e aceitou `gpt-6.1-sol`. O executor de terminal no sandbox do Windows ficou bloqueado. A fila capturou `blocked` no resultado estruturado e preservou a pendência. |
| `engineering.py retry`, `record` e `accept` | A tarefa descartável foi retomada. A evidência foi produzida fora da CLI do Codex, conferida em disco e aceita. O SHA-256 salvo na fila coincidiu com o SHA-256 do arquivo local. |

## Skills externas incluídas

As duas skills vieram da mesma revisão `8c99fa36d90068c82d547f7c12a9d67a3e95f4ee` de [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills/tree/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee). Os hashes individuais estão em [`third-party/skills-lock.json`](../third-party/skills-lock.json). Ambas são instruções e documentação em Markdown distribuídas com licença MIT. A versão de observabilidade inclui o checklist da mesma revisão e um link relativo ajustado para o pacote portátil.

O scanner foi executado com os analisadores locais padrão. A triagem combina esse resultado com verificação de origem, dependências, licença e conteúdo. [Cisco AI Defense Skill Scanner](https://cisco-ai-defense.github.io/docs/skill-scanner/)

## Limites observados

- O teste de escrita pela CLI ficou bloqueado pelo sandbox deste Windows. O registro externo e o aceite foram exercitados. A fila continua utilizável com execução no Desktop.
- A suíte usa fixtures para verificar o orquestrador. Falta um benchmark com uma entrega real de frontend, API e banco pelo executor autônomo.
- O consumo total de tokens varia com modelo, instruções carregadas e repositório. As tentativas de diagnóstico produziram métricas, mas a escrita bloqueada impede uma comparação justa de economia por entrega aceita.
- O nome VibeCoder Engineering OS foi escolhido editorialmente. A disponibilidade comercial da marca ainda precisa de verificação se houver lançamento público.
