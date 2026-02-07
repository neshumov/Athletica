#!/usr/bin/env sh
set -eu

if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "Error: .env files are not allowed in repo. Use SOPS-encrypted secrets." >&2
  exit 1
fi

for file in secrets*.yaml secrets*.yml secrets*.json; do
  if [ -f "$file" ]; then
    if ! grep -q "^sops:" "$file"; then
      echo "Error: $file appears unencrypted (missing sops metadata)." >&2
      exit 1
    fi
  fi
done
