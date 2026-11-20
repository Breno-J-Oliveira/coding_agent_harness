#!/usr/bin/env bash
# Wrapper multiplataforma. Preview by default.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$ROOT/scripts/devkit.py" install "$@"
elif command -v python >/dev/null 2>&1; then
  exec python "$ROOT/scripts/devkit.py" install "$@"
else
  echo 'Instale Python 3.11+ e execute novamente.' >&2; exit 2
fi
