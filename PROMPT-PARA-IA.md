# Instalação inteligente das especialidades (v3.0)

> **Se o usuário pedir para instalar o Dev Kit completo**, siga `AGENTS.md`, faça diagnóstico da base, instale o perfil apropriado com backup e depois escolha skills por projeto. Evite instalar as 55 externas globalmente. Esta instrução não substitui autorização explícita para downloads, scripts remotos, plugins e hooks.
>
> 1. `python scripts/skillpacks.py validate` e `python scripts/skillpacks.py list`.
> 2. `python scripts/skillpacks.py recommend --target CAMINHO_DO_PROJETO`; valide a stack e suas dependências reais.
> 3. `python scripts/skillpacks.py plan --auto --target CAMINHO_DO_PROJETO --with-external` e apresente o inventário para revisão.
> 4. `python scripts/skillpacks.py install --auto --target CAMINHO_DO_PROJETO --apply` instala skills locais sem rede.
> 5. Se o usuário tiver autorizado downloads, execute `install --packs PACK1 PACK2 --with-external --apply` só para as skills adequadas; não execute hooks e plugins sem revisão e consentimento específico.
> 6. Finalize com `python scripts/skillpacks.py audit --target CAMINHO_DO_PROJETO` e testes pequenos de descoberta de skills no Codex. Não declarar execução bem-sucedida apenas por copiar arquivos.

---

# PROMPT PARA IA — INSTALAÇÃO DO VIBECODER DEVKIT 2.0

Copie para um Codex com acesso ao repositório local. Escolha o perfil conforme seu objetivo:

> **Missão:** Instale o VibeCoder DevKit profissional para o meu ambiente de desenvolvimento, sem alterar projetos nem configurações privadas sem necessidade.
>
> 1. Leia `AGENTS.md`, `README.md`, os catálogos em `catalog/` e o plano de atualização em `docs/26-upgrade-audit-uninstall.md`.
> 2. Rode o diagnóstico `python scripts/devkit.py doctor`, verifique plataforma e dependências. Me mostre o resultado sem expor secrets ou informações de configuração sensíveis.
> 3. Escolha comigo o perfil `core`, `web`, `security` ou `full` (use `web` quando objetivo é SaaS/site). Rode `python scripts/devkit.py plan --profile PERFIL --with-skills --with-tools --with-design` e mostre a lista exata de downloads e alterações.
> 4. Se eu já autorizei explicitamente a instalação, execute `python scripts/devkit.py install --profile PERFIL --scope global --apply`. Instale skills, design e CLIs externas somente se eu tiver solicitado (`--with-skills`, `--with-design`, `--with-tools`). Não instale hooks de terceiros sem minha aprovação separada.
> 5. Preserve meu modelo principal, provider, ambiente, MCPs, projetos confiáveis, AGENTS e chaves. Nunca invente IDs de modelos. Instalação por projeto requer `--scope project --target CAMINHO`.
> 6. Execute `python scripts/devkit.py audit`; valide formato dos agentes e skills, e peça uma tarefa real pequena para confirmar descoberta no Codex.
> 7. Para economia de tokens, explique RTK e seu hook como opção separada. Use `scripts/route-task.py` e `scripts/token-report.py` para decisão/medição. Não prometa 90% de economia sem medição controlada.
> 8. Entregue relatório curto com instalado, testado, pendente, conflitos preservados, fontes externas e `uninstall` como reversão.

## Exemplos rápidos

```bash
python scripts/devkit.py doctor
python scripts/devkit.py plan --profile web --with-skills --with-tools --with-design
python scripts/devkit.py install --profile web --apply --with-skills --with-tools --with-design
python scripts/devkit.py audit
python scripts/devkit.py uninstall                 # apenas prévia
```

> **Segurança:** se a intenção de instalar ou baixar ferramentas não estiver clara, execute apenas o plano sem modificar o computador.
