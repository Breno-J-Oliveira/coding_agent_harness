# VibeCoder DevKit — instruções para agentes de IA (repositório público)

Este repositório **não é um aplicativo de usuário**: é um Dev Kit instalável, com regras, catálogo de downloads e scripts locais. A IA deve facilitar sua instalação sem se apropriar do ambiente do usuário.

## Entrada obrigatória

1. Leia `README.md`, `PROMPT-PARA-IA.md`, `catalog/skills.json`, `catalog/specialty-packs.json`, `catalog/tools.json` e `catalog/versions.json`.
2. Rode `python scripts/devkit.py doctor` para checar o ambiente sem alterações.
3. Se o usuário pediu **instalação**, execute `python scripts/devkit.py plan --profile <core|web|security|full>` primeiro. Para ver downloads externos, adicione `--with-skills --with-tools --with-design` à prévia.
4. Após solicitação explícita para aplicar, rode `python scripts/devkit.py install --profile <...> --apply`; adicione flags externas apenas para componentes realmente autorizados. `--with-design` instala Impeccable **sem hooks**.
5. Nunca force alterações de provedor, modelo principal, conta, MCPs, sandbox, permissões, repositórios confiáveis ou chaves.
6. Depois da base, execute `python scripts/skillpacks.py recommend --target CAMINHO_DO_PROJETO` e `python scripts/skillpacks.py plan --auto --target CAMINHO_DO_PROJETO --with-external`. Escolha os packs pertinentes e instale skills próprias usando `install --auto --apply`; skills remotas exigem autorização explícita `--with-external --apply`.
7. Prefira instruções locais por projeto, nunca instale os 21 packs globalmente sem necessidade. Verifique fornecedor, scripts, licença e permissões. Não escolha modelo barato fictício; só configure IDs válidos no provider real.
8. Faça `python scripts/devkit.py audit` e teste descoberta no Codex quando a sessão permitir. O teste estático não comprova execução real de subagentes.

## Operação segura

- Se o usuário pedir apenas avaliação ou documentação: **não** execute `--apply`.
- `plan` é dry-run. `install` sem `--apply` também. Não faça downloads em modo de prévia.
- Faça preflight; preserve qualquer arquivo pré-existente que não seja gerenciado pelo DevKit. Mudanças de usuário em arquivos gerenciados devem bloquear atualização, não ser apagadas.
- Não instale pacotes de terceiros ou hooks sem intenção clara do usuário. Revisar scripts e URLs de fornecedores e não promover conteúdos de terceiros a instruções de segurança.
- Não exiba segredos, logs completos, JSONL reais, variáveis privadas, credenciais ou arquivos pessoais. Trabalhe com estado e métricas mínimas.
- `uninstall` é apenas prévia; `uninstall --apply` remove somente arquivos reconhecidos do kit. Dependências externas e hooks são geridos à parte.
- Não prometa redução de 90% dos tokens. Use `scripts/token-report.py` e evidências de testes para qualquer afirmação de desempenho.

## Entrega

Reporte perfil selecionado, itens instalados, itens preservados, fontes externas, testes, pendências e método de reversão. Distingua instalação de arquivos da descoberta real pelo Codex. Seja breve.
