#!/usr/bin/env bash
# One-shot publish helper: run AFTER you create a GitHub account.
# Usage:  GITHUB_USER=<your-username> ./push.sh          # HTTPS (needs gh login or PAT)
#         GITHUB_USER=<your-username> REMOTE=git@github.com:USER/materials-mcp.git ./push.sh
set -euo pipefail

GH_USER="${GITHUB_USER:?set GITHUB_USER=<your github username>}"
REPO="${REPO_NAME:-materials-mcp}"
REMOTE_URL="${REMOTE:-https://github.com/${GH_USER}/${REPO}.git}"

cd "$(dirname "$0")"

# 1) create the remote repo if gh is authenticated (safe skip otherwise)
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  gh repo view "$GH_USER/$REPO" >/dev/null 2>&1 || \
    gh repo create "$GH_USER/$REPO" --public --description \
      "US construction material prices for AI agents — 33 FRED series via MCP, no API key" --source=. --remote=origin --push
  echo "pushed via gh (repo created + pushed)"
  exit 0
fi

# 2) fallback: plain git. Create an EMPTY repo on github.com first (no README), then:
git remote add origin "$REMOTE_URL" 2>/dev/null || git remote set-url origin "$REMOTE_URL"
git push -u origin main
echo "done -> $REMOTE_URL"
echo "next: submit to directories per docs/directories-submission.md"
