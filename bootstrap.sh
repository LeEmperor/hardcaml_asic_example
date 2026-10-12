#!/bin/bash
set -eu

if ! command -v hardcaml-asic-flow >/dev/null 2>&1; then
    printf '%s\n' 'bootstrap: hardcaml-asic-flow is required on PATH.' \
        'Install a compatible hardcaml_asic provider via opam and activate its environment,' \
        'or explicitly refresh the development provider and source .dev/asic/current/activate.sh (see README.md).' >&2
    exit 127
fi

script_dir=${BASH_SOURCE[0]%/*}
if [[ $script_dir == "${BASH_SOURCE[0]}" ]]; then
    script_dir=.
fi
project_root=$(CDPATH= cd -- "$script_dir" && pwd -P)
exec hardcaml-asic-flow provision --toolchain "${TOOLCHAIN:-$project_root/_flow_tools}" "$@"
