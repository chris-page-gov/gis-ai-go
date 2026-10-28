#!/bin/sh
# Explicit invocation only: reviewed host Python and Git are prerequisites.
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$script_dir/environment.py" "$@"
