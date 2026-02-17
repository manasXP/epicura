#!/usr/bin/env bash
# Add the epicura docs repo as a git submodule at docs/
# Run from the root of any epicura-* repository.

set -euo pipefail

DOCS_REMOTE="git@github.com:manasXP/epicura.git"
SUBMODULE_PATH="docs"

if [ -d "$SUBMODULE_PATH/.git" ] || [ -f "$SUBMODULE_PATH/.git" ]; then
  echo "Submodule already exists at $SUBMODULE_PATH — skipping."
  exit 0
fi

if [ ! -d ".git" ]; then
  echo "Error: not inside a git repository." >&2
  exit 1
fi

echo "Adding epicura docs submodule at $SUBMODULE_PATH ..."
git submodule add "$DOCS_REMOTE" "$SUBMODULE_PATH"
git commit -m "Add epicura docs as submodule

Links the shared documentation repo so developers have
full project docs available while working on this repo."

echo "Done. Docs submodule added at $SUBMODULE_PATH/"
