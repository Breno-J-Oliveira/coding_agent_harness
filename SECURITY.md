# Política de segurança do VibeCoder DevKit

O DevKit é um instalador local e uma coleção de instruções para agentes. **Não é** um mecanismo de blindagem universal. A versão 2.0 não reivindica auditoria de segurança independente dos scripts ou das fontes remotas.

Para relatar vulnerabilidade, abra preferencialmente um advisory privado no GitHub após publicar este repositório (Security > Advisories). Não compartilhe credenciais, hashes privados, URLs internas nem dados de terceiros em issues públicas.

Antes de executar downloads, revise `catalog/skills.json`, `catalog/tools.json` e `catalog/versions.json`. Execute `plan` e inspecione o resultado. `install --apply` é opt-in; RTK hook é uma decisão separada. Mantenha backups do seu `config.toml` e de `hooks.json` privados.

Limitações conhecidas: o kit não verifica criptograficamente o conteúdo das skills de terceiros obtidas do GitHub; o estado remoto não é pinado por commit. Atualizações de fontes externas devem ser revisadas e, quando necessário, executadas em sandbox.
