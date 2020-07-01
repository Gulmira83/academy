#!/usr/bin/env bash

wget --quiet "https://raw.githubusercontent.com/fuchicorp/common_scripts/bugfix/example/set-environments/terraform/google-set-env.sh" \
  -O set-env >/dev/null
source 'set-env' "$@"
rm -rf "set-env"
