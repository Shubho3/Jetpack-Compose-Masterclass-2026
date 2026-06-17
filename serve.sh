#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Jetpack Compose Masterclass — serving at http://localhost:8000 (Ctrl+C to stop)"
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
"$PY" build-site.py
"$PY" -m http.server 8000
