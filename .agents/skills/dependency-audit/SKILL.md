---
name: dependency-audit
description: Revisar dependências, licenças, instalação de pacotes e atualização de vulnerabilidades; não instalar automaticamente.
---

# dependency-audit

1. Leia manifests e lockfiles, e identifique scripts de pós-instalação e fontes externas.
2. Use ferramentas locais aprovadas para advisories e SBOM; não envie segredos.
3. Classifique por versão afetada, exposição, severidade, compatibilidade e confiança da fonte.
4. Proponha atualização mínima, testes e plano de reversão.
5. Distinguir CVEs aplicáveis de avisos genéricos e resultados não comprovados.
