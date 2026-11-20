# 02 — Design profissional: tirar a “cara de IA” de interfaces

## O problema real

UI de baixa qualidade não se resolve só retirando gradientes roxos. Os sintomas incluem: hierarquia fraca, cards repetitivos, espaçamento irregular, fontes genéricas sem intenção, hero sem mensagem, iconografia inconsistente, CTAs pouco claros, estados ausentes e ausência de contexto da marca. **Não confundir gosto subjetivo com erro técnico**: um layout minimalista pode ser excelente.

## As quatro escolhas mais fortes

### 1. [Impeccable](https://github.com/pbakaus/impeccable) — recomendação central

Criado por **Paul Bakaus**. Foco em linguagem de design para agentes. Oferece `critique`, `audit`, `typeset`, `layout`, `adapt`, `polish`, `harden`, `optimize`, `animate`, `shape` e outros comandos. O detector encontra padrões de interface, e pode examinar código ou uma página renderizada. É o melhor ponto de partida quando se quer **construir e revisar** dentro do mesmo fluxo.

```powershell
# Revise o projeto e scripts do repositório antes de executar.
npx impeccable install --providers=codex --scope=project
# O Codex deve ser reiniciado; ative/aprove o hook em /hooks se aplicável.
# Exemplos de pedidos dentro do Codex:
# $impeccable init
# $impeccable critique the onboarding flow
# $impeccable layout the dashboard
# $impeccable polish the billing page
```

```powershell
# Auditorias determinísticas, depois de iniciar o servidor local:
npx impeccable detect src/
npx impeccable detect http://localhost:3000
```

Auditorias de URL podem detectar contraste/texto que não aparece só no scan de JSX/TSX. Detector não substitui WCAG, testes manuais ou revisão de copy.

### 2. [Unslop](https://github.com/heydamir/unslop) — visão de designer

Criado por **Damir Sokolovsky**. Analisa uma interface existente, lista sinais específicos de genericidade, propõe direção visual e corrige em passadas: espaçamento, cores, ícones, texto, tipografia, layout, detalhes, imagens e movimento. **Licença CC BY 4.0**, mantenha atribuição.

```powershell
npx skills add heydamir/unslop --skill unslop -a codex
```

**Quando escolher:** uma tela já funciona, mas sua aparência é pouco original. Não usar simultaneamente com outro sistema que queira impor design novo sem consolidar tokens.

### 3. [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — bibliotecas e decisões

Possui busca de diretrizes para estilos, fontes, paletas e padrões de UX por stack. Útil para criar design tokens coerentes e evitar escolhas aleatórias. O instalador é `ui-ux-pro-max-cli` e o executável `uipro`; a versão básica é aberta e existe oferta premium separada.

```powershell
npx ui-ux-pro-max-cli init --ai codex --dry-run
npx ui-ux-pro-max-cli init --ai codex
# para todos os projetos, consulte modo universal global:
# npx ui-ux-pro-max-cli init --ai universal --global
```

### 4. [Taste Skill](https://github.com/Leonxlnx/taste-skill) — direção de arte opinativa

Especialmente interessante para páginas institucionais/landing pages. Força briefing, hierarquia de seções, identidade mais marcada e checagens em resoluções diversas. Possui dependência de Node 22+ e navegador. **Não usar como framework obrigatório de produto inteiro**: pode impor estrutura inadequada a SaaS ou dashboards complexos.

```powershell
npx skills add Leonxlnx/taste-skill --skill design-taste-frontend -a codex
```

## Loop visual de qualidade (repetir até aprovação)

1. **Brief real**: negócio, usuário, tarefas, valores da marca, referências e o que NÃO fazer.
2. **Inventário visual**: tokens (cores, tipografia, espaço, raio, sombra, densidade), componentes e estados.
3. **Hierarquia**: a principal ação fica óbvia em 5 segundos? Existe contraste sem ruído?
4. **Implementação por área**: hero → navegação → conteúdo → forms → empty/error/success states.
5. **Auditoria de código**: Impeccable + Web Design Guidelines.
6. **Auditoria renderizada**: screenshot 390, 768, 1024, 1440 px; teclado, leitores de tela quando possível.
7. **Teste de fluxo**: usuário tenta uma tarefa sem explicação do criador; observar bloqueios reais.
8. **Refinar**: corrigir os 3 maiores problemas; repetir. Evitar alterar todas as telas de uma vez.

## Grade de espaçamento (ponto de partida, não lei)

Tokens sugeridos: `4, 8, 12, 16, 24, 32, 48, 64, 96` pixels. `space-2 = 8px`, `space-4 = 16px`, `space-6 = 24px`. Prefira gap consistente, grid explícito e limites de largura (`max-width`) definidos pelo conteúdo. Projetos densos (dashboards) pedem ritmos diferentes de landing pages editoriais.

## Matriz de revisão

| Dimensão | Perguntas de auditoria | Evidência |
|---|---|---|
| Identidade | Isso poderia ser de qualquer startup? Há sistema visual? | Screenshots lado a lado |
| Hierarquia | Onde olho primeiro? CTA principal é claro? | Teste de 5 segundos |
| Layout | Eixos alinhados? Espaçamento coerente? | Medidas e tokens CSS |
| Tipografia | Escala, linha, peso, contraste e hierarquia apropriados? | Zoom, viewport e computed styles |
| Conteúdo | Copy específica, concisa e verdadeira? | Revisão por produto/cliente |
| Estados | Loading, vazios, erros, offline, sucesso e permissão? | E2E e screenshots |
| Responsividade | Sem overflow, touch targets adequados, forms usáveis? | 390/768/1024/1440 |
| Acessibilidade | Teclado, foco, labels, contraste, motion? | axe + auditoria manual |
| Performance | Imagens dimensionadas, componentes eficientes? | Lighthouse + Web Vitals |

## Anti-padrões de implementação

- Proibir gradiente por princípio, em vez de perguntar se ele corresponde à marca.
- Aumentar animação sem testar `prefers-reduced-motion`.
- Criar fontes/cores novas a cada seção sem tokens.
- Usar screenshots como prova de acessibilidade.
- Resolver visual sem acertar estados e semântica do HTML.
- Gerar imagens pagas automaticamente sem consentimento.

## Padrão de prompt

> Analise só a rota `/dashboard`. Faça inventário de problemas visuais e UX, com evidências de screenshot a 390/1440 px. Preserve a identidade atual. Proponha três mudanças de alto impacto, implemente-as e mostre comparativo antes/depois. Valide teclado, foco, contraste, responsividade e testes. Não redesenhe outras páginas.

**Fontes:** [Impeccable](https://github.com/pbakaus/impeccable), [Unslop](https://github.com/heydamir/unslop), [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), [Taste Skill](https://github.com/Leonxlnx/taste-skill), [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills).
