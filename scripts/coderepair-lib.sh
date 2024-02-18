#!/bin/bash

# Bash library for controlling the CodeRepair build and environment

# ASSUMPTIONS:
#   - repo root does not move

############################################
# Variables
############################################

export REPO_ROOT="$(cd ${SCRIPT_DIR} && git rev-parse --show-superproject-working-tree --show-toplevel | head -1)"/src

############################################
# Help
############################################

coderepair-help() {
    cat <<'_EOF_'
-------------------------------------------------------------
coderepair-lib: a collection of bash functions to ease development
-------------------------------------------------------------

    Running CodeRepair:
        coderepair run: ------------- Run the CodeRepair debugging program
    
    Building and Installing:
        coderepair install: --------- Install Python dependencies and setup project

    Other:
        coderepair -h|--help: ------------ Prints this help message

Happy developing!

_EOF_

    [[ ${#} -eq 0 ]]
}

############################################
# Running CodeRepair
############################################

coderepair-run() {
    local HELP="""\
Run the CodeRepair debugging program

Syntax: coderepair-run [-h]
----------------------------------------------
    -h                  Print this help message
"""

    python3 "${REPO_ROOT}"/main.py "${@}"
}

############################################
# Aliasing CodeRepair
############################################

coderepair() {
    case "$1" in
        "-h"|"--help") coderepair-help ;;
        "run") coderepair-run "${@:2}" ;;
        *) echo "Unknown command. Run 'coderepair -h' for usage." ;;
    esac
}