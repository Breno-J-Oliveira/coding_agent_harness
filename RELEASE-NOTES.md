# VibeCoder Engineering OS 4.0

**20 de novembro de 2026.** Esta edição acrescenta uma fila de trabalho persistente, triagem de skills com Cisco AI Defense Skill Scanner, detecção de stack em monorepos e quatro skills. Consulte o [guia](docs/36-engineering-os.md) e a [validação](docs/37-validacao-v4.md).

## Histórico da edição 3.0

**Data:** 2026-11-12  
**Compatibilidade:** Python 3.11+ para instalação; Codex Desktop/CLI para uso; Node 22.20+ e Git apenas para skills remotas.

## O que muda

- **21 packs especializados**, aplicáveis individualmente ou recomendados pela detecção de stack.
- **49 skills próprias novas**, mantidas neste repositório, com fluxos específicos e referências de documentação.
- **55 skills remotas distintas** catalogadas, com fonte e nome; downloads sob demanda.
- Instalação em **projeto** por padrão e opção global, com preservação de arquivos pré-existentes e auditoria SHA-256.
- Comandos `list`, `recommend`, `plan`, `install`, `audit`, `uninstall` e `validate` em `scripts/skillpacks.py`.
- Plugins oficiais Sentry/Stripe/Cloudflare e Impeccable/Playwright indicados como opcionais, sem ativação silenciosa.
- Fonte atualizada para skills de Next.js (`vercel/next.js`), evitando coleção antiga.
- Os 28 agentes e 12 skills essenciais da v2 continuam disponíveis sem migração destrutiva.

## Instalação rápida

```bash
python scripts/skillpacks.py list
python scripts/skillpacks.py recommend --target /caminho/do/projeto
python scripts/skillpacks.py plan --auto --target /caminho/do/projeto --with-external
python scripts/skillpacks.py install --auto --target /caminho/do/projeto --apply
```

## Testes

- 29 testes do instalador principal (legado)
- 17 testes de roteamento/ferramentas (legado)
- 13 testes de packs e proteção de arquivos (v3)
- Verificação de TOML, frontmatter do catálogo e links internos

**59 testes de unidade/integridade locais.** Eles não validam o carregamento dos plugins externos ou downloads em uma máquina do usuário.

## Limites

O número de downloads e sua confiabilidade dependem dos mantenedores. A camada de skills não oferece blindagem total de segurança nem garantia de 90% de redução dos tokens de sessão. Testes de browser e conexão com fornecedores precisam ser executados no ambiente do usuário, quando aplicáveis.
