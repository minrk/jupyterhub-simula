#!/bin/bash
# install jupyterhub, dependencies
# run me with sudo
set -e

# apt-get update && apt-get -y dist-upgrade
apt-get -y install \
  git build-essential \
  supervisor \
  realpath \
  ruby

export GROUP=jupyterhub
export ROOT="$(realpath $(dirname $0))"

# local nodejs install
export NVM_DIR=$ROOT/nvm
export NODE_VERSION=5
if [[ ! -d $NVM_DIR ]]; then
  curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
fi
source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
setcap 'cap_net_bind_service=+ep' "$(which node)"
# CHP
npm install -g configurable-http-proxy

# echo -e "export NVM_DIR=$NVM_DIR\nsource $NVM_DIR/nvm.sh\nnvm use default" > /etc/profile.d/nvm.sh
# source /etc/profile.d/nvm.sh

# Get local conda
wget -nc https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
test -d $ROOT/conda || bash Miniconda3-latest-Linux-x86_64.sh -b -p $ROOT/conda
export PATH=$ROOT/conda/bin:$PATH
hash -r
conda install -y sqlalchemy tornado
# Install JupyterHub itself:
pip install -r requirements.txt

# make it group-owned:
chgrp -R $GROUP $ROOT
chmod -R g+rw $ROOT

# add supervisor config
cp $ROOT/jupyterhub.conf /etc/supervisor/conf.d/
supervisorctl reread
supervisorctl update

touch /var/log/jupyterhub.log
chgrp $GROUP /var/log/jupyterhub.log
chmod g+rw /var/log/jupyterhub.log

# Build the singleuser docker image
docker build -t singleuser docker
