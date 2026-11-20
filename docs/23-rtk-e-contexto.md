# 23 — RTK e engenharia de contexto

**RTK (Rust Token Killer)** filtra e comprime saídas de terminal antes de entrarem no contexto. É uma ferramenta real, não uma skill de texto. Consulte [repositório](https://github.com/rtk-ai/rtk) e [instalação](https://www.rtk-ai.app/docs/getting-started/installation/).

## Instalar

Windows:

```powershell
winget install -e --id rtk-ai.rtk
rtk --version
rtk gain
# Veja antes de instalar integração com o Codex:
rtk init -g --codex --dry-run
```

macOS/Linux com Homebrew, se disponível:

```bash
brew install rtk
rtk --version
rtk gain
rtk init -g --codex --dry-run
```

Para instalar hook Codex com backup por meio do DevKit (RTK já deve estar no PATH):

```bash
python scripts/devkit.py install --profile core --apply --with-rtk-hook
```

**Não habilite hook automaticamente quando já houver hooks desconhecidos**. O DevKit imprime uma prévia e faz backup de arquivos de hook conhecidos antes da mudança. Revise o comando e o destino; hooks são código executável. Se a instalação via winget mudou PATH, reinicie o terminal primeiro.

## O que RTK economiza

Saídas de `git status`, `git diff`, buscas, testes e logs contêm texto redundante. O RTK gera versões sucintas sem perder o status essencial em tarefas comuns. Exemplos relatados pelos mantenedores podem atingir grandes reduções de saída, mas os resultados variam. Em caso de erro, falha de segurança ou dúvida, **obtenha a saída original completa** para não perder evidências.

## Outras quatro reduções de contexto

1. Prefira `rg -n 'simbolo' src/` a copiar um diretório inteiro.
2. Use `python scripts/smart-read.py arquivo --find termo --max-lines 40` para ler só o necessário.
3. Execute lint/testes em CLI e entregue ao agente apenas sumários + caminho do log completo.
4. Retenha planos e decisões persistentes em arquivos curtos por projeto, sem repetir informações em cada prompt.

Evite adicionar camadas de resumo e agentes novos sem medir: cada operação de síntese usa tokens adicionais. O orçamento correto é **custo por tarefa aceita**, não o número de agentes ou porcentagem de compressão isolada.

## Medição

`rtk gain` informa economias estimadas em saídas de comandos que passaram pelo RTK. Para medir o custo total, some tokens do modelo principal, dos subagentes, cache e correções. Compare execução A/B com os mesmos cenários, testes de regressão e resultados. Também acompanhe latência, falsos positivos e casos em que a compressão ocultou detalhes relevantes.
