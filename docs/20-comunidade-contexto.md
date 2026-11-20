# 20 — Recomendações de desenvolvedores e engenharia de contexto

## Síntese da literatura técnica

A documentação oficial do Codex recomenda que skills usem **divulgação progressiva**: inicialmente o agente vê nome e descrição; o conteúdo é carregado sob demanda. A lista inicial tem limite de orçamento e pode omitir skills quando o conjunto é muito grande. Portanto, o catálogo deste repositório é **um menu**, não uma ordem para instalar tudo.

- [Codex — Build Skills](https://learn.chatgpt.com/docs/build-skills): documentação oficial sobre orçamento inicial de skills, gatilhos e criação.
- [OpenAI — Rethinking Skills and Prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): recomenda revisar instruções acumuladas e abandonar scaffolding redundante.
- [Matt Pocock — Skills for Real Engineers](https://github.com/mattpocock/skills): prioriza loops reproduzíveis de diagnóstico, teste e modelagem de domínio.
- [Addy Osmani — Agent Skills](https://github.com/addyosmani/agent-skills): propõe fluxo especificar → planejar → construir → verificar → revisar → entregar.

## Comunidade: sinais qualitativos

Relatos em [r/ClaudeCode sobre excesso de skills](https://www.reddit.com/r/ClaudeCode/comments/1t4cy2y/what_do_you_do_when_you_have_too_much_skills/) citam instruções conflitantes e consumo desnecessário de contexto. Em [discussões sobre gestão de contexto](https://www.reddit.com/r/ClaudeCode/comments/1w3d8oa/how_to_manage_context_better/), desenvolvedores mencionam sessões menores, handoffs e checagens do repositório.

Esses relatos são **anecdóticos, com amostras pequenas**, e não provam causalidade nem ganhos universais. Justificam **testar** uma organização mais enxuta, não garantir resultado.

Uma [análise independente de 12 sessões do Codex](https://lucianlabs.dev/en/notes/codex-token-xray-sessions/) sugere que saídas volumosas de ferramentas podem pesar mais no contexto do que os resumos de skills; amostra limitada. Um bom padrão operacional é evitar logs intermináveis, registrar erros completos em arquivo e devolver ao agente apenas trechos relevantes.

## Regras práticas

- Comece com 6–10 skills adequadas ao projeto, não 100.
- Tenha um workflow principal de especificação/review; não sobreponha cinco metodologias.
- Use prompts curtos com critérios claros e limites de escopo.
- Prefira testes determinísticos a agente garantindo verbalmente que funciona.
- Ao terminar, produza um handoff pequeno, com caminhos e comandos reais.
- Reavalie a seleção a cada 30–60 dias ou quando houver alteração significativa de framework.
