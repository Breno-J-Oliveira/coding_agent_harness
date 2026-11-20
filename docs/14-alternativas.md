# 14 — Outras recomendações e o que NÃO instalar de início

## Alternativas que vale conhecer

| Ferramenta | Por que olhar | Por que não está no núcleo |
|---|---|---|
| [Superpowers](https://github.com/obra/superpowers) | Workflows disciplinados de brainstorming, plano, execução e revisão | Pode conflitar com Addy/Matt se ativar muitos fluxos obrigatórios |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | Direção de arte, coerência visual e browser gate | Muito opinativa para produto interno e sites já bem definidos |
| [Cloudflare Security Audit Skill](https://github.com/cloudflare/security-audit-skill) | Auditoria multiestágio e verificação independente | Uso sob demanda, comparar com Trail of Bits e scanner real |
| [Sentry for AI](https://github.com/getsentry/sentry-for-ai) | Debug com evidência de produção | Não compensa em protótipo sem implantação |
| [Trivy](https://github.com/aquasecurity/trivy) | Docker/infra/dependências | É scanner, não skill. Ative em projetos com containers |
| [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) | Orçamento de SEO/a11y/performance | É pipeline; precisa configurar rotas/servidor |
| [Lefthook](https://github.com/evilmartians/lefthook) | Hooks rápidos e multiplataforma | Só quando o time precisa de gates locais |
| [Changesets](https://github.com/changesets/changesets) | Gestão de versões e changelogs em monorepos | Overhead em site de uma aplicação |
| [Vue Skills](https://github.com/antfu/skills) | Orientação para Vue 3 mantida por Anthony Fu | Use somente em projetos Vue |

## Opiniões de desenvolvedores: padrão observado

Em discussões de desenvolvedores no [r/codex](https://www.reddit.com/r/codex/comments/1wgvaa6/what_agent_skills_do_you_actually_find_useful_in/), algumas pessoas relatam preferir poucas skills estreitas (mapa do repositório, testes/bugfix, checklist de PR) e criticam instruções muito globais por consumir contexto. Esses relatos **não constituem prova estatística**; alinham-se, porém, à orientação oficial de disclosure progressivo da OpenAI.

## O que evitar

- Repositórios de “10.000 skills” instalados integralmente sem curadoria.
- Skills que executam scripts remotos sem explicação de permissões.
- Agentes que abrem PR/merge/deploy automaticamente sem controle humano.
- Vários sistemas concorrentes que reescrevem `AGENTS.md`, hooks e comandos globalmente.
- Segurança definida apenas por prompt: sem CI, testes negativos ou scanners.
- “SEO automático” que cria páginas massivas sem conteúdo original.
- Monitoramento que coleta logs com dados pessoais ou segredos.
- Métricas sintéticas de desempenho apresentadas como dados reais.
- Liberação de edição concorrente do mesmo arquivo por agentes diferentes.

## Como decidir sobre nova skill

Preencha a mini-ficha:

```markdown
### Skill candidata
- Repositório e mantenedor:
- Licença:
- Última atualização verificada:
- Problema real que resolve:
- Evidência/artefato produzido:
- Ferramentas/scripts executados:
- Permissões necessárias:
- Sobreposição com skill atual:
- Custo medido no benchmark:
- Decisão: instalar globalmente / no projeto / sob demanda / rejeitar
```
