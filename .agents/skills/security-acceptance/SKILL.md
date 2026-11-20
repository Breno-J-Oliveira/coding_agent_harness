---
name: security-acceptance
description: Use when implementing or reviewing authentication, authorization, payments, personal data, API endpoints, file uploads, dependencies, database access, or deployment security.
---
# Security acceptance gate

Authorized project review only. Never scan external hosts without explicit permission. Avoid production data.

1. Identify assets, users, roles, entry points and trust boundaries. Record likely failure scenarios.
2. Review authn/authz, least privilege, IDOR/BOLA, tenant isolation/RLS, input validation, output encoding, CSRF/XSS/SSRF, secrets, secure headers, dependencies, logging, rate limiting and error handling **as applicable**.
3. Ask for automated evidence: SAST, dependency/secret scan, permission unit/integration tests, CI configuration; tools require local installation and authorization.
4. Reproduce each finding in a local test or prove with a concrete code path. Mark uncertainty and potential false positives.
5. Fix root cause, add regression test, rerun relevant checks. Do not weaken controls to pass tests.
6. Never claim '100% protected' or 'fully hardened'. Unverified items stay open with severity and recommendation.

**Output:** finding, severity rationale, path/line, reproducer (safe, local), fix, evidence, residual risk.
