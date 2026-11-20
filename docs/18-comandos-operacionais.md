# 18 — Central de comandos e prompts de trabalho

> **Cole um prompt por tarefa no Codex**, em vez de colocar tudo em `AGENTS.md`. A equipe é uma lista de papéis possíveis, não 22 processos permanentes.

## A. Criar uma feature ponta a ponta

```text
Objetivo: [feature]. Usuário: [perfil]. Resultado esperado: [comportamento].
Analise o código relevante e escreva critérios de aceite verificáveis.
Escolha FAST/BALANCED/DEEP e explique em até 2 linhas.
Se houver trabalho realmente independente, delegue até 3 áreas delimitadas.
Implemente a menor fatia vertical: UI -> API -> dados, com testes.
Não altere autenticação, estrutura de banco ou deploy fora de escopo sem revisão.
Entregue diff resumido, comandos de teste REALMENTE executados, riscos e pendências.
```

## B. Tirar a cara de site gerado por IA

```text
Faça uma auditoria visual do site [rota] preservando a marca e o conteúdo.
Use design-quality-gate e, se instalados, Impeccable OU Unslop; não rode ambos sem motivo.
Abra a página num navegador, registre screenshots em 390/768/1440px e encontre
problemas específicos de hierarquia, espaçamento, tipografia, responsividade,
copy, contraste e estados interativos. Priorize 5 melhorias, implemente-as,
tire screenshots depois e verifique interações e regressões.
```

## C. Segurança do SaaS/API

```text
Audite SOMENTE o repositório e ambiente de teste autorizados.
Modele papéis, recursos, fronteiras de confiança e principais riscos.
Revise authn/authz, IDOR, isolamento de inquilinos, segredo, entrada de dados,
pagamento, upload, configuração e dependências conforme aplicável.
Use scanners instalados para gerar evidência, sem ataques a terceiros.
Classifique problemas com caminho/linha e teste reproduzível; corrija os de
maior risco e rode regressão. Não declare blindagem total.
```

## D. SEO de site público

```text
Audite somente URLs indexáveis: [URLs]. Verifique status HTTP, robots,
metadados, canonical, sitemap, hreflang se houver, schema JSON-LD,
links internos, renderização JavaScript, conteúdo e Core Web Vitals.
Use seo-audit e, se necessário, schema e site-architecture.
Não invente dados do Search Console. Entregue backlog P0/P1/P2 e evidência.
```

## E. Bug difícil

```text
Reproduza o bug [descrição], registre comando/ambiente/entrada/saída esperada.
Use diagnosing-bugs ou debugging-and-error-recovery, mas apenas um processo.
Formule hipóteses e teste uma por vez. Adicione teste de regressão que falha
antes da correção e passa depois. Evite refatoração não relacionada.
```

## F. Revisão final sem executar deploy

```text
Faça release-gate em modo somente leitura. Valide escopo, testes, lint,
typecheck, segurança aplicável, UX real, migrações, logs e rollback.
Entregue GO / NO-GO com comandos de evidência. Não rode deploy.
```

## G. Token budget / revisão do ecossistema

```text
Revise o AGENTS.md, a lista de skills e agentes disponíveis.
Encontre regras repetidas, descrições vagas e skills sobrepostas.
Sugira o menor conjunto de agentes/skills necessário para [tarefa], sem
instalar nada. Compare custo/contexto e risco. Proponha um handoff curto.
```
