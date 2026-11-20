---
name: release-gate
description: Use before a PR merge, staging release, production deployment, or user-facing delivery to verify code quality, tests, security checks, rollback, observability, and acceptance criteria.
---
# Release gate

1. Read user acceptance criteria and project release standards. Ask if deployment is not authorized.
2. Check diff scope; build, lint, typecheck, unit/integration/E2E results; report exact commands actually run.
3. Verify applicable security and privacy gates, schema migration plans and rollback procedures.
4. Verify web UI visually on target devices and, for public/indexable sites, SEO/performance checks. Mark N/A with reasons.
5. Review whether the product/customer representative's acceptance cases were exercised with real functionality. Distinguish mocks and simulated flows.
6. For release-risk changes, insist on human approval; do not publish automatically.
7. Produce short go/no-go: passing evidence, failed checks, unverified checks, deployment plan, rollback trigger and owner.

**Never** write 'passed' when a tool could not execute. Use blocked/unverified instead.
