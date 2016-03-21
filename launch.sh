#!/bin/bash
set -e


HERE="$(dirname $0)"
source "$HERE/env"

# add nvm to PATH
export NVM_DIR="$HERE/nvm"
source $NVM_DIR/nvm.sh
nvm use default

# add conda to PATH
export PATH="$HERE/conda/bin:$PATH"
hash -r

# launch
exec jupyterhub $@
