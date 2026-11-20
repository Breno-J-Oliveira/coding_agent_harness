---
name: threat-model
description: Projetar defesa antes de criar autenticação, permissões, pagamentos ou dados sensíveis; não afirmar blindagem total.
---

# threat-model

1. Desenhe os fluxos e fronteiras de confiança com ativos e atores.
2. Aplique STRIDE de forma proporcional à superfície existente.
3. Priorize BOLA/IDOR, sessão, secrets, SSRF, uploads e integrações conforme evidência.
4. Para cada ameaça, registre probabilidade, impacto, controle, teste negativo e responsável.
5. Somente valide exploração em ambientes autorizados e isolados.
